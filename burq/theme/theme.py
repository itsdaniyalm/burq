from dataclasses import dataclass, field
from typing import Literal, Optional


@dataclass
class Theme:
    # ── MODE ──
    mode:   Literal["light", "dark", "auto"] = "dark"
    toggle: bool = True

    # ── TYPOGRAPHY ──
    font_sans:      str = "Space Grotesk"
    font_mono:      str = "Space Mono"
    font_size_base: int = 14

    # ── SHAPE ──
    radius:          Literal["none", "sm", "md", "lg", "xl", "2xl"] = "lg"
    spacing_unit:    int = 4
    border_width:    int = 1
    shadow_strength: Literal["none", "sm", "md", "lg"] = "md"

    # ── LIGHT THEME OVERRIDES ──
    light_background:        Optional[str] = None
    light_foreground:        Optional[str] = None
    light_surface:           Optional[str] = None
    light_surface_raised:    Optional[str] = None
    light_muted:             Optional[str] = None
    light_muted_foreground:  Optional[str] = None
    light_accent:            Optional[str] = None
    light_accent_foreground: Optional[str] = None
    light_border:            Optional[str] = None
    light_chrome:            Optional[str] = None
    light_chrome_foreground: Optional[str] = None
    light_chrome_border:     Optional[str] = None

    # ── DARK THEME OVERRIDES ──
    dark_background:        Optional[str] = None
    dark_foreground:        Optional[str] = None
    dark_surface:           Optional[str] = None
    dark_surface_raised:    Optional[str] = None
    dark_muted:             Optional[str] = None
    dark_muted_foreground:  Optional[str] = None
    dark_accent:            Optional[str] = None
    dark_accent_foreground: Optional[str] = None
    dark_border:            Optional[str] = None
    dark_chrome:            Optional[str] = None
    dark_chrome_foreground: Optional[str] = None
    dark_chrome_border:     Optional[str] = None

    # ── STATUS COLOR OVERRIDES ──
    color_success:      Optional[str] = None
    color_success_dark: Optional[str] = None
    color_warning:      Optional[str] = None
    color_warning_dark: Optional[str] = None
    color_error:        Optional[str] = None
    color_error_dark:   Optional[str] = None

    # ── CHART COLORS ──
    chart_colors: Optional[list] = None

    def spacing_scale(self) -> dict:
        u = self.spacing_unit
        return {
            "space-1":  f"{u}px",
            "space-2":  f"{u * 2}px",
            "space-3":  f"{u * 3}px",
            "space-4":  f"{u * 4}px",
            "space-6":  f"{u * 6}px",
            "space-8":  f"{u * 8}px",
            "space-12": f"{u * 12}px",
        }

    def font_scale(self) -> dict:
        b = self.font_size_base
        return {
            "text-xs":   f"{round(b * 0.78)}px",
            "text-sm":   f"{round(b * 0.85)}px",
            "text-base": f"{b}px",
            "text-md":   f"{round(b * 1.14)}px",
            "text-lg":   f"{round(b * 1.42)}px",
            "text-xl":   f"{round(b * 1.71)}px",
            "text-2xl":  f"{round(b * 2.28)}px",
        }

    def radius_scale(self) -> dict:
        fixed = {"none": 0, "sm": 4, "md": 6, "lg": 8, "xl": 12, "2xl": 16}
        return {f"radius-{name}": f"{val}px" for name, val in fixed.items()}

    def shadow_scale(self) -> dict:
        s = {
            "none": (0.00, 0.00, 0.00),
            "sm":   (0.04, 0.08, 0.10),
            "md":   (0.08, 0.15, 0.20),
            "lg":   (0.12, 0.22, 0.30),
        }[self.shadow_strength]
        return {
            "shadow-sm": f"0 1px 4px 0 rgba(0,0,0,{s[0]})",
            "shadow-md": f"0 4px 16px rgba(0,0,0,{s[1]})",
            "shadow-lg": f"0 8px 32px rgba(0,0,0,{s[2]})",
        }