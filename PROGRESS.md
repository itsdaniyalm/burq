# Burq ⚡ — Development Progress

## Project Structure
```
burq/                          # PyPI package
├── __init__.py                ✅ (accordion, empty_state, pagination added)
├── app.py                     ✅ (logo param, bordered layout, dummy kwargs for dynamic routes)
├── context.py                 ✅
├── compiler/
│   ├── __init__.py            ✅ (removed burq_routes.py generation — FastAPI owns routing)
│   ├── html_gen.py            ✅ (logo system, new components, layout fix)
│   ├── js_gen.py              ✅ (initAccordions added)
│   └── css_gen.py             ✅
├── components/
│   ├── __init__.py            ✅
│   ├── layout.py              ✅
│   ├── display.py             ✅
│   ├── forms.py               ✅ (toggle accepts checked= alias)
│   ├── feedback.py            ✅
│   ├── navigation.py          ✅
│   ├── extra.py               ✅ (accordion, empty_state, pagination)
│   └── data.py                ✅
├── theme/
│   ├── __init__.py            ✅
│   ├── theme.py               ✅
│   ├── color.py               ✅ (kept for future theme generator)
│   └── compiler.py            ✅ (Meridian-inspired hardcoded tokens)
└── cli/
    └── main.py                ⬜

dev/                           # never shipped to PyPI
├── crm/
│   ├── backend/
│   │   ├── main.py            ✅ (manual page routes, no burq_routes import)
│   │   ├── models.py          ✅
│   │   ├── seed.py            ✅
│   │   ├── db.py              ✅
│   │   └── requirements.txt   ✅
│   └── ui/
│       ├── layout.css         ✅ (topbar full width, sidebar below topbar)
│       └── components.css     ✅ (accordion, empty_state, pagination added)
└── playground/
    ├── test_tokens.py         ✅
    ├── test_api.py            ✅
    └── test_compile.py        ✅ (settings page added)

dist/                          # compiled output (gitignored)
├── templates/
│   ├── base.html              ✅
│   ├── index.html             ✅
│   ├── contacts.html          ✅
│   ├── deals.html             ✅
│   ├── settings.html          ✅
│   └── contacts_contact_id.html ✅
└── static/
    ├── burq.js                ✅
    ├── tokens.css             ✅
    ├── layout.css             ✅
    └── components.css         ✅
```

---

## Phase 1 — Design System ✅ COMPLETE

### Token System ✅
- Hardcoded Meridian-inspired defaults for light + dark
- Full override params via Theme() — every semantic token overridable
- Spacing, typography, radius, shadow, z-index, component tokens intact
- oklch color.py kept for future theme generator utility

### Layout Components ✅
- `layout`, `topbar`, `sidebar`, `nav-item`, `container`, `row`, `col`, `grid`, `divider`, `spacer`
- **Topbar spans full width** — logo + toggle live in topbar, sidebar starts below
- **Sidebar** `top: 52px`, `height: calc(100vh - 52px)` — always below topbar
- **Toggle before logo** in topbar (hamburger → logo → app title)
- `bordered=False` default — clean borderless chrome, opt-in via `Layout(bordered=True)`
- Logo system: `"default"` = burq logo, `None` = no logo, SVG string, or file path (svg/png/jpg)
- Collapse support via `layout--collapsed`

### UI Components ✅
- `card`, `badge`, `button`, `metric-card`, `table`
- `input`, `textarea`, `select`, `custom-select`, `toggle`, `checkbox`, `radio`
- `toast`, `modal`, `tabs`, `avatar`, `avatar-group`
- `skeleton`, `progress`, `dropdown`, `breadcrumb`, `spinner`, `alert`
- **NEW:** `accordion`, `empty_state`, `pagination`

### JavaScript Runtime ✅
- `ToastManager`, `ModalManager`, `initTabs()`, `initDropdowns()`
- `initCustomSelects()`, `initTables()`, `initSidebar()`, `initThemeToggle()`
- `initActiveNav()` — active nav via data-href + URL match
- `initUrlParams()` — extracts URL params into window.__burqParams
- `initTableExport()` — client-side CSV export
- `initAccordions()` — toggle panels, supports multiple=True
- Table search + pagination (client-side, PAGE_SIZE=10)
- Theme toggle with localStorage persistence

### Backend (CRM Demo) ✅
- FastAPI + SQLite + SQLAlchemy
- All API routes prefixed with `/api`
- Models: Contact (with status), Deal, Activity, DealStatus
- **Page routes manually defined** — no burq_routes dependency
- Serves Jinja2 templates from `dist/templates/`
- Serves static files from `dist/static/`

---

## Phase 2 — Python API ✅ COMPLETE

### App & Config ✅
```python
app = bq.App(
    title="My App",
    author="Daniyal",
    api_base="http://localhost:8000/api",
    layout=bq.Layout(sidebar=True, topbar=True, bordered=False),
    logo="default",          # "default" | None | "<svg>..." | "path/to/logo.png"
    theme=bq.Theme(
        radius="md",
        font_sans="Space Grotesk",
        font_mono="Space Mono",
        mode="dark",
        toggle=True,
    )
)
```

### Column Config System ✅
- `AvatarColumn`, `BadgeColumn`, `CurrencyColumn`, `DateColumn`, `BoolColumn`, `TextColumn`

### New Components API ✅
```python
bq.accordion(items=[
    {"title": "Q?", "content": "A.", "open": True},
])

bq.empty_state(
    title="No results",
    message="Try adjusting your filters.",
    icon="inbox",
    action={"label": "Add Contact", "icon": "plus", "onclick": "..."}
)

bq.pagination(total=120, page=1, per_page=10, on_change="loadPage")
```

---

## Phase 3 — Compiler ✅ COMPLETE

### Routing ✅ REVISED
- **Burq no longer generates `burq_routes.py`** — FastAPI owns all routing
- Each `@app.page("/route")` → Jinja2 template only
- Dynamic routes `@app.page("/contacts/{id}")` → inline param extraction script
- `window.__burqParams` set before `burq.js` loads
- `Burq.fetch()` interpolates `{param}` from `__burqParams`
- User manually defines FastAPI page routes pointing to compiled templates

### Architecture (Revised) ✅
```
FastAPI  → routing, auth, data APIs, serving templates
Burq     → compile .py → .html templates + JS + CSS
Browser  → JS reads URL params, fetches data from FastAPI APIs
```

---

## Phase 4 — CRM Demo App ✅ COMPLETE

### Done ✅
- `dashboard` page — metrics, contacts table, pipeline
- `contacts` page — full table with AvatarColumn, BadgeColumn, DateColumn
- `deals` page — full table with BadgeColumn, CurrencyColumn
- `contact_detail` page — dynamic route, deals + activities tabs
- `settings` page — tabs, accordion, toggles, alert, danger zone
- Active nav, theme toggle, sidebar collapse, light/dark mode
- Table search, pagination, CSV export all working
- Route ordering fix — static routes registered before parameterized

### Still needed ⬜
- `contact_detail` profile header — dynamic fetch for name/status/phone/company
- Nav link from contacts table row → contact detail page
- Empty state on tables with no data

---

## Phase 5 — CLI ⬜ PLANNED

```bash
pip install burq
burq new my-app       # scaffold project
burq dev              # watch + recompile + serve
burq build            # production build → dist/
```

---

## Key Design Decisions
1. **Token first** — never hardcode values in components
2. **Context managers** for layout nesting (Streamlit-inspired)
3. **Imperative calls** for leaf components
4. **Hardcoded Meridian-inspired defaults** — predictable, no generation surprises
5. **Lucide icons** — always, no alternatives
6. **Light + dark** — both themes, toggle optional
7. **FastAPI owns routing** — Burq compiles templates only, no route generation
8. **column_config** — declarative column rendering
9. **Logo system** — default/None/SVG string/file path
10. **Dynamic routes** — `{param}` in page path → JS extracts from URL
11. **bordered=False default** — clean borderless chrome, opt-in
12. **Topbar owns logo** — sidebar is nav-only, logo always visible

---

## Tech Stack
- **Python** 3.10+
- **Jinja2** — template rendering
- **Lucide Icons**
- **Space Grotesk** + **Space Mono** (default fonts)
- **Vanilla JS** (zero runtime dependencies)
- **FastAPI** + **SQLite** (CRM demo backend)
- **Faker** (seed data)

---

## Branding
- Website: https://burq.dev
- Name: Burq (بُرق) — Arabic/Urdu for lightning
- Author: Daniyal
- Logo: accent-colored square, white braces + white bolt, adapts to theme
- Every compiled HTML includes:
  - `<meta name="generator" content="Burq ⚡ — https://burq.dev" />`
  - `<!-- ⚡ Built with Burq — https://burq.dev -->`