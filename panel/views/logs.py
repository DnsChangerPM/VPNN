from __future__ import annotations

from i18n.messages import t
from panel.keyboards import build_rows
from panel.menus import back_row
from panel.pagination import nav_buttons, slice_page


def render(items: list[str], page: int = 0) -> tuple[str, list[list[dict[str, str]]]]:
    chunk, page, total = slice_page(items, page)
    text = t("logs.title") + "\n" + "\n".join(str(x) for x in chunk)
    rows: list[list[tuple[str, str]]] = []
    nav = nav_buttons("lg", page, total)
    if nav:
        rows.append(nav)
    rows.append(back_row("status"))
    return text, build_rows(rows)
