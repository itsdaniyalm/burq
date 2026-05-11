from contextlib import contextmanager
from ..context import container_node, leaf_node


@contextmanager
def row(
    gap:    str  = "md",     # none|sm|md|lg
    align:  str  = "center", # start|center|end|stretch
    justify:str  = "start",  # start|center|end|between
    wrap:   bool = True,
    nowrap: bool = False,
):
    classes = ["row"]
    if gap     != "md":     classes.append(f"row--gap-{gap}")
    if align   == "start":  classes.append("row--start")
    if align   == "end":    classes.append("row--end")
    if align   == "stretch":classes.append("row--stretch")
    if justify == "between":classes.append("row--between")
    if justify == "center": classes.append("row--center")
    if justify == "end":    classes.append("row--end-x")
    if nowrap:              classes.append("row--nowrap")

    with container_node("row", {"classes": classes}):
        yield


@contextmanager
def col(
    gap:   str = "md",      # none|sm|md|lg
    align: str = "stretch", # start|center|end|stretch
):
    classes = ["col"]
    if gap   != "md":      classes.append(f"col--gap-{gap}")
    if align == "start":   classes.append("col--start")
    if align == "center":  classes.append("col--center")
    if align == "end":     classes.append("col--end")

    with container_node("col", {"classes": classes}):
        yield


@contextmanager
def grid(
    cols:    int = 12,
    gap:     str = "md",   # none|sm|md|lg
    row_gap: str = None,
    col_gap: str = None,
):
    classes = ["grid"]
    if cols in [1,2,3,4,6]:  classes.append(f"grid--cols-{cols}")
    if gap  != "md":          classes.append(f"grid--gap-{gap}")
    if row_gap:               classes.append(f"grid--row-gap-{row_gap}")
    if col_gap:               classes.append(f"grid--col-gap-{col_gap}")

    with container_node("grid", {"classes": classes}):
        yield


@contextmanager
def span(cols: int = 1):
    classes = [f"span-{cols}"]
    with container_node("span", {"classes": classes}):
        yield


@contextmanager
def container(size: str = "lg"):
    # size: sm|md|lg|xl|full
    classes = ["container"]
    if size != "lg": classes.append(f"container--{size}")
    with container_node("container", {"classes": classes}):
        yield


def divider(size: str = None, vertical: bool = False):
    classes = ["divider"]
    if vertical:  classes.append("divider--vertical")
    if size:      classes.append(f"divider--{size}")
    leaf_node("divider", {"classes": classes})


@contextmanager
def card(
    title:    str  = None,
    subtitle: str  = None,
    variant:  str  = "default",  # default|raised|flat|ghost
    size:     str  = "md",       # sm|md|lg
    footer:   bool = False,
):
    classes = ["card"]
    if variant != "default": classes.append(f"card--{variant}")
    if size    != "md":      classes.append(f"card--{size}")

    with container_node("card", {
        "classes":  classes,
        "title":    title,
        "subtitle": subtitle,
        "footer":   footer,
    }):
        yield