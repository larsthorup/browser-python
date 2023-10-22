import sys
from url import URL


def show(body: str):
    # TODO: handle entities
    in_angle = False
    for c in body:
        if c == "<":
            in_angle = True
        elif c == ">":
            in_angle = False
        elif not in_angle:
            print(c, end="")


def load(url):
    headers, body = url.request()
    show(body)


if __name__ == "__main__":
    load(URL(sys.argv[1]))
