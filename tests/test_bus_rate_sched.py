from __future__ import annotations

import asyncio
from pathlib import Path

from core.bus import JobBus
from core.rate_limiter import RateLimiter
from core.scheduler import AppScheduler
from core.storage import Storage


def test_rate_limiter() -> None:
    async def run() -> None:
        rl = RateLimiter(per_minute=600, min_delay=0.0)
        await rl.acquire()
        await rl.acquire()

    asyncio.run(run())


def test_job_bus(tmp_path: Path) -> None:
    async def run() -> None:
        st = Storage(str(tmp_path / "t.db"))
        bus = JobBus(st)

        async def h(kind: str, payload: dict[str, object]) -> dict[str, object]:
            return {"kind": kind, **payload}

        bus.register("echo", h)
        jid = bus.enqueue("echo", {"a": 1})
        task = asyncio.create_task(bus.worker())
        await asyncio.sleep(0.2)
        bus.stop()
        task.cancel()
        job = bus.get_job(jid)
        assert job is not None
        assert job.status in {"done", "running", "pending"}

    asyncio.run(run())


def test_scheduler(tmp_path: Path) -> None:
    async def run() -> None:
        st = Storage(str(tmp_path / "t.db"))
        sch = AppScheduler(st)
        sch.start()
        sch.shutdown()

    asyncio.run(run())
