#!/usr/bin/env python3
"""Guard PreToolUse (matcher Edit|Write|MultiEdit) del OS de IA de Libox. Python 3.9+.

  E1  bloquea editar in-place un archivo versionado (_V<n>) existente en docs/linea-base/
  E2  bloquea escribir en src/** o en la config del scaffold mientras ASS-002 siga abierto
  E3  pregunta al usuario si el contenido nuevo introduce nombres legacy fuera de docs/archive/
Válvulas de escape por entorno: LIBOX_PERMITIR_INPLACE=1, LIBOX_DESCONGELAR_SRC=1.
Ante cualquier error propio, permite (exit 0).
"""
import json
import os
import re
import sys
from typing import Callable, Dict, Optional, Tuple

# --- ASS-002: borrar estas tres constantes (y sus tests) al levantar el freeze ---
FROZEN_PREFIX = "src/"
FROZEN_FILES = {
    "package.json", "package-lock.json", "next.config.ts", "tsconfig.json",
    "components.json", "eslint.config.mjs", "postcss.config.mjs",
}
FROZEN_EXEMPT_BASENAMES = {"CLAUDE.md"}
# ---------------------------------------------------------------------------------
CANON_PREFIX = "docs/linea-base/"
ARCHIVE_PREFIX = "docs/archive/"
VERSIONED_RE = re.compile(r"_V\d+\.")
LEGACY_RE = re.compile(r"\b(sortibox|alazar)\b", re.I)

MSG_E1 = (
    "🚫 `{path}` es un documento vigente del corpus canónico: no se edita in-place (CD-01/CD-08).\n"
    "Emite la versión siguiente con el skill `libox-versionar-doc` (copia a V(n+1), identidad en "
    "cuatro lugares, changelog, BASELINE + Registro §1, verify_corpus a cero). "
    "Válvula de escape solo con acuerdo explícito: LIBOX_PERMITIR_INPLACE=1."
)
MSG_E2 = (
    "🚫 `{path}` está congelado: ASS-002 (stack Next.js vs .NET 8) sigue sin ratificar.\n"
    "No se crea ni extiende código hasta cerrarlo (ver .claude/rules/src-congelado.md). "
    "Para fixes al PR #15 o exigencias del CI, con acuerdo explícito: LIBOX_DESCONGELAR_SRC=1."
)
MSG_E3 = (
    "El contenido nuevo de `{path}` menciona un nombre legacy (Sortibox/ALAZAR). "
    "El producto es Libox; esos nombres solo se admiten al enunciar la regla de naming o en docs/archive/. "
    "¿Confirmas la escritura?"
)


def relpath(file_path: str, root: str) -> Optional[str]:
    """Ruta relativa al repo con '/', o None si el archivo está fuera del repo."""
    p = os.path.normpath(file_path)
    if not os.path.isabs(p):
        return p.replace(os.sep, "/")
    r = os.path.normpath(root)
    if p == r or p.startswith(r + os.sep):
        return os.path.relpath(p, r).replace(os.sep, "/")
    return None


def new_content(tool_input: dict) -> str:
    parts = []
    for key in ("new_string", "content", "file_text"):
        if tool_input.get(key):
            parts.append(str(tool_input[key]))
    for e in tool_input.get("edits") or []:
        if isinstance(e, dict) and e.get("new_string"):
            parts.append(str(e["new_string"]))
    return "\n".join(parts)


def decide(tool_input: dict, root: str, env: Dict[str, str],
           exists: Callable[[str], bool] = os.path.exists) -> Tuple[str, str]:
    try:
        fp = tool_input.get("file_path") or tool_input.get("path") or ""
        rel = relpath(fp, root) if fp else None
        if rel is None:
            return "allow", ""
        base = os.path.basename(rel)
        frozen = (rel.startswith(FROZEN_PREFIX) and base not in FROZEN_EXEMPT_BASENAMES) or rel in FROZEN_FILES
        if frozen and env.get("LIBOX_DESCONGELAR_SRC") != "1":
            return "deny", MSG_E2.format(path=rel)
        if rel.startswith(CANON_PREFIX) and VERSIONED_RE.search(base):
            absolute = fp if os.path.isabs(fp) else os.path.join(root, fp)
            if exists(absolute) and env.get("LIBOX_PERMITIR_INPLACE") != "1":
                return "deny", MSG_E1.format(path=rel)
        if not rel.startswith(ARCHIVE_PREFIX) and LEGACY_RE.search(new_content(tool_input)):
            return "ask", MSG_E3.format(path=rel)
        return "allow", ""
    except Exception:  # noqa: BLE001 — un fallo del guard nunca bloquea al usuario
        return "allow", ""


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        return 0
    root = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
    kind, reason = decide(payload.get("tool_input") or {}, root, dict(os.environ))
    if kind == "deny":
        sys.stderr.write(reason + "\n")
        return 2
    if kind == "ask":
        sys.stdout.write(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": reason,
            }
        }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
