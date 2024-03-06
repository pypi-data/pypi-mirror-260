# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from amazon_sagemaker_sql_execution.sql_connection_supplier import SQLConnectionSupplier

from amazon_sagemaker_sql_execution.exceptions import InvalidParameterError
from amazon_sagemaker_sql_execution.utils.metadata_retriever.BaseSQLFactory import (
    BaseSQLFactory,
)


class SQLConnectionSupplierFactory(BaseSQLFactory):
    @staticmethod
    def factory_for_class_type():
        """
        Returns the type of objects produced by the factory.
        """
        return SQLConnectionSupplier

    def __init__(self):
        super().__init__()

    def get_connection_supplier(self, supplier_type: str):
        if supplier_type in self.subclasses:
            return self.subclasses[supplier_type]
        else:
            raise InvalidParameterError(f"No supplier found which can handle: {supplier_type}")
