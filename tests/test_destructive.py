from __future__ import annotations

from pathlib import Path

from core.storage import Storage
from plugins.group_admin import moderate


def test_ban_needs_confirm(tmp_path: Path) -> None:
    import asyncio

    st = Storage(str(tmp_path / "t.db"))
    _ = st

    async def run() -> None:
        r = await moderate("ban", 1, 2, [1], confirmed=False, enabled=True)
        assert r["ok"] is False
        assert r["reason"] == "need_confirm"
        r2 = await moderate("ban", 1, 2, [1], confirmed=True, enabled=True)
        assert r2["ok"] is True

    asyncio.run(run())
