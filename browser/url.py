class URL:
    def __init__(self, url: str):
        self.scheme, url = url.split("://", maxsplit=1)
        assert self.scheme == "http", f"Unsupported scheme: {self.scheme}"
        self.host, url = url.split("/", maxsplit=1)
        self.path = f"/{url}"
