"""Tests de corpus_check: ejecución real de verify_corpus.py en un repo falso. Python 3.9+."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import corpus_check as cc  # noqa: E402

OK_SCRIPT = 'print("RESULTADO: sin fallos, 0 avisos.")\nraise SystemExit(0)\n'
FAIL_SCRIPT = (
    'for i in range(15):\n'
    '    print("linea de ruido {}".format(i))\n'
    'print("RESULTADO: 2 fallos")\n'
    'raise SystemExit(1)\n'
)


def fake_root(tmp, script_src=None):
    """Crea un root con docs/linea-base/ y, si se pide, un verify_corpus.py falso."""
    os.makedirs(os.path.join(tmp, "docs", "linea-base"))
    if script_src is not None:
        with open(os.path.join(tmp, "verify_corpus.py"), "w") as fh:
            fh.write(script_src)
    return tmp


class VerifyCorpus(unittest.TestCase):
    def test_ok_cuando_exit_0_y_sin_fallos(self):
        with tempfile.TemporaryDirectory() as tmp:
            ok, tail = cc.verify_corpus(fake_root(tmp, OK_SCRIPT))
            self.assertTrue(ok)
            self.assertIn("sin fallos", tail)

    def test_falla_cuando_exit_1_con_fallos(self):
        with tempfile.TemporaryDirectory() as tmp:
            ok, tail = cc.verify_corpus(fake_root(tmp, FAIL_SCRIPT))
            self.assertIs(ok, False)
            self.assertIn("2 fallos", tail)
            self.assertLessEqual(len(tail.splitlines()), 12)

    def test_lanza_si_el_script_no_existe(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(cc.CorpusCheckUnavailable):
                cc.verify_corpus(fake_root(tmp))


if __name__ == "__main__":
    unittest.main()
