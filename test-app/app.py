import burq as bq
from burq.compiler import compile_app

app = bq.App(
    title="My App",
    author="",
    api_base="http://localhost:8000/api",
    layout=bq.Layout(sidebar=True, topbar=True, bordered=False),
    logo="default",
    theme=bq.Theme(
        radius="md",
        font_sans="Space Grotesk",
        font_mono="Space Mono",
        mode="dark",
        toggle=True,
    )
)

app.nav([
    bq.NavItem("My Page", icon="layout-dashboard", href="/"),
])

@app.page("/")
def dashboard():
    bq.title("Hello, World! ⚡")
    bq.text("Your burq app is ready.", muted=True)
    bq.spacer(size="sm")
    with bq.card("Get Started"):
        bq.text("Write Python. Ship UI.", muted=True)
        bq.spacer(size="md")
        with bq.row():
            bq.button("Docs", variant="primary", icon="book-open", onclick="window.open('https://burq.dev/docs')")
            bq.button("Examples", variant="secondary", icon="layout-dashboard", onclick="window.open('https://burq.dev/examples')")
            bq.button("GitHub", variant="ghost", icon="github", onclick="window.open('https://github.com/itsdaniyalm/burq')")

if __name__ == "__main__":
    compile_app(app, output_dir="dist")
