import tkinter


FONT_CACHE = {}


def get_font(size, weight, slant):
    key = (size, weight, slant)
    if key not in FONT_CACHE:
        font = tkinter.font.Font(size=size, weight=weight, slant=slant)
        label = '' # tkinter.Label(font=font)
        FONT_CACHE[key] = (font, label)
    return FONT_CACHE[key][0]
