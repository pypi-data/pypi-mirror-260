# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import configparser
import logging
from collections.abc import Iterator
from pathlib import Path

from pgtoolkit import conf as pgconf

from .. import cmd, exceptions, hookimpl, postgresql, types, ui, util
from ..models import interface, system
from ..settings import Settings, _pgbackrest
from ..task import task
from ..types import DEFAULT_BACKUP_TYPE, BackupType, CompletedProcess
from . import base, models
from . import register_if as base_register_if
from . import role
from .base import get_settings

PathRepository = _pgbackrest.PathRepository
logger = logging.getLogger(__name__)


def register_if(settings: Settings) -> bool:
    if not base_register_if(settings):
        return False
    s = get_settings(settings)
    return isinstance(s.repository, PathRepository)


@hookimpl
async def site_configure_install(settings: Settings) -> None:
    s = get_settings(settings)
    base.site_configure_install(settings, base_config(s))
    if not (repo_path := repository_settings(s).path).exists():
        logger.info("creating pgBackRest repository path")
        repo_path.mkdir(exist_ok=True, parents=True)


@hookimpl
async def site_configure_uninstall(settings: Settings) -> None:
    base.site_configure_uninstall(settings)
    s = get_settings(settings)
    # XXX isn't this the responsibility of base.site_configure_uninstall()?
    util.rmdir(s.configpath)
    if (repo_path := repository_settings(s).path).exists():
        if ui.confirm(f"Delete pgbackrest repository path {repo_path}?", False):
            util.rmtree(repo_path)
            logger.info("deleted pgBackRest repository path")


@hookimpl
def site_configure_check(settings: Settings, log: bool) -> Iterator[bool]:
    yield from base.site_configure_check(settings, log)

    s = get_settings(settings)
    if not (repo_path := repository_settings(s).path).exists():
        if log:
            logger.error("pgBackRest repository path %s missing", repo_path)
        yield False
    else:
        yield True


@hookimpl
async def instance_configured(
    instance: system.PostgreSQLInstance,
    manifest: interface.Instance,
    config: pgconf.Configuration,
    changes: types.ConfigChanges,
    creating: bool,
    upgrading_from: system.Instance | None,
) -> None:
    with base.instance_configured(
        instance, manifest, config, changes, creating, upgrading_from
    ) as instance:
        settings = instance._settings
        s = get_settings(settings)
        service_manifest = manifest.service_manifest(models.ServiceManifest)
        service = base.service(instance, service_manifest, s, upgrading_from)
        if creating and upgrading_from is None and base.enabled(instance, s):
            if not ui.confirm(
                f"Stanza {service.stanza!r} already bound to another instance, continue by overwriting it?",
                False,
            ):
                raise exceptions.Cancelled("pgbackrest repository already exists")
            revert_init(service, s, instance.datadir)
            base.revert_setup(
                service,
                s,
                config,
                {},
                False,
                instance.datadir,
                settings.postgresql.backuprole.name,
            )

    if upgrading_from is not None:
        await upgrade(service, s)
    elif creating:
        await init(service, s, instance.datadir)

    if creating and await postgresql.is_running(instance):
        password = None
        backup_role = role(instance._settings, manifest)
        assert backup_role is not None
        if backup_role.password is not None:
            password = backup_role.password.get_secret_value()
        if instance.standby:
            logger.warning("not checking pgBackRest configuration on a standby")
        else:
            await base.check(instance, service, s, password)


@hookimpl
async def instance_dropped(instance: system.Instance) -> None:
    with base.instance_dropped(instance) as service:
        if not service:
            return
        settings = get_settings(instance._settings)
        if not (
            nb_backups := len((await base.backup_info(service, settings))["backup"])
        ) or (
            can_delete_stanza(service, settings, instance.datadir)
            and ui.confirm(
                f"Confirm deletion of {nb_backups} backup(s) for stanza {service.stanza}?",
                False,
            )
        ):
            await delete_stanza(service, settings, instance.datadir)


def repository_settings(settings: _pgbackrest.Settings) -> PathRepository:
    assert isinstance(settings.repository, PathRepository)
    return settings.repository


def base_config(settings: _pgbackrest.Settings) -> configparser.ConfigParser:
    cp = base.parser()
    cp.read_string(
        util.template("pgbackrest", "pgbackrest.conf").format(**dict(settings))
    )
    s = repository_settings(settings)
    cp["global"]["repo1-path"] = str(s.path)
    for opt, value in s.retention:
        cp["global"][f"repo1-retention-{opt}"] = str(value)
    return cp


@task(title="creating pgBackRest stanza {service.stanza}")
async def init(
    service: models.Service,
    settings: _pgbackrest.Settings,
    datadir: Path,
) -> None:
    await cmd.asyncio_run(
        base.make_cmd(service.stanza, settings, "stanza-create", "--no-online"),
        check=True,
    )


@init.revert(title="deleting pgBackRest stanza {service.stanza}")
async def revert_init(
    service: models.Service,
    settings: _pgbackrest.Settings,
    datadir: Path,
) -> None:
    if not can_delete_stanza(service, settings, datadir):
        logger.debug(
            "not deleting stanza %s, still used by another instance", service.stanza
        )
        return
    await delete_stanza(service, settings, datadir)


def can_delete_stanza(
    service: models.Service, settings: _pgbackrest.Settings, datadir: Path
) -> bool:
    for idx, path in base.stanza_pgpaths(service.path, service.stanza):
        if (idx, path) != (service.index, datadir):
            return False
    return True


async def delete_stanza(
    service: models.Service, settings: _pgbackrest.Settings, datadir: Path
) -> None:
    stanza = service.stanza
    await cmd.asyncio_run(base.make_cmd(stanza, settings, "stop"), check=True)
    await cmd.asyncio_run(
        base.make_cmd(
            stanza, settings, "stanza-delete", "--pg1-path", str(datadir), "--force"
        ),
        check=True,
    )


async def upgrade(service: models.Service, settings: _pgbackrest.Settings) -> None:
    """Upgrade stanza"""
    stanza = service.stanza
    logger.info("upgrading pgBackRest stanza %s", stanza)
    await cmd.asyncio_run(
        base.make_cmd(stanza, settings, "stanza-upgrade", "--no-online"), check=True
    )


def backup_command(
    instance: system.Instance,
    settings: _pgbackrest.Settings,
    *,
    type: BackupType = DEFAULT_BACKUP_TYPE,
    start_fast: bool = True,
    backup_standby: bool = False,
) -> list[str]:
    """Return the full pgbackrest command to perform a backup for ``instance``.

    :param type: backup type (one of 'full', 'incr', 'diff').

    Ref.: https://pgbackrest.org/command.html#command-backup
    """
    args = [f"--type={type}", "backup"]
    if start_fast:
        args.insert(-1, "--start-fast")
    if backup_standby:
        args.insert(-1, "--backup-standby")
    s = instance.service(models.Service)
    return base.make_cmd(s.stanza, settings, *args)


async def backup(
    instance: system.Instance,
    settings: _pgbackrest.Settings,
    *,
    type: BackupType = DEFAULT_BACKUP_TYPE,
) -> CompletedProcess:
    """Perform a backup of ``instance``.

    :param type: backup type (one of 'full', 'incr', 'diff').

    Ref.: https://pgbackrest.org/command.html#command-backup
    """
    logger.info("backing up instance %s with pgBackRest", instance)
    cmd_args = backup_command(
        instance, settings, type=type, backup_standby=instance.standby is not None
    )
    postgresql_settings = instance._settings.postgresql
    env = postgresql.ctl.libpq_environ(instance, postgresql_settings.backuprole.name)
    return await cmd.asyncio_run(cmd_args, check=True, env=env)
