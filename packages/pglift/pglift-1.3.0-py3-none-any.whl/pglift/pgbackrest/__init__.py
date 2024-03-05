# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import shlex
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Literal

import pgtoolkit.conf as pgconf
from pydantic import Field
from pydantic.fields import FieldInfo

from .. import cmd, hookimpl, util
from ..models import interface, system
from ..settings import Settings, _pgbackrest
from . import base, models
from .base import available as available
from .base import get_settings as get_settings
from .base import iter_backups as iter_backups
from .base import restore as restore
from .models import ServiceManifest

__all__ = ["available", "backup", "iter_backups", "restore"]

logger = logging.getLogger(__name__)


def register_if(settings: Settings) -> bool:
    return available(settings) is not None


def dirs(settings: _pgbackrest.Settings) -> list[tuple[Path, str]]:
    return [(settings.logpath, "log"), (settings.spoolpath, "spool")]


@hookimpl
async def site_configure_install(settings: Settings) -> None:
    s = get_settings(settings)
    for d, purpose in dirs(s):
        if not d.exists():
            logger.info("creating pgBackRest %s directory", purpose)
            d.mkdir(exist_ok=True, parents=True)


@hookimpl
async def site_configure_uninstall(settings: Settings) -> None:
    s = get_settings(settings)
    for d, purpose in dirs(s):
        if d.exists():
            logger.info("deleting pgBackRest %s directory", purpose)
            util.rmdir(d)


@hookimpl
def site_configure_check(settings: Settings, log: bool) -> Iterator[bool]:
    s = get_settings(settings)
    for d, purpose in dirs(s):
        if not d.exists():
            if log:
                logger.error("pgBackRest %s directory '%s' not found", purpose, d)
            yield False
        else:
            yield True


@hookimpl
def system_lookup(instance: system.PostgreSQLInstance) -> models.Service | None:
    settings = get_settings(instance._settings)
    return base.system_lookup(instance.datadir, settings)


@hookimpl
async def get(instance: system.Instance) -> models.ServiceManifest | None:
    try:
        s = instance.service(models.Service)
    except ValueError:
        return None
    else:
        return models.ServiceManifest(stanza=s.stanza)


@hookimpl
def instance_settings(
    manifest: interface.Instance, instance: system.BaseInstance
) -> pgconf.Configuration:
    settings = get_settings(instance._settings)
    service_manifest = manifest.service_manifest(ServiceManifest)
    return base.postgresql_configuration(
        service_manifest.stanza, settings, instance.datadir
    )


@hookimpl
def interface_model() -> tuple[str, Any, FieldInfo]:
    return (
        models.ServiceManifest.__service__,
        models.ServiceManifest,
        Field(
            description="Configuration for the pgBackRest service, if enabled in site settings.",
            json_schema_extra={"readOnly": True},
        ),
    )


async def initdb_restore_command(
    instance: system.BaseInstance, manifest: interface.Instance
) -> list[str] | None:
    settings = get_settings(instance._settings)
    service_manifest = manifest.service_manifest(ServiceManifest)
    service = base.service(instance, service_manifest, settings, None)
    if not (await base.backup_info(service, settings))["backup"]:
        return None
    cmd_args = [
        str(settings.execpath),
        "--log-level-file=off",
        "--log-level-stderr=info",
        "--config-path",
        str(settings.configpath),
        "--stanza",
        service_manifest.stanza,
        "--pg1-path",
        str(instance.datadir),
    ]
    if instance.waldir != instance.datadir / "pg_wal":
        cmd_args.extend(["--link-map", f"pg_wal={instance.waldir}"])
    if manifest.standby:
        cmd_args.append("--type=standby")
        # Double quote if needed (e.g. to escape white spaces in value).
        value = manifest.standby.full_primary_conninfo.replace("'", "''")
        cmd_args.extend(["--recovery-option", f"primary_conninfo={value}"])
        if manifest.standby.slot:
            cmd_args.extend(
                ["--recovery-option", f"primary_slot_name={manifest.standby.slot}"]
            )
    cmd_args.append("restore")
    return cmd_args


@hookimpl
async def patroni_create_replica_method(
    manifest: interface.Instance, instance: system.BaseInstance
) -> tuple[str, dict[str, Any]] | None:
    if (args := (await initdb_restore_command(instance, manifest))) is None:
        return None
    return "pgbackrest", {
        "command": shlex.join(args),
        "keep_data": True,
        "no_params": True,
    }


@hookimpl
async def initdb(
    manifest: interface.Instance, instance: system.BaseInstance
) -> Literal[True] | None:
    if (args := await initdb_restore_command(instance, manifest)) is None:
        return None
    logger.info("restoring from a pgBackRest backup")
    await cmd.asyncio_run(args, check=True)
    return True


@hookimpl
async def instance_promoted(instance: system.Instance) -> None:
    if service_manifest := await get(instance):
        settings = get_settings(instance._settings)
        service = base.service(instance, service_manifest, settings, None)
        await base.check(instance, service, settings, None)


@hookimpl
def instance_env(instance: system.Instance) -> dict[str, str]:
    pgbackrest_settings = base.get_settings(instance._settings)
    try:
        service = instance.service(models.Service)
    except ValueError:
        return {}
    return base.env_for(service, pgbackrest_settings)


@hookimpl
def rolename(settings: Settings) -> str:
    return settings.postgresql.backuprole.name


@hookimpl
def role(settings: Settings, manifest: interface.Instance) -> interface.Role | None:
    name = rolename(settings)
    service_manifest = manifest.service_manifest(ServiceManifest)
    extra = {}
    if settings.postgresql.auth.passfile is not None:
        extra["pgpass"] = settings.postgresql.backuprole.pgpass
    return interface.Role(
        name=name,
        password=service_manifest.password,
        login=True,
        superuser=True,
        **extra,
    )


@hookimpl
def logrotate_config(settings: Settings) -> str:
    assert settings.logrotate is not None
    s = get_settings(settings)
    return util.template("pgbackrest", "logrotate.conf").format(logpath=s.logpath)
