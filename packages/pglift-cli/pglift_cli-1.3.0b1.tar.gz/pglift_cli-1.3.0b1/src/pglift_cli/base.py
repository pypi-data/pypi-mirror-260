# SPDX-FileCopyrightText: 2024 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from collections import OrderedDict

import click

from pglift import hooks

from . import _site, database
from . import hookspecs as h
from . import instance, pgconf, postgres, role


class CLIGroup(click.Group):
    """Group gathering main commands (defined here), commands from submodules
    and commands from plugins.
    """

    submodules = OrderedDict(
        [
            ("instance", instance.cli),
            ("pgconf", pgconf.cli),
            ("role", role.cli),
            ("database", database.cli),
            ("postgres", postgres.cli),
        ]
    )

    def list_commands(self, context: click.Context) -> list[str]:
        main_commands = super().list_commands(context)
        plugins_commands: list[str] = sorted(g.name for g in hooks(_site.PLUGIN_MANAGER, h.command))  # type: ignore[misc]
        return main_commands + list(self.submodules) + plugins_commands

    def get_command(self, context: click.Context, name: str) -> click.Command | None:
        main_command = super().get_command(context, name)
        if main_command is not None:
            return main_command
        try:
            command = self.submodules[name]
        except KeyError:
            pass
        else:
            assert isinstance(command, click.Command), command
            return command
        for group in hooks(_site.PLUGIN_MANAGER, h.command):
            assert isinstance(group, click.Command)
            if group.name == name:
                return group
        return None
