from __future__ import annotations

from i18n.messages import t
from panel.keyboards import build_rows


def render() -> tuple[str, list[list[dict[str, str]]]]:
    rows = [
        [(t("btn.confirm_yes"), "dn:yes"), (t("btn.confirm_no"), "dn:no")],
    ]
    return f"{t('confirm.title')}\n{t('confirm.body')}", build_rows(rows)
