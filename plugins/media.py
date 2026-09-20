from __future__ import annotations

import zipfile
from pathlib import Path
from typing import Any


async def zip_files(paths: list[str], dest: str) -> dict[str, Any]:
    Path(dest).parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w") as zf:
        for p in paths:
            path = Path(p)
            if path.is_file():
                zf.write(path, path.name)
    return {"zip": dest}


async def download_progress(current: int, total: int) -> dict[str, Any]:
    pct = int(current * 100 / total) if total else 0
    return {"pct": pct}
