# ============================================================
# SHADOW KNIGHTS – Live-Zahlen (transparente Einzel-SVGs)
# Holt Daten aus der chess.com-API und erzeugt pro Zahl ein
# kleines, transparentes SVG – passend zum Neon-Design der
# Sidebar. Die SVGs werden per <img> in die HTML-Blöcke
# eingesetzt (dort, wo die Zahl stehen soll).
#
# Datei: badge.py
# ============================================================

import json
import urllib.request

# --- EINSTELLUNGEN -----------------------------------------
CLUB_SLUG = "DEIN-CLUB-SLUG"   # Der Teil hinter chess.com/club/
# -----------------------------------------------------------

API_URL = f"https://api.chess.com/pub/club/{CLUB_SLUG}"

headers = {"User-Agent": "ShadowKnightsLiveBadge/1.0 (Club-Sidebar)"}
req = urllib.request.Request(API_URL, headers=headers)

with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())

# Live-Zahlen aus der API
members = data.get("members_count", 0)
avg_rating = round(data.get("average_daily_rating", 0))

# --- Vorlage: transparentes SVG mit nur EINER Zahl ----------
def make_number_svg(value, filename, color="#7df9ff"):
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="90" height="20">'
        f'<text x="0" y="16" font-family="Segoe UI, Arial, sans-serif" '
        f'font-size="14" font-weight="bold" fill="{color}">{value}</text>'
        '</svg>'
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg)

# Mitgliederzahl (Neonblau, wie Überschriften)
make_number_svg(members, "members.svg", "#7df9ff")

# Durchschnittliches Rating (Violett, wie der Hinweis-Text)
make_number_svg(avg_rating, "rating.svg", "#b57edd")

print(f"OK: {members} Mitglieder (members.svg), Ø {avg_rating} (rating.svg)")

# ============================================================
# EINBAU IN DIE SIDEBAR (Beispiel):
# Statt einer festen Zahl setzt du ein Mini-Bild ein:
#
#   Aktuell dabei:
#   <img src="https://raw.githubusercontent.com/SHADOW-KNIGHT34/Club/main/members.svg"
#        style="height: 14px; vertical-align: middle;" alt="Mitglieder" /> Ritter
#
# ============================================================

# ============================================================
# Datei: .github/workflows/update-badge.yml
# GitHub Actions: aktualisiert die Zahlen automatisch jede Stunde.
# ============================================================

# name: Live-Stats Update
# on:
#   schedule:
#     - cron: "0 * * * *"   # jede volle Stunde
#   workflow_dispatch: {}    # plus manuell startbar
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
#       - run: python badge.py
#       - run: |
#           git config user.name "LiveStats Bot"
#           git config user.email "actions@github.com"
#           git add members.svg rating.svg
#           git diff --cached --quiet || git commit -m "Update live stats"
#           git push
