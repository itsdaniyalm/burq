# Burq ⚡ — Python UI Compiler

> Write Python. Compile to blazing fast Vanilla JS + HTML. Connect to any API.

*Burq (بُرق) — Arabic/Urdu for lightning.*

---

## The Idea

Every Python developer can build a backend. Almost none want to touch JavaScript. Burq is a compiler that takes Python UI code and compiles it to pure Vanilla JS + HTML + CSS — no framework, no runtime, no server middleman.

You write Python. Burq compiles it. The browser gets fast, clean, static files that talk directly to your existing API.

---

## The Problem

| | Streamlit | React + FastAPI | Django Templates | Burq |
|---|---|---|---|---|
| Write in Python | ✅ | ❌ | Partial | ✅ |
| Works with any API | ❌ | ✅ | ❌ | ✅ |
| Compiles to static files | ❌ | ✅ | ❌ | ✅ |
| No JS knowledge needed | ✅ | ❌ | ✅ | ✅ |
| Production ready | ❌ | ✅ | ✅ | ✅ |
| Component model | ❌ | ✅ | ❌ | ✅ |
| Deploy anywhere | ❌ | ✅ | ❌ | ✅ |

---

## How It Works

```
app.py
  ↓
burq build
  ↓
dist/
├── templates/
│   ├── base.html
│   ├── index.html
│   └── contacts.html
└── static/
    ├── burq.js        (~25kb runtime)
    ├── tokens.css     (design tokens)
    ├── layout.css     (layout system)
    └── components.css (component styles)
```

- **No server required at runtime** — output is pure static files
- **No framework** — compiles to Vanilla JS, zero dependencies in output
- **No WASM** — Python runs only at compile time, not in the browser
- **Connect to any API** — FastAPI, Django, Node, anything with a REST endpoint

---

## Architecture

```
FastAPI  →  routing, auth, data APIs, serving dist/
Burq     →  compile app.py → dist/ (templates + JS + CSS)
Browser  →  JS reads URL params, fetches data from your API
```

Burq never generates route files. FastAPI owns routing. Burq owns compilation.

---

## What It Looks Like

```python
import burq as bq
from burq.compiler import compile_app

app = bq.App(
    title="340B Analyzer",
    api_base="https://my-api.com/api",
    theme=bq.Theme(mode="dark", toggle=True)
)

app.nav([
    bq.NavItem("Dashboard",  icon="layout-dashboard", href="/"),
    bq.NavItem("Practices",  icon="users",            href="/practices"),
    bq.NavItem("Settings",   icon="settings",         href="/settings"),
])


@app.page("/")
def dashboard():
    bq.title("Dashboard")

    with bq.grid(cols=4):
        with bq.span(cols=1):
            bq.metric("Practices", "48", trend="+3", trend_dir="up", icon="users")
        with bq.span(cols=1):
            bq.metric("Critical Risk", "12", trend_dir="down", icon="alert-triangle")
        with bq.span(cols=1):
            bq.metric("Total Spread", "$2.4M", trend="+8%", trend_dir="up")
        with bq.span(cols=1):
            bq.metric("Managed", "31", variant="accent")

    bq.spacer()

    bq.table(
        data=bq.fetch("GET", "/practices/"),
        columns=["name", "provider", "state", "risk_level", "total_spread"],
        column_config={
            "name":         bq.AvatarColumn(sub_key="provider"),
            "risk_level":   bq.BadgeColumn(variant_map={
                "critical": "danger",
                "high":     "warning",
                "managed":  "success",
            }),
            "total_spread": bq.CurrencyColumn(prefix="$"),
        },
        searchable=True,
        sortable=True,
        row_href="/practices/{id}",
    )


@app.page("/practices/{practice_id}")
def practice_detail(practice_id):
    bq.contact_profile(endpoint="/practices/{practice_id}")
    bq.spacer()

    with bq.tabs(["Drug Portfolio", "Risk Breakdown", "Locations"]):
        with bq.tab("Drug Portfolio"):
            bq.table(
                data=bq.fetch("GET", "/practices/{practice_id}/drugs"),
                columns=["drug", "risk_level", "patients", "annual_spread"],
                column_config={
                    "risk_level":    bq.BadgeColumn(variant_map={"critical": "danger", "high": "warning"}),
                    "annual_spread": bq.CurrencyColumn(prefix="$"),
                },
                searchable=True,
                sortable=True,
            )

        with bq.tab("Risk Breakdown"):
            with bq.grid(cols=3):
                with bq.span(cols=1):
                    bq.metric("Critical", "—", icon="alert-triangle")
                with bq.span(cols=1):
                    bq.metric("High", "—", icon="alert-circle")
                with bq.span(cols=1):
                    bq.metric("Managed", "—", icon="check-circle")


@app.page("/settings")
def settings():
    bq.title("Settings")

    with bq.tabs(["General", "Notifications", "Danger Zone"]):

        with bq.tab("General"):
            with bq.card("Workspace"):
                bq.input("Workspace Name", icon="building-2")
                bq.input("API Base URL",   icon="link")
                bq.select("Timezone", options=["UTC", "America/New_York", "Asia/Karachi"])
                bq.button("Save Changes", variant="primary", icon="save")

            bq.spacer()

            bq.accordion(items=[
                {"title": "How does billing work?",
                 "content": "Billed monthly per seat. Prorated on changes."},
                {"title": "How do I connect my API?",
                 "content": "Set the API Base URL above. Burq proxies all fetch calls through it."},
            ])

        with bq.tab("Notifications"):
            with bq.card("Email Notifications"):
                bq.toggle("New assignment",      checked=True)
                bq.toggle("Weekly digest",       checked=False)
                bq.toggle("Risk alerts",         checked=True)
                bq.divider()
                bq.button("Save", variant="primary", icon="save")

        with bq.tab("Danger Zone"):
            bq.alert("These actions cannot be undone.", type="warning")
            bq.spacer()
            with bq.card("Delete Workspace"):
                bq.text("Permanently delete this workspace and all data.", muted=True)
                bq.button("Delete Workspace", variant="danger", icon="trash-2")


compile_app(app, output_dir="dist")
```

---

## CLI

```bash
# Install
pip install burq

# Create new project
burq new my-app
cd my-app

# Dev mode — watch and recompile on save
burq dev

# Build for production
burq build
```

Build output:
```
  ✓ base.html
  ✓ templates/index.html
  ✓ templates/practices.html
  ✓ templates/settings.html
  ✓ tokens.css, layout.css, components.css, burq.js

⚡ Burq build complete → dist/  [38ms]
```

---

## Core Components

### Layout
```python
bq.row()                    # horizontal flex row
bq.col()                    # vertical flex column
bq.card(title)              # card container
bq.grid(cols=3)             # css grid
bq.span(cols=2)             # grid column span
bq.tabs(labels)             # tabbed container
bq.tab(label)               # individual tab panel
bq.divider()                # horizontal rule
bq.spacer(size="md")        # vertical space
with bq.box(background="muted", border=True, radius="lg"):
    ...                     # styled container
```

### Display
```python
bq.title(text)
bq.heading(text)
bq.text(text, muted=False)
bq.metric(label, value, trend=None, trend_dir=None, icon=None, variant="default")
bq.badge(text, variant="default")
bq.avatar(initials, size="md")
bq.progress(label, value, variant="default")
bq.markdown(content)
bq.spinner()
bq.skeleton(variant="text")
bq.breadcrumb(items=[...])
bq.empty_state(title, message, icon, action)
```

### Data
```python
bq.table(
    data=bq.fetch("GET", "/items/"),
    columns=["name", "status", "value"],
    column_config={...},
    searchable=True,
    sortable=True,
    checkable=True,
    row_href="/items/{id}",
)
```

### Forms
```python
bq.input(label, type, placeholder, icon, required, value)
bq.textarea(label, rows, placeholder)
bq.select(label, options, searchable, placeholder)
bq.toggle(label, checked)
bq.checkbox(label, value)
bq.radio(label, name, value)
bq.file_upload(label, accept, helper)
bq.button(label, variant, icon, onclick)
```

### Feedback
```python
bq.alert(message, type)           # success | error | warning | info
bq.accordion(items, multiple)
bq.pagination(total, page, per_page, on_change)
bq.modal(id, title, size)
bq.modal_body()
bq.modal_footer()
```

### API
```python
bq.fetch(method, endpoint)        # compile-time fetch descriptor
bq.open_modal(id)                 # JS: ModalManager.open(id)
bq.close_modal(id)                # JS: ModalManager.close(id)
```

---

## Column Config

| Config | Description |
|---|---|
| `AvatarColumn(initials_key, sub_key)` | Avatar with initials + sub-label |
| `BadgeColumn(variant_map)` | Badge colored by value |
| `CurrencyColumn(prefix, decimals)` | Formatted currency |
| `DateColumn()` | Human-readable date |
| `BoolColumn(true_label, false_label)` | Boolean rendered as badge |
| `TextColumn(muted)` | Plain text cell |

---

## Theme System

```python
bq.Theme(
    mode="dark",              # "light" | "dark"
    toggle=True,              # theme toggle button in topbar
    font_sans="Space Grotesk",
    font_mono="Space Mono",
    font_size_base=14,
    radius="md",              # "none" | "sm" | "md" | "lg" | "xl"
    border_width=1,
    shadow_strength="md",
    spacing_unit=4,

    # override any semantic token:
    dark_accent="#F08C1A",
    light_background="#fef9ed",
    dark_background="#0a0a0b",
)
```

Compiles to CSS custom properties used across all generated stylesheets.

---

## Differentiators

| | Burq | Streamlit | Dash | NiceGUI | Reflex |
|---|---|---|---|---|---|
| Compiles to static files | ✅ | ❌ | ❌ | ❌ | ❌ |
| Works with any REST API | ✅ | ❌ | ❌ | ✅ | ✅ |
| No runtime server needed | ✅ | ❌ | ❌ | ❌ | ❌ |
| Pure Vanilla JS output | ✅ | ❌ | ❌ | ❌ | ❌ |
| Streamlit-style syntax | ✅ | ✅ | ❌ | ❌ | ❌ |
| Deploy to CDN/S3 | ✅ | ❌ | ❌ | ❌ | ❌ |

---

## Compiler Architecture

```
burq/
├── compiler/
│   ├── __init__.py      # compile_app() — orchestrates the pipeline
│   ├── html_gen.py      # Python component tree → HTML
│   ├── js_gen.py        # generates burq.js runtime
│   └── css_gen.py       # generates tokens.css + layout.css + components.css
├── components/
│   ├── layout.py        # row, col, grid, card, box, spacer, divider
│   ├── display.py       # title, text, metric, badge, avatar, progress
│   ├── forms.py         # input, select, toggle, button, file_upload
│   ├── feedback.py      # modal, alert, toast
│   ├── navigation.py    # tabs, tab, dropdown, NavItem
│   ├── data.py          # table, fetch, column configs
│   └── extra.py         # accordion, empty_state, pagination, markdown, contact_profile
├── theme/
│   ├── theme.py         # Theme dataclass
│   └── compiler.py      # token defaults + CSS variable generation
├── app.py               # App + Layout dataclasses
├── context.py           # component tree context manager
└── cli/
    └── main.py          # burq new | build | dev
```

### Compilation Pipeline

```
1. PARSE
   Load app.py → execute decorators → populate app._pages

2. GENERATE HTML
   Each @app.page → one Jinja2 template
   Components → HTML via render_node()
   Dynamic routes → inline JS param extraction

3. GENERATE JS
   burq.js — fetch wrapper, table hydration, sidebar, theme toggle,
              modals, toasts, tabs, dropdowns, accordions, file uploads

4. GENERATE CSS
   tokens.css    — CSS custom properties from Theme config
   layout.css    — grid, topbar, sidebar, nav
   components.css — all component styles

5. OUTPUT
   dist/templates/ + dist/static/
   ⚡ built in Xms
```

---

## Target Audience

- Python backend developers who want a frontend without learning JS
- Data engineers who need more than Streamlit
- Startups building internal tools fast
- Solo developers building SaaS in pure Python
- Teams with a FastAPI backend who need a frontend layer

---

## Roadmap

### v0.1 — Core ✅
- [x] Python component tree → HTML/CSS/JS compiler
- [x] Full component library (layout, display, forms, data, feedback)
- [x] Design token system (Filament theme, light + dark)
- [x] Table hydration — fetch, search, pagination, column config, row click
- [x] Dynamic routes — `{param}` → JS URL param extraction
- [x] CLI — `burq new`, `burq build`, `burq dev`
- [x] CRM demo app

### v0.2 — Developer Experience
- [ ] Hot reload — browser auto-refresh on `burq dev`
- [ ] Error messages with Python line numbers
- [ ] VS Code extension — autocomplete for `bq.*`
- [ ] `burq dev` — serve dist/ directly (optional)

### v0.3 — Ecosystem
- [ ] Documentation site (built with burq)
- [ ] Template library — admin dashboard, data app, CRUD app
- [ ] Databricks Apps deployment guide
- [ ] PyPI publish

---

*burq (بُرق) — Because your UI should be as fast as your backend.*