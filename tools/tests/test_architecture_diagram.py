"""Periksa berkas yang benar-benar dihasilkan generator diagram."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class ArchitectureDiagramTests(unittest.TestCase):
    def test_generated_svg_uses_lf_line_endings(self):
        root = Path(__file__).resolve().parents[2]
        with tempfile.TemporaryDirectory(dir=root / ".tmp") as workdir:
            subprocess.run(
                [sys.executable, "-B", str(root / "tools/make_architecture.py")],
                cwd=workdir,
                check=True,
                capture_output=True,
            )
            output = Path(workdir, "docs/diagram/arsitektur.svg").read_bytes()
            self.assertIn(b"\n", output)
            self.assertEqual(output.count(b"\r\n"), 0, "SVG harus LF sesuai .gitattributes")


if __name__ == "__main__":
    unittest.main()
