import sys
sys.path.insert(0, "../../")

from burq.theme.theme import Theme
from burq.theme.compiler import compile_tokens

theme = Theme(primary="#F0A202", gray="#0E1428", radius="lg", mode="dark")
css = compile_tokens(theme)
print(css)