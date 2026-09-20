from __future__ import annotations

from i18n.messages import t
from panel.keyboards import build_rows
from panel.menus import back_row


def render() -> tuple[str, list[list[dict[str, str]]]]:
    rows = [
        [(t("btn.lang"), "set:lang")],
        [(t("btn.dry_run"), "set:dry")],
        [(t("btn.plugins"), "set:plugins")],
        [(t("btn.quiet"), "set:quiet")],
        back_row("home"),
    ]
    return t("settings.title"), build_rows(rows)
