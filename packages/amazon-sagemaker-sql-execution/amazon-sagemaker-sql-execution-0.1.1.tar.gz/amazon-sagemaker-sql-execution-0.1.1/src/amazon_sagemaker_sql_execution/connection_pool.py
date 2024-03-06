# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from typing import Dict, Optional

from amazon_sagemaker_sql_execution.utils.sql_connection_supplier_factory import (
    SQLConnectionSupplierFactory,
)

from amazon_sagemaker_sql_execution.connection import SQLConnection
from amazon_sagemaker_sql_execution.exceptions import ConnectionPoolError, ConnectionPoolFault
from amazon_sagemaker_sql_execution.utils.sql_connection_factory import (
    SQLConnectionFactory,
)

from amazon_sagemaker_sql_execution.utils.logging_utils import ServiceFileLoggerMixin
from amazon_sagemaker_sql_execution.utils.metrics.service_metrics import (
    get_log_file_location,
    InstanceAttributeMetricsContextMixin,
    add_metrics,
)

from amazon_sagemaker_sql_execution.utils.constants import MetricsConstants


class ConnectionPool(ServiceFileLoggerMixin, InstanceAttributeMetricsContextMixin):
    """
    Connection pool which maintains connections to all databases.

    Callouts:
    - This pool is NOT threadsafe.

    Todo: Look into existing implementations of connection pool to make the pool thread-safe, and use generic methods
    for cleaning up connections, re-using connections etc.

    """

    def __init__(self):
        """
        Connection can either be referenced by its name, or by its hash.
        """
        # connection_cache_by_hash: Dict[hash / name, connection]
        super().__init__()
        self._connection_cache: Dict[str, SQLConnection] = {}

    def log_source(self):
        return self.__class__.__name__

    @add_metrics(MetricsConstants.GET_OR_CREATE_CONNECTION_OPERATION)
    def get_or_create_connection(
        self,
        metastore_type: Optional[str] = None,
        metastore_id: Optional[str] = None,
        connection_parameters: Optional[Dict] = None,
        connection_name: Optional[str] = None,
    ) -> SQLConnection:
        """
        Creates and maintains a cache of connections.

        :param metastore_type:          GLUE / LOCAL_FILE etc
        :param metastore_id:            GLUE_ARN / FILE_PATH etc
        :param connection_parameters:   Customer provided connection params
        :param connection_name:         Customer provided connection identifier. If not provided, we will auto-generate.
        :return:
        """

        self.metrics_context.set_property("MetastoreType", metastore_type)
        self.metrics_context.set_property("MetastoreId", metastore_id)
        try:
            if connection_name:
                if connection_name in self._connection_cache:
                    self.metrics_context.set_property("ConnectionFromCache", 1)
                    return self._connection_cache[connection_name]
                else:
                    self.metrics_context.set_property("ConnectionFromCache", 0)
                    return self._create_connection(
                        connection_name,
                        metastore_type,
                        metastore_id,
                        connection_parameters,
                    )

            connection_hash = self._get_connection_hash(
                metastore_type, metastore_id, connection_parameters
            )
            if connection_hash in self._connection_cache:
                self.metrics_context.set_property("ConnectionFromCache", 1)
                return self._connection_cache[connection_hash]
            self.metrics_context.set_property("ConnectionFromCache", 0)
            return self._create_connection(
                connection_hash, metastore_type, metastore_id, connection_parameters
            )
        except Exception as e:
            self.error(f"Exception in get_or_create_connection connection {e}")
            raise e

    def _get_connection_hash(
        self,
        metastore_type: Optional[str] = None,
        metastore_id: Optional[str] = None,
        connection_parameters: Optional[Dict] = None,
    ):
        """
        Fetches all connections properties to generate a hash for uniquely identifying connection in the pool.
        This is required when a connection_name is not provided.
        """

        metastore_parameters = SQLConnectionFactory.get_connection_parameters_from_metastore(
            metastore_type, metastore_id
        )
        connection_supplier = SQLConnectionSupplierFactory().get_connection_supplier(
            SQLConnectionFactory.determine_connection_type(
                metastore_parameters=metastore_parameters,
                connection_parameters=connection_parameters,
            )
        )
        connection_properties = SQLConnectionFactory.get_final_connection_properties(
            metastore_parameters=metastore_parameters,
            connection_parameters=connection_parameters,
            connection_supplier=connection_supplier,
        )
        return connection_properties.__hash__()

    def _create_connection(
        self,
        connection_name: str,
        metastore_type: Optional[str] = None,
        metastore_id: Optional[str] = None,
        connection_parameters: Optional[Dict] = None,
    ) -> SQLConnection:
        conn = SQLConnectionFactory.create_connection(
            metastore_type, metastore_id, connection_parameters
        )
        self._connection_cache[connection_name] = conn
        return conn

    def list_connections(self):
        """
        :return: connection details.
        """
        return {k: str(v) for k, v in self._connection_cache.items()}

    def close_connection(self, connection_name: str):
        if connection_name not in self._connection_cache:
            raise ConnectionPoolError(
                f"{connection_name} does not correspond to any cached connections."
            )

        self._connection_cache[connection_name].close()
        self._connection_cache.pop(connection_name)

    def close_cached_connection(self, connection: SQLConnection):
        for k, v in self._connection_cache.items():
            if v == connection:
                self.close_connection(k)
                return

    def close(self):
        # Note we must extract keys to a list to avoid `RuntimeError: dictionary changed size during iteration`
        for key in list(self._connection_cache.keys()):
            try:
                self.close_connection(key)
            except Exception as e:
                raise ConnectionPoolFault(e) from e

    def __enter__(self):
        """
        Allow connection pool to be n
        :return:
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        # Return False to re-raise any potential exceptions
        return False

    def __del__(self):
        """
        This method is for additional safety.  We expect clients to always call `cleanup`.
        Note that if the python process is interrupted, `__del__` will NOT run.

        :return:
        """
        self.close()
