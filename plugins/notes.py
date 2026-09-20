from __future__ import annotations

import time
from typing import Any

from core.storage import Storage


async def add_note(storage: Storage, text: str) -> dict[str, Any]:
    nid = storage.add_note(text, time.time())
    return {"id": nid}


async def list_notes(storage: Storage) -> dict[str, Any]:
    rows = storage.list_notes()
    return {"notes": [(int(r["id"]), str(r["text"])) for r in rows]}


async def delete_note(storage: Storage, note_id: int) -> dict[str, Any]:
    storage.delete_note(note_id)
    return {"deleted": note_id}


async def search_notes(storage: Storage, query: str) -> dict[str, Any]:
    rows = storage.search_notes(query)
    return {"notes": [(int(r["id"]), str(r["text"])) for r in rows]}
