# burq — LLM Context Reference

> burq (بُرق) is a Python UI compiler. You write Python. It compiles to Vanilla JS + HTML + CSS static files. No JS, no framework, no runtime server.

Version: **v0.2.1** | `pip install burq` | Python 3.10+

---

## Mental Model

```
app.py  →  burq build  →  dist/
                           ├── templates/base.html
                           ├── templates/index.html
                           └── static/
                               ├── burq.js
                               ├── tokens.css
                               ├── layout.css
                               └── components.css
```

- Python runs **only at compile time** — not in the browser
- Output is **pure static files** — no WASM, no Python in browser
- FastAPI (or any server) owns routing and data APIs
- Browser JS reads URL params and fetches from your API at runtime
- `compile_app()` must be wrapped in `if __name__ == "__main__"` to prevent double-compilation when CLI loads `app.py` via importlib

---

## Quickstart

```python
import burq as bq
from burq.compiler import compile_app

app = bq.App(
    title="My App",
    api_base="http://localhost:8000/api",
    theme=bq.Theme(mode="dark", toggle=True),
)

app.nav([
    bq.NavItem("Dashboard", icon="layout-dashboard", href="/"),
    bq.NavItem("Users",     icon="users",            href="/users"),
])

@app.page("/")
def dashboard():
    bq.title("Dashboard")
    bq.metric("Total Users", "1,240", trend="+12%", trend_dir="up")

if __name__ == "__main__":
    compile_app(app, output_dir="dist")
```

```bash
pip install burq
burq new my-app   # scaffold project
burq build        # compile app.py → dist/
burq dev          # watch + recompile on save
```

---

## App & Layout

```python
app = bq.App(
    title    = "My App",       # browser tab title + topbar wordmark
    api_base = "https://...",  # prefix for all bq.fetch() calls
    api_key  = "",             # optional — sent as Authorization header
    theme    = bq.Theme(...),
    layout   = bq.Layout(...),
    logo     = "default",      # "default" | None | SVG string | file path
)

bq.Layout(
    sidebar    = True,   # show sidebar nav
    topbar     = True,   # show topbar
    bordered   = False,  # chrome borders
    show_title = False,  # text title next to logo
)
```

### Navigation

```python
app.nav(
    items=[
        bq.NavItem("Dashboard", icon="layout-dashboard", href="/"),
        bq.NavGroup("Reports", icon="bar-chart", children=[
            bq.NavItem("Monthly",  href="/reports/monthly"),
            bq.NavItem("Annually", href="/reports/annual"),
        ], default_open=False),
    ],
    footer=[
        bq.NavItem("Settings", icon="settings", href="/settings"),
    ]
)
```

### Pages & Dynamic Routes

```python
@app.page("/")
def index():
    ...

@app.page("/users/{user_id}")
def user_detail(user_id):
    # user_id is a string token at compile time: "{user_id}"
    # at runtime JS extracts the real value from the URL
    bq.contact_profile(endpoint="/users/{user_id}")
    bq.table(data=bq.fetch("GET", "/users/{user_id}/orders"), ...)
```

**Gotcha:** Dynamic route params are string tokens at compile time. Never try to use them as real Python values — only pass them inside endpoint strings for `bq.fetch()` and `bq.contact_profile()`.

---

## Theme

```python
bq.Theme(
    mode            = "dark",          # "light" | "dark"
    toggle          = True,            # theme toggle in topbar
    font_sans       = "Space Grotesk",
    font_mono       = "Space Mono",
    font_size_base  = 14,
    radius          = "md",            # "none"|"sm"|"md"|"lg"|"xl"
    border_width    = 1,
    shadow_strength = "md",
    spacing_unit    = 4,

    # Filament theme defaults (canonical):
    dark_background         = "#0a0a0b",
    dark_surface            = "#111113",
    dark_surface_raised     = "#1e1e22",
    dark_muted              = "#1e1e22",
    dark_muted_foreground   = "#8a8a93",
    dark_accent             = "#F08C1A",
    dark_accent_foreground  = "#0a0a0b",
    dark_border             = "#2a2a2e",
    dark_chrome             = "#111113",
    dark_chrome_foreground  = "#8a8a93",

    light_background        = "#fef9ed",
    light_surface           = "#fff",
    light_muted             = "#f5ecd6",
    light_muted_foreground  = "#5c4d2e",
    light_accent            = "#F08C1A",
    light_border            = "#ebe0c2",

    color_success           = "#1a7a3c",
    color_success_dark      = "#2ec97a",
    color_error             = "#c92e2e",
    color_error_dark        = "#e05252",

    chart_colors = ["#F08C1A","#60a5fa","#2ec97a","#e05252","#c97a2e","#a78bfa","#f472b6"],
)
```

**Gotcha:** `@media (prefers-color-scheme)` does NOT evaluate inside SVGs loaded as `<img>` tags. Use `bq.image(src="light.svg", src_dark="dark.svg")` for theme-aware images.

---

## Layout Components

All layout components are **context managers** (use `with`).

```python
with bq.row(gap="md", align="center", justify="start", wrap=True, nowrap=False):
    ...
# gap: none|sm|md|lg   align: start|center|end|stretch   justify: start|center|end|between

with bq.col(gap="md", align="stretch", justify="start"):
    ...

with bq.grid(cols=4, gap="md", row_gap=None, col_gap=None):
    # cols: 1|2|3|4|6|12
    with bq.span(cols=2):  # grid column span
        ...

with bq.card(title="Card Title", subtitle=None, variant="default", size="md", footer=False):
    # variant: default|raised|flat|ghost   size: sm|md|lg
    ...

with bq.box(background="muted", border=True, radius="lg", padding="md", foreground=None, full_width=False):
    # background: muted|surface|surface_raised|background  (or any CSS value)
    # radius: none|sm|md|lg|xl   padding: none|sm|md|lg
    ...

with bq.container(size="lg"):  # size: sm|md|lg|xl|full
    ...

bq.divider(size=None, vertical=False)
bq.spacer(size="md")   # size: sm|md|lg|xl
bq.grow()              # flex-grow spacer — pushes siblings apart inside row/col
```

---

## Display Components

Leaf nodes — called directly, not used as context managers.

```python
bq.title(text, color=None, size=None)
bq.heading(text, color=None, size=None)
bq.text(content, muted=False, color=None, size=None)

bq.metric(
    label,
    value,
    trend     = None,      # e.g. "+12%"
    trend_dir = None,      # "up"|"down"|"flat"
    icon      = None,      # Lucide icon name
    variant   = "default"  # "default"|"accent"|"ghost"
)

bq.badge(text, variant="default", size="md", dot=False)
# variant: default|accent|success|warning|danger|info   size: sm|md|lg

bq.avatar(initials="", src=None, size="md", variant="square", status=None, color="accent")
# size: xs|sm|md|lg|xl   variant: square|round   status: online|offline|away

bq.avatar_group(avatars=[{"initials":"AB","color":"accent"}, ...], overflow=0)

bq.progress(label=None, value=0, variant="default", size="md", striped=False, animated=False)
# variant: default|success|warning|danger

bq.skeleton(variant="text", width=None, height=None)
# variant: text|text-sm|text-lg|avatar-sm|avatar-md|avatar-lg|button|rect

bq.spinner(size="md", color="accent")
# size: sm|md|lg   color: accent|muted|white

bq.icon(name, size="md", color=None, label=None)

bq.image(src, alt="", src_dark=None, width=None, height=None, radius="md", caption=None, fit="cover")
# src_dark: alternate image path used when dark theme is active

bq.link(label, href="#", icon=None, external=False, muted=False, size=None, onclick=None)

bq.breadcrumb(items=[bq.BreadcrumbItem("Home", href="/"), bq.BreadcrumbItem("Users")], separator="chevron")
# separator: chevron|slash

bq.empty_state(title, message="", icon="inbox", action={"label":"Add Item","onclick":"..."})
```

---

## Form Components

```python
bq.input(
    label, placeholder=None, type="text",  # text|email|password|number
    value=None, required=False, disabled=False,
    size="md", icon=None, icon_pos="left",  # icon_pos: left|right
    error=None, helper=None, name=None
)

bq.textarea(label, placeholder=None, value=None, required=False, disabled=False,
            error=None, helper=None, name=None, rows=3)

bq.select(
    label, options=[],  # list of str or dicts
    value=None, placeholder="Select...",
    label_key=None, value_key=None,   # for dict option lists
    searchable=False, required=False, disabled=False,
    size="md", error=None, helper=None, name=None,
    depends_on=None   # name of another select this one depends on
)

bq.toggle(label, checked=False, disabled=False, name=None)
# alias: value=False also works

bq.checkbox(label, value=False, disabled=False, name=None)

bq.radio(label, name=None, value=None, checked=False, disabled=False)

bq.button(
    label, variant="primary",  # primary|secondary|ghost|outline|danger|link
    size="md",                 # xs|sm|md|lg
    icon=None, icon_pos="left",
    disabled=False, loading=False,
    onclick=None,  # JS expression string
    type="button", name=None,
    href=None, external=False  # href used when variant="link"
)

bq.file_upload(label=None, accept=None, name=None, helper=None, error=None)
```

---

## Data Components

### Table

```python
bq.table(
    data          = bq.fetch("GET", "/items/"),  # or static list
    columns       = ["name", "status", "value"],
    column_config = {
        "name":   bq.AvatarColumn(initials_key="name", sub_key="email"),
        "status": bq.BadgeColumn(variant_map={"active":"success","inactive":"danger"}),
        "value":  bq.CurrencyColumn(prefix="$", decimals=2),
        "date":   bq.DateColumn(format="%b %d, %Y"),
        "active": bq.BoolColumn(true_label="Yes", false_label="No",
                                true_variant="success", false_variant="danger"),
        "notes":  bq.TextColumn(muted=True),
    },
    searchable  = False,
    sortable    = False,
    checkable   = False,   # row checkboxes
    striped     = False,
    pagination  = True,
    page_size   = 10,
    row_href    = "/items/{id}",   # {field} tokens from row data
    actions     = [
        bq.TableAction(label="Edit",   icon="edit",    variant="default", onclick="alert('{id}')"),
        bq.TableAction(label="Delete", icon="trash-2", variant="danger",  onclick="deleteItem('{id}')"),
    ],
    empty_title   = "No items",
    empty_message = "Create one to get started.",
    empty_icon    = "inbox",
)
```

**Gotcha:** Single or double quotes inside static table data values break JSON serialization. Use plain descriptions (e.g. `"empty string"` not `"''"`) for static data in table rows.

### Charts

All charts accept: static list, pandas DataFrame, or `bq.fetch()`.

```python
bq.bar_chart(data, x="month", y=["revenue","expenses"], title=None, stacked=False, height=300)

bq.line_chart(data, x="date", y="value",  title=None, smooth=False, height=300)
# y can be str or list[str]

bq.area_chart(data, x="date", y="value",  title=None, smooth=True,  height=300)

bq.donut_chart(data, label="category", value="count", title=None, height=300)
```

Chart colors come from `Theme(chart_colors=[...])`. Chart.js 4.4 is auto-injected via CDN at compile time.

---

## Feedback Components

```python
bq.alert(message, type="info", title=None, dismiss=True)
# type: success|error|warning|info

bq.toast(title, message=None, type="info", duration=3000)
# duration in ms; 0 = no auto-dismiss

with bq.modal(id="confirm-modal", title="Confirm Action", size="md"):
    # size: sm|md|lg
    with bq.modal_body():
        bq.text("Are you sure?")
    with bq.modal_footer():
        bq.button("Cancel",  variant="secondary", onclick=bq.close_modal("confirm-modal"))
        bq.button("Confirm", variant="danger",    onclick="doAction()")

# Trigger a modal:
bq.button("Open", onclick=bq.open_modal("confirm-modal"))
```

---

## Navigation Components

```python
with bq.tabs(items=["Tab A","Tab B"], variant="default", icons=None, badges=None):
    # variant: default|pills|card
    with bq.tab("Tab A"):
        bq.text("Content A")
    with bq.tab("Tab B"):
        bq.text("Content B")

bq.dropdown(
    trigger=...,         # any component rendered as the trigger
    items=[
        bq.DropdownItem("Edit",   icon="edit"),
        bq.DropdownDivider(),
        bq.DropdownLabel("Danger Zone"),
        bq.DropdownItem("Delete", icon="trash-2", danger=True, onclick="deleteItem()"),
    ],
    align="right"        # right|left
)
```

---

## Extra Components

```python
bq.accordion(
    items=[
        {"title": "Question?", "content": "Answer.", "open": False},
    ],
    multiple=False   # allow multiple open at once
)

bq.markdown(content="# Hello\n\nSome **markdown** content.")

bq.code_block(content="print('hello')", language="python", filename="app.py", line_numbers=True)

bq.rich_text(name="body", label="Content", placeholder="Write something...", value=None)

bq.contact_profile(endpoint="/users/{user_id}")
# Fetches and renders a profile card from API response

bq.pagination(total=100, page=1, per_page=10, on_change="")

bq.script(code="console.log('custom JS')")
# Emits a raw <script> block into the page
```

---

## API Helpers

```python
# Fetch descriptor — compiles to JS fetch() at runtime
bq.fetch("GET",  "/endpoint")
bq.fetch("POST", "/endpoint", data={"key": "value"})
bq.post("/endpoint", data={...})   # shorthand for fetch POST

# Modal control — returns JS expression strings for use in onclick=
bq.open_modal("modal-id")    # → "ModalManager.open('modal-id')"
bq.close_modal("modal-id")   # → "ModalManager.close('modal-id')"
bq.close_modal()             # → closes topmost open modal

# Navigation — returns JS expression strings
bq.navigate("/path")         # → "burq.navigate('/path')"
bq.reload()                  # → "burq.reload()"
```

---

## Icons

burq uses **Lucide icons** exclusively. Pass the kebab-case icon name string anywhere an `icon=` param is accepted.

Examples: `"layout-dashboard"`, `"users"`, `"settings"`, `"trash-2"`, `"alert-triangle"`, `"check-circle"`, `"external-link"`

**Gotcha:** GitHub icon is not in Lucide — use `"external-link"` as replacement.

---

## FastAPI Integration

```python
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

server = FastAPI()
server.mount("/static", StaticFiles(directory="dist/static"), name="static")
templates = Jinja2Templates(directory="dist/templates")

@server.get("/")
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"page_title": "Home"})

@server.get("/users/{user_id}")
def user_detail(request: Request, user_id: int):
    return templates.TemplateResponse(request, "users_user_id.html", {"page_title": "User"})
```

**Template naming convention:** slashes become underscores, hyphens stay as hyphens.
- `/` → `index.html`
- `/users/{user_id}` → `users_user_id.html`
- `/get-started/installation` → `get-started_installation.html`

---

## Project Structure

```
my-app/
├── app.py                  # single entry point — all pages defined here
├── pages/                  # optional: split pages into separate files
│   └── dashboard.py
├── components/             # optional: reusable component functions
│   └── header.py
└── dist/                   # compiled output (gitignored)
    ├── templates/
    └── static/
```

`burq dev` watches `app.py`, `pages/`, and `components/` directories.

---

## Gotchas & Corner Cases

| Issue | Cause | Fix |
|---|---|---|
| `unexpected keyword argument` | Stale pip install | `pip install -e .` during dev |
| Double compilation on `burq dev` | `compile_app()` at module level | Wrap in `if __name__ == "__main__"` |
| Table data breaks JSON | Quotes inside static string values | Avoid `'` or `"` inside static data values |
| Dark/light SVG not switching | `@media prefers-color-scheme` fails inside `<img>` | Use `bq.image(src_dark=...)` with two SVG files |
| Dynamic param value is `"{user_id}"` not real | Compile-time execution | Expected — only use params inside endpoint strings |
| Module not found in `burq dev` | Module cache | burq purges `pages.*`, `components.*`, `_burq_app` from `sys.modules` before recompile |
| GitHub icon missing | Not in Lucide | Use `"external-link"` icon instead |
| `area_chart` not recognized | Missing `__init__.py` export | Ensure burq is reinstalled after any manual additions |
| Chart colors wrong | `chart_colors` not set on Theme | Pass `chart_colors=[...]` to `bq.Theme()` |

---

## What Burq Is NOT For

- Reactive apps with complex client-side state (no two-way binding)
- Real-time features: chat, live dashboards, WebSockets, SSE push
- Optimistic UI or state that changes without a server round-trip
- Replacing React/Vue for highly interactive consumer UIs

Burq is a compiler. If your UI needs to react to state changes without fetching from an API, it is the wrong tool.

---

## Compiler Architecture (Internal)

```
burq/
├── compiler/
│   ├── __init__.py      # compile_app() — orchestrates pipeline
│   ├── html_gen.py      # component tree → HTML (large file — prefer surgical edits)
│   ├── js_gen.py        # generates burq.js runtime
│   └── css_gen.py       # generates tokens.css + layout.css + components.css
├── components/
│   ├── layout.py        # row, col, grid, card, box, spacer, divider, grow
│   ├── display.py       # title, text, metric, badge, avatar, progress, image, icon, link
│   ├── forms.py         # input, textarea, select, toggle, checkbox, radio, button, file_upload
│   ├── feedback.py      # modal, alert, toast
│   ├── navigation.py    # tabs, tab, dropdown, NavItem, NavGroup, breadcrumb
│   ├── data.py          # table, fetch, charts, column configs, TableAction
│   └── extra.py         # accordion, empty_state, pagination, markdown, code_block, contact_profile, script
├── theme/
│   ├── theme.py         # Theme dataclass
│   └── compiler.py      # CSS variable generation
├── app.py               # App + Layout dataclasses, error reporter
├── context.py           # component tree context manager
└── cli/main.py          # burq new | build | dev
```

Pipeline:
1. Load `app.py` → execute decorators → populate `app._pages`
2. Each `@app.page` → one Jinja2 template via `render_node()`
3. Generate `burq.js` — fetch wrapper, table hydration, modals, toasts, tabs, theme toggle
4. Generate CSS — `tokens.css` (design tokens), `layout.css`, `components.css`
5. Output `dist/templates/` + `dist/static/`