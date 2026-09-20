from __future__ import annotations

from typing import TypeVar

from i18n.messages import t

PAGE_SIZE = 6
T = TypeVar("T")


def slice_page(items: list[T], page: int, size: int = PAGE_SIZE) -> tuple[list[T], int, int]:
    total_pages = max(1, (len(items) + size - 1) // size)
    page = max(0, min(page, total_pages - 1))
    start = page * size
    return items[start : start + size], page, total_pages


def nav_buttons(ns: str, page: int, total_pages: int) -> list[tuple[str, str]]:
    row: list[tuple[str, str]] = []
    if page > 0:
        row.append((t("btn.prev"), f"{ns}:page:{page - 1}"))
    row.append((t("page", n=page + 1, total=total_pages), f"{ns}:noop:0"))
    if page < total_pages - 1:
        row.append((t("btn.next"), f"{ns}:page:{page + 1}"))
    return row
