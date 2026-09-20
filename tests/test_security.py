from __future__ import annotations

from core.security import Security
from core.storage import Storage


def test_non_owner_callback_rejected(tmp_path: object) -> None:
    from pathlib import Path

    st = Storage(str(Path(str(tmp_path)) / "t.db"))
    sec = Security(st, owner_id=42)
    assert sec.gate_callback(42) is True
    assert sec.gate_callback(99) is False


def test_pairing_one_time(tmp_path: object) -> None:
    from pathlib import Path

    st = Storage(str(Path(str(tmp_path)) / "t.db"))
    sec = Security(st, owner_id=0)
    code = sec.generate_code()
    assert sec.try_pair(code, 7) is True
    assert sec.owner_id() == 7
    assert sec.try_pair(code, 8) is False
    assert sec.owner_id() == 7
