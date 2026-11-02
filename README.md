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
- `ansicht.py`: was Papa sieht. Immer nur eine Frage, Startzahlen, Rechte nur für die Akte.
- `fehler.py`: Fehler werden lokal gespeichert und Marco per Telegram gemeldet (AKTE_ADMIN_CHAT auf dem Gerät).
- `test_ansicht.py`: Prüfung ohne echte Daten.
- `aktionen.py`: Aktionen an Dokumenten wie in der Akte zu Hause (ansehen, Ordner, Foto, Notiz, eingereicht, zusammenfügen, auflösen, löschen mit Bestätigung), dazu Vorgangsarten: Nebenkosten, Mietvertrag, Steuer, Depot, Versicherung, Sonstiges.
- `test_aktionen.py`: Prüfung ohne echte Dokumente.
- `server.py`: eigener kleiner Server nur für die Akte-Seite. Passwort als Hash auf dem Gerät (AKTE_PASSWORT_HASH), Sitzung, Fehlversuche werden gebremst. Läuft getrennt von Home Assistant, Zugriff über Tailscale.
- `test_server.py`: Prüfung der Anmeldung ohne echte Daten.
- `chat_pruefung.py`: Trennung der Akten. Bot und Chat müssen zusammenpassen, sonst wird verworfen. Zwei getrennte Ordner.
- `test_chat_pruefung.py`: Prüfung der Trennung ohne echte Chats.
