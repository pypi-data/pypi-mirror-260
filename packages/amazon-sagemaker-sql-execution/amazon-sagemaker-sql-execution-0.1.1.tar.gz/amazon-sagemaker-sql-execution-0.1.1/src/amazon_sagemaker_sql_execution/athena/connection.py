# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import pyathena
from botocore.exceptions import ClientError

from amazon_sagemaker_sql_execution.connection import SQLConnection
from amazon_sagemaker_sql_execution.exceptions import (
    SQLExecutionError,
    ConnectionCreationError,
    CredentialsExpiredError,
)
from amazon_sagemaker_sql_execution.models.sql_execution import (
    SQLExecutionRequest,
)
from amazon_sagemaker_sql_execution.athena.models import (
    AthenaSQLExecutionResponse,
    AthenaSQLQueryParameters,
    AthenaSQLConnectionProperties,
)
from amazon_sagemaker_sql_execution.utils.metrics.service_metrics import add_metrics
from amazon_sagemaker_sql_execution.utils.constants import MetricsConstants


class AthenaSQLConnection(SQLConnection):
    def log_source(self):
        return self.__class__.__name__

    @staticmethod
    def engine_type():
        return "ATHENA"

    def __init__(self, connection_props: AthenaSQLConnectionProperties):
        super().__init__(connection_props)
        try:
            conn_params = self._connection_props.to_dict()
            self.connection = pyathena.connect(**conn_params)
        except Exception as e:
            self.error(
                f"Could not create connection using params: {connection_props} due to: {str(e)}"
            )
            raise ConnectionCreationError(e) from e

    @add_metrics(MetricsConstants.SQL_QUERY_EXECUTE_OPERATION)
    def execute(self, execution_request: SQLExecutionRequest) -> AthenaSQLExecutionResponse:
        self.metrics_context.set_dimensions(
            [
                {
                    MetricsConstants.OPERATION_DIMENSION_NAME: MetricsConstants.SQL_QUERY_EXECUTE_OPERATION,
                    MetricsConstants.CONNECTION_TYPE_DIMENSION_NAME: self.engine_type(),
                }
            ]
        )
        try:
            cursor = self.connection.cursor()
            # Convert to AthenaSQLQueryParameters and back to handle database specific inconsistencies
            execution_params = AthenaSQLQueryParameters(execution_request.queryParams).to_dict()

            execution_params["operation"] = execution_request.query
            res_cursor = cursor.execute(**execution_params)

            data = res_cursor.fetchall()
            cursor_desc = res_cursor.description
            cursor.close()

            return AthenaSQLExecutionResponse(data=data, cursor_desc=cursor_desc)

        except Exception as e:
            self.error(f"Error while executing query {e}")
            if (
                isinstance(e.__cause__, ClientError)
                and e.__cause__.response["Error"]["Code"] == "ExpiredTokenException"
            ):
                raise CredentialsExpiredError(e) from e
            raise SQLExecutionError(e) from e

    @add_metrics(MetricsConstants.SQL_CLOSE_CONNECTION_OPERATION)
    def close(self):
        self.metrics_context.set_dimensions(
            [
                {
                    MetricsConstants.OPERATION_DIMENSION_NAME: MetricsConstants.SQL_CLOSE_CONNECTION_OPERATION,
                    MetricsConstants.CONNECTION_TYPE_DIMENSION_NAME: self.engine_type(),
                }
            ]
        )
        if self.connection is not None:
            self.connection.close()
