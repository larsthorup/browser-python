import os
from url import URL


def test_url_http():
    url = URL("http://example.com/path/to/resource")
    assert url.scheme == "http"
    assert url.host == "example.com"
    assert url.port == 80
    assert url.path == "/path/to/resource"


def test_url_https():
    url = URL("https://example.com/path/to/resource")
    assert url.scheme == "https"
    assert url.host == "example.com"
    assert url.port == 443
    assert url.path == "/path/to/resource"


def test_url_localhost():
    url = URL("http://localhost:8000/path/to/resource")
    assert url.scheme == "http"
    assert url.host == "localhost"
    assert url.port == 8000
    assert url.path == "/path/to/resource"


def test_https_request():
    url = URL("https://example.com/")
    headers, body = url.request()
    assert headers["content-type"] == "text/html; charset=UTF-8"
    assert headers["content-length"] == str(len(body))
    assert body.startswith("<!doctype html>")
    assert body.endswith("</html>\n")


def test_file_request():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_url_path = "/" + dir_path.replace(os.sep, "/") if os.name == 'nt' else dir_path
    print(dir_url_path)
    url = URL(f"file://{dir_url_path}/test.html")
    _, body = url.request()
    assert body == "<!doctype html>\n<html>\n\n<body>\n  <p>Test</p>\n</body>\n\n</html>"
