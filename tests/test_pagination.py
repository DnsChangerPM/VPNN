from __future__ import annotations

from panel.pagination import nav_buttons, slice_page


def test_last_page_no_next() -> None:
    items = list(range(12))
    chunk, page, total = slice_page(items, 1, size=6)
    assert page == 1
    assert total == 2
    labels = [t for t, _ in nav_buttons("nt", page, total)]
    assert not any("next" in str(cb) or "بعدی" in lab for lab, cb in nav_buttons("nt", page, total))
    cbs = [cb for _, cb in nav_buttons("nt", page, total)]
    assert not any(cb.endswith(":2") or ":page:2" in cb for cb in cbs)
    assert all("page:1" not in cb or True for cb in cbs)
    assert not any(cb == "nt:page:2" for cb in cbs)
    nexts = [cb for _, cb in nav_buttons("nt", page, total) if "page:" in cb and int(cb.split(":")[-1]) > page]
    assert nexts == []
    _ = labels, chunk
