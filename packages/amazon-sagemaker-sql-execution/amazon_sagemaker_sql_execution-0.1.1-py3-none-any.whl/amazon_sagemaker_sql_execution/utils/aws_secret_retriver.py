# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json
from json import JSONDecodeError
from typing import Dict, Union

import boto3
from botocore.exceptions import ClientError

from amazon_sagemaker_sql_execution.exceptions import (
    SecretsRetrieverError,
)


class AWSSecretsRetriever:
    @staticmethod
    def get_secret_string(secret_name: str, region_name: str = None) -> Dict:
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            secret_string = get_secret_value_response["SecretString"]

            secret_dict = json.loads(secret_string)
            return secret_dict
        except KeyError:
            raise SecretsRetrieverError(f"`SecretString` was not present in secret {secret_name}")
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                raise SecretsRetrieverError(f"Secret {secret_name} not found") from e
            raise SecretsRetrieverError("Error while decoding secret") from e
        except JSONDecodeError as e:
            raise SecretsRetrieverError("Error while decoding secret") from e
