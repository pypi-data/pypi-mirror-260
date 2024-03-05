# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

import typing
from decimal import Decimal
from functools import partial
from typing import Annotated, Literal, Optional

import psycopg.conninfo
from pydantic import AfterValidator, Field, SecretStr

from ..models.helpers import check_conninfo
from ..types import AnsibleConfig, CLIConfig, Manifest

WALSenderState = Literal["startup", "catchup", "streaming", "backup", "stopping"]


def walsender_state(value: str) -> WALSenderState:
    assert value in typing.get_args(
        WALSenderState
    ), f"unexpected WAL sender state {value!r}"
    return value  # type: ignore[return-value]


class Standby(Manifest):
    """Standby information."""

    """Validate 'primary_conninfo' field.

    >>> Standby.model_validate({"primary_conninfo": "host=localhost"})  # doctest: +ELLIPSIS
    Standby(primary_conninfo='host=localhost', password=None, ...)
    >>> Standby.model_validate({"primary_conninfo": "hello"})
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Standby
    primary_conninfo
      Value error, missing "=" after "hello" in connection info string
     [type=value_error, input_value='hello', input_type=str]
        ...
    >>> Standby.model_validate({"primary_conninfo": "host=localhost password=xx"})
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Standby
    primary_conninfo
      Value error, must not contain a password [type=value_error, input_value='host=localhost password=xx', input_type=str]
        ...
    """

    primary_conninfo: Annotated[
        str,
        CLIConfig(name="for"),
        Field(
            description="DSN of primary for streaming replication.",
            json_schema_extra={"readOnly": True},
        ),
        AfterValidator(partial(check_conninfo, exclude=[("password", "a password")])),
    ]
    password: Annotated[
        Optional[SecretStr],
        Field(
            description="Password for the replication user.",
            exclude=True,
            json_schema_extra={"readOnly": True},
        ),
    ] = None
    status: Annotated[
        Literal["demoted", "promoted"],
        CLIConfig(hide=True),
        Field(
            description="Instance standby state.",
            json_schema_extra={"writeOnly": True},
            exclude=True,
        ),
    ] = "demoted"
    slot: Annotated[
        Optional[str],
        Field(
            description="Replication slot name. Must exist on primary.",
            json_schema_extra={"readOnly": True},
        ),
    ] = None
    replication_lag: Annotated[
        Optional[Decimal],
        CLIConfig(hide=True),
        AnsibleConfig(hide=True),
        Field(
            description="Replication lag.",
            json_schema_extra={"readOnly": True},
        ),
    ] = None
    wal_sender_state: Annotated[
        Optional[WALSenderState],
        CLIConfig(hide=True),
        AnsibleConfig(hide=True),
        Field(
            description="State of the WAL sender process (on primary) this standby is connected to.",
            json_schema_extra={"readOnly": True},
        ),
    ] = None

    @property
    def full_primary_conninfo(self) -> str:
        """Connection string to the primary, including password.

        >>> s = Standby.model_validate({"primary_conninfo": "host=primary port=5444", "password": "qwerty"})
        >>> s.full_primary_conninfo
        'host=primary port=5444 password=qwerty'
        """
        kw = {}
        if self.password:
            kw["password"] = self.password.get_secret_value()
        return psycopg.conninfo.make_conninfo(self.primary_conninfo, **kw)
