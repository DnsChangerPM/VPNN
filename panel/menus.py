from __future__ import annotations

from dataclasses import dataclass, field

from i18n.messages import t
from panel.callback import encode


@dataclass
class MenuItem:
    id: str
    text_key: str
    callback: str
    children: list[str] = field(default_factory=list)
    parent: str | None = None
    destructive: bool = False
    view: str = ""


def menu_tree() -> dict[str, MenuItem]:
    items = [
        MenuItem("home", "home.title", encode("nav", "home"), view="home"),
        MenuItem("autoreply", "btn.autoreply", encode("nav", "ar"), parent="home", view="autoreply"),
        MenuItem("notes", "btn.notes", encode("nav", "notes"), parent="home", view="notes"),
        MenuItem("media", "btn.media", encode("nav", "media"), parent="home", view="media"),
        MenuItem("groups", "btn.groups", encode("nav", "groups"), parent="home", view="groups"),
        MenuItem("backup", "btn.backup", encode("nav", "backup"), parent="home", view="backup"),
        MenuItem("scheduler", "btn.scheduler", encode("nav", "sched"), parent="home", view="scheduler"),
        MenuItem("status", "btn.status", encode("nav", "status"), parent="home", view="status"),
        MenuItem("settings", "btn.settings", encode("nav", "settings"), parent="home", view="settings"),
        MenuItem("shutdown", "btn.shutdown", encode("nav", "shutdown"), parent="home", view="danger", destructive=True),
        MenuItem("ar_toggle", "btn.ar_off", encode("ar", "toggle"), parent="autoreply"),
        MenuItem("ar_add", "btn.add", encode("ar", "add"), parent="autoreply"),
        MenuItem("notes_add", "btn.add", encode("nt", "add"), parent="notes"),
        MenuItem("notes_search", "btn.search", encode("nt", "search"), parent="notes"),
        MenuItem("media_dl", "btn.add", encode("md", "dl"), parent="media"),
        MenuItem("ga_toggle", "btn.ga_off", encode("ga", "toggle"), parent="groups"),
        MenuItem("ga_ban", "btn.delete", encode("ga", "ban"), parent="groups", destructive=True),
        MenuItem("bk_start", "btn.add", encode("bk", "start"), parent="backup"),
        MenuItem("sc_add", "btn.add", encode("sc", "add"), parent="scheduler"),
        MenuItem("st_refresh", "btn.refresh", encode("st", "refresh"), parent="status"),
        MenuItem("st_clear", "btn.clear_jobs", encode("st", "clear"), parent="status", destructive=True),
        MenuItem("set_lang", "btn.lang", encode("set", "lang"), parent="settings"),
        MenuItem("set_dry", "btn.dry_run", encode("set", "dry"), parent="settings"),
        MenuItem("set_plugins", "btn.plugins", encode("set", "plugins"), parent="settings"),
        MenuItem("dn_yes", "btn.confirm_yes", encode("dn", "yes"), parent="shutdown", destructive=True),
        MenuItem("dn_no", "btn.confirm_no", encode("dn", "no"), parent="shutdown"),
        MenuItem("logs", "logs.title", encode("nav", "logs"), parent="status", view="logs"),
    ]
    by_id = {m.id: m for m in items}
    children: dict[str, list[str]] = {}
    for m in items:
        if m.parent:
            children.setdefault(m.parent, []).append(m.id)
    for mid, kids in children.items():
        by_id[mid].children = kids
    return by_id


def home_buttons() -> list[list[tuple[str, str]]]:
    keys = [
        ("btn.autoreply", "nav:ar"),
        ("btn.notes", "nav:notes"),
        ("btn.media", "nav:media"),
        ("btn.groups", "nav:groups"),
        ("btn.backup", "nav:backup"),
        ("btn.scheduler", "nav:sched"),
        ("btn.status", "nav:status"),
        ("btn.settings", "nav:settings"),
        ("btn.shutdown", "nav:shutdown"),
    ]
    rows: list[list[tuple[str, str]]] = []
    row: list[tuple[str, str]] = []
    for k, cb in keys:
        row.append((t(k), cb))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return rows


def back_row(parent: str = "home") -> list[tuple[str, str]]:
    return [(t("btn.back"), f"nav:{parent}")]
