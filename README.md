# burq ⚡

> Write Python. Ship UI.

[![PyPI](https://img.shields.io/pypi/v/burq)](https://pypi.org/project/burq)
[![GitHub](https://img.shields.io/badge/github-itsdaniyalm%2Fburq-black)](https://github.com/itsdaniyalm/burq)
[![Docs](https://img.shields.io/badge/docs-burq.dev-orange)](https://burq.dev)

burq is a Python UI compiler. Write your frontend in Python and burq compiles it to pure Vanilla JS + HTML + CSS. No JavaScript. No framework. No runtime server.

```bash
pip install burq
burq new my-app
cd my-app
burq build
```

---

## How it works

```
app.py  →  burq build  →  dist/
                           ├── templates/
                           │   ├── base.html
                           │   └── index.html
                           └── static/
                               ├── burq.js
                               ├── tokens.css
                               ├── layout.css
                               └── components.css
```

You write Python. burq compiles it. Your backend serves the output.

---

## Quickstart

```bash
pip install burq
burq new my-app
cd my-app
burq build
```

Point your FastAPI (or any server) at `dist/`:

```python
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="dist/static"), name="static")
templates = Jinja2Templates(directory="dist/templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"page_title": "Home"})
```

---

## Example

```python
import burq as bq
from burq.compiler import compile_app

app = bq.App(
    title="My CRM",
    api_base="http://localhost:8000/api",
    theme=bq.Theme(mode="dark", toggle=True),
)

app.nav([
    bq.NavItem("Dashboard", icon="layout-dashboard", href="/"),
    bq.NavGroup("Contacts", icon="users", children=[
        bq.NavItem("All Contacts", href="/contacts"),
        bq.NavItem("Import",       href="/contacts/import"),
    ]),
    bq.NavItem("Deals", icon="circle-dollar-sign", href="/deals"),
])

@app.page("/")
def dashboard():
    bq.title("Dashboard")

    with bq.grid(cols=4):
        with bq.span(cols=1):
            bq.metric("Contacts", "2,480", trend="+12%", trend_dir="up")
        with bq.span(cols=1):
            bq.metric("Deals", "143", trend="-4%", trend_dir="down")

    bq.spacer()

    bq.bar_chart(
        data=bq.fetch("GET", "/stats/revenue"),
        x="month",
        y=["revenue", "expenses"],
        title="Revenue vs Expenses",
    )

    bq.spacer()

    bq.table(
        data=bq.fetch("GET", "/contacts/"),
        columns=["name", "company", "status"],
        column_config={
            "name":   bq.AvatarColumn(sub_key="email"),
            "status": bq.BadgeColumn(variant_map={
                "lead": "default", "qualified": "info", "won": "success",
            }),
        },
        searchable=True,
        sortable=True,
        row_href="/contacts/{id}",
    )


@app.page("/contacts/{contact_id}")
def contact_detail(contact_id):
    bq.contact_profile(endpoint="/contacts/{contact_id}")
    bq.spacer()

    with bq.tabs(["Deals", "Activities"]):
        with bq.tab("Deals"):
            bq.table(
                data=bq.fetch("GET", "/contacts/{contact_id}/deals"),
                columns=["title", "status", "value"],
                column_config={
                    "value": bq.CurrencyColumn(prefix="$", decimals=2),
                },
            )


compile_app(app, output_dir="dist")
```

---

## CLI

```bash
burq new my-app      # scaffold a new project
burq build           # compile app.py → dist/
burq dev             # watch for changes and recompile
```

`burq dev` watches `app.py`, `pages/`, and `components/` and recompiles on every save.

---

## Components

### Layout
```python
bq.row()             # horizontal flex row
bq.col()             # vertical flex column
bq.grid(cols=3)      # css grid
bq.span(cols=2)      # grid column span
bq.card("Title")     # card container
bq.tabs(["A", "B"])  # tabbed container
bq.tab("A")          # tab panel
bq.divider()
bq.spacer(size="md")
with bq.box(background="muted", border=True, radius="lg"):
    ...
```

### Display
```python
bq.title("Page Title")
bq.heading("Section")
bq.text("Body text", muted=True)
bq.metric("Revenue", "$84k", trend="+12%", trend_dir="up")
bq.badge("Active", variant="success")
bq.avatar(initials="AB")
bq.progress("Completion", value=72)
bq.markdown("## Hello\n**bold** text")
bq.spinner()
bq.skeleton(variant="text")
```

### Data
```python
bq.table(
    data=bq.fetch("GET", "/items/"),
    columns=["name", "status", "value"],
    column_config={
        "status": bq.BadgeColumn(variant_map={"active": "success"}),
        "value":  bq.CurrencyColumn(prefix="$"),
    },
    searchable=True,
    sortable=True,
    row_href="/items/{id}",
)
```

### Charts
```python
# static data or bq.fetch() , both work
bq.bar_chart(data=df, x="month", y="revenue", title="Revenue", height=300)
bq.bar_chart(data=bq.fetch("GET", "/stats"), x="month", y=["revenue", "expenses"])  # grouped
bq.line_chart(data=bq.fetch("GET", "/trends"), x="date", y=["signups", "churns"], smooth=True)
bq.area_chart(data=bq.fetch("GET", "/revenue"), x="month", y="revenue")
bq.donut_chart(data=bq.fetch("GET", "/breakdown"), label="status", value="count")
```

### Navigation
```python
# flat
bq.NavItem("Dashboard", icon="layout-dashboard", href="/")

# grouped with sub-pages (auto-opens on URL match)
bq.NavGroup("Contacts", icon="users", children=[
    bq.NavItem("All Contacts", href="/contacts"),
    bq.NavItem("Import",       href="/contacts/import"),
])
```

### Forms
```python
bq.input("Email", type="email", icon="mail")
bq.textarea("Notes", rows=4)
bq.select("Status", options=["Lead", "Won"], searchable=True)
bq.toggle("Enable notifications", checked=True)
bq.checkbox("Agree to terms")
bq.file_upload("CSV File", accept=".csv", helper="Max 10MB")
bq.button("Save", variant="primary", icon="save")
```

### Feedback
```python
bq.alert("Saved successfully", type="success")
bq.accordion(items=[
    {"title": "What is burq?", "content": "A Python UI compiler."},
])
bq.empty_state(title="No data", message="Add something to get started.", icon="inbox")
```

### API
```python
bq.fetch("GET", "/items/")                  # GET request
bq.fetch("POST", "/items/", data={...})     # POST request
bq.open_modal("my-modal")                   # open modal
bq.close_modal("my-modal")                  # close modal
```

---

## Column Config

| Type | Usage |
|---|---|
| `AvatarColumn(sub_key="email")` | Avatar with initials + subtitle |
| `BadgeColumn(variant_map={...})` | Colored badge by value |
| `CurrencyColumn(prefix="$", decimals=2)` | Formatted currency |
| `DateColumn()` | Formatted date |
| `BoolColumn(true_label="Yes")` | Boolean as badge |
| `TextColumn(muted=True)` | Plain text, optional muted |

---

## Theme

```python
bq.Theme(
    # ── Mode ──
    mode="dark",              # "light" | "dark"
    toggle=True,              # show theme toggle in topbar

    # ── Typography ──
    font_sans="Space Grotesk",
    font_mono="Space Mono",
    font_size_base=14,        # base px, all sizes scale from this

    # ── Shape ──
    radius="md",              # "none" | "sm" | "md" | "lg" | "xl" | "2xl"
    spacing_unit=4,           # base spacing unit in px
    border_width=1,           # border width in px
    shadow_strength="md",     # "none" | "sm" | "md" | "lg"

    # ── Charts ──
    chart_colors=[
        "#F08C1A",            # accent , always first
        "#60a5fa",
        "#2ec97a",
        "#e05252",
        "#c97a2e",
        "#a78bfa",
        "#f472b6",
    ],
)
```

### Light theme overrides

| Parameter | Default | Usage |
|---|---|---|
| `light_background` | `#fef9ed` | Page background |
| `light_foreground` | `#1a140a` | Primary text |
| `light_surface` | `#ffffff` | Cards, inputs |
| `light_surface_raised` | `#ffffff` | Modals, dropdowns |
| `light_muted` | `#f5ecd6` | Subtle backgrounds |
| `light_muted_foreground` | `#5c4d2e` | Secondary text, icons |
| `light_accent` | `#F08C1A` | Primary action color |
| `light_accent_foreground` | `#ffffff` | Text on accent |
| `light_border` | `#ebe0c2` | Borders |
| `light_chrome` | `#ffffff` | Topbar, sidebar background |
| `light_chrome_foreground` | `#5c4d2e` | Nav text |
| `light_chrome_border` | `#ebe0c2` | Chrome borders |

### Dark theme overrides

| Parameter | Default | Usage |
|---|---|---|
| `dark_background` | `#0a0a0b` | Page background |
| `dark_foreground` | `#ededee` | Primary text |
| `dark_surface` | `#111113` | Cards, inputs |
| `dark_surface_raised` | `#1e1e22` | Modals, dropdowns |
| `dark_muted` | `#1e1e22` | Subtle backgrounds |
| `dark_muted_foreground` | `#8a8a93` | Secondary text, icons |
| `dark_accent` | `#F08C1A` | Primary action color |
| `dark_accent_foreground` | `#0a0a0b` | Text on accent |
| `dark_border` | `#2a2a2e` | Borders |
| `dark_chrome` | `#111113` | Topbar, sidebar background |
| `dark_chrome_foreground` | `#8a8a93` | Nav text |
| `dark_chrome_border` | `#2a2a2e` | Chrome borders |

### Status color overrides

| Parameter | Default (light) | Default (dark) |
|---|---|---|
| `color_success` / `color_success_dark` | `#1a7a3c` | `#2ec97a` |
| `color_warning` / `color_warning_dark` | `#c97a2e` | `#F08C1A` |
| `color_error` / `color_error_dark` | `#c92e2e` | `#e05252` |

### Example: custom brand colors

```python
bq.Theme(
    mode="dark",
    toggle=True,
    dark_accent="#6366f1",        # indigo
    dark_accent_foreground="#ffffff",
    light_accent="#4f46e5",
    light_accent_foreground="#ffffff",
    light_background="#f8f7ff",
    dark_background="#0f0e17",
    chart_colors=["#6366f1", "#f472b6", "#2ec97a", "#f78c6c"],
)
```

### Font loading

Burq loads fonts automatically via Google Fonts CDN. Any Google Font works:

```python
bq.Theme(font_sans="Inter", font_mono="Fira Code")
```

Custom or self-hosted fonts are not yet supported. Coming in v0.2.

---

## Architecture

burq compiles Python → static files. Your backend owns routing and data.

```
FastAPI  →  routing, auth, API endpoints, serving dist/
Burq     →  compile app.py → dist/ (templates + static)
Browser  →  JS fetches data from your API at runtime
```

burq never touches your backend. `dist/` is portable , deploy to S3, Netlify, Vercel, Databricks Apps, or serve with nginx.

---

## Install

```bash
pip install burq
```

Requires Python 3.10+.

---

## When to use burq

**Good fit:**
- Internal tools and admin dashboards
- Data apps and analytics UIs
- CRUD interfaces over a REST API
- SaaS backends that need a frontend layer
- Replacing Streamlit when you need static output

**Not a good fit:**
- Reactive apps with complex client-side state
- Real-time features (chat, live collaboration, live dashboards)
- Two-way form binding or optimistic UI
- Apps that need WebSockets or SSE push updates
- Replacing React/Vue for highly interactive consumer UIs

burq is a compiler, not a framework. It outputs static files that fetch data from your API. If your UI needs to react to state changes without a server round-trip, burq is not the right tool.

---

[docs](https://burq.dev) · [github](https://github.com/itsdaniyalm/burq) · [pypi](https://pypi.org/project/burq)

*burq (بُرق) is Arabic/Urdu for lightning.*