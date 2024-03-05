# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

import socket
from typing import Annotated, Optional

from pydantic import Field, FilePath, SecretStr, field_validator

from ... import types
from .common import RESTAPI


class ClusterMember(types.BaseModel, extra="allow", frozen=True):
    """An item of the list of members returned by Patroni API /cluster endpoint."""

    host: str
    name: str
    port: int
    role: str
    state: str


class ClientSSLOptions(types.BaseModel):
    cert: Annotated[FilePath, Field(description="Client certificate.")]
    key: Annotated[FilePath, Field(description="Private key.")]
    password: Annotated[
        Optional[SecretStr], Field(description="Password for the private key.")
    ] = None


class ClientAuth(types.BaseModel):
    ssl: Annotated[
        Optional[ClientSSLOptions], Field(description="Client certificate options.")
    ] = None


class PostgreSQL(types.BaseModel):
    connect_host: Annotated[
        Optional[str],
        Field(
            description="Host or IP address through which PostgreSQL is externally accessible.",
        ),
    ] = None
    replication: Annotated[
        Optional[ClientAuth],
        Field(
            description="Authentication options for client (libpq) connections to remote PostgreSQL by the replication user.",
        ),
    ] = None
    rewind: Annotated[
        Optional[ClientAuth],
        Field(
            description="Authentication options for client (libpq) connections to remote PostgreSQL by the rewind user.",
        ),
    ] = None


class Etcd(types.BaseModel):
    username: Annotated[
        str,
        Field(
            description="Username for basic authentication to etcd.",
        ),
    ]
    password: Annotated[
        SecretStr, Field(description="Password for basic authentication to etcd.")
    ]


class ServiceManifest(types.ServiceManifest, service_name="patroni"):
    # XXX Or simply use instance.qualname?
    cluster: Annotated[
        str,
        Field(
            description="Name (scope) of the Patroni cluster.",
            json_schema_extra={"readOnly": True},
        ),
    ]
    node: Annotated[
        str,
        Field(
            default_factory=socket.getfqdn,
            description="Name of the node (usually the host name).",
            json_schema_extra={"readOnly": True},
        ),
    ]
    restapi: Annotated[
        RESTAPI, Field(default_factory=RESTAPI, description="REST API configuration")
    ]

    postgresql: Annotated[
        Optional[PostgreSQL],
        Field(
            description="Configuration for PostgreSQL setup and remote connection.",
        ),
    ] = None
    etcd: Annotated[
        Optional[Etcd],
        Field(description="Instance-specific options for etcd DCS backend."),
    ] = None
    cluster_members: Annotated[
        list[ClusterMember],
        types.CLIConfig(hide=True),
        types.AnsibleConfig(hide=True),
        Field(
            description="Members of the Patroni this instance is member of.",
            json_schema_extra={"readOnly": True},
        ),
    ] = []

    __validate_none_values_ = field_validator("node", "restapi", mode="before")(
        classmethod(types.default_if_none)
    )
