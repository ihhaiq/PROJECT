from contextlib import contextmanager
from contextvars import ContextVar, Token
from typing import Iterator


SUPPORTED_LANGUAGES = frozenset({"ar", "en"})
DEFAULT_LANGUAGE = "en"

_current_language: ContextVar[str] = ContextVar(
    "current_language",
    default=DEFAULT_LANGUAGE,
)


def normalize_language(language: str | None, *, default: str = DEFAULT_LANGUAGE) -> str:
    if not isinstance(language, str):
        return default
    value = language.strip().lower().replace("_", "-")
    primary = value.split("-", 1)[0]
    if primary in SUPPORTED_LANGUAGES:
        return primary
    return default


def get_current_language(language: str | None = None) -> str:
    if language is not None:
        return normalize_language(language)
    return _current_language.get()


def is_arabic(language: str | None = None) -> bool:
    return get_current_language(language) == "ar"


def set_current_language(language: str | None) -> Token[str]:
    return _current_language.set(normalize_language(language))


def reset_current_language(token: Token[str]) -> None:
    _current_language.reset(token)


@contextmanager
def language_context(language: str | None) -> Iterator[str]:
    normalized = normalize_language(language)
    token = set_current_language(normalized)
    try:
        yield normalized
    finally:
        reset_current_language(token)
