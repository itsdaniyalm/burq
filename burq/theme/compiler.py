from .theme import Theme

GOOGLE_FONTS_URL = "https://fonts.googleapis.com/css2?family={sans}:wght@300;400;500;600;700&family={mono}:wght@400;700&display=swap"

RADIUS_MAP = {
    "none": "0px",
    "sm":   "4px",
    "md":   "6px",
    "lg":   "8px",
    "xl":   "12px",
    "2xl":  "16px",
}

def compile_tokens(theme: Theme) -> str:
    brand = theme.brand_scale()
    gray  = theme.gray_scale()

    font_url = GOOGLE_FONTS_URL.format(
        sans=theme.font_sans.replace(" ", "+"),
        mono=theme.font_mono.replace(" ", "+")
    )

    radius_base = RADIUS_MAP[theme.radius]

    return f"""@import url('{font_url}');

/* ── PRIMITIVES ── */
:root {{
  --gray-100: {gray[100]};
  --gray-200: {gray[200]};
  --gray-300: {gray[300]};
  --gray-400: {gray[400]};
  --gray-500: {gray[500]};
  --gray-600: {gray[600]};
  --gray-700: {gray[700]};
  --gray-800: {gray[800]};
  --gray-900: {gray[900]};

  --brand-100: {brand[100]};
  --brand-200: {brand[200]};
  --brand-400: {brand[400]};
  --brand-500: {brand[500]};
  --brand-600: {brand[600]};
  --brand-700: {brand[700]};

  --white: #ffffff;
  --black: #0a0a0a;

  /* ── RADIUS ── */
  --radius-none: 0px;
  --radius-sm:   {_step(radius_base, 0)};
  --radius-md:   {_step(radius_base, 1)};
  --radius-lg:   {_step(radius_base, 2)};
  --radius-xl:   {_step(radius_base, 3)};
  --radius-2xl:  {_step(radius_base, 4)};

  /* ── SPACING ── */
  --space-1:  4px;
  --space-2:  8px;
  --space-3:  12px;
  --space-4:  16px;
  --space-6:  24px;
  --space-8:  32px;
  --space-12: 48px;

  /* ── TYPOGRAPHY ── */
  --text-xs:   11px;
  --text-sm:   12px;
  --text-base: 14px;
  --text-md:   16px;
  --text-lg:   20px;
  --text-xl:   24px;
  --text-2xl:  32px;

  --font-sans: '{theme.font_sans}', sans-serif;
  --font-mono: '{theme.font_mono}', monospace;
}}

/* ── LIGHT THEME ── */
[data-theme="light"] {{
  --background:        var(--white);
  --foreground:        var(--gray-900);
  --surface:           var(--gray-100);
  --surface-raised:    var(--white);
  --muted:             var(--gray-100);
  --muted-foreground:  var(--gray-500);
  --accent:            var(--brand-700);
  --accent-foreground: var(--white);
  --border:            var(--gray-200);
  --chrome:            var(--gray-900);
  --chrome-foreground: var(--gray-400);
  --chrome-border:     var(--gray-600);
}}

/* ── DARK THEME ── */
[data-theme="dark"] {{
  --background:        var(--gray-900);
  --foreground:        var(--gray-100);
  --surface:           var(--gray-800);
  --surface-raised:    var(--gray-700);
  --muted:             var(--gray-600);
  --muted-foreground:  var(--gray-400);
  --accent:            var(--brand-500);
  --accent-foreground: var(--gray-900);
  --border:            var(--gray-600);
  --chrome:            var(--gray-800);
  --chrome-foreground: var(--gray-400);
  --chrome-border:     var(--gray-600);
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

def _step(base: str, steps: int) -> str:
    """Increment radius by 2px per step from base."""
    base_val = int(base.replace("px", ""))
    return f"{base_val + (steps * 2)}px"