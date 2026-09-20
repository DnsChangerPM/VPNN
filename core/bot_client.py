from __future__ import annotations

import logging
from typing import Any

from config import Settings
from core.bus import JobBus
from core.rate_limiter import RateLimiter
from core.security import Security
from core.storage import Storage
from i18n.messages import t
from panel.keyboards import telethon_buttons
from panel.router import Router, register_defaults
from panel.views import backup, danger, groups, home, media, notes, scheduler, status
from panel.views import settings as setview
from panel.wizard import Wizard

log = logging.getLogger("bot_client")


class BotRuntime:
    def __init__(
        self,
        settings: Settings,
        storage: Storage,
        bus: JobBus,
        security: Security,
    ) -> None:
        self.settings = settings
        self.storage = storage
        self.bus = bus
        self.security = security
        self.limiter = RateLimiter(settings.rate_limit_per_minute, settings.rate_limit_min_delay)
        self.wizard = Wizard()
        self.router = Router()
        register_defaults(self.router)
        self.client: Any = None
        self.connected = False
        self.last_error = ""
        self.pending_confirm: dict[int, str] = {}

    async def start(self) -> None:
        if self.settings.dry_run or not self.settings.bot_token:
            log.info("bot client dry-run or missing token — skip connect")
            self.connected = False
            return
        from telethon import TelegramClient, events

        self.client = TelegramClient(
            self.settings.bot_session_path,
            self.settings.api_id,
            self.settings.api_hash,
        )
        try:
            await self.client.start(bot_token=self.settings.bot_token)
            self.connected = True
            self.client.add_event_handler(self._on_start, events.NewMessage(pattern=r"^/(start|menu|help|cancel)"))
            self.client.add_event_handler(self._on_callback, events.CallbackQuery)
            self.client.add_event_handler(self._on_text, events.NewMessage)
        except Exception as exc:
            self.last_error = str(exc)
            log.exception("bot client failed")
            self.connected = False

    async def stop(self) -> None:
        if self.client:
            try:
                await self.client.disconnect()
            except Exception:
                log.exception("bot disconnect")
        self.connected = False

    async def _on_start(self, event: Any) -> None:
        uid = int(event.sender_id)
        text = event.raw_text or ""
        if text.startswith("/help"):
            await event.reply(t("help.text"))
            return
        if text.startswith("/cancel"):
            self.wizard.cancel(uid)
            await event.reply(t("wizard.cancelled"))
            return
        if not self.security.owner_id():
            code = self.security.generate_code()
            await event.reply(t("pairing.code", code=code))
            return
        if not self.security.gate_callback(uid):
            return
        body, rows = home.render()
        await event.reply(body, buttons=telethon_buttons(rows))

    async def _on_callback(self, event: Any) -> None:
        uid = int(event.sender_id)
        if not self.security.gate_callback(uid):
            return
        data = event.data.decode() if isinstance(event.data, bytes) else str(event.data)
        try:
            await event.answer()
        except Exception:
            log.exception("answer callback")
        try:
            await self.router.dispatch(data)
        except Exception:
            log.exception("router")
            await event.edit(t("error.generic"))
            return
        ns = data.split(":", 1)[0]
        action = data.split(":")[1] if ":" in data else ""
        if data == "nav:shutdown" or (ns == "ga" and action == "ban") or data == "st:clear":
            self.pending_confirm[uid] = data
            body, rows = danger.render()
            await event.edit(body, buttons=telethon_buttons(rows))
            return
        if data == "dn:no":
            self.pending_confirm.pop(uid, None)
            body, rows = home.render()
            await event.edit(body, buttons=telethon_buttons(rows))
            return
        if data == "dn:yes":
            pending = self.pending_confirm.pop(uid, "")
            if not pending:
                await event.edit(t("confirm.title"))
                return
            if pending == "nav:shutdown":
                self.bus.enqueue("shutdown", {})
            body, rows = home.render()
            await event.edit(body, buttons=telethon_buttons(rows))
            return
        body, rows = self._page_for(data)
        await event.edit(body, buttons=telethon_buttons(rows))

    def _page_for(self, data: str) -> tuple[str, list[list[dict[str, str]]]]:
        if data.startswith("nav:ar") or data.startswith("ar:"):
            enabled = self.storage.get_setting("plugin.auto_reply", "0") == "1"
            return autoreply_render(enabled)
        if data.startswith("nav:notes") or data.startswith("nt:"):
            rows = self.storage.list_notes()
            return notes.render([(int(r["id"]), str(r["text"])) for r in rows])
        if data.startswith("nav:media"):
            return media.render()
        if data.startswith("nav:groups") or data.startswith("ga:"):
            en = self.storage.get_setting("plugin.group_admin", "0") == "1"
            return groups.render(en)
        if data.startswith("nav:backup") or data.startswith("bk:"):
            return backup.render()
        if data.startswith("nav:sched"):
            return scheduler.render()
        if data.startswith("nav:status") or data.startswith("st:"):
            return status.render("-", "-", str(self.bus.job_counts()), "-", "-", "-")
        if data.startswith("nav:settings") or data.startswith("set:"):
            return setview.render()
        return home.render()

    async def _on_text(self, event: Any) -> None:
        uid = int(event.sender_id)
        text = (event.raw_text or "").strip()
        if text.startswith("/"):
            return
        if self.security.try_pair(text, uid):
            await event.reply(t("pairing.done"))
            return
        if not self.security.gate_callback(uid):
            return
        st = self.wizard.get(uid)
        if not st:
            return
        st.data["text"] = text
        await event.reply(t("wizard.saved"))


def autoreply_render(enabled: bool) -> tuple[str, list[list[dict[str, str]]]]:
    from panel.views.autoreply import render

    return render(enabled)


async def send_with_inline_buttons(bot_username: str, query: str) -> str:
    """Only allowed way to show buttons in a real chat: inline mode of helper bot."""
    return f"via @{bot_username} query={query}"
