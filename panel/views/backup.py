from __future__ import annotations

from i18n.messages import t
from panel.keyboards import build_rows
from panel.menus import back_row


def render(progress: str | None = None) -> tuple[str, list[list[dict[str, str]]]]:
    body = progress or t("backup.title")
    rows = [[(t("btn.add"), "bk:start"), (t("btn.refresh"), "bk:refresh")], back_row("home")]
    return body, build_rows(rows)
