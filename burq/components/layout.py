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
    align: str = "stretch",
    justify: str = "start",
):
    classes = ["col"]
    if gap   != "md":      classes.append(f"col--gap-{gap}")
    if align == "start":   classes.append("col--start")
    if align == "center":  classes.append("col--center")
    if align == "end":     classes.append("col--end")
    if justify == "center":  classes.append("col--justify-center")
    if justify == "end":     classes.append("col--justify-end")
    if justify == "between": classes.append("col--justify-between")


    with container_node("col", {"classes": classes}):
        yield


@contextmanager
def grid(
    cols:    int = 12,
    gap:     str = "md",
    row_gap: str = None,
    col_gap: str = None,
    align:   str = None,
    justify: str = None,
):
    classes = ["grid"]
    if cols in [1,2,3,4,6]:  classes.append(f"grid--cols-{cols}")
    if gap  != "md":          classes.append(f"grid--gap-{gap}")
    if row_gap:               classes.append(f"grid--row-gap-{row_gap}")
    if col_gap:               classes.append(f"grid--col-gap-{col_gap}")
    if align:                 classes.append(f"grid--align-{align}")
    if justify:               classes.append(f"grid--justify-{justify}")
    with container_node("grid", {"classes": classes}):
        yield

@contextmanager
def span(
    cols:  int = 1,
    align: str = None,
):
    classes = [f"span-{cols}"]
    if align: classes.append(f"span--align-{align}")
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

def spacer(size: str = "md"):
    leaf_node("spacer", {"size": size})

@contextmanager
def box(
    background: str  = None,
    border:     bool = False,
    radius:     str  = "lg",
    padding:    str  = "md",
    foreground: str  = None,
    full_width: bool = False,
):
    classes = ["box"]
    bg_map  = {
        "muted":          "var(--muted)",
        "surface":        "var(--surface)",
        "surface_raised": "var(--surface-raised)",
        "background":     "var(--background)",
    }
    fg_map  = {
        "muted":   "var(--muted-foreground)",
        "default": "var(--foreground)",
    }
    pad_map = {"none":"0","sm":"var(--space-3)","md":"var(--space-4)","lg":"var(--space-6)"}
    rad_map = {"none":"0","sm":"var(--radius-sm)","md":"var(--radius-md)","lg":"var(--radius-lg)","xl":"var(--radius-xl)"}
    bg_val  = bg_map.get(background, background)
    fg_val  = fg_map.get(foreground, foreground)
    pad_val = pad_map.get(padding, "var(--space-4)")
    rad_val = rad_map.get(radius, "var(--radius-lg)")
    style = f"padding:{pad_val};border-radius:{rad_val};"
    if bg_val:    style += f"background:{bg_val};"
    if fg_val:    style += f"color:{fg_val};"
    if border:    style += "border:var(--border-width) solid var(--border);"
    if full_width:
        classes.append("box--full")
        style += "width:100%;"
    with container_node("box", {"style": style, "classes": classes}):
        yield