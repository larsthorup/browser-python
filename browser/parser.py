from .node import SELF_CLOSING_TAGS, Element, Node, Text

HEAD_TAGS = [
    "base", "basefont", "bgsound", "noscript",
    "link", "meta", "title", "style", "script",
]

class HTMLParser:
    body: str
    unfinished: list[Element]

    def __init__(self, body: str):
        self.body = body
        self.unfinished = []

    def parse(self):
        text = ""
        in_tag = False
        for c in self.body:
            if c == "<":
                in_tag = True
                if text:
                    self.add_text(text)
                text = ""
            elif c == ">":
                in_tag = False
                self.add_tag(text)
                text = ""
            else:
                text += c
        if not in_tag and text:
            self.add_text(text)
        return self.finish()

    def add_text(self, text: str):
        if text.isspace():
            # ignore whitespace only text nodes for brevity
            return
        self.implicit_tags(None)
        if not self.unfinished:
            # handle any text before the first tag
            self.add_tag("html")
        # append this text node to the closest unfinished element
        parent = self.unfinished[-1]
        node = Text(text, parent)
        parent.add_child(node)

    def add_tag(self, text: str):
        tag, attributes = self.get_attributes(text)
        if tag.startswith("!"):
            # ignore comments and doctypes
            return
        self.implicit_tags(tag)
        if tag.startswith("/"):
            if len(self.unfinished) == 1:
                # ignore closing tags for the root element
                return
            # close the closest unfinished element and append it to the next closest unfinished element
            node = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.add_child(node)
        elif tag in SELF_CLOSING_TAGS:
            # create a new element and append it to the closest unfinished element
            parent = self.unfinished[-1]
            node = Element(tag, attributes, parent)
            parent.children.append(node)
        else:
            # create a new element and append it to the closest unfinished element, if any
            parent_optional = self.unfinished[-1] if self.unfinished else None
            node = Element(tag, attributes, parent_optional)
            self.unfinished.append(node)

    def finish(self):
        if len(self.unfinished) == 0:
            # handle empty documents
            self.add_tag("html")
        while len(self.unfinished) > 1:
            # close any remaining unfinished elements and append them to the next closest unfinished element
            node = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.add_child(node)
        return self.unfinished.pop()
    
    def get_attributes(self, text: str):
        parts = text.split()
        tag = parts[0].lower()
        attributes = {}
        for attrpair in parts[1:]:
            if "=" in attrpair:
                key, value = attrpair.split("=", 1)
                if len(value) > 2 and value[0] in ["'", '"'] and value[0] == value[-1]:
                    value = value[1:-1]
                attributes[key.lower()] = value
            else:
                attributes[attrpair.lower()] = ""
        return tag, attributes
    
    def implicit_tags(self, tag: str | None):
        while True:
            open_tags = [node.tag for node in self.unfinished]
            if open_tags == [] and tag != "html":
                self.add_tag("html")
            elif open_tags == ["html"] and tag not in ["head", "body", "/html"]:
                if tag in HEAD_TAGS:
                    self.add_tag("head")
                else:
                    self.add_tag("body")
            elif open_tags == ["html", "head"] and tag not in ["/head"] + HEAD_TAGS:
                self.add_tag("/head")
            else:
                break