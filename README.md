# Familien-Akte (nur Code)

Digitale Akte für Papa: Belege, Mietverträge, Nebenkostenabrechnungen, Steuerunterlagen.
Dieses Repository enthält NUR den Code. Alle Daten liegen auf dem Gerät (Home Assistant), nie hier.

## Aufbau (geplant)
- `packages/`  Home-Assistant-Pakete (Akte, Telegram-Bots, Zugang)
- `www/`       Browser-Seite der Akte
- `claude_tools/` Auswertung und Ablage
- `docs/`      Anleitungen in einfacher Sprache

## Regeln
- Keine echten Dokumente, Namen von Mietern, Kontodaten oder Zugangsdaten ins Repository.
- Schlüssel und Passwörter nur in Home Assistant eintragen, nie in Dateien.
- Dateien mit Daten sind per `.gitignore` ausgeschlossen.

## Vorlagen
- `vorlagen/objekt.json.beispiel`: Aufbau eines Hauses mit Wohneinheiten, Nebenkosten und Steuer (ohne echte Daten)
- `vorlagen/ordner.md`: nur der Hauptordner auf dem Gerät
