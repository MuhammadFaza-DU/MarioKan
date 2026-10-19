"""Generate diagram arsitektur MarioKan sebagai SVG vektor.

Kenapa SVG: diagram ASCII di README pecah di GitHub karena karakter kotak
(─ │ ┌ ┐ └ ┘) punya lebar berbeda di font monospace GitHub. SVG selalu rapi
dan tetap tajam saat di-zoom.

Output: docs/diagram/arsitektur.svg
Jalankan: python tools/make_architecture.py
"""

import os

OUT_DIR = os.path.join("docs", "diagram")
OUT = os.path.join(OUT_DIR, "arsitektur.svg")

W, H = 1200, 1040

SANS = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "'Consolas', 'Menlo', 'DejaVu Sans Mono', monospace"

INK = "#0F172A"
MUTED = "#64748B"
LINE = "#94A3B8"

# (fill, stroke)
C_CLK = ("#F8FAFC", "#475569")
C_IN = ("#EFF6FF", "#2563EB")
C_DEC = ("#E0F2FE", "#0284C7")
C_MUX = ("#F5F3FF", "#7C3AED")
C_FSM = ("#F5F3FF", "#7C3AED")
C_GAME = ("#F0FDF4", "#16A34A")
C_ASSET = ("#FEFCE8", "#CA8A04")
C_REND = ("#FDF2F8", "#DB2777")
C_OUT = ("#FFF7ED", "#EA580C")

parts = []


def add(s):
    parts.append(s)


def rect(x, y, w, h, fill, stroke, rx=10, sw=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" ry="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def txt(x, y, s, size=19, weight="600", anchor="middle", family=SANS,
        color=INK, spacing=None):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    add(f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}" '
        f'dominant-baseline="middle"{ls}>{s}</text>')


def box(x, y, w, h, colors, title, sub=None, dash=None):
    fill, stroke = colors
    rect(x, y, w, h, fill, stroke, dash=dash)
    cy = y + h / 2
    if sub:
        txt(x + w / 2, cy - 12, title, 19, family=MONO)
        txt(x + w / 2, cy + 12, sub, 13.5, weight="400", family=SANS, color=MUTED)
    else:
        txt(x + w / 2, cy, title, 19, family=MONO)


def arrow(x1, y1, x2, y2, color=LINE, sw=2.0, head=6):
    add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="{sw}" stroke-linecap="round"/>')
    if x1 == x2 and y2 > y1:
        add(f'<polygon points="{x2},{y2} {x2-head},{y2-head*1.7} {x2+head},{y2-head*1.7}" '
            f'fill="{color}"/>')
    elif y1 == y2 and x2 > x1:
        add(f'<polygon points="{x2},{y2} {x2-head*1.7},{y2-head} {x2-head*1.7},{y2+head}" '
            f'fill="{color}"/>')
    elif y1 == y2 and x2 < x1:
        add(f'<polygon points="{x2},{y2} {x2+head*1.7},{y2-head} {x2+head*1.7},{y2+head}" '
            f'fill="{color}"/>')


def elbow(x_start, y_start, y_mid, x_end, y_end, color=LINE, sw=2.0):
    """Turun, geser horizontal, lalu turun lagi."""
    add(f'<polyline points="{x_start},{y_start} {x_start},{y_mid} {x_end},{y_mid} '
        f'{x_end},{y_end}" fill="none" stroke="{color}" stroke-width="{sw}" '
        f'stroke-linecap="round" stroke-linejoin="round"/>')
    add(f'<polygon points="{x_end},{y_end} {x_end-6},{y_end-10} {x_end+6},{y_end-10}" '
        f'fill="{color}"/>')


def stage_label(y, text):
    txt(118, y, text, 12, weight="700", anchor="end", family=SANS,
        color=MUTED, spacing="1.2")


# ----------------------------------------------------------------------
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" role="img" '
    f'aria-label="MarioKan hardware architecture block diagram">')
add(f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>')

# ---- pita clock ----
rect(40, 24, 1120, 64, *C_CLK, dash="7 5")
txt(600, 46, "clk_gen  ·  MMCME2_BASE  ·  100 MHz  →  148.4375 MHz", 18, family=MONO)
txt(600, 68, "single clock domain  ·  locked → reset_sync  ·  game logic advances on a 60 Hz clock enable",
    13, weight="400", color=MUTED)

# ---- baris masukan ----
IX = [140, 500, 860]
IW = 300
box(IX[0], 132, IW, 64, C_IN, "PS/2 keyboard", "primary input path")
box(IX[1], 132, IW, 64, C_IN, "PS/2 mouse", "optional · unverified")
box(IX[2], 132, IW, 64, C_IN, "switches · buttons", "demo fallback")
stage_label(164, "INPUT")

for x in IX:
    arrow(x + IW / 2, 196, x + IW / 2, 232)

# ---- baris decoder ----
box(IX[0], 232, IW, 64, C_DEC, "ps2_rx · kbd_decoder", "scan code set 2")
box(IX[1], 232, IW, 64, C_DEC, "ps2_tx · mouse_decoder", "3-byte packets")
box(IX[2], 232, IW, 64, C_DEC, "sync 2-FF · debounce", "async inputs")
stage_label(264, "DECODE")

# ---- input_mux ----
elbow(290, 296, 316, 500, 336)
arrow(650, 296, 650, 336)
elbow(1010, 296, 316, 700, 336)
box(400, 336, 400, 64, C_MUX, "input_mux", "source select")
stage_label(368, "MUX")

arrow(600, 400, 600, 440)

# ---- game_ctrl ----
box(400, 440, 400, 72, C_FSM, "game_ctrl", "MENU · PLAY · PAUSE · DYING · CLEAR")
stage_label(476, "FSM")

arrow(600, 512, 600, 556)

# ---- gameplay ----
box(140, 556, 1020, 64, C_GAME,
    "player · enemy_goomba · items · collision · hud_text", "Q12.8 position · Q8.8 velocity")
stage_label(588, "GAMEPLAY")

arrow(600, 620, 600, 660)

# ---- aset ----
box(140, 660, 1020, 64, C_ASSET,
    "tilemap · sprite_rom · palette (4 banks) · font_rom", "BRAM · synchronous read")
stage_label(692, "ASSETS")

arrow(600, 724, 600, 764)

# ---- render ----
box(140, 764, 1020, 64, C_REND,
    "vga_timing  →  scaler  →  renderer", "384 × 216 logical  →  ×5  →  1920 × 1080")
stage_label(796, "RENDER")

arrow(600, 828, 600, 868)

# ---- keluaran ----
box(340, 868, 520, 64, C_OUT, "RGB444  →  VGA  →  HDMI  →  display", "hsync · vsync · de")
stage_label(900, "OUTPUT")

# ---- catatan ----
txt(600, 972,
    "No framebuffer: every pixel is computed as it is scanned out.",
    13.5, weight="400", color=MUTED)
txt(600, 994,
    "All video outputs are registered together to keep sync and data aligned.",
    13.5, weight="400", color=MUTED)
txt(600, 1016,
    "Mouse support depends on evidence of a separate PS/2 path; keyboard is the guaranteed input.",
    13.5, weight="400", color=MUTED)

add("</svg>")

os.makedirs(OUT_DIR, exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(parts))
print("tersimpan:", OUT)
