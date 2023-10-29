import tkinter.font
from typing import Literal


FONT_CACHE: dict[tuple[int, str, str], tuple[tkinter.font.Font, str]] = {}


def get_font(size: int, weight: Literal["normal", "bold"], slant: Literal["roman", "italic"]) -> tkinter.font.Font:
    key = (size, weight, slant)
    if key not in FONT_CACHE:
        font = tkinter.font.Font(size=size, weight=weight, slant=slant)
        label = '' # tkinter.Label(font=font)
        FONT_CACHE[key] = (font, label)
    return FONT_CACHE[key][0]
