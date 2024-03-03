# `envenom` - an elegant application configurator for the more civilized age
# Copyright (C) 2024-  Artur Ciesielski <artur.ciesielski@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from collections.abc import Callable, Iterable
from dataclasses import Field, field, make_dataclass
from typing import Any, Type, TypeAlias, TypeVar

from envenom.entries import Entry, EntryWithDefault, OptionalEntry, RequiredEntry
from envenom.parsers import default_parser
from envenom.vars import DefaultType, ParserType

T = TypeVar("T")

FieldDefinition: TypeAlias = tuple[str, Type[T], Field[T]]

# Why so much <# type: ignore> in this file?
#
# So dataclasses are lying to us.
#
# When the `field` function is called it creates a Field[T] object, but it tells
# us that it really returns T, I swear, pretty please. Because we're we're exposing
# a similar interface and hooking into this exact layer, we need to:
#   - ignore the return value from `field`; it's a lie anyway
#   - we need to lie to our consumers on the API side just like `field` would


def config(
    namespace: Iterable[str] | str | None = None,
) -> Callable[[Type[T]], Type[T]]:
    def wrapper(cls: Type[T]) -> Type[T]:
        fields: list[FieldDefinition[Any]] = []
        for field_name, field_type in cls.__annotations__.items():
            field_obj = cls.__dict__[field_name]
            if isinstance(field_obj, Entry):
                entry: Entry[Any]
                fields.append(
                    (
                        field_name,
                        field_type,
                        field(
                            init=False,
                            repr=True,
                            hash=True,
                            metadata={
                                "entry": (entry := cls.__dict__[field_name]),
                                "type": field_type,
                                "var": (var := entry.get_var(field_name, namespace)),
                            },
                            default_factory=var.get,  # type: ignore
                        ),
                    )
                )
            else:
                fields.append((field_name, field_type, field_obj))

        return make_dataclass(cls.__name__, fields, frozen=True, eq=True)

    return wrapper


def optional(parser: ParserType[T] = default_parser, *, file: bool = True) -> T | None:
    return OptionalEntry(parser=parser, file=file)  # type: ignore


def with_default(
    parser: ParserType[T] = default_parser,
    *,
    default: DefaultType[T],
    file: bool = True,
) -> T:
    return EntryWithDefault(
        parser=parser,
        file=file,
        default=default,  # type: ignore
    )


def required(parser: ParserType[T] = default_parser, *, file: bool = True) -> T:
    return RequiredEntry(parser=parser, file=file)  # type: ignore
