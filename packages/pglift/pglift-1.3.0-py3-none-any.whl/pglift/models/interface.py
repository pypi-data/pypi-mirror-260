# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Iterator, Mapping, MutableMapping
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Annotated, Any, Final, Literal, Optional, TypeVar, Union

import psycopg.conninfo
import pydantic
from pgtoolkit import conf as pgconf
from pydantic import (
    AfterValidator,
    BeforeValidator,
    ConfigDict,
    Field,
    PostgresDsn,
    SecretStr,
    ValidationInfo,
    model_validator,
)
from pydantic.v1.utils import lenient_issubclass

from .. import exceptions
from .. import settings as s
from .. import types, util
from .._compat import Self, assert_never
from ..pm import PluginManager
from ..postgresql import Standby
from ..settings import _postgresql as pgs
from ..types import (
    AnsibleConfig,
    ByteSize,
    CLIConfig,
    CompositeManifest,
    Manifest,
    Port,
    ServiceManifest,
    Status,
)
from .helpers import check_conninfo, check_excludes

default_port: Final = 5432


def as_dict(value: Union[str, dict[str, Any]]) -> dict[str, Any]:
    """Possibly wrap a str value as a dict with 'name' key.

    >>> as_dict({"x": 1})
    {'x': 1}
    >>> as_dict("x")
    {'name': 'x'}
    """
    if isinstance(value, str):
        return {"name": value}
    return value


def validate_ports(model: pydantic.BaseModel) -> None:
    """Walk fields of 'model', checking those with type Port if their value is
    available.
    """

    def _validate(
        model: pydantic.BaseModel, *, loc: tuple[str, ...] = ()
    ) -> Iterator[tuple[int, tuple[str, ...]]]:
        cls = model.__class__
        for name, field in cls.model_fields.items():
            if (value := getattr(model, name)) is None:
                continue
            if lenient_issubclass(field.annotation, pydantic.BaseModel):
                yield from _validate(value, loc=loc + (name,))
            elif port_validator := types.field_annotation(
                field, types.PortValidatorType
            ):
                if not port_validator.available(value):
                    yield value, loc + (name,)

    if errors := list(_validate(model)):
        raise exceptions.ValidationError(
            [(loc, f"port {value} already in use") for value, loc in errors], model
        ) from None


def validate_state_is_absent(
    value: Union[bool, str], info: ValidationInfo
) -> Union[bool, str]:
    """Make sure state is absent.

    >>> r =  Role(name="bob",  drop_owned=True)
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Role
    drop_owned
      Value error, drop_owned can not be set if state is not 'absent' [type=value_error, input_value=True, input_type=bool]
        ...

    >>> r =  Role(name="bob",  reassign_owned="postgres")
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Role
    reassign_owned
      Value error, reassign_owned can not be set if state is not 'absent' [type=value_error, input_value='postgres', input_type=str]
        ...

    >>> r =  Database(name="db1", force_drop=True)
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Database
    force_drop
      Value error, force_drop can not be set if state is not 'absent' [type=value_error, input_value=True, input_type=bool]
        ...
    """
    if value and info.data.get("state") != "absent":
        raise ValueError(f"{info.field_name} can not be set if state is not 'absent'")
    return value


InstanceState = Literal["stopped", "started", "absent", "restarted"]


def state_from_pg_status(status: Status) -> InstanceState:
    """Instance state from PostgreSQL status.

    >>> state_from_pg_status(Status.running)
    'started'
    >>> state_from_pg_status(Status.not_running)
    'stopped'
    """
    if status is Status.running:
        return "started"
    elif status is Status.not_running:
        return "stopped"
    assert_never(status)


PresenceState = Literal["present", "absent"]


def check_one_password_only(
    value: Optional[SecretStr], info: ValidationInfo
) -> Optional[SecretStr]:
    """Make sure 'password' and 'encrypted_password' are not specified together.

    >>> Role(name="bob", password="secret", encrypted_password="tercec")
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Role
    encrypted_password
      Value error, field is mutually exclusive with 'password' [type=value_error, input_value='tercec', input_type=str]
        ...

    >>> r = Role(name="bob", encrypted_password="tercec")
    >>> r.password, r.encrypted_password
    (None, SecretStr('**********'))
    """
    other = (
        "password" if info.field_name == "encrypted_password" else "encrypted_password"
    )
    if value and info.data.get(other):
        raise ValueError(f"field is mutually exclusive with {other!r}")
    return value


class BaseRole(CompositeManifest):
    name: Annotated[
        str, Field(description="Role name.", json_schema_extra={"readOnly": True})
    ]
    state: Annotated[
        PresenceState,
        Field(
            description="Whether the role be present or absent.",
            exclude=True,
        ),
    ] = "present"
    password: Annotated[
        Optional[SecretStr],
        Field(description="Role password.", exclude=True),
        AfterValidator(check_one_password_only),
    ] = None
    encrypted_password: Annotated[
        Optional[SecretStr],
        Field(description="Role password, already encrypted.", exclude=True),
        AfterValidator(check_one_password_only),
    ] = None

    @classmethod
    def component_models(cls, pm: PluginManager) -> list[tuple[str, Any, Any]]:
        return pm.hook.role_model()  # type: ignore[no-any-return]


DropOwned = Field(
    description="Drop all PostgreSQL's objects owned by the role being dropped.",
    exclude=True,
)
ReassignOwned = Field(
    description="Reassign all PostgreSQL's objects owned by the role being dropped to the specified role name.",
    min_length=1,
    exclude=True,
)


def check_reassign_owned(value: str, info: ValidationInfo) -> str:
    """Validate reassign_owned fields.

    >>> r = RoleDropped(name="bob", drop_owned=True, reassign_owned="postgres")
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for RoleDropped
    reassign_owned
      Value error, drop_owned and reassign_owned are mutually exclusive [type=value_error, input_value='postgres', input_type=str]
        ...

    >>> r = RoleDropped(name="bob", reassign_owned="")
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for RoleDropped
    reassign_owned
      String should have at least 1 character [type=string_too_short, input_value='', input_type=str]
        ...
    >>> RoleDropped(name="bob", reassign_owned=None, drop_owned=True)  # doctest: +ELLIPSIS
    RoleDropped(name='bob', state='absent', ..., drop_owned=True, reassign_owned=None)
    """
    if value and info.data["drop_owned"]:
        raise ValueError("drop_owned and reassign_owned are mutually exclusive")
    return value


class RoleDropped(BaseRole):
    """Model for a role that is being dropped."""

    state: Literal["absent"] = "absent"
    password: Literal[None] = None
    encrypted_password: Literal[None] = None
    drop_owned: Annotated[bool, DropOwned] = False
    reassign_owned: Annotated[
        Optional[str], ReassignOwned, AfterValidator(check_reassign_owned)
    ] = None


def _set_has_password(value: bool, info: ValidationInfo) -> bool:
    """Set 'has_password' field according to 'password'.

    >>> r = Role(name="postgres")
    >>> r.has_password
    False
    >>> r = Role(name="postgres", password="P4zzw0rd")
    >>> r.has_password
    True
    >>> r = Role(name="postgres", has_password=True)
    >>> r.has_password
    True
    """
    return (
        value
        or info.data["password"] is not None
        or info.data["encrypted_password"] is not None
    )


class _RoleExisting(BaseRole):
    """Base model for a role that exists (or should exist, after creation)."""

    has_password: Annotated[
        bool,
        CLIConfig(hide=True),
        AnsibleConfig(hide=True),
        Field(
            description="True if the role has a password.",
            validate_default=True,
            json_schema_extra={"readOnly": True},
        ),
        AfterValidator(_set_has_password),
    ] = False
    inherit: Annotated[
        bool,
        Field(
            description="Let the role inherit the privileges of the roles it is a member of.",
        ),
    ] = True
    login: Annotated[bool, Field(description="Allow the role to log in.")] = False
    superuser: Annotated[
        bool, Field(description="Whether the role is a superuser.")
    ] = False
    createdb: Annotated[
        bool, Field(description="Whether role can create new databases.")
    ] = False
    createrole: Annotated[
        bool, Field(description="Whether role can create new roles.")
    ] = False
    replication: Annotated[
        bool, Field(description="Whether the role is a replication role.")
    ] = False
    connection_limit: Annotated[
        Optional[int],
        Field(description="How many concurrent connections the role can make."),
    ] = None
    validity: Annotated[
        Optional[datetime],
        Field(
            description="Date and time after which the role's password is no longer valid."
        ),
    ] = None
    in_roles: Annotated[
        list[str],
        CLIConfig(name="in_role"),
        Field(
            description="List of roles to which the new role will be added as a new member.",
        ),
    ] = []
    state: Annotated[
        PresenceState,
        CLIConfig(hide=True),
        Field(
            description="Whether the role be present or absent.",
            exclude=True,
        ),
    ] = "present"


class Role(_RoleExisting, RoleDropped):
    """PostgreSQL role"""

    drop_owned: Annotated[
        bool, DropOwned, CLIConfig(hide=True), AfterValidator(validate_state_is_absent)
    ] = False
    reassign_owned: Annotated[
        Optional[str],
        ReassignOwned,
        CLIConfig(hide=True),
        AfterValidator(validate_state_is_absent),
    ] = None


class Tablespace(Manifest):
    name: str
    location: str
    size: ByteSize


class DatabaseListItem(Manifest):
    name: str
    owner: str
    encoding: str
    collation: str
    ctype: str
    acls: list[str]
    size: ByteSize
    description: Optional[str]
    tablespace: Tablespace

    @classmethod
    def build(
        cls,
        *,
        tablespace: str,
        tablespace_location: str,
        tablespace_size: int,
        **kwargs: Any,
    ) -> Self:
        tblspc = Tablespace(
            name=tablespace, location=tablespace_location, size=tablespace_size
        )
        return cls(tablespace=tblspc, **kwargs)


class BaseDatabase(Manifest):
    name: Annotated[
        str,
        Field(
            description="Database name.",
            json_schema_extra={"readOnly": True, "examples": ["demo"]},
        ),
    ]


ForceDrop = Field(description="Force the drop.", exclude=True)


class DatabaseDropped(BaseDatabase):
    """Model for a database that is being dropped."""

    force_drop: Annotated[bool, ForceDrop, CLIConfig(name="force")] = False


class Schema(Manifest):
    name: Annotated[
        str, Field(description="Schema name.", json_schema_extra={"readOnly": True})
    ]

    state: Annotated[
        PresenceState,
        Field(
            description="Schema state.",
            exclude=True,
            json_schema_extra={"examples": ["present"]},
        ),
    ] = "present"

    owner: Annotated[
        Optional[str],
        Field(
            description="The role name of the user who will own the schema.",
            json_schema_extra={"examples": ["postgres"]},
        ),
    ] = None


class Extension(Manifest):
    model_config = ConfigDict(frozen=True)

    name: Annotated[
        str, Field(description="Extension name.", json_schema_extra={"readOnly": True})
    ]
    schema_: Annotated[
        Optional[str],
        Field(
            alias="schema",
            description="Name of the schema in which to install the extension's object.",
        ),
    ] = None
    version: Annotated[
        Optional[str], Field(description="Version of the extension to install.")
    ] = None

    state: Annotated[
        PresenceState,
        Field(
            description="Extension state.",
            exclude=True,
            json_schema_extra={"examples": ["present"]},
        ),
    ] = "present"


class Publication(Manifest):
    name: Annotated[
        str,
        Field(
            description="Name of the publication, unique in the database.",
        ),
    ]
    state: Annotated[
        PresenceState,
        Field(
            description="Presence state.",
            exclude=True,
            json_schema_extra={"examples": ["present"]},
        ),
    ] = "present"


class ConnectionString(Manifest):
    conninfo: Annotated[
        str,
        Field(
            description="The libpq connection string, without password.",
        ),
        AfterValidator(partial(check_conninfo, exclude=[("password", "a password")])),
    ]
    password: Annotated[
        Optional[SecretStr],
        Field(
            description="Optional password to inject into the connection string.",
            exclude=True,
            json_schema_extra={"readOnly": True},
        ),
    ] = None

    @classmethod
    def parse(cls, value: str) -> Self:
        conninfo = psycopg.conninfo.conninfo_to_dict(value)
        password = conninfo.pop("password", None)
        return cls(
            conninfo=psycopg.conninfo.make_conninfo(**conninfo), password=password
        )

    @property
    def full_conninfo(self) -> str:
        """The full connection string, including password field."""
        password = None
        if self.password:
            password = self.password.get_secret_value()
        return psycopg.conninfo.make_conninfo(self.conninfo, password=password)


class Subscription(Manifest):
    name: Annotated[str, Field(description="Name of the subscription.")]
    connection: Annotated[
        ConnectionString,
        Field(
            description="The libpq connection string defining how to connect to the publisher database.",
            json_schema_extra={"readOnly": True},
        ),
    ]
    publications: Annotated[
        list[str],
        Field(
            description="List of publications on the publisher to subscribe to.",
            min_length=1,
        ),
    ]
    enabled: Annotated[
        bool, Field(description="Enable or disable the subscription.")
    ] = True
    state: Annotated[
        PresenceState,
        Field(
            description="Presence state.",
            exclude=True,
            json_schema_extra={"examples": ["present"]},
        ),
    ] = "present"

    @classmethod
    def from_row(cls, **kwargs: Any) -> Self:
        return cls(
            connection=ConnectionString.parse(kwargs.pop("connection")), **kwargs
        )


class CloneOptions(Manifest):
    dsn: Annotated[
        PostgresDsn,
        CLIConfig(name="from", metavar="conninfo"),
        Field(
            description="Data source name of the database to restore into this one, specified as a libpq connection URI.",
        ),
    ]
    schema_only: Annotated[
        bool,
        Field(
            description="Only restore the schema (data definitions).",
        ),
    ] = False


def check_tablespace(value: str) -> Optional[str]:
    """Make sure tablespace is valid (ie. forbid 'default' or 'DEFAULT')

    >>> Database(name="x", tablespace="default")
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Database
    tablespace
      Value error, 'default' is not a valid value for 'tablespace'. Don't provide a value if you want the tablespace to be set to DEFAULT. [type=value_error, input_value='default', input_type=str]
        ...
    >>> Database(name="x", tablespace="DEFAULT")
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Database
    tablespace
      Value error, 'DEFAULT' is not a valid value for 'tablespace'. Don't provide a value if you want the tablespace to be set to DEFAULT. [type=value_error, input_value='DEFAULT', input_type=str]
        ...
    """
    if value and value.lower() == "default":
        raise ValueError(
            f"{value!r} is not a valid value for 'tablespace'. "
            "Don't provide a value if you want the tablespace to be set to DEFAULT."
        )
    return value


class Database(DatabaseDropped):
    """PostgreSQL database"""

    state: Annotated[
        PresenceState,
        CLIConfig(hide=True),
        Field(
            description="Database state.",
            exclude=True,
            json_schema_extra={"examples": ["present"]},
        ),
    ] = "present"
    owner: Annotated[
        Optional[str],
        Field(
            description="The role name of the user who will own the database.",
            json_schema_extra={"examples": ["postgres"]},
        ),
    ] = None
    settings: Annotated[
        Optional[MutableMapping[str, Optional[pgconf.Value]]],
        CLIConfig(hide=True),
        AnsibleConfig(spec={"type": "dict", "required": False}),
        Field(
            description=(
                "Session defaults for run-time configuration variables for the database. "
                "Upon update, an empty (dict) value would reset all settings."
            ),
            json_schema_extra={"examples": [{"work_mem": "5MB"}]},
        ),
    ] = None
    schemas: Annotated[
        list[Annotated[Schema, BeforeValidator(as_dict)]],
        CLIConfig(name="schema"),
        Field(
            description="List of schemas to create in the database.",
            json_schema_extra={"examples": [{"name": "sales"}, "accounting"]},
        ),
    ] = []
    extensions: Annotated[
        list[Annotated[Extension, BeforeValidator(as_dict)]],
        CLIConfig(name="extension"),
        Field(
            description="List of extensions to create in the database.",
            json_schema_extra={
                "examples": [
                    {"name": "unaccent", "schema": "ext", "version": "1.0"},
                    "hstore",
                ]
            },
        ),
    ] = []

    publications: Annotated[
        list[Publication],
        CLIConfig(hide=True),
        Field(
            description="List of publications to in the database.",
            json_schema_extra={"examples": [{"name": "mypub"}]},
        ),
    ] = []

    subscriptions: Annotated[
        list[Subscription],
        CLIConfig(hide=True),
        Field(
            description="List of subscriptions to in the database.",
            json_schema_extra={
                "examples": [
                    {"name": "mysub", "publications": ["mypub"], "enabled": False},
                ]
            },
        ),
    ] = []

    clone: Annotated[
        Optional[CloneOptions],
        Field(
            description="Options for cloning a database into this one.",
            exclude=True,
            json_schema_extra={
                "readOnly": True,
                "writeOnly": True,
                "examples": [
                    "postgresql://app:password@dbserver:5455/appdb",
                    {
                        "dsn": "postgresql://app:password@dbserver:5455/appdb",
                        "schema_only": True,
                    },
                ],
            },
        ),
    ] = None

    tablespace: Annotated[
        Optional[str],
        Field(
            description="The name of the tablespace that will be associated with the database.",
        ),
        AfterValidator(check_tablespace),
    ] = None

    force_drop: Annotated[
        bool, ForceDrop, CLIConfig(hide=True), AfterValidator(validate_state_is_absent)
    ] = False


def _sort(value: list[str]) -> list[str]:
    value.sort()
    return value


def _sort_values(value: dict[str, list[str]]) -> dict[str, list[str]]:
    for v in value.values():
        v.sort()
    return value


class DefaultPrivilege(Manifest):
    """Default access privilege"""

    database: str
    schema_: Annotated[str, Field(alias="schema")]
    object_type: str
    role: str
    privileges: Annotated[list[str], AfterValidator(_sort)]


class Privilege(DefaultPrivilege):
    """Access privilege"""

    object_name: str
    column_privileges: Annotated[Mapping[str, list[str]], AfterValidator(_sort_values)]


class Auth(types.BaseModel):
    local: Annotated[
        Optional[pgs.AuthLocalMethods],
        Field(
            description="Authentication method for local-socket connections",
            json_schema_extra={"readOnly": True},
        ),
    ] = None
    host: Annotated[
        Optional[pgs.AuthHostMethods],
        Field(
            description="Authentication method for local TCP/IP connections",
            json_schema_extra={"readOnly": True},
        ),
    ] = None
    hostssl: Annotated[
        Optional[pgs.AuthHostSSLMethods],
        Field(
            description="Authentication method for SSL-encrypted TCP/IP connections",
            json_schema_extra={"readOnly": True},
        ),
    ] = None


class InstanceListItem(Manifest):
    name: Annotated[str, Field(description="Instance name.")]
    version: Annotated[str, Field(description="PostgreSQL version.")]
    port: Annotated[
        int, Field(description="TCP port the PostgreSQL instance is listening to.")
    ]
    datadir: Annotated[Path, Field(description="PostgreSQL data directory.")]
    status: Annotated[str, Field(description="Runtime status.")]


class Instance(CompositeManifest):
    """PostgreSQL instance

    >>> Instance(name='without_dash')  # doctest: +ELLIPSIS
    Instance(name='without_dash', ...)
    >>> Instance(name='with-dash')
    Traceback (most recent call last):
        ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Instance
    name
      Value error, must not contain dashes [type=value_error, input_value='with-dash', input_type=str]
      ...
    >>> Instance(name='with/slash')
    Traceback (most recent call last):
        ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Instance
    name
      Value error, must not contain slashes [type=value_error, input_value='with/slash', input_type=str]
      ...
    """

    @classmethod
    def component_models(cls, pm: PluginManager) -> list[tuple[str, Any, Any]]:
        return pm.hook.interface_model()  # type: ignore[no-any-return]

    name: Annotated[
        str,
        Field(description="Instance name.", json_schema_extra={"readOnly": True}),
        AfterValidator(partial(check_excludes, ("/", "slashes"))),
        AfterValidator(partial(check_excludes, ("-", "dashes"))),
    ]
    version: Annotated[
        Optional[pgs.PostgreSQLVersion],
        Field(
            description="PostgreSQL version.",
            json_schema_extra={"readOnly": True},
        ),
    ] = None

    port: Annotated[
        Port,
        Field(
            description=(
                "TCP port the PostgreSQL instance will be listening to. "
                f"If unspecified, default to {default_port} unless a 'port' setting is found in 'settings'."
            )
        ),
    ] = default_port
    settings: Annotated[
        MutableMapping[str, Any],
        CLIConfig(hide=True),
        Field(
            description=("Settings for the PostgreSQL instance."),
            json_schema_extra={
                "examples": [
                    {
                        "listen_addresses": "*",
                        "shared_buffers": "1GB",
                        "ssl": True,
                        "ssl_key_file": "/etc/certs/db.key",
                        "ssl_cert_file": "/etc/certs/db.key",
                        "shared_preload_libraries": "pg_stat_statements",
                    }
                ]
            },
        ),
    ] = {}
    surole_password: Annotated[
        Optional[SecretStr],
        Field(
            description="Super-user role password.",
            exclude=True,
            json_schema_extra={"readOnly": True},
        ),
    ] = None
    replrole_password: Annotated[
        Optional[SecretStr],
        Field(
            description="Replication role password.",
            exclude=True,
            json_schema_extra={"readOnly": True},
        ),
    ] = None
    data_checksums: Annotated[
        Optional[bool],
        Field(
            description=(
                "Enable or disable data checksums. "
                "If unspecified, fall back to site settings choice."
            ),
        ),
    ] = None
    locale: Annotated[
        Optional[str],
        Field(
            description="Default locale.",
            json_schema_extra={"readOnly": True},
        ),
    ] = None
    encoding: Annotated[
        Optional[str],
        Field(
            description="Character encoding of the PostgreSQL instance.",
            json_schema_extra={"readOnly": True},
        ),
    ] = None

    auth: Annotated[
        Optional[Auth], Field(exclude=True, json_schema_extra={"writeOnly": True})
    ] = None

    standby: Annotated[
        Optional[Standby],
        Field(description="Standby information."),
    ] = None

    state: Annotated[
        InstanceState,
        CLIConfig(choices=["started", "stopped"]),
        Field(description="Runtime state."),
    ] = "started"
    databases: Annotated[
        list[Database],
        CLIConfig(hide=True),
        Field(
            description="Databases defined in this instance (non-exhaustive list).",
            exclude=True,
            json_schema_extra={"writeOnly": True},
        ),
    ] = []
    roles: Annotated[
        list[Role],
        CLIConfig(hide=True),
        Field(
            description="Roles defined in this instance (non-exhaustive list).",
            exclude=True,
            json_schema_extra={"writeOnly": True},
        ),
    ] = []

    pending_restart: Annotated[
        bool,
        CLIConfig(hide=True),
        AnsibleConfig(hide=True),
        Field(
            description="Whether the instance needs a restart to account for settings changes.",
            json_schema_extra={"readOnly": True},
        ),
    ] = False
    restart_on_changes: Annotated[
        bool,
        CLIConfig(hide=True),
        Field(
            description="Whether or not to automatically restart the instance to account for settings changes.",
            exclude=True,
            json_schema_extra={"writeOnly": True},
        ),
    ] = False

    @model_validator(mode="before")
    @classmethod
    def __validate_port_(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate that 'port' field and settings['port'] are consistent.

        If unspecified, 'port' is either set from settings value or from
        the default port value.

        >>> i = Instance(name="i")
        >>> i.port, "port" in i.settings
        (5432, False)
        >>> i = Instance(name="i", settings={"port": 5423})
        >>> i.port, i.settings["port"]
        (5423, 5423)
        >>> i = Instance(name="i", port=5454)
        >>> i.port, "port" in i.settings
        (5454, False)

        Otherwise, and if settings['port'] exists, make sure values are
        consistent and possibly cast the latter as an integer.

        >>> i = Instance(name="i", settings={"port": 5455})
        >>> i.port, i.settings["port"]
        (5455, 5455)
        >>> i = Instance(name="i", port=123, settings={"port": "123"})
        >>> i.port, i.settings["port"]
        (123, 123)
        >>> Instance(name="i", port=321, settings={"port": 123})
        Traceback (most recent call last):
          ...
        pydantic_core._pydantic_core.ValidationError: 1 validation error for Instance
          Value error, 'port' field and settings['port'] mismatch [type=value_error, input_value={'name': 'i', 'port': 321...ettings': {'port': 123}}, input_type=dict]
            ...
        >>> Instance(name="i", settings={"port": "abc"})
        Traceback (most recent call last):
          ...
        pydantic_core._pydantic_core.ValidationError: 1 validation error for Instance
          Value error, invalid literal for int() with base 10: 'abc' [type=value_error, input_value={'name': 'i', 'settings': {'port': 'abc'}}, input_type=dict]
            ...
        """
        config_port = None
        try:
            port = values["port"]
        except KeyError:
            try:
                config_port = int(values["settings"]["port"])
            except KeyError:
                pass
            else:
                values["port"] = Port(config_port)
        else:
            try:
                config_port = int(values["settings"]["port"])
            except KeyError:
                pass
            else:
                if config_port != port:
                    raise ValueError("'port' field and settings['port'] mismatch")
        if config_port is not None:
            values["settings"]["port"] = config_port
        return values

    @model_validator(mode="before")
    @classmethod
    def __validate_standby_and_patroni_(cls, values: dict[str, Any]) -> dict[str, Any]:
        if values.get("standby") and values.get("patroni"):
            raise ValueError("'patroni' and 'standby' fields are mutually exclusive")
        return values

    _S = TypeVar("_S", bound=ServiceManifest)

    def service_manifest(self, stype: type[_S]) -> _S:
        """Return satellite service manifest attached to this instance.

        :raises ValueError: if not found.
        """
        fname = stype.__service__
        try:
            s = getattr(self, fname)
        except AttributeError as e:
            raise ValueError(fname) from e
        if s is None:
            raise ValueError(fname)
        assert isinstance(
            s, stype
        ), f"expecting field {fname} to have type {stype} (got {type(s)})"
        return s

    def surole(self, settings: s.Settings) -> Role:
        s = settings.postgresql.surole
        extra = {}
        if settings.postgresql.auth.passfile is not None:
            extra["pgpass"] = s.pgpass
        return Role(name=s.name, password=self.surole_password, **extra)

    def replrole(self, settings: s.Settings) -> Optional[Role]:
        if (name := settings.postgresql.replrole) is None:
            return None
        return Role(
            name=name,
            password=self.replrole_password,
            login=True,
            replication=True,
            in_roles=["pg_read_all_stats"],
        )

    def auth_options(self, settings: pgs.AuthSettings) -> Auth:
        local, host, hostssl = settings.local, settings.host, settings.hostssl
        if auth := self.auth:
            local = auth.local or local
            host = auth.host or host
            hostssl = auth.hostssl or hostssl
        return Auth(local=local, host=host, hostssl=hostssl)

    def pg_hba(self, settings: s.Settings) -> str:
        surole = self.surole(settings)
        replrole = self.replrole(settings)
        replrole_name = replrole.name if replrole else None
        auth = self.auth_options(settings.postgresql.auth)
        return util.template("postgresql", "pg_hba.conf").format(
            auth=auth,
            surole=surole.name,
            backuprole=settings.postgresql.backuprole.name,
            replrole=replrole_name,
        )

    def pg_ident(self, settings: s.Settings) -> str:
        surole = self.surole(settings)
        replrole = self.replrole(settings)
        replrole_name = replrole.name if replrole else None
        return util.template("postgresql", "pg_ident.conf").format(
            surole=surole.name,
            backuprole=settings.postgresql.backuprole.name,
            replrole=replrole_name,
            sysuser=settings.sysuser[0],
        )

    def initdb_options(self, base: pgs.InitdbSettings) -> pgs.InitdbSettings:
        data_checksums: Union[None, Literal[True]] = {
            True: True,
            False: None,
            None: base.data_checksums or None,
        }[self.data_checksums]
        return pgs.InitdbSettings(
            locale=self.locale or base.locale,
            encoding=self.encoding or base.encoding,
            data_checksums=data_checksums,
        )


class ApplyResult(Manifest):
    """
    ApplyResult allows to describe the result of a call to apply function
    (Eg: pglift.database.apply) to an object (Eg: database, instance,...).

    The `change_state` attribute of this class can be set to one of to those values:
      - `'created'` if the object has been created,
      - `'changed'` if the object has been changed,
      - `'dropped'` if the object has been dropped,
      - :obj:`None` if nothing happened to the object we manipulate (neither created,
        changed or dropped)
    """

    change_state: Annotated[
        Optional[Literal["created", "changed", "dropped"]],
        Field(
            description="Define the change applied (created, changed or dropped) to a manipulated object",
        ),
    ] = None  #:


class InstanceApplyResult(ApplyResult):
    pending_restart: Annotated[
        bool,
        Field(
            description="Whether the instance needs a restart to account for settings changes.",
        ),
    ] = False
