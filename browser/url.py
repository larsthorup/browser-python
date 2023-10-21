import socket
import ssl

class URL:
    scheme: str
    host: str
    port: int
    path: str

    def __init__(self, url: str):
        self.scheme, url = url.split("://", maxsplit=1)
        assert self.scheme in ["http", "https"], f"Unsupported scheme: {self.scheme}"
        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443
        self.host, url = url.split("/", maxsplit=1)
        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)
        self.path = f"/{url}"

    def request(self):
        # connect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)
        s.connect((self.host, self.port))

        # send request
        request = f"GET {self.path} HTTP/1.0\r\nHost: {self.host}\r\n\r\n"
        s.send(request.encode("utf8"))

        # receive response
        response = s.makefile("r", encoding="utf8", newline="\r\n")

        # parse status
        statusline = response.readline()
        _, status, explanation = statusline.split(" ", 2)
        assert status == "200", f"{status}: {explanation}"

        # parse headers
        headers = {}
        while True:
            line = response.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            headers[header.lower()] = value.strip()
        assert "transfer-encoding" not in headers
        assert "content-encoding" not in headers

        # read body
        body = response.read()
        s.close()

        return headers, body
