import socket

class URL:
    
    def __init__(self, url: str):
        self.scheme, url = url.split("://", maxsplit=1)
        assert self.scheme == "http", f"Unsupported scheme: {self.scheme}"
        self.host, url = url.split("/", maxsplit=1)
        self.path = f"/{url}"

    def request(self):
        # connect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, 80))

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
            if line == "\r\n": break
            header, value = line.split(":", 1)
            headers[header.lower()] = value.strip()
        assert "transfer-encoding" not in headers
        assert "content-encoding" not in headers

        # read body
        body = response.read()
        s.close()

        return headers, body