from __future__ import annotations

from i18n import en, fa

_LANG = "fa"
_PACKS = {"fa": fa.STRINGS, "en": en.STRINGS}


def set_lang(lang: str) -> None:
    global _LANG
    if lang not in _PACKS:
        raise ValueError(f"unsupported lang: {lang}")
    _LANG = lang


def get_lang() -> str:
    return _LANG


def t(key: str, **kwargs: object) -> str:
    pack = _PACKS[_LANG]
    fallback = _PACKS["en"]
    raw = pack.get(key, fallback.get(key, key))
    if kwargs:
        return raw.format(**kwargs)
    return raw


def all_keys() -> set[str]:
    return set(fa.STRINGS.keys()) | set(en.STRINGS.keys())
