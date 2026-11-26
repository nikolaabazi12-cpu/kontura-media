"""Reel 9:16 (1080 × 1920, 30 fps) me shembullin DRITË të Llogaritësit LED.

Shkronjat, shiritat dhe metrat vijnë nga motori i programit (out/led_demo_DRITE.json);
skripti vetëm i animon: shiritat vizatohen shkronjë pas shkronje dhe numëruesi rritet
deri te totali që jep programi.
"""
import base64
import json
import math
import subprocess
import sys
from pathlib import Path

RRENJA = Path(__file__).resolve().parent
D = json.loads((RRENJA / "out" / "led_demo_DRITE.json").read_text(encoding="utf-8"))
SHENJA = base64.b64encode((RRENJA / "asetet" / "shenja_K.svg").read_bytes()).decode("ascii")
DOSJA = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/reel_drite")
DOSJA.mkdir(parents=True, exist_ok=True)

W, H, FPS, KOHA = 1080, 1920, 30, 11.0
NAVY, FACE, EDGE, LED, DRITE, GRI = "#10161C", "#2B3742", "#8FA3B5", "#FFD23F", "#EEF0EA", "#8FA3B5"

T = D["totalet"]
TOTAL_M, ME_REZERVE, RROTULLA = T["m"], T["withRes"], T["rolls"]
REZ = round(D["cfg"]["reserve"]) if isinstance(D["cfg"].get("reserve"), (int, float)) else 5
ROLL = D["cfg"].get("roll", 5)

PJESET = D["pjeset"]
BW, BH = D["kufijte"]["w"], D["kufijte"]["h"]
S = 960.0 / BW                      # px për mm
TX, TY = (W - BW * S) / 2, 690.0    # kuti e fjalës në ekran


def nf(v, d=2):
    return ("%.*f" % (d, v)).replace(".", ",")


def gjatesia(pts):
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


for p in PJESET:
    p["L"] = [gjatesia(s) for s in p["strips"]]

# Vizatimi: 5 s për gjithë LED-in, me shpejtësi të njëjtë; çdo shkronjë merr kohë sa LED-i i saj.
T0, T1 = 1.3, 6.3
LED_GJITHSEJ = sum(p["led_mm"] for p in PJESET)
fillimet, t = [], T0
for p in PJESET:
    d = (T1 - T0) * p["led_mm"] / LED_GJITHSEJ
    fillimet.append((t, d))
    t += d


def lehte(x):  # easeOutCubic në [0, 1]
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def hyrje(t, a, b):
    return lehte((t - a) / (b - a))


def polyline(pts, f, L, **atr):
    if f <= 0 or L <= 0:
        return ""
    pp = " ".join("%.2f,%.2f" % (x, y) for x, y in pts)
    dash = "" if f >= 1 else ' stroke-dasharray="%.2f %.2f" stroke-dashoffset="%.2f"' % (L, L, L * (1 - f))
    a = " ".join('%s="%s"' % (k.replace("_", "-"), v) for k, v in atr.items())
    return '<polyline points="%s" %s%s/>' % (pp, a, dash)


def kuadri(i):
    t = i / FPS
    ops_kok = hyrje(t, 0.0, 0.5)
    ops_shk = hyrje(t, 0.4, 1.1)
    ops_num = hyrje(t, 1.0, 1.3)
    r1, r2, cta = hyrje(t, 6.6, 7.1), hyrje(t, 7.3, 7.8), hyrje(t, 8.2, 8.7)

    led_m, crisp, glow = 0.0, [], []
    for p, (a, d) in zip(PJESET, fillimet):
        f = 1.0 if t >= a + d else (0.0 if t <= a else (t - a) / d)
        led_m += p["led_mm"] / 1000 * f
        for s, L in zip(p["strips"], p["L"]):
            crisp.append(polyline(s, f, L))
            glow.append(polyline(s, f, L))
    if t >= T1:
        led_m = TOTAL_M

    shkronjat = "".join('<path d="%s"/>' % p["d"] for p in PJESET)
    o = []
    o.append('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
             'width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H))
    o.append('<defs><filter id="g" filterUnits="userSpaceOnUse" x="-60" y="-60" width="%.0f" height="%.0f">'
             '<feGaussianBlur stdDeviation="11"/></filter></defs>' % (BW + 120, BH + 120))
    o.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, NAVY))
    # koka: shenja + KONTURA + etiketa
    o.append('<g opacity="%.3f">' % ops_kok)
    o.append('<image x="84" y="236" width="55" height="58" xlink:href="data:image/svg+xml;base64,%s"/>' % SHENJA)
    o.append('<text x="154" y="283" font-family="Barlow Condensed" font-weight="800" font-size="40" '
             'letter-spacing="3.2" fill="%s">KONTURA</text>' % DRITE)
    o.append('<rect x="760" y="241" width="236" height="48" rx="24" fill="%s"/>' % LED)
    o.append('<text x="878" y="273" text-anchor="middle" font-family="Barlow Condensed" font-weight="800" '
             'font-size="24" letter-spacing="1.6" fill="%s">LLOGARITËS LED</text>' % NAVY)
    dy = 30 * (1 - ops_kok)
    o.append('<text font-family="Barlow Condensed" font-weight="800" font-size="124" fill="%s">'
             '<tspan x="84" y="%.1f">Sa metra <tspan fill="%s">LED</tspan></tspan>'
             '<tspan x="84" y="%.1f">duhen?</tspan></text>' % (DRITE, 470 + dy, LED, 590 + dy))
    o.append('</g>')
    # fjala
    o.append('<g transform="translate(%.2f %.2f) scale(%.5f)">' % (TX, TY, S))
    o.append('<g opacity="%.3f" fill="%s" fill-rule="evenodd" stroke="%s" stroke-width="4" '
             'stroke-linejoin="round">%s</g>' % (ops_shk, FACE, EDGE, shkronjat))
    o.append('<g filter="url(#g)" opacity="0.85" fill="none" stroke="%s" stroke-width="18" stroke-linecap="round" '
             'stroke-linejoin="round">%s</g>' % (LED, "".join(glow)))
    o.append('<g fill="none" stroke="%s" stroke-width="10" stroke-linecap="round" stroke-linejoin="round">%s</g>'
             % ("#FFE58A", "".join(crisp)))
    o.append('</g>')
    o.append('<text x="84" y="1022" opacity="%.3f" font-family="Barlow" font-weight="600" font-size="30" '
             'fill="%s">Shembulli DRITË · shkronja 40 cm</text>' % (ops_shk, GRI))
    # numëruesi
    o.append('<g opacity="%.3f">' % ops_num)
    o.append('<text x="84" y="1098" font-family="Barlow Condensed" font-weight="600" font-size="34" '
             'letter-spacing="3" fill="%s">LED GJITHSEJ</text>' % GRI)
    o.append('<text x="534" y="1248" text-anchor="end" font-family="JetBrains Mono" font-weight="700" '
             'font-size="150" fill="%s">%s</text>' % (LED, nf(led_m)))
    o.append('<text x="556" y="1248" font-family="Barlow Condensed" font-weight="800" font-size="100" '
             'fill="%s">m</text>' % LED)
    o.append('</g>')
    o.append('<text x="84" y="%.1f" opacity="%.3f" font-family="Barlow" font-weight="600" font-size="50" '
             'fill="%s">me %d %% rezervë: %s m</text>' % (1336 + 20 * (1 - r1), r1, DRITE, REZ, nf(ME_REZERVE)))
    o.append('<text x="84" y="%.1f" opacity="%.3f" font-family="Barlow" font-weight="600" font-size="50" '
             'fill="%s">%d rrotulla prej %s m</text>' % (1406 + 20 * (1 - r2), r2, DRITE, RROTULLA, nf(ROLL, 0)))
    o.append('<text x="84" y="1480" opacity="%.3f" font-family="Barlow" font-weight="600" font-size="34" '
             'fill="%s">Llogaritës LED për Shkronja · na shkruani në DM</text>' % (cta, GRI))
    o.append('</svg>')
    return "".join(o)


N = int(KOHA * FPS)
for i in range(N):
    (DOSJA / ("f%04d.svg" % i)).write_text(kuadri(i), encoding="utf-8")
print("kuadro:", N, "| LED", nf(TOTAL_M), "m | me rezervë", nf(ME_REZERVE), "m |", RROTULLA, "rrotulla | rezerva",
      REZ, "% | rrotulla", ROLL, "m")
