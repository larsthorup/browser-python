import tkinter
from typing import Literal, TypeAlias

from . import lexer


DisplayItem: TypeAlias = tuple[int, int, str, tkinter.font.Font]
LineItem: TypeAlias = tuple[int, str, tkinter.font.Font]


class Layout:
    width: int
    vstep: int
    hstep: int
    cursor_x: int
    cursor_y: int
    weight: Literal["normal", "bold"]
    style: Literal["roman", "italic"]
    size: int
    font: tkinter.font.Font
    line: list[LineItem]
    display_list: list[DisplayItem]

    def __init__(self, tokens: list[lexer.Token], width: int, size: int):
        self.line = []
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
        if self.line:
            self.flush()

    def token(self, token: lexer.Token):
        if isinstance(token, lexer.Text):
            for word in token.text.split():
                self.word(word)
        elif isinstance(token, lexer.Tag):
            if token.tag == "br":
                self.flush()
            elif token.tag in ["i", "em"]:
                self.update_font(style="italic")
            elif token.tag in ["/i", "/em"]:
                self.update_font(style="roman")
            elif token.tag == "b":
                self.update_font(weight="bold")
            elif token.tag == "/b":
                self.update_font(weight="normal")
            elif token.tag == "small":
                self.update_font(size=self.size - 2)
            elif token.tag == "/small":
                self.update_font(size=self.size + 2)
            elif token.tag == "big":
                self.update_font(size=self.size + 4)
            elif token.tag == "/big":
                self.update_font(size=self.size - 4)
            elif token.tag == "/p":
                self.flush()
                self.cursor_y += self.vstep
        else:
            assert False, f"Unknown token type: {token}"

    def word(self, word: str):
        word_width = self.font.measure(word)
        if self.cursor_x + word_width > self.width - self.hstep:
            self.flush()
        self.line.append((self.cursor_x, word, self.font))
        self.cursor_x += word_width + self.font.measure(" ")

    def flush(self):
        metrics = [font.metrics() for _, _, font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + int(1.25 * max_ascent)
        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font))
        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline + int(1.25 * max_descent)
        self.cursor_x = self.hstep
        self.line = []

    def update_font(self, weight=None, style=None, size=None, force=False):
        if weight is None:
            weight = self.weight
        if style is None:
            style = self.style
        if size is None:
            size = self.size
        if weight != self.weight or style != self.style or size != self.size or force:
            self.weight = weight
            self.style = style
            self.size = size
            self.font = tkinter.font.Font(
                size=self.size,
                weight=self.weight,
                slant=self.style,
            )
