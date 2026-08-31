"""Tests del guard PreToolUse para Edit/Write/MultiEdit (E1–E3). Python 3.9+."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import guard_edit as g  # noqa: E402

ROOT = "/repo"


def edit(path, new="texto", old="viejo"):
    return {"file_path": path, "old_string": old, "new_string": new}


def write(path, content="texto"):
    return {"file_path": path, "content": content}


def exists_factory(existing):
    existing = set(existing)
    return lambda p: p in existing


class E2SrcCongelado(unittest.TestCase):
    def test_bloquea_write_en_src(self):
        kind, msg = g.decide(write(ROOT + "/src/app/page.tsx"), ROOT, {})
        self.assertEqual(kind, "deny")
        self.assertIn("ASS-002", msg)

    def test_bloquea_edit_package_json(self):
        self.assertEqual(g.decide(edit(ROOT + "/package.json"), ROOT, {})[0], "deny")

    def test_bloquea_ruta_relativa(self):
        self.assertEqual(g.decide(edit("src/lib/x.ts"), ROOT, {})[0], "deny")

    def test_exime_claude_md_de_src(self):
        self.assertEqual(g.decide(edit(ROOT + "/src/CLAUDE.md"), ROOT, {})[0], "allow")

    def test_valvula_de_escape(self):
        env = {"LIBOX_DESCONGELAR_SRC": "1"}
        self.assertEqual(g.decide(write(ROOT + "/src/app/page.tsx"), ROOT, env)[0], "allow")

    def test_no_bloquea_fuera_del_repo(self):
        self.assertEqual(g.decide(write("/otro/proyecto/src/a.ts"), ROOT, {})[0], "allow")


class E1CanonInPlace(unittest.TestCase):
    V9 = ROOT + "/docs/linea-base/LIBOX_PRD_BLUEPRINT_MVP_V9.md"
    V10 = ROOT + "/docs/linea-base/LIBOX_PRD_BLUEPRINT_MVP_V10.md"
    SQL = ROOT + "/docs/linea-base/ARTEFACTOS/libox_schema_L3_V7.sql"
    TOKENS = ROOT + "/docs/linea-base/ARTEFACTOS/libox-design-tokens-L4-V2.json"

    def test_bloquea_edit_de_version_existente(self):
        kind, msg = g.decide(edit(self.V9), ROOT, {}, exists=exists_factory([self.V9]))
        self.assertEqual(kind, "deny")
        self.assertIn("libox-versionar-doc", msg)

    def test_bloquea_write_sobre_version_existente(self):
        self.assertEqual(g.decide(write(self.V9), ROOT, {}, exists=exists_factory([self.V9]))[0], "deny")

    def test_bloquea_artefacto_versionado_existente(self):
        self.assertEqual(g.decide(edit(self.SQL), ROOT, {}, exists=exists_factory([self.SQL]))[0], "deny")

    def test_bloquea_artefacto_versionado_con_guion(self):
        self.assertEqual(g.decide(edit(self.TOKENS), ROOT, {}, exists=exists_factory([self.TOKENS]))[0], "deny")

    def test_permite_crear_version_nueva(self):
        self.assertEqual(g.decide(write(self.V10), ROOT, {}, exists=exists_factory([self.V9]))[0], "allow")

    def test_permite_leeme(self):
        p = ROOT + "/docs/linea-base/LEEME.md"
        self.assertEqual(g.decide(edit(p), ROOT, {}, exists=exists_factory([p]))[0], "allow")

    def test_valvula_de_escape(self):
        env = {"LIBOX_PERMITIR_INPLACE": "1"}
        self.assertEqual(g.decide(edit(self.V9), ROOT, env, exists=exists_factory([self.V9]))[0], "allow")


class E3NamingLegacy(unittest.TestCase):
    def test_pregunta_ante_sortibox(self):
        kind, msg = g.decide(write(ROOT + "/docs/glosario.md", "Sortibox era el nombre"), ROOT, {})
        self.assertEqual(kind, "ask")
        self.assertIn("Libox", msg)

    def test_pregunta_ante_alazar_en_edit(self):
        self.assertEqual(g.decide(edit(ROOT + "/docs/x.md", new="ver ALAZAR"), ROOT, {})[0], "ask")

    def test_pregunta_en_multiedit(self):
        ti = {"file_path": ROOT + "/docs/x.md", "edits": [{"old_string": "a", "new_string": "alazar"}]}
        self.assertEqual(g.decide(ti, ROOT, {})[0], "ask")

    def test_no_pregunta_en_archive(self):
        self.assertEqual(g.decide(write(ROOT + "/docs/archive/prd.md", "ALAZAR"), ROOT, {})[0], "allow")

    def test_no_pregunta_por_subcadena(self):
        self.assertEqual(g.decide(write(ROOT + "/docs/x.md", "salazar"), ROOT, {})[0], "allow")

    def test_permite_contenido_normal(self):
        self.assertEqual(g.decide(write(ROOT + "/docs/x.md", "Libox es el producto"), ROOT, {})[0], "allow")


class Robustez(unittest.TestCase):
    def test_sin_file_path_permite(self):
        self.assertEqual(g.decide({}, ROOT, {})[0], "allow")

    def test_acepta_alias_path_y_file_text(self):
        ti = {"path": ROOT + "/src/a.ts", "file_text": "x"}
        self.assertEqual(g.decide(ti, ROOT, {})[0], "deny")

    def test_error_interno_permite(self):
        def boom(_):
            raise OSError("stat falló")
        p = ROOT + "/docs/linea-base/LIBOX_PRD_BLUEPRINT_MVP_V9.md"
        self.assertEqual(g.decide(edit(p), ROOT, {}, exists=boom)[0], "allow")


if __name__ == "__main__":
    unittest.main()
