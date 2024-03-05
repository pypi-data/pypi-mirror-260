# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from abc import ABC
from functools import wraps
import inspect
import os
import sys
import logging.handlers
import datetime
import traceback

from aws_embedded_metrics.sinks.stdout_sink import StdoutSink, Sink
from aws_embedded_metrics import MetricsLogger
from aws_embedded_metrics.logger.metrics_context import MetricsContext
from aws_embedded_metrics.environment.local_environment import LocalEnvironment

from amazon_sagemaker_sql_execution.utils.metrics.stack_trace_filter import (
    StackTraceFilter,
)

from amazon_sagemaker_sql_execution.utils.metrics.app_metadata import (
    get_region_name,
    AppMetadata,
)

from amazon_sagemaker_sql_execution.utils.metrics.aws_config import (
    get_aws_account_id,
)

from amazon_sagemaker_sql_execution.exceptions import Error

from amazon_sagemaker_sql_execution.utils.constants import (
    SAGEMAKER_SQL_EXECUTION_LOG_FILE,
    SAGEMAKER_SQL_EXECUTION_LOG_BASE_DIRECTORY,
    LOGGER_NAME,
)

from amazon_sagemaker_sql_execution.utils.constants import METRICS_NAMESPACE

stack_trace_filter = StackTraceFilter()
app_metadata = AppMetadata()


def initiate_logger(log_file_location: str, logger_name: str):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file_location)
    logger.addHandler(file_handler)
    # https://docs.python.org/3/library/logging.html#logging.Logger.propagate
    logger.propagate = False


def get_log_file_location(log_file_name: str) -> str:
    """
    We try to set log location, if we see an exception, we publish it to the user's home directory
    :param log_file_name:
    :return: log_file_location: str
    """
    try:
        os.makedirs(SAGEMAKER_SQL_EXECUTION_LOG_BASE_DIRECTORY, exist_ok=True)
        return os.path.join(SAGEMAKER_SQL_EXECUTION_LOG_BASE_DIRECTORY, log_file_name)
    except Exception:
        # We cannot create this directory when running code locally, so we use the following location for logs
        home_dir = os.path.expanduser("~")
        log_file_path = os.path.join(home_dir, ".sagemaker")
        os.makedirs(log_file_path, exist_ok=True)
        return os.path.join(log_file_path, log_file_name)


initiate_logger(get_log_file_location(SAGEMAKER_SQL_EXECUTION_LOG_FILE), LOGGER_NAME)


class LogFileSink(StdoutSink):
    def __init__(self, logger_name: str):
        super().__init__()
        self.logger_name = logger_name

    def accept(self, context: MetricsContext) -> None:
        for serialized_content in self.serializer.serialize(context):
            if serialized_content:
                logging.getLogger(self.logger_name).info(serialized_content)

    @staticmethod
    def name() -> str:
        return "LogFileSink"


class LogFileEnvironment(LocalEnvironment):
    def __init__(self, logger_name: str):
        super().__init__()
        self.logger_name = logger_name

    def get_sink(self) -> Sink:
        return LogFileSink(self.logger_name)


class CustomMetricsLogger(MetricsLogger):
    def __init__(self, environment: LogFileEnvironment, context: MetricsContext):
        super().__init__(environment, context)
        self.environment = environment

    def flush(self) -> None:
        """Override the default async MetricsLogger.flush method, flushing to stdout immediately"""
        sink = self.environment.get_sink()
        sink.accept(self.context)
        # we need to explicitly clear the older metrics so the value does not get added to the next time the metric
        # is emitted because the context is instantiated at the instance
        self.context.metrics.clear()
        self.context.properties.clear()
        self.context.dimensions.clear()


def create_metrics_context():
    """
    We create a metrics context in the class when we want to add properties, dimensions or metrics specific to the class
     or methods in the class
    :return: MetricsContext
    """
    context = MetricsContext().empty()
    context.namespace = METRICS_NAMESPACE
    context.should_use_default_dimensions = False
    return context


class InstanceAttributeMetricsContextMixin(ABC):
    """
    Mixin to add metrics_context to an instance where we want to emit metrics
    """

    def __init__(self):
        self.metrics_context = create_metrics_context()


class ClassAttributeMetricsContextMixin(ABC):
    """
    Mixin to add metrics_context to a class where we want to emit metrics
    """

    metrics_context = create_metrics_context()


def get_or_create_metrics_context(args, func) -> MetricsContext:
    """
    We create a metrics context in the class when we want to add properties, dimensions or metrics specific to the class
     or methods in the class
    :return: MetricsContext
    """
    # If we have the InstanceAttributeMetricsContextMixin for the class, we get the metrics context from the instance
    if len(args) > 0:
        instance = args[0]
        if hasattr(instance, "metrics_context"):
            return instance.metrics_context

    # If we have the ClassAttributeMetricsContextMixin for the class, we get the metrics context from the class. We get
    # the class from the function
    module = sys.modules[func.__module__]
    # Qualified name is a string that looks like class_name.method_name
    class_name = func.__qualname__.split(".")[0]
    try:
        cls = getattr(module, class_name)
        if hasattr(cls, "metrics_context"):
            return cls.metrics_context
    except AttributeError:
        pass
    # Only case it would reach here is if we have not provided a metrics context mixin for the class because we don't
    # any properties/metrics/dimensions for this instance/class
    return create_metrics_context()


def add_common_properties_to_metrics_context(context: MetricsContext):
    """
    Adds properties to the metrics context
    :param context: MetricsContext
    :return:
    """
    region = get_region_name()
    context.set_property("Region", region)
    context.set_property("AccountId", get_aws_account_id(region))
    context.set_property("UserProfileName", app_metadata.user_profile_name)
    context.set_property("SharedSpaceName", app_metadata.shared_space_name)
    context.set_property("DomainId", app_metadata.domain_id)


def add_metrics(operation: str):
    """
    Add InstanceAttributeMetricsContextMixin or ClassAttributeMetricsContextMixin to class before using this function. Adds metrics like latency, fault, error and count for the operation performed. It will also serve as
    logging for exception with extra properties that will help with debugging
    :param operation: Name of the operation being performed
    :return:
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.datetime.now()
            error = fault = 0
            context = get_or_create_metrics_context(args, func)
            context.namespace = METRICS_NAMESPACE
            context.put_dimensions({"Operation": operation})
            metrics_logger = CustomMetricsLogger(LogFileEnvironment(LOGGER_NAME), context)
            # In case we're okay with adding a MetricsContext to the signature, this decorator will set the value for it
            # so method/class specific metrics can be added
            if "metrics" in inspect.signature(func).parameters:
                kwargs["metrics"] = metrics_logger
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if isinstance(e, Error):
                    error = 1
                else:
                    fault = 1
                stack_trace = traceback.format_exc()
                context.set_property("StackTrace", stack_trace_filter.filter(stack_trace))
                raise e
            finally:
                try:

                    add_common_properties_to_metrics_context(context)
                    context.put_metric("Error", error, "Count")
                    context.put_metric("Fault", fault, "Count")
                    elapsed = datetime.datetime.now() - start_time
                    context.put_metric(
                        "Latency", int(elapsed.total_seconds() * 1000), "Milliseconds"
                    )
                    metrics_logger.flush()
                except Exception as e:
                    # we silently fail for the extra information that we add
                    # and not affect any api operations
                    logging.getLogger(LOGGER_NAME).error(f"Exception when logging metrics {e}")

        return wrapper

    return decorator


def add_metric(dimension_set: dict, metric_name: str, metric_value, metric_unit: str):
    """
    Adds a metric with the specified dimension set. Useful for non-critical metrics that could be displayed in a dashboard
    :param dimension_set:
    :param metric_name:
    :param metric_value:
    :param metric_unit:
    :return:
    """
    context = MetricsContext().empty()
    context.namespace = METRICS_NAMESPACE
    context.should_use_default_dimensions = False
    metrics_logger = CustomMetricsLogger(LogFileEnvironment(LOGGER_NAME), context)
    for key, value in dimension_set.items():
        context.put_dimensions({key: value})
    add_common_properties_to_metrics_context(context)
    context.put_metric(metric_name, metric_value, metric_unit)
    metrics_logger.flush()
