from dataclasses import dataclass, field
from typing import Literal
from .color import generate_scale

@dataclass
class Theme:
    primary: str = "#F0A202"
    gray: str = "#0E1428"
    radius: Literal["none", "sm", "md", "lg", "xl", "2xl"] = "lg"
    font_sans: str = "Space Grotesk"
    font_mono: str = "Space Mono"
    mode: Literal["light", "dark", "auto"] = "light"

    def brand_scale(self) -> dict[int, str]:
        return generate_scale(self.primary)

    def gray_scale(self) -> dict[int, str]:
        return generate_scale(self.gray)