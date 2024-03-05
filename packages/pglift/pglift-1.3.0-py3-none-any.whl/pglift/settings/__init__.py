# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

import grp
import json
import os
import pwd
import tempfile
from collections.abc import Callable
from functools import cached_property
from pathlib import Path
from typing import Annotated, Any, Literal, Optional

import yaml
from pydantic import AfterValidator, Field, ValidationInfo, model_validator
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from .. import __name__ as pkgname
from .. import exceptions, util
from .._compat import Self
from . import (
    _logrotate,
    _patroni,
    _pgbackrest,
    _postgresql,
    _powa,
    _prometheus,
    _rsyslog,
    _systemd,
    _temboard,
)
from .base import prefix_values


def default_postgresql_version(
    settings: _postgresql.Settings,
) -> _postgresql.PostgreSQLVersion:
    if settings.default_version is not None:
        return settings.default_version
    if not settings.versions:
        raise exceptions.SettingsError("empty 'postgresql.versions' setting")
    return max(v.version for v in settings.versions)


def default_prefix(uid: int) -> Path:
    """Return the default path prefix for 'uid'.

    >>> default_prefix(0)
    PosixPath('/')
    >>> default_prefix(42)  # doctest: +ELLIPSIS
    PosixPath('/.../.local/share/pglift')
    """
    if uid == 0:
        return Path("/")
    return util.xdg_data_home() / pkgname


def default_run_prefix(uid: int) -> Path:
    """Return the default run path prefix for 'uid'."""
    if uid == 0:
        base = Path("/run")
    else:
        try:
            base = util.xdg_runtime_dir(uid)
        except exceptions.FileNotFoundError:
            base = Path(tempfile.gettempdir())

    return base / pkgname


def default_sysuser() -> tuple[str, str]:
    pwentry = pwd.getpwuid(os.getuid())
    grentry = grp.getgrgid(pwentry.pw_gid)
    return pwentry.pw_name, grentry.gr_name


class YamlConfigSettingsSource(PydanticBaseSettingsSource):
    """Load settings values 'settings.yaml' file if found in user or system
    config directory directory.
    """

    @staticmethod
    def site_settings_path() -> Optional[Path]:
        """Return content of 'settings.yaml' if found in site configuration
        directories.
        """
        return util.site_config("settings.yaml")

    @cached_property
    def site_settings(self) -> dict[str, Any]:
        if (path := self.site_settings_path()) is None:
            return {}
        settings = yaml.safe_load(path.read_text())
        if not isinstance(settings, dict):
            raise exceptions.SettingsError(
                f"failed to load site settings from {path}, expecting an object"
            )
        return settings

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> tuple[Any, str, bool]:
        return self.site_settings.get(field_name), field_name, False

    def __call__(self) -> dict[str, Any]:
        return self.site_settings


class JsonConfigSettingsSource(PydanticBaseSettingsSource):
    """Load settings values from 'SETTINGS' environment variable.

    If this variable has a value starting with @, it is interpreted as a path
    to a JSON file. Otherwise, a JSON serialization is expected.
    """

    @cached_property
    def env_settings(self) -> dict[str, Any]:
        env_settings = os.getenv("SETTINGS")
        if not env_settings:
            return {}
        if env_settings.startswith("@"):
            config = Path(env_settings[1:])
            encoding = self.config.get("env_file_encoding")
            # May raise FileNotFoundError, which is okay here.
            env_settings = config.read_text(encoding)
        try:
            return json.loads(env_settings)  # type: ignore[no-any-return]
        except json.decoder.JSONDecodeError as e:
            raise exceptions.SettingsError(str(e)) from e

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> tuple[Any, str, bool]:
        return self.env_settings.get(field_name), field_name, False

    def __call__(self) -> dict[str, Any]:
        return self.env_settings


def is_root() -> bool:
    return os.getuid() == 0


def check_path_is_absolute(value: Path) -> Path:
    """Make sure path settings are absolute."""
    if not value.is_absolute():
        raise ValueError("expecting an absolute path")
    return value


def check_service_manager_scheduler(
    v: Optional[Literal["systemd"]], info: ValidationInfo
) -> Optional[Literal["systemd"]]:
    """Make sure systemd is enabled globally when 'service_manager' or 'scheduler' are set."""
    if info.data.get("systemd") is None and v is not None:
        raise ValueError("cannot use systemd, if 'systemd' is not enabled globally")
    return v


def check_patroni_passfile(
    value: Optional[_patroni.Settings], info: ValidationInfo
) -> Optional[_patroni.Settings]:
    try:
        postgresql_settings = info.data["postgresql"]
    except KeyError:  # Another validation probably failed.
        return value
    assert isinstance(postgresql_settings, _postgresql.Settings)
    if (
        value
        and postgresql_settings.auth.passfile
        and value.postgresql.passfile == postgresql_settings.auth.passfile
    ):
        raise ValueError(
            f"'{info.field_name}.postgresql.passfile' must be different from 'postgresql.auth.passfile'"
        )
    return value


def check_patroni_requires_replrole(
    value: Optional[_patroni.Settings], info: ValidationInfo
) -> Optional[_patroni.Settings]:
    try:
        postgresql_settings = info.data["postgresql"]
    except KeyError:  # Another validation probably failed.
        return value
    assert isinstance(postgresql_settings, _postgresql.Settings)
    if value and postgresql_settings.replrole is None:
        raise ValueError("'postgresql.replrole' must be provided to use 'patroni'")
    return value


class Settings(BaseSettings):
    """Settings for pglift."""

    model_config = SettingsConfigDict(frozen=True)

    postgresql: Annotated[
        _postgresql.Settings, Field(default_factory=_postgresql.Settings)
    ]
    patroni: Annotated[
        Optional[_patroni.Settings],
        AfterValidator(check_patroni_passfile),
        AfterValidator(check_patroni_requires_replrole),
    ] = None
    pgbackrest: Optional[_pgbackrest.Settings] = None
    powa: Optional[_powa.Settings] = None
    prometheus: Optional[_prometheus.Settings] = None
    temboard: Optional[_temboard.Settings] = None
    systemd: Optional[_systemd.Settings] = None
    logrotate: Optional[_logrotate.Settings] = None
    rsyslog: Optional[_rsyslog.Settings] = None

    service_manager: Annotated[
        Optional[Literal["systemd"]],
        AfterValidator(check_service_manager_scheduler),
    ] = None
    scheduler: Annotated[
        Optional[Literal["systemd"]],
        AfterValidator(check_service_manager_scheduler),
    ] = None

    prefix: Annotated[
        Path,
        Field(description="Path prefix for configuration and data files."),
        AfterValidator(check_path_is_absolute),
    ] = default_prefix(os.getuid())

    run_prefix: Annotated[
        Path,
        Field(
            description="Path prefix for runtime socket, lockfiles and PID files.",
        ),
        AfterValidator(check_path_is_absolute),
    ] = default_run_prefix(os.getuid())

    sysuser: Annotated[
        tuple[str, str],
        Field(
            default_factory=default_sysuser,
            description=(
                "(username, groupname) of system user running PostgreSQL; "
                "mostly applicable when operating PostgreSQL with systemd in non-user mode"
            ),
        ),
    ]

    @model_validator(mode="wrap")
    @classmethod
    def __prefix_paths_(
        cls, values: dict[str, Any], handler: Callable[[Any], Self]
    ) -> Self:
        """Prefix child settings fields with the global 'prefix'."""
        prefixes = {
            k: values.get(k, cls.model_fields[k].default)
            for k in ("prefix", "run_prefix")
        }
        return handler(prefix_values(handler(values), prefixes))

    @model_validator(mode="before")
    @classmethod
    def __set_service_manager_scheduler_(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Set 'service_manager' and 'scheduler' to 'systemd' by default if systemd is enabled."""
        if values.get("systemd") is not None:
            values.setdefault("service_manager", "systemd")
            values.setdefault("scheduler", "systemd")
        return values

    @model_validator(mode="before")
    @classmethod
    def __validate_is_not_root_(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Make sure current user is not root.

        This is not supported by postgres (cannot call neither initdb nor pg_ctl as root).
        """
        if is_root():
            raise exceptions.UnsupportedError("pglift cannot be used as root")
        return values


class SiteSettings(Settings):
    """Settings loaded from site-sources.

    Load user or site settings from:
    - 'settings.yaml' if found in user or system configuration directory, and,
    - SETTINGS environment variable.
    """

    model_config = SettingsConfigDict(frozen=True)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            JsonConfigSettingsSource(settings_cls),
            YamlConfigSettingsSource(settings_cls),
        )
