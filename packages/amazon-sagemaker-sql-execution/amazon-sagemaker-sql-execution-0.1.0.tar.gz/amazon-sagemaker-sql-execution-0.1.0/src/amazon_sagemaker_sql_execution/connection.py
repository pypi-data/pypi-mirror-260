# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from abc import abstractmethod, ABC

from amazon_sagemaker_sql_execution.models.sql_execution import (
    SQLExecutionRequest,
    SQLConnectionProperties,
    SQLExecutionResponse,
)

from amazon_sagemaker_sql_execution.utils.logging_utils import ServiceFileLoggerMixin

from amazon_sagemaker_sql_execution.utils.metrics.service_metrics import (
    InstanceAttributeMetricsContextMixin,
)


class SQLConnection(ServiceFileLoggerMixin, InstanceAttributeMetricsContextMixin, ABC):
    @staticmethod
    @abstractmethod
    def engine_type():
        raise NotImplementedError()

    def __init__(self, connection_props: SQLConnectionProperties):
        super().__init__()
        self._connection_props = connection_props

    @abstractmethod
    def execute(self, execution_request: SQLExecutionRequest) -> SQLExecutionResponse:
        """
        :param execution_request:
        :return:
        """
        pass

    def get_properties(self):
        return self._connection_props

    @abstractmethod
    def close(self):
        """
        Client MUST call close() to ensure connections are cleaned up.
        :return:
        """
        pass

    def __str__(self):
        return str(self.get_properties())
