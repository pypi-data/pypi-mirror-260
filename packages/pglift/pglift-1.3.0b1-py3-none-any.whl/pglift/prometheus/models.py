# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Mapping
from functools import partial
from pathlib import Path
from typing import Annotated, ClassVar, Final, Literal, Optional

from attrs import frozen
from pydantic import AfterValidator, Field, SecretStr

from .. import exceptions, types
from ..models.helpers import check_conninfo, check_excludes
from ..settings._prometheus import Settings
from ..types import Port
from . import impl

default_port: Final = 9187
service_name: Final = "postgres_exporter"


@frozen
class Config:
    values: Mapping[str, str]
    path: Path

    def __getitem__(self, key: str) -> str:
        try:
            return self.values[key]
        except KeyError as e:
            raise exceptions.ConfigurationError(self.path, f"{key} not found") from e


@frozen
class Service:
    """A Prometheus postgres_exporter service bound to a PostgreSQL instance."""

    __service_name__: ClassVar[str] = service_name

    name: str
    """Identifier for the service, usually the instance qualname."""

    settings: Settings

    port: int
    """TCP port for the web interface and telemetry."""

    password: Optional[SecretStr]

    def __str__(self) -> str:
        return f"{self.__service_name__}@{self.name}"

    def args(self) -> list[str]:
        config = impl._config(impl._configpath(self.name, self.settings))
        return impl._args(self.settings.execpath, config)

    def pidfile(self) -> Path:
        return impl._pidfile(self.name, self.settings)

    def env(self) -> dict[str, str]:
        config = impl._config(impl._configpath(self.name, self.settings))
        return impl._env(config)


def check_password(v: Optional[SecretStr]) -> Optional[SecretStr]:
    """Validate 'password' field.

    >>> ServiceManifest(password='without_space')  # doctest: +ELLIPSIS
    ServiceManifest(...)
    >>> ServiceManifest(password='with space')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for ServiceManifest
    password
      Value error, password must not contain blank spaces [type=value_error, input_value='with space', input_type=str]
        ...
    """
    # Avoid spaces as this will break postgres_exporter configuration.
    # See https://github.com/prometheus-community/postgres_exporter/issues/393
    if v is not None and " " in v.get_secret_value():
        raise ValueError("password must not contain blank spaces")
    return v


class ServiceManifest(types.ServiceManifest, service_name="prometheus"):
    port: Annotated[
        Port,
        Field(description="TCP port for the web interface and telemetry of Prometheus"),
    ] = default_port
    password: Annotated[
        Optional[SecretStr],
        Field(
            description="Password of PostgreSQL role for Prometheus postgres_exporter.",
            exclude=True,
        ),
        AfterValidator(check_password),
    ] = None


class PostgresExporter(types.Manifest):
    """Prometheus postgres_exporter service."""

    """
    >>> PostgresExporter(name='without-slash', dsn="", port=12)  # doctest: +ELLIPSIS
    PostgresExporter(name='without-slash', ...)
    >>> PostgresExporter(name='with/slash', dsn="", port=12)
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for PostgresExporter
    name
      Value error, must not contain slashes [type=value_error, input_value='with/slash', input_type=str]
        ...
    """

    name: Annotated[
        str,
        Field(description="locally unique identifier of the service"),
        AfterValidator(partial(check_excludes, ("/", "slashes"))),
    ]
    dsn: Annotated[
        str,
        Field(description="connection string of target instance"),
        AfterValidator(partial(check_conninfo, exclude=[])),
    ]
    password: Annotated[
        Optional[SecretStr], Field(description="connection password")
    ] = None
    port: Annotated[
        int, Field(description="TCP port for the web interface and telemetry")
    ]
    state: Annotated[
        Literal["started", "stopped", "absent"],
        types.CLIConfig(choices=["started", "stopped"]),
        Field(description="runtime state"),
    ] = "started"
