"""Generate diagram blok sistem MarioKan (PNG) untuk proposal.

Gambar disimpan ke docs/proposal/gambar/diagram-blok.png
Dijalankan: python tools/make_diagram.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2200, 1140
BG = "#FFFFFF"
INK = "#111827"
MUTED = "#6B7280"
C_INPUT = "#EFF6FF"
C_PROC = "#F0FDF4"
C_OUT = "#FEF3C7"
C_CLK = "#EDE9FE"
B_INPUT = "#1D4ED8"
B_PROC = "#15803D"
B_OUT = "#B45309"
B_CLK = "#6D28D9"


def fnt(size, bold=False):
    path = r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"
    return ImageFont.truetype(path, size)


def text_block(d, cx, y, lines, size=21, bold_first=False, color=INK, gap=5):
    """Tulis beberapa baris teks terpusat horizontal pada cx, mulai y."""
    for i, ln in enumerate(lines):
        f = fnt(size, bold=(bold_first and i == 0))
        bb = d.textbbox((0, 0), ln, font=f)
        w = bb[2] - bb[0]
        d.text((cx - w / 2, y), ln, font=f, fill=color)
        y += (bb[3] - bb[1]) + gap
    return y


def box(d, x, y, w, h, lines, fill, outline, size=21, bold_first=True, radius=14, lw=3):
    d.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill, outline=outline, width=lw)
    # hitung tinggi total teks untuk centering vertikal
    total = 0
    for i, ln in enumerate(lines):
        f = fnt(size, bold=(bold_first and i == 0))
        bb = d.textbbox((0, 0), ln, font=f)
        total += (bb[3] - bb[1]) + 5
    text_block(d, x + w / 2, y + (h - total) / 2 + 2, lines, size=size, bold_first=bold_first)


def arrow(d, x1, y1, x2, y2, color=INK, width=3, head=13):
    d.line([x1, y1, x2, y2], fill=color, width=width)
    if x1 == x2:  # vertikal
        s = 1 if y2 > y1 else -1
        d.polygon([(x2, y2), (x2 - head, y2 - s * head), (x2 + head, y2 - s * head)], fill=color)
    else:  # horizontal
        s = 1 if x2 > x1 else -1
        d.polygon([(x2, y2), (x2 - s * head, y2 - head), (x2 - s * head, y2 + head)], fill=color)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---------- clock ----------
    box(d, 560, 26, 1000, 74,
        ["clk_gen — MMCME2_BASE:  100 MHz  →  148,4375 MHz (clk_pix)  +  locked"],
        C_CLK, B_CLK, size=23)

    # ---------- header kolom ----------
    for label, cx in (("INPUT", 250), ("PROSES", 1060), ("OUTPUT", 1890)):
        f = fnt(26, bold=True)
        bb = d.textbbox((0, 0), label, font=f)
        d.text((cx - (bb[2] - bb[0]) / 2, 124), label, font=f, fill=MUTED)

    # ---------- kolom INPUT ----------
    IX, IW = 70, 360
    box(d, IX, 190, IW, 108,
        ["Keyboard USB", "(PIC24 → PS/2)", "PS2Clk C17 · PS2Data B17"],
        C_INPUT, B_INPUT, size=20)
    box(d, IX, 330, IW, 96,
        ["Mouse USB *", "(opsional, belum", "tervalidasi jalurnya)"],
        C_INPUT, B_INPUT, size=20)
    box(d, IX, 458, IW, 96,
        ["Switch SW[15:13]", "Tombol btnU", "(input cadangan demo)"],
        C_INPUT, B_INPUT, size=20)

    # bus input -> proses
    BUS = 505
    d.line([IX + IW, 244, BUS, 244], fill=B_INPUT, width=3)
    d.line([IX + IW, 378, BUS, 378], fill=B_INPUT, width=3)
    d.line([IX + IW, 506, BUS, 506], fill=B_INPUT, width=3)
    d.line([BUS, 244, BUS, 506], fill=B_INPUT, width=3)
    arrow(d, BUS, 250, 560, 250, color=B_INPUT)

    # ---------- kolom PROSES ----------
    PX, PW = 560, 1000
    box(d, PX, 190, PW, 120,
        ["TAHAP 1 — Akuisisi Input",
         "ps2_rx · kbd_decoder · ps2_tx · mouse_decoder · input_mux"],
        C_PROC, B_PROC, size=21)
    box(d, PX, 340, PW, 120,
        ["TAHAP 2 — Logika Game",
         "game_ctrl (FSM) · player · enemy_goomba · items · collision"],
        C_PROC, B_PROC, size=21)
    box(d, PX, 490, PW, 120,
        ["TAHAP 3 — Memori & Aset",
         "tilemap (BRAM) · sprite ROM · palette 4 bank · font ROM"],
        C_PROC, B_PROC, size=21)
    box(d, PX, 640, PW, 120,
        ["TAHAP 4 — Render Piksel",
         "vga_timing → scaler → renderer  (384×216 logika → ×5 → 1920×1080)"],
        C_PROC, B_PROC, size=21)

    for y in (310, 460, 610):
        arrow(d, PX + PW / 2, y, PX + PW / 2, y + 30, color=B_PROC)

    # ---------- kolom OUTPUT ----------
    OX, OW = 1660, 460
    arrow(d, PX + PW, 700, OX, 700, color=B_OUT)
    box(d, OX, 640, OW, 120,
        ["VGA RGB444", "1920 × 1080 @ 60 Hz", "Hsync · Vsync · DE"],
        C_OUT, B_OUT, size=21)
    arrow(d, OX + OW / 2, 760, OX + OW / 2, 800, color=B_OUT)
    box(d, OX, 800, OW, 96,
        ["Konverter VGA → HDMI"],
        C_OUT, B_OUT, size=21)
    arrow(d, OX + OW / 2, 896, OX + OW / 2, 936, color=B_OUT)
    box(d, OX, 936, OW, 96,
        ["TV (HDMI)"],
        C_OUT, B_OUT, size=21)

    # ---------- catatan ----------
    d.text((70, 1060), "* Mouse bergantung pada bukti jalur PS/2 terpisah; keyboard adalah jalur input utama.",
           font=fnt(19), fill=MUTED)
    d.text((70, 1090), "HUD, skor, dan nyawa juga ditampilkan pada LED dan 7-segmen (jalur debug).",
           font=fnt(19), fill=MUTED)

    out_dir = os.path.join("docs", "proposal", "gambar")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "diagram-blok.png")
    img.save(out, "PNG")
    print("tersimpan:", out, img.size)


if __name__ == "__main__":
    main()
