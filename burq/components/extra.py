from ..context import leaf_node

def accordion(items: list, multiple: bool = False):
    serialized = []
    for item in items:
        serialized.append({
            "title":   item.get("title", ""),
            "content": item.get("content", ""),
            "open":    item.get("open", False),
        })
    leaf_node("accordion", props={"items": serialized, "multiple": multiple})

def empty_state(title: str, message: str = "", icon: str = "inbox", action: dict = None):
    leaf_node("empty_state", props={
        "title":   title,
        "message": message,
        "icon":    icon,
        "action":  action,
    })

def pagination(total: int, page: int = 1, per_page: int = 10, on_change: str = ""):
    leaf_node("pagination", props={
        "total":     total,
        "page":      page,
        "per_page":  per_page,
        "on_change": on_change,
    })