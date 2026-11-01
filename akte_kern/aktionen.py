"""Aktionen an einem Dokument der Akte: dieselben wie in eurer Akte zu Hause.

ansehen, ordner, foto, notiz, eingereicht, zusammenfuegen, aufloesen, loeschen,
plus Vorgangsarten für Nebenkosten und eigene Akten (z. B. privat, Depots).
Löschen braucht eine Bestätigung. Nichts wird ohne Spur entfernt.
"""
from datetime import datetime

AKTIONEN = ["ansehen", "ordner", "foto", "notiz", "eingereicht", "zusammenfuegen", "aufloesen", "loeschen"]

VORGANGSARTEN = {
    "nebenkosten": "Nebenkostenabrechnung",
    "mietvertrag": "Mietvertrag",
    "steuer": "Steuerbeleg",
    "depot": "Depot / Konto",
    "versicherung": "Versicherung",
    "sonst": "Sonstiges",
}


def _spur(eintrag, art, text=""):
    eintrag.setdefault("verlauf", []).append(
        {"zeit": datetime.now().isoformat(timespec="seconds"), "aktion": art, "text": text})
    return eintrag


def ausfuehren(eintrag, aktion, wert=None, bestaetigt=False):
    """Führt eine Aktion aus. Gibt (eintrag, meldung) zurück."""
    if aktion not in AKTIONEN:
        return eintrag, "Diese Aktion gibt es nicht."
    if aktion == "ansehen":
        return eintrag, "Dokument wird angezeigt."
    if aktion == "ordner":
        eintrag["ordner"] = wert or ""
        return _spur(eintrag, "ordner", wert or ""), "Ordner gespeichert."
    if aktion == "foto":
        eintrag.setdefault("fotos", []).append(wert)
        return _spur(eintrag, "foto", wert), "Foto angehängt."
    if aktion == "notiz":
        eintrag["notiz"] = wert or ""
        return _spur(eintrag, "notiz", wert or ""), "Notiz gespeichert."
    if aktion == "eingereicht":
        eintrag["eingereicht"] = datetime.now().date().isoformat()
        return _spur(eintrag, "eingereicht"), "Als eingereicht markiert."
    if aktion == "zusammenfuegen":
        if not wert:
            return eintrag, "Bitte mindestens ein weiteres Dokument wählen."
        eintrag.setdefault("vorgang", []).extend(wert)
        return _spur(eintrag, "zusammenfuegen", ",".join(wert)), "Zu einem Vorgang zusammengefügt."
    if aktion == "aufloesen":
        eintrag["vorgang"] = []
        return _spur(eintrag, "aufloesen"), "Vorgang aufgelöst."
    if aktion == "loeschen":
        if not bestaetigt:
            return eintrag, "Zum Löschen bitte bestätigen."
        eintrag["geloescht"] = True
        return _spur(eintrag, "loeschen"), "Gelöscht. Der Eintrag bleibt im Verlauf sichtbar."
    return eintrag, "Unbekannte Aktion."


def vorgangsart(eintrag, art):
    if art not in VORGANGSARTEN:
        return eintrag, "Diese Art gibt es nicht."
    eintrag["art"] = art
    return _spur(eintrag, "art", VORGANGSARTEN[art]), f"Art: {VORGANGSARTEN[art]}."
