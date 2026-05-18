# burq ⚡ API Reference

Complete reference for every component, config, and CLI command. Write Python, compile to Vanilla JS + HTML.

`Python 3.10+` · `pip install burq` · `import burq as bq` · `v0.1.1`

---

## Getting Started

### `bq.App` — class

Root application object. All pages must be registered via `@app.page()`.

| Param | Type | Default | Description |
|---|---|---|---|
| `title` * | str | — | App name, used in topbar and `<title>` |
| `api_base` * | str | — | Base URL for all `bq.fetch()` calls |
| `theme` | Theme | None | Theme config |
| `layout` | Layout | None | Shell layout config |
| `logo` | str \| None | `"default"` | `"default"` = burq SVG, `None` = no logo, SVG string, or file path |
| `author` | str | None | Author name in generated meta tags |

```python
import burq as bq

app = bq.App(
    title="My CRM",
    api_base="http://localhost:8000/api",
    theme=bq.Theme(mode="dark", toggle=True),
    logo="default",
)
```
### Logo options

| Value | Behaviour |
|---|---|
| `"default"` | burq SVG mark + wordmark |
| `None` | no logo |
| `"<svg>...</svg>"` | inline SVG string |
| `"path/to/logo.svg"` | embedded SVG file |
| `"path/to/logo.png"` | base64-embedded image |

```python
app = bq.App(logo="default")                  # burq logo
app = bq.App(logo=None)                        # no logo
app = bq.App(logo="assets/mylogo.svg")         # custom SVG file
app = bq.App(logo="assets/mylogo.png")         # custom image
app = bq.App(logo="<svg>...</svg>")            # inline SVG
```
---

### `bq.Layout` — class

Shell layout configuration.

| Param | Type | Default | Description |
|---|---|---|---|
| `sidebar` | bool | True | Show/hide sidebar nav |
| `topbar` | bool | True | Show/hide topbar |
| `bordered` | bool | False | Render chrome borders |
| `show_title` | bool | False | Show app title text beside logo in topbar |

---

### `app.nav()` — method

Set the sidebar navigation items. Call once before defining pages.

```python
app.nav([
    bq.NavItem("Dashboard", icon="layout-dashboard", href="/"),
    bq.NavItem("Contacts",  icon="users",            href="/contacts"),
    bq.NavItem("Settings",  icon="settings",         href="/settings"),
])
```

---

### `bq.Theme` — class

Compiles to CSS custom properties. Every token overridable.

| Param | Type | Default | Description |
|---|---|---|---|
| `mode` | str | `"dark"` | `"light"` or `"dark"` |
| `toggle` | bool | True | Show theme toggle in topbar |
| `font_sans` | str | `"Space Grotesk"` | Body/UI font |
| `font_mono` | str | `"Space Mono"` | Code/CLI font |
| `font_size_base` | int | 14 | Base font size in px |
| `radius` | str | `"md"` | `"none"` `"sm"` `"md"` `"lg"` `"xl"` `"2xl"` |
| `border_width` | int | 1 | Border width in px |
| `shadow_strength` | str | `"md"` | `"none"` `"sm"` `"md"` `"lg"` |
| `spacing_unit` | int | 4 | Base spacing unit in px |
| `dark_accent` | str | `"#F08C1A"` | Override dark mode accent |
| `light_accent` | str | `"#F08C1A"` | Override light mode accent |
| `dark_background` | str | `"#0a0a0b"` | Override dark page background |
| `light_background` | str | `"#fef9ed"` | Override light page background |

> All `light_*` and `dark_*` token params follow the same pattern. See README for the full override table.

```python
bq.Theme(
    mode="dark",
    toggle=True,
    dark_accent="#6366f1",
    dark_background="#0f0e17",
    light_accent="#4f46e5",
    radius="lg",
)
```

---

### `@app.page` — decorator

Registers a function as a page. Each page compiles to one Jinja2 template in `dist/templates/`.

| Param | Type | Default | Description |
|---|---|---|---|
| `path` * | str | — | URL path, supports `{param}` dynamic segments |
| `title` | str | `""` | Browser tab title for this page |

```python
# static route
@app.page("/", title="Dashboard")
def dashboard():
    bq.title("Dashboard")
    bq.metric("Users", "2,480")

# dynamic route
@app.page("/contacts/{contact_id}", title="Contact Detail")
def contact_detail(contact_id):
    bq.contact_profile(endpoint="/contacts/{contact_id}")
    # {contact_id} is replaced at runtime from window.__burqParams
```

---

## Layout Components

### `bq.row()` — context

Horizontal flex container.

| Param | Type | Default | Description |
|---|---|---|---|
| `gap` | str | `"md"` | `"none"` `"sm"` `"md"` `"lg"` |
| `align` | str | `"center"` | Cross-axis: `"start"` `"center"` `"end"` `"stretch"` |
| `justify` | str | `"start"` | Main-axis: `"start"` `"center"` `"end"` `"between"` |
| `nowrap` | bool | False | Disable flex wrap |

```python
with bq.row(align="center", justify="between"):
    bq.metric("Total", "100")
    bq.metric("Active", "84")
```

---

### `bq.col()` — context

Vertical flex container.

| Param | Type | Default | Description |
|---|---|---|---|
| `gap` | str | `"md"` | `"none"` `"sm"` `"md"` `"lg"` |
| `align` | str | `"stretch"` | Cross-axis: `"start"` `"center"` `"end"` `"stretch"` |
| `justify` | str | `"start"` | Main-axis: `"start"` `"center"` `"end"` `"between"` |

```python
with bq.col(align="center", justify="center"):
    bq.title("Hello")
    bq.text("World")
```

---

### `bq.grid()` / `bq.span()` — context

CSS grid layout.

| Param | Type | Default | Description |
|---|---|---|---|
| `cols` | int | 12 | Column count — `1` `2` `3` `4` `6` `12` |
| `gap` | str | `"md"` | `"none"` `"sm"` `"md"` `"lg"` |
| `row_gap` | str | None | Override row gap independently |
| `col_gap` | str | None | Override column gap independently |
| `align` | str | None | `"start"` `"center"` `"end"` `"stretch"` |
| `justify` | str | None | `"start"` `"center"` `"end"` `"between"` `"around"` |

**`bq.span()`**

| Param | Type | Default | Description |
|---|---|---|---|
| `cols` | int | 1 | Number of grid columns to span |
| `align` | str | None | Self-align: `"start"` `"center"` `"end"` `"stretch"` |

```python
with bq.grid(cols=4, gap="lg", align="center"):
    with bq.span(cols=1):
        bq.metric("Practices", "48")
    with bq.span(cols=2, align="center"):
        bq.metric("Revenue", "$2.4M")
    with bq.span(cols=1):
        bq.metric("Risk", "12")
```

---
## Layout Guide

### How the layout system works

burq has four layout primitives: `row`, `col`, `grid`, and `span`. They compose to build any layout.

---

### `bq.row()` — horizontal layout

Items sit side by side. Default gap is `md`.

```python
# simple row
with bq.row():
    bq.badge("Python")
    bq.badge("Vanilla JS")
    bq.badge("Zero Runtime")

# spaced apart
with bq.row(justify="between", align="center"):
    bq.title("Users")
    bq.button("Add User", variant="primary")

# no wrap, tight gap
with bq.row(gap="sm", nowrap=True):
    bq.icon("users", color="accent")
    bq.text("2,480 users")
```

---

### `bq.col()` — vertical layout

Items stack top to bottom. Default gap is `md`.

```python
# centered column (good for hero sections)
with bq.col(align="center"):
    bq.title("Write Python,")
    bq.text("Ship UI.", muted=True)
    bq.button("Get Started", variant="primary")

# tight gap
with bq.col(gap="sm"):
    bq.text("Label", muted=True)
    bq.title("$2.4M")
```

---

### `bq.grid()` + `bq.span()` — grid layout

Grid divides the row into columns. `span` controls how many columns a child occupies.

```python
# 4 equal metric cards
with bq.grid(cols=4):
    with bq.span(cols=1):
        bq.metric("Users", "2,480")
    with bq.span(cols=1):
        bq.metric("Revenue", "$84k")
    with bq.span(cols=1):
        bq.metric("Deals", "143")
    with bq.span(cols=1):
        bq.metric("Churn", "3.2%")

# asymmetric layout — wide content + narrow sidebar
with bq.grid(cols=3):
    with bq.span(cols=2):
        bq.table(data=bq.fetch("GET", "/contacts/"), columns=["name", "status"])
    with bq.span(cols=1):
        with bq.card("Summary"):
            bq.metric("Total", "120")
```

---

### Full-width boxes inside grid

By default a `box` is content-width. To fill the grid cell use `full_width=True` on the box and `align="stretch"` on the span:

```python
with bq.grid(cols=4):
    with bq.span(cols=1, align="stretch"):
        with bq.box(background="surface", border=True, padding="lg", full_width=True):
            bq.title("38ms")
            bq.text("Build time")
    with bq.span(cols=1, align="stretch"):
        with bq.box(background="surface", border=True, padding="lg", full_width=True):
            bq.title("0")
            bq.text("Runtime overhead")
```

---

### Nesting layouts

Row, col, grid, and span nest freely:

```python
with bq.grid(cols=2):
    with bq.span(cols=1):
        with bq.col(gap="sm"):
            bq.title("Left column")
            bq.text("Stacked content", muted=True)
    with bq.span(cols=1):
        with bq.row(justify="between"):
            bq.badge("Active")
            bq.button("Edit", variant="ghost")
```

---

### Spacing

Use `bq.spacer()` for vertical rhythm and `bq.divider()` for visual separation:

```python
bq.title("Section A")
bq.spacer(size="md")   # none|sm|md|lg
bq.divider()
bq.spacer(size="md")
bq.title("Section B")
```
---
---
### `bq.card()` — context

Card container with optional header title.

```python
with bq.card("Workspace Settings"):
    bq.input("Name", icon="building-2")
    bq.button("Save", variant="primary")
```

---

### `bq.box()` — context

Styled container with explicit background, border, radius, and padding control.

| Param | Type | Default | Description |
|---|---|---|---|
| `background` | str | `"muted"` | `"muted"` `"surface"` `"accent"` or any CSS color |
| `border` | bool | False | Render border using theme border color |
| `radius` | str | `"md"` | Border radius token |
| `padding` | str | `"md"` | `"sm"` `"md"` `"lg"` |
| `foreground` | str | None | Text color token or CSS value |

```python
with bq.box(background="muted", border=True, radius="lg"):
    bq.text("Custom styled container", muted=True)
```

---

### `bq.tabs()` / `bq.tab()` — context

Tabbed container.

```python
with bq.tabs(["Overview", "Settings", "Danger Zone"]):
    with bq.tab("Overview"):
        bq.metric("Users", "2,480")
    with bq.tab("Settings"):
        bq.input("Name")
```

---

### `bq.divider()` / `bq.spacer()`

```python
bq.divider()
bq.spacer(size="md")  # none|sm|md|lg
```

---

## Display

### `bq.title()` / `bq.heading()` / `bq.text()`

| Param | Type | Default | Description |
|---|---|---|---|
| `color` | str | None | Token (`"accent"` `"muted"` `"success"` `"error"` `"warning"` `"dim"`) or any CSS color |
| `size` | str | None | Token (`"xs"` `"sm"` `"base"` `"md"` `"lg"` `"xl"` `"2xl"` `"3xl"` `"4xl"` `"5xl"` `"6xl"`) or raw CSS e.g. `"52px"` |

```python
bq.title("Write Python,", color="accent", size="5xl")
bq.heading("No JS. No apologies.", size="3xl")
bq.text("Ships to Vanilla JS.", muted=True, size="lg")
```
---

### `bq.metric()` — fn

```python
bq.metric(
    label="Users",
    value="2,480",
    trend="+12%",
    trend_dir="up",       # up|down|flat
    icon="users",
    variant="default",    # default|accent|ghost
)
```

---

### `bq.badge()` — fn

```python
bq.badge("Active", variant="success", size="md", dot=False)
# variants: default|accent|success|warning|danger|info
```

---

### `bq.avatar()` / `bq.avatar_group()`

```python
bq.avatar(initials="DM", size="md", variant="square", status="online", color="accent")
bq.avatar_group(avatars=[...], overflow=3)
```

---

### `bq.progress()`

```python
bq.progress(label="Upload", value=72, variant="success", size="md", striped=True, animated=True)
```

---

### `bq.markdown()`

Renders a markdown string to HTML at compile time.

```python
bq.markdown("## Hello\n\nThis is **markdown**.")
```

---

### `bq.code_block()`

Syntax-highlighted code block with optional line numbers and copy button.

| Param | Type | Default | Description |
|---|---|---|---|
| `content` * | str | — | Code to display |
| `language` | str | `"python"` | Prism language identifier |
| `filename` | str | None | Shown in header bar |
| `line_numbers` | bool | `True` | Show/hide line numbers |

```python
bq.code_block(content="print('hello')", language="python", filename="app.py")
bq.code_block(content="print('hello')", language="python", line_numbers=False)
```

### `bq.icon()`

Inline Lucide icon with theme color support.

| Param | Type | Default | Description |
|---|---|---|---|
| `name` * | str | — | Lucide icon name — [lucide.dev/icons](https://lucide.dev/icons) |
| `size` | str | `"md"` | `"xs"` `"sm"` `"md"` `"lg"` `"xl"` |
| `color` | str | None | Token: `"accent"` `"muted"` `"success"` `"warning"` `"error"` `"foreground"` or any CSS color |
| `label` | str | None | Accessible `aria-label` — omit for decorative icons |

```python
bq.icon("users", size="lg", color="accent")
bq.icon("alert-triangle", size="sm", color="warning")
bq.icon("check-circle", color="#2ec97a")
```

---
---

### `bq.rich_text()`

WYSIWYG editor that serializes to Markdown on submit.

| Param | Type | Default | Description |
|---|---|---|---|
| `name` * | str | — | Form field name — submitted as markdown |
| `label` | str | None | Label shown above editor |
| `placeholder` | str | None | Placeholder in empty editor |
| `endpoint` | str | None | API endpoint for auto-save on blur |
| `value` | str | None | Pre-fill with existing markdown |

```python
bq.rich_text(
    name="body",
    label="Note",
    placeholder="Write something…",
    endpoint="/notes/{note_id}",
)
```

---

### `bq.spinner()` / `bq.skeleton()`

```python
bq.spinner(size="md", color="accent")
bq.skeleton(variant="text")  # text|text-sm|text-lg|avatar-sm|avatar-md|button|rect
```

---

### `bq.breadcrumb()`

```python
bq.breadcrumb(items=[
    bq.BreadcrumbItem("Home", href="/"),
    bq.BreadcrumbItem("Contacts", href="/contacts"),
    bq.BreadcrumbItem("Detail"),
])
```

---

### `bq.image()` — fn
| Param | Type | Default | Description |
|---|---|---|---|
| `src` * | str | — | URL, static path (`"static/images/x.png"`), or `bq.fetch()` |
| `alt` | str | `""` | Alt text |
| `src_dark` | str | None | Alternate src for dark theme — swapped via `data-theme` |
| `width` | str | None | e.g. `"300px"` or `"100%"` |
| `height` | str | None | e.g. `"200px"` |
| `radius` | str | `"md"` | `"none"` `"sm"` `"md"` `"lg"` `"xl"` |
| `caption` | str | None | Caption below image |
| `fit` | str | `"cover"` | `"cover"` `"contain"` `"fill"` `"none"` |

```python
bq.image("https://example.com/photo.jpg", alt="Photo", radius="lg")
bq.image("static/images/logo.png", width="120px")
bq.image("static/images/banner.jpg", width="100%", height="200px", fit="cover", caption="Our team")

# theme-aware — light SVG by default, dark SVG when data-theme="dark"
bq.image("static/burq-flow-light.svg", src_dark="static/burq-flow-dark.svg", alt="How burq works", width="420px")
```

---

### `bq.link()` — fn

| Param | Type | Default | Description |
|---|---|---|---|
| `label` * | str | — | Link text |
| `href` | str | `"#"` | URL |
| `icon` | str | None | Lucide icon name |
| `external` | bool | False | Opens in new tab |
| `muted` | bool | False | Muted color instead of accent |
| `size` | str | None | Text size token |

```python
bq.link("View docs", href="https://burq.dev", external=True)
bq.link("Back to contacts", href="/contacts", icon="arrow-left")
bq.link("Learn more", href="/about", muted=True, size="sm")
```

---

## Data

### `bq.table()`

| Param | Type | Default | Description |
|---|---|---|---|
| `data` * | fetch() | — | Data source — must be a `bq.fetch()` descriptor |
| `columns` * | list[str] | — | Column keys to display, in order |
| `column_config` | dict | `{}` | Key → ColumnConfig for custom rendering |
| `searchable` | bool | False | Client-side search |
| `sortable` | bool | False | Click-to-sort headers |
| `checkable` | bool | False | Row selection checkboxes |
| `row_href` | str | None | Row click URL — use `{id}` for dynamic IDs |

```python
bq.table(
    data=bq.fetch("GET", "/contacts/"),
    columns=["name", "company", "status", "created_at"],
    column_config={
        "name":       bq.AvatarColumn(sub_key="email"),
        "status":     bq.BadgeColumn(variant_map={"active": "success", "churned": "danger"}),
        "created_at": bq.DateColumn(),
    },
    searchable=True,
    sortable=True,
    row_href="/contacts/{id}",
)
```
# static list
bq.table(
    data=[
        {"name": "Alice", "status": "active"},
        {"name": "Bob",   "status": "churned"},
    ],
    columns=["name", "status"],
    column_config={"status": bq.BadgeColumn(variant_map={"active": "success", "churned": "danger"})},
)

# pandas DataFrame
bq.table(data=df, columns=["name", "status"], searchable=True)
---

### `bq.fetch()`

Compile-time fetch descriptor. At runtime, `burq.js` calls `api_base + endpoint`.

```python
bq.fetch("GET", "/contacts/")
bq.fetch("GET", "/contacts/{contact_id}/deals")
bq.fetch("POST", "/items/", data={"name": "New Item"})
```

---

### Column Config Types

| Class | Params | Description |
|---|---|---|
| `AvatarColumn` | `initials_key`, `sub_key` | Avatar with initials + sub-label |
| `BadgeColumn` | `variant_map: dict` | Badge colored by value |
| `CurrencyColumn` | `prefix="$"`, `decimals=2` | Formatted number |
| `DateColumn` | — | Human-readable date |
| `BoolColumn` | `true_label`, `false_label` | Boolean as badge |
| `TextColumn` | `muted=False` | Plain text cell |

---

## Charts

Chart.js 4.4 — CDN auto-injected. Colors from theme tokens.

### `bq.bar_chart()`

```python
bq.bar_chart(
    data=[{"month": "Jan", "revenue": 4000}, ...],
    x="month",
    y="revenue",          # or list for grouped bars
    title="Monthly Revenue",
    stacked=False,
    height=300,
)
```

### `bq.line_chart()`

```python
bq.line_chart(
    data=bq.fetch("GET", "/stats/trends"),
    x="date",
    y=["signups", "churns"],
    title="Growth Trends",
    smooth=True,
    height=300,
)
```

### `bq.area_chart()`

Same API as `line_chart`, `smooth=True` by default.

### `bq.donut_chart()`

```python
bq.donut_chart(
    data=[{"status": "Won", "count": 42}, ...],
    label="status",
    value="count",
    title="Deal Breakdown",
    height=300,
)
```

### Chart colors

```python
bq.Theme(
    chart_colors=[
        "#F08C1A",  # accent — always first
        "#60a5fa",
        "#2ec97a",
        "#e05252",
        "#c97a2e",
        "#a78bfa",
        "#f472b6",
    ]
)
```

---

## Forms

### `bq.input()`

```python
bq.input("Email", type="email", icon="mail", required=True)
bq.input("API Base URL", icon="link", placeholder="https://")
```

### `bq.textarea()`

```python
bq.textarea("Notes", rows=4, placeholder="Add a note…")
```

### `bq.select()`

```python
bq.select("Status", options=["Active", "Inactive"], searchable=True)
```

### `bq.toggle()` / `bq.checkbox()` / `bq.radio()`

```python
bq.toggle("Enable notifications", checked=True)
bq.checkbox("Accept terms", value="terms")
bq.radio("Plan", name="plan", value="pro")
```

### `bq.file_upload()`

```python
bq.file_upload("Avatar", accept="image/*", helper="PNG or JPG, max 2MB")
```

### `bq.button()`

| Param | Type | Default | Description |
|---|---|---|---|
| `label` | str | None | Button text |
| `variant` | str | `"primary"` | `"primary"` `"secondary"` `"ghost"` `"outline"` `"danger"` `"link"` |
| `size` | str | `"md"` | `"xs"` `"sm"` `"md"` `"lg"` |
| `icon` | str | None | Lucide icon name |
| `icon_pos` | str | `"left"` | `"left"` `"right"` |
| `disabled` | bool | False | Disabled state |
| `onclick` | str | None | JS expression or `bq.open_modal()` |
| `type` | str | `"button"` | `"button"` `"submit"` |
| `href` | str | None | Renders as `<a>` — use with `variant="link"` or any variant |
| `external` | bool | False | Adds `target="_blank"` when `href` is set |

```python
bq.button("Save", variant="primary", icon="save")
bq.button("Delete", variant="danger", icon="trash-2")
bq.button("Open", variant="default", onclick=bq.open_modal("my-modal"))
bq.button("Visit docs", variant="link", href="https://burq.dev", external=True)
bq.button("Back", variant="ghost", href="/contacts", icon="arrow-left")
# variants: default|primary|secondary|danger|ghost|outline|link
```
---

---

## Feedback

### `bq.alert()`

```python
bq.alert("Saved successfully.", type="success")
# types: success|error|warning|info
```

### `bq.modal()`

```python
@app.modal("confirm-delete")
def confirm_modal():
    with bq.modal("confirm-delete", title="Delete?", size="sm"):
        with bq.modal_body():
            bq.text("This cannot be undone.")
        with bq.modal_footer():
            bq.button("Cancel",  onclick=bq.close_modal("confirm-delete"))
            bq.button("Delete",  variant="danger")
```

### `bq.accordion()`

```python
bq.accordion(items=[
    {"title": "What is burq?",  "content": "A Python UI compiler."},
    {"title": "Does it need JS?", "content": "No. It compiles to Vanilla JS."},
])
```

### `bq.pagination()`

```python
bq.pagination(total=120, page=1, per_page=10)
```

### `bq.empty_state()`

```python
bq.empty_state(
    title="No contacts yet",
    message="Add your first contact to get started.",
    icon="users",
    action=bq.button("Add Contact", variant="primary", icon="plus"),
)
```

---

## API Helpers

### `bq.open_modal()` / `bq.close_modal()`

```python
bq.button("Open",  onclick=bq.open_modal("my-modal"))
bq.button("Close", onclick=bq.close_modal("my-modal"))
```

### `bq.contact_profile()`

Self-hydrating profile header. Fetches name, email, avatar, and status at runtime.

```python
bq.contact_profile(endpoint="/contacts/{contact_id}")
```

### `bq.NavItem` — class

```python
bq.NavItem("Dashboard", icon="layout-dashboard", href="/")
# icon must be a valid Lucide icon name — lucide.dev/icons
```

### `bq.NavGroup` — class

Collapsible sidebar nav group. Auto-opens if current URL matches any child href.

| Param | Type | Default | Description |
|---|---|---|---|
| `label` * | str | — | Group label |
| `icon` | str | `""` | Lucide icon name |
| `children` * | list[NavItem] | — | Child nav items |
| `default_open` | bool | False | Open by default |

```python
app.nav([
    bq.NavItem("Dashboard", icon="layout-dashboard", href="/"),
    bq.NavGroup("Contacts", icon="users", children=[
        bq.NavItem("All Contacts", href="/contacts"),
        bq.NavItem("Import",       href="/contacts/import"),
    ]),
], footer=[
    bq.NavItem("Settings", icon="settings", href="/settings"),
])
```

---

## CLI

### `burq new <project-name>`

Scaffold a new burq project.

```bash
burq new my-app
cd my-app
```

Creates:
```
my-app/
├── app.py          # App config + nav + Hello World page
├── pages/          # additional pages
├── components/     # custom components
├── dist/           # compiled output (gitignored)
└── .gitignore
```

### `burq build`

Compile `app.py` → `dist/`. Shows per-file output and total build time.

```
  ✓ base.html
  ✓ templates/index.html
  ✓ templates/contacts.html
  ✓ tokens.css, layout.css, components.css, burq.js

⚡ Burq build complete → dist/  [38ms]
```

### `burq dev`

Watch `app.py`, `pages/`, `components/` — recompile on every `.py` save. Debounces 300ms.

```bash
burq dev
```

### `compile_app()` — fn

Programmatic compiler entry point.

```python
from burq.compiler import compile_app
compile_app(app, output_dir="dist")
```