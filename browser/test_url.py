from url import URL

def test_url():
    url = URL("http://example.com/path/to/resource")
    assert url.scheme == "http"
    assert url.host == "example.com"
    assert url.path == "/path/to/resource"

def test_request():
    url = URL("http://example.com/")
    headers, body = url.request()
    assert headers["content-type"] == "text/html; charset=UTF-8"
    assert headers["content-length"] == str(len(body))
    assert body.startswith("<!doctype html>")
    assert body.endswith("</html>\n")