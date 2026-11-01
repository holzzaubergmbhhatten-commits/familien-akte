"""Telegram-Eingang der Familien-Akte.

Nimmt Nachrichten vom Bot entgegen. Nur bekannte Chat-IDs werden angenommen.
Ein Dokument wird abgelegt, dann kommen die Rückfragen als Knöpfe.
Keine Daten, keine Tokens in diesem Repository: Chat-IDs und Token liegen
auf dem Gerät (Umgebungsvariablen).
"""
import os

from eingang import BESITZER, OBJEKTE, eintrag_anlegen, rueckfragen, zuordnen


def erlaubte_chats():
    """Chat-IDs aus der Umgebung, z. B. AKTE_CHATS="123,456"."""
    roh = os.environ.get("AKTE_CHATS", "")
    return {c.strip() for c in roh.split(",") if c.strip()}


def ist_erlaubt(chat_id):
    return str(chat_id) in erlaubte_chats()


def knoepfe_fuer(frage_schluessel, optionen):
    """Telegram-Knöpfe als Liste von Zeilen. callback_data: frage|wert."""
    return [[{"text": name, "callback_data": f"{frage_schluessel}|{schluessel}"}]
            for schluessel, name in optionen]


def verarbeite_dokument(chat_id, dateiname, quelle_pfad):
    """Nimmt ein Dokument an und liefert Antworttext und Knöpfe für die nächste Frage."""
    if not ist_erlaubt(chat_id):
        return {"text": None, "knoepfe": None}   # fremde Chats bekommen keine Antwort
    eintrag = eintrag_anlegen(dateiname, quelle_pfad)
    fragen = rueckfragen(eintrag)
    if not fragen:
        return {"text": f"„{dateiname}“ ist abgelegt.", "knoepfe": None}
    frage_text, optionen = fragen[0]
    schluessel = "objekt" if "Objekt" in frage_text else "besitzer"
    return {"text": f"„{dateiname}“ angekommen. {frage_text}",
            "knoepfe": knoepfe_fuer(schluessel, optionen)}


def verarbeite_antwort(chat_id, callback_data, eintrag):
    """Verarbeitet einen Knopfdruck. Gibt den aktualisierten Eintrag und den nächsten Schritt zurück."""
    if not ist_erlaubt(chat_id):
        return eintrag, None
    feld, wert = callback_data.split("|", 1)
    if feld == "objekt":
        eintrag = zuordnen(eintrag, wert, eintrag["besitzer"])
    elif feld == "besitzer":
        eintrag = zuordnen(eintrag, eintrag["objekt"], wert)
    offen = rueckfragen(eintrag)
    if not offen:
        return eintrag, {"text": "Zugeordnet und abgelegt.", "knoepfe": None}
    frage_text, optionen = offen[0]
    schluessel = "objekt" if "Objekt" in frage_text else "besitzer"
    return eintrag, {"text": frage_text, "knoepfe": knoepfe_fuer(schluessel, optionen)}
