# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from typing import Dict

from amazon_sagemaker_sql_execution.connection import SQLConnection
from amazon_sagemaker_sql_execution.snowflake.connection import SnowflakeSQLConnection
from amazon_sagemaker_sql_execution.snowflake.models import SnowflakeSQLConnectionProperties
from amazon_sagemaker_sql_execution.sql_connection_supplier import SQLConnectionSupplier

from amazon_sagemaker_sql_execution.utils.constants import CONNECTION_TYPE_SNOWFLAKE


class SnowflakeConnectionSupplier(SQLConnectionSupplier):
    @staticmethod
    def supplier_type() -> str:
        return CONNECTION_TYPE_SNOWFLAKE

    @staticmethod
    def create_connection_properties(
        connection_props_dict: Dict,
    ) -> SnowflakeSQLConnectionProperties:
        return SnowflakeSQLConnectionProperties(connection_props_dict)

    @staticmethod
    def create_connection(props: SnowflakeSQLConnectionProperties) -> SQLConnection:
        return SnowflakeSQLConnection(props)
