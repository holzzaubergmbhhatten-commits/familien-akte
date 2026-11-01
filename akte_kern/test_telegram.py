"""Prüft den Telegram-Eingang ohne echte Chats, Tokens oder Dokumente."""
import os
import tempfile
from telegram_eingang import verarbeite_dokument, verarbeite_antwort

with tempfile.TemporaryDirectory() as tmp:
    os.environ["AKTE_PFAD"] = tmp
    os.environ["AKTE_CHATS"] = "111"
    quelle = os.path.join(tmp, "x.txt")
    open(quelle, "w").write("Testinhalt")

    # fremder Chat bekommt nichts
    assert verarbeite_dokument("999", "x.txt", quelle)["text"] is None

    # erlaubter Chat: erst Objekt-Frage, dann Besitzer-Frage, dann fertig
    antwort = verarbeite_dokument("111", "x.txt", quelle)
    assert "Objekt" in antwort["text"] and antwort["knoepfe"]
    eintrag = {"datei": "x.txt", "objekt": "unklar", "besitzer": "unklar", "zugeordnet": False}
    eintrag, schritt = verarbeite_antwort("111", "objekt|haus1", eintrag)
    assert "Besitzer" in schritt["text"] or "gehört" in schritt["text"]
    eintrag, schritt = verarbeite_antwort("111", "besitzer|papa", eintrag)
    assert eintrag["zugeordnet"] and schritt["knoepfe"] is None
print("Telegram-Eingang: alle Prüfungen bestanden")
