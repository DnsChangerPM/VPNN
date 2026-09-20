from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from panel.menus import menu_tree
from panel.router import Router, register_defaults


def main() -> None:
    tree = menu_tree()
    router = Router()
    register_defaults(router)
    print("MENU TREE")
    for mid, item in tree.items():
        kids = ",".join(item.children) if item.children else "-"
        ok = "OK" if router.has_handler(item.callback) else "DEAD"
        print(f"{mid:16} parent={item.parent or '-':10} cb={item.callback:20} kids={kids} [{ok}]")
    print("total", len(tree))


if __name__ == "__main__":
    main()
