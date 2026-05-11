from .theme import Theme

GOOGLE_FONTS_URL = "https://fonts.googleapis.com/css2?family={sans}:wght@300;400;500;600;700&family={mono}:wght@400;700&display=swap"

def compile_tokens(theme: Theme) -> str:
    brand   = theme.brand_scale()
    gray    = theme.gray_scale()
    success = theme.success_scale()
    warning = theme.warning_scale()
    error   = theme.error_scale()
    spacing = theme.spacing_scale()
    fonts   = theme.font_scale()
    radii   = theme.radius_scale()
    shadows = theme.shadow_scale()

    font_url = GOOGLE_FONTS_URL.format(
        sans=theme.font_sans.replace(" ", "+"),
        mono=theme.font_mono.replace(" ", "+")
    )

    bw  = theme.border_width

    return f"""@import url('{font_url}');

/* ── PRIMITIVES ── */
:root {{
  /* gray scale */
  --gray-100: {gray[100]};
  --gray-200: {gray[200]};
  --gray-300: {gray[300]};
  --gray-400: {gray[400]};
  --gray-500: {gray[500]};
  --gray-600: {gray[600]};
  --gray-700: {gray[700]};
  --gray-800: {gray[800]};
  --gray-900: {gray[900]};

  /* brand scale */
  --brand-100: {brand[100]};
  --brand-200: {brand[200]};
  --brand-400: {brand[400]};
  --brand-500: {brand[500]};
  --brand-600: {brand[600]};
  --brand-700: {brand[700]};

  --white: #ffffff;
  --black: #0a0a0a;

  /* ── STATUS COLORS ── */
  --color-success:      {success[500]};
  --color-success-dark: {success[300]};
  --color-error:        {error[500]};
  --color-error-dark:   {error[300]};
  --color-warning:      {warning[500]};
  --color-warning-dark: {warning[300]};

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