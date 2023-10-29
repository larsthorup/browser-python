import io
import os
import pytest
from unittest.mock import patch

from .url import URL


def test_url_http() -> None:
    url = URL("http://example.com/path/to/resource")
    assert url.scheme == "http"
    assert url.host == "example.com"
    assert url.port == 80
    assert url.pathname == "/path/to/resource"


def test_url_https() -> None:
    url = URL("https://example.com/path/to/resource")
    assert url.scheme == "https"
    assert url.host == "example.com"
    assert url.port == 443
    assert url.pathname == "/path/to/resource"


def test_url_localhost() -> None:
    url = URL("http://localhost:8000/path/to/resource")
    assert url.scheme == "http"
    assert url.host == "localhost"
    assert url.port == 8000
    assert url.pathname == "/path/to/resource"


def test_url_file() -> None:
    url = URL("file:///path/to/resource")
    assert url.scheme == "file"
    assert url.pathname == "/path/to/resource"

def test_url_data() -> None:
    url = URL("data:text/html,Hello World!")
    assert url.scheme == "data"
    assert url.pathname == "text/html,Hello World!"


def test_data_request() -> None:
    url = URL("data:text/html,Hello World!")
    headers, body = url.request()
    assert headers == {"content-type": "text/html"}
    assert body == "Hello World!"


def test_request() -> None:
    with patch("socket.socket") as socket:
        s = socket.return_value

        # given that server responds
        s.makefile.return_value = io.StringIO(
            "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello World!"
        )

        # when requesting
        url = URL("http://mockserver/")
        headers, body = url.request()

        # then connection was made
        s.connect.assert_called_once_with(("mockserver", 80))
        
        # then request was sent
        s.send.assert_called_once_with(
            b"GET / HTTP/1.1\r\nHost: mockserver\r\nConnection: close\r\nUser-Agent: github.com/larsthorup/browser-python\r\n\r\n"
        )

        # then headers and body is returned
        assert headers == {"content-type": "text/html"}
        assert body == "Hello World!"


@pytest.mark.skipif(
    not os.environ.get("INTEGRATION_TESTS", False), reason="not INTEGRATION_TESTS"
)
def test_https_request() -> None:
    url = URL("https://example.com/")
    headers, body = url.request()
    assert headers["content-type"] == "text/html; charset=UTF-8"
    assert headers["content-length"] == str(len(body))
    assert body.startswith("<!doctype html>")
    assert body.endswith("</html>\n")


@pytest.mark.skipif(
    not os.environ.get("INTEGRATION_TESTS", False), reason="not INTEGRATION_TESTS"
)
def test_integration_file_request() -> None:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_url_path = "/" + dir_path.replace(os.sep, "/") if os.name == "nt" else dir_path
    url = URL(f"file://{dir_url_path}/test.html")
    _, body = url.request()
    assert (
        body == "<!doctype html>\n<html>\n\n<body>\n  <p>Test</p>\n</body>\n\n</html>"
    )
