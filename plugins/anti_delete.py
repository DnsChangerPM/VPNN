from __future__ import annotations

from typing import Any

from core.storage import Storage


async def record(storage: Storage, sender: str, body: str, ts: float, kind: str) -> dict[str, Any]:
    storage.log_deleted(sender, body, ts, kind)
    return {"ok": True}


async def list_log(storage: Storage) -> dict[str, Any]:
    rows = storage.list_deleted()
    return {"items": [f"{r['kind']} {r['sender']}: {r['body']}" for r in rows]}
