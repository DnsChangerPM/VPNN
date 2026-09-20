from __future__ import annotations

from i18n import en, fa
from i18n.messages import all_keys


def test_keys_match() -> None:
    keys = all_keys()
    assert set(fa.STRINGS) == keys
    assert set(en.STRINGS) == keys
    for k in keys:
        assert fa.STRINGS[k] is not None
        assert en.STRINGS[k] is not None
