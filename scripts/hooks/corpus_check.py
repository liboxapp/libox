#!/usr/bin/env python3
"""Ejecuta verify_corpus.py (CD-10) y resume el resultado. Python 3.9+."""
import os
import subprocess
import sys
from typing import Tuple


class CorpusCheckUnavailable(RuntimeError):
    """verify_corpus.py no pudo ejecutarse (script ausente, timeout, intérprete)."""


def verify_corpus(root: str) -> Tuple[bool, str]:
    """Devuelve (ok, últimas 12 líneas). ok exige exit 0 y la frase 'sin fallos'.

    Lanza CorpusCheckUnavailable si el verificador no llega a ejecutarse (script
    ausente, timeout, intérprete no disponible): quien llama debe tratarlo como
    error propio y permitir, nunca como si el corpus tuviera fallos.
    """
    script = os.path.join(root, "verify_corpus.py")
    corpus = os.path.join(root, "docs", "linea-base")
    if not os.path.exists(script):
        raise CorpusCheckUnavailable("no existe {}".format(script))
    try:
        r = subprocess.run(
            [sys.executable, script, "--dir", corpus],
            capture_output=True, text=True, timeout=60, cwd=root,
        )
    except Exception as exc:  # noqa: BLE001 — un fallo del entorno no debe romper el hook
        raise CorpusCheckUnavailable(str(exc))
    out = (r.stdout + r.stderr).strip()
    tail = "\n".join(out.splitlines()[-12:])
    return (r.returncode == 0 and "sin fallos" in out), tail
