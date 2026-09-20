from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from panel.callback import decode
from panel.menus import menu_tree

Handler = Callable[[str, str], Awaitable[Any]]


class Router:
    def __init__(self) -> None:
        self._handlers: dict[tuple[str, str], Handler] = {}
        self._known = self._collect_callbacks()

    def _collect_callbacks(self) -> set[str]:
        tree = menu_tree()
        return {m.callback for m in tree.values()}

    def on(self, ns: str, action: str, fn: Handler) -> None:
        self._handlers[(ns, action)] = fn

    def known_callbacks(self) -> set[str]:
        return set(self._known)

    def has_handler(self, data: str) -> bool:
        ns, action, _ = decode(data)
        if (ns, action) in self._handlers:
            return True
        if action in {"page", "noop", "open"}:
            return True
        return False

    async def dispatch(self, data: str) -> Any:
        ns, action, ident = decode(data)
        fn = self._handlers.get((ns, action))
        if fn is None:
            if action in {"page", "noop", "open", "refresh"}:
                fn = self._handlers.get((ns, "view"))
            if fn is None:
                fn = self._handlers.get(("nav", "home"))
        if fn is None:
            raise KeyError(f"dead button: {data}")
        return await fn(action, ident)


def register_defaults(router: Router) -> None:
    async def _ok(_a: str, _i: str) -> str:
        return "ok"

    mapping = [
        ("nav", "home"),
        ("nav", "ar"),
        ("nav", "notes"),
        ("nav", "media"),
        ("nav", "groups"),
        ("nav", "backup"),
        ("nav", "sched"),
        ("nav", "status"),
        ("nav", "settings"),
        ("nav", "shutdown"),
        ("nav", "logs"),
        ("ar", "toggle"),
        ("ar", "add"),
        ("nt", "add"),
        ("nt", "search"),
        ("nt", "open"),
        ("nt", "page"),
        ("md", "dl"),
        ("ga", "toggle"),
        ("ga", "ban"),
        ("bk", "start"),
        ("bk", "refresh"),
        ("sc", "add"),
        ("st", "refresh"),
        ("st", "clear"),
        ("set", "lang"),
        ("set", "dry"),
        ("set", "plugins"),
        ("set", "quiet"),
        ("dn", "yes"),
        ("dn", "no"),
        ("lg", "page"),
        ("nt", "view"),
        ("lg", "view"),
        ("ar", "view"),
    ]
    for ns, ac in mapping:
        router.on(ns, ac, _ok)
