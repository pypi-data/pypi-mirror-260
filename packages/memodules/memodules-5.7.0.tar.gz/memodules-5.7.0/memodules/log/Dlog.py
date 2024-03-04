from ..e_typing import (
    ColorStdOut,
)
from functools import wraps
from .cprint import (
    Color,
)
import sys
__all__ = [
    'DebugPrint',
    'log',
]


def log(cfunc=None, /,
        *, debugging=True,
        color=Color.blue,
        show_caller=True,
        show_called=True,
        show_args=True,
        show_returns=True):
    match cfunc:
        case None:
            def decorator(func, /):
                if not debugging: return func
                @wraps(func)
                def wrapper(*args, **kwargs):
                    show = ''
                    flg = False
                    if show_caller:
                        c_frame = sys._getframe(1)
                        _mid = f'{c_frame.f_globals["__name__"]}.'
                        _mid += f'{c_frame.f_code.co_name}'
                        show += f'Caller: {_mid}'
                        del _mid
                        flg = True
                    if show_called:
                        if flg:
                            show += '\n'
                        show += f'Called: {func.__name__}'
                        flg = True
                    if show_args:
                        if flg:
                            show += '\n'
                        show += f'Args: {args}, {kwargs}'
                        flg = True
                    if flg:
                        color(show)
                        del show, flg
                    result = func(*args, **kwargs)
                    if show_returns:
                        color(f'Returns: {result}')
                    return result
                return wrapper
            return decorator
        case f:
            @wraps(f)
            def decorator(func):
                if not debugging: return func
                @wraps(func)
                def wrapper(*args, **kwargs):
                    show = ''
                    flg = False
                    if show_caller:
                        c_frame = sys._getframe(1)
                        _mid = f'{c_frame.f_globals["__name__"]}.'
                        _mid += f'{c_frame.f_code.co_name}'
                        show += f'Caller: {_mid}'
                        del _mid
                        flg = True
                    if show_called:
                        if flg:
                            show += '\n'
                        show += f'Called: {func.__name__}'
                        flg = True
                    if show_args:
                        if flg:
                            show += '\n'
                        show += f'Args: {args}, {kwargs}'
                        flg = True
                    if flg:
                        color(show)
                        del show, flg
                    result = func(*args, **kwargs)
                    if show_returns:
                        color(f'Returns: {result}')
                    return result
                return wrapper
            return decorator(f)


class DebugPrint:
    __slots__ = ('debug', 'nl_num')

    def __init__(self, debug_flg, newline_number=3):
        """デバッグ用ログをデバッグフラグがTrueならcall構文で指定した引数の内容を色違いでコンソール出力してくれるクラス\n
        出力する項目をnewline_number個ごとに改行して出力を見やすくする"""
        self.debug = debug_flg
        self.nl_num = newline_number

    def __call__(self, *args):
        """examples:
            >>> debug = DebugPrint(True)
            >>> debug('debug', 'to', 'example')
            (light green)debug: debug, to, example
            >>> debug = DebugPrint(True, newline_number = 2)
            >>> debug('debug', 'to', 'example')
            debug: debug, to,
            \texample"""
        nt = '\n\t'
        spc = ' '
        if self.debug:
            for i in range(len(args)):
                if i == 0:
                    content = args[i]
                else:
                    mid_entry = nt if i % self.nl_num == 0 else spc
                    content = f'{content},{mid_entry}{args[i]}'

            print(f'\033[92mdebug: {content}\033[0m')
