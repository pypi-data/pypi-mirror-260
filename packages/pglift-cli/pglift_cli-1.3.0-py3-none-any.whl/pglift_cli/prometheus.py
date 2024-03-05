# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from functools import partial
from typing import IO

import click

from pglift import exceptions, prometheus, task
from pglift.models import interface
from pglift.prometheus import impl, models
from pglift.prometheus import register_if as register_if  # noqa: F401

from . import _site, hookimpl, model
from .util import (
    Group,
    Obj,
    OutputFormat,
    async_command,
    dry_run_option,
    foreground_option,
    output_format_option,
    print_argspec,
    print_json_for,
    print_schema,
)


@click.group("postgres_exporter", cls=Group)
@click.option(
    "--schema",
    is_flag=True,
    callback=partial(print_schema, model=models.PostgresExporter),
    expose_value=False,
    is_eager=True,
    help="Print the JSON schema of postgres_exporter model and exit.",
)
@click.option(
    "--ansible-argspec",
    is_flag=True,
    callback=partial(print_argspec, model=models.PostgresExporter),
    expose_value=False,
    is_eager=True,
    hidden=True,
    help="Print the Ansible argspec of postgres_exporter model and exit.",
)
def cli() -> None:
    """Handle Prometheus postgres_exporter"""


@cli.command("apply")
@click.option("-f", "--file", type=click.File("r"), metavar="MANIFEST", required=True)
@output_format_option
@dry_run_option
@click.pass_obj
@async_command
async def apply(
    obj: Obj, file: IO[str], output_format: OutputFormat, dry_run: bool
) -> None:
    """Apply manifest as a Prometheus postgres_exporter."""
    exporter = models.PostgresExporter.parse_yaml(file)
    if dry_run:
        ret = interface.ApplyResult(change_state=None)
    else:
        settings = prometheus.get_settings(_site.SETTINGS)
        with obj.lock:
            ret = await impl.apply(exporter, _site.SETTINGS, settings)
    if output_format == OutputFormat.json:
        print_json_for(ret)


@cli.command("install")
@model.as_parameters(models.PostgresExporter, "create")
@click.pass_obj
@async_command
async def install(obj: Obj, postgresexporter: models.PostgresExporter) -> None:
    """Install the service for a (non-local) instance."""
    settings = prometheus.get_settings(_site.SETTINGS)
    with obj.lock:
        async with task.async_transaction():
            await impl.apply(postgresexporter, _site.SETTINGS, settings)


@cli.command("uninstall")
@click.argument("name")
@click.pass_obj
@async_command
async def uninstall(obj: Obj, name: str) -> None:
    """Uninstall the service."""
    with obj.lock:
        await impl.drop(_site.SETTINGS, name)


@cli.command("start")
@click.argument("name")
@foreground_option
@click.pass_obj
@async_command
async def start(obj: Obj, name: str, foreground: bool) -> None:
    """Start postgres_exporter service NAME.

    The NAME argument is a local identifier for the postgres_exporter
    service. If the service is bound to a local instance, it should be
    <version>-<name>.
    """
    settings = prometheus.get_settings(_site.SETTINGS)
    with obj.lock:
        service = impl.system_lookup(name, settings)
        if service is None:
            raise exceptions.InstanceNotFound(name)
        await impl.start(_site.SETTINGS, service, foreground=foreground)


@cli.command("stop")
@click.argument("name")
@click.pass_obj
@async_command
async def stop(obj: Obj, name: str) -> None:
    """Stop postgres_exporter service NAME.

    The NAME argument is a local identifier for the postgres_exporter
    service. If the service is bound to a local instance, it should be
    <version>-<name>.
    """
    settings = prometheus.get_settings(_site.SETTINGS)
    with obj.lock:
        service = impl.system_lookup(name, settings)
        if service is None:
            raise exceptions.InstanceNotFound(name)
        await impl.stop(_site.SETTINGS, service)


@hookimpl
def command() -> click.Group:
    return cli
