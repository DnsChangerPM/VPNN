from __future__ import annotations

import asyncio
import random
import time
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

T = TypeVar("T")


class RateLimiter:
    def __init__(self, per_minute: float, min_delay: float) -> None:
        self.capacity = max(per_minute, 1.0)
        self.tokens = self.capacity
        self.rate = per_minute / 60.0
        self.min_delay = min_delay
        self._last = 0.0
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self._last if self._last else 0.0
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            if self.tokens < 1.0:
                wait = (1.0 - self.tokens) / self.rate
                await asyncio.sleep(wait)
                self.tokens = 1.0
            since = now - self._last if self._last else self.min_delay
            extra = self.min_delay - since
            if extra > 0:
                await asyncio.sleep(extra + random.uniform(0.05, 0.25))
            else:
                await asyncio.sleep(random.uniform(0.02, 0.12))
            self.tokens -= 1.0
            self._last = time.monotonic()


async def with_flood_wait(
    fn: Callable[..., Awaitable[T]],
    *args: Any,
    retries: int = 3,
    **kwargs: Any,
) -> T:
    from telethon.errors import FloodWaitError

    delay = 1.0
    last: Exception | None = None
    for _attempt in range(retries):
        try:
            return await fn(*args, **kwargs)
        except FloodWaitError as exc:
            last = exc
            await asyncio.sleep(float(exc.seconds) + delay)
            delay *= 2
    if last:
        raise last
    raise RuntimeError("with_flood_wait failed")
