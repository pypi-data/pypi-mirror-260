# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from collections.abc import Iterator
from pathlib import Path

from pgtoolkit.conf import Configuration

from .. import h, hookimpl, hooks, util
from ..models import system
from ..settings import Settings, _rsyslog

logger = logging.getLogger(__name__)


def register_if(settings: Settings) -> bool:
    return settings.rsyslog is not None


def get_settings(settings: Settings) -> _rsyslog.Settings:
    assert settings.rsyslog is not None
    return settings.rsyslog


def config_path(settings: _rsyslog.Settings) -> Path:
    return settings.configdir / "rsyslog.conf"


@hookimpl
async def site_configure_install(settings: Settings) -> None:
    s = get_settings(settings)
    if (fpath := config_path(s)).exists():
        return
    if not s.configdir.exists():
        logger.info("creating rsyslog config directory")
        s.configdir.mkdir(mode=0o750, exist_ok=True, parents=True)
    configs = hooks(settings, h.rsyslog_config, settings=settings)
    with fpath.open("w") as f:
        logger.info("writing rsyslog config")
        f.write("\n".join(configs))


@hookimpl
async def site_configure_uninstall(settings: Settings) -> None:
    s = get_settings(settings)
    if s.configdir.exists():
        logger.info("deleting rsyslog config directory")
        util.rmtree(s.configdir)


@hookimpl
def site_configure_check(settings: Settings, log: bool) -> Iterator[bool]:
    s = get_settings(settings)
    if not (fpath := config_path(s)).exists():
        if log:
            logger.error("rsyslog configuration file '%s' missing", fpath)
        yield False
    else:
        yield True


@hookimpl
def instance_settings(instance: system.BaseInstance) -> Configuration:
    pgconfig = util.template("postgresql", "postgresql-rsyslog.conf").format(
        name=instance.name,
        version=instance.version,
    )
    config = Configuration()
    list(config.parse(pgconfig.splitlines()))
    return config
