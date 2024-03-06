# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json
from typing import Dict
import boto3
import botocore.exceptions

from amazon_sagemaker_sql_execution.exceptions import MetadataRetrieverError
from amazon_sagemaker_sql_execution.utils.metadata_retriever.connection_metadata_retriever import (
    ConnectionMetadataRetriever,
)
from amazon_sagemaker_sql_execution.utils.sql_connection_supplier_factory import (
    SQLConnectionSupplierFactory,
)
from amazon_sagemaker_sql_execution.utils.constants import METASTORE_TYPE_GLUE


class GlueConnectionMetadataRetriever(ConnectionMetadataRetriever):
    @staticmethod
    def supported_metastore() -> str:
        return METASTORE_TYPE_GLUE

    def retrieve_connection_metadata(self, glue_connection_name: str) -> Dict:
        """
        :param glue_connection_name: the name of the connection
        :return:  key-value pairs which can be used for params defined by SQLConnectionProperties
        """
        try:
            glue_client = boto3.client("glue")
            glue_conn_props = glue_client.get_connection(Name=glue_connection_name)
            return self._parse_connection_metadata(glue_conn_props)

        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "EntityNotFoundException":
                raise MetadataRetrieverError(
                    f"Connection with the name {glue_connection_name} could not be found in "
                    f"AWS Glue"
                )
            else:
                raise e

    def _parse_connection_metadata(self, glue_connection_metadata: dict) -> dict:
        """
        Parses connection metadata as received from Glue connection

        :param glue_connection_metadata: contains connection properties specific to connection type
        :return:
        """

        connection_type = self.get_connection_type_from_metadata(
            glue_connection_metadata=glue_connection_metadata
        )
        return {
            **self.get_connection_properties_from_metadata(
                glue_connection_metadata=glue_connection_metadata,
                connection_type=connection_type,
            ),
            "connection_type": connection_type,
        }

    def get_connection_properties_from_metadata(self, *args, **kwargs):
        """
        :return: connection properties based on connection type
        """
        glue_connection_metadata = kwargs.get("glue_connection_metadata")
        connection_type = kwargs.get("connection_type")

        connection_supplier = SQLConnectionSupplierFactory().get_connection_supplier(
            connection_type
        )
        try:
            connection_properties = glue_connection_metadata["Connection"]["ConnectionProperties"][
                connection_supplier.get_connection_properties_key_for_metastore()
            ]
        except KeyError as e:
            missing_key = e.args[0]
            raise MetadataRetrieverError(f'Missing key "{missing_key}" in connection metadata')

        return json.loads(connection_properties)

    def get_connection_type_from_metadata(self, *args, **kwargs):
        """
        :return: connection type from connection metadata
        """
        glue_connection_metadata = kwargs.get("glue_connection_metadata")
        try:
            connection_type = glue_connection_metadata["Connection"]["ConnectionType"]
        except KeyError as e:
            missing_key = e.args[0]
            raise MetadataRetrieverError(f'Missing key "{missing_key}" in connection metadata')
        return connection_type
