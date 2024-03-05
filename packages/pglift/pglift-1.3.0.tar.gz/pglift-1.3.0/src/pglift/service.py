# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging

from . import async_hook, cmd, h
from .settings import Settings
from .types import Runnable, Status

logger = logging.getLogger(__name__)


async def start(settings: Settings, service: Runnable, *, foreground: bool) -> None:
    """Start a service.

    This will use any service manager plugin, if enabled, and fall back to
    a direct subprocess otherwise.

    If foreground=True, the service is started directly through a subprocess.
    """
    if foreground:
        cmd.execute_program(service.args(), env=service.env())
        return
    if await async_hook(
        settings,
        h.start_service,
        settings=settings,
        service=service.__service_name__,
        name=service.name,
    ):
        return
    pidfile = service.pidfile()
    if cmd.status_program(pidfile) == Status.running:
        logger.debug("service '%s' is already running", service)
        return
    async with cmd.asyncio_start_program(service.args(), pidfile, env=service.env()):
        return


async def stop(settings: Settings, service: Runnable) -> None:
    """Stop a service.

    This will use any service manager plugin, if enabled, and fall back to
    a direct program termination (through service's pidfile) otherwise.
    """
    if await async_hook(
        settings,
        h.stop_service,
        settings=settings,
        service=service.__service_name__,
        name=service.name,
    ):
        return
    pidfile = service.pidfile()
    if cmd.status_program(pidfile) == Status.not_running:
        logger.debug("service '%s' is already stopped", service)
        return
    cmd.terminate_program(pidfile)


async def restart(settings: Settings, service: Runnable) -> None:
    """Restart a service.

    This will use any service manager plugin, if enabled, and fall back to
    stop and start method otherwise.
    """
    if await async_hook(
        settings,
        h.restart_service,
        settings=settings,
        service=service.__service_name__,
        name=service.name,
    ):
        return
    await stop(settings, service)
    await start(settings, service, foreground=False)


async def status(settings: Settings, service: Runnable) -> Status:
    service_status = await async_hook(
        settings,
        h.service_status,
        settings=settings,
        service=service.__service_name__,
        name=service.name,
    )
    if service_status is None:
        pidfile = service.pidfile()
        logger.debug(
            "looking for '%s' service status by its PID at %s", service, pidfile
        )
        return cmd.status_program(pidfile)
    return service_status
