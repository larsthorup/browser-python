import tkinter
import tkinter.font
from unittest.mock import MagicMock, call, patch

from .__mocks__.mockfont import MockFont
from .browser import Browser
from .url import URL


@patch("tkinter.Tk")
@patch("tkinter.Canvas")
@patch("tkinter.font.Font", new=MockFont)
def test_browser_draw(Canvas: MagicMock, Tk: MagicMock) -> None:
    browser = Browser()
    canvas = Canvas.return_value
    url = URL("data:text/html,ab<br>c")
    browser.load(url)
    canvas.delete.assert_called_once_with("all")
    font = canvas.create_text.call_args_list[0][1]["font"]
    canvas.create_text.assert_has_calls(
        [
            call(13, 21, text="ab", font=font, anchor="nw"),
            call(13, 39, text="c", font=font, anchor="nw"),
        ]
    )


@patch("tkinter.Tk")
@patch("tkinter.Canvas")
@patch("tkinter.font.Font", new=MockFont)
def test_browser_scroll(Canvas: MagicMock, Tk: MagicMock) -> None:
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
            call(13, -15, text="c", font=font, anchor="nw"),
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
            call(13, 21, text="ab", font=font, anchor="nw"),
            call(13, 39, text="c", font=font, anchor="nw"),
        ]
    )
