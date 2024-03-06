# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

try:
    import snowflake.connector
except ModuleNotFoundError:
    # Swallow exception. All classes assume to handle missing snowflake dependencies in their init method.
    None

from amazon_sagemaker_sql_execution.connection import SQLConnection
from amazon_sagemaker_sql_execution.exceptions import (
    SQLExecutionError,
    ConnectionCreationError,
)
from amazon_sagemaker_sql_execution.models.sql_execution import (
    SQLExecutionRequest,
)
from amazon_sagemaker_sql_execution.snowflake.models import (
    SnowflakeSQLConnectionProperties,
    SnowflakeSQLExecutionResponse,
    SnowflakeSQLQueryParameters,
)
from amazon_sagemaker_sql_execution.utils.metrics.service_metrics import add_metrics
from amazon_sagemaker_sql_execution.utils.constants import MetricsConstants

from amazon_sagemaker_sql_execution.exceptions import CredentialsExpiredError


class SnowflakeSQLConnection(SQLConnection):
    def log_source(self):
        return self.__class__.__name__

    @staticmethod
    def engine_type():
        return "SNOWFLAKE"

    def __init__(self, connection_props: SnowflakeSQLConnectionProperties):
        super().__init__(connection_props)
        try:
            import snowflake.connector
        except ModuleNotFoundError:
            error_str = f"Could not import snowflake. Please ensure `snowflake-connector-python` is installed."
            self.error(error_str)
            raise ConnectionCreationError(error_str)

        try:
            connection_dict = self._connection_props.to_dict()
            self.connection = snowflake.connector.connect(**connection_dict)
        except snowflake.connector.errors.Error as e:
            self.error(
                f"Could not create connection using params: {connection_props} due to: {str(e)}"
            )
            raise ConnectionCreationError(e) from e

    @add_metrics(MetricsConstants.SQL_QUERY_EXECUTE_OPERATION)
    def execute(self, execution_request: SQLExecutionRequest):
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

            # Convert to SnowflakeSQLQueryParameters and back to handle snowflake specific inconsistencies
            execution_params = SnowflakeSQLQueryParameters(execution_request.queryParams).to_dict()

            # Snowflake expects query in `command` param: https://github.com/snowflakedb/snowflake-connector-python/blob/main/src/snowflake/connector/cursor.py#L612
            execution_params["command"] = execution_request.query

            res_cursor = cursor.execute(**execution_params)
            data = res_cursor.fetchall()
            cursor_desc = res_cursor.description

            cursor.close()
            return SnowflakeSQLExecutionResponse(data=data, cursor_desc=cursor_desc)
        except snowflake.connector.errors.Error as e:
            self.error(f"Error while executing query {e}")
            if "Authentication token has expired" in e.msg:
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
