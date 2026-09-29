#!/usr/bin/env python3
"""Gera os arquivos SVG das peças ilustrativas da landing page.

Uso (na raiz do projeto):
    python3 tools/render-parts.py

As imagens são ilustrações criadas para o site. Elas representam tipos de
peça, não produtos do estoque da loja. O script escreve um SVG por peça em
tools/parts/. A conversão para imagem é feita por tools/render-parts.js, que
abre cada SVG no Chromium (Playwright).
"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tools" / "parts"

W, H = 900, 640
BACKGROUND = "#eef1f5"   # mesma cor do cartão na página
RED = "#c00919"          # vermelho do logo
NAVY = "#03194b"         # azul do logo

DEFS = """
    <radialGradient id="steel" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#9aa1a9"/>
      <stop offset=".5" stop-color="#b9c0c7"/>
      <stop offset=".8" stop-color="#e3e7eb"/>
      <stop offset=".96" stop-color="#aeb5bd"/>
      <stop offset="1" stop-color="#7c848d"/>
    </radialGradient>
    <linearGradient id="steelUp" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#eef1f4"/>
      <stop offset=".5" stop-color="#aab1b9"/>
      <stop offset="1" stop-color="#5b636c"/>
    </linearGradient>
    <linearGradient id="steelDown" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#5b636c"/>
      <stop offset=".5" stop-color="#9aa1a9"/>
      <stop offset="1" stop-color="#dfe3e7"/>
    </linearGradient>
    <linearGradient id="cylinder" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#6a7179"/>
      <stop offset=".14" stop-color="#bfc5cc"/>
      <stop offset=".36" stop-color="#f4f6f8"/>
      <stop offset=".62" stop-color="#c3c9cf"/>
      <stop offset=".88" stop-color="#858c94"/>
      <stop offset="1" stop-color="#565d65"/>
    </linearGradient>
    <linearGradient id="chrome" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#7d858e"/>
      <stop offset=".3" stop-color="#ffffff"/>
      <stop offset=".55" stop-color="#c9cfd5"/>
      <stop offset="1" stop-color="#5f676f"/>
    </linearGradient>
    <linearGradient id="red" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#e6222f"/>
      <stop offset=".55" stop-color="#c00919"/>
      <stop offset="1" stop-color="#8a0612"/>
    </linearGradient>
    <linearGradient id="navyBody" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#020f30"/>
      <stop offset=".3" stop-color="#1d3f96"/>
      <stop offset=".55" stop-color="#0a2260"/>
      <stop offset="1" stop-color="#010a22"/>
    </linearGradient>
    <filter id="blur4" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="4"/></filter>
    <filter id="blur10" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="10"/></filter>
    <filter id="blur18" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="18"/></filter>
    <filter id="floor" x="-30%" y="-400%" width="160%" height="900%"><feGaussianBlur stdDeviation="16"/></filter>
    <filter id="contact" x="-30%" y="-400%" width="160%" height="900%"><feGaussianBlur stdDeviation="5"/></filter>
"""


def polar(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def fmt(*values):
    return " ".join(f"{v:.1f}" for v in values)


def sector(cx, cy, r_in, r_out, start, end):
    """Setor de anel entre dois ângulos, em graus (0 aponta para a direita)."""
    large = 1 if (end - start) % 360 > 180 else 0
    x1, y1 = polar(cx, cy, r_out, start)
    x2, y2 = polar(cx, cy, r_out, end)
    x3, y3 = polar(cx, cy, r_in, end)
    x4, y4 = polar(cx, cy, r_in, start)
    return (
        f"M{fmt(x1, y1)} A{r_out},{r_out} 0 {large} 1 {fmt(x2, y2)} "
        f"L{fmt(x3, y3)} A{r_in},{r_in} 0 {large} 0 {fmt(x4, y4)} Z"
    )


def wedge(cx, cy, r, start, end):
    x1, y1 = polar(cx, cy, r, start)
    x2, y2 = polar(cx, cy, r, end)
    return f"M{cx},{cy} L{fmt(x1, y1)} A{r},{r} 0 0 1 {fmt(x2, y2)} Z"


def sheen(cx, cy, r, clip):
    """Reflexos em leque, como em metal escovado em círculo."""
    return f"""<g clip-path="url(#{clip})">
      <path d="{wedge(cx, cy, r + 40, -62, -28)}" fill="#fff" opacity=".62" filter="url(#blur18)"/>
      <path d="{wedge(cx, cy, r + 40, 118, 152)}" fill="#fff" opacity=".5" filter="url(#blur18)"/>
      <path d="{wedge(cx, cy, r + 40, 28, 70)}" fill="#1b2026" opacity=".26" filter="url(#blur18)"/>
      <path d="{wedge(cx, cy, r + 40, 208, 250)}" fill="#1b2026" opacity=".22" filter="url(#blur18)"/>
    </g>"""


def floor_shadow(cx, y, rx):
    return (
        f'<ellipse cx="{cx}" cy="{y}" rx="{rx}" ry="22" fill="#0d1526" opacity=".22" filter="url(#floor)"/>'
        f'<ellipse cx="{cx}" cy="{y - 6}" rx="{rx * 0.72:.0f}" ry="7" fill="#0d1526" opacity=".24" filter="url(#contact)"/>'
    )


def page(body, extra_defs="", background=True):
    rect = f'<rect width="{W}" height="{H}" fill="{BACKGROUND}"/>' if background else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>{DEFS}{extra_defs}</defs>
  {rect}
  {body}
</svg>
"""


# --- Disco de freio ---------------------------------------------------------


def brake_disc(background=True):
    cx, cy, r = 430, 296, 236
    holes = []
    for k in range(12):
        base = k * 30
        for radius, offset in ((146, 0), (176, 9), (206, 18)):
            x, y = polar(cx, cy, radius, base + offset)
            holes.append(
                f'<circle cx="{x + 1.4:.1f}" cy="{y + 1.4:.1f}" r="7" fill="#fff" opacity=".7"/>'
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.6" fill="#23272c"/>'
            )
    grooves = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#000" stroke-opacity=".045" stroke-width="1.2"/>'
        for radius in range(132, 232, 7)
    )
    bolts = []
    for k in range(5):
        x, y = polar(cx, cy, 64, -90 + k * 72)
        bolts.append(
            f'<circle cx="{x + 1.5:.1f}" cy="{y + 1.5:.1f}" r="12.5" fill="#fff" opacity=".55"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="#17191c"/>'
        )
    caliper = sector(cx, cy, 120, 262, -40, 40)
    window = sector(cx, cy, 168, 222, -17, 17)
    caliper_bolts = []
    for deg in (-30, 30):
        x, y = polar(cx, cy, 196, deg)
        caliper_bolts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="url(#steelUp)" stroke="#4d0509" stroke-width="2"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#3a3f45"/>'
        )
    body = f"""
  {floor_shadow(cx + 10, 578, 250)}
  <circle cx="{cx + 8}" cy="{cy + 10}" r="{r}" fill="#343a41"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#steel)"/>
  {sheen(cx, cy, r, "ring")}
  {grooves}
  {"".join(holes)}
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#6d757e" stroke-width="2"/>

  <!-- cubo -->
  <circle cx="{cx + 3}" cy="{cy + 4}" r="122" fill="#1b1f24" opacity=".45" filter="url(#blur4)"/>
  <circle cx="{cx}" cy="{cy}" r="120" fill="url(#steelUp)"/>
  <circle cx="{cx}" cy="{cy}" r="120" fill="none" stroke="#565e67" stroke-width="2"/>
  <circle cx="{cx}" cy="{cy}" r="96" fill="url(#steelDown)"/>
  <circle cx="{cx}" cy="{cy}" r="90" fill="url(#steelUp)"/>
  {"".join(bolts)}
  <circle cx="{cx}" cy="{cy}" r="36" fill="#8d959e"/>
  <circle cx="{cx}" cy="{cy}" r="31" fill="#121416"/>

  <!-- pinça -->
  <g clip-path="url(#discClip)"><path d="{caliper}" transform="translate(-9 9)" fill="#000" opacity=".4" filter="url(#blur10)"/></g>
  <path d="{caliper}" fill="url(#red)" stroke="#6f0610" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="{window}" fill="#5c040c"/>
  <path d="{sector(cx, cy, 250, 258, -36, 36)}" fill="#fff" opacity=".4" filter="url(#blur4)"/>
  <path d="{sector(cx, cy, 124, 132, -36, 36)}" fill="#000" opacity=".3" filter="url(#blur4)"/>
  {"".join(caliper_bolts)}
"""
    defs = f"""
    <clipPath id="ring"><path clip-rule="evenodd" d="M{cx - r},{cy} a{r},{r} 0 1 0 {2 * r},0 a{r},{r} 0 1 0 {-2 * r},0 Z M{cx - 120},{cy} a120,120 0 1 0 240,0 a120,120 0 1 0 -240,0 Z"/></clipPath>
    <clipPath id="discClip"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>
"""
    return page(body, defs, background)


# --- Amortecedor com mola ---------------------------------------------------


def coil(y_top, y_bottom, turns, rx, ry):
    """Devolve os trechos de trás e da frente de uma mola helicoidal."""
    pitch = (y_bottom - y_top) / turns
    back, front = [], []
    steps = 28
    for i in range(turns):
        for half, bucket in ((0, front), (1, back)):
            points = []
            for s in range(steps + 1):
                t = math.pi * (half + s / steps)
                x = rx * math.cos(t)
                y = y_top + pitch * (i + t / (2 * math.pi)) + ry * math.sin(t)
                points.append(f"{x:.1f},{y:.1f}")
            bucket.append("M" + " L".join(points))
    return back, front


def shock_absorber():
    back, front = coil(-196, 44, 6, 68, 15)
    back_paths = "".join(
        f'<path d="{d}" fill="none" stroke="#5c040c" stroke-width="20" stroke-linecap="round"/>' for d in back
    )
    front_paths = "".join(
        f'<path d="{d}" fill="none" stroke="#8a0612" stroke-width="21" stroke-linecap="round"/>'
        f'<path d="{d}" fill="none" stroke="#c9101f" stroke-width="16" stroke-linecap="round" transform="translate(0 -1.5)"/>'
        f'<path d="{d}" fill="none" stroke="#ff7a83" stroke-width="4.5" stroke-linecap="round" opacity=".85" transform="translate(0 -6)"/>'
        for d in front
    )
    body = f"""
  {floor_shadow(450, 590, 230)}
  <g transform="translate(452 306) rotate(-34)">
    <!-- olhal de cima e haste -->
    <circle cx="0" cy="-250" r="30" fill="url(#steelUp)" stroke="#4f5760" stroke-width="2"/>
    <circle cx="0" cy="-250" r="13" fill="#15171a"/>
    <rect x="-10" y="-226" width="20" height="210" fill="url(#chrome)"/>

    {back_paths}

    <!-- prato de cima -->
    <rect x="-84" y="-214" width="168" height="18" rx="9" fill="url(#cylinder)" stroke="#4f5760" stroke-width="1.5"/>

    <!-- corpo -->
    <rect x="-36" y="-34" width="72" height="262" rx="10" fill="url(#navyBody)"/>
    <rect x="-36" y="-34" width="72" height="22" rx="8" fill="url(#cylinder)"/>
    <rect x="-20" y="-6" width="5" height="224" rx="2.5" fill="#fff" opacity=".28"/>

    <!-- prato de baixo -->
    <rect x="-86" y="44" width="172" height="18" rx="9" fill="url(#cylinder)" stroke="#4f5760" stroke-width="1.5"/>

    {front_paths}

    <!-- olhal de baixo -->
    <circle cx="0" cy="246" r="34" fill="url(#steelUp)" stroke="#4f5760" stroke-width="2"/>
    <circle cx="0" cy="246" r="21" fill="url(#steelDown)"/>
    <circle cx="0" cy="246" r="13" fill="#15171a"/>
  </g>
"""
    return page(body)


# --- Pistão e biela ---------------------------------------------------------


def piston():
    rings = "".join(
        f'<path d="M-120,{y} A120,15 0 0 0 120,{y}" fill="none" stroke="#24282d" stroke-width="7"/>'
        f'<path d="M-120,{y + 5} A120,15 0 0 0 120,{y + 5}" fill="none" stroke="#fff" stroke-width="1.6" opacity=".7"/>'
        for y in (-220, -200, -180)
    )
    body = f"""
  {floor_shadow(450, 592, 210)}
  <g transform="translate(452 322) rotate(-17) scale(.96)">
    <!-- biela -->
    <path d="M-24,-74 L24,-74 L32,112 L-32,112 Z" fill="url(#cylinder)" stroke="#4f5760" stroke-width="1.5"/>
    <path d="M-10,-50 L10,-50 L15,100 L-15,100 Z" fill="#6f767e" opacity=".75"/>
    <path d="M-7,-46 L-3,-46 L-7,98 L-12,98 Z" fill="#fff" opacity=".35"/>

    <!-- cabeça da biela -->
    <rect x="-88" y="120" width="26" height="92" rx="5" fill="url(#cylinder)" stroke="#4f5760" stroke-width="1.5"/>
    <rect x="62" y="120" width="26" height="92" rx="5" fill="url(#cylinder)" stroke="#4f5760" stroke-width="1.5"/>
    <circle cx="0" cy="168" r="74" fill="url(#steelUp)" stroke="#4f5760" stroke-width="2"/>
    <circle cx="0" cy="168" r="50" fill="url(#steelDown)"/>
    <circle cx="0" cy="168" r="43" fill="#121416"/>
    <path d="M-74,168 H-50 M50,168 H74" stroke="#3b4148" stroke-width="2.5"/>
    <rect x="-92" y="206" width="34" height="16" rx="3" fill="url(#steelUp)" stroke="#4f5760" stroke-width="1.5"/>
    <rect x="58" y="206" width="34" height="16" rx="3" fill="url(#steelUp)" stroke="#4f5760" stroke-width="1.5"/>

    <!-- pistão -->
    <path d="M-120,-244 V-58 A120,15 0 0 0 120,-58 V-244 Z" fill="url(#cylinder)"/>
    <path d="M-92,-48 V-62 Q-92,-76 -70,-76 H70 Q92,-76 92,-62 V-48 A120,15 0 0 1 -92,-48 Z" fill="#2a2e33"/>
    <path d="M-92,-62 Q-92,-76 -70,-76 H70 Q92,-76 92,-62" fill="none" stroke="#fff" stroke-width="2" opacity=".5"/>
    {rings}
    <ellipse cx="0" cy="-244" rx="120" ry="15" fill="#e9ecef" stroke="#8a9199" stroke-width="1.5"/>
    <ellipse cx="0" cy="-244" rx="78" ry="9" fill="#cfd4d9"/>
    <ellipse cx="-10" cy="-246" rx="40" ry="4" fill="#fff" opacity=".7"/>

    <!-- pino -->
    <circle cx="2" cy="-126" r="36" fill="#1b1f24" opacity=".3" filter="url(#blur4)"/>
    <circle cx="0" cy="-128" r="33" fill="url(#steelDown)" stroke="#5b636c" stroke-width="1.5"/>
    <circle cx="0" cy="-128" r="23" fill="url(#steelUp)"/>
    <circle cx="0" cy="-128" r="23" fill="none" stroke="#3b4148" stroke-width="2"/>
    <circle cx="0" cy="-128" r="9" fill="#1a1d20"/>
  </g>
"""
    return page(body)


# --- Engrenagens ------------------------------------------------------------


def gear_path(cx, cy, teeth, root, outer, phase=0.0):
    pitch = 360 / teeth
    parts = []
    for i in range(teeth):
        center = phase + i * pitch
        a = polar(cx, cy, root, center - 0.30 * pitch)
        b = polar(cx, cy, outer, center - 0.15 * pitch)
        c = polar(cx, cy, outer, center + 0.15 * pitch)
        d = polar(cx, cy, root, center + 0.30 * pitch)
        e = polar(cx, cy, root, center + 0.70 * pitch)
        start = "M" if i == 0 else "L"
        parts.append(
            f"{start}{fmt(*a)} L{fmt(*b)} A{outer},{outer} 0 0 1 {fmt(*c)} "
            f"L{fmt(*d)} A{root},{root} 0 0 1 {fmt(*e)}"
        )
    return " ".join(parts) + " Z"


def gear(cx, cy, teeth, root, outer, phase, holes, clip):
    path = gear_path(cx, cy, teeth, root, outer, phase)
    hub = root * 0.36
    bore = root * 0.17
    lightening = ""
    if holes:
        radius = root * 0.62
        size = root * 0.15
        for k in range(holes):
            x, y = polar(cx, cy, radius, phase + k * 360 / holes)
            lightening += (
                f'<circle cx="{x + 2:.1f}" cy="{y + 2:.1f}" r="{size + 1:.1f}" fill="#fff" opacity=".6"/>'
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size:.1f}" fill="#1c2024"/>'
            )
    return f"""
  <path d="{path}" transform="translate(8 10)" fill="#2f353b"/>
  <path d="{path}" fill="url(#steel)" stroke="#5b636c" stroke-width="1.5" stroke-linejoin="round"/>
  <clipPath id="{clip}"><path d="{path}"/></clipPath>
  {sheen(cx, cy, outer, clip)}
  <circle cx="{cx}" cy="{cy}" r="{root - 14:.1f}" fill="url(#steelDown)" opacity=".9"/>
  <circle cx="{cx}" cy="{cy}" r="{root - 22:.1f}" fill="url(#steelUp)"/>
  {lightening}
  <circle cx="{cx + 2}" cy="{cy + 3}" r="{hub + 3:.1f}" fill="#1b1f24" opacity=".4" filter="url(#blur4)"/>
  <circle cx="{cx}" cy="{cy}" r="{hub:.1f}" fill="url(#steelUp)" stroke="#5b636c" stroke-width="1.5"/>
  <circle cx="{cx}" cy="{cy}" r="{hub - 9:.1f}" fill="url(#steelDown)"/>
  <circle cx="{cx}" cy="{cy}" r="{bore:.1f}" fill="#121416"/>
  <rect x="{cx - bore * 0.32:.1f}" y="{cy - bore * 1.35:.1f}" width="{bore * 0.64:.1f}" height="{bore * 0.7:.1f}" fill="#121416"/>
"""


def gears():
    big = gear(356, 336, 24, 168, 204, 0, 6, "gearA")
    # a engrenagem menor fica encaixada na maior, meio dente defasada
    distance = 186 + 93
    sx, sy = polar(356, 336, distance, -38)
    small = gear(round(sx), round(sy), 12, 76, 112, -38 + 180 + 15, 0, "gearB")
    body = f"""
  {floor_shadow(440, 592, 270)}
  {small}
  {big}
"""
    return page(body)


# --- Bateria ----------------------------------------------------------------


def battery():
    caps = "".join(
        f'<ellipse cx="{x}" cy="196" rx="21" ry="6.5" fill="#0b0e14" stroke="#3b455c" stroke-width="1.5"/>'
        f'<ellipse cx="{x}" cy="194.5" rx="13" ry="3.6" fill="#1b2130"/>'
        for x in range(345, 560, 42)
    )
    ribs = "".join(
        f'<rect x="{x}" y="438" width="6" height="92" rx="3" fill="#000" opacity=".28"/>'
        for x in range(244, 660, 26)
    )

    def terminal(x, color, sign):
        mark = (
            '<path d="M-9,0 H9 M0,-9 V9" stroke="#fff" stroke-width="4" stroke-linecap="round"/>'
            if sign == "+"
            else '<path d="M-9,0 H9" stroke="#fff" stroke-width="4" stroke-linecap="round"/>'
        )
        return f"""
    <ellipse cx="{x}" cy="186" rx="34" ry="10" fill="{color}"/>
    <rect x="{x - 21}" y="148" width="42" height="38" fill="url(#cylinder)"/>
    <ellipse cx="{x}" cy="186" rx="21" ry="6.5" fill="#6f767e"/>
    <ellipse cx="{x}" cy="148" rx="21" ry="6.5" fill="#eef1f4" stroke="#8a9199" stroke-width="1.2"/>
    <g transform="translate({x} 238)">{mark}</g>"""

    body = f"""
  {floor_shadow(450, 590, 280)}
  <!-- alça -->
  <path d="M338,178 C338,96 562,96 562,178" fill="none" stroke="#05070b" stroke-width="15" stroke-linecap="round"/>
  <path d="M338,176 C338,98 562,98 562,176" fill="none" stroke="#3b455c" stroke-width="3" stroke-linecap="round" opacity=".8"/>

  <!-- caixa -->
  <rect x="222" y="252" width="456" height="292" rx="16" fill="url(#batteryBody)"/>
  <rect x="222" y="252" width="456" height="292" rx="16" fill="url(#batterySide)"/>
  {ribs}

  <!-- tampa -->
  <path d="M258,166 H642 L676,216 H224 Z" fill="url(#batteryTop)"/>
  <rect x="212" y="214" width="476" height="54" rx="12" fill="url(#batteryLid)"/>
  <rect x="212" y="214" width="476" height="7" rx="3.5" fill="#fff" opacity=".2"/>
  {caps}
  {terminal(296, RED, "+")}
  {terminal(604, "#0a1224", "-")}

  <!-- faixa -->
  <rect x="222" y="300" width="456" height="112" fill="url(#red)"/>
  <rect x="222" y="300" width="456" height="3" fill="#fff" opacity=".35"/>
  <path d="M462,318 L420,364 H446 L434,396 L482,346 H455 Z" fill="#fff"/>

  <!-- reflexo -->
  <rect x="246" y="262" width="26" height="270" rx="13" fill="#fff" opacity=".1"/>
"""
    defs = """
    <linearGradient id="batteryBody" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1a2234"/>
      <stop offset="1" stop-color="#090c14"/>
    </linearGradient>
    <linearGradient id="batterySide" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#000" stop-opacity=".45"/>
      <stop offset=".12" stop-color="#000" stop-opacity="0"/>
      <stop offset=".88" stop-color="#000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000" stop-opacity=".55"/>
    </linearGradient>
    <linearGradient id="batteryTop" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2c364c"/>
      <stop offset="1" stop-color="#1b2234"/>
    </linearGradient>
    <linearGradient id="batteryLid" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2b3449"/>
      <stop offset="1" stop-color="#111624"/>
    </linearGradient>
"""
    return page(body, defs)


# --- Calota -----------------------------------------------------------------


def window_path(cx, cy, r_in, r_out, start, end, round_in, round_out):
    """Abertura entre dois raios, mais estreita perto do centro."""
    x1, y1 = polar(cx, cy, r_out, start + round_out)
    x2, y2 = polar(cx, cy, r_out, end - round_out)
    x3, y3 = polar(cx, cy, r_in, end - round_in)
    x4, y4 = polar(cx, cy, r_in, start + round_in)
    c1 = polar(cx, cy, r_out + 4, end)
    c2 = polar(cx, cy, r_in - 4, end - round_in * 0.4)
    c3 = polar(cx, cy, r_in - 4, start + round_in * 0.4)
    c4 = polar(cx, cy, r_out + 4, start)
    return (
        f"M{fmt(x1, y1)} A{r_out},{r_out} 0 0 1 {fmt(x2, y2)} "
        f"Q{fmt(*c1)} {fmt(*polar(cx, cy, r_out - 22, end - 3))} "
        f"L{fmt(*polar(cx, cy, r_in + 18, end - round_in + 4))} Q{fmt(*c2)} {fmt(x3, y3)} "
        f"A{r_in},{r_in} 0 0 0 {fmt(x4, y4)} "
        f"Q{fmt(*c3)} {fmt(*polar(cx, cy, r_in + 18, start + round_in - 4))} "
        f"L{fmt(*polar(cx, cy, r_out - 22, start + 3))} Q{fmt(*c4)} {fmt(x1, y1)} Z"
    )


def hubcap():
    cx, cy, r = 450, 296, 238
    windows = ""
    for k in range(7):
        start = -90 + k * 360 / 7 + 9
        end = start + 360 / 7 - 18
        d = window_path(cx, cy, 96, 206, start, end, 9, 5)
        windows += (
            f'<path d="{d}" transform="translate(3 4)" fill="#fff" opacity=".8"/>'
            f'<path d="{d}" fill="url(#hubcapDark)"/>'
            f'<path d="{d}" fill="none" stroke="#000" stroke-opacity=".35" stroke-width="2"/>'
        )
    nuts = ""
    for k in range(5):
        x, y = polar(cx, cy, 44, -90 + k * 72)
        nuts += (
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="url(#steelDown)" stroke="#5b636c" stroke-width="1.2"/>'
        )
    body = f"""
  {floor_shadow(cx + 6, 580, 250)}
  <circle cx="{cx + 7}" cy="{cy + 9}" r="{r}" fill="#343a41"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#steel)"/>
  <clipPath id="capClip"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>
  {sheen(cx, cy, r, "capClip")}
  <circle cx="{cx}" cy="{cy}" r="{r - 3}" fill="none" stroke="#fff" stroke-width="3" opacity=".7"/>
  <circle cx="{cx}" cy="{cy}" r="{r - 20}" fill="none" stroke="#000" stroke-opacity=".16" stroke-width="3"/>
  <circle cx="{cx}" cy="{cy}" r="{r - 23}" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="1.5"/>
  {windows}
  <circle cx="{cx + 2}" cy="{cy + 3}" r="80" fill="#1b1f24" opacity=".35" filter="url(#blur4)"/>
  <circle cx="{cx}" cy="{cy}" r="78" fill="url(#steelUp)" stroke="#6d757e" stroke-width="1.5"/>
  <circle cx="{cx}" cy="{cy}" r="62" fill="url(#steelDown)"/>
  <circle cx="{cx}" cy="{cy}" r="58" fill="url(#steelUp)"/>
  {nuts}
  <circle cx="{cx}" cy="{cy}" r="24" fill="url(#steelDown)" stroke="#6d757e" stroke-width="1.2"/>
  <circle cx="{cx}" cy="{cy}" r="19" fill="url(#steelUp)"/>
"""
    defs = """
    <linearGradient id="hubcapDark" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0f1215"/>
      <stop offset="1" stop-color="#31363c"/>
    </linearGradient>
"""
    return page(body, defs)


PARTS = {
    "peca-disco-de-freio": brake_disc,
    "peca-amortecedor": shock_absorber,
    "peca-pistao": piston,
    "peca-engrenagens": gears,
    "peca-bateria": battery,
    "peca-calota": hubcap,
}


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in PARTS.items():
        (OUT / f"{name}.svg").write_text(build(), encoding="utf-8")
        print(f"{name}.svg")
    # versão sem fundo do disco de freio, usada sobre a foto do hero
    (OUT / "peca-disco-de-freio-sem-fundo.svg").write_text(brake_disc(background=False), encoding="utf-8")
    print("peca-disco-de-freio-sem-fundo.svg")
