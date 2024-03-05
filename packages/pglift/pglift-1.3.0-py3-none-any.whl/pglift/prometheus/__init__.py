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
from .. import systemd
from ..models import interface, system
from ..settings import Settings
from ..types import Status
from . import impl, models
from .impl import apply as apply
from .impl import available as available
from .impl import get_settings as get_settings
from .impl import start as start
from .impl import stop as stop
from .models import PostgresExporter as PostgresExporter
from .models import ServiceManifest

__all__ = ["PostgresExporter", "apply", "available", "start", "stop"]

logger = logging.getLogger(__name__)


def register_if(settings: Settings) -> bool:
    return available(settings) is not None


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
            description="Configuration for the Prometheus service, if enabled in site settings.",
        ),
    )


@hookimpl
async def get(instance: system.Instance) -> models.ServiceManifest | None:
    try:
        s = instance.service(models.Service)
    except ValueError:
        return None
    else:
        return models.ServiceManifest(port=s.port, password=s.password)


SYSTEMD_SERVICE_NAME = "pglift-postgres_exporter@.service"


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
async def instance_configured(
    instance: system.PostgreSQLInstance,
    manifest: interface.Instance,
    config: Configuration,
) -> None:
    """Install postgres_exporter for an instance when it gets configured."""
    settings = get_settings(instance._settings)
    await impl.setup_local(instance, manifest, settings, config)


@hookimpl
async def instance_started(instance: system.Instance) -> None:
    """Start postgres_exporter service."""
    try:
        service = instance.service(models.Service)
    except ValueError:
        return
    await impl.start(instance._settings, service)


@hookimpl
async def instance_stopped(instance: system.Instance) -> None:
    """Stop postgres_exporter service."""
    try:
        service = instance.service(models.Service)
    except ValueError:
        return
    await impl.stop(instance._settings, service)


@hookimpl
async def instance_dropped(instance: system.Instance) -> None:
    """Uninstall postgres_exporter from an instance being dropped."""
    settings = instance._settings
    prometheus_settings = get_settings(settings)
    await impl.revert_setup(instance.qualname, settings, prometheus_settings)


@hookimpl
def role(settings: Settings, manifest: interface.Instance) -> interface.Role | None:
    service_manifest = manifest.service_manifest(ServiceManifest)
    assert settings.prometheus is not None
    return interface.Role(
        name=settings.prometheus.role,
        password=service_manifest.password,
        login=True,
        in_roles=["pg_monitor"],
    )


@hookimpl
async def instance_status(instance: system.Instance) -> tuple[Status, str] | None:
    try:
        service = instance.service(models.Service)
    except ValueError:
        return None
    return (await service_mod.status(instance._settings, service), "prometheus")
