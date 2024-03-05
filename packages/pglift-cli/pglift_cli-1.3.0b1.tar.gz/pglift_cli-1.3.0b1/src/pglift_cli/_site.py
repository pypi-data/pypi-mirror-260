# SPDX-FileCopyrightText: 2024 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Final

import click
import pydantic

from pglift import exceptions, plugin_manager
from pglift.models import interface

from . import hookspecs
from ._settings import Settings, SiteSettings
from .pm import PluginManager


def _load_settings() -> Settings:
    try:
        return SiteSettings()
    except (exceptions.SettingsError, pydantic.ValidationError) as e:
        raise click.ClickException(f"invalid site settings\n{e}") from e
    except exceptions.UnsupportedError as e:
        raise click.ClickException(f"unsupported operation: {e}") from None


SETTINGS: Final = _load_settings()
DEFAULT_SETTINGS: Final = Settings()

PLUGIN_MANAGER = PluginManager.get(SETTINGS, hookspecs)

pm = plugin_manager(SETTINGS)
INSTANCE_MODEL: Final = interface.Instance.composite(pm)
ROLE_MODEL: Final = interface.Role.composite(pm)
