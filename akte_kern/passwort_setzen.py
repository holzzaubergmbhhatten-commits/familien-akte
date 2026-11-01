"""Legt das Passwort für die Akte-Seite an. Auf dem Gerät ausführen, nie hier im Chat.

Ablauf: Das Passwort wird abgefragt (unsichtbar), es erscheint nur der Hash.
Den Hash trägst du als AKTE_PASSWORT_HASH ein. Das Passwort selbst wird nirgends gespeichert.
"""
import getpass
from server import passwort_hash

if __name__ == "__main__":
    a = getpass.getpass("Neues Passwort für die Akte: ")
    b = getpass.getpass("Passwort noch einmal: ")
    if a != b:
        raise SystemExit("Die beiden Eingaben stimmen nicht überein.")
    if len(a) < 10:
        raise SystemExit("Bitte mindestens 10 Zeichen.")
    import os
    ordner = os.environ.get("AKTE_PFAD", ".")
    os.makedirs(ordner, exist_ok=True)
    with open(os.path.join(ordner, "passwort.hash"), "w", encoding="utf-8") as f:
        f.write(passwort_hash(a))
    print("Passwort gespeichert. Es steht nirgends im Klartext.")
