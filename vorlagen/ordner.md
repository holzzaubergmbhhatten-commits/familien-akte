# Ordnerstruktur der Akte (nur Vorlage)

Auf dem Gerät, nicht hier im Repository:

- `akte/objekte/<id>/` für jedes Haus (Stammdaten, Mietverträge, Nebenkosten, Belege)
- `akte/mieter/<id>/` für Mieter (Vertrag, Kontakt, Zahlungen)
- `akte/steuer/<jahr>/` für Steuerunterlagen je Jahr
- `akte/eingang/` für neue Belege per Telegram, bis sie zugeordnet sind

Jede Datei bekommt einen Eintrag in `akte.json` mit Datum, Art und Zuordnung. Die Dateien selbst bleiben lokal.
