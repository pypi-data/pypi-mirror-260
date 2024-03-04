from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Window:
    Resize: Literal["<Configure>"] = "<Configure>"
    """Example:
        my_window.bind(Resize, lambda event: print(event))"""


@dataclass(frozen=True)
class TextWidget:
    PressEnter: Literal["<Return>"] = "<Return>"
    "Events when the Enter key is pressed"
    AnyKey: Literal["<Key>"] = "<Key>"
    "Events when any key is pressed"


Tk = Window()
Toplevel = Window()
Text = TextWidget()
