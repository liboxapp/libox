#!/usr/bin/env python3
"""Guard PreToolUse (matcher Edit|Write|MultiEdit|NotebookEdit) del OS de IA de Libox. Python 3.9+.

  E1  bloquea editar in-place un archivo versionado (_V<n> o -V<n>) existente en docs/linea-base/
  E2  bloquea escribir en src/** o en la config del scaffold hasta el cierre C2/D1
  E3  bloquea contenido nuevo con nombres legacy (Sortibox/ALAZAR) fuera de la allowlist
Válvulas de escape por entorno: LIBOX_PERMITIR_INPLACE=1, LIBOX_DESCONGELAR_SRC=1,
LIBOX_PERMITIR_LEGACY=1, LIBOX_EDITAR_OS=1.
E4 protege el OS; E5 impide sobrescribir informes sin válvula de escape.
El freeze usa allowlist. Errores: permite con AVISO visible.
"""
import json
import os
import re
import sys

from guard_paths import candidates, warn
from audit_reports import is_existing_report
from typing import Callable, Dict, Optional, Tuple

# --- D1: borrar estas tres constantes (y sus tests) al levantar el freeze ---
FROZEN_PREFIX = "src/"
FROZEN_FILES = {
    "package.json", "package-lock.json", "next.config.ts", "tsconfig.json",
    "components.json", "eslint.config.mjs", "postcss.config.mjs", "vitest.config.ts",
}
FROZEN_EXEMPT_BASENAMES = {"CLAUDE.md"}
# ---------------------------------------------------------------------------------
CANON_PREFIX = "docs/linea-base/"
# Rutas que pueden nombrar los nombres legacy porque enuncian la regla de naming o son histórico
LEGACY_ALLOWLIST_FILES = {"CLAUDE.md", "CONTRIBUTING.md"}
LEGACY_ALLOWLIST_PREFIXES = (
    "docs/archive/", ".claude/rules/", ".claude/agents/", ".claude/skills/",
    "docs/equipo/", "docs/superpowers/",
)
VERSIONED_RE = re.compile(r"[_-]V\d+\.", re.I)
LEGACY_RE = re.compile(r"\b(sortibox|alazar)\b", re.I)

MSG_E1 = (
    "🚫 `{path}` es un documento vigente del corpus canónico: no se edita in-place (CD-01/CD-08).\n"
    "Emite la versión siguiente con el skill `libox-versionar-doc` (copia a V(n+1), identidad en "
    "cuatro lugares, changelog, BASELINE + Registro §1, verify_corpus a cero). "
    "Válvula de escape solo con acuerdo explícito: LIBOX_PERMITIR_INPLACE=1."
)
MSG_E2 = (
    "🚫 `{path}` está congelado: TypeScript ratificado por ASS-002; cierre C2/D1 pendiente.\n"
    "No se crea ni extiende código hasta cerrarlo (ver .claude/rules/src-congelado.md). "
    "Excepción autorizada para la sesión (no exime el CI): LIBOX_DESCONGELAR_SRC=1."
)
MSG_E3 = (
    "🚫 El contenido nuevo de `{path}` menciona un nombre legacy (Sortibox/ALAZAR). "
    "El producto es Libox; esos nombres solo se admiten al enunciar la regla de naming "
    "(CLAUDE.md, CONTRIBUTING.md, .claude/rules|agents|skills, docs/equipo, docs/superpowers) "
    "o en docs/archive/. Si es legítimo, con acuerdo explícito: LIBOX_PERMITIR_LEGACY=1, LIBOX_EDITAR_OS=1."
)


OS_PREFIXES = ('scripts/hooks/', '.claude/rules/', '.claude/agents/',
               '.claude/skills/', 'scripts/ci/', 'scripts/audit/')
OS_FILES = {'.claude/settings.json', '.claude/settings.local.json'}
WRITE_PREFIXES = ('docs/', 'scripts/', '.github/', '.claude/', '.agents/', '.obsidian/')
WRITE_FILES = {'readme.md', 'agents.md', 'claude.md', 'contributing.md', 'changelog.md',
               '.gitignore', '.markdownlint-cli2.yaml', 'commitlint.config.cjs',
               'verify_corpus.py', 'release-please-config.json', '.release-please-manifest.json'}


def relpath(file_path: str, root: str) -> Optional[str]:
    paths = candidates(file_path, root)
    return paths[-1][0] if paths else None


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
        fp = tool_input.get('file_path') or tool_input.get('notebook_path') or tool_input.get('path') or ''
        if not fp:
            return 'allow', ''
        if not os.path.isabs(fp) and os.path.normpath(fp).startswith('..' + os.sep):
            return 'deny', 'Ruta relativa fuera del proyecto; use una ruta absoluta verificable.'
        absolute_input = os.path.abspath(os.path.join(root, fp))
        if is_existing_report(absolute_input):
            return 'deny', 'E5: informe existente inmutable; crear un nuevo intento sin sobrescribir.'
        for rel, absolute in candidates(fp, root):
            key = rel.casefold()
            base = key.rsplit('/', 1)[-1]
            if (key.startswith(OS_PREFIXES) or key in OS_FILES):
                if env.get('LIBOX_EDITAR_OS') != '1':
                    return 'deny', 'E4: OS protegido. Cambio autorizado requiere LIBOX_EDITAR_OS=1 (con aviso).'
                print('AVISO: LIBOX_EDITAR_OS=1 permite modificar el OS; CI sigue obligatorio.', file=sys.stderr)
            documentation = key.startswith('src/') and base == 'claude.md'
            frozen = (not documentation and (key == 'src' or key.startswith('src/')
                      or key in FROZEN_FILES or not (key.startswith(WRITE_PREFIXES) or key in WRITE_FILES)))
            if frozen and env.get('LIBOX_DESCONGELAR_SRC') != '1':
                return 'deny', MSG_E2.format(path=ascii(rel))
            if key.startswith(CANON_PREFIX) and VERSIONED_RE.search(base):
                if exists(absolute) and env.get('LIBOX_PERMITIR_INPLACE') != '1':
                    return 'deny', MSG_E1.format(path=ascii(rel))
            if (rel not in LEGACY_ALLOWLIST_FILES and not key.startswith(LEGACY_ALLOWLIST_PREFIXES)
                    and LEGACY_RE.search(new_content(tool_input))
                    and env.get('LIBOX_PERMITIR_LEGACY') != '1'):
                return 'deny', MSG_E3.format(path=ascii(rel))
        return 'allow', ''
    except Exception:
        warn('guard_edit')
        return 'allow', ''


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        warn('guard_edit: payload JSON')
        return 0
    if not isinstance(payload, dict):
        warn('guard_edit: payload')
        return 0
    root = payload.get('cwd') or os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd()
    kind, reason = decide(payload.get("tool_input") or {}, root, dict(os.environ))
    if kind == "deny":
        sys.stderr.write(reason + "\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
