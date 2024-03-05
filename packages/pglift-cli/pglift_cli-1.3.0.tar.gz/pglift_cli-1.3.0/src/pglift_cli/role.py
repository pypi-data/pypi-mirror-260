# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from collections.abc import Sequence
from functools import partial
from typing import IO, Any

import click
from pydantic.v1.utils import deep_update

from pglift import postgresql, privileges, roles
from pglift.models import interface, system

from . import _site, model
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


def print_role_schema(
    context: click.Context, param: click.Parameter, value: bool
) -> None:
    return print_schema(context, param, value, model=_site.ROLE_MODEL)


def print_role_argspec(
    context: click.Context, param: click.Parameter, value: bool
) -> None:
    print_argspec(context, param, value, model=_site.ROLE_MODEL)


@click.group("role", cls=Group)
@instance_identifier_option
@click.option(
    "--schema",
    is_flag=True,
    callback=print_role_schema,
    expose_value=False,
    is_eager=True,
    help="Print the JSON schema of role model and exit.",
)
@click.option(
    "--ansible-argspec",
    is_flag=True,
    callback=print_role_argspec,
    expose_value=False,
    is_eager=True,
    hidden=True,
    help="Print the Ansible argspec of role model and exit.",
)
def cli(**kwargs: Any) -> None:
    """Manage roles."""


@cli.command("create")
@model.as_parameters(_site.ROLE_MODEL, "create")
@pass_instance
@click.pass_obj
@async_command
async def create(obj: Obj, instance: system.Instance, role: interface.Role) -> None:
    """Create a role in a PostgreSQL instance"""
    with obj.lock:
        async with postgresql.running(instance):
            if await roles.exists(instance, role.name):
                raise click.ClickException("role already exists")
            await roles.apply(instance, role)


@cli.command("alter")  # type: ignore[arg-type]
@model.as_parameters(_site.ROLE_MODEL, "update", parse_model=False)
@click.argument("rolname")
@pass_instance
@click.pass_obj
@async_command
async def alter(
    obj: Obj, instance: system.Instance, rolname: str, **changes: Any
) -> None:
    """Alter a role in a PostgreSQL instance"""
    with obj.lock:
        async with postgresql.running(instance):
            values = (await roles.get(instance, rolname)).model_dump(by_alias=True)
            values = deep_update(values, changes)
            altered = _site.ROLE_MODEL.model_validate(values)
            await roles.apply(instance, altered)


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
    """Apply manifest as a role"""
    role = _site.ROLE_MODEL.parse_yaml(file)
    if dry_run:
        ret = interface.ApplyResult(change_state=None)
    else:
        with obj.lock:
            async with postgresql.running(instance):
                ret = await roles.apply(instance, role)
    if output_format == OutputFormat.json:
        print_json_for(ret)


@cli.command("list")
@output_format_option
@pass_instance
@async_command
async def ls(instance: system.Instance, output_format: OutputFormat) -> None:
    """List roles in instance"""
    async with postgresql.running(instance):
        rls = await roles.ls(instance)
    if output_format == OutputFormat.json:
        print_json_for([model_dump(r) for r in rls])
    else:
        print_table_for(rls, partial(model_dump, exclude={"pgpass"}))


@cli.command("get")
@output_format_option
@click.argument("name")
@pass_instance
@async_command
async def get(
    instance: system.Instance, name: str, output_format: OutputFormat
) -> None:
    """Get the description of a role"""
    async with postgresql.running(instance):
        r = await roles.get(instance, name)
    if output_format == OutputFormat.json:
        print_json_for(model_dump(r))
    else:
        print_table_for([r], model_dump, box=None)


@cli.command("drop")
@model.as_parameters(interface.RoleDropped, "create")
@pass_instance
@async_command
async def drop(instance: system.Instance, roledropped: interface.RoleDropped) -> None:
    """Drop a role"""
    async with postgresql.running(instance):
        await roles.drop(instance, roledropped)


@cli.command("privileges")
@click.argument("name")
@click.option(
    "-d", "--database", "databases", multiple=True, help="Database to inspect"
)
@click.option("--default", "defaults", is_flag=True, help="Display default privileges")
@output_format_option
@pass_instance
@async_command
async def list_privileges(
    instance: system.Instance,
    name: str,
    databases: Sequence[str],
    defaults: bool,
    output_format: OutputFormat,
) -> None:
    """List privileges of a role."""
    async with postgresql.running(instance):
        await roles.get(instance, name)  # check existence
        try:
            prvlgs = await privileges.get(
                instance, databases=databases, roles=(name,), defaults=defaults
            )
        except ValueError as e:
            raise click.ClickException(str(e)) from None
    if output_format == OutputFormat.json:
        print_json_for([model_dump(p) for p in prvlgs])
    else:
        print_table_for(prvlgs, model_dump)
