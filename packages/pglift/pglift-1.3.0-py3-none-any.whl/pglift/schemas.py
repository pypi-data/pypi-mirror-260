# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging

import psycopg.rows
from psycopg import sql

from . import db
from .models import interface

logger = logging.getLogger(__name__)


async def ls(cnx: db.Connection) -> list[interface.Schema]:
    """Return list of schemas of database."""
    async with cnx.cursor(row_factory=psycopg.rows.class_row(interface.Schema)) as cur:
        await cur.execute(db.query("list_schemas"))
        return await cur.fetchall()


async def current_role(cnx: db.Connection) -> str:
    async with cnx.cursor(row_factory=psycopg.rows.args_row(str)) as cur:
        r = await (await cur.execute("SELECT CURRENT_ROLE")).fetchone()
        assert r is not None
        return r


async def alter_owner(cnx: db.Connection, name: str, owner: str) -> None:
    opts = sql.SQL("OWNER TO {}").format(sql.Identifier(owner))
    logger.info("setting '%s' schema owner to '%s'", name, owner)
    await cnx.execute(
        db.query("alter_schema", schema=psycopg.sql.Identifier(name), opts=opts)
    )


async def apply(cnx: db.Connection, schema: interface.Schema, dbname: str) -> bool:
    """Apply the state defined by 'schema' in connected database and return
    True if something changed.
    """
    for existing in await ls(cnx):
        if schema.name == existing.name:
            if schema.state == "absent":
                logger.info("dropping schema %s from database %s", schema.name, dbname)
                await cnx.execute(
                    db.query("drop_schema", schema=psycopg.sql.Identifier(schema.name))
                )
                return True

            new_owner = schema.owner or await current_role(cnx)
            if new_owner != existing.owner:
                await alter_owner(cnx, schema.name, new_owner)
                return True
            return False

    if schema.state != "absent":
        await create(cnx, schema, dbname)
        return True
    return False


async def create(cnx: db.Connection, schema: interface.Schema, dbname: str) -> None:
    msg, args = "creating schema '%(name)s' in database %(dbname)s", {
        "name": schema.name,
        "dbname": dbname,
    }
    opts = []
    if schema.owner is not None:
        opts.append(sql.SQL("AUTHORIZATION {}").format(sql.Identifier(schema.owner)))
        msg += " with owner '%(owner)s'"
        args["owner"] = schema.owner

    logger.info(msg, args)
    await cnx.execute(
        db.query(
            "create_schema",
            schema=psycopg.sql.Identifier(schema.name),
            options=sql.SQL(" ").join(opts),
        )
    )
