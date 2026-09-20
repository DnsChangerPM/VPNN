from __future__ import annotations

from typing import Any

from panel.callback import encode

MAX_BUTTONS = 100
MAX_PER_ROW = 8


class KeyboardLimitError(ValueError):
    pass


def build_rows(rows: list[list[tuple[str, str]]]) -> list[list[dict[str, str]]]:
    total = sum(len(r) for r in rows)
    if total > MAX_BUTTONS:
        raise KeyboardLimitError(f"{total} buttons > {MAX_BUTTONS}")
    out: list[list[dict[str, str]]] = []
    for row in rows:
        if len(row) > MAX_PER_ROW:
            raise KeyboardLimitError(f"row has {len(row)} > {MAX_PER_ROW}")
        built: list[dict[str, str]] = []
        for text, data in row:
            if ":" in data:
                parts = data.split(":", 2)
                encode(parts[0], parts[1] if len(parts) > 1 else "x", parts[2] if len(parts) > 2 else "")
            if len(data.encode("utf-8")) > 64:
                raise KeyboardLimitError("callback_data too long")
            built.append({"text": text, "data": data})
        out.append(built)
    return out


def telethon_buttons(rows: list[list[dict[str, str]]]) -> Any:
    from telethon import Button

    return [[Button.inline(b["text"], b["data"].encode()) for b in row] for row in rows]


def assert_limits(button_count: int, per_row: int, cb: str) -> None:
    assert button_count <= MAX_BUTTONS
    assert per_row <= MAX_PER_ROW
    assert len(cb.encode("utf-8")) <= 64
