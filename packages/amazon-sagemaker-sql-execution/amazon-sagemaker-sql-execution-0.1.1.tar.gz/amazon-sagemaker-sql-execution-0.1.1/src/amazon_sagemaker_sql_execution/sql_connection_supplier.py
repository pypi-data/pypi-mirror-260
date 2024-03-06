# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod
from typing import Dict

from amazon_sagemaker_sql_execution.connection import SQLConnection
from amazon_sagemaker_sql_execution.models.sql_execution import SQLConnectionProperties


class SQLConnectionSupplier(ABC):
    @classmethod
    def responds_to(cls) -> str:
        """
        Returns type of object this supplier will supply.
        :return:
        """
        return cls.supplier_type()

    @staticmethod
    def get_connection_properties_key_for_metastore() -> str:
        """
        Returns the key in metastore connection metadata which stores connection information
        """
        return "PythonProperties"

    @staticmethod
    @abstractmethod
    def supplier_type() -> str:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def create_connection_properties(
        connection_props_dict: Dict,
    ) -> SQLConnectionProperties:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def create_connection(props: SQLConnectionProperties) -> SQLConnection:
        raise NotImplementedError()
