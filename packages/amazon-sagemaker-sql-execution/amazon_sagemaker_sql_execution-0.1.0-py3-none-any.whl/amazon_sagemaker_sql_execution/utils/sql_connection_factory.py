# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from typing import Dict, List

from amazon_sagemaker_sql_execution.sql_connection_supplier import SQLConnectionSupplier
from amazon_sagemaker_sql_execution.utils.metadata_retriever.BaseSQLFactory import (
    BaseSQLFactory,
)

from amazon_sagemaker_sql_execution.connection import SQLConnection
from amazon_sagemaker_sql_execution.exceptions import MissingParametersError
from amazon_sagemaker_sql_execution.models.sql_execution import (
    SQLConnectionProperties,
)
from amazon_sagemaker_sql_execution.utils.aws_secret_retriver import AWSSecretsRetriever
from amazon_sagemaker_sql_execution.utils.metadata_retriever.metadata_retriever_factory import (
    ConnectionMetadataRetrieverFactory,
)
from amazon_sagemaker_sql_execution.utils.sql_connection_supplier_factory import (
    SQLConnectionSupplierFactory,
)
from amazon_sagemaker_sql_execution.utils.metrics.service_metrics import add_metrics
from amazon_sagemaker_sql_execution.utils.metrics.service_metrics import (
    ClassAttributeMetricsContextMixin,
)
from amazon_sagemaker_sql_execution.utils.constants import MetricsConstants


class SQLConnectionFactory(BaseSQLFactory, ClassAttributeMetricsContextMixin):
    @staticmethod
    def factory_for_class_type():
        """
        Returns the type of objects produced by the factory.
        """
        return SQLConnection

    @staticmethod
    @add_metrics(MetricsConstants.SQL_CREATE_CONNECTION_OPERATION)
    def create_connection(
        metastore_type: str = None,
        metastore_id: str = None,
        connection_parameters: Dict = None,
    ) -> SQLConnection:
        """
        Creates a concreate connection instance.

        :param metastore_type:          GLUE / LOCAL_FILE_SYSTEM etc
        :param metastore_id:            GLUE_ARN / FILE_PATH etc
        :param connection_parameters:   The over-ridden connection params provided by customers.
        :return:
        """

        metastore_parameters = SQLConnectionFactory.get_connection_parameters_from_metastore(
            metastore_type, metastore_id
        )
        SQLConnectionFactory.metrics_context.set_property("MetastoreType", metastore_type)
        SQLConnectionFactory.metrics_context.set_property("MetastoreId", metastore_id)
        connection_type = SQLConnectionFactory.determine_connection_type(
            metastore_parameters=metastore_parameters,
            connection_parameters=connection_parameters,
        )

        SQLConnectionFactory.metrics_context.set_dimensions(
            [
                {
                    MetricsConstants.OPERATION_DIMENSION_NAME: MetricsConstants.SQL_CREATE_CONNECTION_OPERATION,
                    MetricsConstants.CONNECTION_TYPE_DIMENSION_NAME: connection_type,
                }
            ]
        )
        supplier = SQLConnectionSupplierFactory().get_connection_supplier(connection_type)

        final_connection_props = SQLConnectionFactory.get_final_connection_properties(
            metastore_parameters=metastore_parameters,
            connection_parameters=connection_parameters,
            connection_supplier=supplier,
        )

        connection = supplier.create_connection(final_connection_props)
        return connection

    @staticmethod
    def get_final_connection_properties(
        metastore_parameters: Dict = None,
        connection_parameters: Dict = None,
        connection_supplier: SQLConnectionSupplier = None,
    ) -> SQLConnectionProperties:
        """
        Returns final connection parameters from merging metastore connection parameters and customer overriden
        connection parameters.

        :param metastore_parameters: connection parameters obtained from metastore
        :param connection_parameters: customer overriden connection parameters
        :param connection_supplier: SQLConnectionSupplier sub-class instance to create SQLConnectionProperties from
                                    customer overriden connection parameters
        """
        if connection_supplier is None:
            connection_type = SQLConnectionFactory.determine_connection_type(
                metastore_parameters=metastore_parameters,
                connection_parameters=connection_parameters,
            )
            connection_supplier = SQLConnectionSupplierFactory().get_connection_supplier(
                connection_type
            )

        # Create connection properties class from provided parameters
        connection_props = connection_supplier.create_connection_properties(connection_parameters)

        # Compute final connection parameters
        (
            connection_dict,
            secret_params_keys,
        ) = SQLConnectionFactory._determine_connection_parameters(
            metastore_parameters, connection_props
        )
        return type(connection_props)(connection_dict, list(secret_params_keys))

    @staticmethod
    def determine_connection_type(
        metastore_type: str = None,
        metastore_id: str = None,
        metastore_parameters: Dict = None,
        connection_parameters: Dict = None,
    ) -> str:
        if metastore_parameters is None:
            metastore_parameters = SQLConnectionFactory.get_connection_parameters_from_metastore(
                metastore_type, metastore_id
            )
        if connection_parameters is not None and "connection_type" in connection_parameters.keys():
            return connection_parameters["connection_type"]

        if metastore_parameters is not None and "connection_type" in metastore_parameters.keys():
            return metastore_parameters["connection_type"]

        raise MissingParametersError(
            "connection_type must be present in metastore or provided as connection props."
        )

    @staticmethod
    def _determine_connection_parameters(
        metastore_params: Dict, props: SQLConnectionProperties
    ) -> (Dict, List):
        """
        Determine the final connection parameters.

        Order of precedence is:
        1. Customer-override configs (A)
        2. Configs from AWS Secrets  (B)
        3. Configs from metastore    (C)

        Note that Secret id can be present in both: The meta-store (C) as well as customer-override configs (A).
        In that case, use the customer-provided secret

        :param metastore_params:     The metastore configs. (C)
        :param props:                The customer provided props (A)
        :return:
        """

        aws_secret_arn = None
        if props._aws_secret_arn is not None:
            aws_secret_arn = props._aws_secret_arn
        elif "aws_secret_arn" in metastore_params.keys():
            aws_secret_arn = metastore_params["aws_secret_arn"]

        secrets_as_dictionary = {}
        if aws_secret_arn is not None:
            secrets_as_dictionary = AWSSecretsRetriever.get_secret_string(aws_secret_arn)

        customer_overrides_dict = props.to_dict(include_private_attr=True)

        connection_dict = {
            **metastore_params,
            **secrets_as_dictionary,
            **customer_overrides_dict,
        }
        secret_params_keys = secrets_as_dictionary.keys()
        return connection_dict, secret_params_keys

    @staticmethod
    def get_connection_parameters_from_metastore(
        metastore_type: str = None,
        metastore_id: str = None,
    ) -> Dict:
        if metastore_type and metastore_id:
            retriever = ConnectionMetadataRetrieverFactory.create_retriever(metastore_type)
            metastore_configurations = retriever.retrieve_connection_metadata(metastore_id)
            return metastore_configurations

        return {}
