import tkinter
from unittest.mock import call, patch

from browser import Browser
from url import URL


def test_browser_draw():
    with patch("tkinter.Tk") as Tk, patch("tkinter.Canvas") as Canvas:
        browser = Browser()
        canvas = Canvas.return_value
        url = URL("data:text/html,<b>ab</b>\nc")
        browser.load(url)
        canvas.delete.assert_called_once_with("all")
        canvas.create_text.assert_has_calls(
            [
                call(13, 18, text="a"),
                call(26, 18, text="b"),
                call(13, 45, text="c"),
            ]
        )


def test_browser_scroll():
    with patch("tkinter.Tk") as Tk, patch("tkinter.Canvas") as Canvas:
        browser = Browser()
        canvas = Canvas.return_value
        url = URL("data:text/html,<b>ab</b>\nc")
        browser.load(url)

        # when scrolling down
        canvas.delete.reset_mock()
        canvas.create_text.reset_mock()
        browser.scroll_down(tkinter.Event())

        # then only the last line is drawn
        canvas.delete.assert_called_once_with("all")
        canvas.create_text.assert_has_calls(
            [
                call(13, -9, text="c"),
            ]
        )

        # when scrolling back up
        canvas.delete.reset_mock()
        canvas.create_text.reset_mock()
        browser.scroll_up(tkinter.Event())

        # then all lines are drawn
        canvas.delete.assert_called_once_with("all")
        canvas.create_text.assert_has_calls(
            [
                call(13, 18, text="a"),
                call(26, 18, text="b"),
                call(13, 45, text="c"),
            ]
        )
