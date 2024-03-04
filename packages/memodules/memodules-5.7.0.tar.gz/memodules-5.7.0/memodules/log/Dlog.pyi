from ..e_typing import (
    ColorStdOut,
    CanStdOut,
    StdOut,
)
from functools import wraps, _Wrapper
from typing import (
    overload,
    ParamSpec,
    Callable,
    TypeVar,
    TypeVarTuple,
    Any,
)
from .cprint import (
    Color,
)
__all__ = [
    'DebugPrint',
    'log',
]
_Args = ParamSpec('_Args')
_Returns = TypeVar('_Returns')
type Wrapped[**Par, Ret] = Callable[[Callable[Par, Ret]], Callable[Par, Ret]]


def log[**Args, Returns](cfunc: Callable[Args, Returns] | None = ..., /,
        *, debugging: bool = True,
        color: Color.colors = Color.blue,
        show_caller: bool = True,
        show_called: bool = True,
        show_args: bool = True,
        show_returns: bool = True) -> Wrapped[Args, Returns]: ...


class DebugPrint:
    __slots__ = ('debug', 'nl_num')

    def __init__(self, debug_flg: bool, newline_number: int = 3) -> None:
        """デバッグ用ログをデバッグフラグがTrueならcall構文で指定した引数の内容を色違いでコンソール出力してくれるクラス\n
        出力する項目をnewline_number個ごとに改行して出力を見やすくする"""
        self.debug = debug_flg
        self.nl_num = newline_number

    def __call__[*args](self, *args: *args) -> ColorStdOut[*args]:
        """examples:
            >>> debug = DebugPrint(True)
            >>> debug('debug', 'to', 'example')
            (light green)debug: debug, to, example
            >>> debug = DebugPrint(True, newline_number = 2)
            >>> debug('debug', 'to', 'example')
            debug: debug, to,
            \texample"""
        ...
