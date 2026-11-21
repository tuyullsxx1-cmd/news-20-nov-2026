#!/usr/bin/env python3
"""Draw 'THE WORLD IN ONE DAY' - Friday 20 November 2026, one-page newspaper.
Renders entry.png (1024x1024) from the hardcoded, source-verified story list below.
Deterministic: no randomness, no time, no network. Run: python3 gen.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))
PAPER = (251, 247, 236)
INK = (24, 24, 24)
RED = (176, 32, 32)
NAVY = (31, 42, 68)
GREY = (110, 108, 100)
LTAN = (216, 201, 163)
WHITE = (255, 255, 255)

def font(bold, size):
    return ImageFont.truetype(
        os.path.join(BASE, "fonts", "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)

def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text(d, x, y, s, fnt, fill=INK, anchor="la"):
    d.text((x, y), s, font=fnt, fill=fill, anchor=anchor)

def center(d, cx, y, s, fnt, fill=INK):
    d.text((cx, y), s, font=fnt, fill=fill, anchor="ma")

def rrect(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

# ---------------- pictograms: simple, flat, clearly readable ----------------
def icon_bridge(d, x, y, s, c):
    # arched bridge over water
    d.line([(x, y + s * 0.62), (x + s, y + s * 0.62)], fill=c, width=max(3, s // 14))
    d.arc([x + s * 0.08, y + s * 0.30, x + s * 0.92, y + s * 0.95], 180, 360, fill=c, width=max(3, s // 14))
    for fx in (0.14, 0.50, 0.86):
        d.line([(x + s * fx, y + s * 0.34), (x + s * fx, y + s * 0.62)], fill=c, width=max(2, s // 20))
    d.line([(x + s * 0.10, y + s * 0.78), (x + s * 0.90, y + s * 0.78)], fill=c, width=max(2, s // 22))
    d.line([(x + s * 0.20, y + s * 0.88), (x + s * 0.80, y + s * 0.88)], fill=c, width=max(2, s // 22))

def icon_missile(d, x, y, s, c):
    d.polygon([(x + s * 0.50, y + s * 0.06), (x + s * 0.66, y + s * 0.30),
               (x + s * 0.50, y + s * 0.26), (x + s * 0.34, y + s * 0.30)], fill=c)
    d.rectangle([x + s * 0.42, y + s * 0.26, x + s * 0.58, y + s * 0.66], fill=c)
    d.polygon([(x + s * 0.42, y + s * 0.66), (x + s * 0.30, y + s * 0.86), (x + s * 0.42, y + s * 0.78)], fill=c)
    d.polygon([(x + s * 0.58, y + s * 0.66), (x + s * 0.70, y + s * 0.86), (x + s * 0.58, y + s * 0.78)], fill=c)
    d.polygon([(x + s * 0.44, y + s * 0.70), (x + s * 0.56, y + s * 0.70),
               (x + s * 0.50, y + s * 0.95)], fill=(230, 120, 40))

def icon_chip(d, x, y, s, c):
    d.rectangle([x + s * 0.24, y + s * 0.24, x + s * 0.76, y + s * 0.76], fill=c)
    d.rectangle([x + s * 0.40, y + s * 0.40, x + s * 0.60, y + s * 0.60], fill=(255, 255, 255))
    for i in range(3):
        px = x + s * (0.34 + 0.16 * i)
        d.line([(px, y + s * 0.08), (px, y + s * 0.24)], fill=c, width=max(2, s // 18))
        d.line([(px, y + s * 0.76), (px, y + s * 0.92)], fill=c, width=max(2, s // 18))
        py = y + s * (0.34 + 0.16 * i)
        d.line([(x + s * 0.08, py), (x + s * 0.24, py)], fill=c, width=max(2, s // 18))
        d.line([(x + s * 0.76, py), (x + s * 0.92, py)], fill=c, width=max(2, s // 18))

def icon_cyclone(d, x, y, s, c):
    for k, r in enumerate((0.44, 0.34, 0.24, 0.14)):
        d.arc([x + s * (0.5 - r), y + s * (0.5 - r), x + s * (0.5 + r), y + s * (0.5 + r)],
              40 + k * 55, 300 + k * 55, fill=c, width=max(3, s // 16))
    d.ellipse([x + s * 0.44, y + s * 0.44, x + s * 0.56, y + s * 0.56], fill=c)

def icon_flags(d, x, y, s, c):
    # UK flag (left) + EU flag (right)
    d.rectangle([x + s * 0.06, y + s * 0.20, x + s * 0.46, y + s * 0.55], fill=(30, 60, 140))
    d.rectangle([x + s * 0.06, y + s * 0.33, x + s * 0.46, y + s * 0.42], fill=WHITE)
    d.rectangle([x + s * 0.22, y + s * 0.20, x + s * 0.30, y + s * 0.55], fill=WHITE)
    d.rectangle([x + s * 0.06, y + s * 0.36, x + s * 0.46, y + s * 0.39], fill=RED)
    d.rectangle([x + s * 0.245, y + s * 0.20, x + s * 0.275, y + s * 0.55], fill=RED)
    d.rectangle([x + s * 0.54, y + s * 0.45, x + s * 0.94, y + s * 0.80], fill=(20, 50, 140))
    for k in range(8):
        import math
        a = math.pi * k / 4
        d.ellipse([x + s * (0.74 + 0.10 * math.cos(a)) - 2, y + s * (0.625 + 0.10 * math.sin(a)) - 2,
                   x + s * (0.74 + 0.10 * math.cos(a)) + 2, y + s * (0.625 + 0.10 * math.sin(a)) + 2],
                  fill=(255, 215, 0))

def icon_tanker(d, x, y, s, c):
    d.polygon([(x + s * 0.06, y + s * 0.42), (x + s * 0.94, y + s * 0.42),
               (x + s * 0.86, y + s * 0.68), (x + s * 0.14, y + s * 0.68)], fill=c)
    d.rectangle([x + s * 0.14, y + s * 0.28, x + s * 0.34, y + s * 0.42], fill=c)
    d.rectangle([x + s * 0.40, y + s * 0.30, x + s * 0.58, y + s * 0.42], fill=(200, 60, 40))
    d.rectangle([x + s * 0.62, y + s * 0.30, x + s * 0.80, y + s * 0.42], fill=(220, 170, 40))
    for wy in (0.78, 0.88):
        d.line([(x + s * 0.06, y + s * wy), (x + s * 0.94, y + s * wy)], fill=(90, 140, 190), width=max(2, s // 22))

def icon_controller(d, x, y, s, c):
    d.rounded_rectangle([x + s * 0.08, y + s * 0.30, x + s * 0.92, y + s * 0.74], radius=s * 0.12, fill=c)
    d.rectangle([x + s * 0.24, y + s * 0.44, x + s * 0.34, y + s * 0.60], fill=WHITE)
    d.rectangle([x + s * 0.19, y + s * 0.49, x + s * 0.39, y + s * 0.55], fill=WHITE)
    for bx, by in ((0.66, 0.46), (0.76, 0.54), (0.66, 0.60)):
        d.ellipse([x + s * bx, y + s * by, x + s * (bx + 0.09), y + s * (by + 0.09)], fill=(255, 215, 0))

def icon_car(d, x, y, s, c):
    d.polygon([(x + s * 0.08, y + s * 0.55), (x + s * 0.22, y + s * 0.38), (x + s * 0.55, y + s * 0.34),
               (x + s * 0.78, y + s * 0.42), (x + s * 0.92, y + s * 0.55), (x + s * 0.92, y + s * 0.68),
               (x + s * 0.08, y + s * 0.68)], fill=c)
    d.ellipse([x + s * 0.18, y + s * 0.62, x + s * 0.34, y + s * 0.78], fill=INK)
    d.ellipse([x + s * 0.64, y + s * 0.62, x + s * 0.80, y + s * 0.78], fill=INK)
    for lx in (0.10, 0.20, 0.30):
        d.line([(x + s * lx, y + s * 0.22), (x + s * (lx + 0.12), y + s * 0.22)], fill=(230, 120, 40), width=max(2, s // 20))

def icon_quake(d, x, y, s, c):
    d.line([(x + s * 0.10, y + s * 0.30), (x + s * 0.30, y + s * 0.55), (x + s * 0.45, y + s * 0.35),
            (x + s * 0.62, y + s * 0.70), (x + s * 0.78, y + s * 0.45), (x + s * 0.90, y + s * 0.62)],
           fill=c, width=max(3, s // 14))
    d.line([(x + s * 0.06, y + s * 0.82), (x + s * 0.94, y + s * 0.82)], fill=c, width=max(2, s // 22))
    d.line([(x + s * 0.20, y + s * 0.90), (x + s * 0.80, y + s * 0.90)], fill=c, width=max(2, s // 22))

def icon_cricket(d, x, y, s, c):
    d.polygon([(x + s * 0.42, y + s * 0.08), (x + s * 0.58, y + s * 0.08),
               (x + s * 0.52, y + s * 0.55), (x + s * 0.46, y + s * 0.55)], fill=(190, 150, 90))
    d.polygon([(x + s * 0.36, y + s * 0.55), (x + s * 0.62, y + s * 0.55),
               (x + s * 0.56, y + s * 0.88), (x + s * 0.42, y + s * 0.88)], fill=c)
    d.ellipse([x + s * 0.68, y + s * 0.66, x + s * 0.86, y + s * 0.84], fill=RED)

def icon_speech(d, x, y, s, c):
    d.rounded_rectangle([x + s * 0.08, y + s * 0.12, x + s * 0.66, y + s * 0.52], radius=s * 0.08, fill=c)
    d.polygon([(x + s * 0.20, y + s * 0.52), (x + s * 0.20, y + s * 0.70), (x + s * 0.34, y + s * 0.52)], fill=c)
    d.rounded_rectangle([x + s * 0.42, y + s * 0.48, x + s * 0.92, y + s * 0.82], radius=s * 0.08, fill=(90, 140, 190))
    d.polygon([(x + s * 0.74, y + s * 0.82), (x + s * 0.74, y + s * 0.94), (x + s * 0.60, y + s * 0.82)], fill=(90, 140, 190))
    d.line([(x + s * 0.18, y + s * 0.28), (x + s * 0.56, y + s * 0.28)], fill=WHITE, width=max(2, s // 22))
    d.line([(x + s * 0.18, y + s * 0.38), (x + s * 0.48, y + s * 0.38)], fill=WHITE, width=max(2, s // 22))

def icon_shield(d, x, y, s, c):
    d.polygon([(x + s * 0.50, y + s * 0.06), (x + s * 0.88, y + s * 0.20), (x + s * 0.88, y + s * 0.52),
               (x + s * 0.50, y + s * 0.94), (x + s * 0.12, y + s * 0.52), (x + s * 0.12, y + s * 0.20)], fill=c)
    d.line([(x + s * 0.32, y + s * 0.48), (x + s * 0.46, y + s * 0.64), (x + s * 0.70, y + s * 0.32)],
           fill=WHITE, width=max(3, s // 13))

def icon_globe(d, x, y, s, c):
    d.ellipse([x + s * 0.08, y + s * 0.08, x + s * 0.92, y + s * 0.92], outline=c, width=max(3, s // 14))
    d.ellipse([x + s * 0.38, y + s * 0.08, x + s * 0.62, y + s * 0.92], outline=c, width=max(2, s // 22))
    d.line([(x + s * 0.08, y + s * 0.50), (x + s * 0.92, y + s * 0.50)], fill=c, width=max(2, s // 22))
    d.arc([x + s * 0.08, y + s * 0.22, x + s * 0.92, y + s * 0.78], 200, 340, fill=c, width=max(2, s // 22))
    d.arc([x + s * 0.08, y + s * 0.22, x + s * 0.92, y + s * 0.78], 20, 160, fill=c, width=max(2, s // 22))

ICONS = {"bridge": icon_bridge, "missile": icon_missile, "chip": icon_chip,
         "cyclone": icon_cyclone, "flags": icon_flags, "tanker": icon_tanker,
         "controller": icon_controller, "car": icon_car, "quake": icon_quake,
         "cricket": icon_cricket, "speech": icon_speech, "shield": icon_shield,
         "globe": icon_globe}
ICON_BG = {"bridge": (200, 60, 40), "missile": (150, 30, 30), "chip": (31, 42, 68),
           "cyclone": (20, 120, 130), "flags": (60, 90, 160), "tanker": (40, 70, 110),
           "controller": (110, 60, 150), "car": (220, 90, 20), "quake": (140, 90, 40),
           "cricket": (40, 130, 70), "speech": (70, 90, 120), "shield": (40, 110, 60),
           "globe": (30, 110, 90)}

# ---------------- verified stories: Friday 20 November 2026 ----------------
# (title, detail, source, icon, lat, lon) - every figure from the named source.
FEATURED = [
    ("KYIV'S BRIDGES HIT", "3 bridges over the Dnipro struck by ballistic missiles overnight; 27 ballistic + 84 cruise + 404 drones; 8 killed, 28 hurt", "REUTERS", "bridge", 50.45, 30.52),
    ("MISSILES IN POLAND", "2 missiles + 1 drone in SE Poland; NATO jets scrambled", "AP / REUTERS", "missile", 50.05, 22.45),
    ("NVIDIA -14%", "Fell to $125.53 on SEC probe report; Nasdaq -5.3%", "WSJ / REUTERS", "chip", 37.37, -121.92),
    ("COP31 DEADLOCK", "Draft stripped ALL fossil-fuel mentions; no final text", "ANEWZ", "globe", 36.90, 30.70),
    ("CYCLONE AKVAN", "Landfall Odisha, gusts 90 km/h; 300,000+ evacuated", "IMD", "cyclone", 19.27, 84.92),
    ("UK-EU RESET DEAL", "Food deal 5.1bn pounds/yr; youth mobility 100,000/yr", "REUTERS", "flags", 50.85, 4.35),
    ("HORMUZ TANKER HIT", "Tanker struck off Khasab, Oman; fire, no casualties", "REUTERS / UKMTO", "tanker", 26.18, 56.24),
    ("GTA VI: $3.79B", "32.5M copies; biggest entertainment launch ever", "CNN / TAKE-TWO", "controller", 40.71, -74.00),
    ("F1 RUSSELL FASTEST", "Las Vegas FP3 1:34.041; Mercedes 1-2; clash probed", "F1.COM", "car", 36.17, -115.14),
    ("PERU M6.7 QUAKE", "Central Peru 19:09 local; felt in Lima; no casualties", "USGS", "quake", -11.16, -75.99),
    ("PHILLIPS 118", "Centuries in all 3 formats vs India in one year", "ICC / AP", "cricket", -41.29, 174.78),
    ("TRUMP: PUTIN TIRED", "Putin is tired and ready for a deal, Trump says", "CNN", "speech", 38.90, -77.04),
    ("IRAQ RECLAIMS TOWN", "Forces enter Kataib Hezbollah town, 1st time in 12 yrs", "AFP / REUTERS", "shield", 32.80, 44.20),
]

# (number, title, detail, source, lat, lon)
LISTED = [
    (14, "Anthropic -9% after IPO", "Shares ~$89, day after debut closed +17% at $97", "INVESTOPEDIA", 37.77, -122.42),
    (15, "Iran seizes tanker Talara", "Marshall Islands-flagged; 'unauthorised cargo'", "HELLENIC SHIPPING", 26.50, 56.00),
    (16, "Tara Gas: 2nd Hormuz hit", "1 Indian sailor missing; 24 of 25 crew accounted for", "TECHWORDNEWS", 26.30, 56.10),
    (17, "Angola buys 10% of De Beers", "About $180M for the stake, via state miner Endiama", "REUTERS", -8.83, 13.23),
    (18, "India busts opioid network", "6 arrested; network shipped opioids to US via apps", "REUTERS", 28.61, 77.21),
    (19, "US Treasury warns SG + MY", "Officials pressed both on Iran sanctions compliance", "REUTERS", 1.35, 103.82),
    (20, "Saudi strikes Hodeidah + Sanaa", "Hit Houthi-held port; 5 drones + 1 missile downed", "AP", 14.80, 42.95),
    (21, "Estonia closes Russia border", "Road crossings shut from 1 Dec for at least 6 months", "REUTERS", 59.44, 24.75),
    (22, "Houthi threat to Saudi pact", "Senate vote on the pact due in the week of 30 Nov", "REUTERS", 24.71, 46.68),
    (23, "Riemann hypothesis CLAIM", "Claims he + Claude proved it; NOT verified", "SCIAM", 37.77, -122.42),
    (24, "California quakes", "M4.2 near LA; M5.0 Pinnacles + 78 aftershocks", "USGS", 34.05, -118.24),
    (25, "BTS win Artist of the Year", "MAMA Day 1 Osaka; 8th Daesang; ENHYPEN win", "ALLKPOP", 34.66, 135.50),
    (26, "Ronaldo goal No. 986", "14 from 1,000; scored 14th min, Al-Ahli won 3-1", "ESPN", 24.71, 46.68),
    (27, "Asia rout", "Nikkei -4.8%, KOSPI -5.2%, TAIEX -6.6%", "REUTERS", 35.68, 139.69),
    (28, "Nations League draw", "Spain-France, Norway-England, Netherlands-Portugal", "UEFA", 46.20, 6.14),
    (29, "Xi-Albanese turnaround", "'Comprehensive turnaround'; 2027 = tourism year", "REUTERS", 22.55, 114.06),
    (30, "Florida floods", "~100 water rescues; Fort Lauderdale 17in rain in 48h", "NWS", 28.54, -81.38),
    (31, "Kenya starts oil drilling", "Turkana spudding Fri; 1st oil Dec 1; 20,000 bpd", "PEOPLE DAILY", 3.00, 35.50),
    (32, "Malawi fuel crisis", "Queues overnight; ration 20L/day; 6 blast deaths", "AL JAZEERA", -15.77, 35.00),
    (33, "Infantino in Warri, Nigeria", "Inspects 20,000-seat stadium; 30bn naira rebuild", "TELEGRAPH", 5.55, 5.80),
    (34, "Bayer $7.25B settlement", "Court approves Roundup cancer-claims settlement", "AP", 38.63, -90.20),
    (35, "Denmark: Russia plot to kill", "Russia accused of plot to kill American-Ukrainian", "AP", 55.68, 12.57),
    (36, "Italy general strike", "CGIL strike in 100+ cities; 1M+ marched", "REUTERS", 41.90, 12.50),
    (37, "Korea: AI exam cheating", "Lee orders exam overhaul; 111 device violations", "ASIA DAILY", 37.57, 126.98),
    (38, "Mamdani: close Rikers Island", "Plan to shut NYC's notorious jail", "AP", 40.71, -74.00),
    (39, "Senate passes permitting bill", "Energy permitting overhaul 62-33; House action next", "AP", 38.90, -77.04),
    (40, "Sydney terror raid", "Man charged after raids; car-bomb research alleged", "REUTERS", -33.87, 151.21),
]

REGIONS = [("Americas", 11), ("Middle East", 7), ("Europe", 7), ("Asia", 7),
           ("Africa", 4), ("Global", 2), ("Oceania", 2)]

LEFT_OUT = ["World Court verdict on Myanmar", "Shenzhen trilateral declaration",
            "Tonga drought", "Senegal migrant boat"]
# (also Thu, noted in SOURCES.md only: Druzhba strike confirmed Fri; Bangladesh violence Wed-Thu)
NOT_YET = ["BepiColombo enters Mercury orbit", "COP31 final text"]

STRIP = ["3 BRIDGES HIT", "NVDA -14%", "$3.79B GTA VI", "M6.7 PERU",
         "300K EVACUATED", "$7.25B BAYER"]

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66), (-80, 73),
     (-65, 60), (-55, 52), (-60, 46), (-70, 42), (-75, 35), (-80, 32), (-85, 30),
     (-90, 21), (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49),
     (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 9), (-75, 11), (-62, 11), (-52, 5), (-50, 0), (-44, -3), (-35, -8),
     (-40, -20), (-48, -28), (-58, -38), (-65, -45), (-68, -52), (-70, -54),
     (-73, -44), (-73, -30), (-70, -18), (-80, -5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (3, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (30, 60), (30, 70), (25, 71), (18, 69),
     (12, 66), (5, 60), (-5, 58), (-10, 54), (-10, 43)],
    [(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12), (51, 11),
     (48, 2), (40, -10), (35, -18), (32, -26), (26, -33), (19, -35),
     (15, -27), (12, -18), (9, -1), (9, 4), (-8, 5), (-13, 8), (-17, 15),
     (-17, 21), (-10, 30)],
    [(30, 36), (35, 36), (43, 41), (48, 38), (54, 37), (58, 26), (60, 25),
     (66, 25), (72, 20), (77, 8), (80, 7), (85, 20), (89, 22), (92, 16),
     (95, 16), (100, 8), (103, 1), (104, 9), (108, 11), (109, 15), (106, 20),
     (108, 22), (113, 22), (117, 23), (120, 25), (122, 30), (127, 33),
     (129, 35), (132, 38), (135, 43), (138, 46), (141, 50), (142, 54),
     (140, 60), (142, 68), (158, 66), (170, 66), (178, 65), (178, 62),
     (170, 60), (162, 58), (156, 52), (150, 59), (142, 54)],
    [(114, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32),
     (136, -35), (140, -38), (145, -38), (150, -37), (153, -27), (153, -22),
     (146, -19), (142, -11), (137, -12), (132, -12), (126, -14), (122, -17)],
]

# ---------------- layout ----------------
def draw_masthead(d):
    d.line([(16, 12), (1008, 12)], fill=INK, width=3)
    center(d, 512, 16, "THE WORLD IN ONE DAY", font(True, 62), INK)
    center(d, 512, 82, "FRIDAY  20  NOVEMBER  2026", font(True, 30), RED)
    d.line([(16, 116), (1008, 116)], fill=INK, width=2)

def draw_strip(d):
    d.rectangle([16, 124, 1008, 158], fill=NAVY)
    line = "   \u2022   ".join(STRIP)
    size = 19
    while size > 12 and d.textlength(line, font=font(True, size)) > 972:
        size -= 1
    center(d, 512, 133, line, font(True, size), WHITE)

def draw_banner(d):
    x0, y0, x1, y1 = 16, 166, 1008, 284
    d.rectangle([x0, y0, x1, y1], fill=(253, 236, 236), outline=RED, width=2)
    d.rectangle([x0, y0, x0 + 8, y1], fill=RED)
    title, detail, src, ic, la, lo = FEATURED[0]
    # bridge pictogram, large
    rrect(d, [x0 + 20, y0 + 14, x0 + 116, y0 + 104], 10, fill=ICON_BG[ic])
    icon_bridge(d, x0 + 28, y0 + 22, 80, WHITE)
    text(d, x0 + 132, y0 + 12, "TOP STORY  \u2014  KYIV, UKRAINE", font(True, 15), RED)
    text(d, x0 + 132, y0 + 32, title, font(True, 30), INK)
    for i, ln in enumerate(wrap(d, detail, font(False, 16), x1 - x0 - 160)):
        text(d, x0 + 132, y0 + 66 + i * 20, ln, font(False, 16), (60, 60, 60))
    text(d, x1 - 16, y0 + 12, src, font(True, 14), RED, anchor="ra")

def draw_tiles(d):
    tiles = FEATURED[1:]
    tw, th, gap = 242, 82, 8
    for i, (title, detail, src, ic, la, lo) in enumerate(tiles):
        col, row = i % 4, i // 4
        x0 = 16 + col * (tw + gap)
        y0 = 292 + row * (th + 6)
        d.rectangle([x0, y0, x0 + tw, y0 + th], fill=WHITE, outline=(200, 196, 184), width=1)
        rrect(d, [x0 + 6, y0 + 6, x0 + 54, y0 + 54], 8, fill=ICON_BG[ic])
        ICONS[ic](d, x0 + 11, y0 + 11, 38, WHITE)
        lines = wrap(d, title, font(True, 14), tw - 62)
        for j, ln in enumerate(lines[:2]):
            text(d, x0 + 60, y0 + 6 + j * 17, ln, font(True, 14), INK)
        det = wrap(d, detail, font(False, 12), tw - 62)
        max_det = 2 if len(lines[:2]) == 1 else 1
        base = y0 + 6 + len(lines[:2]) * 17
        for j, ln in enumerate(det[:max_det]):
            text(d, x0 + 60, base + j * 15, ln, font(False, 12), (70, 70, 70))
        text(d, x0 + tw - 6, y0 + th - 16, src, font(True, 10), GREY, anchor="ra")

def draw_list(d):
    y = 556
    text(d, 16, y, "THE REST OF THE DAY  \u2014  27 MORE STORIES", font(True, 17), INK)
    text(d, 1008, y, "40 STORIES IN ALL", font(True, 14), RED, anchor="ra")
    d.line([(16, y + 24), (1008, y + 24)], fill=INK, width=2)
    y0 = y + 32
    colw, rowh = 324, 31
    for i, (num, title, detail, src, la, lo) in enumerate(LISTED):
        col, row = i // 9, i % 9
        x = 16 + col * (colw + 8)
        yy = y0 + row * rowh
        # source rides on the title line; detail gets the full column width
        text(d, x, yy, f"{num}. {title}", font(True, 13), INK)
        text(d, x + colw, yy, src, font(True, 9), GREY, anchor="ra")
        text(d, x, yy + 15, detail, font(False, 11), (70, 70, 70))

def draw_bottom(d):
    y0 = 872
    d.line([(16, y0 - 6), (1008, y0 - 6)], fill=INK, width=2)
    # --- map ---
    text(d, 16, y0, "WHERE IT HAPPENED", font(True, 15), INK)
    mx0, my0, mx1, my1 = 16, y0 + 22, 400, y0 + 122
    d.rectangle([mx0, my0, mx1, my1], fill=(232, 240, 244), outline=(200, 196, 184), width=1)
    mw, mh = mx1 - mx0, my1 - my0
    for poly in CONTINENTS:
        pts = [(mx0 + (lon + 180) / 360 * mw, my0 + (90 - lat) / 180 * mh) for lon, lat in poly]
        d.polygon(pts, fill=LTAN, outline=(150, 135, 100))
    allstories = FEATURED + [("x", det, s, "globe", la, lo) for (_, _, det, s, la, lo) in LISTED]
    for (_, _, _, _, la, lo) in allstories:
        px = mx0 + (lo + 180) / 360 * mw
        py = my0 + (90 - la) / 180 * mh
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED, outline=WHITE, width=1)
    # --- region counts ---
    rx = 424
    text(d, rx, y0, "BY REGION", font(True, 15), INK)
    for i, (name, cnt) in enumerate(REGIONS):
        yy = y0 + 24 + i * 15
        bar = int(cnt / 12 * 90)
        d.rectangle([rx, yy + 2, rx + bar, yy + 11], fill=NAVY)
        text(d, rx + 96, yy, f"{name}  {cnt}", font(False, 12), INK)
    # --- date check ---
    dx0, dx1 = 648, 1008
    d.rectangle([dx0, y0, dx1, y0 + 122], fill=(240, 240, 234), outline=INK, width=1)
    text(d, dx0 + 10, y0 + 6, "DATE CHECK", font(True, 15), RED)
    yy = y0 + 24
    text(d, dx0 + 10, yy, "LEFT OUT \u2014 Thursday 19 Nov:", font(True, 11), INK)
    yy += 12
    for item in LEFT_OUT:
        for ln in wrap(d, "\u2022  " + item, font(False, 10), dx1 - dx0 - 20):
            text(d, dx0 + 10, yy, ln, font(False, 10), (60, 60, 60))
            yy += 11
    yy += 2
    text(d, dx0 + 10, yy, "NOT YET \u2014 had not happened:", font(True, 11), INK)
    yy += 12
    for item in NOT_YET:
        text(d, dx0 + 10, yy, "\u2022  " + item, font(False, 10), (60, 60, 60))
        yy += 11
    # footer
    center(d, 512, 1004, "Every story first reported Friday 20 November 2026  \u2022  Sources beside each story",
           font(False, 11), GREY)

def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_strip(d)
    draw_banner(d)
    draw_tiles(d)
    draw_list(d)
    draw_bottom(d)
    return img

if __name__ == "__main__":
    out = os.path.join(BASE, "entry.png")
    render().save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")
