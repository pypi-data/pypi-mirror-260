# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod
from typing import Dict


class ConnectionMetadataRetriever(ABC):
    """
    Fetches database-connection specific information from appropriate connection metastore.
    I.e. ConnectionMetadataRetrieverGlue
    """

    @staticmethod
    @abstractmethod
    def supported_metastore() -> str:
        """
        :return: metadata stores from which this particular retriever can retrieve metadata
        """
        pass

    @abstractmethod
    def get_connection_properties_from_metadata(self, *args, **kwargs):
        """
        Gets connection properties
        """
        pass

    @abstractmethod
    def get_connection_type_from_metadata(self, *args, **kwargs):
        """
        Gets connection type
        """
        pass

    @abstractmethod
    def retrieve_connection_metadata(self, key: str) -> Dict:
        """
        :param id: The connection id from which to retrieve connection metadata.
        :return:  key-value pairs which can be used for params defined by SQLConnectionProperties
        """
        return {}

    @abstractmethod
    def _parse_connection_metadata(self, contents):
        pass
