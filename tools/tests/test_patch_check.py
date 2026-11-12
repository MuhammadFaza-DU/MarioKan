"""Regresi hunk no-op, konteks salah dan urutan patch mundur."""

import importlib.util
from pathlib import Path
import unittest


class PatchCheckTests(unittest.TestCase):
    def setUp(self):
        script = Path(__file__).resolve().parents[1] / "check_patch.py"
        self.assertTrue(script.is_file(), "validator patch belum tersedia")
        spec = importlib.util.spec_from_file_location("patch_check", script)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def test_rejects_no_op_hunk(self):
        with self.assertRaisesRegex(ValueError, "no-op"):
            self.module.validate_hunks("first\nsecond\n", [[" first"]])

    def test_rejects_backwards_hunks(self):
        with self.assertRaisesRegex(ValueError, "order"):
            self.module.validate_hunks("first\nsecond\nthird\n",
                                       [["-third", "+THIRD"], ["-first", "+FIRST"]])

    def test_rejects_incorrect_context(self):
        with self.assertRaisesRegex(ValueError, "context"):
            self.module.validate_hunks("first\nsecond\n", [["-absent", "+new"]])

    def test_accepts_real_changes_in_source_order(self):
        self.module.validate_hunks("first\nsecond\nthird\n",
                                   [["-first", "+FIRST"], [" second", "-third", "+THIRD"]])


if __name__ == "__main__":
    unittest.main()
