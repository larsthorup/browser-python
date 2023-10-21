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


def test_request():
    url = URL("https://example.com/")
    headers, body = url.request()
    assert headers["content-type"] == "text/html; charset=UTF-8"
    assert headers["content-length"] == str(len(body))
    assert body.startswith("<!doctype html>")
    assert body.endswith("</html>\n")
