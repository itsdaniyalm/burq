import os
import sys
import time
import typer
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app_cli = typer.Typer(
    help="burq ⚡ — Python UI compiler",
    add_completion=False,
)

# ── SCAFFOLD TEMPLATES ──

GITIGNORE = """dist/
__pycache__/
*.pyc
.env
"""

APP_PY = '''import burq as bq
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
'''


# ── COMMANDS ──

@app_cli.command()
def new(name: str = typer.Argument(..., help="Project name")):
    """Scaffold a new burq project."""
    base = Path(name)

    if base.exists():
        typer.echo(f"  ✗ Directory '{name}' already exists.")
        raise typer.Exit(1)

    (base / "pages").mkdir(parents=True)
    (base / "components").mkdir(parents=True)
    (base / "dist").mkdir(parents=True)
    (base / "app.py").write_text(APP_PY, encoding="utf-8")
    (base / "pages" / ".gitkeep").write_text("", encoding="utf-8")
    (base / "components" / ".gitkeep").write_text("", encoding="utf-8")
    (base / ".gitignore").write_text(GITIGNORE, encoding="utf-8")

    typer.echo(f"\n⚡ burq project created → {name}/\n")
    typer.echo(f"  cd {name}")
    typer.echo(f"  burq build\n")


@app_cli.command()
def build(
    app_file: str = typer.Option("app.py", "--app", "-a", help="Entry point file"),
    output:   str = typer.Option("dist",   "--out", "-o", help="Output directory"),
):
    """Build for production → dist/"""
    _compile(app_file, output, production=True)


@app_cli.command()
def dev(
    app_file: str = typer.Option("app.py", "--app", "-a", help="Entry point file"),
    output:   str = typer.Option("dist",   "--out", "-o", help="Output directory"),
):
    """Watch for changes and recompile."""
    typer.echo("\n⚡ burq dev — watching for changes...\n")

    _compile(app_file, output, production=False)

    watch_dirs = [d for d in [Path("."), Path("pages"), Path("components")] if d.exists()]

    handler = _BurqReloadHandler(app_file, output)
    observer = Observer()
    for d in watch_dirs:
        observer.schedule(handler, str(d), recursive=True)

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        typer.echo("\n  stopped.\n")
    observer.join()


# ── HELPERS ──

def _compile(app_file: str, output: str, production: bool = False):
    app_path = Path(app_file)
    if not app_path.exists():
        typer.echo(f"  ✗ {app_file} not found.")
        raise typer.Exit(1)

    cwd = str(Path(".").resolve())
    if cwd not in sys.path:
        sys.path.insert(0, cwd)

    # purge everything user-land
    to_delete = [k for k in sys.modules
             if k == "_burq_app"
             or k.startswith("pages")
             or k.startswith("components")
             or (not k.startswith("_")
                 and not k.startswith("burq")
                 and not k.startswith("fastapi")
                 and not k.startswith("starlette")
                 and not k.startswith("importlib")
                 and k not in sys.stdlib_module_names)]
    for k in to_delete:
        del sys.modules[k]

    try:
        import importlib.util
        spec   = importlib.util.spec_from_file_location("_burq_app", app_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        burq_app = None
        import burq as bq
        for attr, obj in vars(module).items():
            if isinstance(obj, bq.App):
                burq_app = obj
                break

        if not burq_app:
            typer.echo("  ✗ No bq.App instance found in app.py")
            raise typer.Exit(1)

        from burq.compiler import compile_app
        compile_app(burq_app, output_dir=output)

    except SystemExit:
        raise
    except Exception as e:
        typer.echo(f"  ✗ compile error: {e}")


class _BurqReloadHandler(FileSystemEventHandler):
    def __init__(self, app_file: str, output: str):
        self.app_file = app_file
        self.output   = output
        self._last    = 0

    def on_modified(self, event):
        if event.is_directory:
            return
        now = time.time()
        if now - self._last < 0.3:
            return
        self._last = now

        path = Path(event.src_path)
        if path.suffix != ".py":
            return
        if "dist" in path.parts or "__pycache__" in path.parts:
            return

        ts = time.strftime("%H:%M:%S")
        typer.echo(f"\n  [{ts}] change detected: {path.name}")
        _compile(self.app_file, self.output, production=False)


def main():
    app_cli()


if __name__ == "__main__":
    main()