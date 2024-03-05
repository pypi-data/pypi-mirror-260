# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import click
import pgtoolkit.conf

from pglift import h, hook, instances, postgresql
from pglift.models import system
from pglift.types import ConfigChanges, Status

from .util import Group, Obj, async_command, instance_identifier_option, pass_instance


@click.group(cls=Group)
@instance_identifier_option
def cli(**kwargs: Any) -> None:
    """Manage configuration of a PostgreSQL instance."""


def show_configuration_changes(
    changes: ConfigChanges, parameters: Iterable[str] | None = None
) -> None:
    for param, (old, new) in sorted(changes.items()):
        click.secho(f"{param}: {old} -> {new}", err=True, fg="green")
    if parameters is None:
        return
    if unchanged := set(parameters) - set(changes):
        click.secho(
            f"changes in {', '.join(map(repr, sorted(unchanged)))} not applied",
            err=True,
            fg="red",
        )
        click.secho(
            " hint: either these changes have no effect (values already set) "
            "or specified parameters are already defined in an un-managed file "
            "(e.g. 'postgresql.conf')",
            err=True,
            fg="blue",
        )


@cli.command("show")
@click.argument("parameter", nargs=-1)
@pass_instance
def show(instance: system.Instance, parameter: tuple[str]) -> None:
    """Show configuration (all parameters or specified ones).

    Only uncommented parameters are shown when no PARAMETER is specified. When
    specific PARAMETERs are queried, commented values are also shown.
    """
    config = instance.config()
    for entry in config.entries.values():
        if parameter:
            if entry.name in parameter:
                if entry.commented:
                    click.echo(f"# {entry.name} = {entry.serialize()}")
                else:
                    click.echo(f"{entry.name} = {entry.serialize()}")
        elif not entry.commented:
            click.echo(f"{entry.name} = {entry.serialize()}")


def validate_configuration_parameters(
    context: click.Context, param: click.Parameter, value: tuple[str]
) -> dict[str, str]:
    items = {}
    for v in value:
        try:
            key, val = v.split("=", 1)
        except ValueError:
            raise click.BadParameter(v) from None
        items[key] = val
    return items


@cli.command("set")
@click.argument(
    "parameters",
    metavar="<PARAMETER>=<VALUE>...",
    nargs=-1,
    callback=validate_configuration_parameters,
    required=True,
)
@pass_instance
@click.pass_obj
@async_command
async def set_(obj: Obj, instance: system.Instance, parameters: dict[str, Any]) -> None:
    """Set configuration items."""
    with obj.lock:
        status = await postgresql.status(instance)
        manifest = await instances._get(instance, status)
        manifest.settings.update(parameters)
        changes = await instances.configure(
            instance, manifest, _is_running=status == Status.running
        )
        show_configuration_changes(changes, parameters.keys())


@cli.command("remove")
@click.argument("parameters", nargs=-1, required=True)
@pass_instance
@click.pass_obj
@async_command
async def remove(obj: Obj, instance: system.Instance, parameters: tuple[str]) -> None:
    """Remove configuration items."""
    with obj.lock:
        status = await postgresql.status(instance)
        manifest = await instances._get(instance, status)
        for p in parameters:
            try:
                del manifest.settings[p]
            except KeyError:
                raise click.ClickException(
                    f"{p!r} not found in managed configuration"
                ) from None
        changes = await instances.configure(
            instance, manifest, _is_running=status == Status.running
        )
        show_configuration_changes(changes, parameters)


@cli.command("edit")
@pass_instance
@click.pass_obj
@async_command
async def edit(obj: Obj, instance: system.Instance) -> None:
    """Edit managed configuration."""
    with obj.lock:
        actual_config = hook(
            instance._settings, h.postgresql_editable_conf, instance=instance
        )
        edited = click.edit(text=actual_config)
        if edited is None:
            click.echo("no change", err=True)
            return
        config = pgtoolkit.conf.parse_string(edited)
        values = config.as_dict()
        status = await postgresql.status(instance)
        manifest = await instances._get(instance, status)
        manifest.settings.clear()
        manifest.settings.update(values)
        changes = await instances.configure(
            instance, manifest, _is_running=status == Status.running
        )
        show_configuration_changes(changes)
