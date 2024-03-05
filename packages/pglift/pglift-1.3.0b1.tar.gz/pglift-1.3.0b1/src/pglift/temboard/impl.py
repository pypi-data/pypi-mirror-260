# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import configparser
import json
import logging
from pathlib import Path

import pydantic
from pgtoolkit import conf as pgconf

from .. import async_hook, exceptions, h
from .. import service as service_mod
from .. import util
from ..models import interface, system
from ..settings import Settings, _temboard
from ..task import task
from .models import Service, ServiceManifest, service_name

logger = logging.getLogger(__name__)


def available(settings: Settings) -> _temboard.Settings | None:
    return settings.temboard


def get_settings(settings: Settings) -> _temboard.Settings:
    """Return settings for temboard

    Same as `available` but assert that settings are not None.
    Should be used in a context where settings for the plugin are surely
    set (for example in hookimpl).
    """
    assert settings.temboard is not None
    return settings.temboard


def enabled(qualname: str, settings: _temboard.Settings) -> bool:
    return _configpath(qualname, settings).exists()


def _args(execpath: Path, configpath: Path) -> list[str]:
    return [str(execpath), "--config", str(configpath)]


def _configpath(qualname: str, settings: _temboard.Settings) -> Path:
    return Path(str(settings.configpath).format(name=qualname))


def _homedir(qualname: str, settings: _temboard.Settings) -> Path:
    return Path(str(settings.home).format(name=qualname))


def _pidfile(qualname: str, settings: _temboard.Settings) -> Path:
    return Path(str(settings.pid_file).format(name=qualname))


def _logfile(qualname: str, settings: _temboard.Settings) -> Path:
    return settings.logpath / f"temboard_agent_{qualname}.log"


def config_var(configpath: Path, *, name: str, section: str) -> str:
    """Return temboardagent configuration value for given 'name' in 'section'."""
    if not configpath.exists():
        raise exceptions.FileNotFoundError(
            f"temboard agent configuration file {configpath} not found"
        )
    cp = configparser.ConfigParser()
    cp.read(configpath)
    for s, items in cp.items():
        if s != section:
            continue
        try:
            return items[name]
        except KeyError:
            pass
    raise exceptions.ConfigurationError(
        configpath, f"{name} not found in {section} section"
    )


def port(qualname: str, settings: _temboard.Settings) -> int:
    configpath = _configpath(qualname, settings)
    return int(config_var(configpath, name="port", section="temboard"))


def password(qualname: str, settings: _temboard.Settings) -> str | None:
    configpath = _configpath(qualname, settings)
    try:
        return config_var(configpath, name="password", section="postgresql")
    except exceptions.ConfigurationError:
        return None


def system_lookup(
    name: str, settings: _temboard.Settings, *, warn: bool = True
) -> Service | None:
    try:
        p_ = port(name, settings)
        passwd_ = password(name, settings)
    except exceptions.FileNotFoundError as exc:
        if warn:
            logger.debug(
                "failed to read temboard-agent configuration %s: %s", name, exc
            )
        return None
    else:
        password_ = None
        if passwd_ is not None:
            password_ = pydantic.SecretStr(passwd_)
        return Service(name=name, settings=settings, port=p_, password=password_)


@task
async def setup(
    instance: system.PostgreSQLInstance,
    manifest: interface.Instance,
    settings: _temboard.Settings,
    instance_config: pgconf.Configuration,
) -> None:
    """Setup temboardAgent"""
    service_manifest = manifest.service_manifest(ServiceManifest)
    configpath = _configpath(instance.qualname, settings)

    password_: str | None = None
    if not configpath.exists():
        if service_manifest.password:
            password_ = service_manifest.password.get_secret_value()
    else:
        # Get the password from config file
        password_ = password(instance.qualname, settings)

    cp = configparser.ConfigParser()
    cp["temboard"] = {
        "port": str(service_manifest.port),
        "plugins": json.dumps(settings.plugins),
        "ssl_cert_file": str(settings.certificate.cert),
        "ssl_key_file": str(settings.certificate.key),
        "home": str(_homedir(instance.qualname, settings)),
        "ui_url": str(settings.ui_url),
        "signing_public_key": str(settings.signing_key),
    }
    if settings.certificate.ca_cert:
        cp["temboard"]["ssl_ca_cert_file"] = str(settings.certificate.ca_cert)

    cp["postgresql"] = {
        "user": settings.role,
        "instance": instance.qualname,
    }
    if "port" in instance_config:
        cp["postgresql"]["port"] = str(instance_config["port"])
    if "unix_socket_directories" in instance_config:
        pghost = instance_config.unix_socket_directories.split(",")[0]  # type: ignore[union-attr]
        cp["postgresql"]["host"] = pghost
    if password_:
        cp["postgresql"]["password"] = password_
    cp["logging"] = {
        "method": settings.logmethod,
        "level": settings.loglevel,
    }
    if settings.logmethod == "file":
        cp["logging"]["destination"] = str(_logfile(instance.qualname, settings))

    name = instance.qualname
    needs_restart = False
    if service := system_lookup(name, settings, warn=False):
        assert configpath.exists()
        cp_actual = configparser.ConfigParser()
        cp_actual.read(configpath)
        if cp != cp_actual:
            logger.info("reconfiguring temboard agent %s", name)
            with configpath.open("w") as configfile:
                cp.write(configfile)
            needs_restart = True
    else:
        logger.info("configuring temboard agent %s", name)
        configpath.parent.mkdir(mode=0o700, exist_ok=True, parents=True)
        configpath.touch(mode=0o600)
        with configpath.open("w") as configfile:
            cp.write(configfile)

        homedir = _homedir(name, settings)
        homedir.mkdir(mode=0o700, exist_ok=True, parents=True)

        pidfile = _pidfile(name, settings)
        pidfile.parent.mkdir(mode=0o700, exist_ok=True, parents=True)

        service = system_lookup(name, settings)
        assert service is not None

    s = instance._settings
    await async_hook(
        s, h.enable_service, settings=s, service=service_name, name=instance.qualname
    )

    if needs_restart:
        await restart(s, service)


@setup.revert(title="deconfiguring temboard agent")
async def revert_setup(
    instance: system.PostgreSQLInstance,
    manifest: interface.Instance,
    settings: _temboard.Settings,
    instance_config: pgconf.Configuration,
) -> None:
    """Un-setup temboard"""
    _configpath(instance.qualname, settings).unlink(missing_ok=True)
    _pidfile(instance.qualname, settings).unlink(missing_ok=True)
    _logfile(instance.qualname, settings).unlink(missing_ok=True)
    homedir = _homedir(instance.qualname, settings)
    if homedir.exists():
        util.rmtree(homedir)
    s = instance._settings
    await async_hook(
        s,
        h.disable_service,
        settings=s,
        service=service_name,
        name=instance.qualname,
        now=True,
    )


async def start(
    settings: Settings, service: Service, *, foreground: bool = False
) -> None:
    logger.info("starting temboard-agent %s", service.name)
    await service_mod.start(settings, service, foreground=foreground)


async def stop(settings: Settings, service: Service) -> None:
    logger.info("stopping temboard-agent %s", service.name)
    await service_mod.stop(settings, service)


async def restart(settings: Settings, service: Service) -> None:
    logger.info("restarting temboard-agent %s", service.name)
    await service_mod.restart(settings, service)
