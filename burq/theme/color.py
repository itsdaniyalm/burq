from coloraide import Color

SHADE_LIGHTNESS = {
    100: 0.95,
    200: 0.88,
    300: 0.78,
    400: 0.65,
    500: 0.52,
    600: 0.42,
    700: 0.32,
    800: 0.20,
    900: 0.12,
}

def generate_scale(hex_color: str) -> dict[int, str]:
    """Given one hex color, returns a dict of 9 shades in hex."""
    base = Color(hex_color).convert("oklch")
    chroma = base["chroma"]
    hue = base["hue"]

    scale = {}
    for shade, lightness in SHADE_LIGHTNESS.items():
        c = Color("oklch", [lightness, chroma, hue])
        scale[shade] = c.convert("srgb").to_string(hex=True)

    return scale


if __name__ == "__main__":
    scale = generate_scale("#F0A202")
    for shade, hex_val in scale.items():
        print(f"brand-{shade}: {hex_val}")