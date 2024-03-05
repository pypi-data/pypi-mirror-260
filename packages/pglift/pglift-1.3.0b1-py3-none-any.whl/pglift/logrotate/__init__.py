# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from collections.abc import Iterator
from pathlib import Path

from .. import h, hookimpl, hooks, util
from ..models.system import Instance, PostgreSQLInstance
from ..settings import Settings, _logrotate

logger = logging.getLogger(__name__)


def register_if(settings: Settings) -> bool:
    return settings.logrotate is not None


def get_settings(settings: Settings) -> _logrotate.Settings:
    assert settings.logrotate is not None
    return settings.logrotate


def config_path(settings: _logrotate.Settings) -> Path:
    return settings.configdir / "logrotate.conf"


@hookimpl
async def site_configure_install(settings: Settings) -> None:
    s = get_settings(settings)
    if (fpath := config_path(s)).exists():
        return
    if not s.configdir.exists():
        logger.info("creating logrotate config directory")
        s.configdir.mkdir(mode=0o750, exist_ok=True, parents=True)
    configs = hooks(settings, h.logrotate_config, settings=settings)
    with fpath.open("w") as f:
        logger.info("writing logrotate config")
        f.write("\n".join(configs))


@hookimpl
async def site_configure_uninstall(settings: Settings) -> None:
    s = get_settings(settings)
    if s.configdir.exists():
        logger.info("deleting logrotate config directory")
        util.rmtree(s.configdir)


@hookimpl
def site_configure_check(settings: Settings, log: bool) -> Iterator[bool]:
    s = get_settings(settings)
    if not (fpath := config_path(s)).exists():
        if log:
            logger.error("logrotate configuration '%s' missing", fpath)
        yield False
    else:
        yield True


def instance_configpath(
    settings: _logrotate.Settings, instance: PostgreSQLInstance
) -> Path:
    return settings.configdir / f"{instance.qualname}.conf"


@hookimpl
async def instance_dropped(instance: Instance) -> None:
    settings = get_settings(instance._settings)
    instance_configpath(settings, instance).unlink(missing_ok=True)
