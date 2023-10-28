from unittest import TestCase

from .node import outerHTML
from .parser import HTMLParser
from .url import URL


class TestHTMLParser(TestCase):
    def test_parse(self):
        url = URL("data:text/html,ab<br>c")
        _, body = url.request()
        root = HTMLParser(body).parse()
        self.assertEqual(outerHTML(root), '<html><body>ab<br>c</body></html>')