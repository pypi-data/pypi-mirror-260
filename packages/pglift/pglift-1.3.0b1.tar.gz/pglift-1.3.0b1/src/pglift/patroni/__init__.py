# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from collections.abc import Iterator
from typing import Any, Literal, NoReturn, Optional

import pgtoolkit.conf
from pydantic import Field

from .. import exceptions, hookimpl, instances, postgresql
from .. import service as service_mod
from .. import systemd, types, util
from ..models import interface, system
from ..settings import Settings
from . import impl, models
from .impl import available as available
from .impl import get_settings as get_settings

logger = logging.getLogger(__name__)


def register_if(settings: Settings) -> bool:
    return available(settings) is not None


@hookimpl
def system_lookup(instance: system.BaseInstance) -> models.Service | None:
    settings = get_settings(instance._settings)
    try:
        patroni = models.Patroni.get(instance.qualname, settings)
    except FileNotFoundError:
        return None
    return models.Service(
        cluster=patroni.scope,
        node=patroni.name,
        name=instance.qualname,
        settings=settings,
    )


@hookimpl
def interface_model() -> tuple[str, Any, Any]:
    return (
        models.ServiceManifest.__service__,
        Optional[models.ServiceManifest],
        Field(
            default=None,
            description="Configuration for the Patroni service, if enabled in site settings",
        ),
    )


@hookimpl
async def standby_model(instance: system.Instance) -> NoReturn | None:
    if system_lookup(instance) is None:
        return None
    raise ValueError("standby not supported with Patroni")


@hookimpl
async def get(instance: system.Instance) -> models.ServiceManifest | None:
    settings = get_settings(instance._settings)
    if (s := system_lookup(instance)) is None:
        return None
    config = models.Patroni.get(instance.qualname, settings)
    cluster_members = await impl.cluster_members(instance.qualname, settings)
    return models.ServiceManifest(
        cluster=s.cluster,
        node=s.node,
        postgresql={
            "connect_host": types.address_host(config.postgresql.connect_address)
        },
        restapi=config.restapi,
        cluster_members=cluster_members,
    )


SYSTEMD_SERVICE_NAME = "pglift-patroni@.service"


@hookimpl
def systemd_units() -> list[str]:
    return [SYSTEMD_SERVICE_NAME]


@hookimpl
def systemd_unit_templates(settings: Settings) -> Iterator[tuple[str, str]]:
    s = get_settings(settings)
    configpath = str(s.configpath).replace("{name}", "%i")
    yield SYSTEMD_SERVICE_NAME, systemd.template(SYSTEMD_SERVICE_NAME).format(
        executeas=systemd.executeas(settings),
        configpath=configpath,
        execpath=s.execpath,
    )


@hookimpl
async def initdb(
    manifest: interface.Instance, instance: system.BaseInstance
) -> Literal[True] | None:
    """Initialize PostgreSQL database cluster through Patroni by configuring
    Patroni, then starting it (as the only way to get the actual instance
    created).
    """
    settings = get_settings(instance._settings)
    try:
        service_manifest = manifest.service_manifest(models.ServiceManifest)
    except ValueError:
        return None
    configuration = instances.configuration(manifest, instance)
    async with impl.setup(
        instance,
        manifest,
        service_manifest,
        settings,
        configuration,
        validate=True,
    ) as patroni:
        pass
    service = models.Service(
        cluster=patroni.scope,
        name=instance.qualname,
        node=patroni.name,
        settings=settings,
    )
    await impl.init(instance, patroni, service)
    return True


@hookimpl
async def configure_postgresql(
    manifest: interface.Instance,
    configuration: pgtoolkit.conf.Configuration,
    instance: system.BaseInstance,
) -> types.ConfigChanges | None:
    """Build and validate Patroni configuration, and return changes to PostgreSQL configuration."""
    settings = get_settings(instance._settings)
    try:
        service = manifest.service_manifest(models.ServiceManifest)
    except ValueError:
        return None
    async with impl.setup(
        instance, manifest, service, settings, configuration
    ) as patroni:
        changes = impl.postgresql_changes(instance.qualname, patroni, settings)
    if changes:
        await impl.reload(instance, settings)
    return changes


@hookimpl
def configure_auth(manifest: interface.Instance) -> Literal[False] | None:
    # In 'patroni' is defined in 'manifest', this is a no-op, since pg_hba.conf
    # and pg_ident.conf are installed through Patroni configuration.
    try:
        manifest.service_manifest(models.ServiceManifest)
    except ValueError:
        return None
    return False


@hookimpl
def postgresql_editable_conf(instance: system.PostgreSQLInstance) -> str | None:
    settings = get_settings(instance._settings)
    try:
        patroni = models.Patroni.get(instance.qualname, settings)
    except FileNotFoundError:
        return None
    conf = pgtoolkit.conf.Configuration()
    with conf.edit() as entries:
        for k, v in patroni.postgresql.parameters.items():
            entries.add(k, v)
    return "".join(conf.lines)


@hookimpl
async def start_postgresql(
    instance: system.PostgreSQLInstance, foreground: bool, wait: bool
) -> Literal[True] | None:
    """Start PostgreSQL with Patroni."""
    if (service := system_lookup(instance)) is None:
        return None
    await impl.start(instance._settings, service, foreground=foreground)
    if wait:
        await postgresql.wait_ready(instance)
    return True


@hookimpl
async def stop_postgresql(
    instance: system.BaseInstance, deleting: bool
) -> Literal[True] | None:
    """Stop PostgreSQL through Patroni.

    If 'deleting', do nothing as this will be handled upon by Patroni
    deconfiguration.
    """
    if not deleting:
        if (service := system_lookup(instance)) is None:
            return None
        await impl.stop(instance._settings, service)
    return True


@hookimpl
async def restart_postgresql(instance: system.BaseInstance) -> Literal[True] | None:
    """Restart PostgreSQL with Patroni."""
    settings = get_settings(instance._settings)
    if system_lookup(instance) is None:
        return None
    await impl.restart(instance, settings)
    return True


@hookimpl
async def reload_postgresql(instance: system.BaseInstance) -> Literal[True] | None:
    settings = get_settings(instance._settings)
    if system_lookup(instance) is None:
        return None
    await impl.reload(instance, settings)
    return True


@hookimpl
async def promote_postgresql(instance: system.PostgreSQLInstance) -> NoReturn | None:
    if system_lookup(instance) is None:
        return None
    raise exceptions.UnsupportedError(
        "unsupported operation: instance managed by Patroni"
    )


@hookimpl
def postgresql_service_name(instance: system.BaseInstance) -> str | None:
    if system_lookup(instance) is None:
        return None
    return "patroni"


@hookimpl
async def instance_status(instance: system.Instance) -> tuple[types.Status, str] | None:
    try:
        service = instance.service(models.Service)
    except ValueError:
        return None
    return (await service_mod.status(instance._settings, service), "Patroni API")


@hookimpl
async def instance_dropped(instance: system.Instance) -> None:
    """Uninstall Patroni from an instance being dropped."""
    if system_lookup(instance) is None:
        return
    service = instance.service(models.Service)
    await impl.delete(instance._settings, service)


@hookimpl
def instance_env(instance: system.Instance) -> dict[str, str]:
    settings = get_settings(instance._settings)
    if (s := system_lookup(instance)) is None:
        return {}
    configpath = impl._configpath(instance.qualname, settings)
    assert configpath.exists()
    return {
        "PATRONI_NAME": s.node,
        "PATRONI_SCOPE": s.cluster,
        "PATRONICTL_CONFIG_FILE": str(configpath),
    }


@hookimpl
def logrotate_config(settings: Settings) -> str:
    s = get_settings(settings)
    return util.template("patroni", "logrotate.conf").format(logpath=s.logpath)
