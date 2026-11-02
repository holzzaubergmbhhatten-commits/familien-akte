"""Prüft die Trennung der Akten ohne echte Chats oder Bots."""
import os
import tempfile
import chat_pruefung as cp

with tempfile.TemporaryDirectory() as tmp:
    os.environ.update({"AKTE_BOT_MARCO": "bot_marco", "AKTE_BOT_PAPA": "bot_papa",
                       "AKTE_CHATS_MARCO": "111", "AKTE_CHATS_PAPA": "222",
                       "AKTE_ORDNER_MARCO": os.path.join(tmp, "m"), "AKTE_ORDNER_PAPA": os.path.join(tmp, "p")})
    assert cp.akte_fuer("bot_marco", "111")[0] == "marco"
    assert cp.akte_fuer("bot_papa", "222")[0] == "papa"
    # falscher Bot mit richtigem Chat: verworfen
    assert cp.akte_fuer("bot_papa", "111") is None
    assert cp.akte_fuer("bot_marco", "222") is None
    # unbekannter Chat: verworfen
    assert cp.akte_fuer("bot_marco", "999") is None
    assert cp.ordner_sind_getrennt()
    os.environ["AKTE_ORDNER_PAPA"] = os.environ["AKTE_ORDNER_MARCO"]
    assert not cp.ordner_sind_getrennt()
print("Chat-Trennung: alle Prüfungen bestanden")
