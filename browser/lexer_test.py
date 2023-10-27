from unittest import TestCase

from .lexer import Tag, Text, lex
from .url import URL


class TestLexer(TestCase):
    def test_Text(self):
        self.assertEqual(Text("abc").__repr__(), 'Text("abc")')

    def test_Tag(self):
        self.assertEqual(Tag("br").__repr__(), 'Tag("br")')
        
    def test_lex(self):
        url = URL("data:text/html,ab<br>c")
        _, body = url.request()
        tokens = lex(body)
        self.assertEqual(tokens, [
            Text("ab"),
            Tag("br"),
            Text("c"),
        ])
