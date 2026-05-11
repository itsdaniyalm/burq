from dataclasses import dataclass
from typing import Literal
from .color import generate_scale

@dataclass
class Theme:
    # ── BRAND ──
    primary: str = "#FEE715"
    gray: str    = "#101820"

    # ── STATUS COLORS ──
    color_success: str = "#0f8a4a"
    color_warning: str = "#c97a2e"
    color_error:   str = "#c92e2e"

    # ── RADIUS ──
    radius: Literal["none","sm","md","lg","xl","2xl"] = "lg"

    # ── SPACING ──
    spacing_unit: int = 4

    # ── TYPOGRAPHY ──
    font_sans:      str = "Space Grotesk"
    font_mono:      str = "Space Mono"
    font_size_base: int = 14

    # ── BORDERS ──
    border_width: int = 1

    # ── SHADOWS ──
    shadow_strength: Literal["none","sm","md","lg"] = "md"

    # ── MODE ──
    mode:   Literal["light","dark","auto"] = "dark"
    toggle: bool = True

    def brand_scale(self)   -> dict[int, str]: return generate_scale(self.primary)
    def gray_scale(self)    -> dict[int, str]: return generate_scale(self.gray)
    def success_scale(self) -> dict[int, str]: return generate_scale(self.color_success)
    def warning_scale(self) -> dict[int, str]: return generate_scale(self.color_warning)
    def error_scale(self)   -> dict[int, str]: return generate_scale(self.color_error)

    def spacing_scale(self) -> dict[str, str]:
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

    def font_scale(self) -> dict[str, str]:
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

    def radius_scale(self) -> dict[str, str]:
        fixed = {"none": 0, "sm": 4, "md": 6, "lg": 8, "xl": 12, "2xl": 16}
        return {f"radius-{name}": f"{val}px" for name, val in fixed.items()}

    def shadow_scale(self) -> dict[str, str]:
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