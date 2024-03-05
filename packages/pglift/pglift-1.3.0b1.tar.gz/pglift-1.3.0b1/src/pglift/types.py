# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import abc
import enum
import logging
import re
import socket
import subprocess
import typing
from functools import cache
from pathlib import Path
from typing import (
    IO,
    TYPE_CHECKING,
    Annotated,
    Any,
    ClassVar,
    Literal,
    Optional,
    Protocol,
    TypedDict,
    TypeVar,
)

import attrs
import humanize
import psycopg.errors
import pydantic
import yaml
from pgtoolkit import conf as pgconf
from pydantic import ConfigDict, SecretStr, ValidationInfo, create_model
from pydantic.fields import FieldInfo
from pydantic.types import StringConstraints
from typing_extensions import TypeAlias

from ._compat import Self

if TYPE_CHECKING:
    CompletedProcess = subprocess.CompletedProcess[str]
    Popen = subprocess.Popen[str]
    from .pm import PluginManager
else:
    CompletedProcess = subprocess.CompletedProcess
    Popen = subprocess.Popen

logger = logging.getLogger(__name__)


class ConnectionString(str):
    pass


class ByteSizeType:
    human_readable = staticmethod(humanize.naturalsize)


ByteSize: TypeAlias = Annotated[int, ByteSizeType()]


class StrEnum(str, enum.Enum):
    def __str__(self) -> str:
        assert isinstance(self.value, str)
        return self.value


@enum.unique
class AutoStrEnum(StrEnum):
    """Enum base class with automatic values set to member name.

    >>> class State(AutoStrEnum):
    ...     running = enum.auto()
    ...     stopped = enum.auto()
    >>> State.running
    <State.running: 'running'>
    >>> State.stopped
    <State.stopped: 'stopped'>
    """

    def _generate_next_value_(name, *args: Any) -> str:  # type: ignore[override] # noqa: B902
        return name


class Status(enum.IntEnum):
    running = 0
    not_running = 3


ConfigChanges: TypeAlias = dict[
    str, tuple[Optional[pgconf.Value], Optional[pgconf.Value]]
]


BackupType = Literal["full", "incr", "diff"]
BACKUP_TYPES: tuple[BackupType] = typing.get_args(BackupType)
DEFAULT_BACKUP_TYPE: BackupType = "incr"


PostgreSQLStopMode = Literal["smart", "fast", "immediate"]


class Role(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def password(self) -> SecretStr | None: ...

    @property
    def encrypted_password(self) -> SecretStr | None: ...


class NoticeHandler(Protocol):
    def __call__(self, diag: psycopg.errors.Diagnostic) -> Any: ...


class AnsibleArgSpec(TypedDict, total=False):
    required: bool
    type: str
    default: Any
    choices: list[str]
    description: list[str]
    no_log: bool
    elements: str
    options: dict[str, Any]


@attrs.define(frozen=True, kw_only=True)
class CLIConfig:
    """Configuration for CLI argument generation from a manifest field."""

    name: str | None = None
    hide: bool = False
    metavar: str | None = None
    choices: list[str] | None = None


@attrs.define(frozen=True, kw_only=True)
class AnsibleConfig:
    """Configuration for Ansible argspec generation from a manifest field."""

    hide: bool = False
    choices: list[str] | None = None
    spec: AnsibleArgSpec | None = None


_T = TypeVar("_T")


def field_annotation(field: FieldInfo, t: type[_T]) -> _T | None:
    """Return the annotation of type 't' in field, or None if not found."""
    assert not isinstance(
        field.annotation, typing.ForwardRef
    ), "field type is a ForwardRef"
    for m in field.metadata:
        if isinstance(m, t):
            return m
    return None


def default_if_none(
    cls: type[pydantic.BaseModel], value: Any | None, info: ValidationInfo
) -> Any:
    """Return default value from field's default_factory when a None value got
    passed and it's not allowed by field definition.

    This is useful to prevent validation errors when receiving None value from
    Ansible for fields with a dynamic default.

    To be used with pre=True and allow_reuse=True.

    >>> import pydantic
    >>> class MyModel(pydantic.BaseModel):
    ...     name: str
    ...     foo: int = pydantic.Field(default_factory=lambda: 0)
    ...     __validate_foo_ = pydantic.field_validator("foo", mode="before")(
    ...         classmethod(default_if_none)
    ...     )

    >>> MyModel(name="test", foo=None).model_dump()
    {'name': 'test', 'foo': 0}
    >>> MyModel(name="test", foo=1).model_dump()
    {'name': 'test', 'foo': 1}
    """
    if value is None:
        assert info.field_name is not None
        field = cls.model_fields[info.field_name]
        assert field.default_factory is not None
        return field.default_factory()
    return value


class PortValidatorType:
    @staticmethod
    def available(port: int) -> bool:
        """Return True if this port is free to use."""
        for family, socktype, proto, _canonname, sockaddr in socket.getaddrinfo(
            None, port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE
        ):
            try:
                s = socket.socket(family, socktype, proto)
            except OSError:
                logger.debug(
                    "failed to create socket from family=%s, type=%s, proto=%s",
                    family,
                    socktype,
                    proto,
                )
                continue
            else:
                if s.connect_ex(sockaddr) == 0:
                    return False
            finally:
                s.close()
        return True


PortValidator = PortValidatorType()  # singleton
Port = Annotated[int, PortValidator]


class BaseModel(pydantic.BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        validate_assignment=True,
    )


class Manifest(BaseModel):
    """Base class for manifest data classes."""

    @classmethod
    def parse_yaml(cls, value: str | IO[str]) -> Self:
        """Parse from a YAML stream."""
        data = yaml.safe_load(value)
        return cls.model_validate(data)

    def yaml(self, **kwargs: Any) -> str:
        """Return a YAML serialization of this manifest."""
        data = self.model_dump(mode="json", by_alias=True, **kwargs)
        return yaml.dump(data, sort_keys=False, explicit_start=True)

    def _copy_validate(self, update: dict[str, Any]) -> Self:
        """Like .copy(), but with validation (and default value setting).

        (Internal method, mostly useful for test purpose.)
        """
        return self.__class__.model_validate(
            dict(self.model_dump(by_alias=True), **update)
        )


class CompositeManifest(Manifest, abc.ABC):
    """A manifest type with extra fields from plugins."""

    # Allow extra fields to permit plugins to populate an object with
    # their specific data, following (hopefully) what's defined by
    # the "composite" model (see composite()).
    model_config = Manifest.model_config | ConfigDict(extra="allow")

    @classmethod
    def composite(cls, pm: PluginManager) -> type[Self]:
        fields = {}
        for name, m, f in cls.component_models(pm):
            if name in fields:
                raise ValueError(f"duplicated {name!r} service")
            fields[name] = m, f
        # XXX Spurious 'type: ignore' below.
        m = create_model(cls.__name__, __base__=cls, __module__=__name__, **fields)  # type: ignore[call-overload]
        # pydantic.create_model() uses type(), so this will confuse mypy which
        # cannot handle dynamic base class; hence the 'type: ignore'.
        return m  # type: ignore[no-any-return]

    @classmethod
    @abc.abstractmethod
    def component_models(cls, pm: PluginManager) -> list[tuple[str, Any, Any]]: ...


class ServiceManifest(Manifest):
    __service__: ClassVar[str]

    def __init_subclass__(cls, *, service_name: str, **kwargs: Any) -> None:
        """Set a __name__ to subclasses.

        >>> class MyS(ServiceManifest, service_name="my"):
        ...     x: str
        >>> s = MyS(x='y')
        >>> s.__class__.__service__
        'my'
        """
        super().__init_subclass__(**kwargs)
        cls.__service__ = service_name


class Runnable(Protocol):
    __service_name__: ClassVar[str]

    @property
    def name(self) -> str | None: ...

    def args(self) -> list[str]: ...

    def pidfile(self) -> Path: ...

    def env(self) -> dict[str, str] | None: ...


address_pattern = r"(?P<host>[^\s:?#]+):(?P<port>\d+)"


Address = Annotated[str, StringConstraints(pattern=address_pattern)]
#: Network address type <host or ip>:<port>.


def make_address(host: str, port: int) -> Address:
    return f"{host}:{port}"


def local_address(port: int) -> Address:
    host = socket.gethostbyname(socket.gethostname())
    if host.startswith("127."):  # loopback addresses
        host = socket.getfqdn()
    return make_address(host, port)


def unspecified_address() -> Address:
    return Address()


address_rgx = re.compile(address_pattern)


@cache
def address_host(addr: Address) -> str:
    m = address_rgx.match(addr)
    assert m
    return m.group("host")


@cache
def address_port(addr: Address) -> int:
    m = address_rgx.match(addr)
    assert m
    return int(m.group("port"))
