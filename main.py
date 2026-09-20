from __future__ import annotations

import argparse
import asyncio
import logging
import signal
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import Settings, load_settings
from core.bot_client import BotRuntime
from core.bus import JobBus
from core.scheduler import AppScheduler
from core.security import Security
from core.storage import Storage
from core.user_client import UserRuntime
from i18n.messages import set_lang
from plugins import discover

log = logging.getLogger("main")


def setup_logging(settings: Settings) -> None:
    Path(settings.log_dir).mkdir(parents=True, exist_ok=True)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    root = logging.getLogger()
    root.setLevel(settings.log_level.upper())
    fh = RotatingFileHandler(
        Path(settings.log_dir) / "selfbot.log",
        maxBytes=settings.max_log_size_mb * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    root.handlers.clear()
    root.addHandler(fh)
    root.addHandler(sh)


def mask(s: str) -> str:
    if len(s) <= 4:
        return "****"
    return s[:2] + "****" + s[-2:]


class App:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.storage = Storage(settings.db_path)
        self.bus = JobBus(self.storage)
        self.security = Security(self.storage, settings.owner_id)
        self.user = UserRuntime(settings, self.storage, self.bus)
        self.bot = BotRuntime(settings, self.storage, self.bus, self.security)
        self.scheduler = AppScheduler(self.storage)
        self._stop = asyncio.Event()

    async def start(self) -> None:
        set_lang(self.settings.lang)
        self.bus.register("user", self.user.handle_job)
        self.bus.register("shutdown", self._shutdown_job)
        self.bus.recover_pending()
        asyncio.create_task(self._safe(self.bus.worker(), "bus"))
        asyncio.create_task(self._safe(self.user.start(), "user"))
        asyncio.create_task(self._safe(self.bot.start(), "bot"))
        self.scheduler.start()
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, self.request_stop)
            except NotImplementedError:
                pass

    async def _shutdown_job(self, _kind: str, _payload: dict[str, object]) -> dict[str, object]:
        self.request_stop()
        return {"ok": True}

    def request_stop(self) -> None:
        self._stop.set()

    async def wait(self) -> None:
        await self._stop.wait()

    async def stop(self) -> None:
        self.bus.stop()
        self.scheduler.shutdown()
        await self.user.stop()
        await self.bot.stop()
        self.storage.close()

    async def _safe(self, coro: object, name: str) -> None:
        try:
            await coro  # type: ignore[misc]
        except Exception:
            log.exception("task %s crashed", name)


def self_check(settings: Settings) -> int:
    issues = settings.validate_self_check()
    plugins = discover()
    from panel.menus import menu_tree
    from panel.router import Router, register_defaults

    tree = menu_tree()
    router = Router()
    register_defaults(router)
    dead = []
    for item in tree.values():
        if not router.has_handler(item.callback):
            dead.append(item.callback)
    print("self-check plugins:", sorted(plugins.keys()))
    print("self-check menus:", len(tree))
    print("self-check dead buttons:", dead)
    print("self-check issues:", issues)
    print("self-check dry_run:", settings.dry_run)
    print("self-check lang:", settings.lang)
    return 1 if issues or dead else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    settings = load_settings()
    setup_logging(settings)
    log.info("boot dry_run=%s lang=%s token=%s", settings.dry_run, settings.lang, mask(settings.bot_token))
    if args.self_check:
        return self_check(settings)

    async def runner() -> None:
        app = App(settings)
        await app.start()
        await app.wait()
        await app.stop()

    asyncio.run(runner())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
