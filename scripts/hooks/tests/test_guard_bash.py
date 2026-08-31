"""Tests del guard PreToolUse para Bash (B1–B4). Python 3.9+."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import guard_bash as g  # noqa: E402


def ctx(staged=(), changed=(), email="dev@liboxapp.com", verify=(True, "sin fallos")):
    return {
        "staged_files": lambda: list(staged),
        "changed_files": lambda: list(changed),
        "user_email": lambda: email,
        "verify_corpus": lambda: verify,
    }


class B1Coautor(unittest.TestCase):
    def test_bloquea_trailer_coauthored_by(self):
        cmd = 'git commit -m "feat: x\n\nCo-Authored-By: Claude <noreply@anthropic.com>"'
        kind, msg = g.decide(cmd, ctx())
        self.assertEqual(kind, "deny")
        self.assertIn("co-autoría", msg)

    def test_bloquea_generated_with(self):
        cmd = 'git commit -m "docs: y" -m "Generated with Claude Code"'
        self.assertEqual(g.decide(cmd, ctx())[0], "deny")

    def test_permite_commit_limpio(self):
        self.assertEqual(g.decide('git commit -m "feat: limpio"', ctx())[0], "allow")


class B2PushMain(unittest.TestCase):
    def test_bloquea_push_origin_main(self):
        self.assertEqual(g.decide("git push origin main", ctx())[0], "deny")

    def test_bloquea_push_head_main(self):
        self.assertEqual(g.decide("git push -u origin HEAD:main", ctx())[0], "deny")

    def test_bloquea_force_push_main(self):
        self.assertEqual(g.decide("git push --force-with-lease origin main", ctx())[0], "deny")

    def test_permite_push_rama(self):
        self.assertEqual(g.decide("git push -u origin chore/os-ia", ctx())[0], "allow")

    def test_permite_borrar_rama_remota(self):
        self.assertEqual(g.decide("git push --delete origin main-old", ctx())[0], "allow")


class B3VerifyCorpus(unittest.TestCase):
    def test_bloquea_commit_canon_con_fallos(self):
        c = ctx(staged=["docs/linea-base/LIBOX_PRD_BLUEPRINT_MVP_V10.md"], verify=(False, "RESULTADO: 2 fallos"))
        kind, msg = g.decide('git commit -m "docs: prd v10"', c)
        self.assertEqual(kind, "deny")
        self.assertIn("2 fallos", msg)

    def test_bloquea_commit_verify_corpus_py_con_fallos(self):
        c = ctx(staged=["verify_corpus.py"], verify=(False, "RESULTADO: 1 fallo"))
        self.assertEqual(g.decide('git commit -m "chore: baseline"', c)[0], "deny")

    def test_permite_commit_canon_sin_fallos(self):
        c = ctx(staged=["docs/linea-base/LIBOX_PRD_BLUEPRINT_MVP_V10.md"], verify=(True, "sin fallos"))
        self.assertEqual(g.decide('git commit -m "docs: prd v10"', c)[0], "allow")

    def test_no_corre_verify_si_no_toca_canon(self):
        def boom():
            raise AssertionError("verify_corpus no debía ejecutarse")
        c = ctx(staged=["docs/glosario.md"])
        c["verify_corpus"] = boom
        self.assertEqual(g.decide('git commit -m "docs: glosario"', c)[0], "allow")

    def test_commit_dash_a_incluye_cambios_sin_stage(self):
        c = ctx(staged=[], changed=["docs/linea-base/LIBOX_BACKLOG_MVP_V4.md"], verify=(False, "RESULTADO: 1 fallo"))
        self.assertEqual(g.decide('git commit -am "docs: backlog"', c)[0], "deny")


class B4Correo(unittest.TestCase):
    def test_bloquea_correo_fuera_de_la_org(self):
        kind, msg = g.decide('git commit -m "feat: x"', ctx(email="dian.cs183@gmail.com"))
        self.assertEqual(kind, "deny")
        self.assertIn("git config user.email", msg)

    def test_bloquea_correo_vacio(self):
        self.assertEqual(g.decide('git commit -m "feat: x"', ctx(email=""))[0], "deny")

    def test_no_exige_correo_fuera_de_commit(self):
        self.assertEqual(g.decide("git status", ctx(email=""))[0], "allow")


class Robustez(unittest.TestCase):
    def test_comando_vacio_permite(self):
        self.assertEqual(g.decide("", ctx())[0], "allow")

    def test_error_en_git_permite(self):
        def boom():
            raise RuntimeError("git no disponible")
        c = ctx()
        c["user_email"] = boom
        self.assertEqual(g.decide('git commit -m "feat: x"', c)[0], "allow")


if __name__ == "__main__":
    unittest.main()
