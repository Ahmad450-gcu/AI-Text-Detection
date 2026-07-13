import re
import unicodedata

_CONTROL_CHARS_RE = re.compile(r"[\x00-\x1F\x7F]")
_WHITESPACE_RE = re.compile(r"\s+")
_URL_PLACEHOLDER_RE = re.compile(r"URL_\d+")

def normalize_text(text: str | None) -> str:
    """Unicode-normalize, strip control characters, and collapse whitespace."""
    if text is None:
        return ""
    text = unicodedata.normalize("NFKC", str(text))
    text = _CONTROL_CHARS_RE.sub(" ", text)
    text = _WHITESPACE_RE.sub(" ", text)
    return text.strip()


def clean_text(text: str | None) -> str:
    text = normalize_text(text)
    text = _URL_PLACEHOLDER_RE.sub("<URL>", text)
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text
