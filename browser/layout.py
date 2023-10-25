import tkinter
from typing import Literal, TypeAlias

from . import lexer


DisplayItem: TypeAlias = tuple[int, int, str, tkinter.font.Font]

class Layout:
    display_list: list[DisplayItem]
    width: int
    vstep: int
    hstep: int
    cursor_x: int
    cursor_y: int
    weight: Literal['normal', 'bold']
    style: Literal["roman", 'italic']
    size: int
    font: tkinter.font.Font


    def __init__(self, tokens: list[lexer.Token], width: int, size: int):
        self.display_list = []
        self.size = size
        self.vstep = self.size * 2
        self.hstep = int(self.size * 1.5)
        self.cursor_x = self.hstep
        self.cursor_y = self.vstep
        self.weight = "normal"
        self.style = "roman"
        self.update_font(force=True)
        self.width = width
        for tok in tokens:
            self.token(tok)
    
    def token(self, token: lexer.Token):
        if isinstance(token, lexer.Text):
            for word in token.text.split():
                self.word(word)
        elif isinstance(token, lexer.Tag):
            if token.tag == "br":
                self.cursor_y += int(self.font.metrics("linespace") * 1.25)
                self.cursor_x = self.hstep
            elif token.tag in ["i", "em"]:
                self.update_font(style="italic")
            elif token.tag in ["/i", "/em"]:
                self.update_font(style="roman")
            elif token.tag == "b":
                self.update_font(weight="bold")
            elif token.tag == "/b":
                self.update_font(weight="normal")
        else:
            assert False, f"Unknown token type: {token}"

    def word(self, word: str):
        word_width = self.font.measure(word)
        if self.cursor_x + word_width > self.width - self.hstep:
            self.cursor_y += int(self.font.metrics("linespace") * 1.25)
            self.cursor_x = self.hstep
        display_item = (self.cursor_x, self.cursor_y, word, self.font)
        self.display_list.append(display_item)
        self.cursor_x += word_width + self.font.measure(" ")

    def update_font(self, weight=None, style=None, force=False):
        if weight is None:
            weight = self.weight
        if style is None:
            style = self.style
        if weight != self.weight or style != self.style or force:
            self.weight = weight
            self.style = style
            self.font = tkinter.font.Font(
                size=self.size,
                weight=self.weight,
                slant=self.style,
            )