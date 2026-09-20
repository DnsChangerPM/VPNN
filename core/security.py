from __future__ import annotations

import logging
import random
import time

from core.storage import Storage

log = logging.getLogger("security")


class Security:
    def __init__(self, storage: Storage, owner_id: int) -> None:
        self.storage = storage
        self._owner = owner_id
        self._ensure_row()
        if owner_id:
            self.bind(owner_id)

    def _ensure_row(self) -> None:
        row = self.storage.fetchone("SELECT * FROM pairing WHERE id=1")
        if not row:
            self.storage.execute(
                "INSERT INTO pairing(id, code, owner_id, used) VALUES(1, NULL, NULL, 0)"
            )

    def owner_id(self) -> int:
        row = self.storage.fetchone("SELECT owner_id FROM pairing WHERE id=1")
        if row and row["owner_id"]:
            return int(row["owner_id"])
        return self._owner

    def is_owner(self, user_id: int) -> bool:
        oid = self.owner_id()
        return bool(oid) and user_id == oid

    def generate_code(self) -> str:
        code = f"{random.randint(0, 999999):06d}"
        self.storage.execute(
            "UPDATE pairing SET code=?, used=0 WHERE id=1",
            (code,),
        )
        return code

    def try_pair(self, text: str, user_id: int) -> bool:
        row = self.storage.fetchone("SELECT code, used FROM pairing WHERE id=1")
        if not row or not row["code"] or int(row["used"]) == 1:
            return False
        if text.strip() != str(row["code"]):
            return False
        self.bind(user_id)
        self.storage.execute("UPDATE pairing SET used=1, code=NULL WHERE id=1")
        return True

    def bind(self, owner_id: int) -> None:
        self._owner = owner_id
        self.storage.execute("UPDATE pairing SET owner_id=? WHERE id=1", (owner_id,))
        self.storage.set_setting("owner_id", str(owner_id))

    def gate_callback(self, user_id: int) -> bool:
        if self.is_owner(user_id):
            return True
        log.warning("security: rejected uid=%s at %s", user_id, int(time.time()))
        return False
