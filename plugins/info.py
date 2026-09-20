from __future__ import annotations

import os
import time
from typing import Any

_START = time.time()


async def status() -> dict[str, Any]:
    rss = 0
    try:
        with open("/proc/self/status", encoding="utf-8") as fh:
            for line in fh:
                if line.startswith("VmRSS:"):
                    rss = int(line.split()[1])
                    break
    except OSError:
        rss = 0
    return {
        "uptime": int(time.time() - _START),
        "ram_kb": rss,
        "pid": os.getpid(),
    }
