from dataclasses import dataclass, field
from typing import Callable, Optional
from .theme.theme import Theme
from .context import reset_context, get_context


@dataclass
class Layout:
    sidebar: bool = True
    topbar:  bool = True


@dataclass
class NavItem:
    label: str
    icon:  str  = ""
    href:  str  = "#"


class App:
    def __init__(
        self,
        title:    str    = "Burq App",
        api_base: str    = "",
        api_key:  str    = "",
        layout:   Layout = None,
        theme:    Theme  = None,
    ):
        self.title    = title
        self.api_base = api_base
        self.api_key  = api_key
        self.layout   = layout or Layout()
        self.theme    = theme  or Theme()

        self._pages:   dict[str, Callable] = {}
        self._modals:  dict[str, Callable] = {}
        self._nav:     list[NavItem]       = []
        self._nav_footer: list[NavItem]    = []

    def nav(
        self,
        items:  list[NavItem],
        footer: list[NavItem] = None
    ):
        self._nav        = items
        self._nav_footer = footer or []

    def page(self, path: str):
        """Decorator to register a page."""
        def decorator(fn: Callable):
            self._pages[path] = fn
            return fn
        return decorator

    def modal(self, name: str):
        """Decorator to register a modal."""
        def decorator(fn: Callable):
            self._modals[name] = fn
            return fn
        return decorator

    def run_page(self, path: str) -> list:
        """Execute a page function and return its component tree."""
        fn = self._pages.get(path)
        if not fn:
            raise ValueError(f"No page registered for path: {path}")
        reset_context()
        fn()
        return get_context().collect()

    def run_modal(self, name: str) -> list:
        """Execute a modal function and return its component tree."""
        fn = self._modals.get(name)
        if not fn:
            raise ValueError(f"No modal registered: {name}")
        reset_context()
        fn()
        return get_context().collect()