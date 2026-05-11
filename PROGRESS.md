# Burq ⚡ — Development Progress

## Project Structure
```
burq/                          # PyPI package
├── __init__.py                ✅
├── app.py                     ✅
├── context.py                 ✅
├── compiler/
│   ├── __init__.py            ✅
│   ├── html_gen.py            ✅
│   ├── js_gen.py              ⬜
│   └── css_gen.py             ⬜
├── components/
│   ├── __init__.py            ✅
│   ├── layout.py              ✅
│   ├── display.py             ✅
│   ├── forms.py               ✅
│   ├── feedback.py            ✅
│   ├── navigation.py          ✅
│   └── data.py                ✅
├── runtime/
│   └── burq.js                ⬜
├── theme/
│   ├── __init__.py            ✅
│   ├── theme.py               ✅
│   ├── color.py               ✅
│   └── compiler.py            ✅
└── cli/
    └── main.py                ⬜

dev/                           # never shipped to PyPI
├── crm/
│   ├── backend/
│   │   ├── main.py            ✅
│   │   ├── models.py          ✅
│   │   ├── seed.py            ✅
│   │   ├── db.py              ✅
│   │   └── requirements.txt   ✅
│   └── ui/
│       ├── tokens.css         ✅
│       ├── layout.css         ✅
│       ├── components.css     ✅
│       └── index.html         ✅
└── playground/
    ├── test_tokens.py         ✅
    └── test_api.py            ✅
```

---

## Phase 1 — Design System ✅ COMPLETE

### Token System ✅
- oklch-based color scale generator (`burq/theme/color.py`)
- Full token compiler (`burq/theme/compiler.py`)
- Theme class with ALL scales derived from user config:
  - `primary` hex → brand-100 to brand-700 via oklch
  - `gray` hex → gray-100 to gray-900 via oklch
  - `color_success/warning/error` → full scales via oklch
  - `spacing_unit` → space-1 through space-12
  - `font_size_base` → text-xs through text-2xl
  - `radius` → fixed scale (0/4/6/8/12/16px)
  - `border_width` → border-width/2/3
  - `shadow_strength` → shadow-sm/md/lg
- Semantic tokens: background, foreground, surface, surface-raised,
  muted, muted-foreground, accent, accent-foreground, border,
  chrome, chrome-foreground, chrome-border
- Status color tokens: color-success/warning/error + dark variants
- Z-index tokens: dropdown(150), sticky(10), sidebar(20), modal(200), toast(300)
- Component tokens: toast, modal, tabs, skeleton, progress

### Layout Components ✅
- `layout` — grid shell with 4 modes:
  - sidebar + topbar (default)
  - topbar only
  - sidebar only
  - bare
  - collapsed sidebar (56px icons only)
- `topbar` — sticky, left/right slots, theme toggle
- `sidebar` — sticky, logo, nav, footer slots
- `nav-item` — icon + label, active state, collapsed state
- `container` — max-width wrapper (sm|md|lg|xl|full)
- `row` — flexbox horizontal (gap, align, justify, wrap)
- `col` — flexbox vertical (gap, align)
- `grid` — 12-col CSS grid (cols, gap, row-gap, col-gap, span)
- `divider` — horizontal rule (sm|md|lg, vertical)

### UI Components ✅
- `card` — (default|raised|flat|ghost × sm|md|lg)
- `badge` — (default|accent|success|warning|danger|info × sm|md|lg)
- `button` — (primary|secondary|ghost|outline|danger × xs|sm|md|lg|icon)
- `metric-card` — KPI (default|accent|ghost, trend up/down/flat)
- `table` — searchable, sortable, checkable, pagination, actions, striped
- `input` — (text|email|password|number × sm|md|lg, icon, error)
- `textarea` — multiline, error state
- `select` — native + custom searchable with keyboard nav
- `toggle` — on/off switch
- `checkbox` — styled
- `radio` — styled
- `toast` — (success|error|warning|info, auto-dismiss, stack)
- `modal` — (sm|md|lg, backdrop, ESC, animation)
- `tabs` — (default|pills|card)
- `avatar` — (xs|sm|md|lg|xl, round, status dot)
- `avatar-group` — overlapping + overflow count
- `skeleton` — shimmer (text|avatar|button|rect|card|table)
- `progress` — (default|success|warning|danger × sm|md|lg, striped, animated)
- `dropdown` — keyboard nav, dividers, danger item
- `breadcrumb` — chevron|slash separator
- `spinner` — (sm|md|lg × accent|muted|white)
- `alert` — (success|error|warning|info, dismissible)

### JavaScript Runtime (inline) ✅
- `ToastManager` — show/dismiss/auto-dismiss
- `ModalManager` — open/close, backdrop, ESC
- `initCustomSelects()` — searchable select, keyboard nav
- `initTabs()` — tab switching
- `initDropdowns()` — open/close, keyboard nav
- Sidebar toggle (collapse/expand)
- `lucide.createIcons()`

### Backend (CRM Demo) ✅
- FastAPI + SQLite + SQLAlchemy
- Models: Contact, Deal, Activity, DealStatus
- Faker seed (40 contacts, 1-3 deals, 1-4 activities each)
- Endpoints: contacts, deals, activities, summary
- CORS enabled

---

## Phase 2 — Python API ✅ COMPLETE

### App & Config ✅
```python
app = bq.App(
    title="My App",
    author="Daniyal",
    api_base="https://api.example.com",
    api_key="my-key",
    layout=bq.Layout(sidebar=True, topbar=True),
    theme=bq.Theme(
        primary="#F0A202",
        gray="#0E1428",
        color_success="#16a34a",
        color_warning="#d97706",
        color_error="#dc2626",
        radius="lg",
        spacing_unit=4,
        font_sans="Space Grotesk",
        font_mono="Space Mono",
        font_size_base=14,
        border_width=1,
        shadow_strength="md",
        mode="dark",
        toggle=True,
    )
)
```

### Navigation ✅
```python
app.nav([
    bq.NavItem("Dashboard", icon="layout-dashboard", href="/"),
    bq.NavItem("Contacts",  icon="users",            href="/contacts"),
], footer=[
    bq.NavItem("Settings",  icon="settings",         href="/settings"),
])
```

### Pages & Modals ✅
```python
@app.page("/")
def dashboard():
    bq.title("Dashboard")
    with bq.row():
        bq.metric("Contacts", "2,480", trend="+12%", trend_dir="up")

@app.modal("add-contact")
def add_contact():
    with bq.modal("add-contact", title="Add Contact"):
        with bq.modal_body():
            bq.input("Name", required=True)
        with bq.modal_footer():
            bq.button("Save", variant="primary")
```

### Context System ✅
- `RenderContext` — tracks component tree as Python executes
- `container_node` — context manager for layout components
- `leaf_node` — adds leaf components to current parent
- `get_context()` / `reset_context()` — global singleton

### Component API ✅
All components implemented in:
- `burq/components/layout.py` — row, col, grid, span, container, divider, card
- `burq/components/display.py` — title, heading, text, metric, badge, avatar, avatar_group, progress, skeleton, breadcrumb, spinner, BreadcrumbItem
- `burq/components/forms.py` — input, textarea, select, toggle, checkbox, radio, button, file_upload
- `burq/components/feedback.py` — toast, modal, modal_body, modal_footer, alert, open_modal, close_modal
- `burq/components/navigation.py` — tabs, tab, dropdown, DropdownItem, DropdownDivider, DropdownLabel, NavItem, navigate, reload
- `burq/components/data.py` — table, line_chart, bar_chart, donut_chart, fetch, post

### HTML Generator ✅
- `burq/compiler/html_gen.py`
- `render_node()` — walks component tree, dispatches to renderers
- `render_tree()` — renders full page tree
- `render_page_shell()` — full HTML document with layout
- All components have HTML renderers
- Table renders with data-fetch attributes for JS hydration
- Modal renders as overlay divs
- Branding: meta generator tag + HTML comment

---

## Phase 3 — Compiler ⬜ IN PROGRESS

### Next Steps
- [ ] `burq/compiler/js_gen.py` — generates burq.js runtime
  - fetch() calls with auth headers
  - table data hydration
  - onclick handlers
  - navigation (history.pushState)
  - theme toggle
  - sidebar toggle
  - all init functions (tabs, dropdowns, custom selects)
- [ ] `burq/compiler/css_gen.py` — generates tokens.css from Theme
  - wraps compile_tokens() from theme/compiler.py
- [ ] `burq/compiler/html_gen.py` — test and verify output
- [ ] Wire up full compile pipeline: app → dist/

---

## Phase 4 — CRM Demo App ⬜ PLANNED

Build actual CRM pages using burq Python API:
- `pages/dashboard.py` — metrics, recent contacts table, pipeline progress
- `pages/contacts.py` — contacts table, search, filter, add modal
- `pages/contact_detail.py` — contact profile, deals, activities tabs
- `pages/deals.py` — deals table
- `pages/settings.py` — tabs, forms

Connects to existing FastAPI CRM backend at `http://localhost:8000`.

---

## Phase 5 — CLI ⬜ PLANNED

```bash
pip install burq
burq new my-app       # scaffold project
burq dev              # watch + recompile on save
burq build            # production build → dist/
```

Deploy anywhere: S3, Netlify, GitHub Pages, Vercel,
Databricks Apps, nginx

---

## Key Design Decisions
1. **Token first** — never hardcode values in components
2. **Context managers** for layout nesting (Streamlit-inspired)
3. **Imperative calls** for leaf components
4. **oklch color scale** — perceptually uniform, one hex → full scale
5. **Lucide icons** — always, no alternatives
6. **Light + dark** — both themes out of the box, toggle optional
7. **Static output** — pure HTML/CSS/JS, no server at runtime
8. **Deploy anywhere** — S3, Netlify, CDN, Databricks Apps

---

## Tech Stack
- **Python** 3.10+
- **oklch** color scale via `coloraide`
- **Lucide Icons** (always)
- **Space Grotesk** + **Space Mono** (default fonts)
- **Vanilla JS** output (zero runtime dependencies)
- **FastAPI** + **SQLite** (CRM demo backend)
- **Faker** (seed data)

---

## Branding
- Website: https://burq.dev
- Name: Burq (بُرق) — Arabic/Urdu for lightning
- Author: Daniyal
- Every compiled HTML includes:
  - `<meta name="generator" content="Burq ⚡ — https://burq.dev" />`
  - `<!-- ⚡ Built with Burq — https://burq.dev -->`
