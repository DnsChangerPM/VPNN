from __future__ import annotations

from typing import Any

from core.storage import Storage


async def set_enabled(storage: Storage, enabled: bool) -> dict[str, Any]:
    storage.set_setting("plugin.auto_forward", "1" if enabled else "0")
    return {"enabled": enabled}


async def should_forward(text: str, keyword: str) -> bool:
    if not keyword:
        return True
    return keyword.lower() in text.lower()
