from __future__ import annotations


class CallbackTooLongError(ValueError):
    pass


MAX_CB = 64


def encode(ns: str, action: str, ident: str = "") -> str:
    parts = [ns, action]
    if ident != "":
        parts.append(ident)
    data = ":".join(parts)
    raw = data.encode("utf-8")
    if len(raw) > MAX_CB:
        raise CallbackTooLongError(f"callback_data {len(raw)} bytes > {MAX_CB}: {data!r}")
    return data


def decode(data: str) -> tuple[str, str, str]:
    parts = data.split(":", 2)
    ns = parts[0] if parts else ""
    action = parts[1] if len(parts) > 1 else ""
    ident = parts[2] if len(parts) > 2 else ""
    return ns, action, ident
