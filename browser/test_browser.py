import tkinter
import tkinter.font
from unittest.mock import call, patch

from browser import Browser
from url import URL

class MockFont:
    def __init__(self, *args, **kwargs):
        pass

    def measure(self, text):
        return len(text) * 10
    
    def metrics(self, metric):
        assert metric == "linespace"
        return 18


def test_browser_draw():
    with patch("tkinter.Tk"), patch("tkinter.Canvas") as Canvas, patch("tkinter.font.Font", new=MockFont):
        browser = Browser()
        canvas = Canvas.return_value
        url = URL("data:text/html,ab<br>c")
        browser.load(url)
        canvas.delete.assert_called_once_with("all")
        font = canvas.create_text.call_args_list[0][1]["font"]
        canvas.create_text.assert_has_calls(
            [
                call(13, 18, text="ab", font=font, anchor="nw"),
                call(13, 40, text="c", font=font, anchor="nw"),
            ]
        )


def test_browser_scroll():
    with patch("tkinter.Tk"), patch("tkinter.Canvas") as Canvas, patch("tkinter.font.Font", new=MockFont):
        browser = Browser()
        canvas = Canvas.return_value
        url = URL("data:text/html,ab<br>c")
        browser.load(url)
        font = canvas.create_text.call_args_list[0][1]["font"]

        # when scrolling down
        canvas.delete.reset_mock()
        canvas.create_text.reset_mock()
        browser.handle_key_down(tkinter.Event())

        # then only the last line is drawn
        canvas.delete.assert_called_once_with("all")
        canvas.create_text.assert_has_calls(
            [
                call(13, -14, text="c", font=font, anchor="nw"),
            ]
        )

        # when scrolling back up
        canvas.delete.reset_mock()
        canvas.create_text.reset_mock()
        browser.handle_key_up(tkinter.Event())

        # then all lines are drawn
        canvas.delete.assert_called_once_with("all")
        canvas.create_text.assert_has_calls(
            [
                call(13, 18, text="ab", font=font, anchor="nw"),
                call(13, 40, text="c", font=font, anchor="nw"),
            ]
        )
