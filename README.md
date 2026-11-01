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

## Akte-Kern (akte_kern/)
- `eingang.py`: nimmt Dokumente an, fragt nach Objekt und Besitzer, ordnet zu. Daten nur über `AKTE_PFAD` auf dem Gerät.
- `test_eingang.py`: Prüfung mit temporärem Ordner, ohne echte Daten.
- `telegram_eingang.py`: Telegram-Eingang. Nur erlaubte Chat-IDs (Umgebungsvariable AKTE_CHATS auf dem Gerät), Rückfragen als Knöpfe.
- `test_telegram.py`: Prüfung ohne echte Chats und Tokens.
