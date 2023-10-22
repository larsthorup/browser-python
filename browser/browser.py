import os
import tkinter
import tkinter.font

from url import URL

SCROLL_STEP = 54


class Browser:
    width: int
    height: int
    window: tkinter.Tk
    canvas: tkinter.Canvas
    scroll: int
    font_size: int
    document_text: str
    display_list: list[tuple[int, int, str]]

    def __init__(self):
        self.width = 800
        self.height = 600
        self.font_size = 9
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.pack(fill="both", expand=True)
        self.scroll = 0
        self.display_list = []
        self.window.bind("<Down>", self.handle_key_down)
        self.window.bind("<Up>", self.handle_key_up)
        self.window.bind("<MouseWheel>", self.handle_mouse_wheel)
        self.window.bind("<Configure>", self.handle_window_resize)
        self.window.bind("<Control-plus>", self.handle_control_plus)
        self.window.bind("<Control-minus>", self.handle_control_minus)

    def load(self, url: URL):
        _, self.document_text = url.request()
        self.render()

    def render(self):
        text = lex(self.document_text)
        self.vstep = self.font_size * 2
        self.hstep = int(self.font_size * 1.5)
        self.paragraph_step = int(1.5 * self.vstep)
        self.display_list = self.layout(text)
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        font = tkinter.font.Font(size=self.font_size)
        for x, y, c in self.display_list:
            if y > self.scroll + self.height:
                # skip drawing text below the bottom of the window
                continue
            if y + self.vstep < self.scroll:
                # skip drawing text above the top of the window
                continue
            self.canvas.create_text(x, y - self.scroll, text=c, font=font, anchor="nw")

    def handle_key_down(self, _: tkinter.Event):
        self.scroll_to(self.scroll + SCROLL_STEP)

    def handle_key_up(self, _: tkinter.Event):
        self.scroll_to(self.scroll - SCROLL_STEP)

    def handle_mouse_wheel(self, event: tkinter.Event):
        assert os.name == "nt", f"Unsupported mouse wheel event on {os.name}"
        self.scroll_to(self.scroll - event.delta)

    def handle_window_resize(self, event: tkinter.Event):
        self.width = event.width
        self.height = event.height
        self.render()

    def handle_control_plus(self, _: tkinter.Event):
        self.zoom_to(self.font_size + 2)

    def handle_control_minus(self, _: tkinter.Event):
        self.zoom_to(self.font_size - 2)

    def scroll_to(self, y: int):
        self.scroll = y
        if self.scroll < 0:
            self.scroll = 0
        self.draw()

    def zoom_to(self, font_size: int):
        self.font_size = font_size
        self.render()

    def layout(self, text: str):
        display_list: list[tuple[int, int, str]] = []
        cursor_x, cursor_y = self.hstep, self.vstep
        for c in text:
            if c == "\n":
                cursor_y += self.paragraph_step
                cursor_x = self.hstep
            else:
                display_list.append((cursor_x, cursor_y, c))
                cursor_x += self.hstep
                if cursor_x >= self.width - self.hstep:
                    cursor_y += self.vstep
                    cursor_x = self.hstep
        return display_list


def lex(body: str):
    # TODO: handle entities
    text = ""
    in_angle = False
    for c in body:
        if c == "<":
            in_angle = True
        elif c == ">":
            in_angle = False
        elif not in_angle:
            text += c
    return text
