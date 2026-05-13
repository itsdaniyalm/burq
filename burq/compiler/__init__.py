import os
import time
import pathlib
from ..app import App
from .html_gen import render_tree, render_base_template, render_page_template
from .js_gen import generate_js
from .css_gen import generate_css, generate_layout_css, generate_components_css


def compile_app(app: App, output_dir: str = "dist"):
    start = time.perf_counter()  # ← start timer

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

    # ── 3. static ──
    _write(static_dir, "tokens.css",     generate_css(app.theme))
    _write(static_dir, "layout.css",     generate_layout_css())
    _write(static_dir, "components.css", generate_components_css())
    _write(static_dir, "burq.js",        generate_js(app))
    print("  ✓ tokens.css, layout.css, components.css, burq.js")

    elapsed = (time.perf_counter() - start) * 1000  # ← end timer
    print(f"\n⚡ Burq build complete → {output_dir}/  [{elapsed:.0f}ms]")


def _path_to_filename(path: str) -> str:
    clean = path.strip("/").replace("{", "").replace("}", "").replace("/", "_")
    return (clean or "index") + ".html"


def _write(directory: str, filename: str, content: str):
    path = os.path.join(directory, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)