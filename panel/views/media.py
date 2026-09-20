from __future__ import annotations

from i18n.messages import t
from panel.keyboards import build_rows
from panel.menus import back_row


def render() -> tuple[str, list[list[dict[str, str]]]]:
    rows = [[(t("btn.add"), "md:dl")], back_row("home")]
    return f"{t('media.title')}\n{t('media.body')}", build_rows(rows)
