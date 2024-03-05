# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import contextlib
import logging
import os
import shutil
import subprocess
import tempfile
from collections.abc import AsyncIterator, Iterator
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

import pgtoolkit.conf as pgconf

from .. import async_hook, cmd, conf, db, execpath, h, hook, hookimpl, systemd, util
from ..models import system
from ..types import ConfigChanges, PostgreSQLStopMode, Status
from .ctl import check_status as check_status  # noqa: F401
from .ctl import is_ready as is_ready  # noqa: F401
from .ctl import is_running as is_running
from .ctl import logfile as logfile  # noqa: F401
from .ctl import logs as logs  # noqa: F401
from .ctl import pg_ctl
from .ctl import replication_lag as replication_lag
from .ctl import status as status  # noqa: F401
from .ctl import wait_ready as wait_ready
from .ctl import wal_sender_state as wal_sender_state
from .models import Standby as Standby

if TYPE_CHECKING:
    from ..models import interface
    from ..settings import Settings

logger = logging.getLogger(__name__)
POSTGRESQL_SERVICE_NAME = "pglift-postgresql@.service"


@hookimpl
async def site_configure_install(settings: Settings) -> None:
    if not settings.postgresql.logpath.exists():
        logger.info("creating PostgreSQL log directory")
        settings.postgresql.logpath.mkdir(mode=0o740, parents=True, exist_ok=True)


@hookimpl
async def site_configure_uninstall(settings: Settings) -> None:
    if settings.postgresql.logpath.exists():
        logger.info("deleting PostgreSQL log directory")
        util.rmtree(settings.postgresql.logpath)


@hookimpl
def site_configure_check(settings: Settings, log: bool) -> Iterator[bool]:
    if not settings.postgresql.logpath.exists():
        if log:
            logger.error(
                "PostgreSQL log directory '%s' missing", settings.postgresql.logpath
            )
        yield False
    else:
        yield True


@hookimpl(trylast=True)
def postgresql_service_name() -> str:
    return "postgresql"


@hookimpl(trylast=True)
async def standby_model(
    instance: system.PostgreSQLInstance, standby: system.Standby, running: bool
) -> Standby:
    values: dict[str, Any] = {
        "primary_conninfo": standby.primary_conninfo,
        "slot": standby.slot,
        "password": standby.password,
    }
    if running:
        values["replication_lag"] = await replication_lag(instance)
    values["wal_sender_state"] = await wal_sender_state(instance)
    return Standby.model_validate(values)


@hookimpl(trylast=True)
def postgresql_editable_conf(instance: system.PostgreSQLInstance) -> str:
    return "".join(instance.config(managed_only=True).lines)


async def init_replication(instance: system.BaseInstance, standby: Standby) -> None:
    with tempfile.TemporaryDirectory() as _tmpdir:
        tmpdir = Path(_tmpdir)
        # pg_basebackup will also copy config files from primary datadir.
        # So to have expected configuration at this stage we have to backup
        # postgresql.conf & pg_hba.conf (created by prior pg_ctl init) and
        # restore after pg_basebackup finishes.
        keep = {"postgresql.conf", "pg_hba.conf"}
        for name in keep:
            shutil.copyfile(instance.datadir / name, tmpdir / name)
        util.rmtree(instance.datadir)
        util.rmtree(instance.waldir)
        cmd_args = [
            str(instance.bindir / "pg_basebackup"),
            "--pgdata",
            str(instance.datadir),
            "--write-recovery-conf",
            "--checkpoint=fast",
            "--no-password",
            "--progress",
            "--verbose",
            "--dbname",
            standby.primary_conninfo,
            "--waldir",
            str(instance.waldir),
        ]

        if standby.slot:
            cmd_args += ["--slot", standby.slot]

        env = None
        if standby.password:
            env = os.environ.copy()
            env["PGPASSWORD"] = standby.password.get_secret_value()
        await cmd.asyncio_run(cmd_args, check=True, env=env)
        for name in keep:
            shutil.copyfile(tmpdir / name, instance.datadir / name)


@hookimpl(trylast=True)
async def initdb(
    manifest: interface.Instance, instance: system.BaseInstance
) -> Literal[True]:
    """Initialize the PostgreSQL database cluster with plain initdb."""
    assert instance.bindir.exists()  # Per BaseInstance.get().
    pgctl = await pg_ctl(instance.bindir)

    settings = instance._settings
    surole = manifest.surole(settings)
    auth_options = manifest.auth_options(settings.postgresql.auth).model_dump(
        exclude={"hostssl"}
    )
    opts = (
        {
            "waldir": str(instance.waldir),
            "username": surole.name,
        }
        | {f"auth_{m}": v for m, v in auth_options.items()}
        | manifest.initdb_options(settings.postgresql.initdb).model_dump(
            exclude_none=True
        )
    )

    if surole.password:
        with tempfile.NamedTemporaryFile("w") as pwfile:
            pwfile.write(surole.password.get_secret_value())
            pwfile.flush()
            await pgctl.init(instance.datadir, pwfile=pwfile.name, **opts)
    else:
        await pgctl.init(instance.datadir, **opts)

    if manifest.standby:
        await init_replication(instance=instance, standby=manifest.standby)

    return True


@hookimpl(trylast=True)
async def configure_postgresql(
    configuration: pgconf.Configuration, instance: system.BaseInstance
) -> ConfigChanges:
    postgresql_conf = pgconf.parse(instance.datadir / "postgresql.conf")
    config_before = postgresql_conf.as_dict()
    conf.update(postgresql_conf, **configuration.as_dict())
    config_after = postgresql_conf.as_dict()
    changes = conf.changes(config_before, config_after)

    if changes:
        postgresql_conf.save()

    return changes


@hookimpl(trylast=True)
def configure_auth(
    instance: system.BaseInstance, manifest: interface.Instance
) -> Literal[True]:
    """Configure authentication for the PostgreSQL instance."""
    logger.info("configuring PostgreSQL authentication")
    hba_path = instance.datadir / "pg_hba.conf"
    hba = manifest.pg_hba(instance._settings)
    hba_path.write_text(hba)

    ident_path = instance.datadir / "pg_ident.conf"
    ident = manifest.pg_ident(instance._settings)
    ident_path.write_text(ident)
    return True


@hookimpl(trylast=True)
async def start_postgresql(
    instance: system.PostgreSQLInstance,
    foreground: bool,
    wait: bool,
    run_hooks: bool = True,
    **runtime_parameters: str,
) -> Literal[True]:
    logger.info("starting PostgreSQL %s", instance.qualname)
    if not foreground and run_hooks:
        settings = instance._settings
        service = hook(settings, h.postgresql_service_name, instance=instance)
        assert service is not None
        if await async_hook(
            settings,
            h.start_service,
            settings=settings,
            service=service,
            name=instance.qualname,
        ):
            if wait:
                await wait_ready(instance)
            return True

    options: list[str] = []
    for name, value in runtime_parameters.items():
        options.extend(["-c", f"{name}={value}"])
    if foreground:
        command = [str(instance.bindir / "postgres"), "-D", str(instance.datadir)]
        cmd.execute_program(command + options)
    else:
        pgctl = await pg_ctl(instance.bindir)
        command = [
            str(pgctl.pg_ctl),
            "start",
            "-D",
            str(instance.datadir),
            "-o",
            " ".join(options),
        ]
        if wait:
            command.append("--wait")
        await cmd.asyncio_run(
            command,
            capture_output=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        if wait:
            await wait_ready(instance)
    return True


@hookimpl(trylast=True)
async def stop_postgresql(
    instance: system.PostgreSQLInstance,
    mode: PostgreSQLStopMode,
    wait: bool,
    run_hooks: bool = True,
) -> Literal[True]:
    logger.info("stopping PostgreSQL %s", instance.qualname)

    if run_hooks:
        settings = instance._settings
        service = hook(settings, h.postgresql_service_name, instance=instance)
        assert service is not None
        if await async_hook(
            settings,
            h.stop_service,
            settings=settings,
            service=service,
            name=instance.qualname,
        ):
            return True

    pgctl = await pg_ctl(instance.bindir)
    await pgctl.stop(instance.datadir, mode=mode, wait=wait)
    return True


@hookimpl(trylast=True)
async def restart_postgresql(
    instance: system.PostgreSQLInstance, mode: PostgreSQLStopMode, wait: bool
) -> Literal[True]:
    logger.info("restarting PostgreSQL")
    await stop_postgresql(instance, mode=mode, wait=wait)
    await start_postgresql(instance, foreground=False, wait=wait)
    return True


@hookimpl(trylast=True)
async def reload_postgresql(instance: system.PostgreSQLInstance) -> Literal[True]:
    logger.info(f"reloading PostgreSQL configuration for {instance.qualname}")
    async with db.connect(instance) as cnx:
        await cnx.execute("SELECT pg_reload_conf()")
    return True


@hookimpl(trylast=True)
async def promote_postgresql(instance: system.PostgreSQLInstance) -> Literal[True]:
    logger.info("promoting PostgreSQL instance")
    pgctl = await pg_ctl(instance.bindir)
    await cmd.asyncio_run(
        [str(pgctl.pg_ctl), "promote", "-D", str(instance.datadir)],
        check=True,
    )
    return True


@contextlib.asynccontextmanager
async def running(instance: system.PostgreSQLInstance) -> AsyncIterator[None]:
    """Context manager to temporarily start a PostgreSQL instance."""
    if await is_running(instance):
        yield
        return

    await start_postgresql(
        instance,
        foreground=False,
        wait=True,
        run_hooks=False,
        # Keep logs to stderr, uncollected, to get meaningful errors on our side.
        logging_collector="off",
        log_destination="stderr",
    )
    try:
        yield
    finally:
        await stop_postgresql(instance, mode="fast", wait=True, run_hooks=False)


@hookimpl
def systemd_units() -> list[str]:
    return [POSTGRESQL_SERVICE_NAME]


@hookimpl
def systemd_unit_templates(
    settings: Settings, env: dict[str, Any]
) -> Iterator[tuple[str, str]]:
    yield POSTGRESQL_SERVICE_NAME, systemd.template(POSTGRESQL_SERVICE_NAME).format(
        executeas=systemd.executeas(settings),
        execpath=execpath,
        environment=systemd.environment(env),
    )


@hookimpl
def logrotate_config(settings: Settings) -> str:
    return util.template("postgresql", "logrotate.conf").format(
        logpath=settings.postgresql.logpath
    )


@hookimpl
def rsyslog_config(settings: Settings) -> str:
    user, group = settings.sysuser
    return util.template("postgresql", "rsyslog.conf").format(
        logpath=settings.postgresql.logpath, user=user, group=group
    )


@hookimpl
async def instance_status(instance: system.PostgreSQLInstance) -> tuple[Status, str]:
    return (await status(instance), "PostgreSQL")
