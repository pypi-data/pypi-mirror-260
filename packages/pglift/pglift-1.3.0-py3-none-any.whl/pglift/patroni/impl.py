# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import asyncio
import logging
import socket
import subprocess
import tempfile
import time
import urllib.parse
from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager, contextmanager
from functools import partial
from pathlib import Path
from typing import IO, Any

import httpx
import pgtoolkit.conf
import tenacity
import yaml
from tenacity import AsyncRetrying
from tenacity.before_sleep import before_sleep_log
from tenacity.retry import retry_if_exception_type
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_exponential, wait_fixed

from .. import conf, exceptions, postgresql
from .. import service as service_mod
from .. import types, ui
from ..models import interface, system
from ..settings import Settings, _patroni
from ..task import task
from .models import ClusterMember, Patroni, Service, ServiceManifest

logger = logging.getLogger(__name__)


def available(settings: Settings) -> _patroni.Settings | None:
    return settings.patroni


def get_settings(settings: Settings) -> _patroni.Settings:
    """Return settings for patroni

    Same as `available` but assert that settings are not None.
    Should be used in a context where settings for the plugin are surely
    set (for example in hookimpl).
    """
    assert settings.patroni is not None
    return settings.patroni


def enabled(qualname: str, settings: _patroni.Settings) -> bool:
    return _configpath(qualname, settings).exists()


def _configpath(qualname: str, settings: _patroni.Settings) -> Path:
    return Path(str(settings.configpath).format(name=qualname))


def _pgpass(qualname: str, settings: _patroni.PostgreSQL) -> Path:
    return Path(str(settings.passfile).format(name=qualname))


def logdir(qualname: str, settings: _patroni.Settings) -> Path:
    return settings.logpath / qualname


def validate_config(content: str, settings: _patroni.Settings) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".yaml") as f:
        f.write(content)
        f.seek(0)
        try:
            subprocess.run(  # nosec B603
                [str(settings.execpath), "--validate-config", f.name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            logger.warning("invalid Patroni configuration: %s", e.stdout.strip())


def write_config(
    name: str, config: Patroni, settings: _patroni.Settings, *, validate: bool = False
) -> None:
    """Write Patroni YAML configuration to disk after validation."""
    content = config.yaml()
    if validate:
        validate_config(content, settings)
    path = _configpath(name, settings)
    path.parent.mkdir(mode=0o750, exist_ok=True, parents=True)
    path.write_text(content)
    path.chmod(0o600)


async def maybe_backup_config(
    qualname: str, *, node: str, cluster: str, settings: _patroni.Settings
) -> None:
    """Make a backup of Patroni configuration for 'qualname' instance
    alongside the original file, if 'node' is the last member in 'cluster'.
    """
    configpath = _configpath(qualname, settings)
    members = await cluster_members(qualname, settings)
    if len(members) == 1 and members[0].name == node:
        backupname = f"{cluster}-{node}-{time.time()}"
        backuppath = configpath.parent / f"{backupname}.yaml"
        logger.warning(
            "'%s' appears to be the last member of cluster '%s', "
            "saving Patroni configuration file to %s",
            node,
            cluster,
            backuppath,
        )
        backuppath.write_text(
            f"# Backup of Patroni configuration for instance {qualname!r}\n"
            + configpath.read_text()
        )
        if (pgpass := _pgpass(qualname, settings.postgresql)).exists():
            (configpath.parent / f"{backupname}.pgpass").write_text(pgpass.read_text())


def postgresql_changes(
    qualname: str, patroni: Patroni, settings: _patroni.Settings
) -> types.ConfigChanges:
    """Return changes to PostgreSQL parameters w.r.t. to actual Patroni configuration."""
    config_before = {}
    if _configpath(qualname, settings).exists():
        config_before = Patroni.get(qualname, settings).postgresql.parameters
    # Round-trip dump/load in order to get the suppress serialization effects
    # (e.g. timedelta to / from str).
    config_after = yaml.safe_load(patroni.yaml())["postgresql"]["parameters"]
    return conf.changes(config_before, config_after)


async def api_request(
    patroni: Patroni, method: str, path: str, **kwargs: Any
) -> httpx.Response:
    protocol = "http"
    verify: bool | str = True
    if patroni.restapi.cafile:
        protocol = "https"
        verify = str(patroni.restapi.cafile)
    url = urllib.parse.urlunparse((protocol, patroni.restapi.listen, path, "", "", ""))
    cert: tuple[str, str] | None = None
    if patroni.restapi.certfile and patroni.restapi.keyfile:
        cert = (str(patroni.restapi.certfile), str(patroni.restapi.keyfile))
    async with httpx.AsyncClient(verify=verify, cert=cert) as client:
        r = await client.request(method, url, **kwargs)
    r.raise_for_status()
    return r


@asynccontextmanager
async def setup(
    instance: system.BaseInstance,
    manifest: interface.Instance,
    service: ServiceManifest,
    settings: _patroni.Settings,
    configuration: pgtoolkit.conf.Configuration,
    *,
    validate: bool = False,
) -> AsyncIterator[Patroni]:
    """Context manager setting up Patroni for instance *in memory*, yielding
    the Patroni object, and writing to disk upon successful exit.
    """
    logger.info("setting up Patroni service")
    logpath = logdir(instance.qualname, settings)
    logpath.mkdir(exist_ok=True, parents=True)
    if (p := _configpath(instance.qualname, settings)).exists():
        with p.open() as f:
            args = yaml.safe_load(f)
    else:
        args = {}
    args.setdefault("scope", service.cluster)
    args.setdefault("name", service.node)
    args.setdefault("log", {"dir": logpath})
    args.setdefault("watchdog", settings.watchdog)
    args.setdefault(
        "restapi",
        settings.restapi.model_dump(mode="json")
        | service.restapi.model_dump(mode="json"),
    )
    args.setdefault("ctl", settings.ctl)
    args.setdefault(
        "postgresql",
        {
            "use_pg_rewind": settings.postgresql.use_pg_rewind,
            "pgpass": _pgpass(instance.qualname, settings.postgresql),
        },
    )
    patroni = await Patroni.build(
        settings, service, instance, manifest, configuration, **args
    )
    yield patroni
    write_config(instance.qualname, patroni, settings, validate=validate)


@task(title="bootstrapping PostgreSQL with Patroni")
async def init(
    instance: system.BaseInstance, patroni: Patroni, service: Service
) -> None:
    """Call patroni for bootstrap.

    Then wait for Patroni to bootstrap by checking that (1) the postgres
    instance exists, (2) that it's up and running and, (3) that Patroni REST
    API is ready.

    At each retry, log new lines found in Patroni and PostgreSQL logs to our
    logger.
    """

    @tenacity.retry(
        retry=retry_if_exception_type(exceptions.FileNotFoundError),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        stop=stop_after_attempt(5),
        before_sleep=before_sleep_log(logger, logging.DEBUG),
        reraise=True,
    )
    def wait_logfile(
        instance: system.BaseInstance, settings: _patroni.Settings
    ) -> Path:
        logfile = logdir(instance.qualname, settings) / "patroni.log"
        if not logfile.exists():
            raise exceptions.FileNotFoundError("Patroni log file not found (yet)")
        logger.debug("Patroni log file found %s", logfile)
        return logfile

    def postgres_logfile(instance: system.PostgreSQLInstance) -> IO[str] | None:
        try:
            postgres_logpath = next(postgresql.logfile(instance, timeout=0))
        except exceptions.FileNotFoundError:
            # File current_logfiles not found
            return None
        logger.debug("reading current PostgreSQL logs from %s", postgres_logpath)
        try:
            return postgres_logpath.open()
        except OSError as e:
            # Referenced file not created yet or gone?
            logger.warning(
                "failed to open PostgreSQL log file %s (%s)", postgres_logpath, e
            )
            return None

    def log_process(f: IO[str], level: int, *, execpath: Path) -> None:
        for line in f:
            logger.log(level, "%s: %s", execpath, line.rstrip())

    await start(instance._settings, service, foreground=False)

    patroni_settings = service.settings
    logf = wait_logfile(instance, patroni_settings)
    log_patroni = partial(log_process, execpath=patroni_settings.execpath)
    log_postgres = partial(log_process, execpath=instance.bindir / "postgres")

    retry_ctrl = AsyncRetrying(
        retry=(
            retry_if_exception_type(exceptions.InstanceNotFound)
            | retry_if_exception_type(exceptions.InstanceStateError)
            | retry_if_exception_type(httpx.HTTPError)
        ),
        # Retry indefinitely (no 'stop' option), waiting exponentially until
        # the 10s delay gets reached (and then waiting fixed).
        wait=wait_exponential(multiplier=1, min=1, max=10),
        before_sleep=before_sleep_log(logger, logging.DEBUG),
    )

    with logstream(logf) as f:
        postgres_logf: IO[str] | None = None
        pginstance: system.PostgreSQLInstance | None = None
        try:
            async for attempt in retry_ctrl:
                with attempt:
                    level = logging.DEBUG
                    if not await check_api_status(instance.qualname, patroni_settings):
                        level = logging.WARNING
                    log_patroni(f, level)

                    if pginstance is None:
                        pginstance = system.PostgreSQLInstance.system_lookup(instance)
                        logger.info(
                            "PostgreSQL instance %s created by Patroni", pginstance
                        )

                    if postgres_logf := (postgres_logf or postgres_logfile(pginstance)):
                        log_postgres(postgres_logf, level)

                    if not await postgresql.is_ready(pginstance):
                        raise exceptions.InstanceStateError(f"{instance} not ready")

                    logger.debug("checking Patroni readiness")
                    await api_request(patroni, "GET", "readiness")

        except tenacity.RetryError as retry_error:
            if ui.confirm("Patroni failed to start, abort?", default=False):
                raise exceptions.Cancelled(
                    f"Patroni {instance.qualname} start cancelled"
                ) from retry_error.last_attempt.result()
        finally:
            if postgres_logf:
                postgres_logf.close()

    logger.info("instance %s successfully created by Patroni", instance)


@init.revert(title="deconfiguring Patroni service")
async def revert_init(
    instance: system.BaseInstance, patroni: Patroni, service: Service
) -> None:
    """Call patroni for bootstrap."""
    await delete(instance._settings, service)


async def delete(settings: Settings, service: Service) -> None:
    """Remove Patroni configuration for 'instance'."""
    if await check_api_status(service.name, service.settings):
        await maybe_backup_config(
            service.name,
            node=service.node,
            cluster=service.cluster,
            settings=service.settings,
        )
    await stop(settings, service)
    _configpath(service.name, service.settings).unlink(missing_ok=True)
    _pgpass(service.name, service.settings.postgresql).unlink(missing_ok=True)
    (logdir(service.name, service.settings) / "patroni.log").unlink(missing_ok=True)


async def start(
    settings: Settings,
    service: Service,
    *,
    foreground: bool = False,
) -> None:
    logger.info("starting Patroni %s", service.name)
    await service_mod.start(settings, service, foreground=foreground)


async def stop(settings: Settings, service: Service) -> None:
    logger.info("stopping Patroni %s", service.name)
    await service_mod.stop(settings, service)
    await wait_api_down(service.name, service.settings)


async def restart(
    instance: system.BaseInstance, settings: _patroni.Settings, timeout: int = 3
) -> None:
    logger.info("restarting Patroni %s", instance.qualname)
    patroni = Patroni.get(instance.qualname, settings)
    await api_request(patroni, "POST", "restart", json={"timeout": timeout})


async def reload(instance: system.BaseInstance, settings: _patroni.Settings) -> None:
    logger.info("reloading Patroni %s", instance.qualname)
    patroni = Patroni.get(instance.qualname, settings)
    await api_request(patroni, "POST", "reload")


async def cluster_members(
    qualname: str, settings: _patroni.Settings
) -> list[ClusterMember]:
    """Return the list of members of the Patroni cluster which 'instance' is member of."""
    patroni = Patroni.get(qualname, settings)
    r = await api_request(patroni, "GET", "cluster")
    return [ClusterMember(**item) for item in r.json()["members"]]


async def cluster_leader(qualname: str, settings: _patroni.Settings) -> str | None:
    for m in await cluster_members(qualname, settings):
        if m.role == "leader":
            return m.name
    return None


async def check_api_status(
    name: str, settings: _patroni.Settings, *, logger: logging.Logger | None = logger
) -> bool:
    """Return True if the REST API of Patroni with 'name' is listening."""
    patroni = Patroni.get(name, settings)
    api_address = patroni.restapi.listen
    if logger:
        logger.debug(
            "checking status of REST API for Patroni %s at %s", name, api_address
        )
    try:
        _, writer = await asyncio.open_connection(
            types.address_host(api_address),
            types.address_port(api_address),
            family=socket.AF_INET,
        )
        writer.close()
        await writer.wait_closed()
    except OSError as exc:
        if logger:
            logger.error(
                "REST API for Patroni %s not listening at %s: %s",
                name,
                api_address,
                exc,
            )
        return False
    return True


@tenacity.retry(
    retry=retry_if_exception_type(exceptions.Error),
    wait=wait_fixed(1),
    before_sleep=before_sleep_log(logger, logging.DEBUG),
)
async def wait_api_down(name: str, settings: _patroni.Settings) -> None:
    if await check_api_status(name, settings, logger=None):
        raise exceptions.Error("Patroni REST API still running")


@contextmanager
def logstream(logpath: Path) -> Iterator[IO[str]]:
    with logpath.open() as f:
        yield f


def logs(name: str, settings: _patroni.Settings) -> Iterator[str]:
    logf = logdir(name, settings) / "patroni.log"
    if not logf.exists():
        raise exceptions.FileNotFoundError(f"no Patroni logs found at {logf}")
    with logstream(logf) as f:
        yield from f
