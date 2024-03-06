# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
SM_PLUGIN_PREFIX: We require all the plugins for SM SQL to start with this prefix.
"""

SM_PLUGIN_PREFIX = "sm_sql"

METASTORE_TYPE_LOCAL_FILE = "LOCAL_FILE"
METASTORE_TYPE_GLUE = "GLUE_CONNECTION"

CONNECTION_TYPE_REDSHIFT = "REDSHIFT"
CONNECTION_TYPE_ATHENA = "ATHENA"
CONNECTION_TYPE_SNOWFLAKE = "SNOWFLAKE"

SAGEMAKER_SQL_EXECUTION_LOG_BASE_DIRECTORY = "/var/log/studio/sagemaker_notebook_sql_experience"
SAGEMAKER_SQL_EXECUTION_LOG_FILE = "notebook_sql_execution.log"
LOGGER_NAME = "sagemaker-notebook-sql-execution"

UNKNOWN_METRIC_VALUE = "UNKNOWN"
METRICS_NAMESPACE = "SagemakerNotebookSQL"

# Regex pattern for stack trace filters
EMAIL_REGEX = "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}"
# credit to https://uibakery.io/regex-library/phone-number-python
PHONE_NUMBER_REGEX = "\+?\d{1,4}?[-.\s]?\(?(\d{1,3}?)\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}"
PASSWORD_REGEX = "(?i)password'*\"*\s*[:=]\s*\S+"
API_KEY_REGEX = "(?i)apikey\s*[:= ]\s*\S+"
AWS_SECRETKEY_REGEX = "(?i)aws_secret_access_key\s*[:=]\s*\S+"


class MetricsConstants:
    OPERATION_DIMENSION_NAME = "Operation"
    CONNECTION_TYPE_DIMENSION_NAME = "ConnectionType"
    GET_OR_CREATE_CONNECTION_OPERATION = "GetOrCreateConnection"
    SQL_CREATE_CONNECTION_OPERATION = "CreateConnection"
    SQL_QUERY_EXECUTE_OPERATION = "SQLQueryExecute"
    SQL_CLOSE_CONNECTION_OPERATION = "SQLConnectionClose"
