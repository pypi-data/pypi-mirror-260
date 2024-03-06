# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from typing import Dict

from amazon_sagemaker_sql_execution.athena.connection import AthenaSQLConnection
from amazon_sagemaker_sql_execution.athena.models import AthenaSQLConnectionProperties
from amazon_sagemaker_sql_execution.connection import SQLConnection
from amazon_sagemaker_sql_execution.sql_connection_supplier import SQLConnectionSupplier

from amazon_sagemaker_sql_execution.utils.constants import CONNECTION_TYPE_ATHENA


class AthenaConnectionSupplier(SQLConnectionSupplier):
    @staticmethod
    def supplier_type() -> str:
        return CONNECTION_TYPE_ATHENA

    @staticmethod
    def create_connection_properties(
        connection_props_dict: Dict,
    ) -> AthenaSQLConnectionProperties:
        return AthenaSQLConnectionProperties(connection_props_dict)

    @staticmethod
    def create_connection(props: AthenaSQLConnectionProperties) -> SQLConnection:
        return AthenaSQLConnection(props)
