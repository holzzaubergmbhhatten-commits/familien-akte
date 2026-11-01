"""Prüft Ansicht und Fehlermeldung ohne echte Daten."""
import json
import os
import tempfile
from ansicht import naechste_frage, zusammenfassung, erlaubte_bereiche
from fehler import melde_fehler

with tempfile.TemporaryDirectory() as tmp:
    os.environ["AKTE_PFAD"] = tmp
    os.environ["AKTE_ADMIN_CHAT"] = "111"
    gesendet = []
    text = melde_fehler("Dokument nicht lesbar", "PDF-Header fehlt", senden=lambda c, t: gesendet.append((c, t)))
    assert "Marco" in text and gesendet[0][0] == "111" and "PDF-Header" in gesendet[0][1]
    assert json.load(open(os.path.join(tmp, "fehler.json")))[0]["kurz"] == "Dokument nicht lesbar"
    # ohne Admin-Chat: nichts wird verschickt, aber lokal gespeichert
    os.environ["AKTE_ADMIN_CHAT"] = ""
    melde_fehler("noch ein Fehler", "x", senden=lambda c, t: gesendet.append((c, t)))
    assert len(gesendet) == 1

    frage = naechste_frage({"objekt": "unklar", "besitzer": "unklar"})
    assert frage["frage"].startswith("Zu welchem Objekt") and len(frage["antworten"]) == 5
    assert naechste_frage({"objekt": "birk", "besitzer": "papa"}) is None

    z = zusammenfassung([{"zugeordnet": True}, {"zugeordnet": False}])
    assert z["fertig"] == 1 and z["wartet"] == 1

    rechte = erlaubte_bereiche()
    assert rechte["akte"] and not rechte["heizung"] and not rechte["tueren"]
print("Ansicht und Fehlermeldung: alle Prüfungen bestanden")
