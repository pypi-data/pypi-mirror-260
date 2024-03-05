# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import asyncio
import io
import logging
import os
import subprocess
import time
from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager
from decimal import Decimal
from pathlib import Path
from typing import IO

import psycopg
from async_lru import alru_cache
from pgtoolkit import ctl
from psycopg.conninfo import conninfo_to_dict
from psycopg.rows import args_row
from tenacity import retry
from tenacity.retry import retry_if_exception_type
from tenacity.stop import stop_after_attempt

from .. import cmd, db, exceptions
from ..models.system import BaseInstance, PostgreSQLInstance
from ..settings._postgresql import PostgreSQLVersion
from ..types import Status
from .models import WALSenderState, walsender_state

logger = logging.getLogger(__name__)


@alru_cache(maxsize=len(PostgreSQLVersion) + 1)
async def pg_ctl(bindir: Path) -> ctl.AsyncPGCtl:
    return await ctl.AsyncPGCtl.get(bindir, run_command=cmd.asyncio_run)


async def is_ready(instance: PostgreSQLInstance) -> bool:
    """Return True if the instance is ready per pg_isready."""
    logger.debug("checking if PostgreSQL instance %s is ready", instance)
    pg_isready = str(instance.bindir / "pg_isready")
    user = instance._settings.postgresql.surole.name
    dsn = db.dsn(instance, user=user)
    env = libpq_environ(instance, user)
    r = await cmd.asyncio_run([pg_isready, "-d", dsn], env=env)
    if r.returncode == 0:
        return True
    assert r.returncode in (
        1,
        2,
    ), f"Unexpected exit status from pg_isready {r.returncode}: {r.stdout}, {r.stderr}"
    return False


async def wait_ready(instance: PostgreSQLInstance, *, timeout: int = 10) -> None:
    for __ in range(timeout):
        if await is_ready(instance):
            return
        await asyncio.sleep(1)
    raise exceptions.InstanceStateError(f"{instance} not ready after {timeout}s")


async def status(instance: BaseInstance) -> Status:
    """Return the status of an instance."""
    logger.debug("get status of PostgreSQL instance %s", instance)
    # Map pg_ctl status (0, 3, 4) to our Status definition, assuming that 4
    # (data directory not specified) cannot happen at this point, otherwise
    # the 'instance' value would not exist.
    return Status(
        (await (await pg_ctl(instance.bindir)).status(instance.datadir)).value
    )


async def is_running(instance: BaseInstance) -> bool:
    """Return True if the instance is running based on its status."""
    return (await status(instance)) == Status.running


async def check_status(instance: BaseInstance, expected: Status) -> None:
    """Check actual instance status with respected to `expected` one.

    :raises ~exceptions.InstanceStateError: in case the actual status is not expected.
    """
    if (st := await status(instance)) != expected:
        raise exceptions.InstanceStateError(f"instance is {st.name}")


async def get_data_checksums(instance: PostgreSQLInstance) -> bool:
    """Return True/False if data_checksums is enabled/disabled on instance."""
    controldata = await (await pg_ctl(instance.bindir)).controldata(instance.datadir)
    return controldata["Data page checksum version"] != "0"


async def set_data_checksums(instance: PostgreSQLInstance, enabled: bool) -> None:
    """Enable/disable data checksums on instance.

    The instance MUST NOT be running.
    """
    action = "enable" if enabled else "disable"
    await cmd.asyncio_run(
        [
            str(instance.bindir / "pg_checksums"),
            f"--{action}",
            "--pgdata",
            str(instance.datadir),
        ],
        check=True,
    )


def logfile(
    instance: PostgreSQLInstance,
    *,
    timeout: float | None = None,
    poll_interval: float = 0.1,
) -> Iterator[Path]:
    """Yield the current log file by polling current_logfiles for changes.

    :raises ~exceptions.FileNotFoundError: if the current log file, matching
        first configured log_destination, is not found.
    :raises ~exceptions.SystemError: if the current log file cannot be opened
        for reading.
    :raises ValueError: if no record matching configured log_destination is
        found in current_logfiles (this indicates a misconfigured instance).
    :raises TimeoutError: if no new log file was polled from current_logfiles
        within specified 'timeout'.
    """
    config = instance.config()
    log_destination = config.get("log_destination", "stderr")
    assert isinstance(log_destination, str), log_destination
    log_destination = log_destination.split(",")[0]
    current_logfiles = instance.datadir / "current_logfiles"
    if not current_logfiles.exists():
        raise exceptions.FileNotFoundError(
            f"file 'current_logfiles' for instance {instance} not found"
        )

    @retry(
        retry=retry_if_exception_type(FileNotFoundError),
        stop=stop_after_attempt(2),
        reraise=True,
    )
    def logf() -> Path:
        """Get the current log file, matching configured log_destination.

        Retry in case the 'current_logfiles' file is unavailable for reading,
        which might happen as postgres typically re-creates it upon update.
        """
        with current_logfiles.open() as f:
            for line in f:
                destination, location = line.strip().split(None, maxsplit=1)
                if destination == log_destination:
                    break
            else:
                raise ValueError(
                    f"no record matching {log_destination!r} log destination found for instance {instance}"
                )
        fpath = Path(location)
        if not fpath.is_absolute():
            fpath = instance.datadir / fpath
        return fpath

    current_logfile = None
    start_time = time.monotonic()
    while True:
        f = logf()
        if f == current_logfile:
            if timeout is not None:
                if time.monotonic() - start_time >= timeout:
                    raise TimeoutError("timed out waiting for a new log file")
            time.sleep(poll_interval)
            continue
        current_logfile = f
        start_time = time.monotonic()
        yield current_logfile


def logs(
    instance: PostgreSQLInstance,
    *,
    timeout: float | None = None,
    poll_interval: float = 0.1,
) -> Iterator[str]:
    """Return the content of current log file as an iterator."""
    for fpath in logfile(instance, timeout=timeout, poll_interval=poll_interval):
        logger.info("reading logs of instance %s from %s", instance, fpath)
        try:
            with fpath.open() as f:
                yield from f
        except OSError as e:
            raise exceptions.SystemError(
                f"failed to read {fpath} on instance {instance}"
            ) from e


@asynccontextmanager
async def log(instance: PostgreSQLInstance) -> AsyncIterator[None]:
    """Context manager forwarding PostgreSQL log messages (emitted during the
    context) to our logger.

    If no PostgreSQL log file is found, do nothing.
    """
    try:
        logpath = next(logfile(instance, timeout=0))
    except exceptions.FileNotFoundError:
        yield None
        return

    # Log PostgreSQL messages, read from current log file, using a
    # thread to avoid blocking.
    def logpg(f: IO[str], execpath: Path) -> None:
        """Log lines read from 'f', until it gets closed."""
        while True:
            try:
                line = f.readline()
            except ValueError:  # I/O operation on closed file
                break
            if line:
                logger.debug("%s: %s", execpath, line.rstrip())

    logf = logpath.open()
    logf.seek(0, io.SEEK_END)
    # TODO: use asyncio.TaskGroup from Python 3.11
    task = asyncio.create_task(
        asyncio.to_thread(logpg, logf, instance.bindir / "postgres")
    )
    try:
        yield None
    finally:
        logf.close()  # Would terminate the threaded task.
        await task


async def replication_lag(instance: PostgreSQLInstance) -> Decimal | None:
    """Return the replication lag of a standby instance.

    The instance must be running; if the primary is not running, None is
    returned.

    :raises TypeError: if the instance is not a standby.
    """
    standby = instance.standby
    if standby is None:
        raise TypeError(f"{instance} is not a standby")

    try:
        async with await db.primary_connect(standby) as cnx:
            row = await (
                await cnx.execute("SELECT pg_current_wal_lsn() AS lsn")
            ).fetchone()
    except psycopg.OperationalError as e:
        logger.warning("failed to connect to primary: %s", e)
        return None
    assert row is not None
    primary_lsn = row["lsn"]

    password = standby.password.get_secret_value() if standby.password else None
    dsn = db.dsn(
        instance,
        dbname="template1",
        user=instance._settings.postgresql.replrole,
        password=password,
    )
    async with await db.connect_dsn(dsn) as cnx:
        row = await (
            await cnx.execute(
                "SELECT %s::pg_lsn - pg_last_wal_replay_lsn() AS lag", (primary_lsn,)
            )
        ).fetchone()
    assert row is not None
    lag = row["lag"]
    assert isinstance(lag, Decimal)
    return lag


async def wal_sender_state(instance: PostgreSQLInstance) -> WALSenderState | None:
    """Return the state of the WAL sender process (on the primary) connected
    to standby 'instance'.

    This queries pg_stat_replication view on the primary, filtered by
    application_name assuming that the standby instance name is used there.
    Prior to PostgreSQL version 12, application_name is always 'walreceiver',
    so this does not work. Otherwise, we retrieve application_name if set in
    primary_conninfo, use cluster_name otherwise or fall back to instance
    name.
    """
    assert instance.standby is not None, f"{instance} is not a standby"
    primary_conninfo = conninfo_to_dict(instance.standby.primary_conninfo)
    try:
        application_name = primary_conninfo["application_name"]
    except KeyError:
        application_name = instance.config().get("cluster_name", instance.name)

    try:
        async with (
            await db.primary_connect(instance.standby) as cnx,
            cnx.cursor(row_factory=args_row(walsender_state)) as cur,
        ):
            return await (
                await cur.execute(
                    "SELECT state FROM pg_stat_replication WHERE application_name = %s",
                    (application_name,),
                )
            ).fetchone()
    except psycopg.OperationalError as e:
        logger.warning("failed to connect to primary: %s", e)
        return None


def libpq_environ(
    instance: BaseInstance, role: str, *, base: dict[str, str] | None = None
) -> dict[str, str]:
    """Return a dict with libpq environment variables for authentication."""
    auth = instance._settings.postgresql.auth
    if base is None:
        env = os.environ.copy()
    else:
        env = base.copy()
    if auth.passfile is not None:
        env.setdefault("PGPASSFILE", str(auth.passfile))
    if auth.password_command and "PGPASSWORD" not in env:
        try:
            cmd_args = [
                c.format(instance=instance, role=role) for c in auth.password_command
            ]
        except ValueError as e:
            raise exceptions.SettingsError(
                f"failed to format auth.password_command: {e}"
            ) from None
        logger.debug("getting password for '%s' role from password_command", role)
        password = subprocess.run(  # nosec
            cmd_args, check=True, capture_output=True, text=True
        ).stdout.strip()
        if password:
            env["PGPASSWORD"] = password
    return env
