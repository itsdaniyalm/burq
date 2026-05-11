from ..context import container_node, leaf_node
from contextlib import contextmanager


@contextmanager
def tabs(
    items:   list[str],
    variant: str = "default",  # default|pills|card
    icons:   list[str] = None,
    badges:  list[str] = None,
):
    with container_node("tabs", {
        "items":   items,
        "variant": variant,
        "icons":   icons or [],
        "badges":  badges or [],
    }):
        yield


@contextmanager
def tab(label: str):
    with container_node("tab", {"label": label}):
        yield


def dropdown(
    trigger,          # bq.button() or any component
    items:   list,    # list of DropdownItem / DropdownDivider
    align:   str = "right",  # right|left
):
    leaf_node("dropdown", {
        "trigger": trigger,
        "items":   items,
        "align":   align,
    })


class DropdownItem:
    def __init__(
        self,
        label:    str,
        icon:     str  = None,
        danger:   bool = False,
        disabled: bool = False,
        onclick:  str  = None,
    ):
        self.label    = label
        self.icon     = icon
        self.danger   = danger
        self.disabled = disabled
        self.onclick  = onclick


class DropdownDivider:
    pass


class DropdownLabel:
    def __init__(self, text: str):
        self.text = text


def breadcrumb(
    items:     list,
    separator: str = "chevron",  # chevron|slash
):
    leaf_node("breadcrumb", {
        "items":     items,
        "separator": separator,
    })


class NavItem:
    def __init__(
        self,
        label: str,
        icon:  str = "",
        href:  str = "#",
    ):
        self.label = label
        self.icon  = icon
        self.href  = href


# ── API HELPERS ──

def navigate(href: str) -> str:
    return f"burq.navigate('{href}')"


def reload() -> str:
    return "burq.reload()"