# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from typing import List, Optional

from amazon_sagemaker_sql_execution.models.sql_execution import (
    SQLConnectionProperties,
    SQLQueryParameters,
    SQLExecutionResponse,
)

from amazon_sagemaker_sql_execution.utils.constants import CONNECTION_TYPE_SNOWFLAKE


class SnowflakeSQLQueryParameters(SQLQueryParameters):
    def __init__(self, params: Optional[dict] = None):
        super().__init__(params)
        self.params = None
        self.timeout = None
        self._set_instance_variables(params)

    @property
    def parameters(self):
        """
        Snowflake is not consistent with codebase and documentation.
        parameters are referred to as "parameters" in doc, but as "params" in code
        https://github.com/snowflakedb/snowflake-connector-python/blob/main/src/snowflake/connector/cursor.py#L612
        https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-api#object-cursor
        :return:
        """
        return self.params

    @parameters.setter
    def parameters(self, val):
        self.params = val


class SnowflakeSQLConnectionProperties(SQLConnectionProperties):
    def __init__(self, params: dict, secret_params_keys: list = None):
        """
        Fields here MUST have 1:1 mapping with attributes used for snowflake's .connect()
        Any field not used by snowflake's .connect() must be excluded by inserting to internal_only_params
        """
        super().__init__(params=params)
        self.user = None
        self.account = None
        self.password = None
        self.private_key = None
        self.warehouse = None
        self.database = None
        self.schema = None
        self.role = None
        self.login_timeout = None
        self.network_timeout = None
        self.autocommit = None
        self.validate_default_parameters = None
        self.paramstyle = None
        self.timezone = None
        self.arrow_number_to_decimal = None

        self._connection_type = CONNECTION_TYPE_SNOWFLAKE

        # attributes to support private key based auth
        self._pk_pem_path = None
        self._pk_passphrase = None

        self._set_instance_variables(params, secret_params_keys)
        self._set_private_key()

    def _get_encoded_passphrase(self):
        if self._pk_passphrase is not None:
            return self._pk_passphrase.encode()
        return None

    def _set_private_key(self):
        # Reference: https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-connect#using-key-pair-authentication-key-pair-rotation
        if self._pk_pem_path and self.private_key is None:
            with open(self._pk_pem_path, "rb") as key:
                p_key = serialization.load_pem_private_key(
                    key.read(),
                    password=self._get_encoded_passphrase(),
                    backend=default_backend(),
                )

            self.private_key = p_key.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )


class SnowflakeSQLExecutionResponse(SQLExecutionResponse):
    class SnowflakeColumnMetadataEntry(SQLExecutionResponse.ColumnMetadataEntry):
        def __init__(self, params):
            dct = params._asdict()
            super().__init__(dct)

            # Snowflake differs from DB API in its nullable field:
            # https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-api#description
            self.null_ok = dct["is_nullable"]

    # cursor_desc: List[ResultMetadata]
    def __init__(self, data: "List[tuple] | List[dict]", cursor_desc: List[object]):
        super().__init__()
        self.column_metadata = [
            SnowflakeSQLExecutionResponse.SnowflakeColumnMetadataEntry(data) for data in cursor_desc
        ]
        self.data = data
