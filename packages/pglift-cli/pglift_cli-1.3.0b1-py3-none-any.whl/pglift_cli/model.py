# SPDX-FileCopyrightText: 2024 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import enum
import functools
import inspect
import logging
import typing
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, ClassVar, TypeVar

import click
import pydantic
from pydantic.fields import FieldInfo
from pydantic.v1.utils import deep_update, lenient_issubclass

from pglift import exceptions
from pglift._compat import zip
from pglift.models.helpers import Operation, is_optional, optional_type
from pglift.types import CLIConfig, StrEnum, field_annotation

logger = logging.getLogger(__name__)

ModelType = type[pydantic.BaseModel]
T = TypeVar("T", bound=pydantic.BaseModel)
Callback = Callable[..., Any]
ClickDecorator = Callable[[Callback], Callback]
DEFAULT = object()


def as_parameters(
    model_type: ModelType, operation: Operation, *, parse_model: bool = True
) -> ClickDecorator:
    """Attach click parameters (arguments or options) built from a pydantic
    model to the command.

    The argument in callback function must match the base name (lower-case) of
    the pydantic model class. Otherwise, a TypeError is raised.
    """

    def decorator(f: Callback) -> Callback:
        modelnames_and_argnames, paramspecs = zip(
            *reversed(list(_paramspecs_from_model(model_type, operation))), strict=True
        )

        def params_to_modelargs(kwargs: dict[str, Any]) -> dict[str, Any]:
            args = {}
            for modelname, argname in modelnames_and_argnames:
                value = kwargs.pop(argname)
                if value is DEFAULT:
                    continue
                args[modelname] = value
            return args

        if parse_model:
            s = inspect.signature(f)
            model_argname = model_type.__name__.lower()
            try:
                model_param = s.parameters[model_argname]
            except KeyError as e:
                raise TypeError(
                    f"expecting a '{model_argname}: {model_type.__name__}' parameter in '{f.__name__}{s}'"
                ) from e
            ptype = model_param.annotation
            if isinstance(ptype, str):
                # The annotation is "stringized"; we thus follow the wrapper
                # chain as suggested in Python how-to about annotations.
                # Implementation is simplified version of inspect.get_annotations().
                w = f
                while True:
                    if hasattr(w, "__wrapped__"):
                        w = w.__wrapped__
                    elif isinstance(w, functools.partial):
                        w = w.func
                    else:
                        break
                if hasattr(w, "__globals__"):
                    f_globals = w.__globals__
                ptype = eval(ptype, f_globals, None)  # nosec: B307
            if ptype not in (
                model_type,
                inspect.Signature.empty,
            ) and not issubclass(model_type, ptype):
                raise TypeError(
                    f"expecting a '{model_argname}: {model_type.__name__}' parameter in '{f.__name__}{s}'; got {model_param.annotation}"
                )

            @functools.wraps(f)
            def callback(**kwargs: Any) -> Any:
                args = params_to_modelargs(kwargs)
                with catch_validationerror(*paramspecs):
                    model = parse_params_as(model_type, args)
                kwargs[model_argname] = model
                return f(**kwargs)

        else:

            @functools.wraps(f)
            def callback(**kwargs: Any) -> Any:
                args = params_to_modelargs(kwargs)
                values = unnest(model_type, args)
                kwargs.update(values)
                with catch_validationerror(*paramspecs):
                    return f(**kwargs)

        cb = callback
        for p in paramspecs:
            cb = p.decorator(cb)
        return cb

    return decorator


def parse_params_as(model_type: type[T], params: dict[str, Any]) -> T:
    obj = unnest(model_type, params)
    return model_type.model_validate(obj)


def unnest(model_type: type[T], params: dict[str, Any]) -> dict[str, Any]:
    if is_optional(model_type):
        model_type = optional_type(model_type)
    known_fields: dict[str, FieldInfo] = {}
    for fname, f in model_type.model_fields.items():
        if config := field_annotation(f, CLIConfig):
            if config.hide:
                continue
        known_fields[(f.alias or fname)] = f
    obj: dict[str, Any] = {}
    for k, v in params.items():
        if v is None:
            continue
        if k in known_fields:
            obj[k] = v
        elif "_" in k:
            p, subk = k.split("_", 1)
            try:
                field = known_fields[p]
            except KeyError as e:
                raise ValueError(k) from e
            assert field.annotation is not None
            nested = unnest(field.annotation, {subk: v})
            obj[p] = deep_update(obj.get(p, {}), nested)
        else:
            raise ValueError(k)
    return obj


@dataclass(frozen=True)
class ParamSpec(ABC):
    """Intermediate representation for a future click.Parameter."""

    param_decls: Sequence[str]
    attrs: dict[str, Any]
    loc: tuple[str, ...]

    objtype: ClassVar = click.Parameter

    @property
    @abstractmethod
    def decorator(self) -> ClickDecorator:
        """The click decorator for this parameter."""

    def match_loc(self, loc: tuple[str | int, ...]) -> bool:
        """Return True if this parameter spec matches a 'loc' tuple (from
        pydantic.ValidationError).
        """
        return self.loc == loc

    def badparameter_exception(self, message: str) -> click.BadParameter:
        return click.BadParameter(
            message, None, param=self.objtype(self.param_decls, **self.attrs)
        )


class ArgumentSpec(ParamSpec):
    """Intermediate representation for a future click.Argument."""

    objtype: ClassVar = click.Argument

    def __post_init__(self) -> None:
        assert (
            len(self.param_decls) == 1
        ), f"expecting exactly one parameter declaration: {self.param_decls}"

    @property
    def decorator(self) -> ClickDecorator:
        return click.argument(*self.param_decls, **self.attrs)


class OptionSpec(ParamSpec):
    """Intermediate representation for a future click.Option."""

    objtype: ClassVar = click.Option

    @property
    def decorator(self) -> ClickDecorator:
        return click.option(*self.param_decls, **self.attrs)


@dataclass(frozen=True)
class _Parent:
    argname: str
    required: bool


def _paramspecs_from_model(
    model_type: ModelType,
    operation: Operation,
    *,
    _parents: tuple[_Parent, ...] = (),
) -> Iterator[tuple[tuple[str, str], ParamSpec]]:
    """Yield parameter declarations for click corresponding to fields of a
    pydantic model type.
    """

    def default(ctx: click.Context, param: click.Argument, value: Any) -> Any:
        if (param.multiple and value == ()) or (value == param.default):
            return DEFAULT
        return value

    for fname, field in model_type.model_fields.items():
        modelname = argname = field.alias or fname
        if config := field_annotation(field, CLIConfig):
            if config.hide:
                continue
            if config.name is not None:
                argname = config.name
        if (
            operation == "update"
            and isinstance(field.json_schema_extra, dict)
            and field.json_schema_extra.get("readOnly")
        ):
            continue
        ftype = field.annotation
        assert ftype is not None
        if is_optional(ftype):
            ftype = optional_type(ftype)
        origin_type = typing.get_origin(ftype)
        if origin_type is typing.Annotated:
            ftype = typing.get_args(ftype)[0]
            assert ftype is not None
        nested = lenient_issubclass(origin_type or ftype, pydantic.BaseModel)
        required = field.is_required()
        if not nested and not _parents and required:
            yield (modelname, argname), ArgumentSpec(
                (argname.replace("_", "-"),), {"type": ftype}, loc=(modelname,)
            )
        else:
            metavar: str | None
            if config and config.metavar is not None:
                metavar = config.metavar
            else:
                metavar = argname
            if metavar is not None:
                metavar = metavar.upper()
            argparts = tuple(p.argname for p in _parents) + tuple(argname.split("_"))
            fname = f"--{'-'.join(argparts)}"
            description = None
            if field.description:
                description = field.description
                description = description[0].upper() + description[1:]
            attrs: dict[str, Any] = {}
            if origin_type is typing.Literal:
                choices = list(typing.get_args(ftype))
                if len(choices) == 1:  # const
                    continue
                if config and config.choices is not None:
                    choices = config.choices
                attrs["type"] = click.Choice(choices)
                metavar = None
            elif lenient_issubclass(ftype, enum.Enum):
                if config and config.choices is not None:
                    choices = config.choices
                else:
                    choices = choices_from_enum(ftype)
                attrs["type"] = click.Choice(choices)
            elif nested:
                yield from _paramspecs_from_model(
                    ftype, operation, _parents=_parents + (_Parent(argname, required),)
                )
                continue
            elif lenient_issubclass(origin_type or ftype, list):
                if operation != "create":
                    continue
                attrs["multiple"] = True
                try:
                    (itemtype,) = ftype.__args__
                except ValueError:
                    pass
                else:
                    if lenient_issubclass(itemtype, enum.Enum):
                        attrs["type"] = click.Choice(choices_from_enum(itemtype))
                    else:
                        attrs["metavar"] = metavar
            elif lenient_issubclass(ftype, pydantic.SecretStr):
                attrs["prompt"] = (
                    description.rstrip(".") if description is not None else True
                )
                attrs["prompt_required"] = False
                attrs["confirmation_prompt"] = True
                attrs["hide_input"] = True
            elif lenient_issubclass(ftype, bool):
                fname = f"{fname}/--no-{fname[2:]}"
                # Use None to distinguish unspecified option from the default value.
                attrs["default"] = None
            else:
                attrs["metavar"] = metavar
            if description is not None:
                if description[-1] not in ".?":
                    description += "."
                attrs["help"] = description
            if field.is_required() and all(p.required for p in _parents):
                attrs["required"] = True
            argname = "_".join(argparts)
            loc = tuple(p.argname for p in _parents) + (modelname,)
            modelname = "_".join(loc)
            yield (modelname, argname), OptionSpec(
                (fname,), {"callback": default, **attrs}, loc=loc
            )


def choices_from_enum(e: type[enum.Enum]) -> list[Any]:
    if lenient_issubclass(e, StrEnum):
        return list(e)
    else:
        return [v.value for v in e]


@contextmanager
def catch_validationerror(*paramspec: ParamSpec) -> Iterator[None]:
    try:
        yield None
    except (exceptions.ValidationError, pydantic.ValidationError) as e:
        errors = e.errors()
        for pspec in paramspec:
            for err in errors:
                if pspec.match_loc(err["loc"]):
                    raise pspec.badparameter_exception(err["msg"]) from None
        logger.debug("a validation error occurred", exc_info=True)
        raise click.ClickException(str(e)) from None
