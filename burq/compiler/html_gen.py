import base64
import os
import json as _json
from ..components.navigation import NavGroup 

TOKEN_MAP = {
    "accent":  "var(--accent)",
    "muted":   "var(--muted-foreground)",
    "success": "var(--color-success)",
    "error":   "var(--color-error)",
    "warning": "var(--color-warning)",
    "dim":     "var(--muted-foreground)",
}
SIZE_MAP = {
    "xs":   "var(--text-xs)",
    "sm":   "var(--text-sm)",
    "base": "var(--text-base)",
    "md":   "var(--text-md)",
    "lg":   "var(--text-lg)",
    "xl":   "var(--text-xl)",
    "2xl":  "var(--text-2xl)",
    "3xl":  "40px",
    "4xl":  "48px",
    "5xl":  "64px",
    "6xl":  "80px",
}

def _size_style(size):
    if not size:
        return ""
    css = SIZE_MAP.get(size, size)  # falls back to raw CSS e.g. "52px"
    return f"font-size:{css};"

def classes(*args) -> str:
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


DEFAULT_LOGO = '''<svg viewBox="0 0 130 36" fill="none" style="height:28px;flex-shrink:0;">
  <!-- tile: 36x36 -->
  <rect width="36" height="36" rx="7" fill="var(--accent)"/>
  <!-- braces scaled from 100x100 to fit 36x36 tile with padding -->
  <g transform="translate(3, 3) scale(0.3)">
    <path d="M 38 12 C 30 12 28 22 28 32 C 28 42 18 44 14 50 C 18 56 28 58 28 68 C 28 78 30 88 38 88" fill="none" stroke="#ffffff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M 62 12 C 70 12 72 22 72 32 C 72 42 82 44 86 50 C 82 56 72 58 72 68 C 72 78 70 88 62 88" fill="none" stroke="#ffffff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M 54 24 L 38 54 L 48 54 L 44 78 L 62 46 L 52 46 L 56 24 Z" fill="#ffffff"/>
  </g>
  <!-- wordmark -->
   <text x="46" y="25" font-family="Space Grotesk, sans-serif" font-weight="700" font-size="20" letter-spacing="-0.03em" fill="var(--foreground)">burq</text>
</svg>'''

def render_logo(logo, size="28px") -> str:
    """
    logo = "default"        → burq default SVG
    logo = None             → empty string (no logo)
    logo = "<svg>...</svg>" → inline SVG string
    logo = "path/to/file"   → embedded file (svg/png/jpg)
    """
    if logo is None:
        return ""
    if logo == "default":
        return DEFAULT_LOGO
    if isinstance(logo, str) and logo.strip().startswith("<svg"):
        return logo
    if isinstance(logo, str) and os.path.isfile(logo):
        ext = os.path.splitext(logo)[1].lower()
        if ext == ".svg":
            with open(logo, encoding="utf-8") as f:
                content = f.read()
            # inject size style if not present
            if "width" not in content[:100]:
                content = content.replace("<svg", f'<svg style="width:{size};height:{size};flex-shrink:0;"', 1)
            return content
        else:
            mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
            mime = mime_map.get(ext, "image/png")
            with open(logo, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            return f'<img src="data:{mime};base64,{b64}" style="width:{size};height:{size};object-fit:contain;flex-shrink:0;" />'
    return ""


# ── NODE RENDERERS ──

def render_node(node: dict, app=None) -> str:
    tag = node.get("tag")
    props = node.get("props", {})
    children = node.get("children", [])
    rendered_children = "\n".join(render_node(c, app) for c in children)

    renderers = {
        "title":        render_title,
        "heading":      render_heading,
        "text":         render_text,
        "row":          render_row,
        "col":          render_col,
        "grid":         render_grid,
        "span":         render_span,
        "container":    render_container,
        "divider":      render_divider,
        "card":         render_card,
        "metric":       render_metric,
        "badge":        render_badge,
        "avatar":       render_avatar,
        "avatar_group": render_avatar_group,
        "progress":     render_progress,
        "skeleton":     render_skeleton,
        "spinner":      render_spinner,
        "breadcrumb":   render_breadcrumb,
        "table":        render_table,
        "input":        render_input,
        "textarea":     render_textarea,
        "select":       render_select,
        "toggle":       render_toggle,
        "checkbox":     render_checkbox,
        "radio":        render_radio,
        "button":       render_button,
        "modal":        render_modal,
        "modal_body":   render_modal_body,
        "modal_footer": render_modal_footer,
        "alert":        render_alert,
        "tabs":         render_tabs,
        "tab":          render_tab,
        "dropdown":     render_dropdown,
        "spacer":       render_spacer,
        "grow":         render_grow,
        "accordion":    render_accordion,
        "empty_state":  render_empty_state,
        "pagination":   render_pagination,
        "contact_profile": render_contact_profile,
        "box":      render_box,
        "markdown": render_markdown,
        "file_upload": render_file_upload,
        "code_block":  render_code_block,
        "rich_text":   render_rich_text,
        "line_chart":  render_chart,
        "area_chart":  render_chart,
        "bar_chart":   render_chart,
        "donut_chart": render_chart,
        "icon":     render_icon,
        "image": render_image,
        "link":  render_link,
        "script": render_script,
    }

    renderer = renderers.get(tag)
    if renderer:
        return renderer(props, rendered_children)
    return f"<!-- unknown tag: {tag} -->"


def render_tree(tree: list, app=None) -> str:
    return "\n".join(render_node(node, app) for node in tree)

def render_icon(props, _children=""):
    size_map = {"xs": "12px", "sm": "14px", "md": "16px", "lg": "20px", "xl": "24px"}
    token_map = {
        "accent": "var(--accent)", "muted": "var(--muted-foreground)",
        "success": "var(--color-success)", "warning": "var(--color-warning)",
        "error": "var(--color-error)", "dim": "var(--fg-dim)",
        "foreground": "var(--foreground)",
    }
    size_val  = size_map.get(props.get("size", "md"), props.get("size", "16px"))
    color_raw = props.get("color")
    color_val = token_map.get(color_raw, color_raw) if color_raw else "currentColor"
    label_attr = f'aria-label="{props["label"]}"' if props.get("label") else 'aria-hidden="true"'
    return f'<i data-lucide="{props["name"]}" {label_attr} style="width:{size_val};height:{size_val};color:{color_val};display:inline-flex;flex-shrink:0;"></i>'

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

def render_file_upload(props, children):
    label   = props.get("label")
    accept  = props.get("accept", "")
    name    = props.get("name", "file")
    helper  = props.get("helper")
    error   = props.get("error")
    uid     = f"fu-{abs(hash(name)) % 100000}"

    label_html  = f'<label class="form-label">{label}</label>' if label else ""
    helper_html = f'<span class="form-helper">{helper}</span>' if helper else ""
    error_html  = f'<span class="form-error"><i data-lucide="circle-alert" class="form-error__icon"></i>{error}</span>' if error else ""

    return f'''
<div class="form-field">
    {label_html}
    <div class="file-upload" id="{uid}" data-accept="{accept}">
        <input type="file" class="file-upload__input" name="{name}" accept="{accept}" id="{uid}-input" />
        <div class="file-upload__zone" onclick="document.getElementById('{uid}-input').click()">
            <div class="file-upload__icon">
                <i data-lucide="upload-cloud"></i>
            </div>
            <div class="file-upload__text">
                <span class="file-upload__primary">Drop file here or <span class="file-upload__link">browse</span></span>
                <span class="file-upload__secondary">{accept if accept else "Any file type"}</span>
            </div>
        </div>
        <div class="file-upload__preview" id="{uid}-preview" style="display:none;">
            <i data-lucide="file" class="file-upload__file-icon"></i>
            <span class="file-upload__filename" id="{uid}-name"></span>
            <button class="file-upload__clear" onclick="burqClearFile('{uid}')" type="button">
                <i data-lucide="x"></i>
            </button>
        </div>
    </div>
    {helper_html}
    {error_html}
</div>'''

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

def _color_style(color):
    if not color:
        return ""
    return f"color:{TOKEN_MAP.get(color, color)};"

def _build_style(props):
    s = _color_style(props.get("color"))
    s += _size_style(props.get("size"))
    return f' style="{s}"' if s else ""

def render_title(props, children):
    return f'<h1 class="page-title"{_build_style(props)}>{props.get("text","")}</h1>'

def render_heading(props, children):
    return f'<h2 class="page-heading"{_build_style(props)}>{props.get("text","")}</h2>'

def render_text(props, children):
    cls = "muted-text" if props.get("muted") else "body-text"
    return f'<p class="{cls}"{_build_style(props)}>{props.get("content","")}</p>'


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

def render_image(props, children):
    src      = props.get("src", "")
    src_dark = props.get("src_dark")
    alt      = props.get("alt", "")
    width    = props.get("width")
    height   = props.get("height")
    radius   = props.get("radius", "md")
    caption  = props.get("caption")
    fit      = props.get("fit", "cover")

    if src and not src.startswith("http") and not src.startswith("/"):
        src = f"/{src}"
    if src_dark and not src_dark.startswith("http") and not src_dark.startswith("/"):
        src_dark = f"/{src_dark}"

    style = f"object-fit:{fit};"
    if width:  style += f"width:{width};"
    if height: style += f"height:{height};"

    if src_dark:
        img_html = (
            f'<img class="bq-image radius--{radius} bq-img--light" src="{src}"      alt="{alt}" style="{style}">'
            f'<img class="bq-image radius--{radius} bq-img--dark"  src="{src_dark}" alt="{alt}" style="{style}">'
        )
    else:
        img_html = f'<img class="bq-image radius--{radius}" src="{src}" alt="{alt}" style="{style}">'

    cap_html = f'<figcaption class="bq-image__caption">{caption}</figcaption>' if caption else ""
    return f'<figure class="bq-image-wrap">{img_html}{cap_html}</figure>'


def render_link(props, children):
    label    = props.get("label", "")
    href     = props.get("href", "#")
    ico      = props.get("icon")
    external = props.get("external", False)
    muted    = props.get("muted", False)
    size     = props.get("size")
    onclick  = props.get("onclick", "")

    cls      = "bq-link"
    if muted: cls += " bq-link--muted"

    style_attr   = f' style="font-size:var(--text-{size})"' if size else ""
    ext_attr     = ' target="_blank" rel="noopener"' if external else ""
    onclick_attr = f' onclick="{onclick}"' if onclick else ""
    icon_html    = f'<i data-lucide="{ico}" class="bq-link__icon"></i>' if ico else ""

    if href and "{" in href:
        return f'<a class="{cls}" data-href-template="{href}"{ext_attr}{style_attr}{onclick_attr}>{icon_html}{label}</a>'
    return f'<a class="{cls}" href="{href}"{ext_attr}{style_attr}{onclick_attr}>{icon_html}{label}</a>'


def render_spinner(props, children):
    size  = props.get("size", "md")
    color = props.get("color", "accent")
    cls   = f"spinner spinner--{size}"
    if color != "accent": cls += f" spinner--{color}"
    return f'<div class="{cls}"></div>'


def render_spacer(props, children):
    sizes = {
        "xs": "var(--space-2)",
        "sm": "var(--space-3)",
        "md": "var(--space-6)",
        "lg": "var(--space-8)",
        "xl": "var(--space-12)",
    }
    height = sizes.get(props.get("size", "md"), "var(--space-6)")
    return f'<div style="height:{height};"></div>'


def render_grow(props, children):
    return '<div style="flex:1;"></div>'


def render_breadcrumb(props, children):
    items     = props.get("items", [])
    separator = props.get("separator", "chevron")

    items_html = ""
    for i, item in enumerate(items):
        label = item.label if hasattr(item, "label") else item.get("label", "")
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

def render_contact_profile(props, children):
    endpoint = props.get("endpoint", "")
    uid = "contact-profile"

    return f'''
<div id="{uid}">
  <div class="contact-profile">
    <div class="skeleton skeleton--avatar-lg" style="width:56px;height:56px;border-radius:var(--radius-xl);flex-shrink:0;"></div>
    <div class="col" style="gap:var(--space-2);flex:1;">
      <div class="skeleton skeleton--text-lg" style="width:180px;"></div>
      <div class="skeleton skeleton--text-sm" style="width:120px;"></div>
    </div>
    <div class="row" style="gap:var(--space-4);margin-left:auto;">
      <div class="skeleton skeleton--rect" style="width:90px;height:48px;"></div>
      <div class="skeleton skeleton--rect" style="width:90px;height:48px;"></div>
      <div class="skeleton skeleton--rect" style="width:90px;height:48px;"></div>
    </div>
  </div>
</div>
<script>
document.addEventListener("DOMContentLoaded", async function() {{
  try {{
    const endpoint = "{endpoint}".replace(/\\{{(\\w+)\\}}/g, (_, k) => (window.__burqParams||{{}})[k] || "");
    const data = await Burq.fetch("GET", endpoint);
    const initials = (data.name || "").split(" ").map(w => w[0]).join("").slice(0,2).toUpperCase();
    const statusVariants = {{
      lead: "default", qualified: "info", proposal: "warning", won: "success", lost: "danger"
    }};
    const status  = data.status || "lead";
    const variant = statusVariants[status] || "default";
    const date    = data.created_at ? new Date(data.created_at).toLocaleDateString("en-US", {{year:"numeric",month:"short",day:"numeric"}}) : "—";

    document.getElementById("{uid}").innerHTML = `
      <div class="contact-profile">
        <div class="avatar avatar--xl" style="border-radius:var(--radius-xl);font-size:var(--text-md);">${{initials}}</div>
        <div class="col" style="gap:var(--space-1);flex:1;">
          <div style="font-size:var(--text-xl);font-weight:700;color:var(--foreground);letter-spacing:-0.02em;">${{data.name || "—"}}</div>
          <div style="font-size:var(--text-base);color:var(--muted-foreground);">${{data.title || ""}}${{data.title && data.company ? " · " : ""}}${{data.company || ""}}</div>
        </div>
        <div class="row" style="gap:var(--space-6);margin-left:auto;align-items:center;">
          <div class="col" style="gap:2px;align-items:flex-end;">
            <span style="font-family:var(--font-mono);font-size:var(--text-xs);text-transform:uppercase;letter-spacing:0.08em;color:var(--muted-foreground);">Status</span>
            <span class="badge badge--${{variant}}">${{status}}</span>
          </div>
          <div class="col" style="gap:2px;align-items:flex-end;">
            <span style="font-family:var(--font-mono);font-size:var(--text-xs);text-transform:uppercase;letter-spacing:0.08em;color:var(--muted-foreground);">Phone</span>
            <span style="font-size:var(--text-base);font-weight:500;color:var(--foreground);">${{data.phone || "—"}}</span>
          </div>
          <div class="col" style="gap:2px;align-items:flex-end;">
            <span style="font-family:var(--font-mono);font-size:var(--text-xs);text-transform:uppercase;letter-spacing:0.08em;color:var(--muted-foreground);">Member Since</span>
            <span style="font-size:var(--text-base);font-weight:500;color:var(--foreground);">${{date}}</span>
          </div>
        </div>
      </div>
    `;
    lucide.createIcons();
  }} catch(e) {{
    console.error("Profile load failed", e);
  }}
}});
</script>'''

def render_box(props, children):
    style   = props.get("style", "")
    classes = " ".join(props.get("classes", ["box"]))
    return f'<div class="{classes}" style="{style}">{children}</div>'


def render_markdown(props, children):
    content = props.get("content", "")
    # escape backticks and backslashes for JS template literal
    content_escaped = content.replace("\\", "\\\\").replace("`", "\\`")
    uid = f"md-{abs(hash(content)) % 100000}"
    return f'''<div id="{uid}" class="markdown-body"></div>
<script>
(function() {{
  var el = document.getElementById("{uid}");
  if (window.marked) {{
    el.innerHTML = marked.parse(`{content_escaped}`);
  }} else {{
    el.textContent = `{content_escaped}`;
  }}
}})();
</script>'''


def render_script(props, children):
    code = props.get("code", "")
    return f'<script>\n{code}\n</script>'


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

    fetch_method   = ""
    fetch_endpoint = ""
    static_data    = None
    if isinstance(data, dict) and data.get("__burq_fetch__"):
        fetch_method   = data.get("method", "GET")
        fetch_endpoint = data.get("endpoint", "")
    elif data is not None:
        # DataFrame or list — serialize to JSON at compile time
        if hasattr(data, "to_dict"):
            static_data = _json.dumps(data.to_dict(orient="records"))
        elif isinstance(data, list):
            static_data = _json.dumps(data)
    table_cls = "table"
    if striped: table_cls += " table--striped"

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

    checkbox_th = '<th class="table__checkbox-col"><input type="checkbox" class="table__checkbox" /></th>' if checkable else ""
    actions_th  = '<th class="table__actions-col"></th>' if actions else ""

    headers = ""
    for col in columns:
        sort_icon = '<i data-lucide="arrow-up" class="table__sort-icon"></i>' if sortable else ""
        sort_cls  = "sortable" if sortable else ""
        headers  += f'<th class="{sort_cls}">{col.replace("_"," ").title()} {sort_icon}</th>'

    tbody_id = f"tbody-{abs(hash(fetch_endpoint + str(id(props)))) % 999999}"

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

    column_config = props.get("column_config", {})
    config_serialized = {}
    for col, cfg in column_config.items():
        if hasattr(cfg, "__class__"):
            d = {"type": cfg.__class__.__name__}
            d.update({k: v for k, v in cfg.__dict__.items() if v is not None})
            config_serialized[col] = d

    config_json = _json.dumps(config_serialized)

    # serialize actions — support both TableAction dataclasses and plain strings
    actions_serialized = []
    for a in actions:
        if hasattr(a, "__class__") and hasattr(a, "label"):
            actions_serialized.append({
                "label":   a.label,
                "icon":    a.icon or "",
                "variant": a.variant or "default",
                "onclick": a.onclick or "",
            })
        else:
            # legacy plain string — treat as label only
            actions_serialized.append({"label": str(a), "icon": "", "variant": "default", "onclick": ""})
    actions_json = _json.dumps(actions_serialized)

    empty_title   = props.get("empty_title", "")
    empty_message = props.get("empty_message", "")
    empty_icon    = props.get("empty_icon", "")
    data_static_attr = f"data-static='{static_data}'" if static_data else ""
    return f'''
    <div class="table-wrapper"
        data-fetch-method="{fetch_method}"
        data-fetch-endpoint="{fetch_endpoint}"
        {data_static_attr}
        data-columns="{",".join(columns)}"
        data-checkable="{str(checkable).lower()}"
        data-actions='{actions_json}'
        data-column-config='{config_json}'
        data-row-href="{props.get('row_href') or ''}"
        data-empty-title="{empty_title}"
        data-empty-message="{empty_message}"
        data-empty-icon="{empty_icon}">
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

# ── CHARTS ──

def render_chart(props, children):
    chart_type = props.get("chart_type", "line")
    title      = props.get("title", "")
    height     = props.get("height", 300)
    data       = props.get("data", {})

    fetch_method   = ""
    fetch_endpoint = ""
    inline_data    = "null"

    if isinstance(data, dict) and data.get("__burq_fetch__"):
        fetch_method   = data.get("method", "GET")
        fetch_endpoint = data.get("endpoint", "")
    elif isinstance(data, list):
        inline_data = _json.dumps(data)
    else:
        try:
            inline_data = data.to_json(orient="records")
        except Exception:
            inline_data = "[]"

    chart_id = f"chart-{abs(hash(str(id(props)))) % 999999}"
    cfg      = {k: v for k, v in props.items()
                if k not in ("data", "chart_type", "title", "height")}
    cfg_json = _json.dumps(cfg)
    title_html = f'<div class="chart__title">{title}</div>' if title else ""

    return f'''
<div class="chart-wrapper">
    {title_html}
    <div class="chart__container" style="height:{height}px;position:relative;width:100%;">
        <canvas id="{chart_id}"
            data-chart-type="{chart_type}"
            data-chart-config=\'{cfg_json}\'
            data-fetch-method="{fetch_method}"
            data-fetch-endpoint="{fetch_endpoint}"
            data-inline=\'{inline_data}\'>
        </canvas>
    </div>
</div>'''

# ── FORMS ──

def render_input(props, children):
    label       = props.get("label")
    placeholder = props.get("placeholder") or ""
    type_       = props.get("type", "text")
    required    = props.get("required", False)
    disabled    = props.get("disabled", False)
    size        = props.get("size", "md")
    ico         = props.get("icon")
    icon_pos    = props.get("icon_pos", "left")
    error       = props.get("error")
    helper      = props.get("helper")
    name        = props.get("name") or ""

    input_cls = "input"
    if size != "md":  input_cls += f" input--{size}"
    if error:         input_cls += " input--error"

    disabled_attr = " disabled" if disabled else ""
    required_attr = " required" if required else ""

    label_html = ""
    if label:
        req_cls    = " form-label--required" if required else ""
        label_html = f'<label class="form-label{req_cls}">{label}</label>'

    value      = props.get("value")
    value_attr = f' value="{value}"' if value is not None else ""

    input_html = f'<input class="{input_cls}" type="{type_}" name="{name}" placeholder="{placeholder}"{value_attr}{disabled_attr}{required_attr} />'

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

    label_html = ""
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
        options_html = ""
        for opt in options:
            if isinstance(opt, dict):
                val = opt.get(value_key or "value", "")
                lbl = opt.get(label_key or "label", "")
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

    cls = "select"
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

    checked_attr  = " checked"  if value    else ""
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
    loading  = props.get("loading", False)
    onclick  = props.get("onclick", "")
    type_    = props.get("type", "button")
    href     = props.get("href")
    external = props.get("external", False)

    cls = f"btn btn--{variant}"
    if size != "md":          cls += f" btn--{size}"
    if not label and not loading: cls += " btn--icon"
    if loading:               cls += " btn--loading"

    disabled_attr = " disabled" if (disabled or loading) else ""
    onclick_attr  = f' onclick="{onclick}"' if onclick else ""
    icon_html     = f'<i data-lucide="{ico}" class="btn__icon"></i>' if ico else ""
    spinner_html  = '<span class="btn__spinner"></span>' if loading else ""
    content       = f"{spinner_html}{icon_html}{label}" if icon_pos == "left" else f"{label}{icon_html}{spinner_html}"

    # render as <a> if variant="link" or href is set
    if variant == "link" or href:
        ext_attr = ' target="_blank" rel="noopener"' if external else ""
        href_val = href or "#"
        if href_val and "{" in href_val:
            return f'<a class="{cls}" data-href-template="{href_val}"{ext_attr}{onclick_attr}>{content}</a>'
        return f'<a class="{cls}" href="{href_val}"{ext_attr}{onclick_attr}>{content}</a>'

    orig_attr = f' data-original-label="{label}"' if label else ""
    return f'<button class="{cls}" type="{type_}"{onclick_attr}{disabled_attr}{orig_attr}>{content}</button>'

# ── FEEDBACK ──

def render_modal(props, children):
    id_   = props.get("id", "modal")
    title = props.get("title", "")
    size  = props.get("size", "md")

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
        badge_html = f'<span class="badge badge--default">{badges[i]}</span>'        if i < len(badges) and badges[i] else ""
        triggers  += f'<button class="tabs__trigger">{ico_html}{item}{badge_html}</button>'

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
    trigger_html = trigger_html.replace("<button ", "<button data-dropdown-trigger ", 1)
    trigger_html = trigger_html.replace("<a ", "<a data-dropdown-trigger ", 1)
    items_html = ""
    for item in items:
        if hasattr(item, "label"):
            ico_html   = f'<i data-lucide="{item.icon}" class="dropdown__icon"></i>' if item.icon else ""
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


# ── NEW COMPONENTS ──

def render_accordion(props, children):
    items    = props.get("items", [])
    multiple = props.get("multiple", False)  # allow multiple open panels

    panels_html = ""
    for i, item in enumerate(items):
        title   = item.get("title", "") if isinstance(item, dict) else getattr(item, "title", "")
        content = item.get("content", "") if isinstance(item, dict) else getattr(item, "content", "")
        default_open = item.get("open", False) if isinstance(item, dict) else getattr(item, "open", False)

        open_cls    = " accordion__item--open" if default_open else ""
        open_attr   = ' data-open="true"'       if default_open else ""

        panels_html += f'''
<div class="accordion__item{open_cls}"{open_attr}>
    <button class="accordion__trigger" type="button">
        <span class="accordion__title">{title}</span>
        <i data-lucide="chevron-down" class="accordion__icon"></i>
    </button>
    <div class="accordion__panel">
        <div class="accordion__content">{content}</div>
    </div>
</div>'''

    multiple_attr = ' data-multiple="true"' if multiple else ""
    return f'<div class="accordion"{multiple_attr}>{panels_html}</div>'


def render_empty_state(props, children):
    ico     = props.get("icon", "inbox")
    title   = props.get("title", "Nothing here yet")
    message = props.get("message", "")
    action  = props.get("action")   # dict: {label, onclick, icon}

    action_html = ""
    if action:
        ico_html    = f'<i data-lucide="{action.get("icon")}" class="btn__icon"></i>' if action.get("icon") else ""
        onclick_attr = f' onclick="{action["onclick"]}"' if action.get("onclick") else ""
        action_html  = f'<button class="btn btn--primary btn--sm"{onclick_attr}>{ico_html}{action.get("label","")}</button>'

    message_html = f'<p class="empty-state__message">{message}</p>' if message else ""

    return f'''
<div class="empty-state">
    <div class="empty-state__icon">
        <i data-lucide="{ico}"></i>
    </div>
    <div class="empty-state__title">{title}</div>
    {message_html}
    {action_html}
</div>'''


def render_pagination(props, children):
    total       = props.get("total", 0)
    page        = props.get("page", 1)
    per_page    = props.get("per_page", 10)
    on_change   = props.get("on_change", "")  # JS callback name

    total_pages = max(1, -(-total // per_page))  # ceiling division
    start       = (page - 1) * per_page + 1
    end         = min(page * per_page, total)

    # build page buttons — show max 5 around current
    buttons_html = ""
    page_range = sorted(set(
        [1, 2, total_pages - 1, total_pages] +
        list(range(max(1, page - 1), min(total_pages + 1, page + 2)))
    ))

    prev_p = None
    for p in page_range:
        if p < 1 or p > total_pages:
            continue
        if prev_p and p - prev_p > 1:
            buttons_html += '<span class="pagination__ellipsis">…</span>'
        active_cls  = " pagination__btn--active" if p == page else ""
        onclick_str = f' onclick="{on_change}({p})"' if on_change else ""
        buttons_html += f'<button class="pagination__btn{active_cls}"{onclick_str}>{p}</button>'
        prev_p = p

    prev_disabled = " disabled" if page <= 1 else ""
    next_disabled = " disabled" if page >= total_pages else ""
    prev_onclick  = f' onclick="{on_change}({page - 1})"' if on_change and page > 1 else ""
    next_onclick  = f' onclick="{on_change}({page + 1})"' if on_change and page < total_pages else ""

    return f'''
<div class="pagination">
    <span class="pagination__info">Showing {start}–{end} of {total}</span>
    <div class="pagination__controls">
        <button class="pagination__btn pagination__btn--nav"{prev_onclick}{prev_disabled}>
            <i data-lucide="chevron-left" style="width:14px;height:14px;"></i>
        </button>
        {buttons_html}
        <button class="pagination__btn pagination__btn--nav"{next_onclick}{next_disabled}>
            <i data-lucide="chevron-right" style="width:14px;height:14px;"></i>
        </button>
    </div>
</div>'''


def render_code_block(props, children):
    content      = props.get("content", "")
    language     = props.get("language", "python")
    filename     = props.get("filename")
    line_numbers = props.get("line_numbers", True)

    content_escaped = (content
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;"))

    header_left  = f'<span class="bq-codeblock-filename">{filename}</span>' if filename else '<span></span>'
    header_right = f'<span class="bq-codeblock-lang">{language}</span>'
    uid = f"ln-{abs(hash(content)) % 99999}"

    if line_numbers:
        ln_div = f'<div class="bq-line-numbers" id="{uid}"></div>'
        js_body = f'''
  var el = document.getElementById("{uid}");
  var code = el.nextElementSibling.querySelector("code");
  if (!el || !code) return;
  var lines = code.textContent.split("\\n").length;
  el.innerHTML = Array.from({{length: lines}}, function(_, i) {{ return "<span>" + (i+1) + "</span>"; }}).join("");
  if (window.Prism) Prism.highlightElement(code);'''
    else:
        ln_div = ''
        js_body = '''
  var code = document.currentScript.previousElementSibling.querySelector("code");
  if (!code) return;
  if (window.Prism) Prism.highlightElement(code);'''

    return f'''
<div class="bq-codeblock">
  <div class="bq-codeblock-header">
    {header_left}
    {header_right}
  </div>
  <div class="bq-codeblock-inner">
    {ln_div}
    <pre class="language-{language}" style="margin:0;border:none!important;border-radius:0!important;"><code class="language-{language}">{content_escaped}</code></pre>
  </div>
</div>
<script>
(function() {{{js_body}
}})();
</script>'''

def render_rich_text(props, children):
    name        = props.get("name", "content")
    label       = props.get("label")
    placeholder = props.get("placeholder", "Write something...")
    value       = props.get("value", "")

    label_html = f'<label class="form-label">{label}</label>' if label else ""
    uid        = f"rte-{abs(hash(name)) % 99999}"

    return f'''
<div class="form-field">
  {label_html}
  <div class="bq-rte-wrap">
    <div class="bq-rte-toolbar">
      <select class="bq-rte-select" onchange="rteHeading(this, '{uid}')">
        <option value="">Paragraph</option>
        <option value="h1">Heading 1</option>
        <option value="h2">Heading 2</option>
        <option value="h3">Heading 3</option>
      </select>
      <div class="bq-rte-sep"></div>
      <button class="bq-rte-btn" type="button" title="Bold" onclick="rteExec('bold', '{uid}')"><b>B</b></button>
      <button class="bq-rte-btn" type="button" title="Italic" onclick="rteExec('italic', '{uid}')"><i>I</i></button>
      <button class="bq-rte-btn" type="button" title="Strikethrough" onclick="rteExec('strikeThrough', '{uid}')"><s>S</s></button>
      <div class="bq-rte-sep"></div>
      <button class="bq-rte-btn" type="button" title="Bullet list" onclick="rteExec('insertUnorderedList', '{uid}')">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="9" y1="6" x2="20" y2="6"/><line x1="9" y1="12" x2="20" y2="12"/><line x1="9" y1="18" x2="20" y2="18"/><circle cx="4" cy="6" r="1.5" fill="currentColor"/><circle cx="4" cy="12" r="1.5" fill="currentColor"/><circle cx="4" cy="18" r="1.5" fill="currentColor"/></svg>
      </button>
      <button class="bq-rte-btn" type="button" title="Ordered list" onclick="rteExec('insertOrderedList', '{uid}')">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="10" y1="6" x2="21" y2="6"/><line x1="10" y1="12" x2="21" y2="12"/><line x1="10" y1="18" x2="21" y2="18"/><text x="2" y="9" fill="currentColor" stroke="none" font-size="8" font-family="monospace">1.</text><text x="2" y="21" fill="currentColor" stroke="none" font-size="8" font-family="monospace">2.</text></svg>
      </button>
      <button class="bq-rte-btn" type="button" title="Blockquote" onclick="rteBlockquote('{uid}')">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z"/><path d="M15 21c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z"/></svg>
      </button>
      <div class="bq-rte-sep"></div>
      <button class="bq-rte-btn" type="button" title="Inline code" onclick="rteInlineCode('{uid}')">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
      </button>
      <button class="bq-rte-btn" type="button" title="Code block" onclick="rteCodeBlock('{uid}')">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="9" y1="9" x2="15" y2="9"/><line x1="9" y1="13" x2="13" y2="13"/></svg>
      </button>
      <button class="bq-rte-btn" type="button" title="Link" onclick="rteLink('{uid}')">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg>
      </button>
    </div>
    <div class="bq-rte-editor" id="{uid}" contenteditable="true" data-placeholder="{placeholder}"></div>
    <div class="bq-rte-footer">
      <span class="bq-rte-charcount" id="{uid}-count">0 chars</span>
    </div>
  </div>
  <input type="hidden" id="{uid}-hidden" name="{name}" value="{value}" />
</div>
<script>
(function() {{
  var editor = document.getElementById("{uid}");
  var hidden = document.getElementById("{uid}-hidden");
  var counter = document.getElementById("{uid}-count");
  if (editor) {{
    editor.addEventListener("input", function() {{
      var md = burqHtmlToMarkdown(editor.innerHTML);
      if (hidden) hidden.value = md;
      if (counter) counter.textContent = editor.innerText.replace(/\\n/g, "").length + " chars";
    }});
  }}
}})();
</script>'''

# ── BASE TEMPLATE ──

def render_base_template(app) -> str:
    theme      = app.theme
    layout     = app.layout
    nav        = app._nav
    nav_footer = app._nav_footer
    prism_theme = (
    "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css"
    if theme.mode == "light" else
    "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css"
    )

    bordered   = getattr(layout, 'bordered', False)
    layout_cls = "layout"
    if layout.sidebar: layout_cls += " layout--with-sidebar"
    if layout.topbar:  layout_cls += " layout--with-topbar"
    if bordered:       layout_cls += " layout--bordered"

    def _render_nav_item(item) -> str:
        if isinstance(item, NavGroup):
            open_cls  = " nav-group--open" if item.default_open else ""
            children_html = "".join(_render_nav_item(c) for c in item.children)
            icon_html = f'<i data-lucide="{item.icon}" class="nav-item__icon"></i>' if item.icon else ""
            return f'''
            <div class="nav-group{open_cls}">
                <button class="nav-group__trigger" type="button">
                    {icon_html}
                    <span class="nav-item__label">{item.label}</span>
                    <i data-lucide="chevron-right" class="nav-group__chevron"></i>
                </button>
                <div class="nav-group__children">
                    {children_html}
                </div>
            </div>'''
        else:
            icon_html = f'<i data-lucide="{item.icon}" class="nav-item__icon"></i>' if item.icon else ""
            return f'''
            <a class="nav-item" href="{item.href}" data-href="{item.href}">
                {icon_html}
                <span class="nav-item__label">{item.label}</span>
            </a>'''

    nav_html = "".join(_render_nav_item(item) for item in nav)
    nav_footer_html = "".join(_render_nav_item(item) for item in nav_footer)

    logo_html = render_logo(app.logo)

    sidebar_html = ""
    if layout.sidebar:
        sidebar_html = f'''
  <aside class="sidebar" id="sidebar">
    <nav class="sidebar__nav">{nav_html}</nav>
    <div class="sidebar__footer">{nav_footer_html}</div>
  </aside>'''
    sidebar_toggle = ""
    if layout.sidebar:
        sidebar_toggle = '<button class="topbar__toggle" id="sidebarToggle"><i data-lucide="menu" class="topbar__icon"></i></button>'
    topbar_html = ""
    if layout.topbar:
        theme_toggle = ""
        if theme.toggle:
            theme_toggle = '''
            <button class="topbar__toggle" id="themeToggle" title="Toggle theme">
                <i data-lucide="sun" class="topbar__icon" id="themeIcon"></i>
            </button>'''
            
        title_html = f'<span class="topbar__app-title">{app.title}</span>' if layout.show_title else ""

        topbar_html = f'''
  <header class="topbar">
    <div class="topbar__left">
        {sidebar_toggle}
        {logo_html}
        {title_html}
    </div>
    <div class="topbar__right">
        {theme_toggle}
    </div>
  </header>'''
        
    return f'''<!DOCTYPE html>
<html lang="en" data-theme="{theme.mode}">
<head>
  <meta charset="UTF-8" />
  <script>(function(){{var t=localStorage.getItem("burq-theme");if(t)document.documentElement.setAttribute("data-theme",t);}})()</script>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="generator" content="Burq ⚡ — https://burq.dev" />
  {f'<meta name="author" content="{app.author}" />' if app.author else ""}
  <title>{{% block page_title %}}{app.title}{{% endblock %}}</title>
  <link rel="stylesheet" href="/static/tokens.css" />
  <link rel="stylesheet" href="/static/layout.css" />
  <link rel="stylesheet" href="/static/components.css" />
  <script src="https://unpkg.com/lucide@latest"></script>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" />
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-javascript.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-json.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-markup.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>

  <style>
    .nav-item__icon      {{ width: 18px; height: 18px; flex-shrink: 0; }}
    .topbar__icon        {{ width: 18px; height: 18px; }}
    .topbar__app-title   {{ font-size: var(--text-md); font-weight: 700; letter-spacing: -0.02em; color: var(--foreground); }}
    .page-title          {{ font-size: var(--text-2xl); font-weight: 700; color: var(--foreground); letter-spacing: -0.02em; margin-bottom: var(--space-4); }}
    .page-heading        {{ font-size: var(--text-xl); font-weight: 600; color: var(--foreground); letter-spacing: -0.01em; margin-bottom: var(--space-3); }}
    .body-text           {{ font-size: var(--text-base); color: var(--foreground); }}
    .muted-text          {{ font-size: var(--text-base); color: var(--muted-foreground); }}
  </style>
</head>
<body>
<div class="{layout_cls}" id="layout">
  {topbar_html}
  {sidebar_html}
  <main class="content">
    <div style="padding: var(--space-6);">
      {{% block content %}}{{% endblock %}}
    </div>
  </main>
</div>

{{% block modals %}}{{% endblock %}}

<script src="/static/burq.js"></script>
</body>
</html>'''


def render_page_template(page_content: str, modal_content: str = "", url_pattern: str = "", page_title: str = "", app_title: str = "") -> str:
    param_script = ""
    if "{" in url_pattern:
        js = (
            "(function() {\n"
            "  var pattern = \"" + url_pattern + "\";\n"
            "  var path    = window.location.pathname;\n"
            "  var keys    = [];\n"
            "  var regexStr = pattern.replace(/\\{(\\w+)\\}/g, function(_, k) { keys.push(k); return \"([^/]+)\"; });\n"
            "  var match   = path.match(new RegExp(\"^\" + regexStr + \"$\"));\n"
            "  if (match) {\n"
            "    window.__burqParams = {};\n"
            "    keys.forEach(function(k, i) { window.__burqParams[k] = match[i+1]; });\n"
            "  }\n"
            "})();"
        )
        param_script = "<script>\n" + js + "\n</script>"

    resolved_title = page_title if page_title else app_title

    return f"""{{% extends "base.html" %}}
{{% block page_title %}}{resolved_title}{{% endblock %}}
{{% block content %}}
{param_script}
{page_content}
{{% endblock %}}
{{% block modals %}}
{modal_content}
{{% endblock %}}"""