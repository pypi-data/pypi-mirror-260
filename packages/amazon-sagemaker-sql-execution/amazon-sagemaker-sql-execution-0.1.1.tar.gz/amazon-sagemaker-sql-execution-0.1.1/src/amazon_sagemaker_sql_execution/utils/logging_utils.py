# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import logging
import os
import sys
from abc import ABC, abstractmethod
from uuid import uuid4

from amazon_sagemaker_sql_execution.utils.constants import (
    SAGEMAKER_SQL_EXECUTION_LOG_FILE,
    SAGEMAKER_SQL_EXECUTION_LOG_BASE_DIRECTORY,
)


class ServiceFileLogger:
    """
    Logs service logs to a given file.
    """

    context_logger = None

    def __init__(
        self,
        log_file_name,
        log_base_directory,
        context_logger=None,
        also_write_to_stdout=False,
    ):
        """
        :param log_file_name:           File name to publish logs to
        :param log_base_directory:      log_base_directory : Creates directory structure if one does not exist.
        :param context_logger:          Loggers passed from caller's context.
                                        Errors while creating logger / logging are sent to this logger.
        :param also_write_to_stdout:    also_write_to_stdout
        """

        try:
            self.context_logger = context_logger
            os.makedirs(log_base_directory, exist_ok=True)

            self.file_logger = logging.getLogger(uuid4().hex)
            self.file_logger.handlers.clear()
            self.file_logger.setLevel(logging.INFO)
            file_path = os.path.join(log_base_directory, log_file_name)
            file_handler = logging.FileHandler(file_path)
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s]%(message)s", "%Y-%m-%d %H:%M:%S"
            )
            file_handler.setFormatter(formatter)
            self.file_logger.addHandler(file_handler)

            if also_write_to_stdout:
                stream_handler = logging.StreamHandler(stream=sys.stdout)
                self.file_logger.addHandler(stream_handler)

        except Exception as e:
            self.file_logger = None
            if self.context_logger and context_logger is not None:
                context_logger.error(f"Failed to initialize ServiceFileLogger: {e}")

    def info(self, payload, exc_info=False):
        try:
            self.file_logger.info(payload, exc_info=exc_info)
        except Exception as e:
            if self.context_logger and self.context_logger is not None:
                self.context_logger.error(f"Failed to log service payload: {e}")

    def error(self, payload, exc_info=False):
        try:
            self.file_logger.error(payload, exc_info=exc_info)
        except Exception as e:
            if self.context_logger and self.context_logger is not None:
                self.context_logger.error(f"Failed to log service payload: {e}")


class ServiceFileLoggerMixin(ABC):
    """
    Mixin to add logging to a class.
    """

    _logger = ServiceFileLogger(
        log_file_name=SAGEMAKER_SQL_EXECUTION_LOG_FILE,
        log_base_directory=SAGEMAKER_SQL_EXECUTION_LOG_BASE_DIRECTORY,
        context_logger=None,
        also_write_to_stdout=False,
    )

    @abstractmethod
    def log_source(self):
        raise NotImplementedError()

    def info(self, payload, exc_info=False):
        self._logger.info(payload, exc_info=exc_info)

    def error(self, payload, exc_info=True):
        self._logger.error(payload, exc_info=exc_info)
