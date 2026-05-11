from ..context import leaf_node


def table(
    data:        list   = None,   # list of dicts or bq.fetch()
    columns:     list   = None,   # list of str column keys
    searchable:  bool   = False,
    sortable:    bool   = False,
    checkable:   bool   = False,
    striped:     bool   = False,
    actions:     list   = None,   # ["edit", "delete", "view"]
    pagination:  bool   = True,
    page_size:   int    = 10,
):
    leaf_node("table", {
        "data":       data,
        "columns":    columns or [],
        "searchable": searchable,
        "sortable":   sortable,
        "checkable":  checkable,
        "striped":    striped,
        "actions":    actions or [],
        "pagination": pagination,
        "page_size":  page_size,
    })


def line_chart(
    data:  list,
    x:     str,
    y:     str,
    label: str = None,
    color: str = None,
):
    leaf_node("line_chart", {
        "data":  data,
        "x":     x,
        "y":     y,
        "label": label,
        "color": color,
    })


def bar_chart(
    data:  list,
    x:     str,
    y:     str,
    label: str = None,
    color: str = None,
):
    leaf_node("bar_chart", {
        "data":  data,
        "x":     x,
        "y":     y,
        "label": label,
        "color": color,
    })


def donut_chart(
    data:  list,
    label: str,
    value: str,
):
    leaf_node("donut_chart", {
        "data":  data,
        "label": label,
        "value": value,
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