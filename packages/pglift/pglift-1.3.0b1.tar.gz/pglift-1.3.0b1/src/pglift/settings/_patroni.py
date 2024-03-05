# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from typing import Annotated, Any, Literal, Optional

from pydantic import AfterValidator, DirectoryPath, Field, FilePath, ValidationInfo

from .. import types
from .base import BaseModel, ConfigPath, LogPath, RunPath, TemplatedPath


def check_cert_and_protocol(
    value: Optional[FilePath], info: ValidationInfo
) -> Optional[FilePath]:
    """Make sure protocol https is used when setting certificates."""
    if value is not None and info.data["protocol"] == "http":
        raise ValueError("'https' protocol is required")
    return value


class Etcd(BaseModel):
    """Settings for Etcd (for Patroni)."""

    v2: Annotated[bool, Field(description="Configure Patroni to use etcd v2.")] = False

    hosts: Annotated[
        tuple[types.Address, ...], Field(description="List of etcd endpoint.")
    ] = (types.local_address(2379),)

    protocol: Annotated[
        Literal["http", "https"],
        Field(description="http or https, if not specified http is used."),
    ] = "http"

    cacert: Annotated[
        Optional[FilePath],
        Field(description="Certificate authority to validate the server certificate."),
        AfterValidator(check_cert_and_protocol),
    ] = None

    cert: Annotated[
        Optional[FilePath],
        Field(description="Client certificate for authentication."),
        AfterValidator(check_cert_and_protocol),
    ] = None

    key: Annotated[
        Optional[FilePath],
        Field(description="Private key corresponding to the client certificate."),
    ] = None


def check_path_exists(value: Path) -> Path:
    if value and not value.exists():
        raise ValueError(f"path {value} does not exists")
    return value


class WatchDog(BaseModel):
    """Settings for watchdog (for Patroni)."""

    mode: Annotated[
        Literal["off", "automatic", "required"], Field(description="watchdog mode.")
    ] = "off"

    device: Annotated[
        Optional[Path],
        Field(description="Path to watchdog."),
        AfterValidator(check_path_exists),
    ] = None

    safety_margin: Annotated[
        Optional[int],
        Field(
            description="Number of seconds of safety margin between watchdog triggering and leader key expiration."
        ),
    ] = None


def check_verify_client_and_certfile(
    value: Optional[Any], info: ValidationInfo
) -> Optional[Any]:
    """Make sure that certfile is set when verify_client is."""
    if value is not None and info.data.get("certfile") is None:
        raise ValueError("requires 'certfile' to enable TLS")
    return value


class RESTAPI(BaseModel):
    """Settings for Patroni's REST API."""

    cafile: Annotated[
        Optional[FilePath],
        Field(
            description="Certificate authority (or bundle) to verify client certificates."
        ),
    ] = None

    certfile: Annotated[
        Optional[FilePath],
        Field(description="PEM-encoded server certificate to enable HTTPS."),
    ] = None

    keyfile: Annotated[
        Optional[FilePath],
        Field(
            description="PEM-encoded private key corresponding to the server certificate."
        ),
    ] = None

    verify_client: Annotated[
        Optional[Literal["optional", "required"]],
        Field(description="Whether to check client certificates."),
        AfterValidator(check_verify_client_and_certfile),
    ] = None


class CTL(BaseModel):
    """Settings for Patroni's CTL."""

    certfile: Annotated[FilePath, Field(description="PEM-encoded client certificate.")]

    keyfile: Annotated[
        FilePath,
        Field(
            description="PEM-encoded private key corresponding to the client certificate."
        ),
    ]


class ServerSSLOptions(BaseModel):
    """Settings for server certificate verification."""

    mode: Annotated[
        Optional[
            Literal[
                "disable",
                "allow",
                "prefer",
                "require",
                "verify-ca",
                "verify-full",
            ]
        ],
        Field(description="Verification mode."),
    ] = None
    crl: Annotated[
        Optional[FilePath], Field(description="Certificate Revocation List (CRL).")
    ] = None
    crldir: Annotated[
        Optional[DirectoryPath], Field(description="Directory with CRL files.")
    ] = None
    rootcert: Annotated[
        Optional[FilePath], Field(description="Root certificate(s).")
    ] = None


class ConnectionOptions(BaseModel):
    ssl: Annotated[
        Optional[ServerSSLOptions],
        Field(
            description="Settings for server certificate verification when connecting to remote PostgreSQL instances."
        ),
    ] = None


class PostgreSQL(BaseModel):
    connection: Annotated[
        Optional[ConnectionOptions],
        Field(
            description="Client (libpq) connection options.",
        ),
    ] = None
    passfile: Annotated[
        Path,
        AfterValidator(TemplatedPath("name")),
        ConfigPath,
        Field(
            description="Path to .pgpass password file managed by Patroni.",
            validate_default=True,
        ),
    ] = Path("patroni/{name}.pgpass")
    use_pg_rewind: Annotated[
        bool, Field(description="Whether or not to use pg_rewind.")
    ] = False


def check_restapi_verify_client(value: RESTAPI, info: ValidationInfo) -> RESTAPI:
    """Make sure 'ctl' client certificates are provided when setting
    restapi.verify_client to required.
    """
    if value.verify_client == "required" and info.data.get("ctl") is None:
        raise ValueError(
            f"'ctl' must be provided when '{info.field_name}.verify_client' is set to 'required'"
        )
    return value


class Settings(BaseModel):
    """Settings for Patroni."""

    execpath: Annotated[FilePath, Field(description="Path to patroni executable.")] = (
        Path("/usr/bin/patroni")
    )

    configpath: Annotated[
        Path,
        AfterValidator(TemplatedPath("name")),
        ConfigPath,
        Field(description="Path to the config file.", validate_default=True),
    ] = Path("patroni/{name}.yaml")

    logpath: Annotated[
        Path,
        LogPath,
        Field(
            description="Path where directories are created (based on instance name) to store patroni log files.",
        ),
    ] = Path("patroni")

    pid_file: Annotated[
        Path,
        AfterValidator(TemplatedPath("name")),
        RunPath,
        Field(
            description="Path to which Patroni process PID will be written.",
            validate_default=True,
        ),
    ] = Path("patroni/{name}.pid")

    loop_wait: Annotated[
        int, Field(description="Number of seconds the loop will sleep.")
    ] = 10

    etcd: Annotated[Etcd, Field(default_factory=Etcd, description="Etcd settings.")]

    watchdog: Annotated[
        WatchDog, Field(default_factory=WatchDog, description="Watchdog settings.")
    ]

    ctl: Annotated[Optional[CTL], Field(description="CTL settings.")] = None

    postgresql: Annotated[
        PostgreSQL,
        Field(default_factory=PostgreSQL, description="PostgreSQL settings."),
    ]

    restapi: Annotated[
        RESTAPI,
        Field(default_factory=RESTAPI, description="REST API settings."),
        AfterValidator(check_restapi_verify_client),
    ]
