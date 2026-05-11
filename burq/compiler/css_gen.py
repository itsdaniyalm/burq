from ..theme.theme import Theme
from ..theme.compiler import compile_tokens


def generate_css(theme: Theme) -> str:
    """Generate tokens.css from Theme config."""
    return compile_tokens(theme)