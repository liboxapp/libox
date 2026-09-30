"""Guard de transcripción: código protegido heredado, no prueba su corrección."""
from pathlib import Path
import re
import hashlib
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'docs/linea-base/LIBOX_ESPECIFICACION_TECNICA_L3_V7.md'
DRAFT = ROOT / 'docs/superpowers/specs/c1-l3-v8/LIBOX_ESPECIFICACION_TECNICA_L3_V8_DRAFT.md'

# Bloques de V7 cuya transcripción no debe cambiar lógica, comentarios ni literales.
# Índices anclados por el SHA comprobado en la prueba, para no seleccionar otro bloque.
PROTECTED_BLOCKS = (6, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 26, 27,
                    30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 57, 58, 59)


def indented_blocks(text):
    return [match.group() for match in re.finditer(r'(?m)(?:^    .*\n|^\n(?=    ))+', text)]


def code_lines(text):
    # Solo elimina líneas vacías/espacios finales por lint. Conserva la indentación
    # de líneas no vacías y todo token, incluidos comentarios y espacios internos.
    return '\n'.join(line.rstrip() for line in text.splitlines() if line.strip())


class PreservedL3(unittest.TestCase):
    def test_protected_code_is_transcribed_without_semantic_edits(self):
        self.assertEqual(hashlib.sha256(BASE.read_bytes()).hexdigest(),
                         '13217f018af355f6f827f3926f8562d371bcf475f35f182f089738610d0f1f8d')
        original = BASE.read_text()
        blocks = indented_blocks(original)
        self.assertEqual(len(blocks), 60, 'Revisar mapa de bloques si cambia V7')
        candidate = code_lines('\n'.join(indented_blocks(DRAFT.read_text())))
        for index in PROTECTED_BLOCKS:
            with self.subTest(block=index):
                self.assertEqual(candidate.count(code_lines(blocks[index])), 1,
                                 "El bloque debe aparecer exactamente una vez")

        # Una redefinición posterior también cambia comportamiento aunque conserve
        # la copia original. Comprobar identidades SQL/Python de los bloques protegidos.
        protected = '\n'.join(blocks[i] for i in PROTECTED_BLOCKS)
        patterns = (
            r'CREATE (?:OR REPLACE )?(?:TABLE|FUNCTION) ([a-z_]+)',
            r'(?m)^    def ([a-z_]+)\(',
        )
        for pattern in patterns:
            names = set(re.findall(pattern, protected))
            original_names = re.findall(pattern, code_lines('\n'.join(blocks)))
            candidate_names = re.findall(pattern, candidate)
            for name in names:
                self.assertEqual(candidate_names.count(name), original_names.count(name), name)

    def test_no_unfinished_transcription_marker(self):
        draft = DRAFT.read_text()
        self.assertNotIn('<!-- CONTINUA-BORRADOR -->', draft)
        self.assertIn('14.8', draft)
        self.assertIn('F7', draft)
