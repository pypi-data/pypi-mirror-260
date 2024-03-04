from __future__ import annotations
from dataclasses import dataclass
from ..e_typing import (
    ColorStdOut,
)
from typing import (
    Callable,
    TypeVar,
    TypeVarTuple,
    TypeAlias,
    Generic,
    Literal,
    Type,
    Any,
)
__all__ = [
    # const
    'Color',

    # functions
    # #custom
    'color_print',

    # #presets
    'blue',
    'gray',
    'green',
    'magenta',
    'red',
    'turquoise',
    'yellow',

    # #decoration
    'border',
]
_AT = TypeVar('_AT', bound=Callable[..., Any])
values = TypeVarTuple('values')
default = TypeVar('default', Literal[True], Literal[False])


def color_print(*args: _AT,
                color: str,
                undo_when_exit: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Color of Custom`"
    ...


def gray(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Gray Color`"
    ...


def red(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Red Color`"
    ...


def green(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Green Color`"
    ...


def yellow(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Yellow Color`"
    ...


def blue(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Blue Color`"
    ...


def magenta(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Magenta Color`"
    ...


def turquoise(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Turquoise Color`"
    ...


def border(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Border String`"
    ...


@dataclass(frozen=True)
class Color:
    """```Python

class Color:
    def blue(*values: _AT, default: bool = True) -> ColorStdOut[_AT]: ...
    def gray(*values: _AT, default: bool = True) -> ColorStdOut[_AT]: ...
    def green(*values: _AT, default: bool = True) -> ColorStdOut[_AT]: ...
    def magenta(*values: _AT, default: bool = True) -> ColorStdOut[_AT]: ...
    def red(*values: _AT, default: bool = True) -> ColorStdOut[_AT]: ...
    def turquoise(*values: _AT, default: bool = True) -> ColorStdOut[_AT]: ...
    def yellow(*values: _AT, default: bool = True) -> ColorStdOut[_AT]: ...
    def border(*values: _AT, default: bool = True) -> ColorStdOut[_AT]: ...
```
```MarkDown
======================================================
Constant of `cprint` Functions
```"""
    colors: Type[Callable[[*values, default], ColorStdOut[*values]]]
    blue: Callable[[*values, default], ColorStdOut[*values]]
    gray: Callable[[*values, default], ColorStdOut[*values]]
    green: Callable[[*values, default], ColorStdOut[*values]]
    magenta: Callable[[*values, default], ColorStdOut[*values]]
    red: Callable[[*values, default], ColorStdOut[*values]]
    turquoise: Callable[[*values, default], ColorStdOut[*values]]
    yellow: Callable[[*values, default], ColorStdOut[*values]]
    border: Callable[[*values, default], ColorStdOut[*values]]
