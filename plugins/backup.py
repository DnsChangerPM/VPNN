from __future__ import annotations

import json
from pathlib import Path
from typing import Any


async def export_messages(
    messages: list[dict[str, Any]], dest_json: str, dest_html: str
) -> dict[str, Any]:
    Path(dest_json).parent.mkdir(parents=True, exist_ok=True)
    Path(dest_json).write_text(json.dumps(messages, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["<html><body><ul>"]
    for m in messages:
        lines.append(f"<li>{m.get('date','')} {m.get('sender','')}: {m.get('text','')}</li>")
    lines.append("</ul></body></html>")
    Path(dest_html).write_text("\n".join(lines), encoding="utf-8")
    return {"n": len(messages), "json": dest_json, "html": dest_html}


def progress(done: int, total: int) -> int:
    if total <= 0:
        return 100
    return min(100, int(done * 100 / total))
