# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from collections.abc import Iterator
from typing import Any

from pgtoolkit.conf import Configuration
from pydantic import Field

from .. import hookimpl
from .. import service as service_mod
from .. import systemd, util
from ..models import interface, system
from ..settings import Settings
from ..types import Status
from . import impl, models
from .impl import available as available
from .impl import get_settings

logger = logging.getLogger(__name__)


def register_if(settings: Settings) -> bool:
    return available(settings) is not None


@hookimpl
async def site_configure_install(settings: Settings) -> None:
    s = get_settings(settings)
    if not s.logpath.exists():
        logger.info("creating temBoard log directory")
        s.logpath.mkdir(mode=0o740, parents=True, exist_ok=True)


@hookimpl
async def site_configure_uninstall(settings: Settings) -> None:
    s = get_settings(settings)
    if s.logpath.exists():
        logger.info("deleting temBoard log directory")
        util.rmtree(s.logpath)


@hookimpl
def site_configure_check(settings: Settings, log: bool) -> Iterator[bool]:
    s = get_settings(settings)
    if not s.logpath.exists():
        if log:
            logger.error("temBoard log directory '%s' missing", s.logpath)
        yield False
    else:
        yield True


@hookimpl
def system_lookup(instance: system.PostgreSQLInstance) -> models.Service | None:
    settings = get_settings(instance._settings)
    return impl.system_lookup(instance.qualname, settings)


@hookimpl
def interface_model() -> tuple[str, Any, Any]:
    return (
        models.ServiceManifest.__service__,
        models.ServiceManifest,
        Field(
            default=models.ServiceManifest(),
            description="Configuration for the temBoard service, if enabled in site settings.",
        ),
    )


@hookimpl
async def get(instance: system.Instance) -> models.ServiceManifest | None:
    try:
        s = instance.service(models.Service)
    except ValueError:
        return None
    else:
        return models.ServiceManifest(port=s.port)


SYSTEMD_SERVICE_NAME = "pglift-temboard_agent@.service"


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
        execpath=str(s.execpath),
    )


@hookimpl
async def instance_configured(
    instance: system.PostgreSQLInstance,
    manifest: interface.Instance,
    config: Configuration,
) -> None:
    """Install temboard agent for an instance when it gets configured."""
    settings = get_settings(instance._settings)
    await impl.setup(instance, manifest, settings, config)


@hookimpl
async def instance_started(instance: system.Instance) -> None:
    """Start temboard agent service."""
    try:
        service = instance.service(models.Service)
    except ValueError:
        return
    await impl.start(instance._settings, service)


@hookimpl
async def instance_stopped(instance: system.Instance) -> None:
    """Stop temboard agent service."""
    try:
        service = instance.service(models.Service)
    except ValueError:
        return
    await impl.stop(instance._settings, service)


@hookimpl
async def instance_dropped(instance: system.Instance) -> None:
    """Uninstall temboard from an instance being dropped."""
    settings = get_settings(instance._settings)
    manifest = interface.Instance(name=instance.name, version=instance.version)
    await impl.revert_setup(instance, manifest, settings, instance.config())


@hookimpl
def rolename(settings: Settings) -> str:
    assert settings.temboard
    return settings.temboard.role


@hookimpl
def role(settings: Settings, manifest: interface.Instance) -> interface.Role:
    name = rolename(settings)
    service_manifest = manifest.service_manifest(models.ServiceManifest)
    return interface.Role(
        name=name, password=service_manifest.password, login=True, superuser=True
    )


@hookimpl
async def instance_status(instance: system.Instance) -> tuple[Status, str] | None:
    try:
        service = instance.service(models.Service)
    except ValueError:
        return None
    return (await service_mod.status(instance._settings, service), "temBoard")
