# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from typing import List, Optional, Tuple

from amazon_sagemaker_sql_execution.models.sql_execution import (
    SQLConnectionProperties,
    SQLQueryParameters,
    SQLExecutionResponse,
)

from amazon_sagemaker_sql_execution.utils.constants import CONNECTION_TYPE_REDSHIFT


class RedshiftSQLQueryParameters(SQLQueryParameters):
    def __init__(
        self,
        parameters: "Dict[Any, Any] | List[Any] | None" = None,
    ):
        super().__init__(parameters)
        # Redshift uses `args` to refer to params to be bound to statement.
        # Ref: https://github.com/aws/amazon-redshift-python-driver/blob/2898d86de9bb6be1e3def88e15c78c9ea767ec52/redshift_connector/cursor.py#L202
        self.args = None
        self._set_instance_variables(parameters)

    @property
    def parameters(self):
        # Redshift uses `args` to refer to params to be bound to statement.
        # Ref: https://github.com/aws/amazon-redshift-python-driver/blob/2898d86de9bb6be1e3def88e15c78c9ea767ec52/redshift_connector/cursor.py#L202
        return self.args

    @parameters.setter
    def parameters(self, val):
        self.args = val


class RedshiftSQLConnectionProperties(SQLConnectionProperties):
    def __init__(self, params: dict, secret_params_keys: list = None):
        """
        Fields here MUST have 1:1 mapping with attributes used for Redshift's .connect()
        Any field not used by Redshift's .connect() must be excluded by inserting to internal_only_params

        Note that several type-hints below differ from `redshift_connector/redshift_property.py` type hints to allow
        for optional values
        """
        self._engine: Optional[str] = None

        super().__init__(params=params)

        self.access_key_id: Optional[str] = None
        self.auto_create: Optional[bool] = None
        self.cluster_identifier: Optional[str] = None
        self.db_groups: Optional[List[str]] = None
        self.db_user: Optional[str] = None
        self.database: Optional[str] = None
        self.database_metadata_current_db_only: Optional[bool] = None
        self.host: Optional[str] = None
        self.iam: Optional[bool] = None
        self.iam_disable_cache: Optional[bool] = None
        self.max_prepared_statements: Optional[int] = None
        self.numeric_to_float: Optional[bool] = None
        self.password: Optional[str] = None
        self.port: Optional[int] = None
        self.profile: Optional[str] = None
        self.region: Optional[str] = None
        """
        Note that Redshift differs in documentation and actual code.
        https://docs.aws.amazon.com/redshift/latest/mgmt/python-configuration-options.html#python-database-option
        https://github.com/aws/amazon-redshift-python-driver/blob/b2dde82ec9156e2adcc801ac54c051f3cfe61e33/redshift_connector/__init__.py#L112
        """
        self.secret_access_key: Optional[str] = None
        self.serverless_acct_id: Optional[str] = None
        self.serverless_work_group: Optional[str] = None
        self.ssl: Optional[bool] = None
        self.sslmode: Optional[str] = None
        self.timeout: Optional[int] = None
        self.user: Optional[str] = None

        self._connection_type = CONNECTION_TYPE_REDSHIFT
        self._set_instance_variables(params, secret_params_keys)

    @property
    def username(self):
        """
        In AWS Secrets manager, if you choose to store secret of type REDSHIFT CLUSTER,
        The `key/value` asked is `username`, but the python connector expects `user` key.
        :return:
        """
        return self.user

    @username.setter
    def username(self, val: str):
        self.user = val

    @property
    def secret_access_key_id(self):
        return self.secret_access_key

    @secret_access_key_id.setter
    def secret_access_key_id(self, val):
        self.secret_access_key = val

    @property
    def dbClusterIdentifier(self):
        """
        In AWS Secrets manager, if you choose to store secret of type REDSHIFT CLUSTER,
        secret manager can automatically add `dbClusterIdentifier`, but the python connector expects `cluster_identifier` key.
        :return:
        """
        return self.cluster_identifier

    @dbClusterIdentifier.setter
    def dbClusterIdentifier(self, val):
        self.cluster_identifier = val

    @property
    def engine(self):
        """
        In AWS Secrets manager, if you choose to store secret of type REDSHIFT CLUSTER,
        secret manager can automatically add `engine`, but the python connector doesn't support it.
        That is why we make it an internal property
        :return:
        """
        return self._engine

    @engine.setter
    def engine(self, val):
        self._engine = val


class RedshiftSQLExecutionResponse(SQLExecutionResponse):
    class RedshiftColumnMetadataEntry(SQLExecutionResponse.ColumnMetadataEntry):
        def __init__(self, params: Optional[Tuple]):
            super().__init__(self._to_dict(params))

        def _to_dict(self, params: Optional[Tuple]):
            """
            Converts redshift-provided params result to the dict expected by ColumnMetadataEntry
            :param params:
            :return:
            """
            """
            Redshift only returns col name and col type. Others are hard-coded to None.
            https://github.com/aws/amazon-redshift-python-driver/blob/2898d86de9bb6be1e3def88e15c78c9ea767ec52/redshift_connector/cursor.py#L183
            """
            dct = {}
            if params is not None:
                dct["name"] = params[0]
                dct["type_code"] = params[1]
            return dct

    def __init__(self, data: "List[tuple] | List[dict] | tuple", cursor_desc: List):
        super().__init__()
        self.column_metadata = [
            RedshiftSQLExecutionResponse.RedshiftColumnMetadataEntry(data) for data in cursor_desc
        ]
        self.data = data
