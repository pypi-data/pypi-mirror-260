# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import asyncio
import datetime
import logging
import shlex
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import psycopg.rows
import pydantic_core
from pgtoolkit import conf as pgconf
from psycopg import sql

from . import (
    cmd,
    db,
    exceptions,
    extensions,
    hookimpl,
    publications,
    schemas,
    subscriptions,
    types,
    ui,
    util,
)
from .models import interface, system
from .postgresql.ctl import libpq_environ
from .task import task

logger = logging.getLogger(__name__)


async def apply(
    instance: system.PostgreSQLInstance, database: interface.Database
) -> interface.ApplyResult:
    """Apply state described by specified interface model as a PostgreSQL database.

    The instance should be running and not a standby.
    """
    if instance.standby:
        raise exceptions.InstanceReadOnlyError(instance)

    async with db.connect(instance) as cnx:
        return await _apply(cnx, database, instance)


async def _apply(
    cnx: db.Connection,
    database: interface.Database,
    instance: system.PostgreSQLInstance,
) -> interface.ApplyResult:
    name = database.name
    if database.state == "absent":
        dropped = False
        if await _exists(cnx, name):
            await _drop(cnx, database)
            dropped = True
        return interface.ApplyResult(change_state="dropped" if dropped else None)

    changed = created = False
    if not await _exists(cnx, name):
        await create(cnx, database, instance)
        created = True
    else:
        logger.info("altering '%s' database on instance %s", database.name, instance)
        changed = await alter(cnx, database)

    if (
        database.schemas
        or database.extensions
        or database.publications
        or database.subscriptions
    ):
        async with db.connect(instance, dbname=name) as db_cnx:
            for schema in database.schemas:
                if await schemas.apply(db_cnx, schema, name):
                    changed = True
            for extension in database.extensions:
                if await extensions.apply(db_cnx, extension, name):
                    changed = True
            for publication in database.publications:
                if await publications.apply(db_cnx, publication, name):
                    changed = True
            for subscription in database.subscriptions:
                if await subscriptions.apply(db_cnx, subscription, name):
                    changed = True

    if created:
        state = "created"
    elif changed:
        state = "changed"
    else:
        state = None
    return interface.ApplyResult(change_state=state)


async def clone(
    name: str,
    options: interface.CloneOptions,
    instance: system.PostgreSQLInstance,
) -> None:
    logger.info("cloning '%s' database in %s from %s", name, instance, options.dsn)

    def log_cmd(program: Path, cmd_args: list[str]) -> None:
        args = [str(program)] + [
            (
                db.obfuscate_conninfo(a)
                if isinstance(a, (types.ConnectionString, pydantic_core.MultiHostUrl))
                else a
            )
            for a in cmd_args
        ]
        logger.debug(shlex.join(args))

    pg_dump = instance.bindir / "pg_dump"
    dump_args = ["--format", "custom", "-d", str(options.dsn)]
    user = instance._settings.postgresql.surole.name
    pg_restore = instance.bindir / "pg_restore"
    restore_args = [
        "--exit-on-error",
        "-d",
        db.dsn(instance, dbname=name, user=user),
    ]
    if options.schema_only:
        dump_args.append("--schema-only")
        restore_args.append("--schema-only")
    env = libpq_environ(instance, user)

    log_cmd(pg_dump, dump_args)
    dump = await asyncio.create_subprocess_exec(
        pg_dump, *dump_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    log_cmd(pg_restore, restore_args)
    restore = await asyncio.create_subprocess_exec(
        pg_restore,
        *restore_args,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        env=env,
    )

    async def pipe(from_: asyncio.StreamReader, to: asyncio.StreamWriter) -> None:
        async for data in from_:
            to.write(data)
            await to.drain()
        to.close()
        await to.wait_closed()

    # TODO: use asyncio.TaskGroup from Python 3.11
    assert dump.stderr is not None
    dump_stderr = asyncio.create_task(cmd.log_stream(pg_dump, dump.stderr))
    assert restore.stderr is not None
    restore_stderr = asyncio.create_task(cmd.log_stream(pg_restore, restore.stderr))
    assert dump.stdout is not None and restore.stdin is not None
    dump2restore = asyncio.create_task(pipe(dump.stdout, restore.stdin))
    restore_rc, dump_rc = await asyncio.gather(restore.wait(), dump.wait())
    await asyncio.gather(dump2restore, dump_stderr, restore_stderr)

    if dump_rc:
        raise exceptions.CommandError(dump_rc, [str(pg_dump)] + dump_args)
    if restore_rc:
        raise exceptions.CommandError(restore_rc, [str(pg_restore)] + restore_args)


async def get(instance: system.PostgreSQLInstance, name: str) -> interface.Database:
    """Return the database object with specified name.

    :raises ~pglift.exceptions.DatabaseNotFound: if no database with specified
        'name' exists.
    """
    if not await exists(instance, name):
        raise exceptions.DatabaseNotFound(name)
    async with db.connect(instance, dbname=name) as cnx:
        return await _get(cnx, dbname=name)


async def _get(cnx: db.Connection, dbname: str) -> interface.Database:
    row = await (
        await cnx.execute(db.query("database_inspect"), {"database": dbname})
    ).fetchone()
    assert row is not None
    settings = row.pop("settings")
    if settings is None:
        row["settings"] = None
    else:
        row["settings"] = {}
        for s in settings:
            k, v = s.split("=", 1)
            row["settings"][k.strip()] = pgconf.parse_value(v.strip())
    row["schemas"] = await schemas.ls(cnx)
    row["extensions"] = await extensions.ls(cnx)
    row["publications"] = await publications.ls(cnx)
    row["subscriptions"] = await subscriptions.ls(cnx, dbname)
    return interface.Database.model_validate(row)


async def ls(
    instance: system.PostgreSQLInstance, dbnames: Sequence[str] = ()
) -> list[interface.DatabaseListItem]:
    """List databases in instance.

    :param dbnames: restrict operation on databases with a name in this list.
    """
    async with db.connect(instance) as cnx:
        return await _list(cnx, dbnames)


async def _list(
    cnx: db.Connection, dbnames: Sequence[str] = ()
) -> list[interface.DatabaseListItem]:
    where_clause = (
        sql.SQL("AND d.datname IN ({})").format(
            sql.SQL(", ").join(map(sql.Literal, dbnames))
        )
        if dbnames
        else sql.SQL("")
    )
    async with cnx.cursor(
        row_factory=psycopg.rows.kwargs_row(interface.DatabaseListItem.build)
    ) as cur:
        await cur.execute(db.query("database_list", where_clause=where_clause))
        return await cur.fetchall()


async def drop(
    instance: system.PostgreSQLInstance, database: interface.DatabaseDropped
) -> None:
    """Drop a database from a primary instance.

    :raises ~pglift.exceptions.DatabaseNotFound: if no database with specified
        'name' exists.
    """
    if instance.standby:
        raise exceptions.InstanceReadOnlyError(instance)
    async with db.connect(instance) as cnx:
        if not await _exists(cnx, database.name):
            raise exceptions.DatabaseNotFound(database.name)
        await _drop(cnx, database)


async def _drop(cnx: db.Connection, database: interface.DatabaseDropped) -> None:
    logger.info("dropping '%s' database", database.name)
    options = ""
    if database.force_drop:
        if cnx.info.server_version < 130000:
            raise exceptions.UnsupportedError(
                "Force drop option can't be used with PostgreSQL < 13"
            )
        options = "WITH (FORCE)"

    await cnx.execute(
        db.query(
            "database_drop",
            database=sql.Identifier(database.name),
            options=sql.SQL(options),
        )
    )


async def exists(instance: system.PostgreSQLInstance, name: str) -> bool:
    """Return True if named database exists in 'instance'.

    The instance should be running.
    """
    async with db.connect(instance) as cnx:
        return await _exists(cnx, name)


async def _exists(cnx: db.Connection, name: str) -> bool:
    cur = await cnx.execute(db.query("database_exists"), {"database": name})
    return cur.rowcount == 1


@task(title="creating '{database.name}' database in {instance}")
async def create(
    cnx: db.Connection,
    database: interface.Database,
    instance: system.PostgreSQLInstance,
) -> None:
    opts = []
    if database.owner is not None:
        opts.append(sql.SQL("OWNER {}").format(sql.Identifier(database.owner)))
    if database.tablespace is not None:
        opts.append(
            sql.SQL("TABLESPACE {}").format(sql.Identifier(database.tablespace))
        )

    await cnx.execute(
        db.query(
            "database_create",
            database=sql.Identifier(database.name),
            options=sql.SQL(" ").join(opts),
        ),
    )
    if database.settings is not None:
        await _configure(cnx, database.name, database.settings)

    if database.clone:
        await clone(database.name, database.clone, instance)


@create.revert
async def revert_create(
    cnx: db.Connection,
    database: interface.Database,
    instance: system.PostgreSQLInstance,
) -> None:
    await _drop(cnx, interface.DatabaseDropped(name=database.name))


async def alter(cnx: db.Connection, database: interface.Database) -> bool:
    owner: sql.Composable
    actual = await _get(cnx, database.name)
    if database.owner is None:
        owner = sql.SQL("CURRENT_USER")
    else:
        owner = sql.Identifier(database.owner)
    options = sql.SQL("OWNER TO {}").format(owner)
    await cnx.execute(
        db.query(
            "database_alter",
            database=sql.Identifier(database.name),
            options=options,
        ),
    )

    if database.settings is not None:
        await _configure(cnx, database.name, database.settings)

    if actual.tablespace != database.tablespace and database.tablespace is not None:
        options = sql.SQL("SET TABLESPACE {}").format(
            sql.Identifier(database.tablespace)
        )
        await cnx.execute(
            db.query(
                "database_alter",
                database=sql.Identifier(database.name),
                options=options,
            ),
        )

    return (await _get(cnx, database.name)) != actual


async def _configure(
    cnx: db.Connection, dbname: str, db_settings: Mapping[str, pgconf.Value | None]
) -> None:
    if not db_settings:
        # Empty input means reset all.
        await cnx.execute(
            db.query(
                "database_alter",
                database=sql.Identifier(dbname),
                options=sql.SQL("RESET ALL"),
            )
        )
    else:
        async with cnx.transaction():
            for k, v in db_settings.items():
                if v is None:
                    options = sql.SQL("RESET {}").format(sql.Identifier(k))
                else:
                    options = sql.SQL("SET {} TO {}").format(
                        sql.Identifier(k), sql.Literal(v)
                    )
                await cnx.execute(
                    db.query(
                        "database_alter",
                        database=sql.Identifier(dbname),
                        options=options,
                    )
                )


async def encoding(cnx: db.Connection) -> str:
    """Return the encoding of connected database."""
    row = await (await cnx.execute(db.query("database_encoding"))).fetchone()
    assert row is not None
    value = row["encoding"]
    return str(value)


async def run(
    instance: system.PostgreSQLInstance,
    sql_command: str,
    *,
    dbnames: Sequence[str] = (),
    exclude_dbnames: Sequence[str] = (),
    notice_handler: types.NoticeHandler = db.default_notice_handler,
) -> dict[str, list[dict[str, Any]]]:
    """Execute a SQL command on databases of `instance`.

    :param dbnames: restrict operation on databases with a name in this list.
    :param exclude_dbnames: exclude databases with a name in this list from
        the operation.
    :param notice_handler: a function to handle notice.

    :returns: a dict mapping database names to query results, if any.

    :raises psycopg.ProgrammingError: in case of unprocessable query.
    """
    result = {}
    if dbnames:
        target = ", ".join(dbnames)
    else:
        target = "ALL databases"
        if exclude_dbnames:
            target += f" except {', '.join(exclude_dbnames)}"
    if not ui.confirm(
        f"Confirm execution of {sql_command!r} on {target} of {instance}?", True
    ):
        raise exceptions.Cancelled(f"execution of {sql_command!r} cancelled")

    for database in await ls(instance):
        if (
            dbnames and database.name not in dbnames
        ) or database.name in exclude_dbnames:
            continue
        async with db.connect(instance, dbname=database.name) as cnx:
            cnx.add_notice_handler(notice_handler)
            logger.info(
                'running "%s" on %s database of %s',
                sql_command,
                database.name,
                instance,
            )
            cur = await cnx.execute(sql_command)
            if cur.statusmessage:
                logger.info(cur.statusmessage)
            if cur.description is not None:
                result[database.name] = await cur.fetchall()
    return result


async def dump(
    instance: system.PostgreSQLInstance,
    dbname: str,
    output_directory: Path | None = None,
) -> None:
    """Dump a database of `instance` (logical backup).

    :param dbname: Database name.
    :param dumps_directory: An *existing* directory to write dump file(s) to;
        if unspecified `postgresql.dumps_directory` setting value will be
        used.

    :raises psycopg.OperationalError: if the database with 'dbname' does not exist.
    """
    logger.info("backing up database '%s' on instance %s", dbname, instance)
    postgresql_settings = instance._settings.postgresql
    async with db.connect(
        instance, dbname=dbname, user=postgresql_settings.surole.name
    ) as cnx:
        password = cnx.info.password
    conninfo = db.dsn(instance, dbname=dbname, user=postgresql_settings.surole.name)

    date = (
        datetime.datetime.now(datetime.timezone.utc)
        .astimezone()
        .isoformat(timespec="seconds")
    )
    dumps_directory = output_directory or instance.dumps_directory
    cmds = [
        [
            c.format(
                bindir=instance.bindir,
                path=dumps_directory,
                conninfo=conninfo,
                dbname=dbname,
                date=date,
            )
            for c in args
        ]
        for args in postgresql_settings.dump_commands
    ]
    env = libpq_environ(instance, postgresql_settings.surole.name)
    if "PGPASSWORD" not in env and password:
        env["PGPASSWORD"] = password
    for args in cmds:
        await cmd.asyncio_run(args, check=True, env=env)


@hookimpl
async def instance_configured(
    instance: system.PostgreSQLInstance, creating: bool
) -> None:
    if creating:
        instance.dumps_directory.mkdir(parents=True, exist_ok=True)


@hookimpl
async def instance_dropped(instance: system.Instance) -> None:
    dumps_directory = instance.dumps_directory
    if not dumps_directory.exists():
        return
    has_dumps = next(dumps_directory.iterdir(), None) is not None
    if not has_dumps or ui.confirm(
        f"Confirm deletion of database dump(s) for instance {instance}?",
        True,
    ):
        util.rmtree(dumps_directory)
