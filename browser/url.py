import io
import os
import socket
import ssl


class URL:
    scheme: str
    host: str
    port: int
    pathname: str

    def __init__(self, url: str):
        self.scheme, url = url.split(":", maxsplit=1)
        assert self.scheme in [
            "data",
            "file",
            "http",
            "https",
        ], f"Unsupported scheme: {self.scheme}"
        if self.scheme == "data":
            self.pathname = url
        else:
            _, url = url.split("//", maxsplit=1)
            if self.scheme in ["http", "https"]:
                self.port = 80 if self.scheme == "http" else 443
                self.host, url = url.split("/", maxsplit=1)
                if ":" in self.host:
                    self.host, port = self.host.split(":", 1)
                    self.port = int(port)
                self.pathname = f"/{url}"
            if self.scheme == "file":
                self.pathname = url

    def request(self) -> tuple[dict[str, str], str]:
        resource: socket.socket | io.TextIOWrapper | None
        if self.scheme in ["http", "https"]:
            resource, response, headers = self.get_socket_response()
        elif self.scheme == "file":
            resource, response, headers = self.get_file_response()
        elif self.scheme == "data":
            resource, response, headers = self.get_data_response()
        else:
            assert False, f"Unsupported scheme: {self.scheme}"

        # read body
        # TODO: switch encoding if requested in headers or meta tag
        body = response.read()
        if resource:
            resource.close()

        return headers, body

    def get_socket_response(self) -> tuple[socket.socket, io.TextIOWrapper, dict[str, str]]:
        # connect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)
        s.connect((self.host, self.port))

        # send request
        request = (
            f"GET {self.pathname} HTTP/1.1\r\n"
            f"Host: {self.host}\r\n"
            f"Connection: close\r\n"
            f"User-Agent: github.com/larsthorup/browser-python\r\n"
            f"\r\n"
        )
        s.send(request.encode("utf8"))

        # parse status
        statusline = readline(s)
        _, status, explanation = statusline.split(" ", 2)
        assert status == "200", f"{status}: {explanation}"
        # TODO: handle redirects

        # parse headers
        headers = {}
        while True:
            line = readline(s)
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            headers[header.lower()] = value.strip()
        assert "content-encoding" not in headers, headers

        if headers.get('transfer-encoding') == "chunked":
            body = ""
            bytes = b""
            while True:
                line = readline(s)
                print(line)
                if line == "\r\n" or line == '':
                    break
                length = int(line, 16)
                if length == 0:
                    break
                chunk = read_chunk(s, length)
                bytes += chunk
                crlf = read_chunk(s, 2)
                assert crlf == b"\r\n", crlf
            body = bytes.decode("utf8")
            return s, io.StringIO(body), headers
        else:
            assert "transfer-encoding" not in headers, headers
            response = s.makefile("r", encoding="utf8", newline="\r\n")
            return s, response, headers

    def get_file_response(self) -> tuple[io.TextIOWrapper, io.TextIOWrapper, dict[str, str]]:
        # open file
        path = (
            self.pathname[1:].replace("/", os.sep) if os.name == "nt" else self.pathname
        )
        file = open(path, "r", encoding="utf8")
        return file, file, {}

    def get_data_response(self) -> tuple[None, io.StringIO, dict[str, str]]:
        resource = None
        mime_type, body = self.pathname.split(",", maxsplit=1)
        headers = {"content-type": mime_type}
        file = io.StringIO(body)
        return resource, file, headers

def readline(s: socket.socket) -> str:
    bytes = b""
    while True:
        byte = s.recv(1)
        bytes += byte
        if byte == b"\n":
            break
    return bytes.decode("utf8")

def read_chunk(s: socket.socket, length: int) -> bytes:
    chunk = b""
    while length > 0:
        received = s.recv(length)
        chunk += received
        length -= len(received)
    return chunk
