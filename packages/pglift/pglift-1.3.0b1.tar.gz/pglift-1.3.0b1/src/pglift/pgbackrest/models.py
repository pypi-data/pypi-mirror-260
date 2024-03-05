# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from datetime import datetime
from pathlib import Path
from typing import Annotated, Literal, Optional

from attrs import frozen
from pydantic import Field, SecretStr

from .. import types


@frozen
class Service:
    """A pgbackrest service bound to a PostgreSQL instance."""

    stanza: str
    """Name of the stanza"""

    path: Path
    """Path to configuration file for this stanza"""

    index: int = 1
    """index of pg-path option in the stanza"""


class ServiceManifest(types.ServiceManifest, service_name="pgbackrest"):
    stanza: Annotated[
        str,
        Field(
            description=(
                "Name of pgBackRest stanza. "
                "Something describing the actual function of the instance, such as 'app'."
            ),
            json_schema_extra={"readOnly": True},
        ),
    ]
    password: Annotated[
        Optional[SecretStr],
        Field(
            description="Password of PostgreSQL role for pgBackRest.",
            exclude=True,
        ),
    ] = None


class Backup(types.Manifest):
    label: str
    size: types.ByteSize
    repo_size: Annotated[Optional[int], types.ByteSizeType()]
    date_start: datetime
    date_stop: datetime
    type: Literal["incr", "diff", "full"]
    databases: list[str]
