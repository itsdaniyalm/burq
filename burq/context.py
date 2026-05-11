from contextlib import contextmanager
from typing import Any

class RenderContext:
    """
    Global render context. Tracks the current component tree
    as Python UI code executes top to bottom.
    """
    def __init__(self):
        self._stack: list[list] = []   # stack of child lists
        self._root:  list       = []   # top level nodes

    def push(self, node: dict):
        """Add a node to the current parent."""
        target = self._stack[-1] if self._stack else self._root
        target.append(node)

    def open(self, node: dict) -> list:
        """Open a container node — push onto stack."""
        children = []
        node["children"] = children
        self.push(node)
        self._stack.append(children)
        return children

    def close(self):
        """Close the current container node."""
        if self._stack:
            self._stack.pop()

    def collect(self) -> list:
        """Return the full tree and reset."""
        tree = self._root
        self._root = []
        self._stack = []
        return tree

    def reset(self):
        self._root = []
        self._stack = []


# Global singleton — one context per compile run
_ctx = RenderContext()

def get_context() -> RenderContext:
    return _ctx

def reset_context():
    _ctx.reset()

@contextmanager
def container_node(tag: str, props: dict[str, Any] = None):
    """
    Context manager for any container component.
    Usage:
        with container_node("row", {"gap": "md"}):
            leaf_node("text", {"content": "Hello"})
    """
    node = {"tag": tag, "props": props or {}}
    get_context().open(node)
    try:
        yield node
    finally:
        get_context().close()

def leaf_node(tag: str, props: dict[str, Any] = None):
    """
    Add a leaf component to the current context.
    Usage:
        leaf_node("metric", {"label": "Revenue", "value": "$84k"})
    """
    node = {"tag": tag, "props": props or {}, "children": []}
    get_context().push(node)
    return node