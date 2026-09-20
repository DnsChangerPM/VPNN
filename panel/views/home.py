from __future__ import annotations

from i18n.messages import t
from panel.keyboards import build_rows
from panel.menus import home_buttons


def render() -> tuple[str, list[list[dict[str, str]]]]:
    text = f"{t('home.title')}\n{t('home.body')}"
    return text, build_rows(home_buttons())
