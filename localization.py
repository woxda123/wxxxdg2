import json
import os
from config import DEFAULT_LANG, SUPPORTED_LANGS

_translations = {}

def load_translations():
    base = os.path.join(os.path.dirname(__file__), "texts")
    for lang in SUPPORTED_LANGS:
        path = os.path.join(base, f"{lang}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                _translations[lang] = json.load(f)

def get_text(lang: str, key: str, **kwargs) -> str:
    if lang not in _translations:
        lang = DEFAULT_LANG
    text = _translations.get(lang, {}).get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
