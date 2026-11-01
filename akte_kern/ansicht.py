"""Was Papa auf der Akte-Seite sieht. Einfach: eine Frage nach der anderen, nie mehr als eine.

Dieselben Rechte wie zu Hause, aber nur für die Akte (nicht für Heizung, Kameras, Türen).
"""
from eingang import BESITZER, OBJEKTE, rueckfragen


def naechste_frage(eintrag):
    """Höchstens eine Frage gleichzeitig."""
    offen = rueckfragen(eintrag)
    if not offen:
        return None
    text, optionen = offen[0]
    return {"frage": text, "antworten": [{"schluessel": s, "name": n} for s, n in optionen]}


def zusammenfassung(eintraege):
    """Zählt für die Startseite: wie viele sind fertig, wie viele warten auf eine Antwort."""
    fertig = sum(1 for e in eintraege if e.get("zugeordnet"))
    wartet = len(eintraege) - fertig
    return {"fertig": fertig, "wartet": wartet,
            "text": f"{fertig} Dokumente abgelegt" + (f", {wartet} warten auf eine kurze Antwort." if wartet else ".")}


def erlaubte_bereiche():
    """Papa darf die Akte, nichts anderes im Haus."""
    return {"akte": True, "heizung": False, "kameras": False, "tueren": False}
