# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


class SQLParameterMixin:
    # The default keys which will be obfuscated with ***** when printing connection_parameters.
    DEFAULT_SECRET_PARAMS_KEYS = ["password", "private_key", "pk_passphrase"]

    def _set_instance_variables(self, params, secret_params_keys=None):
        """
        Set the instance variables to the parameters provided.

        Sets parameters in the following priority:
        1. Tries to set internal parameter (params starting with `_`) if that exists
        2. Sets the parameter as-is if the above condition fails

        :param params:
        :return: None
        """
        if secret_params_keys is None:
            secret_params_keys = []
        secret_keys = []

        if params is not None:
            for k, v in params.items():
                internal_parameter_name = "_" + k

                if hasattr(self, internal_parameter_name):
                    setattr(self, internal_parameter_name, v)
                    if internal_parameter_name in secret_params_keys:
                        secret_keys.append(internal_parameter_name)
                else:
                    # Adds all other properties in params to self.
                    #
                    # This branch allows customer to pass in custom properties. Use case, when connector pkg
                    # supports new properties, this allows customer to benefit before execution lib is updated to
                    # support these new properties.
                    #
                    # Add a new else branch to allow adding differentiating logic on pre-defined and
                    # non-pre-defined properties later.
                    #
                    # For connection use case, either the underlying connector ignores the unknown properties or
                    # have strict validation to fail the connection.
                    setattr(self, k, v)
                    if k in secret_params_keys:
                        secret_keys.append(k)

        if secret_keys and len(secret_keys) != 0:
            self._secret_params_keys = secret_keys

    def to_dict(self, include_private_attr=False):
        """
        Converts parameters to a dictionary which can be used to directly create or execute a
        connection.

        1. Removes None params
        2. Removes internal params (params starting with `_`) if include_private_attr is True

        :return: dictionary with connector-specific connection properties
        """

        return {
            k: v
            for k, v in vars(self).items()
            if v is not None
            and (include_private_attr or not k.startswith("_"))
            and "_secret_params_keys" != k
        }
