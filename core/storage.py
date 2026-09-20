from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path
from typing import Any


class Storage:
    def __init__(self, path: str) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init()

    def _init(self) -> None:
        with self._lock:
            c = self._conn
            c.executescript(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kind TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    result TEXT,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    created_at REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS deleted_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT,
                    body TEXT,
                    ts REAL NOT NULL,
                    kind TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS pairing (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    code TEXT,
                    owner_id INTEGER,
                    used INTEGER NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS callbacks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    payload TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    when_ts REAL NOT NULL,
                    text TEXT NOT NULL,
                    done INTEGER NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS auto_reply (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    cooldown INTEGER NOT NULL DEFAULT 60
                );
                """
            )
            c.commit()

    def execute(self, sql: str, params: tuple[Any, ...] = ()) -> sqlite3.Cursor:
        with self._lock:
            cur = self._conn.execute(sql, params)
            self._conn.commit()
            return cur

    def fetchall(self, sql: str, params: tuple[Any, ...] = ()) -> list[sqlite3.Row]:
        with self._lock:
            return list(self._conn.execute(sql, params).fetchall())

    def fetchone(self, sql: str, params: tuple[Any, ...] = ()) -> sqlite3.Row | None:
        with self._lock:
            row = self._conn.execute(sql, params).fetchone()
            return row if row is not None else None

    def get_setting(self, key: str, default: str = "") -> str:
        row = self.fetchone("SELECT value FROM settings WHERE key=?", (key,))
        return str(row["value"]) if row else default

    def set_setting(self, key: str, value: str) -> None:
        self.execute(
            "INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )

    def add_note(self, text: str, ts: float) -> int:
        cur = self.execute("INSERT INTO notes(text, created_at) VALUES(?,?)", (text, ts))
        return int(cur.lastrowid or 0)

    def list_notes(self) -> list[sqlite3.Row]:
        return self.fetchall("SELECT * FROM notes ORDER BY id DESC")

    def delete_note(self, note_id: int) -> None:
        self.execute("DELETE FROM notes WHERE id=?", (note_id,))

    def search_notes(self, q: str) -> list[sqlite3.Row]:
        return self.fetchall(
            "SELECT * FROM notes WHERE text LIKE ? ORDER BY id DESC", (f"%{q}%",)
        )

    def log_deleted(self, sender: str, body: str, ts: float, kind: str) -> None:
        self.execute(
            "INSERT INTO deleted_log(sender, body, ts, kind) VALUES(?,?,?,?)",
            (sender, body, ts, kind),
        )

    def list_deleted(self) -> list[sqlite3.Row]:
        return self.fetchall("SELECT * FROM deleted_log ORDER BY id DESC")

    def store_callback_payload(self, payload: dict[str, Any]) -> int:
        cur = self.execute("INSERT INTO callbacks(payload) VALUES(?)", (json.dumps(payload),))
        return int(cur.lastrowid or 0)

    def get_callback_payload(self, cid: int) -> dict[str, Any] | None:
        row = self.fetchone("SELECT payload FROM callbacks WHERE id=?", (cid,))
        if not row:
            return None
        data = json.loads(str(row["payload"]))
        if not isinstance(data, dict):
            return None
        return data

    def close(self) -> None:
        with self._lock:
            self._conn.close()
