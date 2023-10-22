from unittest.mock import call, patch

from browser import Browser
from url import URL


def test_browser_draw():
    with patch("tkinter.Tk") as Tk, patch("tkinter.Canvas") as Canvas:
        browser = Browser()
        canvas = Canvas.return_value
        url = URL("data:text/html,<p>abc</p>")
        browser.load(url)
        canvas.delete.assert_called_once_with("all")
        canvas.create_text.assert_has_calls(
            [
                call(13, 18, text="a"),
                call(26, 18, text="b"),
                call(39, 18, text="c"),
            ]
        )
