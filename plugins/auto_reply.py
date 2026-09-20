from __future__ import annotations

from typing import Any

from core.storage import Storage


async def set_enabled(storage: Storage, enabled: bool) -> dict[str, Any]:
    storage.set_setting("plugin.auto_reply", "1" if enabled else "0")
    return {"enabled": enabled}


async def is_enabled(storage: Storage) -> bool:
    return storage.get_setting("plugin.auto_reply", "0") == "1"


async def add_rule(storage: Storage, chat_id: int, text: str, cooldown: int) -> dict[str, Any]:
    storage.execute(
        "INSERT INTO auto_reply(chat_id, text, cooldown) VALUES(?,?,?)",
        (chat_id, text, cooldown),
    )
    return {"ok": True}


def in_quiet_hours(hour: int, start: int, end: int) -> bool:
    if start == end:
        return False
    if start < end:
        return start <= hour < end
    return hour >= start or hour < end
