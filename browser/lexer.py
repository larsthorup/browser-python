class Token:
    pass


class Text(Token):
    text: str

    def __init__(self, text: str):
        self.text = text

    def __repr__(self):
        return f'{__class__.__name__ }("{self.text}")'  # type: ignore[name-defined] # https://github.com/python/mypy/issues/4177

    def __eq__(self, other: object):
        return isinstance(other, __class__) and self.text == other.text  # type: ignore[name-defined] # https://github.com/python/mypy/issues/4177


class Tag(Token):
    tag: str

    def __init__(self, tag: str):
        self.tag = tag

    def __repr__(self):
        return f'{__class__.__name__ }("{self.tag}")'  # type: ignore [name-defined] # https://github.com/python/mypy/issues/4177

    def __eq__(self, other: object):
        return isinstance(other, __class__) and self.tag == other.tag  # type: ignore [name-defined] # https://github.com/python/mypy/issues/4177


def lex(body: str):
    out: list[Token] = []
    text = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
            if text:
                out.append(Text(text))
            text = ""
        elif c == ">":
            in_tag = False
            out.append(Tag(text))
            text = ""
        else:
            text += c
    if not in_tag and text:
        out.append(Text(text))
    return out
