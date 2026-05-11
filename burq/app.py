from dataclasses import dataclass
from typing import Callable
from .theme.theme import Theme
from .context import reset_context, get_context


@dataclass
class Layout:
    sidebar: bool = True
    topbar:  bool = True


class App:
    def __init__(
        self,
        title:    str    = "Burq App",
        author:   str    = "",
        api_base: str    = "",
        api_key:  str    = "",
        layout:   Layout = None,
        theme:    Theme  = None,
    ):
        self.title    = title
        self.author   = author
        self.api_base = api_base
        self.api_key  = api_key
        self.layout   = layout or Layout()
        self.theme    = theme  or Theme()

        self._pages:      dict[str, Callable] = {}
        self._modals:     dict[str, Callable] = {}
        self._nav:        list                = []
        self._nav_footer: list                = []

    def nav(self, items: list, footer: list = None):
        self._nav        = items
        self._nav_footer = footer or []

    def page(self, path: str):
        def decorator(fn: Callable):
            self._pages[path] = fn
            return fn
        return decorator

    def modal(self, name: str):
        def decorator(fn: Callable):
            self._modals[name] = fn
            return fn
        return decorator

    def run_page(self, path: str) -> list:
        fn = self._pages.get(path)
        if not fn:
            raise ValueError(f"No page registered for path: {path}")
        reset_context()
        fn()
        return get_context().collect()

    def run_modal(self, name: str) -> list:
        fn = self._modals.get(name)
        if not fn:
            raise ValueError(f"No modal registered: {name}")
        reset_context()
        fn()
        return get_context().collect()