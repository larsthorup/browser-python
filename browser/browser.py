import tkinter

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
PARAGRAPH_STEP = int(1.5 * VSTEP)
SCROLL_STEP = 3 * VSTEP


class Browser:
    window: tkinter.Tk
    canvas: tkinter.Canvas
    scroll: int
    display_list: list[tuple[int, int, str]]

    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.scroll = 0
        self.display_list = []
        self.window.bind("<Down>", self.scroll_down)
        self.window.bind("<Up>", self.scroll_up)
    
    def load(self, url):
        _, body = url.request()
        text = lex(body)
        self.display_list = layout(text)
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            if y > self.scroll + HEIGHT: 
                # skip drawing text below the bottom of the window
                continue
            if y + VSTEP < self.scroll: 
                # skip drawing text above the top of the window
                continue
            self.canvas.create_text(x, y - self.scroll, text=c)

    def scroll_down(self, _: tkinter.Event):
        self.scroll += SCROLL_STEP
        self.draw()

    def scroll_up(self, _: tkinter.Event):
        self.scroll -= SCROLL_STEP
        if self.scroll < 0:
            self.scroll = 0
        self.draw()

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


def layout(text: str):
    display_list: list[tuple[int, int, str]] = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
        if (c == "\n"):
            cursor_y += PARAGRAPH_STEP
            cursor_x = HSTEP
        else:
            display_list.append((cursor_x, cursor_y, c))
            cursor_x += HSTEP
            if cursor_x >= WIDTH - HSTEP:
                cursor_y += VSTEP
                cursor_x = HSTEP
    return display_list
