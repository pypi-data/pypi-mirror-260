# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import abc
import asyncio
import enum
import json
import logging
import os
import pathlib
import tempfile
import time
import typing
from collections.abc import Coroutine, Iterable, Iterator, Sequence
from contextlib import contextmanager
from functools import cache, cached_property, singledispatch, wraps
from typing import Any, Callable, TypeVar

import click
import filelock
import psycopg
import pydantic
import pydantic_core
import rich
import rich.prompt
from click.shell_completion import CompletionItem
from rich.console import Console
from rich.table import Table

from pglift import exceptions, install, instances, task
from pglift._compat import ParamSpec
from pglift.models import helpers, system
from pglift.settings import Settings
from pglift.settings._postgresql import PostgreSQLVersion
from pglift.task import Displayer
from pglift.types import AutoStrEnum, ByteSizeType

from . import _site, model
from .console import console

logger = logging.getLogger("pglift")


def model_dump(
    m: pydantic.BaseModel, by_alias: bool = True, **kwargs: Any
) -> dict[str, Any]:
    return m.model_dump(by_alias=by_alias, **kwargs)


@singledispatch
def prettify(value: Any, annotations: Sequence[Any] = ()) -> str:
    """Prettify a value."""
    return str(value)


@prettify.register(int)
def _(value: int, annotations: Sequence[Any] = ()) -> str:
    """Prettify an integer value"""
    for a in annotations:
        if isinstance(a, ByteSizeType):
            return a.human_readable(value)
    return str(value)


@prettify.register(list)
def _(value: list[Any], annotations: Sequence[Any] = ()) -> str:
    """Prettify a List value"""
    return ", ".join(str(x) for x in value)


@prettify.register(set)
def _(value: set[Any], annotations: Sequence[Any] = ()) -> str:
    """Prettify a Set value"""
    return prettify(sorted(value), annotations)


@prettify.register(type(None))
def _(value: None, annotations: Sequence[Any] = ()) -> str:
    """Prettify a None value"""
    return ""


@prettify.register(dict)
def _(value: dict[str, Any], annotations: Sequence[Any] = ()) -> str:
    """Prettify a Dict value"""

    def prettify_dict(
        d: dict[str, Any], level: int = 0, indent: str = "  "
    ) -> Iterator[str]:
        for key, value in d.items():
            row = f"{indent * level}{key}:"
            if isinstance(value, dict):
                yield row
                yield from prettify_dict(value, level + 1)
            else:
                yield row + " " + prettify(value)

    return "\n".join(prettify_dict(value))


_I = TypeVar("_I")


def print_table_for(
    items: Iterable[_I],
    asdict: Callable[[_I], dict[str, Any]],
    title: str | None = None,
    *,
    console: Console = console,
    **kwargs: Any,
) -> None:
    """Render a list of items as a table."""
    table = None
    headers: list[str] = []
    rows = []
    for item in items:
        row = []
        hdr = []
        annotations = typing.get_type_hints(item.__class__, include_extras=True)
        for k, v in asdict(item).items():
            f_annotations = []
            try:
                i_annotations = annotations[k]
            except KeyError:
                pass
            else:
                if args := typing.get_args(i_annotations):
                    _, *f_annotations = args
            hdr.append(k)
            row.append(prettify(v, f_annotations))
        if not headers:
            headers = hdr[:]
        rows.append(row)
    if not rows:
        return
    table = Table(*headers, title=title, **kwargs)
    for row in rows:
        table.add_row(*row)
    console.print(table)


def print_json_for(data: Any, *, console: Console = console) -> None:
    """Render `data` as JSON."""
    console.print_json(data=pydantic_core.to_jsonable_python(data))


P = ParamSpec("P")


def print_schema(
    context: click.Context,
    param: click.Parameter,
    value: bool,
    *,
    model: type[pydantic.BaseModel],
    console: Console = console,
) -> None:
    """Callback for --schema flag."""
    if value:
        console.print_json(data=model.model_json_schema())
        context.exit()


def print_argspec(
    context: click.Context,
    param: click.Parameter,
    value: bool,
    *,
    model: type[pydantic.BaseModel],
) -> None:
    """Callback for --ansible-argspec flag."""
    if value:
        click.echo(
            json.dumps(helpers.argspec_from_model(model), sort_keys=False, indent=2)
        )
        context.exit()


def pass_instance(f: Callable[P, None]) -> Callable[P, None]:
    """Command decorator passing 'instance' bound to click.Context's object."""

    @wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
        context = click.get_current_context()
        instance = context.obj.instance
        assert isinstance(instance, system.Instance), instance
        context.invoke(f, instance, *args, **kwargs)

    return wrapper


def get_instance(name: str, version: str | None, settings: Settings) -> system.Instance:
    """Return an Instance from name/version, possibly guessing version if unspecified."""
    if version is None:
        found = None
        for version in PostgreSQLVersion:
            try:
                instance = system.Instance.system_lookup((name, version, settings))
            except exceptions.InstanceNotFound:
                logger.debug("instance '%s' not found in version %s", name, version)
            else:
                if found:
                    raise click.BadParameter(
                        f"instance {name!r} exists in several PostgreSQL versions;"
                        " please select version explicitly"
                    )
                found = instance

        if found:
            return found

        raise click.BadParameter(f"instance {name!r} not found")

    try:
        return system.Instance.system_lookup((name, version, settings))
    except Exception as e:
        raise click.BadParameter(str(e)) from None


def nameversion_from_id(instance_id: str) -> tuple[str, str | None]:
    version = None
    try:
        version, name = instance_id.split("/", 1)
    except ValueError:
        name = instance_id
    return name, version


def instance_lookup(
    context: click.Context, param: click.Parameter, value: None | str | tuple[str]
) -> system.Instance | tuple[system.Instance, ...]:
    """Return one or more system.Instance, possibly guessed if there is only
    one on system, depending on 'param' variadic flag (nargs).
    """

    settings = _site.SETTINGS

    def guess() -> tuple[str, str | None]:
        """Return (name, version) of the instance found on system, if there's
        only one, or fail.
        """
        try:
            (i,) = instances.system_list(settings)
        except ValueError:
            raise click.UsageError(
                f"argument {param.get_error_hint(context)} is required."
            ) from None
        return i.name, i.version

    if context.params.get("all_instances"):
        return tuple(
            get_instance(i.name, i.version, i._settings)
            for i in instances.system_list(settings)
        )

    if param.nargs == 1:
        if value is None:
            name, version = guess()
        else:
            assert isinstance(value, str)
            name, version = nameversion_from_id(value)
        return get_instance(name, version, settings)

    elif param.nargs == -1:
        assert isinstance(value, tuple)
        if value:
            return tuple(
                get_instance(*nameversion_from_id(item), settings) for item in value
            )
        else:
            name, version = guess()
            return (get_instance(name, version, settings),)

    else:
        raise AssertionError(f"unexpected nargs={param.nargs}")


def instance_bind_context(
    context: click.Context, param: click.Parameter, value: str | None
) -> None:
    """Bind instance specified as -i/--instance to context's object, possibly
    guessing from available instance if there is only one.
    """
    obj: Obj = context.obj
    version: str | None
    if value is None:
        values = list(instances.system_list(_site.SETTINGS))
        if not values:
            obj._instance = "no instance found; create one first."
            return
        elif len(values) > 1:
            option = param.get_error_hint(context)
            obj._instance = f"several instances found; option {option} is required."
            return
        (i,) = values
        name, version = i.name, i.version
    else:
        name, version = nameversion_from_id(value)
    instance = get_instance(name, version, _site.SETTINGS)
    obj._instance = instance


def _list_instances(
    context: click.Context, param: click.Parameter, incomplete: str
) -> list[CompletionItem]:
    """Shell completion function for instance identifier <name> or <version>/<name>."""
    out = []
    iname, iversion = nameversion_from_id(incomplete)
    for i in instances.system_list(_site.SETTINGS):
        if iversion is not None and i.version.startswith(iversion):
            if i.name.startswith(iname):
                out.append(
                    CompletionItem(f"{i.version}/{i.name}", help=f"port={i.port}")
                )
            else:
                out.append(CompletionItem(i.version))
        else:
            out.append(
                CompletionItem(i.name, help=f"{i.version}/{i.name} port={i.port}")
            )
    return out


F = TypeVar("F", bound=Callable[..., Any])


def instance_identifier(nargs: int = 1, required: bool = False) -> Callable[[F], F]:
    def decorator(fn: F) -> F:
        command = click.argument(
            "instance",
            nargs=nargs,
            required=required,
            callback=instance_lookup,
            shell_complete=_list_instances,
        )(fn)
        assert command.__doc__
        command.__doc__ += (
            "\n\n    INSTANCE identifies target instance as <version>/<name> where the "
            "<version>/ prefix may be omitted if there is only one instance "
            "matching <name>."
        )
        if not required:
            command.__doc__ += " Required if there is more than one instance on system."
        return command

    return decorator


instance_identifier_option = click.option(
    "-i",
    "--instance",
    "instance",
    metavar="<version>/<name>",
    callback=instance_bind_context,
    shell_complete=_list_instances,
    help=(
        "Instance identifier; the <version>/ prefix may be omitted if "
        "there's only one instance matching <name>. "
        "Required if there is more than one instance on system."
    ),
)


class OutputFormat(AutoStrEnum):
    """Output format"""

    json = enum.auto()


output_format_option = click.option(
    "-o",
    "--output-format",
    type=click.Choice(model.choices_from_enum(OutputFormat), case_sensitive=False),
    help="Specify the output format.",
)

dry_run_option = click.option(
    "--dry-run", is_flag=True, help="Only validate input data."
)


def validate_foreground(
    context: click.Context, param: click.Parameter, value: bool
) -> bool:
    if _site.SETTINGS.service_manager == "systemd" and value:
        raise click.BadParameter("cannot be used with systemd")
    return value


foreground_option = click.option(
    "--foreground",
    is_flag=True,
    help="Start the program in foreground.",
    callback=validate_foreground,
)


@contextmanager
def command_logging(logdir: pathlib.Path) -> Iterator[None]:
    logdir_created = False
    logfilename = f"{time.time()}.log"
    logfile = logdir / logfilename
    try:
        if not logdir.exists():
            logdir.mkdir(parents=True)
            logdir_created = True
    except OSError:
        # Might be, e.g. PermissionError, if log file path is not writable.
        logfile = pathlib.Path(
            tempfile.NamedTemporaryFile(prefix="pglift", suffix=logfilename).name
        )
    handler = logging.FileHandler(logfile)
    formatter = logging.Formatter(
        fmt="%(levelname)-8s - %(asctime)s - %(name)s:%(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if logdir_created:
        logger.debug("created log directory %s", logdir)
    logger.debug("logging command at %s", logfile)
    keep_logfile = False
    try:
        yield None
    except (click.Abort, click.ClickException, click.exceptions.Exit):
        raise
    except Exception:
        keep_logfile = True
        logger.exception("an unexpected error occurred")
        raise click.ClickException(
            "an unexpected error occurred, this is probably a bug; "
            f"details can be found at {logfile}"
        ) from None
    finally:
        if not keep_logfile:
            os.unlink(logfile)
            if logdir_created and next(logdir.iterdir(), None) is None:
                logger.debug("removing log directory %s", logdir)
                logdir.rmdir()


class LogDisplayer:
    def handle(self, msg: str) -> None:
        logger.info(msg)


class InteractiveUserInterface:
    """An interactive UI that prompts for confirmation."""

    def confirm(self, message: str, default: bool) -> bool:
        return rich.prompt.Confirm().ask(
            f"[yellow]>[/yellow] {message}", default=default
        )

    @cache
    def prompt(self, message: str, hide_input: bool = False) -> str:
        return rich.prompt.Prompt().ask(
            f"[yellow]>[/yellow] {message}", password=hide_input
        )


class Obj:
    """Object bound to click.Context"""

    # Set in commands taking a -i/--instance option through
    # instance_identifier_option decorator's callback.
    _instance: str | system.Instance

    def __init__(
        self,
        *,
        displayer: Displayer | None = None,
        debug: bool = False,
    ) -> None:
        self.displayer = displayer
        self.debug = debug

    @cached_property
    def lock(self) -> filelock.FileLock:
        """Lock to prevent concurrent execution."""
        lockfile = _site.SETTINGS.cli.lock_file
        lockfile.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        return filelock.FileLock(lockfile, timeout=0)

    @cached_property
    def instance(self) -> system.Instance:
        if isinstance(self._instance, system.Instance):
            return self._instance
        else:
            assert isinstance(self._instance, str)
            raise click.UsageError(self._instance)


def async_command(
    callback: Callable[P, Coroutine[None, None, None]]
) -> Callable[P, None]:
    @wraps(callback)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
        asyncio.run(callback(*args, **kwargs))

    return wrapper


class Command(click.Command):
    def invoke(self, context: click.Context) -> Any:
        obj: Obj = context.obj
        displayer = obj.displayer
        with command_logging(_site.SETTINGS.cli.logpath):
            try:
                with task.displayer_installed(displayer):
                    return super().invoke(context)
            except filelock.Timeout:
                raise click.ClickException("another operation is in progress") from None
            except exceptions.Cancelled as e:
                logger.warning(str(e))
                raise click.Abort from None
            except (exceptions.ValidationError, pydantic.ValidationError) as e:
                raise click.ClickException(str(e)) from None
            except exceptions.Error as e:
                logger.debug("an internal error occurred", exc_info=obj.debug)
                msg = str(e)
                if isinstance(e, exceptions.CommandError):
                    if e.stderr:
                        msg += f"\n{e.stderr}"
                    if e.stdout:
                        msg += f"\n{e.stdout}"
                raise click.ClickException(msg) from None
            except psycopg.DatabaseError as e:
                logger.debug("a database error occurred", exc_info=True)
                raise click.ClickException(str(e).strip()) from None


class Group(click.Group):
    command_class = Command
    group_class = type

    def add_command(self, command: click.Command, name: str | None = None) -> None:
        name = name or command.name
        assert name not in self.commands, f"command {name!r} already registered"
        super().add_command(command, name)

    def invoke(self, ctx: click.Context) -> Any:
        if not install.check(_site.SETTINGS):
            raise click.ClickException(
                "broken installation; did you run 'site-configure install'?",
            )
        return super().invoke(ctx)


class PluggableCommandGroup(abc.ABC, Group):
    _plugin_commands_loaded: bool = False

    @abc.abstractmethod
    def register_plugin_commands(self, obj: Obj) -> None: ...

    def _load_plugins_commands(self, context: click.Context) -> None:
        if self._plugin_commands_loaded:
            return
        obj: Obj | None = context.obj
        if obj is None:
            obj = context.ensure_object(Obj)
        if obj is None:
            return
        self.register_plugin_commands(obj)
        self._plugin_commands_loaded = True

    def list_commands(self, context: click.Context) -> list[str]:
        self._load_plugins_commands(context)
        return super().list_commands(context)

    def get_command(self, context: click.Context, name: str) -> click.Command | None:
        self._load_plugins_commands(context)
        return super().get_command(context, name)
