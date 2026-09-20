from __future__ import annotations

from i18n.messages import t
from panel.keyboards import build_rows
from panel.menus import back_row


def render(enabled: bool) -> tuple[str, list[list[dict[str, str]]]]:
    toggle = t("btn.ga_on" if enabled else "btn.ga_off")
    rows = [
        [(toggle, "ga:toggle")],
        [(t("btn.delete"), "ga:ban")],
        back_row("home"),
    ]
    body = t("groups.title") if enabled else t("groups.off")
    return f"{t('groups.title')}\n{body}", build_rows(rows)
