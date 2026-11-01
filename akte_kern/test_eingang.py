"""Prüft den Kern ohne echte Daten: läuft mit einem temporären Ordner."""
import os
import tempfile
from eingang import eintrag_anlegen, rueckfragen, zuordnen, OBJEKTE, BESITZER

with tempfile.TemporaryDirectory() as tmp:
    os.environ["AKTE_PFAD"] = tmp
    quelle = os.path.join(tmp, "beispiel.txt")
    with open(quelle, "w") as f:
        f.write("Testdatei ohne Inhalt")
    e = eintrag_anlegen("beispiel.txt", quelle)
    assert not e["zugeordnet"]
    assert len(rueckfragen(e)) == 2
    e = zuordnen(e, "birk", "papa")
    assert e["zugeordnet"] is True
    assert rueckfragen(e) == []
    e2 = zuordnen(eintrag_anlegen("b2.txt", quelle), "gibtsnicht", "papa")
    assert e2["objekt"] == "unklar" and not e2["zugeordnet"]
    assert "privat" in OBJEKTE and "stief" in BESITZER
print("alle Prüfungen bestanden")
