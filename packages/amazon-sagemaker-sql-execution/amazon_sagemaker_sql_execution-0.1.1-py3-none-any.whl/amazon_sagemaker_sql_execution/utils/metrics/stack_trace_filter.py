# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import re

from amazon_sagemaker_sql_execution.utils.constants import (
    EMAIL_REGEX,
    PHONE_NUMBER_REGEX,
    PASSWORD_REGEX,
    API_KEY_REGEX,
    AWS_SECRETKEY_REGEX,
)


class StackTraceFilter:
    def __init__(self):
        # Define patterns for potentially sensitive data
        self.patterns = [
            (re.compile(EMAIL_REGEX), "<EMAIL>"),
            (re.compile(PHONE_NUMBER_REGEX), "<PHONE>"),
            (re.compile(PASSWORD_REGEX), "<SECRET>"),
            (re.compile(API_KEY_REGEX), "<SECRET>"),
            (re.compile(AWS_SECRETKEY_REGEX), "<AWS_SECRET>"),
        ]

    def filter(self, stack_trace: str) -> str:
        """Filter sensitive data from the given stack trace."""
        for pattern, replacement in self.patterns:
            stack_trace = re.sub(pattern, replacement, stack_trace)
        return stack_trace
