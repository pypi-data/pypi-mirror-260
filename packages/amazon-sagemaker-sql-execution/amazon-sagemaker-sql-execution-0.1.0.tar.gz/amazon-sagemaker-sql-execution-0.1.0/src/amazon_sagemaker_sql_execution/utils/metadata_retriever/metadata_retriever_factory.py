# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
from amazon_sagemaker_sql_execution.exceptions import InvalidParameterError
from amazon_sagemaker_sql_execution.utils.metadata_retriever.BaseSQLFactory import (
    BaseSQLFactory,
)
from amazon_sagemaker_sql_execution.utils.metadata_retriever.connection_metadata_retriever import (
    ConnectionMetadataRetriever,
)
from amazon_sagemaker_sql_execution.utils.metadata_retriever.file_metadata_retriever import (
    FileMetadataRetriever,
)
from amazon_sagemaker_sql_execution.utils.metadata_retriever.glueconnection_metadata_retriever import (
    GlueConnectionMetadataRetriever,
)
from amazon_sagemaker_sql_execution.utils.constants import (
    METASTORE_TYPE_LOCAL_FILE,
    METASTORE_TYPE_GLUE,
)


class ConnectionMetadataRetrieverFactory(BaseSQLFactory):
    @staticmethod
    def factory_for_class_type():
        """
        Returns the type of objects produced by the factory.
        """
        return ConnectionMetadataRetriever

    @staticmethod
    def create_retriever(data_provider_type) -> ConnectionMetadataRetriever:
        """
        :param data_provider_type:
        :return:
        """
        # TODO: Make the factory plugin compatible. use `self.subclasses` of BaseFactory to instantiate objects.
        if data_provider_type == METASTORE_TYPE_LOCAL_FILE:
            return FileMetadataRetriever()
        elif data_provider_type == METASTORE_TYPE_GLUE:
            return GlueConnectionMetadataRetriever()
        else:
            raise NotImplementedError()
