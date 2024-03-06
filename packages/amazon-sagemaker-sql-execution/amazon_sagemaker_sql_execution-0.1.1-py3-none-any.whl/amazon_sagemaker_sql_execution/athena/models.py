# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
from typing import Type, Dict, Any, Optional, Tuple, List
import time

from pyathena.common import BaseCursor, CursorIterator
from pyathena.converter import Converter
from pyathena.cursor import Cursor
from pyathena.formatter import Formatter
from pyathena.util import RetryConfig

from amazon_sagemaker_sql_execution.models.sql_execution import (
    SQLConnectionProperties,
    SQLQueryParameters,
    SQLExecutionResponse,
)

from amazon_sagemaker_sql_execution.utils.constants import CONNECTION_TYPE_ATHENA


class AthenaSQLQueryParameters(SQLQueryParameters):
    def __init__(self, params: Optional[dict] = None) -> None:
        super().__init__(params)
        """
        The AthenaSQLQueryParameters object allows client to pass in per execution configuration including query params,
        work group, s3 staging folder and query behavior customization.
        ref: https://github.com/laughingman7743/PyAthena/blob/master/pyathena/cursor.py#L89
        """
        self.parameters: Optional[Dict[str, Any]] = None

        self.work_group: Optional[str] = None
        self.s3_staging_dir: Optional[str] = None
        self.cache_size: int = 0
        self.cache_expiration_time: int = 0
        self.result_reuse_enable: Optional[bool] = None
        self.result_reuse_minutes: Optional[int] = None

        self._set_instance_variables(params)


class AthenaSQLConnectionProperties(SQLConnectionProperties):
    def __init__(self, params: dict, secret_params_keys: list = None):
        """
        Fields in this connection properties object are 1:1 mapping with attributes used for creating the connection.
        ref: https://github.com/laughingman7743/PyAthena/blob/master/pyathena/connection.py#L49
        """
        super().__init__(params=params)

        self.s3_staging_dir: Optional[str] = None
        self.region_name: Optional[str] = None
        self.schema_name: Optional[str] = "default"
        self.catalog_name: Optional[str] = "awsdatacatalog"
        self.work_group: Optional[str] = None
        self.poll_interval: float = 1
        self.encryption_option: Optional[str] = None
        self.kms_key: Optional[str] = None

        self.profile_name: Optional[str] = None
        self.role_arn: Optional[str] = None

        # role_session_name is not supported in Glue connection config
        self.role_session_name: str = f"sm-studio-session-{int(time.time())}"
        self.duration_seconds: int = 3600
        self.aws_access_key_id = None
        self.aws_secret_access_key = None

        # Following 5 attributes are not supported in Glue connection config. They can be configured in library mode.
        self.converter: Optional[Converter] = None
        self.formatter: Optional[Formatter] = None
        self.retry_config: Optional[RetryConfig] = None
        self.cursor_class: Type[BaseCursor] = Cursor
        self.cursor_kwargs: Optional[Dict[str, Any]] = None

        self.result_reuse_enable: bool = False
        self.result_reuse_minutes: int = CursorIterator.DEFAULT_RESULT_REUSE_MINUTES

        self._connection_type = CONNECTION_TYPE_ATHENA
        self._set_instance_variables(params, secret_params_keys)


class AthenaSQLExecutionResponse(SQLExecutionResponse):
    class AthenaColumnMetadataEntry(SQLExecutionResponse.ColumnMetadataEntry):
        def __init__(self, params: Optional[Tuple]):
            super().__init__(self._to_dict(params))

        def _to_dict(self, params: Optional[Tuple]):
            # ref: https://github.com/laughingman7743/PyAthena/blob/master/pyathena/result_set.py#L264
            dct = {}
            if params is not None:
                dct["name"] = params[0]
                dct["type_code"] = params[1]
                dct["precision"] = params[4]
                dct["scale"] = params[5]
                dct["null_ok"] = params[6]
            return dct

    def __init__(self, data: "List[tuple] | List[dict]", cursor_desc: List[Tuple]):
        super().__init__()
        self.column_metadata = [
            AthenaSQLExecutionResponse.AthenaColumnMetadataEntry(data) for data in cursor_desc
        ]
        self.data = data
