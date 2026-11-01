"""Fehlermeldungen der Akte. Gehen immer an Marco (AKTE_ADMIN_CHAT auf dem Gerät).

Papa sieht eine einfache Meldung, Marco bekommt die technische Ursache.
Ohne Token oder Chat-ID geschieht nichts, damit nichts im Code steht.
"""
import json
import os
from datetime import datetime

FEHLER_DATEI = "fehler.json"


def admin_chat():
    return os.environ.get("AKTE_ADMIN_CHAT", "").strip()


def melde_fehler(kurz, technisch, senden=None):
    """Schreibt den Fehler in die lokale Liste und schickt Marco eine Nachricht.

    senden: Funktion (chat_id, text) -> None, z. B. der Telegram-Versand.
    Gibt die Nachricht zurück, die Papa sieht.
    """
    eintrag = {"zeit": datetime.now().isoformat(timespec="seconds"), "kurz": kurz, "technisch": technisch}
    pfad = os.path.join(os.environ.get("AKTE_PFAD", "."), FEHLER_DATEI)
    alt = []
    if os.path.exists(pfad):
        with open(pfad, encoding="utf-8") as f:
            alt = json.load(f)
    alt.append(eintrag)
    with open(pfad, "w", encoding="utf-8") as f:
        json.dump(alt[-200:], f, ensure_ascii=False, indent=2)
    if senden and admin_chat():
        senden(admin_chat(), f"⚠️ Akte: {kurz}\nTechnik: {technisch}")
    return f"Da hat etwas nicht geklappt: {kurz}. Marco wurde informiert."
