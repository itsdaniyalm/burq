# Burq ⚡ — Brand Guidelines

> *Burq (بُرق) — Arabic/Urdu for lightning.*

---

## Name

- Always written as **burq** — all lowercase, no exceptions
- Never: Burq, BURQ, burQ
- Taglines: *"Write Python. Ship UI."* / *"No JS. No apologies."*

---

## Logo

### Mark
Bold curly braces `{ }` with a lightning bolt inside, on a square tile with rounded corners.

```
┌──────────┐
│          │
│  { ⚡ }  │
│          │
└──────────┘
```

- Tile background: `var(--accent)` — adapts to theme
- Braces: white `#ffffff`
- Bolt: white `#ffffff`
- Corner radius: 12px (at 56×56px reference size)
- Must read clearly at 28×28px (topbar size)

### Wordmark
- Font: **Space Grotesk 700**
- Color: single color only — never two-tone
- On dark: `#e8ede9` (foreground)
- On light: `#0a1f14` (foreground)

### Logo variants
| Usage | Value |
|---|---|
| Default (burq logo) | `logo="default"` |
| No logo | `logo=None` |
| Custom SVG | `logo="<svg>...</svg>"` |
| Custom file | `logo="path/to/logo.svg"` or `.png` / `.jpg` |

### Clear space
Minimum clear space = 1× the tile size on all sides.

---

## Color Palette

### Light Theme
| Token | Hex | Usage |
|---|---|---|
| `background` | `#f7f9f7` | Page background |
| `foreground` | `#0a1f14` | Primary text |
| `surface` | `#ffffff` | Cards, inputs |
| `surface_raised` | `#ffffff` | Modals, dropdowns |
| `muted` | `#e8f0eb` | Subtle backgrounds |
| `muted_foreground` | `#5a9070` | Secondary text, icons |
| `accent` | `#0f8a4a` | Primary action color |
| `accent_foreground` | `#ffffff` | Text on accent |
| `border` | `#ccddd4` | Borders |
| `chrome` | `#ffffff` | Topbar, sidebar |
| `chrome_foreground` | `#2d6b4a` | Nav text, topbar text |
| `chrome_border` | `#ccddd4` | Chrome borders |

### Dark Theme
| Token | Hex | Usage |
|---|---|---|
| `background` | `#0a0f0d` | Page background |
| `foreground` | `#e8ede9` | Primary text |
| `surface` | `#0d1710` | Cards, inputs |
| `surface_raised` | `#111a14` | Modals, dropdowns |
| `muted` | `#1a2e22` | Subtle backgrounds |
| `muted_foreground` | `#4a7a62` | Secondary text, icons |
| `accent` | `#2ec97a` | Primary action color |
| `accent_foreground` | `#0a0f0d` | Text on accent |
| `border` | `#1a2e22` | Borders |
| `chrome` | `#0d1710` | Topbar, sidebar |
| `chrome_foreground` | `#7aaa90` | Nav text, topbar text |
| `chrome_border` | `#1a2e22` | Chrome borders |

### Status Colors
| Token | Light | Dark |
|---|---|---|
| Success | `#0f8a4a` | `#2ec97a` |
| Warning | `#c97a2e` | `#c97a2e` |
| Error | `#c92e2e` | `#c92e2e` |

---

## Typography

### Fonts
| Role | Font | Weight |
|---|---|---|
| Display / UI | Space Grotesk | 700 |
| Body / Labels | Space Grotesk | 400, 500 |
| Code / CLI / Mono labels | Space Mono | 400 |

### Scale
| Token | Size | Usage |
|---|---|---|
| `text-xs` | 11px | Badges, mono labels |
| `text-sm` | 12px | Helper text, table sub |
| `text-base` | 14px | Body, inputs, nav |
| `text-md` | 15px | Card titles, modal titles |
| `text-lg` | 16px | Section headings |
| `text-xl` | 20px | Metric values |
| `text-2xl` | 24px | Page titles |

---

## Layout

### Shell
```
┌─────────────────────────────────────────┐
│  TOPBAR (full width, 52px, sticky)      │
│  [ ☰ ] [ logo ] [ burq CRM ] ··· [ 🔔 ]│
├──────────┬──────────────────────────────┤
│ SIDEBAR  │  MAIN CONTENT               │
│ 220px    │  padding: var(--space-6)    │
│ nav only │                             │
└──────────┴──────────────────────────────┘
```

- Topbar always full width — spans over sidebar
- Sidebar starts at `top: 52px`, `height: calc(100vh - 52px)`
- Sidebar toggle (hamburger) is leftmost element in topbar
- Logo lives in topbar, never in sidebar
- Sidebar collapses to 56px via `layout--collapsed`
- `bordered=False` by default — opt in with `Layout(bordered=True)`

---

## Components

### Spacing
- Base unit: 4px (`--space-1`)
- Common gaps: `--space-2` (8px), `--space-3` (12px), `--space-4` (16px), `--space-6` (24px)

### Border Radius
| Token | Value | Usage |
|---|---|---|
| `radius-sm` | 4px | Badges, small elements |
| `radius-md` | 6px | Inputs, buttons |
| `radius-lg` | 8px | Cards, dropdowns |
| `radius-xl` | 12px | Large cards, modals |

### Icons
- **Always Lucide** — no other icon library
- Nav icons: 18×18px
- UI icons: 14–16px
- Never use emoji as icons

---

## Voice & Tone

### Principles
- Direct — no fluff, no filler
- Playful but not juvenile
- Developer-first — assumes technical literacy
- Confident — burq knows what it is

### Examples
| ✅ Do | ❌ Don't |
|---|---|
| *"Write Python. Ship UI."* | *"Build beautiful frontends with ease!"* |
| *"No JS. No apologies."* | *"We handle the JavaScript so you don't have to!"* |
| *"Compiles to Vanilla JS."* | *"Leverages a powerful compilation engine."* |
| *"burq dev"* | *"Start the Burq Development Server"* |

### CLI voice
Short, lowercase, emoji-free:
```
  ✓ base.html
  ✓ contacts.html
  ✓ tokens.css, burq.js
  ⚡ Burq build complete → dist/
```

---

## Generator Tag

Every compiled HTML file includes:
```html
<meta name="generator" content="Burq ⚡ — https://burq.dev" />
<!-- ⚡ Built with Burq — https://burq.dev -->
```

---

## What burq is not

- Not a framework — it's a compiler
- Not Streamlit — output is static files, not a running server
- Not React — zero JS runtime in the output
- Not a design system — it ships one, but that's not the product