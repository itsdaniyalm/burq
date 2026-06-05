from dataclasses import dataclass, field
from typing import Optional
from ..context import leaf_node


def table(
    data:          list   = None,
    columns:       list   = None,
    column_config: dict   = None,   
    searchable:    bool   = False,
    sortable:      bool   = False,
    checkable:     bool   = False,
    striped:       bool   = False,
    actions:       list   = None,
    pagination:    bool   = True,
    page_size:     int    = 10,
    row_href:      str    = None,
    empty_title:   str    = None,
    empty_message: str    = None,
    empty_icon:    str    = None,
):
    leaf_node("table", {
        "data":          data,
        "columns":       columns or [],
        "column_config": column_config or {},
        "searchable":    searchable,
        "sortable":      sortable,
        "checkable":     checkable,
        "striped":       striped,
        "actions":       actions or [],
        "pagination":    pagination,
        "page_size":     page_size,
        "row_href":      row_href,
        "empty_title":   empty_title or "",
        "empty_message": empty_message or "",
        "empty_icon":    empty_icon or "",
    })

def line_chart(
    data,
    x:      str,
    y,                        # str or list[str]
    title:  str  = None,
    smooth: bool = False,
    height: int  = 300,
):
    leaf_node("line_chart", {
        "data": data, "x": x, "y": y,
        "title": title, "smooth": smooth, "height": height,
        "chart_type": "line",
    })

def area_chart(
    data,
    x:      str,
    y,
    title:  str  = None,
    smooth: bool = True,
    height: int  = 300,
):
    leaf_node("area_chart", {
        "data": data, "x": x, "y": y,
        "title": title, "smooth": smooth, "height": height,
        "chart_type": "area",
    })

def bar_chart(
    data,
    x:       str,
    y,
    title:   str  = None,
    stacked: bool = False,
    height:  int  = 300,
):
    leaf_node("bar_chart", {
        "data": data, "x": x, "y": y,
        "title": title, "stacked": stacked, "height": height,
        "chart_type": "bar",
    })

def donut_chart(
    data,
    label:  str,
    value:  str,
    title:  str = None,
    height: int = 300,
):
    leaf_node("donut_chart", {
        "data": data, "label": label, "value": value,
        "title": title, "height": height,
        "chart_type": "donut",
    })


# ── API HELPERS ──

def fetch(method: str, endpoint: str, data: dict = None) -> dict:
    """
    Represents an API call in the component tree.
    At compile time this becomes a fetch() JS call.
    At runtime returns a placeholder for type checking.
    """
    return {
        "__burq_fetch__": True,
        "method":         method,
        "endpoint":       endpoint,
        "data":           data,
    }


def post(endpoint: str, data: dict = None) -> str:
    """Shorthand for fetch POST — compiles to JS fetch call."""
    return {
        "__burq_fetch__": True,
        "method":         "POST",
        "endpoint":       endpoint,
        "data":           data,
    }

@dataclass
class BadgeColumn:
    variant_map: dict = field(default_factory=dict)
    # e.g. {"lead": "default", "won": "success"}


@dataclass
class AvatarColumn:
    initials_key: str = "name"
    sub_key:      str = None   # e.g. "email"


@dataclass
class CurrencyColumn:
    prefix:   str = "$"
    decimals: int = 0


@dataclass
class DateColumn:
    format: str = "%b %d, %Y"


@dataclass
class BoolColumn:
    true_label:  str = "Yes"
    false_label: str = "No"
    true_variant:  str = "success"
    false_variant: str = "danger"


@dataclass
class TextColumn:
    muted: bool = False


@dataclass
class TableAction:
    label:   str  = ""
    icon:    str  = None
    variant: str  = "default"   # default|danger|warning
    onclick: str  = ""          # JS expression; {field} tokens substituted from row