"""Kern der Familien-Akte: Eingang, Rückfragen, Ablage.

Keine Daten in diesem Repository. Ablage und Schlüssel liegen auf dem Gerät
(Umgebungsvariable AKTE_PFAD), nie hier.
"""
import json
import os
import shutil
from datetime import datetime

OBJEKTE = {
    "haus1": "Haus 1 (Name auf dem Gerät)",
    "haus2": "Haus 2 (Name auf dem Gerät)",
    "haus3": "Haus 3 (Name auf dem Gerät)",
    "privat": "Privat (Depots, Konten, Versicherungen)",
    "unklar": "Noch unklar",
}

BESITZER = {
    "papa": "Papa",
    "stief": "Stiefmutter",
    "gemeinsam": "Gemeinsam",
    "unklar": "Noch unklar",
}


def akte_pfad():
    pfad = os.environ.get("AKTE_PFAD")
    if not pfad:
        raise RuntimeError("AKTE_PFAD ist nicht gesetzt (liegt auf dem Gerät, nicht hier)")
    return pfad


def eintrag_anlegen(dateiname, quelle_pfad):
    """Legt ein Dokument im Eingang ab und merkt sich die offenen Rückfragen."""
    base = akte_pfad()
    eingang = os.path.join(base, "eingang")
    os.makedirs(eingang, exist_ok=True)
    ziel = os.path.join(eingang, dateiname)
    shutil.copy2(quelle_pfad, ziel)
    eintrag = {
        "datei": dateiname,
        "eingegangen": datetime.now().isoformat(timespec="seconds"),
        "objekt": "unklar",
        "besitzer": "unklar",
        "zugeordnet": False,
    }
    _schreiben(os.path.join(base, "akte.json"), eintrag)
    return eintrag


def rueckfragen(eintrag):
    """Fragen, die der Bot stellt, bevor ein Dokument abgelegt wird."""
    fragen = []
    if eintrag["objekt"] == "unklar":
        fragen.append(("Zu welchem Objekt gehört das?", list(OBJEKTE.items())))
    if eintrag["besitzer"] == "unklar":
        fragen.append(("Wem gehört das?", list(BESITZER.items())))
    return fragen


def zuordnen(eintrag, objekt, besitzer):
    """Schreibt die Antworten zurück. Nur gültige Schlüssel werden angenommen."""
    if objekt in OBJEKTE:
        eintrag["objekt"] = objekt
    if besitzer in BESITZER:
        eintrag["besitzer"] = besitzer
    eintrag["zugeordnet"] = eintrag["objekt"] != "unklar" and eintrag["besitzer"] != "unklar"
    return eintrag


def _schreiben(pfad, eintrag):
    alt = []
    if os.path.exists(pfad):
        with open(pfad, encoding="utf-8") as f:
            alt = json.load(f)
    alt.append(eintrag)
    tmp = pfad + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(alt, f, ensure_ascii=False, indent=2)
    os.replace(tmp, pfad)
