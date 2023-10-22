import os
from socket import socket as Socket, AF_INET, SOCK_STREAM
import ssl


class URL:
    scheme: str
    host: str
    port: int
    path: str

    def __init__(self, url: str):
        self.scheme, url = url.split("://", maxsplit=1)
        assert self.scheme in [
            "http",
            "https",
            "file",
        ], f"Unsupported scheme: {self.scheme}"
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
        if self.scheme in ["http", "https"]:
            resource, response, headers = self.get_socket_response()

        if self.scheme == "file":
            headers: dict[str, str] = {}
            resource, response = self.get_file_response()

        # TODO: handle data: schema

        # read body
        # TODO: switch encoding if requested in headers or meta tag
        body = response.read()
        if resource:
            resource.close()

        return headers, body

    def get_socket_response(self):
        # connect
        socket = Socket(AF_INET, SOCK_STREAM)
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            socket = ctx.wrap_socket(socket, server_hostname=self.host)
        socket.connect((self.host, self.port))

        # send request
        request = (
            f"GET {self.path} HTTP/1.1\r\n"
            f"Host: {self.host}\r\n"
            f"Connection: close\r\n"
            f"User-Agent: github.com/larsthorup/browser-python\r\n"
            f"\r\n"
        )
        socket.send(request.encode("utf8"))

        # receive response
        response = socket.makefile("r", encoding="utf8", newline="\r\n")

        # parse status
        statusline = response.readline()
        _, status, explanation = statusline.split(" ", 2)
        assert status == "200", f"{status}: {explanation}"
        # TODO: handle redirects

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

        return socket, response, headers

    def get_file_response(self):
        # open file
        path = self.path[1:].replace("/", os.sep) if os.name == "nt" else self.path
        file = open(path, "r", encoding="utf8")
        return file, file
