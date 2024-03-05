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


async def ls(cnx: db.Connection) -> list[interface.Publication]:
    async with cnx.cursor(
        row_factory=psycopg.rows.class_row(interface.Publication)
    ) as cur:
        await cur.execute(db.query("publications"))
        return await cur.fetchall()


async def apply(
    cnx: db.Connection, publication: interface.Publication, dbname: str
) -> bool:
    absent = publication.state == "absent"
    exists = publication.name in {p.name for p in await ls(cnx)}
    if not absent and not exists:
        logger.info("creating publication %s in database %s", publication.name, dbname)
        await cnx.execute(
            sql.SQL("CREATE PUBLICATION {name} FOR ALL TABLES").format(
                name=sql.Identifier(publication.name)
            )
        )
        return True
    elif absent and exists:
        logger.info(
            "dropping publication %s from database %s", publication.name, dbname
        )
        await cnx.execute(
            sql.SQL("DROP PUBLICATION IF EXISTS {name}").format(
                name=sql.Identifier(publication.name)
            )
        )
        return True
    return False
