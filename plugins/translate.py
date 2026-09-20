from __future__ import annotations

from typing import Any

_MAP = {
    "سلام": "hello",
    "hello": "سلام",
    "خداحافظ": "goodbye",
    "goodbye": "خداحافظ",
}


async def translate(text: str) -> dict[str, Any]:
    key = text.strip().lower()
    if key in _MAP:
        return {"ok": True, "text": _MAP[key]}
    # offline fallback: reverse as last resort with clear message
    return {"ok": False, "error": "no_offline_dict", "text": text}
