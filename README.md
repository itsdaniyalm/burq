# burq ⚡

> Write Python. Ship UI.

burq is a Python UI compiler. Write your frontend in Python — burq compiles it to pure Vanilla JS + HTML + CSS. No JavaScript. No framework. No runtime server.

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
    bq.NavItem("Contacts",  icon="users",            href="/contacts"),
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

`burq dev` watches `app.py`, `pages/`, and `components/` — recompiles on every save.

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
    mode="dark",           # "light" | "dark"
    toggle=True,           # show theme toggle button
    font_sans="Space Grotesk",
    font_mono="Space Mono",
    radius="md",           # "none" | "sm" | "md" | "lg" | "xl"
    border_width=1,
    # override any token:
    dark_accent="#F08C1A",
    light_background="#fef9ed",
)
```

---

## Architecture

burq compiles Python → static files. Your backend owns routing and data.

```
FastAPI  →  routing, auth, API endpoints, serving dist/
Burq     →  compile app.py → dist/ (templates + static)
Browser  →  JS fetches data from your API at runtime
```

burq never touches your backend. `dist/` is portable — deploy to S3, Netlify, Vercel, Databricks Apps, or serve with nginx.

---

## Install

```bash
pip install burq
```

Requires Python 3.10+.

---

*burq (بُرق) — Arabic/Urdu for lightning.*