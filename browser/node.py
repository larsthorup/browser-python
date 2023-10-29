from typing import Union


SELF_CLOSING_TAGS = [
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
]

class Node:
    parent: Union["Node", None]
    children: list["Node"]

    def __init__(self, parent: Union["Node", None], children: list["Node"]):
        self.parent = parent
        self.children = children

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, __class__)  # type: ignore[name-defined] # https://github.com/python/mypy/issues/4177
            and self.parent == other.parent
            and self.children == other.children
        )

    def add_child(self, child: "Node") -> None:
        self.children.append(child)
        child.parent = self

    def print_tree(self, level: int = 0) -> None:
        print("  " * level, self)
        for child in self.children:
            child.print_tree(level + 1)


class Text(Node):
    text: str

    def __init__(
        self, text: str, parent: Node | None = None, children: list[Node] | None = None
    ):
        super().__init__(parent, children or [])
        self.text = text

    def __repr__(self) -> str:
        return self.text


class Element(Node):
    tag: str
    attributes: dict[str, str]

    def __init__(
        self,
        tag: str,
        attributes: dict[str, str] | None = None,
        parent: Node | None = None,
        children: list[Node] | None = None,
    ):
        super().__init__(parent, children or [])
        self.tag = tag
        self.attributes = attributes or {}

    def __repr__(self) -> str:
        return f"<{self.tag}>"

def outerHTML(node: Node) -> str:
    if isinstance(node, Text):
        return node.text
    elif isinstance(node, Element):
        if node.tag in SELF_CLOSING_TAGS:
            return f"<{node.tag}>"
        if node.children == []:
            return f"<{node.tag} />"
        else:
            innerHTML = "".join(outerHTML(child) for child in node.children)
            return f"<{node.tag}>{innerHTML}</{node.tag}>"
    else:
        assert False, f"Unexpected node type: {type(node)}"
