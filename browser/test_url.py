from url import URL

def test_url():
    url = URL("http://example.com/path/to/resource")
    assert url.scheme == "http"
    assert url.host == "example.com"
    assert url.path == "/path/to/resource"