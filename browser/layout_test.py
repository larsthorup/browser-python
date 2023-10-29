from unittest import TestCase
from unittest.mock import patch


from .__mocks__.mockfont import MockFont
from .layout import DocumentLayout
from .parser import HTMLParser
from .url import URL


class TestLayout(TestCase):
    @patch("tkinter.font.Font", new=MockFont)
    def test_Layout(self) -> None:
        url = URL("data:text/html,ab<br>c")
        _, body = url.request()
        root = HTMLParser(body).parse()
        document = DocumentLayout(root, width=100, size=9)
        document.layout()
        display_list = document.display_list
        print(display_list)
        font = display_list[0][3]
        self.assertEqual(display_list, [
            (13, 21, 'ab', font),
            (13, 39, 'c', font),
        ])
