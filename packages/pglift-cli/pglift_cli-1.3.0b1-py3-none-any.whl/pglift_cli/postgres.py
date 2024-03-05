# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import click

from pglift.cmd import execute_program
from pglift.exceptions import InstanceNotFound
from pglift.models import system

from . import _site


def instance_from_qualname(
    context: click.Context, param: click.Parameter, value: str
) -> system.PostgreSQLInstance:
    try:
        return system.PostgreSQLInstance.from_qualname(value, _site.SETTINGS)
    except (ValueError, InstanceNotFound) as e:
        raise click.BadParameter(str(e), context) from None


@click.command("postgres", hidden=True)
@click.argument("instance", callback=instance_from_qualname)
def cli(instance: system.Instance) -> None:
    """Start postgres for specified INSTANCE, identified as <version>-<name>."""
    cmd = [str(instance.bindir / "postgres"), "-D", str(instance.datadir)]
    execute_program(cmd)
