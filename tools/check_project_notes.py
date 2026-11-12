"""Periksa konsistensi catatan aktif dan batas checkpoint publik MarioKan."""

from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def main():
    failures = []

    def check(name, condition):
        print(f"{'PASS' if condition else 'FAIL'}: {name}")
        if not condition:
            failures.append(name)

    def read(relative):
        return (ROOT / relative).read_text(encoding="utf-8")

    readme = read("README.md")
    prd = read("docs/PRD.md")
    contributing = read("CONTRIBUTING.md")
    state = read("CHECKPOINTS.md").split("## Change Log", 1)[0]
    check("PRD mencatat tanggal pembaruan", re.search(r"\*\*Diperbarui:\*\* \d{4}-\d{2}-\d{2}", prd) is not None)
    check("PRD tidak memakai status discovery lama", "menunggu review pemilik + 3 dokumen eksternal" not in prd)
    check("kontribusi menyebut public, bukan private", "publik" in contributing and "repo ini **private**" not in contributing)
    check("tidak menjanjikan agent melihat hasil fisik sendiri", "Agent bisa flash & membaca hasil sendiri" not in prd)
    check("toleransi monitor tidak dijamin universal", "monitors actually accept" not in readme and "jauh di bawah toleransi 0,5%" not in prd)
    check("dua jalur dan reset tetap terkunci", all(token in prd for token in ("D-13", "D-14", "D-15", "D-16", "sw[0] = 1", "sw[0] = 0")))
    check("bukti diagnostik pada README", all(token in readme for token in ("tb_input_probe", "+2.068 ns", "+0.128 ns", "not programmed")))
    check("PRD memisahkan diagnostik dari game", "tb_input_probe" in prd and "input_probe_top" in prd)
    check("state tidak lagi meminta checkpoint yang sudah diizinkan", "Tawarkan checkpoint publik `stable-2026-11-12-v2`" not in state)
    check("state mempertahankan BOARD belum dites", "BOARD input/video/game belum dites" in state)

    academic = ROOT / "docs/proposal/proyek-2"
    if academic.is_dir():
        diagram = read("docs/proposal/proyek-2/CATATAN_DIAGRAM.md")
        technical = read("docs/proposal/proyek-2/RANCANGAN_TEKNIS.md")
        review = read("docs/proposal/proyek-2/REVIEW_MODUL.md")
        check("catatan diagram mengakui ekspor dan QA", "Ekspor SVG/PNG untuk README dan laporan belum dibuat" not in diagram and "drawio-export.json" in diagram)
        check("rancangan menunjuk rubrik baru", "../../brief/proyek-2.pdf" in technical and "`Proyek 2.pdf` di root" not in technical)
        check("rancangan memisahkan bukti diagnostik terbaru", "tb_input_probe" in technical and "input_probe_top" in technical)
        check("review awal diberi status historis", "Arsip review awal" in review and "REVIEW.md" in review)
    else:
        print("SKIP: catatan akademik lokal tidak tersedia pada checkout ini")

    private_paths = ["docs/proposal/proyek-2/NASKAH_P2.md", "docs/brief/proyek-2.pdf",
                     "docs/rubrik.md", "tools/make_proposal.py",
                     ".tmp/diagnostics/input_probe_core.vhd", "reference/probe.txt",
                     "docs/diagram/architecture-v2.json", "docs/diagram/arsitektur-draft.png",
                     "docs/diagram/arsitektur-draft.svg", "tools/make_architecture_v2.py",
                     "tools/tests/test_architecture_v2.py"]
    for path in private_paths:
        result = subprocess.run(["git", "check-ignore", "--quiet", "--", path], cwd=ROOT, check=False)
        check("lokal-only " + path, result.returncode == 0)
    tracked = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout.decode("utf-8").split("\0")
    forbidden = [path for path in tracked if path.startswith(("docs/proposal/", "docs/brief/", ".tmp/", "reference/"))
                 or path in private_paths or path.lower().endswith((".docx", ".pdf", ".bit", ".zip"))]
    check("index/repo tidak memuat materi lokal-only", not forbidden)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
