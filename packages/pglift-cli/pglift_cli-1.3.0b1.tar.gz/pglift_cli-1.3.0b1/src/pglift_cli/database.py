# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import functools
from collections.abc import Sequence
from pathlib import Path
from typing import IO, Any

import click
import psycopg
from pydantic.v1.utils import deep_update

from pglift import databases, postgresql, privileges, task
from pglift.models import interface, system

from . import model
from .util import (
    Group,
    Obj,
    OutputFormat,
    async_command,
    dry_run_option,
    instance_identifier_option,
    model_dump,
    output_format_option,
    pass_instance,
    print_argspec,
    print_json_for,
    print_schema,
    print_table_for,
)


@click.group("database", cls=Group)
@instance_identifier_option
@click.option(
    "--schema",
    is_flag=True,
    callback=functools.partial(print_schema, model=interface.Database),
    expose_value=False,
    is_eager=True,
    help="Print the JSON schema of database model and exit.",
)
@click.option(
    "--ansible-argspec",
    is_flag=True,
    callback=functools.partial(print_argspec, model=interface.Database),
    expose_value=False,
    is_eager=True,
    hidden=True,
    help="Print the Ansible argspec of database model and exit.",
)
def cli(**kwargs: Any) -> None:
    """Manage databases."""


@cli.command("create")
@model.as_parameters(interface.Database, "create")
@pass_instance
@click.pass_obj
@async_command
async def create(
    obj: Obj, instance: system.Instance, database: interface.Database
) -> None:
    """Create a database in a PostgreSQL instance"""
    with obj.lock:
        async with postgresql.running(instance):
            if await databases.exists(instance, database.name):
                raise click.ClickException("database already exists")
            async with task.async_transaction():
                await databases.apply(instance, database)


@cli.command("alter")  # type: ignore[arg-type]
@model.as_parameters(interface.Database, "update", parse_model=False)
@click.argument("dbname")
@pass_instance
@click.pass_obj
@async_command
async def alter(
    obj: Obj, instance: system.Instance, dbname: str, **changes: Any
) -> None:
    """Alter a database in a PostgreSQL instance"""
    with obj.lock:
        async with postgresql.running(instance):
            values = (await databases.get(instance, dbname)).model_dump(by_alias=True)
            values = deep_update(values, changes)
            altered = interface.Database.model_validate(values)
            await databases.apply(instance, altered)


@cli.command("apply", hidden=True)
@click.option("-f", "--file", type=click.File("r"), metavar="MANIFEST", required=True)
@output_format_option
@dry_run_option
@pass_instance
@click.pass_obj
@async_command
async def apply(
    obj: Obj,
    instance: system.Instance,
    file: IO[str],
    output_format: OutputFormat,
    dry_run: bool,
) -> None:
    """Apply manifest as a database"""
    database = interface.Database.parse_yaml(file)
    if dry_run:
        ret = interface.ApplyResult(change_state=None)
    else:
        with obj.lock:
            async with postgresql.running(instance):
                ret = await databases.apply(instance, database)
    if output_format == OutputFormat.json:
        print_json_for(ret)


@cli.command("get")
@output_format_option
@click.argument("name")
@pass_instance
@async_command
async def get(
    instance: system.Instance, name: str, output_format: OutputFormat
) -> None:
    """Get the description of a database"""
    async with postgresql.running(instance):
        db = await databases.get(instance, name)
    if output_format == OutputFormat.json:
        print_json_for(model_dump(db))
    else:
        print_table_for(
            [db],
            functools.partial(model_dump, exclude={"extensions", "schemas"}),
            box=None,
        )


@cli.command("list")
@output_format_option
@click.argument("dbname", nargs=-1)
@pass_instance
@async_command
async def ls(
    instance: system.Instance, dbname: Sequence[str], output_format: OutputFormat
) -> None:
    """List databases (all or specified ones)

    Only queried databases are shown when DBNAME is specified.
    """

    async with postgresql.running(instance):
        dbs = await databases.ls(instance, dbnames=dbname)
    if output_format == OutputFormat.json:
        print_json_for([model_dump(db) for db in dbs])
    else:
        print_table_for(dbs, model_dump)


@cli.command("drop")
@model.as_parameters(interface.DatabaseDropped, "create")
@pass_instance
@click.pass_obj
@async_command
async def drop(
    obj: Obj, instance: system.Instance, databasedropped: interface.DatabaseDropped
) -> None:
    """Drop a database"""
    with obj.lock:
        async with postgresql.running(instance):
            await databases.drop(instance, databasedropped)


@cli.command("privileges")
@click.argument("name")
@click.option("-r", "--role", "roles", multiple=True, help="Role to inspect")
@click.option("--default", "defaults", is_flag=True, help="Display default privileges")
@output_format_option
@pass_instance
@async_command
async def list_privileges(
    instance: system.Instance,
    name: str,
    roles: Sequence[str],
    defaults: bool,
    output_format: OutputFormat,
) -> None:
    """List privileges on a database."""
    async with postgresql.running(instance):
        await databases.get(instance, name)  # check existence
        try:
            prvlgs = await privileges.get(
                instance, databases=(name,), roles=roles, defaults=defaults
            )
        except ValueError as e:
            raise click.ClickException(str(e)) from None
    if output_format == OutputFormat.json:
        print_json_for([model_dump(p) for p in prvlgs])
    else:
        print_table_for(prvlgs, model_dump)


@cli.command("run")
@click.argument("sql_command")
@click.option(
    "-d", "--database", "dbnames", multiple=True, help="Database to run command on"
)
@click.option(
    "-x",
    "--exclude-database",
    "exclude_dbnames",
    multiple=True,
    help="Database to not run command on",
)
@output_format_option
@pass_instance
@async_command
async def run(
    instance: system.Instance,
    sql_command: str,
    dbnames: Sequence[str],
    exclude_dbnames: Sequence[str],
    output_format: OutputFormat,
) -> None:
    """Run given command on databases of a PostgreSQL instance"""
    async with postgresql.running(instance):
        try:
            result = await databases.run(
                instance,
                sql_command,
                dbnames=dbnames,
                exclude_dbnames=exclude_dbnames,
            )
        except psycopg.ProgrammingError as e:
            raise click.ClickException(str(e)) from None
    if output_format == OutputFormat.json:
        print_json_for(result)
    else:
        for dbname, rows in result.items():
            print_table_for(rows, lambda m: m, title=f"Database {dbname}")


@cli.command("dump")
@click.option(
    "-o",
    "--output",
    metavar="DIRECTORY",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Write dump file(s) to DIRECTORY instead of configured 'dumps_directory'.",
)
@click.argument("dbname")
@pass_instance
@async_command
async def dump(instance: system.Instance, dbname: str, output: Path | None) -> None:
    """Dump a database"""
    async with postgresql.running(instance):
        await databases.dump(instance, dbname, output)
