"""Prüft vor jeder Ablage, zu welcher Akte eine Nachricht gehört.

Deine Akte und Papas Akte sind getrennt: eigener Bot, eigene Chat-Liste, eigener Ordner.
Eine Nachricht, die nicht zum Bot und zum Chat passt, wird verworfen. Nichts wird geraten.
"""
import os


def akte_fuer(bot_name, chat_id):
    """Gibt ('marco' | 'papa', Ordner) zurück, oder None, wenn Bot und Chat nicht zusammenpassen."""
    chat = str(chat_id)
    if bot_name == os.environ.get("AKTE_BOT_MARCO", "") and chat in _liste("AKTE_CHATS_MARCO"):
        return "marco", os.environ.get("AKTE_ORDNER_MARCO", "")
    if bot_name == os.environ.get("AKTE_BOT_PAPA", "") and chat in _liste("AKTE_CHATS_PAPA"):
        return "papa", os.environ.get("AKTE_ORDNER_PAPA", "")
    return None


def _liste(name):
    return {c.strip() for c in os.environ.get(name, "").split(",") if c.strip()}


def ordner_sind_getrennt():
    m = os.environ.get("AKTE_ORDNER_MARCO", "")
    p = os.environ.get("AKTE_ORDNER_PAPA", "")
    return bool(m) and bool(p) and os.path.abspath(m) != os.path.abspath(p)
