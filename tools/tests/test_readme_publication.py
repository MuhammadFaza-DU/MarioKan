"""Uji README publik, sumber ekspor dan tautan tanpa layanan eksternal."""

import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[2]


class ReadmePublicationTests(unittest.TestCase):
    def test_approved_diagram_has_inline_preview_and_editable_source(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"!\[[^\]]{20,}\]\(docs/diagram/arsitektur\.png\)")
        self.assertIn("](" + "docs/diagram/arsitektur.drawio)", text)

    def test_export_manifest_matches_master_and_png_bytes(self):
        manifest = ROOT / "docs/diagram/arsitektur-export.json"
        self.assertTrue(manifest.is_file(), "manifest publik ekspor belum tersedia")
        data = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual(data["source"], "docs/diagram/arsitektur.drawio")
        self.assertEqual(data["png"], "docs/diagram/arsitektur.png")
        master = (ROOT / data["source"]).read_bytes()
        png = (ROOT / data["png"]).read_bytes()
        self.assertEqual(hashlib.sha256(master).hexdigest(), data["source_sha256"])
        self.assertEqual(data["source_sha256"], "c1c43f130d9be6f1334d74d47cc885bd6fa61ba92ba441fe6c4574afc1acf18b")
        self.assertEqual(hashlib.sha256(png).hexdigest(), data["png_sha256"])
        self.assertEqual(data["png_sha256"], "5cc47969a51b2a81e5434d4c1c2c123cc7d21c9f7140d2c7e4975c9affae37e2")
        self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack("!II", png[16:24]), (3456, 2283))
        self.assertIn("https://embed.diagrams.net", data["renderer"])

    def test_readme_local_links_and_anchors_resolve(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        anchors = {re.sub(r"[^a-z0-9 -]", "", line.lstrip("# ").lower()).replace(" ", "-")
                   for line in text.splitlines() if line.startswith("#")}
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
            if target.startswith(("http:", "https:")):
                continue
            if target.startswith("#"):
                self.assertIn(target[1:], anchors, target)
            else:
                relative = target.split("#", 1)[0]
                resolved = (ROOT / relative).resolve()
                self.assertTrue(resolved.is_relative_to(ROOT.resolve()), target)
                self.assertTrue(resolved.is_file(), target)
                ignored = subprocess.run(
                    ["git", "check-ignore", "--no-index", "--quiet", "--", relative],
                    cwd=ROOT, capture_output=True, text=True, check=False,
                )
                self.assertEqual(ignored.returncode, 1, f"tautan di-ignore atau pemeriksaan Git gagal: {target}; {ignored.stderr}")
        self.assertNotIn("](#)", text)

    def test_overview_and_evidence_do_not_claim_a_playable_game(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("not implemented", text[:1200])
        for required in ("tb_input_probe", "+2.068 ns", "+0.128 ns", "not programmed", "BOARD"):
            self.assertIn(required, text)
        self.assertNotIn("\u2014", text)

    def test_readme_serves_design_progress_and_contributor_readers(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for path in ("docs/PRD.md", "docs/INPUT_GUIDE.md", "docs/ASSET_FEASIBILITY.md",
                     "docs/PORTING_NOTES.md", "CHECKPOINTS.md", "CONTRIBUTING.md"):
            self.assertIn("](" + path + ")", text)


if __name__ == "__main__":
    unittest.main()
