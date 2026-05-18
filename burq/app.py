import traceback
import linecache
from dataclasses import dataclass, field
from typing import Callable
from .theme.theme import Theme
from .context import reset_context, get_context


@dataclass
class Layout:
    sidebar:    bool = True
    topbar:     bool = True
    bordered:   bool = False
    show_title: bool = False


class App:
    def __init__(
        self,
        title:    str    = "Burq App",
        author:   str    = "",
        api_base: str    = "",
        api_key:  str    = "",
        layout:   Layout = None,
        theme:    Theme  = None,
        logo:     str    = "default",
    ):
        self.title    = title
        self.author   = author
        self.api_base = api_base
        self.api_key  = api_key
        self.layout   = layout or Layout()
        self.theme    = theme  or Theme()
        self.logo     = logo
        self._pages:      dict[str, Callable] = {}
        self._modals:     dict[str, Callable] = {}
        self._nav:        list                = []
        self._nav_footer: list                = []

    def nav(self, items: list, footer: list = None):
        self._nav        = items
        self._nav_footer = footer or []

    def page(self, path: str, title: str = ""):
        def decorator(fn: Callable):
            self._pages[path] = {"fn": fn, "title": title}
            return fn
        return decorator

    def modal(self, name: str):
        def decorator(fn: Callable):
            self._modals[name] = fn
            return fn
        return decorator

    def run_page(self, path: str) -> list:
        fn = self._pages[path]["fn"]
        if not fn:
            raise ValueError(f"No page registered for path: {path}")
        reset_context()
        import inspect
        sig          = inspect.signature(fn)
        dummy_kwargs = {k: f"{{{k}}}" for k in sig.parameters}
        try:
            fn(**dummy_kwargs)
        except Exception as e:
            _report_error(e, fn)
            raise SystemExit(1)
        return get_context().collect()

    def run_modal(self, name: str) -> list:
        fn = self._modals.get(name)
        if not fn:
            raise ValueError(f"No modal registered: {name}")
        reset_context()
        try:
            fn()
        except Exception as e:
            _report_error(e, fn)
            raise SystemExit(1)
        return get_context().collect()


# ── ERROR REPORTER ──

def _report_error(exc: Exception, fn: Callable):
    import os

    tb = traceback.extract_tb(exc.__traceback__)

    # Find the deepest frame that lives in user code (not burq internals)
    burq_internals = (
        "burq" + os.sep,
        os.path.join("burq", ""),
        "site-packages",
    )

    user_frame = None
    for frame in reversed(tb):
        filepath = frame.filename
        # Skip burq library internals
        is_internal = any(p in filepath for p in burq_internals)
        if not is_internal:
            user_frame = frame
            break

    # Fallback: use the deepest frame
    if user_frame is None and tb:
        user_frame = tb[-1]

    print("\n" + "─" * 56)
    print(f"  ✗  burq compile error in {fn.__name__}()")
    print("─" * 56)

    if user_frame:
        rel_path = _rel(user_frame.filename)
        print(f"  File: {rel_path}, line {user_frame.lineno}")
        print()

        # Show context: 2 lines before, the error line, 2 lines after
        lineno   = user_frame.lineno
        filepath = user_frame.filename
        start    = max(1, lineno - 2)
        end      = lineno + 2

        for i in range(start, end + 1):
            raw = linecache.getline(filepath, i).rstrip()
            if not raw and i > lineno:
                break
            prefix = "  →  " if i == lineno else "     "
            print(f"  {i:>4}  {prefix}{raw}")

        print()

    print(f"  {type(exc).__name__}: {exc}")
    print("─" * 56 + "\n")


def _rel(filepath: str) -> str:
    """Return path relative to cwd if possible."""
    import os
    try:
        return os.path.relpath(filepath)
    except ValueError:
        return filepath