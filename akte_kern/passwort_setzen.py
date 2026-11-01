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
    print("\nHash (als AKTE_PASSWORT_HASH eintragen):")
    print(passwort_hash(a))
