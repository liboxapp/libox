#!/usr/bin/env python3
"""Ejecuta verify_corpus.py (CD-10) y resume el resultado. Python 3.9+."""
import os
import subprocess
import sys
from typing import Tuple


def verify_corpus(root: str) -> Tuple[bool, str]:
    """Devuelve (ok, últimas 12 líneas). ok exige exit 0 y la frase 'sin fallos'."""
    script = os.path.join(root, "verify_corpus.py")
    corpus = os.path.join(root, "docs", "linea-base")
    try:
        r = subprocess.run(
            [sys.executable, script, "--dir", corpus],
            capture_output=True, text=True, timeout=60, cwd=root,
        )
    except Exception as exc:  # noqa: BLE001 — un fallo del entorno no debe romper el hook
        return False, "no se pudo ejecutar verify_corpus.py: {}".format(exc)
    out = (r.stdout + r.stderr).strip()
    tail = "\n".join(out.splitlines()[-12:])
    return (r.returncode == 0 and "sin fallos" in out), tail
