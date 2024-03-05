# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any, ClassVar, TypeVar

import psycopg.conninfo
import pydantic
from attrs import asdict, field, frozen
from attrs.validators import instance_of
from pgtoolkit.conf import Configuration

from .. import conf, exceptions, h, hooks
from .._compat import Self
from ..settings import Settings, default_postgresql_version
from ..settings._postgresql import PostgreSQLVersion


@frozen
class BaseInstance:
    name: str
    version: PostgreSQLVersion = field(converter=PostgreSQLVersion)

    bindir: Path = field(init=False)
    _settings: Settings = field(validator=instance_of(Settings))

    def __attrs_post_init__(self) -> None:
        for v in self._settings.postgresql.versions:
            if self.version == v.version:
                object.__setattr__(self, "bindir", v.bindir)
                break
        else:
            raise exceptions.InvalidVersion(
                f"version {self.version} unsupported in site settings"
            )

    def __str__(self) -> str:
        return f"{self.version}/{self.name}"

    @property
    def qualname(self) -> str:
        """Version qualified name, e.g. 13-main."""
        return f"{self.version}-{self.name}"

    @property
    def datadir(self) -> Path:
        """Path to data directory for this instance."""
        return Path(
            str(self._settings.postgresql.datadir).format(
                version=self.version, name=self.name
            )
        )

    @property
    def waldir(self) -> Path:
        """Path to WAL directory for this instance."""
        return Path(
            str(self._settings.postgresql.waldir).format(
                version=self.version, name=self.name
            )
        )

    @property
    def dumps_directory(self) -> Path:
        """Path to directory where database dumps are stored."""
        return Path(
            str(self._settings.postgresql.dumps_directory).format(
                version=self.version, name=self.name
            )
        )

    @property
    def psqlrc(self) -> Path:
        return self.datadir / ".psqlrc"

    @property
    def psql_history(self) -> Path:
        return self.datadir / ".psql_history"

    def notfound(self, hint: str | None = None) -> exceptions.InstanceNotFound:
        return exceptions.InstanceNotFound(str(self), hint)

    def check(self) -> None:
        """Check if the instance exists based on system lookup.

        :raises ~exceptions.InvalidVersion: if PG_VERSION content does not
            match declared version
        :raises ~pglift.exceptions.InstanceNotFound: if PGDATE does not exist
        """
        if not self.datadir.exists():
            raise self.notfound("data directory does not exist")
        try:
            real_version = (self.datadir / "PG_VERSION").read_text().splitlines()[0]
        except FileNotFoundError:
            raise self.notfound("PG_VERSION file not found") from None
        if real_version != self.version:
            raise exceptions.InvalidVersion(
                f"version mismatch ({real_version} != {self.version})"
            )

    @classmethod
    def get(cls, name: str, version: str | None, settings: Settings) -> Self:
        """Return a BaseInstance object from specified name and version.

        :raises ~exceptions.InvalidVersion: if PostgreSQL executable directory
            (bindir) does not exist for specified version.
        """
        # attrs strip leading underscores at init for private attributes.
        if version is None:
            version = default_postgresql_version(settings.postgresql)
        else:
            version = PostgreSQLVersion(version)
        return cls(name, version, settings=settings)


@frozen
class Standby:
    primary_conninfo: str
    slot: str | None
    password: pydantic.SecretStr | None

    @classmethod
    def system_lookup(cls, instance: PostgreSQLInstance) -> Self | None:
        standbyfile = (
            "standby.signal"
            if instance.version >= PostgreSQLVersion.v12
            else "recovery.conf"
        )
        if not (instance.datadir / standbyfile).exists():
            return None
        config = instance.config()
        try:
            dsn = config["primary_conninfo"]
        except KeyError:
            return None
        if not dsn:
            return None
        assert isinstance(dsn, str), dsn
        primary_conninfo = psycopg.conninfo.conninfo_to_dict(dsn)
        try:
            password = pydantic.SecretStr(primary_conninfo.pop("password"))
        except KeyError:
            password = None
        slot = config.get("primary_slot_name")
        if slot is not None:
            assert isinstance(slot, str), slot
        return cls(
            primary_conninfo=psycopg.conninfo.make_conninfo(**primary_conninfo),
            slot=slot or None,
            password=password,
        )


@frozen
class PostgreSQLInstance(BaseInstance):
    """A bare PostgreSQL instance."""

    @classmethod
    def system_lookup(
        cls, value: BaseInstance | tuple[str, str | None, Settings]
    ) -> Self:
        """Build a (real) instance by system lookup.

        :param value: either a BaseInstance object or a (name, version) tuple.

        :raises ~exceptions.InstanceNotFound: if the instance could not be
            found by system lookup.
        """
        if not isinstance(value, BaseInstance):
            try:
                name, version, settings = value
            except ValueError as e:
                raise TypeError(
                    "expecting either a BaseInstance or a (name, version) tuple as 'value' argument"
                ) from e
            try:
                self = cls.get(name, version, settings)
            except exceptions.InvalidVersion as e:
                raise exceptions.InstanceNotFound(f"{version}/{name}") from e
        else:
            self = cls(value.name, value.version, settings=value._settings)
        self.check()
        return self

    @property
    def standby(self) -> Standby | None:
        return Standby.system_lookup(self)

    @classmethod
    def from_qualname(cls, value: str, settings: Settings) -> Self:
        """Lookup for an Instance by its qualified name."""
        try:
            version, name = value.split("-", 1)
        except ValueError:
            raise ValueError(f"invalid qualified name {value!r}") from None
        return cls.system_lookup((name, version, settings))

    def check(self) -> None:
        """Check if the instance exists and its configuration is valid.

        :raises ~pglift.exceptions.InstanceNotFound: if configuration cannot
            be read
        """
        super().check()
        try:
            self.config()
        except FileNotFoundError as e:
            raise self.notfound(str(e)) from e

    def config(self, managed_only: bool = False) -> Configuration:
        """Return parsed PostgreSQL configuration for this instance.

        Refer to :func:`pglift.conf.read` for complete documentation.
        """
        try:
            return conf.read(self.datadir, managed_only=managed_only)
        except exceptions.FileNotFoundError:
            if managed_only:
                return Configuration()
            raise

    @property
    def port(self) -> int:
        """TCP port the server listens on."""
        return int(self.config().get("port", 5432))  # type: ignore[arg-type]

    @property
    def socket_directory(self) -> str | None:
        """Directory path in which the socket should be.

        This is determined from 'unix_socket_directories' configuration entry,
        only considering the first item not starting with @. None if that
        setting is not defined.
        """
        if value := self.config().get("unix_socket_directories"):
            assert isinstance(value, str)
            for sdir in value.split(","):
                sdir = sdir.strip()
                if not sdir.startswith("@"):
                    return sdir
        return None


@frozen
class Instance(PostgreSQLInstance):
    """A PostgreSQL instance with satellite services."""

    services: list[Any] = field()

    @services.validator
    def _validate_services(cls, attribute: Any, value: list[Any]) -> None:
        if len(set(map(type, value))) != len(value):
            raise ValueError("values for 'services' field must be of distinct types")

    @classmethod
    def system_lookup(
        cls, value: BaseInstance | tuple[str, str | None, Settings]
    ) -> Self:
        pg_instance = PostgreSQLInstance.system_lookup(value)
        values = asdict(pg_instance)
        del values["bindir"]  # init=False
        # attrs strip leading underscores at init for private attributes.
        settings = values["settings"] = values.pop("_settings")
        assert "services" not in values
        values["services"] = [
            s
            for s in hooks(settings, h.system_lookup, instance=pg_instance)
            if s is not None
        ]
        return cls(**values)

    S = TypeVar("S")

    def service(self, stype: type[S]) -> S:
        """Return bound satellite service object matching requested type.

        :raises ValueError: if not found.
        """
        for s in self.services:
            if isinstance(s, stype):
                return s
        raise ValueError(stype)


@frozen
class DatabaseDump:
    id: str
    dbname: str
    date: datetime = field(converter=datetime.fromisoformat)  # type: ignore[misc]

    @classmethod
    def build(cls, dbname: str, date: str) -> Self:
        """Build a DatabaseDump from dbname and date.

        >>> DatabaseDump.build("postgres", str(datetime(2023, 3, 14)))  # doctest: +ELLIPSIS
        DatabaseDump(id='postgres_...', dbname='postgres', date=datetime.datetime(2023, 3, 14, 0, 0))
        """
        id = "_".join(
            [
                dbname,
                hashlib.blake2b(
                    (dbname + date).encode("utf-8"), digest_size=5
                ).hexdigest(),
            ]
        )
        return cls(id=id, dbname=dbname, date=date)


@frozen
class PGSetting:
    """A column from pg_settings view."""

    query: ClassVar[str] = (
        "SELECT name, setting, context, pending_restart FROM pg_settings"
    )

    name: str
    setting: str
    context: str
    pending_restart: bool
