from .theme import Theme
import json as _json

GOOGLE_FONTS_URL = "https://fonts.googleapis.com/css2?family={sans}:wght@300;400;500;600;700&family={mono}:wght@400;700&display=swap"

# ── FILAMENT DEFAULTS ──
LIGHT_DEFAULTS = {
    "background":        "#fef9ed",
    "foreground":        "#1a140a",
    "surface":           "#ffffff",
    "surface_raised":    "#ffffff",
    "muted":             "#f5ecd6",
    "muted_foreground":  "#5c4d2e",
    "accent":            "#F08C1A",
    "accent_foreground": "#ffffff",
    "border":            "#ebe0c2",
    "chrome":            "#ffffff",
    "chrome_foreground": "#5c4d2e",
    "chrome_border":     "#ebe0c2",
}

DARK_DEFAULTS = {
    "background":        "#0a0a0b",
    "foreground":        "#ededee",
    "surface":           "#111113",
    "surface_raised":    "#1e1e22",
    "muted":             "#1e1e22",
    "muted_foreground":  "#8a8a93",
    "accent":            "#F08C1A",
    "accent_foreground": "#0a0a0b",
    "border":            "#2a2a2e",
    "chrome":            "#111113",
    "chrome_foreground": "#8a8a93",
    "chrome_border":     "#2a2a2e",
}

STATUS_DEFAULTS = {
    "color_success":      "#1a7a3c",
    "color_success_dark": "#2ec97a",
    "color_warning":      "#c97a2e",
    "color_warning_dark": "#F08C1A",
    "color_error":        "#c92e2e",
    "color_error_dark":   "#e05252",
}

CHART_COLOR_DEFAULTS = [
    "#F08C1A",
    "#60a5fa",
    "#2ec97a",
    "#e05252",
    "#c97a2e",
    "#a78bfa",
    "#f472b6",
]

def _resolve(theme_val, default: str) -> str:
    """Use theme override if set, otherwise use default."""
    return theme_val if theme_val is not None else default


def compile_tokens(theme: Theme) -> str:
    spacing = theme.spacing_scale()
    fonts   = theme.font_scale()
    radii   = theme.radius_scale()
    shadows = theme.shadow_scale()
    bw      = theme.border_width

    font_url = GOOGLE_FONTS_URL.format(
        sans=theme.font_sans.replace(" ", "+"),
        mono=theme.font_mono.replace(" ", "+")
    )

    # ── resolve light tokens ──
    l = {k: _resolve(getattr(theme, f"light_{k}", None), v) for k, v in LIGHT_DEFAULTS.items()}

    # ── resolve dark tokens ──
    d = {k: _resolve(getattr(theme, f"dark_{k}", None), v) for k, v in DARK_DEFAULTS.items()}

    # ── resolve status tokens ──
    s = {k: _resolve(getattr(theme, k, None), v) for k, v in STATUS_DEFAULTS.items()}

    chart_colors      = theme.chart_colors or CHART_COLOR_DEFAULTS
    chart_colors_json = _json.dumps(chart_colors)

    return f"""@import url('{font_url}');

/* ── PRIMITIVES ── */
:root {{
  --white: #ffffff;
  --black: #0a0a0a;

  /* ── STATUS COLORS ── */
  --color-success:      {s['color_success']};
  --color-success-dark: {s['color_success_dark']};
  --color-error:        {s['color_error']};
  --color-error-dark:   {s['color_error_dark']};
  --color-warning:      {s['color_warning']};
  --color-warning-dark: {s['color_warning_dark']};

  /* ── RADIUS ── */
  --radius-none: {radii['radius-none']};
  --radius-sm:   {radii['radius-sm']};
  --radius-md:   {radii['radius-md']};
  --radius-lg:   {radii['radius-lg']};
  --radius-xl:   {radii['radius-xl']};
  --radius-2xl:  {radii['radius-2xl']};

  /* ── SPACING ── */
  --space-1:  {spacing['space-1']};
  --space-2:  {spacing['space-2']};
  --space-3:  {spacing['space-3']};
  --space-4:  {spacing['space-4']};
  --space-6:  {spacing['space-6']};
  --space-8:  {spacing['space-8']};
  --space-12: {spacing['space-12']};

  /* ── TYPOGRAPHY ── */
  --text-xs:   {fonts['text-xs']};
  --text-sm:   {fonts['text-sm']};
  --text-base: {fonts['text-base']};
  --text-md:   {fonts['text-md']};
  --text-lg:   {fonts['text-lg']};
  --text-xl:   {fonts['text-xl']};
  --text-2xl:  {fonts['text-2xl']};

  --font-sans: '{theme.font_sans}', sans-serif;
  --font-mono: '{theme.font_mono}', monospace;

  /* ── BORDER ── */
  --border-width:   {bw}px;
  --border-width-2: {bw * 2}px;
  --border-width-3: {bw * 3}px;

  /* ── SHADOW ── */
  --shadow-sm: {shadows['shadow-sm']};
  --shadow-md: {shadows['shadow-md']};
  --shadow-lg: {shadows['shadow-lg']};

  /* ── FOCUS RING ── */
  --focus-ring:       0 0 0 3px color-mix(in srgb, var(--accent) 20%, transparent);
  --focus-ring-error: 0 0 0 3px color-mix(in srgb, var(--color-error) 20%, transparent);

  /* ── TRANSITIONS ── */
  --transition-fast: 100ms ease;
  --transition-base: 150ms ease;
  --transition-slow: 200ms ease;

  /* ── Z-INDEX ── */
  --z-dropdown: 150;
  --z-sticky:   10;
  --z-sidebar:  20;
  --z-modal:    200;
  --z-toast:    300;

  /* ── TOAST ── */
  --toast-width: 320px;
  --toast-gap:   var(--space-3);

  /* ── CHART COLORS ── */
  --chart-colors: '{chart_colors_json}';

  /* ── MODAL ── */
  --modal-sm: 400px;
  --modal-md: 560px;
  --modal-lg: 720px;
  --overlay-bg: rgba(0, 0, 0, 0.6);

  /* ── TABS ── */
  --tab-indicator-height: 2px;

  /* ── SKELETON ── */
  --skeleton-bg:    var(--muted);
  --skeleton-shine: var(--surface-raised);

  /* ── PROGRESS ── */
  --progress-bg:     var(--muted);
  --progress-radius: var(--radius-2xl);
}}

/* ── LIGHT THEME ── */
[data-theme="light"] {{
  --background:        {l['background']};
  --foreground:        {l['foreground']};
  --surface:           {l['surface']};
  --surface-raised:    {l['surface_raised']};
  --muted:             {l['muted']};
  --muted-foreground:  {l['muted_foreground']};
  --accent:            {l['accent']};
  --accent-foreground: {l['accent_foreground']};
  --border:            {l['border']};
  --chrome:            {l['chrome']};
  --chrome-foreground: {l['chrome_foreground']};
  --chrome-border:     {l['chrome_border']};
}}

/* ── DARK THEME ── */
[data-theme="dark"] {{
  --background:        {d['background']};
  --foreground:        {d['foreground']};
  --surface:           {d['surface']};
  --surface-raised:    {d['surface_raised']};
  --muted:             {d['muted']};
  --muted-foreground:  {d['muted_foreground']};
  --accent:            {d['accent']};
  --accent-foreground: {d['accent_foreground']};
  --border:            {d['border']};
  --chrome:            {d['chrome']};
  --chrome-foreground: {d['chrome_foreground']};
  --chrome-border:     {d['chrome_border']};
}}

/* ── BASE ── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
  font-family: var(--font-sans);
  font-size: var(--text-base);
  background: var(--background);
  color: var(--foreground);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}}
"""