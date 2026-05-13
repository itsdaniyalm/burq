# Burq ⚡ — Development Progress

## Project Structure
```
burq/                          # PyPI package
├── __init__.py                ✅
├── app.py                     ✅ (logo param, dummy kwargs for dynamic routes)
├── context.py                 ✅
├── compiler/
│   ├── __init__.py            ✅ (url_pattern passed to render_page_template)
│   ├── html_gen.py            ✅ (param_script injection for dynamic routes)
│   ├── js_gen.py              ✅ (Burq.fetch interpolates __burqParams, export as raw string)
│   └── css_gen.py             ✅
├── components/
│   ├── __init__.py            ✅
│   ├── layout.py              ✅ (spacer added)
│   ├── display.py             ✅
│   ├── forms.py               ✅
│   ├── feedback.py            ✅
│   ├── navigation.py          ✅
│   └── data.py                ✅
├── theme/
│   ├── __init__.py            ✅
│   ├── theme.py               ✅ (hardcoded defaults, full override params)
│   ├── color.py               ✅ (kept for future theme generator)
│   └── compiler.py            ✅ (Meridian-inspired hardcoded tokens)
└── cli/
    └── main.py                ⬜

dev/                           # never shipped to PyPI
├── crm/
│   ├── backend/
│   │   ├── main.py            ✅ (all API routes /api prefixed)
│   │   ├── models.py          ✅ (Contact has status field)
│   │   ├── seed.py            ✅
│   │   ├── db.py              ✅
│   │   └── requirements.txt   ✅
│   └── ui/
│       ├── layout.css         ✅
│       ├── components.css     ✅
└── playground/
    ├── test_tokens.py         ✅
    ├── test_api.py            ✅
    └── test_compile.py        ✅

dist/                          # compiled output (gitignored)
├── templates/
│   ├── base.html              ✅
│   ├── index.html             ✅
│   ├── contacts.html          ✅
│   ├── deals.html             ✅
│   └── contacts_contact_id.html ✅
├── static/
│   ├── burq.js                ✅
│   ├── tokens.css             ✅
│   ├── layout.css             ✅
│   └── components.css         ✅
└── burq_routes.py             ✅
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
- Burger in sidebar, seamless chrome, collapse support
- Logo configurable via `app.logo`

### UI Components ✅
- `card`, `badge`, `button`, `metric-card`, `table`
- `input`, `textarea`, `select`, `custom-select`, `toggle`, `checkbox`, `radio`
- `toast`, `modal`, `tabs`, `avatar`, `avatar-group`
- `skeleton`, `progress`, `dropdown`, `breadcrumb`, `spinner`, `alert`

### JavaScript Runtime ✅
- `ToastManager`, `ModalManager`, `initTabs()`, `initDropdowns()`
- `initCustomSelects()`, `initTables()`, `initSidebar()`, `initThemeToggle()`
- `initActiveNav()` — active nav via data-href + URL match
- `initUrlParams()` — extracts URL params into window.__burqParams
- `initTableExport()` — client-side CSV export (raw string, no f-string issues)
- Table search + pagination (client-side, PAGE_SIZE=10)
- Theme toggle with localStorage persistence

### Backend (CRM Demo) ✅
- FastAPI + SQLite + SQLAlchemy
- All API routes prefixed with `/api`
- Models: Contact (with status), Deal, Activity, DealStatus
- Serves Jinja2 templates via burq_routes router
- Serves static files from dist/static/

---

## Phase 2 — Python API ✅ COMPLETE

### App & Config ✅
```python
app = bq.App(
    title="My App",
    author="Daniyal",
    api_base="http://localhost:8000/api",
    layout=bq.Layout(sidebar=True, topbar=True),
    logo="<svg>...</svg>",   # optional
    theme=bq.Theme(
        radius="md",
        font_sans="Space Grotesk",
        font_mono="Space Mono",
        mode="dark",
        toggle=True,
        # optional overrides:
        # dark_accent="#2ec97a"
        # light_background="#f7f9f7"
    )
)
```

### Column Config System ✅
- `AvatarColumn`, `BadgeColumn`, `CurrencyColumn`, `DateColumn`, `BoolColumn`, `TextColumn`

---

## Phase 3 — Compiler ✅ COMPLETE

### Routing ✅
- Each `@app.page("/route")` → Jinja2 template + FastAPI route
- Dynamic routes `@app.page("/contacts/{id}")` → inline param extraction script
- `window.__burqParams` set before `burq.js` loads
- `Burq.fetch()` interpolates `{param}` from `__burqParams`
- `app.run_page()` passes dummy kwargs for dynamic route compilation

---

## Phase 4 — CRM Demo App 🔄 IN PROGRESS

### Done ✅
- `dashboard` page — metrics, contacts table, pipeline
- `contacts` page — full table with AvatarColumn, BadgeColumn, DateColumn
- `deals` page — full table with BadgeColumn, CurrencyColumn
- `contact_detail` page — dynamic route, deals + activities tabs
- Active nav, theme toggle, sidebar collapse, light/dark mode
- Table search, pagination, CSV export all working

### Still needed ⬜
- `settings` page — tabs + forms
- `contact_detail` profile header — dynamic fetch for name/status/phone/company
- Nav link from contacts table row → contact detail page

---

## Phase 5 — CLI ⬜ PLANNED

```bash
pip install burq
burq new my-app
burq dev
burq build
```

---

## Key Design Decisions
1. **Token first** — never hardcode values in components
2. **Context managers** for layout nesting (Streamlit-inspired)
3. **Imperative calls** for leaf components
4. **Hardcoded Meridian-inspired defaults** — predictable, no generation surprises
5. **Lucide icons** — always, no alternatives
6. **Light + dark** — both themes, toggle optional
7. **FastAPI/Jinja2 routing** — FastAPI owns all routing
8. **column_config** — declarative column rendering
9. **Logo configurable** — `app.logo` accepts any SVG string
10. **Dynamic routes** — `{param}` in page path → JS extracts from URL

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
