# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from collections.abc import Iterator
from typing import Any

from . import async_hook, execpath, hookimpl
from . import hookspecs as h
from . import systemd
from .models import system
from .pgbackrest import repo_path
from .settings import Settings

logger = logging.getLogger(__name__)
service_name = "backup"
BACKUP_SERVICE_NAME = "pglift-backup@.service"
BACKUP_TIMER_NAME = "pglift-backup@.timer"


def register_if(settings: Settings) -> bool:
    return (
        settings.service_manager == "systemd"
        and settings.scheduler == "systemd"
        and settings.pgbackrest is not None
        and repo_path.register_if(settings)
    )


@hookimpl
def systemd_units() -> list[str]:
    return [BACKUP_SERVICE_NAME, BACKUP_TIMER_NAME]


@hookimpl
def systemd_unit_templates(
    settings: Settings, env: dict[str, Any]
) -> Iterator[tuple[str, str]]:
    yield BACKUP_SERVICE_NAME, systemd.template(BACKUP_SERVICE_NAME).format(
        executeas=systemd.executeas(settings),
        environment=systemd.environment(env),
        execpath=execpath,
    )
    yield BACKUP_TIMER_NAME, systemd.template(BACKUP_TIMER_NAME)


@hookimpl
async def instance_configured(instance: system.BaseInstance) -> None:
    """Enable scheduled backup job for configured instance."""
    s = instance._settings
    await async_hook(
        s,
        h.schedule_service,
        settings=s,
        service=service_name,
        name=instance.qualname,
    )


@hookimpl
async def instance_dropped(instance: system.BaseInstance) -> None:
    """Disable scheduled backup job when instance is being dropped."""
    s = instance._settings
    await async_hook(
        s,
        h.unschedule_service,
        settings=s,
        service=service_name,
        name=instance.qualname,
        now=True,
    )


@hookimpl
async def instance_started(instance: system.BaseInstance) -> None:
    """Start schedule backup job at instance startup."""
    s = instance._settings
    await async_hook(
        s,
        h.start_timer,
        settings=s,
        service=service_name,
        name=instance.qualname,
    )


@hookimpl
async def instance_stopped(instance: system.BaseInstance) -> None:
    """Stop schedule backup job when instance is stopping."""
    s = instance._settings
    await async_hook(
        s,
        h.stop_timer,
        settings=s,
        service=service_name,
        name=instance.qualname,
    )
