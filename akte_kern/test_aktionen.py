"""Prüft die Aktionen ohne echte Dokumente."""
from aktionen import ausfuehren, vorgangsart, AKTIONEN, VORGANGSARTEN

e = {"datei": "x.pdf"}
for a in AKTIONEN:
    e, _ = ausfuehren(e, a, wert="x", bestaetigt=True) if a != "zusammenfuegen" else ausfuehren(e, a, wert=["y"])
e = {"datei": "x.pdf"}
e, m = ausfuehren(e, "loeschen")
assert "bestätigen" in m and not e.get("geloescht")
e, m = ausfuehren(e, "loeschen", bestaetigt=True)
assert e["geloescht"] and e["verlauf"][-1]["aktion"] == "loeschen"
e, _ = ausfuehren(e, "foto", wert="bild1.jpg")
assert e["fotos"] == ["bild1.jpg"]
e, _ = vorgangsart({"datei": "n.pdf"}, "nebenkosten")
assert e["art"] == "nebenkosten" and "nebenkosten" in VORGANGSARTEN
assert ausfuehren({}, "gibtsnicht")[1] == "Diese Aktion gibt es nicht."
print("Aktionen: alle Prüfungen bestanden")
