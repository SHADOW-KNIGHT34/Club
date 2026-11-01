# ============================================================
# SHADOW KNIGHTS – Live-Zahlen als PNG (badge.py)
# Erzeugt transparente PNG-Bilder mit den Live-Zahlen
# (Mitglieder + Ø-Rating) – PNG ist das sicherste Bildformat
# für chess.com-Seitenleisten.
#
# Datei: badge.py  (kompletten Inhalt der alten badge.py ersetzen!)
# ============================================================

import json
import urllib.request
from PIL import Image, ImageDraw, ImageFont

# --- EINSTELLUNGEN -----------------------------------------
CLUB_SLUG = "shadow-knights34"   # Der Teil hinter chess.com/club/
CLUB_URL = "https://www.chess.com/club/shadow-knights34"
# -----------------------------------------------------------

API_URL = f"https://api.chess.com/pub/club/{CLUB_SLUG}"

headers = {"User-Agent": "ShadowKnightsLiveBadge/1.0 (Club-Sidebar)"}
req = urllib.request.Request(API_URL, headers=headers)

with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())

# Live-Zahlen aus der API
members = data.get("members_count", 0)
avg_rating = round(data.get("average_daily_rating", 0))

# --- PNG-Erzeugung (transparente Zahl, passend zur Schrift) --
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT = ImageFont.truetype(FONT_PATH, 28)

def make_number_png(value, filename, hex_color):
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
    text = str(value)
    # Textgroesse messen
    messer = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    bbox = messer.textbbox((0, 0), text, font=FONT)
    breite = bbox[2] - bbox[0] + 8
    hoehe = bbox[3] - bbox[1] + 8
    img = Image.new("RGBA", (breite, hoehe), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((4 - bbox[0], 4 - bbox[1]), text, font=FONT, fill=rgb + (255,))
    img.save(filename)
    print(f"Erzeugt: {filename} ({text})")

# Mitgliederzahl (Neonblau) und Rating (Violett) als PNG
make_number_png(members, "members.png", "#7df9ff")
make_number_png(avg_rating, "rating.png", "#b57edd")

# --- Live-Stats-Webseite bleibt wie bisher (index.html) -----
html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SHADOW KNIGHTS – Live-Stats</title>
<style>
  body {{ margin: 0; padding: 40px 20px; background: #0b0b1a;
         font-family: 'Segoe UI', Arial, sans-serif; color: #e6e6fa; text-align: center; }}
  .box {{ max-width: 420px; margin: 0 auto; background: rgba(20, 20, 45, 0.6);
         border: 1px solid #3b3b6d; border-radius: 12px; padding: 25px 20px;
         box-shadow: 0 0 15px rgba(125, 249, 255, 0.15); }}
  h1 {{ color: #7df9ff; font-size: 20px; letter-spacing: 2px; margin: 0 0 25px 0; }}
  .stat {{ margin-bottom: 25px; }}
  .stat .zahl {{ font-size: 48px; font-weight: bold; color: #7df9ff; line-height: 1.1; }}
  .stat .label {{ font-size: 13px; color: #b0a8d8; letter-spacing: 2px; margin-top: 4px; }}
  .stat.violett .zahl {{ color: #b57edd; }}
  .trenner {{ border: 0; border-top: 1px solid #3b3b6d; margin: 10px 0 25px 0; }}
  a.button {{ display: inline-block; background: linear-gradient(135deg, #6a5acd, #3b3b6d);
             color: #7df9ff; font-weight: bold; font-size: 13px; text-decoration: none;
             padding: 10px 18px; border-radius: 6px; border: 1px solid #7df9ff;
             box-shadow: 0 0 10px rgba(125, 249, 255, 0.3); letter-spacing: 1px; }}
  .fussnote {{ margin-top: 20px; font-size: 11px; color: #b0a8d8; font-style: italic; }}
</style>
</head>
<body>
  <div class="box">
    <h1>&#9876;&#65039; SHADOW KNIGHTS LIVE-STATS &#9876;&#65039;</h1>
    <div class="stat"><div class="zahl">{members}</div><div class="label">RITTER IM CLUB</div></div>
    <hr class="trenner">
    <div class="stat violett"><div class="zahl">&#216; {avg_rating}</div><div class="label">T&Auml;GLICHES-SCHACH-RATING</div></div>
    <a class="button" href="{CLUB_URL}" target="_blank" rel="noopener">&#9876;&#65039; ZUM CLUB</a>
    <div class="fussnote">Diese Zahlen werden automatisch jede Stunde aktualisiert.</div>
  </div>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"OK: {members} Mitglieder, Ø {avg_rating} -> members.png, rating.png, index.html")

# ============================================================
# Datei: .github/workflows/update-badge.yml
# WICHTIG: zwei Veraenderungen gegenueber der alten Version!
#   1. Neue Zeile:  - run: pip install pillow   (vor python badge.py)
#   2. git add: members.png rating.png index.html
# ============================================================

# name: Live-Stats Update
# on:
#   schedule:
#     - cron: "0 * * * *"
#   workflow_dispatch: {}
# permissions:
#   contents: write
# jobs:
#   update:
#     runs-on: ubuntu-latest
#     steps:
#       - uses: actions/checkout@v4
#       - uses: actions/setup-python@v5
#         with:
#           python-version: "3.12"
#       - run: pip install pillow
#       - run: python badge.py
#       - run: |
#           git config user.name "LiveStats Bot"
#           git config user.email "actions@github.com"
#           git add members.png rating.png index.html
#           git diff --cached --quiet || git commit -m "Update live stats"
#           git push

# ============================================================
# SIDEBAR-EINBAU (neue PNG-Adressen!):
# ============================================================
#
# <img src="https://raw.githubusercontent.com/SHADOW-KNIGHT34/Club/main/members.png"
#      style="height: 14px; vertical-align: middle;" alt="Mitglieder" />
#
# <img src="https://raw.githubusercontent.com/SHADOW-KNIGHT34/Club/main/rating.png"
#      style="height: 14px; vertical-align: middle;" alt="Rating" />
#
# Alternativ ueber GitHub Pages:
#   https://shadow-knight34.github.io/Club/members.png
#   https://shadow-knight34.github.io/Club/rating.png
