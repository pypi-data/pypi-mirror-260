# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
from abc import ABC
from typing import Optional, Dict

from amazon_sagemaker_sql_execution.utils.mixins import SQLParameterMixin


class SQLQueryParameters(SQLParameterMixin):
    """
    Contains sql-query specific properties which will vary per query. E.g. Parameter binding etc
    """

    def __init__(self, params: Optional[dict] = None):
        self._set_instance_variables(params)


class SQLConnectionProperties(SQLParameterMixin, ABC):
    """
    Contains properties specific to a db connection. For e.g. host / port / userid / password for connection.

    TODO:
    1. Add versioning support for all SQL connection properties
    2. Determine how we can have a single source of truth to define all the supported parameters, so that adding a new
    parameter which can be transparently passed through to the execution layer doesn't have to involve code change.
    """

    def __init__(self, params: dict, secret_params_keys: list = None):
        """
        Notes:
        1. params with _ prefixed are params used by execution layer and not recognized by data-source

        TODO: What happens if both metastore and customer over-ride provides aws secret arn?
        ```
            "aws_secret_arn": "metastore_specified_arn",
            "_aws_secret_arn": "my_custom_arn",
        ```

        :param params:          the connection properties.
        """

        self._connection_type = None
        self._aws_secret_arn = None

        self._set_instance_variables(params, secret_params_keys)

    def _to_hashable_object(self, obj):
        """
        Converts a given object to a hashable type.
        :param obj:
        :return:
        """
        if isinstance(obj, list):
            return tuple(self._to_hashable_object(element) for element in sorted(obj))
        return obj

    def __hash__(self):
        """
        Note: python `hash` is not guaranteed to produce the same hash value across different executions.
        I.e. Hashes should not be persisted outside of python execution.

        However, one kernel uses a single run of python per notebook. E.g. Hashes will yield consistent
        results for all cells running in a notebook, as long as kernel is not re-started.

        Further note: Functions like hashlib only operate on byte-like objects. All objects may not be easily
        convertible to this notation (All objs are not json-dumpable, and __str__ is not reliable as it can mask items
        -- ref our redaction loigic). Only move to hashlib or other hash alternatives after thorough testing.

        :return: hash from dict
        """

        dct = self.to_dict(include_private_attr=True)
        sorted_keys = sorted(dct.keys())
        members_to_hash = tuple((key, self._to_hashable_object(dct[key])) for key in sorted_keys)
        return hash(members_to_hash)

    def __str__(self):
        return str(self._to_redacted_dict())

    def _to_redacted_dict(self, include_private_attr=False):
        return {k: self._get_redacted_value(k) for k in self.to_dict(include_private_attr).keys()}

    def _get_redacted_value(self, key):
        """
        Returns redacted value if sensitive key, otherwise returns value.
        :param key:
        :return:
        """
        if hasattr(self, "_secret_params_keys") and key in self._secret_params_keys:
            return f"[Secret from {self._aws_secret_arn}]"
        if key in self.DEFAULT_SECRET_PARAMS_KEYS:
            return "******"
        return getattr(self, key)


class SQLExecutionRequest:
    def __init__(
        self,
        query: str,
        query_params: Optional[Dict],
    ):
        self.query = query
        self.queryParams = query_params


class SQLExecutionResponse:
    class ColumnMetadataEntry(SQLParameterMixin):
        def __init__(self, params: dict):
            """
            Python db api cursor description specification specifies the below 7 items
            https://peps.python.org/pep-0249/#description
            """
            self.name = None
            self.type_code = None
            self.precision = None
            self.scale = None
            self.null_ok = None
            self.display_size = None
            self.internal_size = None

            self._set_instance_variables(params)

        def __str__(self):
            return str(vars(self))

    def __init__(self):
        self.column_metadata = None
        self.data = None
        self.next_token = None
