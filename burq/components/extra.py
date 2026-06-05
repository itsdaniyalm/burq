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

def contact_profile(endpoint: str):
    leaf_node("contact_profile", props={"endpoint": endpoint})

def markdown(content: str):
    leaf_node("markdown", props={"content": content})

def code_block(content: str, language: str = "python", filename: str = None, line_numbers: bool = True):
    leaf_node("code_block", props={
        "content":      content,
        "language":     language,
        "filename":     filename,
        "line_numbers": line_numbers,
    })

def rich_text(
    name:        str,
    label:       str  = None,
    placeholder: str  = None,
    value:       str  = None,
):
    leaf_node("rich_text", props={
        "name":        name,
        "label":       label,
        "placeholder": placeholder or "Write something...",
        "value":       value,
    })

def script(code: str):
    """Emit a raw <script> block into the page output."""
    leaf_node("script", props={"code": code})