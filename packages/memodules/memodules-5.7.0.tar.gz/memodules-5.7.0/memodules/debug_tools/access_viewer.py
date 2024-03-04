from typing import Any, Self, TextIO
import sys


class AccessObserver:
    def __init__(self, name: str, target_object: object, o_out: TextIO = sys.stdout, chain_observe: bool = True) -> None:
        self.name = name
        self.target = target_object
        self.stdout = o_out
        self.chain = chain_observe

    def __getattr__(self, name: str):
        if self.chain:
            def args_viewer(*args: Any, **kwargs: Any):
                result = None
                if name == 'fileno':
                    result = 0
                elif name == 'readline':
                    result = 'test line'
                print(f'{self.name}\nAccessName: {name}\nArgs: {args}\nKwArgs: {kwargs}', file=self.stdout)
                result = self if result is None else result
                return result
            return args_viewer
        else:
            print(f'AccessName: {name}')
            return getattr(self.target, name)


class StdIOTestSpace:
    def __enter__(self) -> Self:
        self.o_in = sys.stdin
        self.o_out = sys.stdout
        self.o_err = sys.stderr
        sys.stdin = AccessObserver('sys.stdin', self.o_out)
        sys.stdout = AccessObserver('sys.stdout', self.o_out)
        sys.stderr = AccessObserver('sys.stderr', self.o_out)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        sys.stdin = self.o_in
        sys.stdout = self.o_out
        sys.stderr = self.o_err
        return False
