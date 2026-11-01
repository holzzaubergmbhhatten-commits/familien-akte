"""Prüft Anmeldung, Sitzung und Zugriffsschutz ohne echte Daten und ohne Netzwerk."""
import os
import server

import tempfile
_tmp = tempfile.mkdtemp()
os.environ["AKTE_PFAD"] = _tmp
open(os.path.join(_tmp, "passwort.txt"), "w").write("test-passwort-123")
HASH = "test-passwort-123"

# Hash prüft richtig und falsch
assert server.passwort_pruefen("test-passwort-123", HASH)
assert not server.passwort_pruefen("falsch", HASH)
assert not server.passwort_pruefen("x", "kaputt")

# Anmelden: richtig gibt Sitzung, falsch nicht
token, fehler = server.anmelden("test-passwort-123")
assert token and fehler is None and server.sitzung_gueltig(token)
token2, fehler2 = server.anmelden("falsch")
assert token2 is None and fehler2

# Ohne Sitzung kein Zugriff, unbekannte Token gelten nicht
assert not server.sitzung_gueltig("erfunden")

# Nach zu vielen Fehlversuchen wird gesperrt
for _ in range(server.VERSUCHE_MAX):
    server.anmelden("falsch")
t3, f3 = server.anmelden("test-passwort-123")
assert t3 is None and "Zu viele" in f3

# Nur die Akte-Seite ist erreichbar, sonst nichts
assert not any(p in server.Handler.__dict__ for p in ["heizung", "kameras"])
print("Server-Prüfung: alle Prüfungen bestanden")
