import os
import pathlib
import shutil
from ..app import App
from .html_gen import render_tree, render_base_template, render_page_template
from .js_gen import generate_js
from .css_gen import generate_css


def compile_app(app: App, output_dir: str = "dist"):
    templates_dir = os.path.join(output_dir, "templates")
    static_dir    = os.path.join(output_dir, "static")
    os.makedirs(templates_dir, exist_ok=True)
    os.makedirs(static_dir,    exist_ok=True)

    # ── 1. base.html ──
    _write(templates_dir, "base.html", render_base_template(app))
    print("  ✓ base.html")

    # ── 2. per-page templates ──
    for path, fn in app._pages.items():
        page_tree     = app.run_page(path)
        page_content  = render_tree(page_tree, app)
        modal_content = ""
        for name in app._modals:
            modal_tree     = app.run_modal(name)
            modal_content += render_tree(modal_tree, app)

        filename = _path_to_filename(path)
        _write(templates_dir, filename, render_page_template(page_content, modal_content, url_pattern=path))
        print(f"  ✓ templates/{filename}")

    # ── 3. static: tokens.css + burq.js ──
    _write(static_dir, "tokens.css", generate_css(app.theme))
    _write(static_dir, "burq.js",    generate_js(app))
    print("  ✓ tokens.css, burq.js")

    # ── 4. copy layout.css + components.css → static/ ──
    _copy_static(static_dir)

    print(f"\n⚡ Burq build complete → {output_dir}/")


def _path_to_filename(path: str) -> str:
    clean = path.strip("/").replace("{", "").replace("}", "").replace("/", "_")
    return (clean or "index") + ".html"


def _write(directory: str, filename: str, content: str):
    path = os.path.join(directory, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _copy_static(static_dir: str):
    here   = pathlib.Path(__file__).parent
    ui_dir = here.parent.parent / "dev" / "crm" / "ui"
    for css_file in ["layout.css", "components.css"]:
        src = ui_dir / css_file
        dst = os.path.join(static_dir, css_file)
        if src.exists():
            shutil.copy(src, dst)
            print(f"  ✓ {css_file}")
        else:
            print(f"  ⚠ {css_file} not found at {src}")