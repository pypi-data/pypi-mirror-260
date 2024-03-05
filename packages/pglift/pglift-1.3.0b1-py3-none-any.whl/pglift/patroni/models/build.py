# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from datetime import timedelta
from pathlib import Path
from typing import Annotated, Any, Literal, Optional, Union

import pgtoolkit.conf
import psycopg.conninfo
import pydantic
import yaml
from pydantic import Field, SecretStr

from ... import async_hooks, exceptions, h, types
from ..._compat import Self
from ...models import interface, system
from ...settings._patroni import Settings
from .. import impl
from . import common
from . import interface as i


def bootstrap(
    instance: system.BaseInstance, manifest: interface.Instance
) -> dict[str, Any]:
    """Return values for the "bootstrap" section of Patroni configuration."""
    settings = instance._settings
    patroni_settings = settings.patroni
    assert patroni_settings
    initdb_options = manifest.initdb_options(settings.postgresql.initdb)
    initdb: list[Union[str, dict[str, Union[str, Path]]]] = [
        {key: value}
        for key, value in initdb_options.model_dump(
            exclude={"data_checksums"}, exclude_none=True
        ).items()
    ]
    initdb.append({"waldir": instance.waldir})
    if initdb_options.data_checksums:
        initdb.append("data-checksums")
    pg_hba = manifest.pg_hba(settings).splitlines()
    pg_ident = manifest.pg_ident(settings).splitlines()
    return dict(
        dcs={"loop_wait": patroni_settings.loop_wait},
        initdb=initdb,
        pg_hba=pg_hba,
        pg_ident=pg_ident,
    )


def export_model(model: pydantic.BaseModel) -> dict[str, Any]:
    """Export a model as a dict unshadowing secret fields.

    >>> class S(pydantic.BaseModel):
    ...     user: str
    ...     pw: Optional[SecretStr] = None
    >>> export_model(S(user="bob", pw="s3kret"))
    {'user': 'bob', 'pw': 's3kret'}
    """
    return {
        n: v.get_secret_value() if isinstance(v, SecretStr) else v
        for n, v in model
        if v is not None
    }


def libpq_ssl_settings(model: pydantic.BaseModel) -> dict[str, Any]:
    """Return a dict suitable for libpq connection SSL options.

    >>> class S(pydantic.BaseModel):
    ...     cert: str
    ...     password: Optional[SecretStr] = None
    ...     rootcert: Optional[str]

    >>> libpq_ssl_settings(S(cert="a", rootcert=None))
    {'sslcert': 'a'}
    >>> libpq_ssl_settings(S(cert="z", rootcert="y", password="pwd"))
    {'sslcert': 'z', 'sslpassword': 'pwd', 'sslrootcert': 'y'}
    """
    options = {f"ssl{n}": v for n, v in export_model(model).items()}
    # Verify that the result is valid for libpq.
    assert not options or psycopg.conninfo.make_conninfo(**options)
    return options


async def postgresql(
    instance: system.BaseInstance,
    manifest: interface.Instance,
    configuration: pgtoolkit.conf.Configuration,
    postgresql_options: Optional[i.PostgreSQL],
    **args: Any,
) -> dict[str, Any]:
    """Return values for the "postgresql" section of Patroni configuration.

    Any values from `**args` are used over default values that would be
    inferred but values from `manifest` still take precedence.
    """
    settings = instance._settings
    if "authentication" not in args:
        patroni_settings = settings.patroni
        assert patroni_settings is not None
        sslopts = {}
        if (
            patroni_settings.postgresql.connection
            and patroni_settings.postgresql.connection.ssl
        ):
            sslopts = libpq_ssl_settings(patroni_settings.postgresql.connection.ssl)

        def r(
            role: interface.Role,
            opts: Optional[i.ClientAuth],
        ) -> dict[str, str]:
            d = {"username": role.name} | sslopts
            if role.password:
                d["password"] = role.password.get_secret_value()
            if opts and opts.ssl:
                d |= libpq_ssl_settings(opts.ssl)
            return d

        surole = manifest.surole(settings)
        replrole = manifest.replrole(settings)
        assert replrole  # Per settings validation
        args["authentication"] = {
            "superuser": r(surole, None),
            "replication": r(
                replrole,
                postgresql_options.replication if postgresql_options else None,
            ),
            "rewind": r(
                surole,
                postgresql_options.rewind if postgresql_options else None,
            ),
        }

    if postgresql_options and postgresql_options.connect_host is not None:
        args["connect_address"] = types.make_address(
            postgresql_options.connect_host, manifest.port
        )
    else:
        args["connect_address"] = types.local_address(manifest.port)

    def s(entry: pgtoolkit.conf.Entry) -> Union[str, bool, int, float]:
        # Serialize pgtoolkit entry without quoting; specially needed to
        # timedelta.
        if isinstance(entry.value, timedelta):
            return entry.serialize().strip("'")
        return entry.value

    parameters = args.setdefault("parameters", {})
    parameters.update({k: s(e) for k, e in sorted(configuration.entries.items())})

    listen_addresses = parameters.get("listen_addresses", "*")
    args["listen"] = types.make_address(listen_addresses, manifest.port)

    args.setdefault("use_unix_socket", True)
    args.setdefault("use_unix_socket_repl", True)
    args.setdefault("data_dir", instance.datadir)
    args.setdefault("bin_dir", instance.bindir)
    if "pg_hba" not in args:
        args["pg_hba"] = manifest.pg_hba(settings).splitlines()
    if "pg_ident" not in args:
        args["pg_ident"] = manifest.pg_ident(settings).splitlines()

    if "create_replica_methods" not in args:
        args["create_replica_methods"] = []
        for method, config in filter(
            None,
            await async_hooks(
                settings,
                h.patroni_create_replica_method,
                manifest=manifest,
                instance=instance,
            ),
        ):
            args["create_replica_methods"].append(method)
            args[method] = config
        args["create_replica_methods"].append("basebackup")
        args.setdefault("basebackup", [{"waldir": instance.waldir}])
    return args


def etcd(model: Optional[i.Etcd], settings: Settings, **args: Any) -> dict[str, Any]:
    if args:
        return args
    return settings.etcd.model_dump(mode="json", exclude={"v2"}, exclude_none=True) | (
        export_model(model) if model is not None else {}
    )


class _BaseModel(types.BaseModel, extra="allow"):
    """A BaseModel with extra inputs allowed.

    >>> types.BaseModel(x=1)
    Traceback (most recent call last):
        ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for BaseModel
    x
      Extra inputs are not permitted [type=extra_forbidden, input_value=1, input_type=int]
      ...
    >>> _BaseModel(x=1)
    _BaseModel(x=1)
    """


class PostgreSQL(_BaseModel):
    connect_address: types.Address
    listen: types.Address
    parameters: dict[str, Any]


class RESTAPI(common.RESTAPI, _BaseModel):
    cafile: Optional[Path] = None
    certfile: Optional[Path] = None
    keyfile: Optional[Path] = None
    verify_client: Optional[Literal["optional", "required"]] = None


class Patroni(_BaseModel):
    """A partial representation of a patroni instance, as defined in a YAML
    configuration.

    Only fields that are handled explicitly on our side are modelled here.
    Other fields are loaded as "extra" (allowed by _BaseModel class).
    """

    scope: Annotated[str, Field(description="Cluster name.")]
    name: Annotated[str, Field(description="Host name.")]
    restapi: Annotated[RESTAPI, Field(default_factory=RESTAPI)]
    postgresql: PostgreSQL

    @classmethod
    async def build(
        cls,
        settings: Settings,
        service: i.ServiceManifest,
        instance: system.BaseInstance,
        manifest: interface.Instance,
        configuration: pgtoolkit.conf.Configuration,
        **args: Any,
    ) -> Self:
        """Build a Patroni instance from passed arguments."""
        if "bootstrap" not in args:
            args["bootstrap"] = bootstrap(instance, manifest)
        args["postgresql"] = await postgresql(
            instance,
            manifest,
            configuration,
            service.postgresql,
            **args.pop("postgresql", {}),
        )
        dcs = "etcd" if settings.etcd.v2 else "etcd3"
        args[dcs] = etcd(service.etcd, settings, **args.pop(dcs, {}))
        return cls(**args)

    @classmethod
    def get(cls, qualname: str, settings: Settings) -> Self:
        """Get a Patroni instance from its qualified name, by loading
        respective YAML configuration file.
        """
        if not (fpath := impl._configpath(qualname, settings)).exists():
            raise exceptions.FileNotFoundError(
                f"Patroni configuration for {qualname} node not found"
            )
        with fpath.open() as f:
            data = yaml.safe_load(f)
        return cls.model_validate(data)

    def yaml(self, **kwargs: Any) -> str:
        data = self.model_dump(mode="json", exclude_none=True, **kwargs)
        return yaml.dump(data, sort_keys=True)
