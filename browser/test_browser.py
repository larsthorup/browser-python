import tkinter
from unittest.mock import call, patch

from browser import Browser
from url import URL


def test_browser_draw():
    with patch("tkinter.Tk"), patch("tkinter.Canvas") as Canvas, patch("tkinter.font.Font") as Font:
        browser = Browser()
        canvas = Canvas.return_value
        font = Font.return_value
        url = URL("data:text/html,<b>ab</b>\nc")
        browser.load(url)
        canvas.delete.assert_called_once_with("all")
        canvas.create_text.assert_has_calls(
            [
                call(13, 18, text="a", font=font, anchor="nw"),
                call(26, 18, text="b", font=font, anchor="nw"),
                call(13, 45, text="c", font=font, anchor="nw"),
            ]
        )


def test_browser_scroll():
    with patch("tkinter.Tk"), patch("tkinter.Canvas") as Canvas, patch("tkinter.font.Font") as Font:
        browser = Browser()
        canvas = Canvas.return_value
        font = Font.return_value
        url = URL("data:text/html,<b>ab</b>\nc")
        browser.load(url)

        # when scrolling down
        canvas.delete.reset_mock()
        canvas.create_text.reset_mock()
        browser.handle_key_down(tkinter.Event())

        # then only the last line is drawn
        canvas.delete.assert_called_once_with("all")
        canvas.create_text.assert_has_calls(
            [
                call(13, -9, text="c", font=font, anchor="nw"),
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
                call(13, 18, text="a", font=font, anchor="nw"),
                call(26, 18, text="b", font=font, anchor="nw"),
                call(13, 45, text="c", font=font, anchor="nw"),
            ]
        )
