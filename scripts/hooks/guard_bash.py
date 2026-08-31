#!/usr/bin/env python3
"""Guard PreToolUse (matcher Bash) del OS de IA de Libox. Python 3.9+.

Lee el JSON del hook por stdin y bloquea con exit 2 + mensaje por stderr:
  B1  commit con trailer de co-autoría de IA
  B2  push a main
  B3  commit que toca docs/linea-base/ o verify_corpus.py con verify_corpus en rojo
  B4  commit con correo de autoría fuera de @liboxapp.com
Ante cualquier error propio, permite (exit 0).
"""
import json
import os
import re
import subprocess
import sys
from typing import Callable, Dict, List, Tuple

from corpus_check import verify_corpus

COAUTHOR_RE = re.compile(
    r"git\s+commit[\s\S]*(Co-Authored-By|Generated with Claude|noreply@anthropic\.com)", re.I
)
PUSH_MAIN_RE = re.compile(
    r"git\s+push\s+(?!--delete)[^\n]*\b(origin\s+main|main:main|HEAD:main|--force\S*\s+origin\s+main)\b"
)
COMMIT_RE = re.compile(r"\bgit\b[^|;&\n]*\bcommit\b")
COMMIT_ALL_RE = re.compile(r"\s(-[a-zA-Z]*a[a-zA-Z]*|--all)(\s|$)")
CANON_PREFIX = "docs/linea-base/"
CANON_FILES = {"verify_corpus.py"}
ORG_DOMAIN = "@liboxapp.com"

MSG_B1 = (
    "🚫 Trailer de co-autoría de IA detectado en el commit.\n"
    "Regla firme del repo (CONTRIBUTING.md → \"Autoría: sin co-autores automáticos\"): "
    "los commits no llevan `Co-Authored-By: Claude ...` ni \"Generated with Claude Code\". "
    "Reescribe el mensaje sin el trailer y vuelve a intentar."
)
MSG_B2 = (
    "🚫 Push directo a `main` bloqueado.\n"
    "`main` solo recibe cambios vía Pull Request con rebase-and-merge. "
    "Crea una rama `<type>/<kebab>`, súbela con `git push -u origin <rama>` y abre el PR (skill `libox-pr`)."
)
MSG_B3 = (
    "🚫 El commit toca el corpus canónico y `verify_corpus.py` tiene fallos (CD-10).\n"
    "Corrige hasta cero fallos antes de commitear. Últimas líneas:\n{tail}"
)
MSG_B4 = (
    "🚫 Correo de autoría fuera de la organización: {email}.\n"
    "Configúralo local al repo: `git config user.email <tu>@liboxapp.com` y vuelve a commitear "
    "(el CI rechaza commits con otros dominios; ver docs/equipo/onboarding.md)."
)

Ctx = Dict[str, Callable]


def decide(command: str, ctx: Ctx) -> Tuple[str, str]:
    if not command:
        return "allow", ""
    if COAUTHOR_RE.search(command):
        return "deny", MSG_B1
    if PUSH_MAIN_RE.search(command):
        return "deny", MSG_B2
    if COMMIT_RE.search(command):
        try:
            email = (ctx["user_email"]() or "").strip()
            if not email.endswith(ORG_DOMAIN):
                return "deny", MSG_B4.format(email=email or "(vacío)")
            files = set(ctx["staged_files"]())
            if COMMIT_ALL_RE.search(command):
                files |= set(ctx["changed_files"]())
            if any(f.startswith(CANON_PREFIX) or f in CANON_FILES for f in files):
                ok, tail = ctx["verify_corpus"]()
                if not ok:
                    return "deny", MSG_B3.format(tail=tail)
        except Exception:  # noqa: BLE001 — un fallo del guard nunca bloquea al usuario
            return "allow", ""
    return "allow", ""


def _git(root: str, *args: str) -> List[str]:
    r = subprocess.run(["git", "-C", root] + list(args), capture_output=True, text=True, timeout=20)
    if r.returncode != 0:
        return []
    return [line for line in r.stdout.splitlines() if line.strip()]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        return 0
    command = (payload.get("tool_input") or {}).get("command") or ""
    root = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
    ctx = {
        "staged_files": lambda: _git(root, "diff", "--cached", "--name-only"),
        "changed_files": lambda: _git(root, "diff", "--name-only"),
        "user_email": lambda: " ".join(_git(root, "config", "user.email")),
        "verify_corpus": lambda: verify_corpus(root),
    }
    kind, reason = decide(command, ctx)
    if kind == "deny":
        sys.stderr.write(reason + "\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
