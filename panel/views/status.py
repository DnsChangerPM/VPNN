from __future__ import annotations

from i18n.messages import t
from panel.keyboards import build_rows
from panel.menus import back_row


def render(uptime: str, ram: str, jobs: str, user: str, bot: str, err: str) -> tuple[str, list[list[dict[str, str]]]]:
    body = t("status.body", uptime=uptime, ram=ram, jobs=jobs, user=user, bot=bot, err=err)
    rows = [
        [(t("btn.refresh"), "st:refresh")],
        [(t("btn.clear_jobs"), "st:clear")],
        [(t("logs.title"), "nav:logs")],
        back_row("home"),
    ]
    return f"{t('status.title')}\n{body}", build_rows(rows)
