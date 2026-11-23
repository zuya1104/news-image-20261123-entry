#!/usr/bin/env python3
"""Render the 23 November 2026 world-news poster (1024x1024).

Deterministic: fixed layout, fixed fonts, fixed story data. No clock, no
randomness, no network. Output: entry.png next to this script.
Stories: 3 leads + 40 grid items = 43 stories, 7 regions, all verified
against live news sources on the morning of 23 Nov 2026.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 230)
INK = (22, 19, 14)
RED = (179, 39, 30)
BLUE = (29, 78, 137)
TEAL = (14, 107, 92)
GOLD = (176, 124, 0)
NAVY = (20, 38, 63)
SLATE = (55, 71, 79)
WINE = (123, 30, 59)
OCHRE = (158, 110, 20)
ORANGE = (192, 86, 33)
WHITE = (255, 255, 255)
CARD = (255, 253, 247)
MUTED = (107, 101, 88)
RULE = (196, 186, 166)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, font):
    return draw.textlength(s, font=font)


def wrap(draw, s, font, max_w):
    words = s.split(" ")
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_one(draw, s, font, max_w):
    """Single line, truncated with an ellipsis if it does not fit."""
    if text_w(draw, s, font) <= max_w:
        return s
    ell = "..."
    while s and text_w(draw, s + ell, font) > max_w:
        s = s[:-1]
    return s + ell


def center(draw, cx, y, s, font, fill):
    draw.text((cx - text_w(draw, s, font) / 2, y), s, font=font, fill=fill)


# ---------------------------------------------------------------- data
LEADS = [
    {
        "color": TEAL,
        "kicker": "CLIMATE  |  ANTALYA",
        "head": "COP31 COLLAPSES \u2014 NO DEAL ON CLIMATE",
        "stand": "EU rejects a draft that never mentions fossil fuels. The longest COP ever ends with no pact \u2014 the first failure since Copenhagen 2009.",
        "art": "cop31",
    },
    {
        "color": NAVY,
        "kicker": "WAR IN UKRAINE  |  KYIV REGION",
        "head": "DRONE FLATTENS FLATS \u2014 14 MISSING",
        "stand": "A Russian drone hits a five-storey block in Dymer. Two killed, two children among the missing. 186 drones in one night; 161 shot down.",
        "art": "kyiv",
    },
    {
        "color": RED,
        "kicker": "GULF WAR  |  BAHRAIN",
        "head": "WAR REACHES BAHRAIN \u2014 TANKERS HIT",
        "stand": "Iran strikes a Sitra industrial site; two hurt, one critical. IRGC claims US bases hit; two tankers struck in the Strait of Hormuz.",
        "art": "gulf",
    },
]

SECTIONS = [
    ("EUROPE", BLUE, [
        ("NATO meets today over Poland breach",
         "Emergency council in Brussels; \u2018every inch\u2019 defended."),
        ("Three Russian objects fell in Poland",
         "Kh-101 found; Swedish Gripen held fire in bad weather."),
        ("UK and EU agree Brexit reset deal",
         "Food trade, carbon, youth mobility; fees row open."),
        ("EU proposes \u20ac45bn loan for Ukraine",
         "Funding would cover Kyiv through 2027, leaders say."),
        ("Russian cargo ship burns off Finland",
         "Vessel still ablaze days after reported attack."),
        ("Lisbon marches over cost of living",
         "Thousands take to the streets as prices bite."),
        ("90+ nations sign electrification pledge",
         "COP31\u2019s one bright spot as the main deal dies."),
    ]),
    ("MIDDLE EAST", RED, [
        ("Iran starts rationing electricity",
         "War strains the grid; blackouts ordered from Sunday."),
        ("Tehran weighs changing nuclear doctrine",
         "FM Araqchi: the case for a shift has \u2018strong logic\u2019."),
        ("Gulf states condemn Iran strikes",
         "Saudi Arabia, Kuwait and Qatar denounce Bahrain attack."),
        ("IRGC claims US Patriot radars hit",
         "Revolutionary Guards say Al-Riffa and Awali bases struck."),
        ("Bahrain defences down Iranian targets",
         "Debris fire at industrial site; two hurt, one critical."),
        ("Hormuz shipping slumps in the war",
         "263 ships passed 12\u201318 Nov, down from ~135 a day."),
    ]),
    ("ASIA-PACIFIC", TEAL, [
        ("Trump, Xi and Putin meet in Shenzhen",
         "Trilateral declares 4 points: peace, nukes, energy, rules."),
        ("ICJ: evidence of Rohingya genocide",
         "Historic ruling finds Myanmar case proven, 19 Nov."),
        ("Nepal PM in India; talks with Modi",
         "Balendra Shah\u2019s state visit; bilateral talks today."),
        ("S. Korea minister quits in AI scandal",
         "Education chief resigns over AI-cheating affair."),
        ("Indonesia factory fire: 50 missing",
         "Seven body bags recovered; search goes on."),
        ("Myanmar calls ASEAN ruling \u2018unfair\u2019",
         "Military-backed govt rejects bloc\u2019s decision."),
    ]),
    ("AMERICAS", OCHRE, [
        ("FBI probes hack of crime database",
         "Suspected breach of the national NCIC system."),
        ("California braces for record king tide",
         "SF mayor: no non-essential travel Mon\u2013Wed."),
        ("US and Libya sign minerals deal",
         "Aviation and rare-minerals pacts agreed, 22 Nov."),
        ("Trump defends calling Putin a friend",
         "President stands by the remark, reports say."),
        ("US Embassy warns Americans in Bahrain",
         "Heightened Iranian and Houthi threats cited."),
    ]),
    ("AFRICA", ORANGE, [
        ("Ethiopia vaccinates 11m children",
         "Polio drive launched with WHO and UNICEF, 22 Nov."),
        ("Sudan army clears 10 RSF positions",
         "Offensive in West Kordofan enters second week."),
        ("Gambia intercepts 491 migrants",
         "Would-be irregular migrants stopped at sea."),
        ("AFCON: Ivory Coast snatch late draw",
         "Qualifier drama against Gambia in Banjul."),
        ("AU mourns S. Africa deputy president",
         "Mlambo-Ngcuka remembered across the continent."),
        ("Libya: Russian ship \u2018hit by UAV\u2019",
         "Tripoli claims strike at Benghazi naval base."),
    ]),
    ("TECH & CYBER", SLATE, [
        ("Patch vCenter today, CISA orders",
         "CVE-2026-123890 (9.8) exploited by China-linked group."),
        ("CISA lists 4 exploited flaws at once",
         "Cisco, Apache Roller, SAP join vCenter; all due 23 Nov."),
        ("Nvidia aide \u2018ran China chip network\u2019",
         "Alice Huang linked to secret AI-chip diversion."),
        ("VMware ESX flaw hid attacker moves",
         "WARP PANDA used logging bypass as a zero-day."),
        ("AI helps track polio in Africa",
         "Surveillance boost for vaccination campaigns."),
    ]),
    ("SPORT & CULTURE", WINE, [
        ("India smash Test record: 720/9d",
         "Wellington run-feast vs New Zealand."),
        ("Anupama keeps snooker world crown",
         "IBSF women\u2019s champion defends her title."),
        ("BRICS film chiefs meet at IFFI",
         "Roundtable backs industry partnership."),
        ("Tripoli fine-arts show opens",
         "Libya\u2019s national exhibition returns."),
        ("Washington\u2019s hair sells for $4,000",
         "A strand of the first president\u2019s hair at auction."),
    ]),
]

NUMBERS_A = [
    ("14", "people missing under the Dymer rubble"),
    ("186", "drones fired at Ukraine in one night"),
    ("90+", "nations signed the COP31 electrification pledge"),
]
NUMBERS_B = [
    ("\u20ac45bn", "EU loan proposed for Ukraine in 2027"),
    ("11m+", "children in Ethiopia\u2019s polio drive"),
    ("263", "ships through Hormuz, 12\u201318 Nov"),
]


# ---------------------------------------------------------------- art
def art_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(23, 92, 79))
    d.ellipse([x + w - 118, y - 26, x + w + 26, y + 118], fill=(244, 196, 66))
    d.ellipse([x + 26, y + 8, x + 132, y + h - 8], fill=(46, 139, 120))
    d.ellipse([x + 44, y + 22, x + 114, y + h - 22], fill=(16, 110, 94))
    for k in range(3):
        yy = y + 18 + k * 20
        d.arc([x + 30, yy - 8, x + 128, yy + 26], 200, 340, fill=(255, 255, 255), width=2)
    d.line([x + 8, y + h - 6, x + w - 8, y + 6], fill=(179, 39, 30), width=7)
    d.line([x + 8, y + 6, x + w - 8, y + h - 6], fill=(179, 39, 30), width=7)


def art_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 28, 52))
    for i in range(14):
        d.ellipse([x + 14 + i * 20, y + 6 + (i % 3) * 5, x + 34 + i * 20, y + 16 + (i % 3) * 5],
                  fill=(120, 130, 150))
    d.rectangle([x + 30, y + 34, x + 130, y + h], fill=(74, 80, 92))
    d.rectangle([x + 150, y + 52, x + 250, y + h], fill=(58, 64, 76))
    for r in range(4):
        for c in range(4):
            lit = (r + c) % 3 == 0
            d.rectangle([x + 42 + c * 22, y + 44 + r * 16, x + 56 + c * 22, y + 56 + r * 16],
                        fill=(244, 196, 66) if lit else (30, 34, 44))
    d.polygon([(x + 150, y + h), (x + 175, y + h - 34), (x + 205, y + h - 18),
               (x + 230, y + h - 40), (x + 250, y + h)], fill=(232, 116, 26))
    d.polygon([(x + 168, y + h), (x + 188, y + h - 20), (x + 212, y + h - 8), (x + 226, y + h)],
              fill=(244, 196, 66))
    d.line([x + w - 52, y + 12, x + w - 18, y + 12], fill=(10, 10, 10), width=3)
    d.line([x + w - 35, y + 4, x + w - 35, y + 20], fill=(10, 10, 10), width=3)


def art_gulf(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 44, 78))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(10, 30, 58))
    for k in range(4):
        yy = y + h - 26 + k * 8
        d.arc([x + 10 + k * 12, yy, x + 90 + k * 12, yy + 14], 180, 360, fill=(140, 180, 220), width=2)
    d.polygon([(x + 40, y + h - 34), (x + 250, y + h - 34), (x + 268, y + h - 12),
               (x + 22, y + h - 12)], fill=(12, 12, 14))
    for i, cc in enumerate([(179, 39, 30), (240, 240, 240), (29, 78, 137), (176, 124, 0)]):
        d.rectangle([x + 56 + i * 44, y + h - 62, x + 94 + i * 44, y + h - 34], fill=cc)
    cx, cy = x + 150, y + 26
    for a, b in [(0, 14), (45, 14), (90, 14), (135, 14)]:
        import math
        r1 = 10
        r2 = 26
        x1 = cx + r1 * math.cos(math.radians(a))
        y1 = cy + r1 * math.sin(math.radians(a))
        x2 = cx + r2 * math.cos(math.radians(a + 22))
        y2 = cy + r2 * math.sin(math.radians(a + 22))
        d.polygon([(cx, cy), (x1, y1), (x2, y2)], fill=(232, 116, 26))
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(244, 196, 66))


ARTS = {"cop31": art_cop31, "kyiv": art_kyiv, "gulf": art_gulf}


# ---------------------------------------------------------------- draw
def draw_lead(d, x, y, w, h, lead):
    color = lead["color"]
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=RULE, width=1)
    d.rectangle([x, y, x + w, y + 26], fill=color)
    d.text((x + 10, y + 5), lead["kicker"], font=F(SANS_B, 12), fill=WHITE)
    ay = y + 26
    ARTS[lead["art"]](d, x, ay, w, 66)
    ty = ay + 66 + 6
    head_lines = wrap(d, lead["head"], F(SERIF_B, 18), w - 20)
    for ln in head_lines[:2]:
        d.text((x + 10, ty), ln, font=F(SERIF_B, 18), fill=INK)
        ty += 22
    sy = ty + 2
    for ln in wrap(d, lead["stand"], F(SANS, 12), w - 20)[:3]:
        d.text((x + 10, sy), ln, font=F(SANS, 12), fill=(52, 48, 40))
        sy += 14


def draw_section(d, x, y, w, title, color, items):
    d.rectangle([x, y, x + w, y + 20], fill=color)
    d.text((x + 8, y + 3), title, font=F(SANS_B, 12), fill=WHITE)
    d.text((x + w - 8 - text_w(d, str(len(items)), F(SANS_B, 11)), y + 3),
           str(len(items)), font=F(SANS_B, 11), fill=WHITE)
    yy = y + 20
    for head, summ in items:
        d.text((x + 2, yy + 2), fit_one(d, head, F(SANS_B, 13), w - 4),
               font=F(SANS_B, 13), fill=INK)
        d.text((x + 2, yy + 17), fit_one(d, summ, F(SANS, 11), w - 4),
               font=F(SANS, 11), fill=(74, 68, 58))
        yy += 31
        d.line([x, yy - 1, x + w, yy - 1], fill=(226, 219, 203), width=1)
    return yy


def draw_numbers(d, x, y, w, title, items):
    d.rectangle([x, y, x + w, y + 178], fill=NAVY)
    d.text((x + 10, y + 10), title, font=F(SANS_B, 12), fill=(244, 196, 66))
    yy = y + 40
    for num, label in items:
        d.text((x + 10, yy), num, font=F(SERIF_B, 22), fill=WHITE)
        d.text((x + 82, yy + 6), fit_one(d, label, F(SANS, 11), w - 92),
               font=F(SANS, 11), fill=(205, 212, 222))
        yy += 44


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 80], fill=INK)
    center(d, W // 2, 12, "THE WORLD IN ONE DAY", F(SERIF_B, 46), WHITE)
    d.rectangle([0, 80, W, 84], fill=RED)
    d.text((10, 92), "MONDAY 23 NOVEMBER 2026", font=F(SANS_B, 14), fill=RED)
    right = "43 STORIES  \u2022  7 REGIONS  \u2022  ONE IMAGE"
    d.text((W - 10 - text_w(d, right, F(SANS_B, 14)), 92), right,
           font=F(SANS_B, 14), fill=INK)
    center(d, W // 2, 116,
           "The climate talks collapse, war reaches the Gulf \u2014 and a drone flattens a Kyiv apartment block.",
           F(SERIF_I, 15), (74, 68, 58))

    # Leads
    lx, lw, lh, gap = 10, 328, 192, 10
    for i, lead in enumerate(LEADS):
        draw_lead(d, lx + i * (lw + gap), 138, lw, lh, lead)

    # Grid: 3 columns; A = Europe + Americas, B = Middle East + Africa,
    # C = Asia-Pacific + Tech & Cyber + Sport & Culture
    cols = [
        [SECTIONS[0], SECTIONS[3]],
        [SECTIONS[1], SECTIONS[4]],
        [SECTIONS[2], SECTIONS[5], SECTIONS[6]],
    ]
    gx, gw = 10, 328
    gy = 340
    for ci, sections in enumerate(cols):
        x = gx + ci * (gw + gap)
        yy = gy
        for title, color, items in sections:
            yy = draw_section(d, x, yy, gw, title, color, items)
            yy += 6
    # Numbers boxes under columns A and B
    draw_numbers(d, gx, 772, gw, "THE DAY IN NUMBERS", NUMBERS_A)
    draw_numbers(d, gx + (gw + gap), 772, gw, "THE DAY IN NUMBERS", NUMBERS_B)

    # Footer
    d.rectangle([0, 962, W, H], fill=INK)
    center(d, W // 2, 972,
           "43 stories from every continent \u2014 verified against live reports on the morning of 23 November 2026.",
           F(SANS, 12), (220, 214, 200))
    center(d, W // 2, 992,
           "Sources: Reuters  \u2022  AFP  \u2022  RFE/RL  \u2022  CISA  \u2022  PANA  \u2022  NATO  \u2022  UN  \u2014  Compiled by an AI agent for make.fun",
           F(SANS, 11), (160, 154, 140))

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
