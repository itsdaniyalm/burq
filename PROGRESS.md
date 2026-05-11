Here's the updated `PROGRESS.md`:

```markdown
# Burq ⚡ — Development Progress

## Project Structure
```
burq/                          # PyPI package
├── __init__.py                ✅
├── app.py                     ✅ (logo param added)
├── context.py                 ✅
├── compiler/
│   ├── __init__.py            ✅ (outputs templates/ + static/ + burq_routes.py)
│   ├── html_gen.py            ✅ (Jinja2 base + page templates)
│   ├── js_gen.py              ✅ (initActiveNav added)
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
│   ├── color.py               ✅ (kept, unused in compiler)
│   └── compiler.py            ✅ (Meridian-inspired hardcoded tokens)
└── cli/
    └── main.py                ⬜

dev/                           # never shipped to PyPI
├── crm/
│   ├── backend/
│   │   ├── main.py            ✅ (FastAPI + Jinja2 routing via burq_routes)
│   │   ├── models.py          ✅ (Contact has status field)
│   │   ├── seed.py            ✅ (Contact seeded with random status)
│   │   ├── db.py              ✅
│   │   └── requirements.txt   ✅
│   └── ui/
│       ├── layout.css         ✅ (burger in sidebar, seamless chrome)
│       ├── components.css     ✅
│       └── tokens.css         ⬜ (generated, not hand-authored)
└── playground/
    ├── test_tokens.py         ✅
    ├── test_api.py            ✅
    └── test_compile.py        ✅

dist/                          # compiled output (gitignored)
├── templates/
│   ├── base.html              ✅
│   ├── index.html             ✅
│   └── contacts.html          ✅
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
- Theme class with explicit override params for every semantic token
- Hardcoded Meridian-inspired defaults for light + dark (no oklch generation)
- User can override any token via `Theme(light_background="#...", dark_accent="#...")`
- Semantic tokens: background, foreground, surface, surface-raised,
  muted, muted-foreground, accent, accent-foreground, border,
  chrome, chrome-foreground, chrome-border
- Status color tokens: color-success/warning/error + dark variants
- Spacing, typography, radius, shadow, z-index, component tokens all intact
- oklch `color.py` kept for future theme generator utility

### Layout Components ✅
- `layout` — grid shell with 4 modes
- `topbar` — sticky, right slots, theme toggle
- `sidebar` — sticky, logo (configurable via `app.logo`), nav, footer, burger toggle
- `nav-item` — icon + label, active state (JS-driven), collapsed state
- `container`, `row`, `col`, `grid`, `divider`, `spacer`

### UI Components ✅
- `card`, `badge`, `button`, `metric-card`, `table`
- `input`, `textarea`, `select`, `custom-select`, `toggle`, `checkbox`, `radio`
- `toast`, `modal`, `tabs`, `avatar`, `avatar-group`
- `skeleton`, `progress`, `dropdown`, `breadcrumb`, `spinner`, `alert`

### JavaScript Runtime ✅
- `ToastManager`, `ModalManager`, `initTabs()`, `initDropdowns()`
- `initCustomSelects()`, `initTables()`, `initSidebar()`, `initThemeToggle()`
- `initActiveNav()` — sets active nav item based on current URL
- Table hydration with `column_config` support
- Theme toggle with localStorage persistence

### Backend (CRM Demo) ✅
- FastAPI + SQLite + SQLAlchemy
- Models: Contact (with status), Deal, Activity, DealStatus
- Endpoints: contacts, deals, activities, summary
- Serves Jinja2 templates via burq_routes router
- Serves static files from dist/static/
- CORS enabled

---

## Phase 2 — Python API ✅ COMPLETE

### App & Config ✅
```python
app = bq.App(
    title="My App",
    author="Daniyal",
    api_base="http://localhost:8000",
    layout=bq.Layout(sidebar=True, topbar=True),
    logo="<svg>...</svg>",   # optional, defaults to Burq mark
    theme=bq.Theme(
        radius="md",
        spacing_unit=4,
        font_sans="Space Grotesk",
        font_mono="Space Mono",
        font_size_base=14,
        border_width=1,
        shadow_strength="md",
        mode="dark",
        toggle=True,
        # optional overrides:
        # dark_accent="#2ec97a"
        # light_background="#f7f9f7"
    )
)
```

### Column Config System ✅
```python
bq.table(
    data=bq.fetch("GET", "/contacts/"),
    columns=["name", "company", "status", "value", "created_at", "active"],
    column_config={
        "name":       bq.AvatarColumn(sub_key="email"),
        "status":     bq.BadgeColumn(variant_map={
                          "lead": "default", "qualified": "info",
                          "won": "success",  "lost": "danger",
                      }),
        "value":      bq.CurrencyColumn(prefix="$", decimals=2),
        "created_at": bq.DateColumn(),
        "active":     bq.BoolColumn(true_label="Yes", false_label="No"),
        "company":    bq.TextColumn(muted=True),
    }
)
```

---

## Phase 3 — Compiler ✅ COMPLETE

### Routing ✅ RESOLVED
- Each `@app.page("/route")` → Jinja2 template + FastAPI route
- Compiler outputs `dist/templates/base.html` + per-page templates
- Compiler outputs `dist/burq_routes.py` — auto-generated FastAPI router
- User wires in one line: `app.include_router(burq_router)`
- FastAPI owns all routing — real URLs, browser back/forward works
- Static files served from `dist/static/` via `/static/` mount

### Compiler Pipeline ✅
- `html_gen.py` — component tree → Jinja2 templates
- `js_gen.py` — generates `burq.js` runtime
- `css_gen.py` — generates `tokens.css` from Theme
- `compiler/__init__.py` — full `compile_app()` pipeline

---

## Phase 4 — CRM Demo App 🔄 IN PROGRESS

### Done
- `dashboard` page — metrics grid, contacts table, pipeline progress
- `contacts` page — full table with AvatarColumn, BadgeColumn, DateColumn
- Active nav, theme toggle, sidebar collapse all working
- Light + dark mode both polished

### Still needed
- `deals` page — deals table with BadgeColumn for status
- `contact_detail` page — profile, deals, activities tabs
- `settings` page — tabs, forms

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
7. **FastAPI/Jinja2 routing** — FastAPI owns all routing, no SPA complexity
8. **column_config** — declarative column rendering, never hardcoded
9. **Logo configurable** — `app.logo` accepts any SVG string

---

## Tech Stack
- **Python** 3.10+
- **Jinja2** — template rendering
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
- Logo: accent-colored square, white braces + white bolt, adapts to theme
- Every compiled HTML includes:
  - `<meta name="generator" content="Burq ⚡ — https://burq.dev" />`
  - `<!-- ⚡ Built with Burq — https://burq.dev -->`
```