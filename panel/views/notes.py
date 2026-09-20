from __future__ import annotations

from i18n.messages import t
from panel.keyboards import build_rows
from panel.menus import back_row
from panel.pagination import nav_buttons, slice_page


def render(notes: list[tuple[int, str]], page: int = 0) -> tuple[str, list[list[dict[str, str]]]]:
    chunk, page, total = slice_page(notes, page)
    lines = [t("notes.title")]
    rows: list[list[tuple[str, str]]] = []
    if not notes:
        lines.append(t("notes.empty"))
    for nid, text in chunk:
        preview = text[:20]
        rows.append([(f"#{nid} {preview}", f"nt:open:{nid}")])
    nav = nav_buttons("nt", page, total)
    if nav:
        rows.append(nav)
    rows.append([(t("btn.add"), "nt:add"), (t("btn.search"), "nt:search")])
    rows.append(back_row("home"))
    return "\n".join(lines), build_rows(rows)
