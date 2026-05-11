import os
from ..app import App
from .html_gen import render_tree, render_page_shell
from .js_gen import generate_js
from .css_gen import generate_css


def compile_app(app: App, output_dir: str = "dist"):
    """
    Full compile pipeline:
    App → tokens.css + layout.css + components.css + burq.js + *.html
    """
    os.makedirs(output_dir, exist_ok=True)

    # ── 1. CSS — tokens ──
    tokens_css = generate_css(app.theme)
    _write(output_dir, "tokens.css", tokens_css)

    # ── 2. JS — runtime ──
    burq_js = generate_js(app)
    _write(output_dir, "burq.js", burq_js)

    # ── 3. Copy static CSS files ──
    _copy_static(output_dir)

    # ── 4. HTML — one file per page ──
    for path, fn in app._pages.items():
        page_tree = app.run_page(path)
        page_html = render_tree(page_tree, app)

        # collect modals for this page
        modal_html = ""
        for name, modal_fn in app._modals.items():
            modal_tree = app.run_modal(name)
            modal_html += render_tree(modal_tree, app)

        slug     = _path_to_slug(path)
        filename = f"{slug}.html"
        title    = fn.__name__.replace("_", " ").title()

        shell = render_page_shell(
            app=app,
            page_content=page_html,
            modal_content=modal_html,
            page_title=title,
        )
        _write(output_dir, filename, shell)
        print(f"  ✓ {filename}")

    print(f"\n⚡ Burq build complete → {output_dir}/")


def _write(directory: str, filename: str, content: str):
    path = os.path.join(directory, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _path_to_slug(path: str) -> str:
    """Convert URL path to filename slug."""
    if path == "/":
        return "index"
    return path.strip("/").replace("/", "-").replace("{", "").replace("}", "")


def _copy_static(output_dir: str):
    """
    Copy layout.css and components.css from dev/crm/ui/
    into the output directory.
    In production this would be bundled differently.
    """
    import shutil
    import pathlib

    # find dev/crm/ui relative to this file
    here    = pathlib.Path(__file__).parent
    ui_dir  = here.parent.parent / "dev" / "crm" / "ui"

    for css_file in ["layout.css", "components.css"]:
        src = ui_dir / css_file
        dst = os.path.join(output_dir, css_file)
        if src.exists():
            shutil.copy(src, dst)
            print(f"  ✓ {css_file}")
        else:
            print(f"  ⚠ {css_file} not found at {src}")