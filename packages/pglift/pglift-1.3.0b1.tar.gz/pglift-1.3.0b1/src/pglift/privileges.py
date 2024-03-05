# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from collections.abc import Sequence

import psycopg.rows
from psycopg import sql

from . import db
from .models import interface, system


async def inspect_privileges(
    instance: system.PostgreSQLInstance,
    database: str,
    roles: Sequence[str] = (),
    defaults: bool = False,
) -> list[interface.DefaultPrivilege] | list[interface.Privilege]:
    args = {}
    where_clause = sql.SQL("")
    if roles:
        where_clause = sql.SQL("AND pg_roles.rolname = ANY(%(roles)s)")
        args["roles"] = list(roles)
    rtype: type[interface.DefaultPrivilege]
    if defaults:
        rtype = interface.DefaultPrivilege
        query = "database_default_acl"
    else:
        rtype = interface.Privilege
        query = "database_privileges"
    async with db.connect(instance, dbname=database) as cnx:
        async with cnx.cursor(row_factory=psycopg.rows.class_row(rtype)) as cur:
            await cur.execute(db.query(query, where_clause=where_clause), args)
            return await cur.fetchall()


async def get(
    instance: system.PostgreSQLInstance,
    *,
    databases: Sequence[str] = (),
    roles: Sequence[str] = (),
    defaults: bool = False,
) -> list[interface.DefaultPrivilege] | list[interface.Privilege]:
    """List access privileges for databases of an instance.

    :param databases: list of databases to inspect (all will be inspected if
        unspecified).
    :param roles: list of roles to restrict inspection on.
    :param defaults: if ``True``, get default privileges.

    :raises ValueError: if an element of `databases` or `roles` does not
        exist.
    """

    async with db.connect(instance) as cnx:
        cur = await cnx.execute(db.query("database_list", where_clause=sql.SQL("")))
        existing_databases = [db["name"] for db in await cur.fetchall()]
    if not databases:
        databases = existing_databases
    else:
        if unknown_dbs := set(databases) - set(existing_databases):
            raise ValueError(f"database(s) not found: {', '.join(unknown_dbs)}")

    if roles:
        async with db.connect(instance) as cnx:
            cur = await cnx.execute(db.query("role_list_names"))
            existing_roles = [n["rolname"] async for n in cur]
        if unknown_roles := set(roles) - set(existing_roles):
            raise ValueError(f"role(s) not found: {', '.join(unknown_roles)}")

    return [
        prvlg
        for database in databases
        for prvlg in await inspect_privileges(
            instance, database, roles=roles, defaults=defaults
        )
    ]
