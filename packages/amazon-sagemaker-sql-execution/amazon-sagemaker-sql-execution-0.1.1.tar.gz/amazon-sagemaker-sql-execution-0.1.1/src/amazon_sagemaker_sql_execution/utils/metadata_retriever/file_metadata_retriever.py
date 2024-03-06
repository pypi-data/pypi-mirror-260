# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json
from typing import Dict

from amazon_sagemaker_sql_execution.exceptions import MetadataRetrieverError
from amazon_sagemaker_sql_execution.utils.metadata_retriever.connection_metadata_retriever import (
    ConnectionMetadataRetriever,
)
from amazon_sagemaker_sql_execution.utils.constants import METASTORE_TYPE_LOCAL_FILE


class FileMetadataRetriever(ConnectionMetadataRetriever):
    @staticmethod
    def supported_metastore() -> str:
        return METASTORE_TYPE_LOCAL_FILE

    def retrieve_connection_metadata(self, file_path: str) -> Dict:
        """
        :param file_path: The local file path
        :return:  key-value pairs which can be used for params defined by SQLConnectionProperties
        """
        try:
            with open(file_path, "r") as f:
                contents = f.read()
                return self._parse_connection_metadata(contents)

        except FileNotFoundError as e:
            raise MetadataRetrieverError(e) from e

    def _parse_connection_metadata(self, file_contents) -> dict:
        """
        Loads connection metadata information from file content

        :param file_contents: contents of the file
        :return:
        """
        return self.get_connection_properties_from_metadata(file_contents=file_contents)

    def get_connection_type_from_metadata(self, *args, **kwargs):
        # we don't need to explicitly get connection type for file metadata retriever
        return

    def get_connection_properties_from_metadata(self, *args, **kwargs):
        file_contents = kwargs.get("file_contents")
        return json.loads(file_contents)
