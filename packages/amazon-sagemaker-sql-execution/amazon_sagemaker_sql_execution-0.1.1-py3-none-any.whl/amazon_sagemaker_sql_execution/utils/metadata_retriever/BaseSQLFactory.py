# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from abc import abstractmethod, ABC

from amazon_sagemaker_sql_execution.utils.constants import SM_PLUGIN_PREFIX

# TODO: Find a fix for __subclasses__() import-issue which aligns with best-practices
# subclasses need to be imported to show up in __subclasses__() if they reside in a different module
from amazon_sagemaker_sql_execution.athena.connection_supplier import AthenaConnectionSupplier
from amazon_sagemaker_sql_execution.snowflake.connection_supplier import (
    SnowflakeConnectionSupplier,
)
from amazon_sagemaker_sql_execution.redshift.connection_supplier import (
    RedshiftConnectionSupplier,
)


class BaseSQLFactory(ABC):
    """
    Base class for all SQL Factories.
    """

    plugin_util = None

    @staticmethod
    @abstractmethod
    def factory_for_class_type():
        """
        Returns the type of objects produced by the factory.
        """
        raise NotImplementedError()

    def __init__(self):
        self.subclasses = {}
        all_subclasses = self._all_subclasses(self.factory_for_class_type())

        for subclass in all_subclasses:
            subclass_key = subclass.responds_to()
            self.subclasses[subclass_key] = subclass

    @classmethod
    def _all_subclasses(cls, base_class):
        return set(base_class.__subclasses__()).union(
            [s for c in base_class.__subclasses__() for s in cls._all_subclasses(c)]
        )
