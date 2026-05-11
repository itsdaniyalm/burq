from ..context import container_node, leaf_node
from contextlib import contextmanager


def title(text: str):
    leaf_node("title", {"text": text})


def heading(text: str):
    leaf_node("heading", {"text": text})


def text(content: str, muted: bool = False):
    leaf_node("text", {"content": content, "muted": muted})


def metric(
    label:     str,
    value:     str,
    trend:     str  = None,
    trend_dir: str  = None,   # up|down|flat
    icon:      str  = None,
    variant:   str  = "default",  # default|accent|ghost
):
    leaf_node("metric", {
        "label":     label,
        "value":     value,
        "trend":     trend,
        "trend_dir": trend_dir,
        "icon":      icon,
        "variant":   variant,
    })


def badge(
    text:    str,
    variant: str = "default",  # default|accent|success|warning|danger|info
    size:    str = "md",       # sm|md|lg
    dot:     bool = False,
):
    leaf_node("badge", {
        "text":    text,
        "variant": variant,
        "size":    size,
        "dot":     dot,
    })


def avatar(
    initials: str  = "",
    src:      str  = None,
    size:     str  = "md",     # xs|sm|md|lg|xl
    variant:  str  = "square", # square|round
    status:   str  = None,     # online|offline|away
    color:    str  = "accent", # accent|gray
):
    leaf_node("avatar", {
        "initials": initials,
        "src":      src,
        "size":     size,
        "variant":  variant,
        "status":   status,
        "color":    color,
    })


def avatar_group(
    avatars:  list,
    overflow: int = 0,
):
    leaf_node("avatar_group", {
        "avatars":  avatars,
        "overflow": overflow,
    })


def progress(
    label:    str  = None,
    value:    int  = 0,
    variant:  str  = "default",  # default|success|warning|danger
    size:     str  = "md",       # sm|md|lg
    striped:  bool = False,
    animated: bool = False,
):
    leaf_node("progress", {
        "label":    label,
        "value":    value,
        "variant":  variant,
        "size":     size,
        "striped":  striped,
        "animated": animated,
    })


def skeleton(
    variant: str = "text",  # text|text-sm|text-lg|avatar-sm|avatar-md|avatar-lg|button|rect
    width:   str = None,
    height:  str = None,
):
    leaf_node("skeleton", {
        "variant": variant,
        "width":   width,
        "height":  height,
    })


def breadcrumb(
    items:     list,           # list of BreadcrumbItem
    separator: str = "chevron" # chevron|slash
):
    leaf_node("breadcrumb", {
        "items":     items,
        "separator": separator,
    })


class BreadcrumbItem:
    def __init__(self, label: str, href: str = None):
        self.label = label
        self.href  = href

def spinner(size: str = "md", color: str = "accent"):
    # size: sm|md|lg
    # color: accent|muted|white
    leaf_node("spinner", {
        "size":  size,
        "color": color,
    })