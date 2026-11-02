from http.server import BaseHTTPRequestHandler
from urllib.request import Request, urlopen
import json

CLUB_SLUG = "shadow-knights34"   # Teil hinter chess.com/club/

def hole_zahl():
    url = f"https://api.chess.com/pub/club/{CLUB_SLUG}"
    anfrage = Request(url, headers={"User-Agent": "ShadowKnightsLive/1.0"})
    with urlopen(anfrage) as antwort:
        daten = json.loads(antwort.read().decode())
    return round(daten.get("average_daily_rating", 0))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        zahl = hole_zahl()
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="90" height="20">'
            f'<text x="45" y="16" text-anchor="middle" '
            f'font-family="Segoe UI, Arial, sans-serif" font-size="14" '
            f'font-weight="bold" fill="#b57edd">{zahl}</text>'
            '</svg>'
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "image/svg+xml")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(svg)
