# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import logging
import os

import boto3
from functools import lru_cache

from amazon_sagemaker_sql_execution.utils.constants import UNKNOWN_METRIC_VALUE, LOGGER_NAME


@lru_cache(maxsize=1)
def get_aws_account_id(region_name):
    try:
        account_id = os.environ.get("AWS_ACCOUNT_ID")
        if account_id is None:
            # we are in standalone jupyterlab
            session = boto3.session.Session()
            client = session.client(service_name="sts", region_name=region_name)
            return client.get_caller_identity()["Account"]
        return account_id
    except Exception as e:
        logging.getLogger(LOGGER_NAME).error(f"Failed to get aws account id: {e}")
        return UNKNOWN_METRIC_VALUE
