from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass
class WizardState:
    kind: str
    step: str
    data: dict[str, str]
    expires: float


class Wizard:
    def __init__(self, timeout: float = 180.0) -> None:
        self.timeout = timeout
        self._state: dict[int, WizardState] = {}

    def start(self, user_id: int, kind: str, step: str = "text") -> None:
        self._state[user_id] = WizardState(kind=kind, step=step, data={}, expires=time.time() + self.timeout)

    def get(self, user_id: int) -> WizardState | None:
        st = self._state.get(user_id)
        if not st:
            return None
        if time.time() > st.expires:
            self._state.pop(user_id, None)
            return None
        return st

    def cancel(self, user_id: int) -> None:
        self._state.pop(user_id, None)

    def finish(self, user_id: int) -> WizardState | None:
        return self._state.pop(user_id, None)
