from __future__ import annotations

import pytest

from panel.callback import CallbackTooLongError, encode
from panel.keyboards import KeyboardLimitError, assert_limits, build_rows


def test_limits() -> None:
    assert_limits(100, 8, "ns:action:1")
    rows = [[("a", "n:a:1")] * 8]
    build_rows(rows)


def test_too_many_buttons() -> None:
    rows = [[("x", "n:a:1")] * 8 for _ in range(13)]
    with pytest.raises(KeyboardLimitError):
        build_rows(rows)


def test_callback_encode_too_long() -> None:
    with pytest.raises(CallbackTooLongError):
        encode("ns", "action", "x" * 80)
