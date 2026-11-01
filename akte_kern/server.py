"""Eigener kleiner Server für die Akte-Seite (nur die Akte, nichts anderes).

Läuft getrennt von Home Assistant. Papa bekommt nur diese Adresse, nicht das Haus.
Anmeldung mit Passwort. Das Passwort wird nur als Hash auf dem Gerät gespeichert.
Keine Dateiliste, keine Heizung, keine Kameras, keine Türen.
"""
import hashlib
import hmac
import http.server
import json
import os
import secrets
import time
from urllib.parse import urlparse

HIER = os.path.dirname(os.path.abspath(__file__))
SEITE = os.path.join(HIER, "..", "www", "akte.html")
BILDER = os.path.join(HIER, "..", "www", "bilder")
SITZUNG_SEKUNDEN = 60 * 60 * 12
VERSUCHE_MAX = 8
VERSUCHE_FENSTER = 15 * 60
_sitzungen = {}     # token -> Ablaufzeit
_versuche = []      # Zeitpunkte fehlgeschlagener Anmeldungen


def passwort_hash(passwort, salz=None):
    salz = salz or secrets.token_bytes(16)
    h = hashlib.pbkdf2_hmac("sha256", passwort.encode("utf-8"), salz, 200_000)
    return salz.hex() + "$" + h.hex()


def passwort_pruefen(passwort, gespeichert):
    try:
        salz_hex, h_hex = gespeichert.split("$", 1)
    except ValueError:
        return False
    neu = passwort_hash(passwort, bytes.fromhex(salz_hex)).split("$", 1)[1]
    return hmac.compare_digest(neu, h_hex)


def gespeicherter_hash():
    """Liest den Hash aus AKTE_PFAD/passwort.hash (wird von passwort_setzen.py angelegt)."""
    datei = os.path.join(os.environ.get("AKTE_PFAD", "."), "passwort.hash")
    if not os.path.isfile(datei):
        raise RuntimeError("Noch kein Passwort gesetzt: passwort_setzen.py ausführen")
    with open(datei, encoding="utf-8") as f:
        return f.read().strip()


def anmelden(passwort):
    jetzt = time.time()
    _versuche[:] = [t for t in _versuche if jetzt - t < VERSUCHE_FENSTER]
    if len(_versuche) >= VERSUCHE_MAX:
        return None, "Zu viele Versuche. Bitte 15 Minuten warten."
    if not passwort_pruefen(passwort, gespeicherter_hash()):
        _versuche.append(jetzt)
        return None, "Das Passwort passt nicht."
    token = secrets.token_urlsafe(32)
    _sitzungen[token] = jetzt + SITZUNG_SEKUNDEN
    return token, None


def sitzung_gueltig(token):
    ablauf = _sitzungen.get(token)
    if not ablauf or time.time() > ablauf:
        _sitzungen.pop(token, None)
        return False
    return True


class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "Akte"

    def _antwort(self, code, body, typ="application/json; charset=utf-8", kopf=None):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False).encode("utf-8")
        elif isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", typ)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Robots-Tag", "noindex, nofollow")
        self.send_header("X-Content-Type-Options", "nosniff")
        for k, v in (kopf or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _token(self):
        for teil in self.headers.get("Cookie", "").split(";"):
            if teil.strip().startswith("akte_sitz="):
                return teil.strip().split("=", 1)[1]
        return ""

    def _eingeloggt(self):
        return sitzung_gueltig(self._token())

    def do_GET(self):
        pfad = urlparse(self.path).path
        if pfad == "/":
            if not self._eingeloggt():
                return self._antwort(200, ANMELDUNG_HTML, "text/html; charset=utf-8")
            with open(SEITE, encoding="utf-8") as f:
                return self._antwort(200, f.read(), "text/html; charset=utf-8")
        if pfad.startswith("/bilder/") and self._eingeloggt():
            name = os.path.basename(pfad)
            datei = os.path.join(BILDER, name)
            if os.path.isfile(datei) and name.endswith(".png"):
                with open(datei, "rb") as f:
                    return self._antwort(200, f.read(), "image/png")
        if pfad == "/api/daten" and self._eingeloggt():
            return self._antwort(200, {"ok": True, "hinweis": "Daten folgen bei der Einspielung"})
        return self._antwort(404, {"ok": False, "fehler": "Nicht gefunden"})

    def do_POST(self):
        pfad = urlparse(self.path).path
        laenge = int(self.headers.get("Content-Length", "0") or 0)
        if laenge > 4096:
            return self._antwort(413, {"ok": False, "fehler": "Zu groß"})
        daten = self.rfile.read(laenge).decode("utf-8", "replace")
        if pfad == "/anmelden":
            passwort = ""
            for teil in daten.split("&"):
                if teil.startswith("passwort="):
                    from urllib.parse import unquote_plus
                    passwort = unquote_plus(teil.split("=", 1)[1])
            token, fehler = anmelden(passwort)
            if fehler:
                return self._antwort(401, {"ok": False, "fehler": fehler})
            kopf = {"Set-Cookie": f"akte_sitz={token}; Path=/; Max-Age={SITZUNG_SEKUNDEN}; HttpOnly; Secure; SameSite=Strict"}
            return self._antwort(200, {"ok": True}, kopf=kopf)
        if pfad.startswith("/api/") and self._eingeloggt():
            return self._antwort(200, {"ok": True})
        return self._antwort(403, {"ok": False, "fehler": "Bitte anmelden"})

    def log_message(self, format, *args):
        return  # keine Zugriffsprotokolle mit Adressen oder Passwörtern


ANMELDUNG_HTML = """<!doctype html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>Akte – Anmelden</title>
<style>body{font-family:system-ui,sans-serif;background:#f7f4ed;color:#2d3329;margin:0;padding:24px}
.k{max-width:380px;margin:40px auto;background:#fff;border-radius:16px;padding:22px}
input{width:100%;font-size:20px;padding:12px;border:1px solid #d8c7a3;border-radius:10px;margin:10px 0}
button{width:100%;font-size:18px;padding:12px;border:0;border-radius:10px;background:#536b45;color:#fff}
#f{color:#b5452a;display:none}</style></head><body>
<div class="k"><h2>Akte</h2><p>Bitte Passwort eingeben.</p>
<form id="form"><input type="password" id="pw" autocomplete="current-password" placeholder="Passwort">
<button type="submit">Anmelden</button></form><p id="f"></p></div>
<script>
document.getElementById('form').onsubmit=async e=>{e.preventDefault();
const r=await fetch('/anmelden',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'passwort='+encodeURIComponent(document.getElementById('pw').value)});
if(r.ok){location.reload()}else{const j=await r.json().catch(()=>({}));const f=document.getElementById('f');f.textContent=j.fehler||'Das hat nicht geklappt.';f.style.display='block'}};
</script></body></html>"""


def start(port=8765, host="127.0.0.1"):
    """Startet den Server. Für den Zugriff über Tailscale an die Tailscale-Adresse binden."""
    gespeicherter_hash()   # bricht früh ab, wenn kein Passwort gesetzt ist
    http.server.ThreadingHTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    start(port=int(os.environ.get("AKTE_PORT", "8765")), host=os.environ.get("AKTE_HOST", "127.0.0.1"))
