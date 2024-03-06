# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json
import logging
import os
from enum import Enum
from botocore.session import Session
from amazon_sagemaker_sql_execution.utils.constants import UNKNOWN_METRIC_VALUE, LOGGER_NAME

# This is a public contract - https://docs.aws.amazon.com/sagemaker/latest/dg/notebooks-run-and-manage-metadata.html#notebooks-run-and-manage-metadata-app
app_metadata_file_location = "/opt/ml/metadata/resource-metadata.json"

DEFAULT_REGION = "us-east-2"


class UserTypes(Enum):
    SHARED_SPACE_USER = "shared-space"
    PROFILE_USER = "user-profile"

    def __str__(self):
        return self.value


class JupyterLabEnvironment(Enum):
    SAGEMAKER_STUDIO = "SageMakerStudio"
    VANILLA_JUPYTERLAB = "VanillaJupyterLab"


def get_region_name():
    """
    Get region config in following order:
    1. AWS_REGION env var
    2. Region from AWS config (for example, through `aws configure`)
    3. AWS_DEFAULT_REGION env var
    4. If none of above are set, use us-east-2 (same as Studio Lab)
    :return:
    """
    region_config_chain = [
        os.environ.get(
            "AWS_REGION"
        ),  # this value is set for Studio, so we dont need any special environment specific logic
        Session().get_scoped_config().get("region"),
        os.environ.get("AWS_DEFAULT_REGION"),
        DEFAULT_REGION,
    ]
    for region_config in region_config_chain:
        if region_config is not None:
            return region_config
    return UNKNOWN_METRIC_VALUE


class AppMetadata:
    def __init__(self):
        app_metadata = _get_app_metadata_file()
        if app_metadata:
            self.sagemaker_environment = JupyterLabEnvironment.SAGEMAKER_STUDIO
        else:
            self.sagemaker_environment = JupyterLabEnvironment.VANILLA_JUPYTERLAB
        self.user_profile_name = app_metadata.get("UserProfileName", UNKNOWN_METRIC_VALUE)
        self.shared_space_name = app_metadata.get("SpaceName", UNKNOWN_METRIC_VALUE)
        self.domain_id = app_metadata.get("DomainId", UNKNOWN_METRIC_VALUE)


def _get_app_metadata_file():
    try:
        with open(app_metadata_file_location) as file:
            return json.loads(file.read())
    except Exception:
        # This means vanilla jupyter lab, not an error, so returning empty value
        return {}
