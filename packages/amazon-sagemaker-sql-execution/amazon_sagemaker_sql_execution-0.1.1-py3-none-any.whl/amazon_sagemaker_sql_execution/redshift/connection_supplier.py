# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from typing import Dict

from amazon_sagemaker_sql_execution.connection import SQLConnection
from amazon_sagemaker_sql_execution.redshift.connection import RedshiftSQLConnection
from amazon_sagemaker_sql_execution.redshift.models import RedshiftSQLConnectionProperties
from amazon_sagemaker_sql_execution.sql_connection_supplier import SQLConnectionSupplier

from amazon_sagemaker_sql_execution.utils.constants import CONNECTION_TYPE_REDSHIFT


class RedshiftConnectionSupplier(SQLConnectionSupplier):
    @staticmethod
    def supplier_type() -> str:
        return CONNECTION_TYPE_REDSHIFT

    @staticmethod
    def create_connection_properties(
        connection_props_dict: Dict,
    ) -> RedshiftSQLConnectionProperties:
        return RedshiftSQLConnectionProperties(connection_props_dict)

    @staticmethod
    def create_connection(props: RedshiftSQLConnectionProperties) -> SQLConnection:
        return RedshiftSQLConnection(props)
