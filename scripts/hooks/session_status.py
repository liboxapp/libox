#!/usr/bin/env python3
"""Hook SessionStart: cuatro líneas de estado del OS de IA (rama, freeze de desarrollo, verify_corpus).

Lo que imprime por stdout entra al contexto de la sesión: se mantiene corto a propósito.
Python 3.9+. Ante error emite AVISO y sale 0.
"""
import os
import subprocess
import sys
from typing import List, Optional

from guard_paths import warn
from corpus_check import verify_corpus, CorpusCheckUnavailable

FREEZE_RULE = os.path.join(".claude", "rules", "src-congelado.md")


def status_lines(branch: str, frozen: bool, verify_ok: Optional[bool]) -> List[str]:
    """Arma las cuatro líneas de estado.

    ``verify_ok`` es True (sin fallos), False (con fallos) o None (no se pudo ejecutar).
    """
    if verify_ok is True:
        verify_line = "- verify_corpus: sin fallos"
    elif verify_ok is False:
        verify_line = ("- verify_corpus: CON FALLOS — corre "
                       "`python3 verify_corpus.py --dir docs/linea-base`")
    else:
        verify_line = ("- verify_corpus: no se pudo ejecutar — revisa "
                       "`python3 verify_corpus.py --dir docs/linea-base`")
    return [
        "## Estado del OS de IA (auto)",
        "- Rama: `{}`".format(branch or "?"),
        ("- TypeScript ratificado (ASS-002) — `src/` congelado hasta D1 (`.claude/rules/src-congelado.md`)"
         if frozen else "- Regla de freeze ausente — verificar el doc 20 y cierre D1; no inferir habilitación"),
        verify_line,
    ]


def main() -> int:
    try:
        sys.stdin.read()  # el payload no se usa; se consume para no dejar el pipe abierto
        root = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
        r = subprocess.run(["git", "-C", root, "rev-parse", "--abbrev-ref", "HEAD"],
                           capture_output=True, text=True, timeout=10)
        branch = r.stdout.strip() if r.returncode == 0 else "?"
        frozen = os.path.exists(os.path.join(root, FREEZE_RULE))
        try:
            ok, _ = verify_corpus(root)
        except CorpusCheckUnavailable:
            ok = None
        sys.stdout.write("\n".join(status_lines(branch, frozen, ok)) + "\n")
    except Exception:  # noqa: BLE001
        warn('session_status')
    return 0


if __name__ == "__main__":
    sys.exit(main())
