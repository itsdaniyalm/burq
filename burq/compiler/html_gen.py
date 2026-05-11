from typing import Any
import json as _json

def classes(*args) -> str:
    """Join class lists into a string."""
    result = []
    for a in args:
        if isinstance(a, list):
            result.extend(a)
        elif isinstance(a, str) and a:
            result.append(a)
    return " ".join(result)


def icon(name: str, cls: str = "") -> str:
    if not name:
        return ""
    return f'<i data-lucide="{name}" class="{cls}"></i>'


# ── NODE RENDERERS ──

def render_node(node: dict, app=None) -> str:
    tag = node.get("tag")
    props = node.get("props", {})
    children = node.get("children", [])
    rendered_children = "\n".join(render_node(c, app) for c in children)

    renderers = {
        "title":       render_title,
        "heading":     render_heading,
        "text":        render_text,
        "row":         render_row,
        "col":         render_col,
        "grid":        render_grid,
        "span":        render_span,
        "container":   render_container,
        "divider":     render_divider,
        "card":        render_card,
        "metric":      render_metric,
        "badge":       render_badge,
        "avatar":      render_avatar,
        "avatar_group":render_avatar_group,
        "progress":    render_progress,
        "skeleton":    render_skeleton,
        "spinner":     render_spinner,
        "breadcrumb":  render_breadcrumb,
        "table":       render_table,
        "input":       render_input,
        "textarea":    render_textarea,
        "select":      render_select,
        "toggle":      render_toggle,
        "checkbox":    render_checkbox,
        "radio":       render_radio,
        "button":      render_button,
        "modal":       render_modal,
        "modal_body":  render_modal_body,
        "modal_footer":render_modal_footer,
        "alert":       render_alert,
        "tabs":        render_tabs,
        "tab":         render_tab,
        "dropdown":    render_dropdown,
    }

    renderer = renderers.get(tag)
    if renderer:
        return renderer(props, rendered_children)
    return f"<!-- unknown tag: {tag} -->"


def render_tree(tree: list, app=None) -> str:
    return "\n".join(render_node(node, app) for node in tree)


# ── LAYOUT ──

def render_row(props, children):
    cls = classes(props.get("classes", ["row"]))
    return f'<div class="{cls}">{children}</div>'


def render_col(props, children):
    cls = classes(props.get("classes", ["col"]))
    return f'<div class="{cls}">{children}</div>'


def render_grid(props, children):
    cls = classes(props.get("classes", ["grid"]))
    return f'<div class="{cls}">{children}</div>'


def render_span(props, children):
    cls = classes(props.get("classes", ["span-1"]))
    return f'<div class="{cls}">{children}</div>'


def render_container(props, children):
    cls = classes(props.get("classes", ["container"]))
    return f'<div class="{cls}">{children}</div>'


def render_divider(props, children):
    cls = classes(props.get("classes", ["divider"]))
    return f'<hr class="{cls}" />'


def render_card(props, children):
    cls      = classes(props.get("classes", ["card"]))
    title    = props.get("title")
    subtitle = props.get("subtitle")

    header = ""
    if title:
        sub_html = f'<div class="card__subtitle">{subtitle}</div>' if subtitle else ""
        header = f'''
        <div class="card__header">
            <div>
                <div class="card__title">{title}</div>
                {sub_html}
            </div>
        </div>'''

    return f'''
<div class="{cls}">
    {header}
    <div class="card__body">
        {children}
    </div>
</div>'''


# ── DISPLAY ──

def render_title(props, children):
    return f'<h1 class="page-title">{props.get("text","")}</h1>'


def render_heading(props, children):
    return f'<h2 class="page-heading">{props.get("text","")}</h2>'


def render_text(props, children):
    cls = "muted-text" if props.get("muted") else "body-text"
    return f'<p class="{cls}">{props.get("content","")}</p>'


def render_metric(props, children):
    label     = props.get("label", "")
    value     = props.get("value", "")
    trend     = props.get("trend")
    trend_dir = props.get("trend_dir")
    ico       = props.get("icon")
    variant   = props.get("variant", "default")

    cls = "metric-card"
    if variant != "default":
        cls += f" metric-card--{variant}"

    icon_html = f'<i data-lucide="{ico}" class="metric-card__icon"></i>' if ico else ""

    trend_html = ""
    if trend and trend_dir:
        trend_icons = {"up": "arrow-up", "down": "arrow-down", "flat": "minus"}
        trend_cls   = f"metric-card__trend metric-card__trend--{trend_dir}" if trend_dir in ["up","down"] else "metric-card__trend"
        trend_html  = f'''
        <div class="{trend_cls}">
            <i data-lucide="{trend_icons.get(trend_dir,'minus')}" class="metric-card__trend-icon"></i>
            {trend}
        </div>'''

    return f'''
<div class="{cls}">
    <div class="metric-card__header">
        <span class="metric-card__label">{label}</span>
        {icon_html}
    </div>
    <div class="metric-card__value">{value}</div>
    {trend_html}
</div>'''


def render_badge(props, children):
    variant = props.get("variant", "default")
    size    = props.get("size", "md")
    text    = props.get("text", "")
    dot     = props.get("dot", False)

    cls = f"badge badge--{variant}"
    if size != "md": cls += f" badge--{size}"

    dot_html = '<span class="badge__dot"></span>' if dot else ""
    return f'<span class="{cls}">{dot_html}{text}</span>'


def render_avatar(props, children):
    initials = props.get("initials", "")
    src      = props.get("src")
    size     = props.get("size", "md")
    variant  = props.get("variant", "square")
    status   = props.get("status")
    color    = props.get("color", "accent")

    cls = f"avatar avatar--{size}"
    if variant == "round": cls += " avatar--round"
    if color != "accent":  cls += f" avatar--{color}"

    inner = f'<img src="{src}" alt="{initials}" />' if src else initials

    status_html = ""
    if status:
        status_html = f'<span class="avatar__status avatar__status--{status}"></span>'
        return f'''
<div style="position:relative;display:inline-flex;">
    <div class="{cls}">{inner}</div>
    {status_html}
</div>'''

    return f'<div class="{cls}">{inner}</div>'


def render_avatar_group(props, children):
    avatars  = props.get("avatars", [])
    overflow = props.get("overflow", 0)

    items = ""
    for av in avatars:
        items += render_avatar(av, "")

    overflow_html = ""
    if overflow:
        overflow_html = f'<div class="avatar-group__overflow">+{overflow}</div>'

    return f'<div class="avatar-group">{items}{overflow_html}</div>'


def render_progress(props, children):
    label    = props.get("label")
    value    = props.get("value", 0)
    variant  = props.get("variant", "default")
    size     = props.get("size", "md")
    striped  = props.get("striped", False)
    animated = props.get("animated", False)

    cls = "progress"
    if variant != "default": cls += f" progress--{variant}"
    if size    != "md":      cls += f" progress--{size}"
    if striped:              cls += " progress--striped"
    if animated:             cls += " progress--animated"

    header_html = ""
    if label:
        header_html = f'''
        <div class="progress__header">
            <span class="progress__label">{label}</span>
            <span class="progress__value">{value}%</span>
        </div>'''

    return f'''
<div class="{cls}">
    {header_html}
    <div class="progress__track">
        <div class="progress__fill" style="width:{value}%;"></div>
    </div>
</div>'''


def render_skeleton(props, children):
    variant = props.get("variant", "text")
    width   = props.get("width")
    height  = props.get("height")

    cls   = f"skeleton skeleton--{variant}"
    style = ""
    if width:  style += f"width:{width};"
    if height: style += f"height:{height};"

    style_attr = f' style="{style}"' if style else ""
    return f'<div class="{cls}"{style_attr}></div>'


def render_spinner(props, children):
    size  = props.get("size", "md")
    color = props.get("color", "accent")
    cls   = f"spinner spinner--{size}"
    if color != "accent": cls += f" spinner--{color}"
    return f'<div class="{cls}"></div>'


def render_breadcrumb(props, children):
    items     = props.get("items", [])
    separator = props.get("separator", "chevron")

    items_html = ""
    for i, item in enumerate(items):
        label = item.label if hasattr(item, "label") else item.get("label","")
        href  = item.href  if hasattr(item, "href")  else item.get("href")
        is_last = i == len(items) - 1

        sep_html = ""
        if i > 0:
            if separator == "chevron":
                sep_html = '<i data-lucide="chevron-right" class="breadcrumb__separator"></i>'
            else:
                sep_html = '<span class="breadcrumb__separator">/</span>'

        if is_last or not href:
            content = f'<span class="breadcrumb__current">{label}</span>'
        else:
            content = f'<a class="breadcrumb__link" href="{href}">{label}</a>'

        items_html += f'<li class="breadcrumb__item">{sep_html}{content}</li>'

    return f'<nav><ol class="breadcrumb">{items_html}</ol></nav>'


# ── TABLE ──

def render_table(props, children):
    columns    = props.get("columns", [])
    searchable = props.get("searchable", False)
    sortable   = props.get("sortable", False)
    checkable  = props.get("checkable", False)
    actions    = props.get("actions", [])
    striped    = props.get("striped", False)
    pagination = props.get("pagination", True)
    data       = props.get("data", {})

    # fetch info
    fetch_method   = ""
    fetch_endpoint = ""
    if isinstance(data, dict) and data.get("__burq_fetch__"):
        fetch_method   = data.get("method", "GET")
        fetch_endpoint = data.get("endpoint", "")

    table_cls = "table"
    if striped: table_cls += " table--striped"

    # toolbar
    toolbar = ""
    if searchable or actions:
        search_html = ""
        if searchable:
            search_html = '''
            <div class="table-search">
                <i data-lucide="search" class="table-search__icon"></i>
                <input class="table-search__input" placeholder="Search..." />
            </div>'''
        toolbar = f'''
        <div class="table-toolbar">
            <div class="table-toolbar__left">{search_html}</div>
            <div class="table-toolbar__right">
                <button class="btn btn--secondary btn--sm">
                    <i data-lucide="download" class="btn__icon"></i>Export
                </button>
            </div>
        </div>'''

    # headers
    checkbox_th = '<th class="table__checkbox-col"><input type="checkbox" class="table__checkbox" /></th>' if checkable else ""
    actions_th  = '<th class="table__actions-col"></th>' if actions else ""

    headers = ""
    for col in columns:
        sort_icon = '<i data-lucide="arrow-up" class="table__sort-icon"></i>' if sortable else ""
        sort_cls  = "sortable" if sortable else ""
        headers  += f'<th class="{sort_cls}">{col.replace("_"," ").title()} {sort_icon}</th>'

    # tbody placeholder — filled by JS at runtime
    tbody_id = f"tbody-{fetch_endpoint.replace('/','').replace('{','').replace('}','')}"

    # pagination
    pagination_html = ""
    if pagination:
        pagination_html = '''
        <div class="table-pagination">
            <span class="table-pagination__info">Loading...</span>
            <div class="table-pagination__controls">
                <button class="table-pagination__btn" disabled>
                    <i data-lucide="chevron-left" style="width:14px;height:14px;"></i>
                </button>
                <button class="table-pagination__btn table-pagination__btn--active">1</button>
                <button class="table-pagination__btn">
                    <i data-lucide="chevron-right" style="width:14px;height:14px;"></i>
                </button>
            </div>
        </div>'''

    # serialize column_config to JSON for JS
    column_config = props.get("column_config", {})
    config_serialized = {}
    for col, cfg in column_config.items():
        if hasattr(cfg, "__class__"):
            d = {"type": cfg.__class__.__name__}
            d.update({k: v for k, v in cfg.__dict__.items() if v is not None})
            config_serialized[col] = d

    config_json = _json.dumps(config_serialized)

    return f'''
    <div class="table-wrapper"
        data-fetch-method="{fetch_method}"
        data-fetch-endpoint="{fetch_endpoint}"
        data-columns="{",".join(columns)}"
        data-checkable="{str(checkable).lower()}"
        data-actions="{",".join(actions)}"
        data-column-config='{config_json}'>
    {toolbar}
    <table class="{table_cls}">
        <thead>
            <tr>
                {checkbox_th}
                {headers}
                {actions_th}
            </tr>
        </thead>
        <tbody id="{tbody_id}">
            <tr><td colspan="{len(columns)+2}" style="text-align:center;padding:var(--space-6);">
                <div class="spinner spinner--md" style="margin:0 auto;"></div>
            </td></tr>
        </tbody>
    </table>
    {pagination_html}
</div>'''


# ── FORMS ──

def render_input(props, children):
    label       = props.get("label")
    placeholder = props.get("placeholder", "")
    type_       = props.get("type", "text")
    required    = props.get("required", False)
    disabled    = props.get("disabled", False)
    size        = props.get("size", "md")
    ico         = props.get("icon")
    icon_pos    = props.get("icon_pos", "left")
    error       = props.get("error")
    helper      = props.get("helper")
    name        = props.get("name", "")

    input_cls = "input"
    if size != "md":  input_cls += f" input--{size}"
    if error:         input_cls += " input--error"

    disabled_attr  = " disabled" if disabled else ""
    required_attr  = " required" if required else ""

    label_html  = ""
    if label:
        req_cls    = " form-label--required" if required else ""
        label_html = f'<label class="form-label{req_cls}">{label}</label>'

    input_html = f'<input class="{input_cls}" type="{type_}" name="{name}" placeholder="{placeholder}"{disabled_attr}{required_attr} />'

    if ico:
        wrapper_cls = "input-wrapper" if icon_pos == "left" else "input-wrapper input-wrapper--right"
        input_html  = f'''
        <div class="{wrapper_cls}">
            <i data-lucide="{ico}" class="input-wrapper__icon"></i>
            {input_html}
        </div>'''

    helper_html = f'<span class="form-helper">{helper}</span>' if helper else ""
    error_html  = f'''
        <span class="form-error">
            <i data-lucide="circle-alert" class="form-error__icon"></i>{error}
        </span>''' if error else ""

    return f'''
<div class="form-field">
    {label_html}
    {input_html}
    {helper_html}
    {error_html}
</div>'''


def render_textarea(props, children):
    label       = props.get("label")
    placeholder = props.get("placeholder", "")
    required    = props.get("required", False)
    disabled    = props.get("disabled", False)
    error       = props.get("error")
    helper      = props.get("helper")
    name        = props.get("name", "")
    rows        = props.get("rows", 3)

    cls = "textarea"
    if error: cls += " textarea--error"

    disabled_attr = " disabled" if disabled else ""
    required_attr = " required" if required else ""

    label_html  = ""
    if label:
        req_cls    = " form-label--required" if required else ""
        label_html = f'<label class="form-label{req_cls}">{label}</label>'

    helper_html = f'<span class="form-helper">{helper}</span>' if helper else ""
    error_html  = f'''
        <span class="form-error">
            <i data-lucide="circle-alert" class="form-error__icon"></i>{error}
        </span>''' if error else ""

    return f'''
<div class="form-field">
    {label_html}
    <textarea class="{cls}" name="{name}" rows="{rows}" placeholder="{placeholder}"{disabled_attr}{required_attr}></textarea>
    {helper_html}
    {error_html}
</div>'''


def render_select(props, children):
    label       = props.get("label")
    options     = props.get("options", [])
    placeholder = props.get("placeholder", "Select...")
    searchable  = props.get("searchable", False)
    required    = props.get("required", False)
    disabled    = props.get("disabled", False)
    size        = props.get("size", "md")
    error       = props.get("error")
    helper      = props.get("helper")
    name        = props.get("name", "")
    label_key   = props.get("label_key")
    value_key   = props.get("value_key")

    label_html = ""
    if label:
        req_cls    = " form-label--required" if required else ""
        label_html = f'<label class="form-label{req_cls}">{label}</label>'

    helper_html = f'<span class="form-helper">{helper}</span>' if helper else ""
    error_html  = f'''
        <span class="form-error">
            <i data-lucide="circle-alert" class="form-error__icon"></i>{error}
        </span>''' if error else ""

    if searchable:
        # custom searchable select
        options_html = ""
        for opt in options:
            if isinstance(opt, dict):
                val  = opt.get(value_key or "value", "")
                lbl  = opt.get(label_key or "label", "")
            else:
                val = lbl = opt
            options_html += f'''
            <div class="custom-select__option" data-value="{val}">
                {lbl}
                <i data-lucide="check" class="custom-select__option-check"></i>
            </div>'''

        err_cls = " custom-select__trigger--error" if error else ""
        return f'''
<div class="form-field">
    {label_html}
    <div class="custom-select">
        <div class="custom-select__trigger{err_cls}">
            <span class="custom-select__placeholder">{placeholder}</span>
            <span class="custom-select__value"></span>
            <div class="custom-select__icons">
                <span class="custom-select__clear">
                    <i data-lucide="x" style="width:12px;height:12px;"></i>
                </span>
                <i data-lucide="chevron-down" class="custom-select__chevron"></i>
            </div>
        </div>
        <div class="custom-select__dropdown">
            <div class="custom-select__search">
                <i data-lucide="search" class="custom-select__search-icon"></i>
                <input class="custom-select__search-input" placeholder="Search..." />
            </div>
            <div class="custom-select__options">
                {options_html}
                <div class="custom-select__empty">No results found.</div>
            </div>
        </div>
    </div>
    {helper_html}
    {error_html}
</div>'''

    # native select
    cls = f"select"
    if size  != "md": cls += f" select--{size}"
    if error:         cls += " select--error"

    options_html = f'<option value="" disabled selected>{placeholder}</option>'
    for opt in options:
        if isinstance(opt, dict):
            val = opt.get(value_key or "value", "")
            lbl = opt.get(label_key or "label", "")
        else:
            val = lbl = opt
        options_html += f'<option value="{val}">{lbl}</option>'

    return f'''
<div class="form-field">
    {label_html}
    <select class="{cls}" name="{name}">
        {options_html}
    </select>
    {helper_html}
    {error_html}
</div>'''


def render_toggle(props, children):
    label    = props.get("label", "")
    value    = props.get("checked", props.get("value", False))
    disabled = props.get("disabled", False)
    name     = props.get("name", "")

    checked_attr  = " checked" if value    else ""
    disabled_attr = " disabled" if disabled else ""

    return f'''
<label class="toggle">
    <input type="checkbox" class="toggle__input" name="{name}"{checked_attr}{disabled_attr} />
    <div class="toggle__track"><div class="toggle__thumb"></div></div>
    <span class="toggle__label">{label}</span>
</label>'''


def render_checkbox(props, children):
    label    = props.get("label", "")
    value    = props.get("value", False)
    disabled = props.get("disabled", False)
    name     = props.get("name", "")

    checked_attr  = " checked"  if value    else ""
    disabled_attr = " disabled" if disabled else ""

    return f'''
<label class="checkbox">
    <input type="checkbox" class="checkbox__input" name="{name}"{checked_attr}{disabled_attr} />
    <span class="checkbox__label">{label}</span>
</label>'''


def render_radio(props, children):
    label    = props.get("label", "")
    name     = props.get("name", "")
    value    = props.get("value", "")
    checked  = props.get("checked", False)
    disabled = props.get("disabled", False)

    checked_attr  = " checked"  if checked  else ""
    disabled_attr = " disabled" if disabled else ""

    return f'''
<label class="radio">
    <input type="radio" class="radio__input" name="{name}" value="{value}"{checked_attr}{disabled_attr} />
    <span class="radio__label">{label}</span>
</label>'''


def render_button(props, children):
    label    = props.get("label", "")
    variant  = props.get("variant", "primary")
    size     = props.get("size", "md")
    ico      = props.get("icon")
    icon_pos = props.get("icon_pos", "left")
    disabled = props.get("disabled", False)
    onclick  = props.get("onclick", "")
    type_    = props.get("type", "button")

    cls = f"btn btn--{variant}"
    if size != "md": cls += f" btn--{size}"
    if not label:    cls += " btn--icon"

    disabled_attr = " disabled" if disabled else ""
    onclick_attr  = f' onclick="{onclick}"' if onclick else ""

    icon_html = f'<i data-lucide="{ico}" class="btn__icon"></i>' if ico else ""

    content = ""
    if icon_pos == "left":
        content = f"{icon_html}{label}"
    else:
        content = f"{label}{icon_html}"

    return f'<button class="{cls}" type="{type_}"{onclick_attr}{disabled_attr}>{content}</button>'


# ── FEEDBACK ──

def render_modal(props, children):
    id_    = props.get("id", "modal")
    title  = props.get("title", "")
    size   = props.get("size", "md")

    cls = "modal"
    if size != "md": cls += f" modal--{size}"

    return f'''
<div class="overlay" id="{id_}">
    <div class="{cls}">
        <div class="modal__header">
            <span class="modal__title">{title}</span>
            <button class="modal__close" onclick="ModalManager.close('{id_}')">
                <i data-lucide="x" style="width:14px;height:14px;"></i>
            </button>
        </div>
        {children}
    </div>
</div>'''


def render_modal_body(props, children):
    return f'<div class="modal__body">{children}</div>'


def render_modal_footer(props, children):
    return f'<div class="modal__footer">{children}</div>'


def render_alert(props, children):
    message = props.get("message", "")
    type_   = props.get("type", "info")
    title   = props.get("title")

    icons = {
        "success": "circle-check",
        "error":   "circle-x",
        "warning": "triangle-alert",
        "info":    "info"
    }

    title_html = f'<div class="alert__title">{title}</div>' if title else ""

    return f'''
<div class="alert alert--{type_}">
    <i data-lucide="{icons.get(type_,"info")}" class="alert__icon"></i>
    <div class="alert__body">
        {title_html}
        <div class="alert__message">{message}</div>
    </div>
</div>'''


# ── NAVIGATION ──

def render_tabs(props, children):
    items   = props.get("items", [])
    variant = props.get("variant", "default")
    icons   = props.get("icons", [])
    badges  = props.get("badges", [])

    cls = "tabs"
    if variant != "default": cls += f" tabs--{variant}"

    triggers = ""
    for i, item in enumerate(items):
        ico_html   = f'<i data-lucide="{icons[i]}" class="tabs__trigger__icon"></i>' if i < len(icons) and icons[i] else ""
        badge_html = f'<span class="badge badge--default">{badges[i]}</span>' if i < len(badges) and badges[i] else ""
        triggers  += f'<button class="tabs__trigger">{ico_html}{item}{badge_html}</button>'

    # panels come from children (tab nodes)
    return f'''
<div class="{cls}">
    <div class="tabs__list">{triggers}</div>
    {children}
</div>'''


def render_tab(props, children):
    return f'<div class="tabs__panel">{children}</div>'


def render_dropdown(props, children):
    items   = props.get("items", [])
    align   = props.get("align", "right")
    trigger = props.get("trigger", {})

    trigger_html = render_node(trigger) if isinstance(trigger, dict) else ""

    items_html = ""
    for item in items:
        if hasattr(item, "label"):
            ico_html  = f'<i data-lucide="{item.icon}" class="dropdown__icon"></i>' if item.icon else ""
            danger_cls = " dropdown__item--danger"   if item.danger   else ""
            dis_cls    = " dropdown__item--disabled" if item.disabled else ""
            onclick    = f' onclick="{item.onclick}"' if item.onclick else ""
            items_html += f'<button class="dropdown__item{danger_cls}{dis_cls}"{onclick}>{ico_html}{item.label}</button>'
        elif hasattr(item, "text"):
            items_html += f'<div class="dropdown__label">{item.text}</div>'
        else:
            items_html += '<div class="dropdown__divider"></div>'

    menu_cls = "dropdown__menu"
    if align == "left": menu_cls += " dropdown__menu--left"

    return f'''
<div class="dropdown">
    {trigger_html}
    <div class="{menu_cls}">{items_html}</div>
</div>'''


# ── PAGE SHELL ──

def render_page_shell(
    app,
    page_content: str,
    modal_content: str = "",
    page_title: str = "",
) -> str:
    from ..theme.compiler import compile_tokens

    theme      = app.theme
    layout     = app.layout
    nav        = app._nav
    nav_footer = app._nav_footer

    # sidebar classes
    layout_cls = "layout"
    if layout.sidebar: layout_cls += " layout--with-sidebar"
    if layout.topbar:  layout_cls += " layout--with-topbar"

    # nav items
    nav_html = ""
    for item in nav:
        nav_html += f'''
        <a class="nav-item" href="{item.href}">
            <i data-lucide="{item.icon}" class="nav-item__icon"></i>
            <span class="nav-item__label">{item.label}</span>
        </a>'''

    nav_footer_html = ""
    for item in nav_footer:
        nav_footer_html += f'''
        <a class="nav-item" href="{item.href}">
            <i data-lucide="{item.icon}" class="nav-item__icon"></i>
            <span class="nav-item__label">{item.label}</span>
        </a>'''

    sidebar_html = ""
    if layout.sidebar:
        sidebar_html = f'''
  <aside class="sidebar">
    <div class="sidebar__logo">
      <svg class="sidebar__logo-mark" viewBox="0 0 56 56" fill="none">
        <path d="M20 10 C16 10 14 12 14 16 L14 22 C14 24.5 12 26 10 28 C12 30 14 31.5 14 34 L14 40 C14 44 16 46 20 46" stroke="#f5f5f5" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        <path d="M36 10 C40 10 42 12 42 16 L42 22 C42 24.5 44 26 46 28 C44 30 42 31.5 42 34 L42 40 C42 44 40 46 36 46" stroke="#f5f5f5" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        <path d="M31 14 L22 29 L27.5 29 L25 42 L36 25 L30 25 L33 14 Z" fill="#F0A202"/>
      </svg>
      <span class="sidebar__logo-name">{app.title}</span>
    </div>
    <nav class="sidebar__nav">{nav_html}</nav>
    <div class="sidebar__footer">{nav_footer_html}</div>
  </aside>'''

    topbar_html = ""
    if layout.topbar:
        toggle_btn = f'''
        <button class="topbar__toggle" id="sidebarToggle">
            <i data-lucide="menu" class="topbar__icon"></i>
        </button>''' if layout.sidebar else ""

        theme_toggle = ""
        if theme.toggle:
            theme_toggle = '''
            <button class="topbar__toggle" id="themeToggle" title="Toggle theme">
                <i data-lucide="sun" class="topbar__icon" id="themeIcon"></i>
            </button>'''

        author_html = f'<meta name="author" content="{app.author}" />' if app.author else ""

        topbar_html = f'''
  <header class="topbar">
    <div class="topbar__left">
        {toggle_btn}
        <span class="topbar__title">{page_title or app.title}</span>
    </div>
    <div class="topbar__right">
        {theme_toggle}
        <button class="topbar__toggle">
            <i data-lucide="bell" class="topbar__icon"></i>
        </button>
    </div>
  </header>'''

    return f'''<!DOCTYPE html>
<html lang="en" data-theme="{theme.mode}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="generator" content="Burq ⚡ — https://burq.dev" />
  {f'<meta name="author" content="{app.author}" />' if app.author else ""}
  <title>{page_title or app.title}</title>
  <!-- ⚡ Built with Burq — https://burq.dev -->
  {f'<!-- Created by {app.author} -->' if app.author else ""}
  <link rel="stylesheet" href="tokens.css" />
  <link rel="stylesheet" href="layout.css" />
  <link rel="stylesheet" href="components.css" />
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    .nav-item__icon {{ width: 18px; height: 18px; flex-shrink: 0; }}
    .topbar__icon   {{ width: 18px; height: 18px; }}
    .page-title     {{ font-size: var(--text-2xl); font-weight: 700; color: var(--foreground); letter-spacing: -0.02em; margin-bottom: var(--space-4); }}
    .page-heading   {{ font-size: var(--text-xl);  font-weight: 600; color: var(--foreground); letter-spacing: -0.01em; margin-bottom: var(--space-3); }}
    .body-text      {{ font-size: var(--text-base); color: var(--foreground); }}
    .muted-text     {{ font-size: var(--text-base); color: var(--muted-foreground); }}
  </style>
</head>
<body>
<div class="{layout_cls}" id="layout">
  {sidebar_html}
  {topbar_html}
  <main class="content">
    <div style="padding: var(--space-6);">
      {page_content}
    </div>
  </main>
</div>

{modal_content}

<script src="burq.js"></script>
</body>
</html>'''