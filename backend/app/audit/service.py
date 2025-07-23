import time
from typing import Any

_events: list[dict[str, Any]] = []


def log_event(user_id: str | None, action: str, meta: dict | None = None) -> None:
    _events.append({"ts": time.time(), "user": user_id, "action": action, "meta": meta or {}})


def get_events(limit: int = 100) -> list[dict[str, Any]]:
    return list(reversed(_events))[:limit]
