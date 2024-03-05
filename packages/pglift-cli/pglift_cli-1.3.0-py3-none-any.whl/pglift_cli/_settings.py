# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from typing import Annotated

from pydantic import Field

from pglift.settings import Settings as BaseSettings
from pglift.settings import SiteSettings as BaseSiteSettings
from pglift.settings.base import BaseModel, LogPath, RunPath


class CLISettings(BaseModel):
    """Settings for pglift's command-line interface."""

    logpath: Annotated[
        Annotated[Path, LogPath],
        Field(
            description="Directory where temporary log files from command executions will be stored",
            title="CLI log directory",
        ),
    ] = Path()

    log_format: Annotated[
        str, Field(description="Format for log messages when written to a file")
    ] = "%(asctime)s %(levelname)-8s %(name)s - %(message)s"

    date_format: Annotated[
        str, Field(description="Date format in log messages when written to a file")
    ] = "%Y-%m-%d %H:%M:%S"

    lock_file: Annotated[
        Path, RunPath, Field(description="Path to lock file dedicated to pglift")
    ] = Path(".pglift.lock")


class Settings(BaseSettings):
    cli: Annotated[CLISettings, Field(default_factory=CLISettings)]


class SiteSettings(Settings, BaseSiteSettings):
    pass
