from __future__ import annotations

import logging
import time
from collections.abc import Callable
from typing import Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.storage import Storage

log = logging.getLogger("scheduler")


class AppScheduler:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage
        self._sched = AsyncIOScheduler()

    def start(self) -> None:
        if not self._sched.running:
            self._sched.start()
            self._restore()

    def shutdown(self) -> None:
        if self._sched.running:
            self._sched.shutdown(wait=False)

    def add_reminder(self, when_ts: float, text: str, callback: Callable[..., Any]) -> int:
        cur = self.storage.execute(
            "INSERT INTO reminders(when_ts, text, done) VALUES(?,?,0)",
            (when_ts, text),
        )
        rid = int(cur.lastrowid or 0)
        self._sched.add_job(
            callback,
            "date",
            run_date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(when_ts)),
            args=[rid, text],
            id=f"rem-{rid}",
            replace_existing=True,
        )
        return rid

    def list_reminders(self) -> list[Any]:
        return self.storage.fetchall("SELECT * FROM reminders WHERE done=0 ORDER BY when_ts")

    def mark_done(self, rid: int) -> None:
        self.storage.execute("UPDATE reminders SET done=1 WHERE id=?", (rid,))

    def _restore(self) -> None:
        now = time.time()
        for row in self.list_reminders():
            if float(row["when_ts"]) < now:
                continue
            log.info("restored reminder %s", row["id"])
