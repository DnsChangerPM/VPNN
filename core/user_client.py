from __future__ import annotations

import logging
from typing import Any

from config import Settings
from core.bus import JobBus
from core.rate_limiter import RateLimiter
from core.storage import Storage

log = logging.getLogger("user_client")


class UserRuntime:
    def __init__(self, settings: Settings, storage: Storage, bus: JobBus) -> None:
        self.settings = settings
        self.storage = storage
        self.bus = bus
        self.limiter = RateLimiter(settings.rate_limit_per_minute, settings.rate_limit_min_delay)
        self.client: Any = None
        self.connected = False
        self.last_error = ""

    async def start(self) -> None:
        if self.settings.dry_run or not self.settings.api_id:
            log.info("user client dry-run or missing api — skip connect")
            self.connected = False
            return
        from telethon import TelegramClient

        self.client = TelegramClient(
            self.settings.session_path,
            self.settings.api_id,
            self.settings.api_hash,
        )
        try:
            await self.client.start()
            self.connected = True
        except Exception as exc:
            self.last_error = str(exc)
            log.exception("user client failed")
            self.connected = False

    async def stop(self) -> None:
        if self.client:
            try:
                await self.client.disconnect()
            except Exception:
                log.exception("user disconnect")
        self.connected = False

    async def handle_job(self, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
        if self.settings.dry_run:
            log.info("DRY_RUN skip write kind=%s", kind)
            return {"dry_run": True, "kind": kind}
        await self.limiter.acquire()
        return {"ok": True, "kind": kind, "payload": payload}
