from __future__ import annotations

from i18n.messages import t
from panel.keyboards import build_rows
from panel.menus import back_row


def render(enabled: bool) -> tuple[str, list[list[dict[str, str]]]]:
    toggle = t("btn.ar_on" if enabled else "btn.ar_off")
    rows = [
        [(toggle, "ar:toggle")],
        [(t("btn.add"), "ar:add")],
        back_row("home"),
    ]
    return f"{t('ar.title')}\n{t('ar.body')}", build_rows(rows)
