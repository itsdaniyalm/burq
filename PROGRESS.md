# Burq ⚡ — Development Progress

## Project Structure
```
burq/                          # PyPI package
├── __init__.py
├── app.py
├── context.py
├── compiler/
│   ├── parser.py
│   ├── tree.py
│   ├── html_gen.py
│   ├── js_gen.py
│   └── css_gen.py
├── components/
│   ├── __init__.py
│   ├── layout.py
│   ├── display.py
│   ├── forms.py
│   ├── feedback.py
│   ├── navigation.py
│   └── data.py
├── runtime/
│   └── burq.js
├── theme/
│   ├── __init__.py
│   ├── theme.py
│   ├── color.py
│   └── compiler.py
└── cli/
    └── main.py

dev/                           # never shipped to PyPI
├── crm/
│   ├── backend/
│   │   ├── main.py            # FastAPI app
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── seed.py            # dummy data
│   │   ├── db.py              # SQLite connection
│   │   └── requirements.txt
│   └── ui/
│       ├── tokens.css         # design token system
│       ├── layout.css         # layout components
│       ├── components.css     # all UI components
│       └── index.html         # component playground
└── playground/
    └── test_tokens.py
```

---

## Phase 1 — Design System ✅ COMPLETE

### Token System
- oklch-based color scale generator (`burq/theme/color.py`)
- Full token compiler (`burq/theme/compiler.py`)
- Theme class with primary + gray hex → full scale generation
- Semantic tokens: background, foreground, surface, surface-raised,
  muted, muted-foreground, accent, accent-foreground, border,
  chrome, chrome-foreground, chrome-border
- Scale tokens: radius, spacing, typography, border-width, shadow,
  focus-ring, transitions, z-index, status colors

### Layout Components ✅
- `layout` — grid shell with sidebar + topbar modes
  - `layout--with-sidebar`
  - `layout--with-topbar`
  - `layout--with-sidebar.layout--with-topbar`
  - `layout--collapsed` — sidebar collapses to 56px icons only
  - `layout--bare` — no sidebar, no topbar
- `topbar` — sticky top bar with left/right slots
- `sidebar` — sticky sidebar with logo, nav, footer slots
- `nav-item` — icon + label, active state, collapsed state
- `container` — max-width wrapper (sm|md|lg|xl|full)
- `row` — flexbox horizontal (gap, align, justify, wrap variants)
- `col` — flexbox vertical (gap, align variants)
- `grid` — 12-col CSS grid (cols, gap, row-gap, col-gap, span)
- `divider` — horizontal rule (sm|md|lg, vertical variant)

### UI Components ✅
- `card` — surface container (default|raised|flat|ghost, sm|md|lg)
  - `card__header`, `card__title`, `card__subtitle`
  - `card__body`, `card__footer`
- `badge` — status indicator (default|accent|success|warning|danger|info, sm|md|lg)
  - `badge__dot` — status dot
- `button` — (primary|secondary|ghost|outline|danger × xs|sm|md|lg|icon)
- `metric-card` — KPI display (default|accent|ghost)
  - trend up/down/flat with color tokens
- `table` — data table
  - toolbar with search + filter + export
  - sortable column headers
  - checkbox selection
  - avatar cells
  - badge cells
  - action buttons
  - pagination
  - striped variant
- `form-field` — label + helper + error wrapper
- `input` — text/email/password/number (sm|md|lg, icon, error state)
- `textarea` — multiline input
- `select` — native dropdown (sm|md|lg, error state)
- `custom-select` — searchable dropdown with keyboard navigation
- `toggle` — on/off switch
- `checkbox` — styled checkbox
- `radio` — styled radio
- `toast` — notification (success|error|warning|info, auto-dismiss, stack)
- `modal` — dialog (sm|md|lg, backdrop, ESC close, animation)
- `tabs` — tabbed content (default|pills|card)
- `avatar` — initials/image (xs|sm|md|lg|xl, round, status dot)
- `avatar-group` — overlapping avatars with overflow count
- `skeleton` — loading placeholder (text|avatar|button|rect|card|table, shimmer)
- `progress` — progress bar (default|success|warning|danger, sm|md|lg, striped, animated)
- `dropdown` — action menu (icon+label, divider, danger item, keyboard nav)
- `breadcrumb` — navigation trail (chevron|slash separator)

### JavaScript Runtime (inline) ✅
- `ToastManager` — show/dismiss/auto-dismiss toasts
- `ModalManager` — open/close modals, backdrop click, ESC key
- `initCustomSelects()` — searchable select with keyboard nav
- `initTabs()` — tab switching
- `initDropdowns()` — dropdown open/close, keyboard nav
- Sidebar toggle (collapse/expand)
- `lucide.createIcons()` — Lucide icon rendering

### Backend (CRM Demo) ✅
- FastAPI + SQLite + SQLAlchemy
- Models: Contact, Deal, Activity, DealStatus
- Faker seed data (40 contacts, 1-3 deals each, 1-4 activities each)
- Endpoints:
  - `GET /contacts/`
  - `GET /contacts/{id}`
  - `GET /contacts/{id}/deals`
  - `GET /contacts/{id}/activities`
  - `GET /deals/`
  - `GET /deals/{id}`
  - `GET /activities/`
  - `GET /summary/`
- CORS enabled

---

## Phase 2 — Python API 🔄 IN PROGRESS

### Design Decisions ✅
- Context manager style (Streamlit-inspired)
- Imperative calls inside context managers
- Separate `burq.config.py` for app + theme config
- `burq.Theme` generates full token sheet via oklch

### Theme API (confirmed) ✅
```python
bq.Theme(
    # Brand
    primary="#F0A202",
    gray="#0E1428",
    # Status
    color_success="#16a34a",
    color_warning="#d97706",
    color_error="#dc2626",
    # Radius
    radius="lg",
    # Spacing
    spacing_unit=4,
    # Typography
    font_sans="Space Grotesk",
    font_mono="Space Mono",
    font_size_base=14,
    # Borders
    border_width=1,
    # Shadows
    shadow_strength="md",
    # Mode
    mode="dark",
    toggle=True,
)
```

### Component API (confirmed) ✅
```python
# Layout
with bq.row(gap="md", align="between"):
    ...
with bq.col(gap="lg"):
    ...
with bq.grid(cols=3, gap="md"):
    ...
with bq.card("Title", variant="raised"):
    ...

# Display
bq.title("Dashboard")
bq.heading("Section")
bq.text("Some text", muted=True)
bq.metric("Contacts", "2,480", trend="+12%", trend_dir="up", icon="users")
bq.badge("Active", variant="success")
bq.avatar(initials="JD", size="md", variant="round", status="online")
bq.progress("Revenue", value=72, variant="default")
bq.skeleton(variant="card")
bq.breadcrumb([...], separator="chevron")

# Forms
bq.input("Full Name", required=True, icon="user")
bq.textarea("Notes")
bq.select("Status", options=[...], searchable=True)
bq.toggle("Active", value=True)
bq.checkbox("Subscribe")
bq.radio("Lead", name="type", value="lead")
bq.button("Save", variant="primary", icon="save", onclick=...)

# Feedback
bq.toast("Saved", type="success")
bq.modal("add-contact", title="Add Contact", size="md")

# Navigation
with bq.tabs(["Contacts","Deals"], variant="pills"):
    ...
bq.dropdown(trigger=..., items=[...])

# Data
bq.table(data=..., columns=[...], searchable=True, sortable=True)

# API
bq.fetch("GET", "/contacts/")
bq.post("/contacts/", data)
bq.navigate("/contacts")
bq.reload()
bq.open_modal("add-contact")
bq.close_modal()
```

### Next Steps
- [ ] `burq/theme/theme.py` — full Theme class
- [ ] `burq/context.py` — render context + component tree
- [ ] `burq/components/layout.py` — row, col, grid, card, container, divider
- [ ] `burq/components/display.py` — title, heading, text, metric, badge, avatar, progress, skeleton, breadcrumb
- [ ] `burq/components/forms.py` — input, textarea, select, toggle, checkbox, radio, button
- [ ] `burq/components/feedback.py` — toast, modal
- [ ] `burq/components/navigation.py` — tabs, dropdown, nav
- [ ] `burq/components/data.py` — table
- [ ] `burq/app.py` — App class, page decorator, modal decorator
- [ ] `burq/__init__.py` — public API exports
- [ ] `burq/compiler/` — AST parser + HTML/JS/CSS generators
- [ ] `burq/runtime/burq.js` — tiny browser runtime
- [ ] `burq/cli/main.py` — burq new, burq dev, burq build

---

## Phase 3 — Compiler ⬜ PLANNED

```
1. PARSE    — read .py files → Python AST
2. ANALYZE  — walk AST → pages, components, modals
             resolve bq.fetch() → API endpoints
             resolve component dependencies
3. HTML GEN — each @app.page → one .html file
             components → HTML partials
             modals → hidden HTML divs
4. JS GEN   — bq.fetch() → fetch() with auth headers
             onclick handlers → JS event listeners
             state (depends_on) → JS reactive bindings
             navigation → history.pushState routing
5. CSS GEN  — Theme → tokens.css
             component styles → scoped CSS
6. BUNDLE   — combine into dist/
             minify for production
```

---

## Phase 4 — CRM Demo App ⬜ PLANNED

Build actual CRM pages using burq Python API:
- `pages/dashboard.py` — metrics, charts, recent activity
- `pages/contacts.py` — contacts table, search, filter
- `pages/contact_detail.py` — contact profile, deals, activities
- `pages/deals.py` — deals table, kanban view
- `pages/settings.py` — tabs, forms, file upload

Connects to existing FastAPI CRM backend.

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

## Tech Stack
- **Python** 3.10+
- **oklch** color scale via `coloraide`
- **Lucide Icons** (always, no alternatives)
- **Space Grotesk** + **Space Mono** (default fonts)
- **Vanilla JS** output (zero dependencies)
- **FastAPI** + **SQLite** (CRM demo backend)

## Key Design Principles
1. Token first — never hardcode values in components
2. Context managers for layout nesting
3. Imperative calls for leaf components
4. Lucide icons everywhere
5. Light + dark theme out of the box
6. Deploy anywhere — pure static output
