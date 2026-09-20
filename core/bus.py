from __future__ import annotations

import asyncio
import json
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from core.storage import Storage

JobHandler = Callable[[str, dict[str, Any]], Awaitable[dict[str, Any]]]


@dataclass
class Job:
    id: int
    kind: str
    payload: dict[str, Any]
    status: str
    result: dict[str, Any] | None


class JobBus:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage
        self._queue: asyncio.Queue[int] = asyncio.Queue()
        self._handlers: dict[str, JobHandler] = {}
        self._listeners: list[Callable[[Job], Awaitable[None]]] = []
        self._running = False

    def register(self, kind: str, handler: JobHandler) -> None:
        self._handlers[kind] = handler

    def on_update(self, fn: Callable[[Job], Awaitable[None]]) -> None:
        self._listeners.append(fn)

    def enqueue(self, kind: str, payload: dict[str, Any]) -> int:
        now = time.time()
        cur = self.storage.execute(
            "INSERT INTO jobs(kind,payload,status,created_at,updated_at) VALUES(?,?,?,?,?)",
            (kind, json.dumps(payload), "pending", now, now),
        )
        job_id = int(cur.lastrowid or 0)
        self._queue.put_nowait(job_id)
        return job_id

    def get_job(self, job_id: int) -> Job | None:
        row = self.storage.fetchone("SELECT * FROM jobs WHERE id=?", (job_id,))
        if not row:
            return None
        payload = json.loads(str(row["payload"]))
        result = json.loads(str(row["result"])) if row["result"] else None
        return Job(
            id=int(row["id"]),
            kind=str(row["kind"]),
            payload=payload if isinstance(payload, dict) else {},
            status=str(row["status"]),
            result=result if isinstance(result, dict) else None,
        )

    def job_counts(self) -> dict[str, int]:
        rows = self.storage.fetchall("SELECT status, COUNT(*) c FROM jobs GROUP BY status")
        return {str(r["status"]): int(r["c"]) for r in rows}

    def clear_pending(self) -> int:
        cur = self.storage.execute("DELETE FROM jobs WHERE status IN ('pending','failed')")
        return int(cur.rowcount)

    def recover_pending(self) -> None:
        rows = self.storage.fetchall("SELECT id FROM jobs WHERE status IN ('pending','running')")
        for r in rows:
            self._queue.put_nowait(int(r["id"]))

    async def _notify(self, job: Job) -> None:
        for fn in self._listeners:
            try:
                await fn(job)
            except Exception:
                continue

    async def worker(self) -> None:
        self._running = True
        while self._running:
            try:
                job_id = await asyncio.wait_for(self._queue.get(), timeout=0.5)
            except TimeoutError:
                continue
            job = self.get_job(job_id)
            if not job:
                continue
            now = time.time()
            self.storage.execute(
                "UPDATE jobs SET status=?, updated_at=? WHERE id=?",
                ("running", now, job_id),
            )
            job.status = "running"
            await self._notify(job)
            handler = self._handlers.get(job.kind)
            try:
                if handler is None:
                    raise RuntimeError(f"no handler for {job.kind}")
                result = await handler(job.kind, job.payload)
                status = "done"
            except Exception as exc:
                result = {"error": str(exc)}
                status = "failed"
            self.storage.execute(
                "UPDATE jobs SET status=?, result=?, updated_at=? WHERE id=?",
                (status, json.dumps(result), time.time(), job_id),
            )
            job.status = status
            job.result = result
            await self._notify(job)

    def stop(self) -> None:
        self._running = False
