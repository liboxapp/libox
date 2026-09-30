"""Tests del hook SessionStart de estado del OS. Python 3.9+."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import session_status as s  # noqa: E402


class StatusLines(unittest.TestCase):
    def test_tres_lineas_mas_titulo(self):
        lines = s.status_lines("main", True, True)
        self.assertEqual(len(lines), 4)
        self.assertTrue(lines[0].startswith("## "))

    def test_reporta_rama(self):
        self.assertIn("chore/os-ia", s.status_lines("chore/os-ia", True, True)[1])

    def test_reporta_freeze(self):
        self.assertIn("congelado hasta D1", s.status_lines("main", True, True)[2])
        self.assertIn("verificar el doc 20", s.status_lines("main", False, True)[2])

    def test_reporta_verify(self):
        self.assertIn("sin fallos", s.status_lines("main", True, True)[3])
        self.assertIn("CON FALLOS", s.status_lines("main", True, False)[3])

    def test_reporta_verify_no_disponible(self):
        self.assertIn("no se pudo ejecutar", s.status_lines("main", True, None)[3])


if __name__ == "__main__":
    unittest.main()
