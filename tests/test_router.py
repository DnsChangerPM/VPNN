from __future__ import annotations

from panel.menus import menu_tree
from panel.router import Router, register_defaults


def test_no_dead_buttons() -> None:
    router = Router()
    register_defaults(router)
    dead = [m.callback for m in menu_tree().values() if not router.has_handler(m.callback)]
    assert dead == []
