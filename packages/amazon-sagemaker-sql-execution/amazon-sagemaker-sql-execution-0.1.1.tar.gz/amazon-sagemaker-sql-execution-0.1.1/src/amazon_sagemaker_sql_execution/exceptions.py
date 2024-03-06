# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


class Error(Exception):
    """
    Generic exception that is the base exception for all other Errors from this lib
    """

    pass


class Fault(Exception):
    """
    Generic exception that is the base exception for all other Faults from this lib
    """

    pass


class MissingParametersError(Error):
    pass


class InvalidParameterError(Error):
    pass


"""
CREDENTIALS EXPIRED ERROR
"""


class CredentialsExpiredError(Error):
    pass


"""
CONNECTION FAULTS / ERRORS
"""


class ConnectionCreationError(Error):
    pass


class SQLExecutionError(Error):
    pass


"""
CONNECTION POOL FAULTS / ERRORS
"""


class ConnectionPoolError(Error):
    pass


class ConnectionPoolFault(Fault):
    pass


"""
SECRETS RETRIEVER FAULTS / ERRORS
"""


class SecretsRetrieverError(Error):
    pass


"""
METASTORE METADATA RETRIEVER FAULTS / ERRORS
"""


class MetadataRetrieverError(Error):
    pass
