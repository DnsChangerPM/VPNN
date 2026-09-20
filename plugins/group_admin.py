from __future__ import annotations

from typing import Any

from core.storage import Storage

ALLOWED = {"ban", "unban", "mute", "warn"}


async def is_enabled(storage: Storage) -> bool:
    return storage.get_setting("plugin.group_admin", "0") == "1"


async def set_enabled(storage: Storage, enabled: bool) -> dict[str, Any]:
    storage.set_setting("plugin.group_admin", "1" if enabled else "0")
    return {"enabled": enabled}


async def moderate(
    action: str,
    chat_id: int,
    user_id: int,
    admin_chats: list[int],
    confirmed: bool,
    enabled: bool,
) -> dict[str, Any]:
    if not enabled:
        return {"ok": False, "reason": "disabled"}
    if not confirmed:
        return {"ok": False, "reason": "need_confirm"}
    if action not in ALLOWED:
        return {"ok": False, "reason": "unknown"}
    if chat_id not in admin_chats:
        return {"ok": False, "reason": "not_admin_chat"}
    return {"ok": True, "action": action, "chat_id": chat_id, "user_id": user_id}
