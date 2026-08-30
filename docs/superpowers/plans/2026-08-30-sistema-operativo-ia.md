---
title: Plan de implementación — Sistema operativo de IA
status: aprobado
tags: [libox, equipo, claude-code, plan]
updated: 2026-08-30
description: Plan paso a paso, con TDD y commits atómicos, para implementar el spec del sistema operativo de IA (rules, guards, skills, agentes, manual, higiene).
---

# Sistema operativo de IA — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dejar versionada en el repo la capa operativa de Claude Code del equipo: `CLAUDE.md` magro + reglas por ruta, hooks nativos testeados, skills y agentes Libox, manual en `docs/equipo/`, e higiene del entorno.

**Architecture:** Todo vive en el repo y lo carga Claude Code al clonar. Las reglas se inyectan por ruta (`.claude/rules/*.md` con `paths:`); los guards son scripts Python stdlib invocados como hooks `PreToolUse`/`SessionStart` desde `.claude/settings.json`, con tests `unittest`; skills y agentes son archivos markdown con frontmatter. Nada presupone un stack de aplicación (ASS-002 abierto).

**Tech Stack:** Claude Code (hooks, rules, skills, subagents) · Python 3.9+ stdlib (`json`, `re`, `subprocess`, `unittest`) · GitHub Actions · markdown.

**Spec:** [`docs/superpowers/specs/2026-08-30-sistema-operativo-ia-design.md`](../specs/2026-08-30-sistema-operativo-ia-design.md)

## Global Constraints

- **Python 3.9 compatible** en `scripts/hooks/` (la máquina de Diego corre 3.9.6; CI prueba 3.9 y 3.12): sin `match`, sin `X | Y` en anotaciones, sin `str.removeprefix`.
- **Sin trailers de co-autoría de IA** en commits ni "Generated with Claude Code" en PRs (regla firme; el guard B1 lo bloquea a partir de la Tarea 5).
- **Commits:** Conventional Commits en español, scope `os-ia`; correo `@liboxapp.com` (`git config user.email` debe terminar en `@liboxapp.com`).
- **Rama de trabajo:** `chore/sistema-operativo-ia` (ya creada; contiene el spec). Nunca push a `main`.
- **Idioma:** todo texto que lee un humano, en español. Nombres de archivos, campos de frontmatter y código, en inglés cuando el harness lo exige.
- **Docs en `docs/`:** frontmatter `title/status/tags/updated/description`; links markdown relativos; sin wikilinks. `.claude/**` está excluido de markdownlint.
- **No tocar** `docs/linea-base/**`, `src/**` (salvo `src/CLAUDE.md` en la Tarea 9) ni `.agents/`.
- **Naming:** el producto es Libox; "Sortibox"/"ALAZAR" solo aparecen al enunciar la regla.
- Los hooks deben ser **inofensivos ante error**: si el JSON de entrada no se puede leer o `git` falla, el guard permite (exit 0) — nunca deja al usuario bloqueado por un bug del propio guard.

---

### Task 1: Reglas por ruta (`.claude/rules/`)

**Files:**
- Create: `.claude/rules/linea-base.md`
- Create: `.claude/rules/docs.md`
- Create: `.claude/rules/src-congelado.md`
- Create: `.claude/rules/git.md`

**Interfaces:**
- Produces: la existencia de `.claude/rules/src-congelado.md` es la señal que `session_status.py` (Tarea 4) usa para reportar "ASS-002 abierto". Las variables `LIBOX_DESCONGELAR_SRC` y `LIBOX_PERMITIR_INPLACE` que se documentan aquí las implementa `guard_edit.py` (Tarea 3).

- [ ] **Step 1: Crear `.claude/rules/linea-base.md`**

```markdown
---
paths:
  - "docs/linea-base/**"
---

# Corpus canónico (`docs/linea-base/`)

Gobernado por el Registro Maestro V6 (`LIBOX_REGISTRO_MAESTRO_LINEA_BASE_V6.md`, §1 y §4).
Si un documento no figura en su §1, no rige. La línea base está **congelada**.

- **Nunca edites un documento vigente in-place.** Todo cambio es una versión
  completa nueva `X_V<n>` → `X_V<n+1>` (CD-01, CD-02). La anterior se archiva sin
  editar (CD-08). El guard `guard_edit.py` bloquea la edición de archivos `_V<n>`
  existentes; la válvula de escape es `LIBOX_PERMITIR_INPLACE=1` en el entorno
  (o en `env` de `.claude/settings.local.json`) y solo se usa con acuerdo explícito.
- **Identidad en cuatro lugares** (CD-03): nombre de archivo, título interno, pie
  y campo de versión deben coincidir.
- **Changelog interno** con la columna "decisión que invalida" (CD-04).
- **Autonomía** (CD-06): la versión nueva no remite a la derogada para contenido normativo.
- **Emisión = un solo acto** (CD-10, CD-11): `python3 verify_corpus.py --dir docs/linea-base`
  con cero fallos + alta en `BASELINE` (`verify_corpus.py`) + Registro §1, en el mismo commit.
  Si el Registro cambia, también sube de versión.
- **Hallazgos que no justifican romper el freeze** (CD-07: solo rompe lo que impide
  construir o expone a riesgo legal/patrimonial) van al backlog de cambio o al doc 20
  de Outline (ASS-/CHANGE-/RISK-). Usa el skill `libox-registrar-hallazgo`.
- **Precedencia ante conflicto:** L0 > L2 > L3 > L4; VIES manda en identidad de marca.
- Para emitir una versión, sigue el skill `libox-versionar-doc`.
```

- [ ] **Step 2: Crear `.claude/rules/docs.md`**

```markdown
---
paths:
  - "docs/**"
---

# Documentación (`docs/`)

Referencia completa: `docs/equipo/estilo-documentacion.md`. Reglas mínimas:

- **Español.** Prosa directa, sin relleno; negritas y listas solo cuando aportan.
- **Frontmatter obligatorio** en todo `.md` de `docs/` (salvo `docs/linea-base/`):
  `title`, `status` (`vigente | borrador | obsoleto | aprobado`), `tags`, `updated`
  (`YYYY-MM-DD`), `description` (una línea para decidir si abrirlo).
- **Links markdown estándar** `[texto](ruta.md)`, relativos al archivo; nunca
  wikilinks `[[...]]`. El CI (`lychee --offline`) rompe si un link relativo no resuelve.
- **~150 líneas** por documento; si crece, partir en notas enlazadas.
- **`docs/archive/` es histórico**: no se cita como fuente vigente.
- **Claims legales** marcados `[LEGAL→ABOGADO]` hasta ratificación del abogado.
- **Decisiones**: ya no se abren ADRs Z nuevos; los hallazgos van al backlog de
  cambio o al doc 20 de Outline y se vuelven normativos solo con una versión nueva
  del documento del canon (ver `.claude/rules/linea-base.md`).
- `CLAUDE.md` y `MEMORY.md` se mantienen magros: reglas y punteros, el contenido va en `docs/`.
```

- [ ] **Step 3: Crear `.claude/rules/src-congelado.md`**

```markdown
---
paths:
  - "src/**"
  - "package.json"
  - "package-lock.json"
  - "next.config.ts"
  - "tsconfig.json"
  - "components.json"
  - "eslint.config.mjs"
  - "postcss.config.mjs"
---

# Scaffold congelado — ASS-002 abierto

El canon (L3 V7 §0.3) fija **.NET 8** como runtime; ADR Z.6 y el scaffold real son
**Next.js**. La derogación de facto de Z.6 no fue ratificada por los socios
(ASS-002, doc 20 de Outline). Hasta que se cierre:

- **No crear ni extender código** bajo `src/` ni tocar la configuración del scaffold.
  El guard `guard_edit.py` (E2) bloquea cualquier escritura en estas rutas.
  `src/**/CLAUDE.md` queda exento: es documentación, no código.
- **Excepciones admitidas:** fixes al PR #15 ya abierto y cambios que exija el CI.
  Válvula de escape: `LIBOX_DESCONGELAR_SRC=1` en el entorno o en `env` de
  `.claude/settings.local.json`, solo para esa sesión y con acuerdo explícito.
- **Cómo se levanta el freeze:** el PR que cierre ASS-002 (nueva versión de L3 o
  registro de la ratificación) borra este archivo y la constante `FROZEN_PREFIX` /
  `FROZEN_FILES` de `scripts/hooks/guard_edit.py` (con sus tests), y actualiza
  `src/CLAUDE.md`. Ese mismo PR puede añadir la capa `dev` del OS (agentes
  ejecutor/tester/depurador).
```

- [ ] **Step 4: Crear `.claude/rules/git.md`**

```markdown
# Git y Pull Requests

Normativo: `CONTRIBUTING.md`. Resumen operativo:

- **Rama por cambio:** `<type>/<kebab>` desde `main` actualizado. Nunca commits ni
  push directos a `main` (el guard B2 y la regla hookify lo bloquean).
- **Conventional Commits en español** (`feat`, `fix`, `docs`, `chore`, `ci`,
  `refactor`, `test`), cuerpo que explica el porqué. Los valida `commitlint` en CI.
- **Correo de autoría `@liboxapp.com`** (`git config user.email`). El guard B4 lo
  exige antes de commitear; el CI rechaza commits con otros dominios.
- **Sin trailers de IA:** nunca `Co-Authored-By: Claude ...` ni "Generated with
  Claude Code" (guard B1 + hookify). La autoría es de quien revisa y firma.
- **Si el commit toca `docs/linea-base/` o `verify_corpus.py`**, el guard B3 corre
  `verify_corpus.py` y bloquea si hay fallos (CD-10).
- **PR:** `gh pr create` con cuerpo *Qué / Por qué / Verificación*; rebase-and-merge;
  ramas en vuelo se rebasan (`git push --force-with-lease`). Usa el skill `libox-pr`.
```

- [ ] **Step 5: Verificar que las cuatro reglas existen y que las tres con `paths:` abren con frontmatter**

Run:

```bash

ls .claude/rules/ && for f in linea-base docs src-congelado; do head -1 .claude/rules/$f.md; done

```

Expected: lista de 4 archivos y tres líneas `---`.

- [ ] **Step 6: Commit**

```bash
git add .claude/rules/
git commit -m "chore(os-ia): reglas por ruta para canon, docs, scaffold congelado y git

Cuatro rules de Claude Code que se inyectan solo al tocar la zona
correspondiente, en lugar de cargar todo en CLAUDE.md cada sesión."
```

---

### Task 2: Guard de Bash (B1–B4) con TDD

**Files:**
- Create: `scripts/hooks/corpus_check.py`
- Create: `scripts/hooks/guard_bash.py`
- Create: `scripts/hooks/tests/test_guard_bash.py`
- Modify: `.gitignore` (añadir `__pycache__/` y `*.pyc` si faltan)

**Interfaces:**
- Produces: `corpus_check.verify_corpus(root: str) -> Tuple[bool, str]` (ok, últimas 12 líneas de salida). `guard_bash.decide(command: str, ctx: dict) -> Tuple[str, str]` donde `ctx` tiene las callables `staged_files() -> List[str]`, `changed_files() -> List[str]`, `user_email() -> str`, `verify_corpus() -> Tuple[bool, str]`, y el retorno es `("allow"|"deny", mensaje)`.
- Consumida por: Tarea 4 (`corpus_check`) y Tarea 5 (wiring en `settings.json`).

- [ ] **Step 1: Escribir los tests (fallan porque el módulo no existe)**

`scripts/hooks/tests/test_guard_bash.py`:

```python
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
```

- [ ] **Step 2: Correr los tests y verificar que fallan**

Run: `python3 -m unittest discover -s scripts/hooks/tests -v 2>&1 | tail -3`
Expected: `ModuleNotFoundError: No module named 'guard_bash'`.

- [ ] **Step 3: Crear `scripts/hooks/corpus_check.py`**

```python
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
```

- [ ] **Step 4: Crear `scripts/hooks/guard_bash.py`**

```python
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
```

- [ ] **Step 5: Correr los tests y verificar que pasan**

Run: `python3 -m unittest discover -s scripts/hooks/tests -v 2>&1 | tail -3`
Expected: `OK` con 17 tests.

- [ ] **Step 6: Prueba de humo con stdin real (B1 y comando limpio)**

Run:

```bash

printf '%s' '{"tool_name":"Bash","cwd":"'"$PWD"'","tool_input":{"command":"git commit -m \"x\" -m \"Co-Authored-By: Claude <noreply@anthropic.com>\""}}' | CLAUDE_PROJECT_DIR="$PWD" python3 scripts/hooks/guard_bash.py; echo "exit=$?"
printf '%s' '{"tool_name":"Bash","cwd":"'"$PWD"'","tool_input":{"command":"git status"}}' | CLAUDE_PROJECT_DIR="$PWD" python3 scripts/hooks/guard_bash.py; echo "exit=$?"

```

Expected: primer comando imprime el mensaje 🚫 y `exit=2`; segundo imprime nada y `exit=0`.

- [ ] **Step 7: Ignorar bytecode de Python y commitear**

```bash
grep -q '__pycache__' .gitignore || printf '\n# Python (tests de hooks)\n__pycache__/\n*.pyc\n' >> .gitignore
git add .gitignore scripts/hooks/corpus_check.py scripts/hooks/guard_bash.py scripts/hooks/tests/test_guard_bash.py
git commit -m "feat(os-ia): guard de Bash — co-autoría, push a main, CD-10 y correo de la org

Hook PreToolUse en Python stdlib con tests unittest. Duplica a propósito
las dos reglas hookify (redundancia deliberada) y añade verify_corpus
antes de commitear cambios al canon y la comprobación del correo."
```

---

### Task 3: Guard de edición (E1–E3) con TDD

**Files:**
- Create: `scripts/hooks/guard_edit.py`
- Create: `scripts/hooks/tests/test_guard_edit.py`

**Interfaces:**
- Produces: `guard_edit.decide(tool_input: dict, root: str, env: dict, exists=os.path.exists) -> Tuple[str, str]` con retorno `("allow"|"deny"|"ask", mensaje)`. Constantes `FROZEN_PREFIX`, `FROZEN_FILES`, `FROZEN_EXEMPT_BASENAMES` (las borra el PR que cierre ASS-002).
- Consumida por: Tarea 5 (wiring).

- [ ] **Step 1: Escribir los tests**

`scripts/hooks/tests/test_guard_edit.py`:

```python
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

    def test_bloquea_edit_de_version_existente(self):
        kind, msg = g.decide(edit(self.V9), ROOT, {}, exists=exists_factory([self.V9]))
        self.assertEqual(kind, "deny")
        self.assertIn("libox-versionar-doc", msg)

    def test_bloquea_write_sobre_version_existente(self):
        self.assertEqual(g.decide(write(self.V9), ROOT, {}, exists=exists_factory([self.V9]))[0], "deny")

    def test_bloquea_artefacto_versionado_existente(self):
        self.assertEqual(g.decide(edit(self.SQL), ROOT, {}, exists=exists_factory([self.SQL]))[0], "deny")

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


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr y verificar que fallan**

Run: `python3 -m unittest scripts.hooks.tests.test_guard_edit 2>&1 | tail -2 || python3 -m unittest discover -s scripts/hooks/tests -p 'test_guard_edit.py' 2>&1 | tail -2`
Expected: `ModuleNotFoundError: No module named 'guard_edit'`.

- [ ] **Step 3: Crear `scripts/hooks/guard_edit.py`**

```python
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
```

- [ ] **Step 4: Correr toda la suite y verificar que pasa**

Run: `python3 -m unittest discover -s scripts/hooks/tests -v 2>&1 | tail -3`
Expected: `OK` con 37 tests.

- [ ] **Step 5: Prueba de humo con stdin real (E2, E1, E3)**

Run:

```bash

H="CLAUDE_PROJECT_DIR=$PWD python3 scripts/hooks/guard_edit.py"
printf '%s' '{"tool_name":"Write","cwd":"'"$PWD"'","tool_input":{"file_path":"'"$PWD"'/src/app/x.tsx","content":"x"}}' | eval $H; echo "exit=$?"
printf '%s' '{"tool_name":"Edit","cwd":"'"$PWD"'","tool_input":{"file_path":"'"$PWD"'/docs/linea-base/LIBOX_PRD_BLUEPRINT_MVP_V9.md","old_string":"a","new_string":"b"}}' | eval $H; echo "exit=$?"
printf '%s' '{"tool_name":"Write","cwd":"'"$PWD"'","tool_input":{"file_path":"'"$PWD"'/docs/glosario.md","content":"Sortibox"}}' | eval $H; echo; echo "exit=$?"

```

Expected: dos mensajes 🚫 con `exit=2`; el tercero imprime el JSON con `"permissionDecision": "ask"` y `exit=0`.

- [ ] **Step 6: Commit**

```bash
git add scripts/hooks/guard_edit.py scripts/hooks/tests/test_guard_edit.py
git commit -m "feat(os-ia): guard de edición — canon in-place, scaffold congelado y naming legacy

E1 bloquea editar versiones vigentes de docs/linea-base, E2 bloquea src/
y la config del scaffold mientras ASS-002 siga abierto (src/**/CLAUDE.md
exento), E3 pide confirmación ante Sortibox/ALAZAR fuera de docs/archive."
```

---

### Task 4: Estado de sesión (`SessionStart`) con tests

**Files:**
- Create: `scripts/hooks/session_status.py`
- Create: `scripts/hooks/tests/test_session_status.py`

**Interfaces:**
- Consumes: `corpus_check.verify_corpus(root)` (Tarea 2); existencia de `.claude/rules/src-congelado.md` (Tarea 1).
- Produces: `session_status.status_lines(branch: str, frozen: bool, verify_ok: bool) -> List[str]`.

- [ ] **Step 1: Escribir los tests**

`scripts/hooks/tests/test_session_status.py`:

```python
"""Tests del hook SessionStart de estado del OS. Python 3.9+."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import session_status as s  # noqa: E402


class StatusLines(unittest.TestCase):
    def test_tres_lineas_mas_titulo(self):
        lines = s.status_lines("main", True, True)
        self.assertEqual(len(lines), 4)
        self.assertTrue(lines[0].startswith("## "))

    def test_reporta_rama(self):
        self.assertIn("chore/os-ia", s.status_lines("chore/os-ia", True, True)[1])

    def test_reporta_freeze(self):
        self.assertIn("ASS-002 abierto", s.status_lines("main", True, True)[2])
        self.assertIn("ASS-002 cerrado", s.status_lines("main", False, True)[2])

    def test_reporta_verify(self):
        self.assertIn("sin fallos", s.status_lines("main", True, True)[3])
        self.assertIn("CON FALLOS", s.status_lines("main", True, False)[3])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr y verificar que fallan**

Run: `python3 -m unittest discover -s scripts/hooks/tests -p 'test_session_status.py' 2>&1 | tail -2`
Expected: `ModuleNotFoundError: No module named 'session_status'`.

- [ ] **Step 3: Crear `scripts/hooks/session_status.py`**

```python
#!/usr/bin/env python3
"""Hook SessionStart: tres líneas de estado del OS de IA (rama, freeze ASS-002, verify_corpus).

Lo que imprime por stdout entra al contexto de la sesión: se mantiene corto a propósito.
Python 3.9+. Ante error, no imprime nada y sale 0.
"""
import os
import subprocess
import sys
from typing import List

from corpus_check import verify_corpus

FREEZE_RULE = os.path.join(".claude", "rules", "src-congelado.md")


def status_lines(branch: str, frozen: bool, verify_ok: bool) -> List[str]:
    return [
        "## Estado del OS de IA (auto)",
        "- Rama: `{}`".format(branch or "?"),
        ("- ASS-002 abierto — `src/` congelado (`.claude/rules/src-congelado.md`)"
         if frozen else "- ASS-002 cerrado — `src/` habilitado"),
        ("- verify_corpus: sin fallos"
         if verify_ok else "- verify_corpus: CON FALLOS — corre `python3 verify_corpus.py --dir docs/linea-base`"),
    ]


def main() -> int:
    try:
        sys.stdin.read()  # el payload no se usa; se consume para no dejar el pipe abierto
        root = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
        r = subprocess.run(["git", "-C", root, "rev-parse", "--abbrev-ref", "HEAD"],
                           capture_output=True, text=True, timeout=10)
        branch = r.stdout.strip() if r.returncode == 0 else "?"
        frozen = os.path.exists(os.path.join(root, FREEZE_RULE))
        ok, _ = verify_corpus(root)
        sys.stdout.write("\n".join(status_lines(branch, frozen, ok)) + "\n")
    except Exception:  # noqa: BLE001
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Correr toda la suite**

Run: `python3 -m unittest discover -s scripts/hooks/tests 2>&1 | tail -3`
Expected: `OK` con 41 tests.

- [ ] **Step 5: Prueba de humo**

Run: `echo '{}' | CLAUDE_PROJECT_DIR="$PWD" python3 scripts/hooks/session_status.py`
Expected: cuatro líneas: título, `Rama: chore/sistema-operativo-ia`, `ASS-002 abierto — src/ congelado`, `verify_corpus: sin fallos`.

- [ ] **Step 6: Commit**

```bash
git add scripts/hooks/session_status.py scripts/hooks/tests/test_session_status.py
git commit -m "feat(os-ia): estado del OS al inicio de sesión (rama, freeze ASS-002, verify_corpus)"
```

---

### Task 5: Wiring en `settings.json` y CI de hooks

**Files:**
- Modify: `.claude/settings.json`
- Create: `.github/workflows/hooks.yml`

**Interfaces:**
- Consumes: `scripts/hooks/guard_bash.py`, `guard_edit.py`, `session_status.py` (Tareas 2–4).
- Produces: a partir de este commit, los guards están activos en toda sesión nueva de Claude Code sobre el repo — **incluida la que ejecuta las tareas siguientes** (recuerda: `src/CLAUDE.md` está exento de E2; el resto de este plan no toca rutas bloqueadas).

- [ ] **Step 1: Reemplazar `.claude/settings.json` completo**

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"${CLAUDE_PROJECT_DIR}/scripts/team-digest.sh\""
          },
          {
            "type": "command",
            "command": "python3 \"${CLAUDE_PROJECT_DIR}/scripts/hooks/session_status.py\""
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"${CLAUDE_PROJECT_DIR}/scripts/hooks/guard_bash.py\"",
            "timeout": 90
          }
        ]
      },
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"${CLAUDE_PROJECT_DIR}/scripts/hooks/guard_edit.py\"",
            "timeout": 15
          }
        ]
      }
    ]
  },
  "enabledPlugins": {
    "superpowers@claude-plugins-official": true,
    "frontend-design@claude-plugins-official": true,
    "skill-creator@claude-plugins-official": true,
    "hookify@claude-plugins-official": true,
    "claude-md-management@claude-plugins-official": true,
    "context-mode@context-mode": true,
    "security-guidance@claude-plugins-official": true,
    "claude-security@claude-plugins-official": true,
    "typescript-lsp@claude-plugins-official": true,
    "pr-review-toolkit@claude-plugins-official": true,
    "vercel@claude-plugins-official": true,
    "claude-mem@thedotmack": false,
    "vercel-plugin@vercel": false
  },
  "extraKnownMarketplaces": {
    "context-mode": {
      "source": {
        "source": "github",
        "repo": "mksglu/context-mode"
      }
    }
  }
}
```

- [ ] **Step 2: Crear `.github/workflows/hooks.yml`**

```yaml
name: hooks

# Los guards del OS de IA (scripts/hooks/) son código de infraestructura del
# equipo: se prueban como cualquier otro. Matriz 3.9/3.12 porque las máquinas
# de desarrollo corren Python 3.9 y el CI 3.12.

on:
  pull_request:
    paths:
      - "scripts/hooks/**"
      - ".claude/settings.json"
  push:
    branches: [main]
    paths:
      - "scripts/hooks/**"
      - ".claude/settings.json"

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ["3.9", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - name: Tests de los guards
        run: python3 -m unittest discover -s scripts/hooks/tests -v
      - name: settings.json es JSON válido y sus hooks apuntan a scripts existentes
        run: |
          python3 - <<'PY'
          import json, re, os, sys
          cfg = json.load(open(".claude/settings.json"))
          missing = []
          for event, groups in cfg.get("hooks", {}).items():
              for group in groups:
                  for h in group.get("hooks", []):
                      for m in re.findall(r"\$\{CLAUDE_PROJECT_DIR\}/([^\"]+)", h.get("command", "")):
                          if not os.path.exists(m):
                              missing.append(m)
          if missing:
              sys.exit("hooks referencian scripts inexistentes: %s" % missing)
          print("settings.json OK")
          PY
```

- [ ] **Step 3: Validar localmente el JSON y la referencia a scripts**

Run:

```bash

python3 -c "import json;json.load(open('.claude/settings.json'));print('JSON OK')" && ls scripts/hooks/guard_bash.py scripts/hooks/guard_edit.py scripts/hooks/session_status.py scripts/team-digest.sh

```

Expected: `JSON OK` y las cuatro rutas listadas.

- [ ] **Step 4: Commit**

```bash
git add .claude/settings.json .github/workflows/hooks.yml
git commit -m "ci(os-ia): activa los guards como hooks nativos y los prueba en CI

PreToolUse (Bash y Edit|Write|MultiEdit) y SessionStart apuntan a
scripts/hooks/ vía CLAUDE_PROJECT_DIR. claude-mem y vercel-plugin quedan
desactivados a nivel proyecto (Z.8). Workflow hooks.yml con matriz 3.9/3.12."
```

- [ ] **Step 5: Verificación en sesión nueva (la hace el orquestador, no el subagente)**

Abrir una sesión nueva de Claude Code en el repo y comprobar: el arranque muestra el bloque "Estado del OS de IA"; pedir `git push origin main` → bloqueado; pedir editar `docs/linea-base/LIBOX_PRD_BLUEPRINT_MVP_V9.md` → bloqueado; pedir crear `src/x.ts` → bloqueado; pedir escribir "Sortibox" en `docs/glosario.md` → pregunta. Si el harness no muestra la pregunta de E3 sino que la ignora, cambiar en `guard_edit.py` el retorno `"ask"` por `"deny"` con allowlist `{"CLAUDE.md", "CONTRIBUTING.md"} ∪ rutas bajo ".claude/rules/" y "docs/equipo/"`, ajustar los tests de `E3NamingLegacy` (esperar `deny` y añadir un caso `allow` para `CLAUDE.md`) y commitear como `fix(os-ia): E3 bloquea con allowlist (ask no soportado)`.

---

### Task 6: Skills Libox

**Files:**
- Create: `.claude/skills/libox-versionar-doc/SKILL.md`
- Create: `.claude/skills/libox-registrar-hallazgo/SKILL.md`
- Create: `.claude/skills/libox-outline-sync/SKILL.md`
- Create: `.claude/skills/libox-pr/SKILL.md`

**Interfaces:**
- Consumes: `scripts/outline-sync.sh` y `scripts/outline-map.json` (existentes; el script hace `skip (not mapped)` para archivos sin ID), MCP de Outline (`create_document`, `update_document`, `list_documents`), `verify_corpus.py`.
- Produces: nombres invocables `/libox-versionar-doc`, `/libox-registrar-hallazgo`, `/libox-outline-sync`, `/libox-pr`, referenciados por rules, agentes y manual.

- [ ] **Step 1: Crear `.claude/skills/libox-versionar-doc/SKILL.md`**

```markdown
---
name: libox-versionar-doc
description: Emite una nueva versión completa de un documento del corpus canónico (docs/linea-base) cumpliendo CD-01..CD-11. Úsalo siempre que haya que cambiar cualquier documento o artefacto de la línea base.
---

# Versionar un documento del canon

Entrada: `$ARGUMENTS` = nombre del archivo vigente (p. ej. `LIBOX_BACKLOG_MVP_V3.md`) y el motivo.

1. **Justifica el freeze.** La línea base está congelada (CD-07). Solo se emite si el
   cambio impide construir o expone a riesgo legal/patrimonial. Si no, detente y usa
   `libox-registrar-hallazgo` (queda en backlog de cambio / doc 20) — informa al usuario.
2. **Crea la versión siguiente.** Copia `X_V<n>.md` → `X_V<n+1>.md` (CD-01/02). No edites
   la anterior (CD-08; el guard E1 lo impide).
3. **Identidad en cuatro lugares** (CD-03): nombre de archivo, título interno, pie y
   campo de versión de la interfaz deben decir `V<n+1>`.
4. **Changelog interno** (CD-04): añade la fila con fecha, cambio y la decisión que
   invalida (ASS-/CHANGE-/RISK- o "hallazgo de construcción").
5. **Autonomía** (CD-06): la versión nueva no remite a la derogada para nada normativo.
6. **Registro y BASELINE en el mismo acto** (CD-11): actualiza `BASELINE` en
   `verify_corpus.py` (versión + archivo) y el §1 del Registro Maestro. Como el Registro
   es un documento del canon, también sube de versión (repite 2–5 para él).
7. **Verifica** (CD-10): `python3 verify_corpus.py --dir docs/linea-base` hasta
   `RESULTADO: sin fallos`. El guard B3 bloquea el commit si no.
8. **Integra:** rama `docs/<slug>`, commit `docs(canon): emite <DOC> V<n+1> — <motivo>`,
   PR con `libox-pr`. Deja la versión anterior en su sitio (el Registro §2 la marca derogada).
9. **Tras el merge:** pide al humano correr `/libox-outline-sync` para republicar el espejo.
```

- [ ] **Step 2: Crear `.claude/skills/libox-registrar-hallazgo/SKILL.md`**

```markdown
---
name: libox-registrar-hallazgo
description: Registra un supuesto (ASS-), solicitud de cambio (CHANGE-), riesgo (RISK-) o idea (IDEA-) en el doc 20 de Outline y, si aplica, en el backlog de cambio (CD-07), sin abrir una versión del canon. Úsalo cuando aparezca una observación que no justifica romper el freeze.
---

# Registrar un hallazgo

Entrada: `$ARGUMENTS` = descripción libre del hallazgo.

1. **Clasifica** con una sola etiqueta:
   - `ASS-` supuesto sobre el que se está construyendo y que alguien debe ratificar.
   - `CHANGE-` cambio propuesto a un documento del canon (va también al backlog de cambio).
   - `RISK-` riesgo con probabilidad e impacto.
   - `IDEA-` idea de producto/negocio sin compromiso.
2. **Localiza el registro** en Outline (MCP): colección "Libox — Negocio", documento cuyo
   título empieza por `20` (registro de asunciones y cambios). Usa `list_documents` /
   búsqueda por título; lee la última entrada para tomar el siguiente número correlativo.
3. **Redacta la entrada** con esta plantilla y añádela al final de la tabla del tipo
   correspondiente con `update_document` (no reescribas el resto del documento):

   | ID | Fecha | Origen | Descripción | Impacto | Dueño | Estado |
   |---|---|---|---|---|---|---|
   | `<TIPO>-<nnn>` | `YYYY-MM-DD` | doc/sección o PR que lo originó | una o dos frases | qué bloquea o qué cambia si se confirma | persona | `abierto` |

4. **Si es `CHANGE-`**, añade además una línea en el backlog de cambio del corpus
   (`docs/linea-base/LIBOX_BACKLOG_MVP_V3.md` **no se edita in-place**: el backlog de
   cambio vive en el doc 20; cuando se apruebe, el cambio se aplica con `libox-versionar-doc`).
5. **Devuelve al usuario** el ID asignado, el enlace al documento y la frase exacta registrada.
```

- [ ] **Step 3: Crear `.claude/skills/libox-outline-sync/SKILL.md`**

```markdown
---
name: libox-outline-sync
description: Republica en Outline los documentos de docs/ que tienen espejo, creando el doc en Outline y registrando su ID en scripts/outline-map.json cuando aún no está mapeado. Solo lo invoca un humano tras un merge en main.
disable-model-invocation: true
---

# Sincronizar el espejo de Outline

Publica fuera del repo: por eso solo lo dispara un humano. Entrada: `$ARGUMENTS` =
rutas a sincronizar (vacío = todas las mapeadas).

1. **Precondiciones:** estás en `main` actualizado (`git pull --ff-only`); `OUTLINE_API_KEY`
   y `OUTLINE_BASE_URL` están en el entorno o en `~/.outline-skills/config.json`.
2. **Detecta archivos sin mapear:** para cada ruta pedida, comprueba si existe como clave en
   `scripts/outline-map.json`. Si no existe:
   a. Crea el documento en Outline con el MCP (`create_document`) en la colección
      "Libox — Negocio", bajo el árbol **Desarrollo**, con el título del frontmatter y un
      cuerpo provisional de una línea.
   b. Añade `"<ruta>": "<id>"` al mapa y commitea: `chore(outline): mapea <ruta>` (rama +
      PR; el mapa vive en el repo).
3. **Sincroniza:** `scripts/outline-sync.sh <rutas>`. Lee la salida: `synced:` es éxito;
   `skip (not mapped)` significa que falta el paso 2; `skip (missing on disk)` señala una
   entrada del mapa cuyo archivo ya no existe (p. ej. rutas movidas a `docs/archive/`):
   propón al humano remapearla o quitarla.
4. **Reporta:** lista de documentos publicados con su enlace y las entradas huérfanas detectadas.
```

- [ ] **Step 4: Crear `.claude/skills/libox-pr/SKILL.md`**

````markdown
---
name: libox-pr
description: Integra trabajo terminado — comprueba rama, correo y commits, sube la rama y abre el Pull Request con la plantilla del equipo (sin trailers de IA). Úsalo cuando el trabajo esté verificado y listo para revisión.
---

# Abrir un Pull Request conforme

1. **Comprobaciones** (todas deben pasar; si una falla, corrígela antes de seguir):
   - `git branch --show-current` ≠ `main` y con formato `<type>/<kebab>`.
   - `git config user.email` termina en `@liboxapp.com`.
   - `git log origin/main..HEAD --format=%B` no contiene `Co-Authored-By`, `Generated with`
     ni `noreply@anthropic.com`; cada asunto sigue Conventional Commits en español.
   - Árbol limpio (`git status --porcelain` vacío) y verificación del cambio ya ejecutada
     (tests, `verify_corpus.py` si tocó el canon, `markdownlint` si tocó `docs/`).
2. **Sube la rama:** `git push -u origin $(git branch --show-current)` (si ya existía y se
   rebasó: `--force-with-lease`).
3. **Abre el PR** con `gh pr create --base main --title "<type>(<scope>): <resumen>" --body-file <archivo>`
   cuyo cuerpo sigue exactamente:

   ```
   ## Qué
   <una o dos frases>

   ## Por qué
   <motivo, hallazgo o decisión que lo origina; enlaza spec/ADR/ASS si existe>

   ## Verificación
   - [ ] <comando ejecutado y resultado>
   ```

   Nunca añadas "Generated with Claude Code" ni menciones de la herramienta.
4. **Devuelve** la URL del PR y, si el CI tiene checks requeridos, recuerda que el merge es
   rebase-and-merge.
````

- [ ] **Step 5: Verificar frontmatter de los cuatro skills**

Run:

```bash

for s in libox-versionar-doc libox-registrar-hallazgo libox-outline-sync libox-pr; do python3 - "$s" <<'PY'
import sys, re
p = ".claude/skills/%s/SKILL.md" % sys.argv[1]
t = open(p, encoding="utf-8").read()
m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
assert m and "name: " + sys.argv[1] in m.group(1) and "description:" in m.group(1), p
print("ok", p)
PY
done

```

Expected: cuatro líneas `ok`.

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/libox-versionar-doc .claude/skills/libox-registrar-hallazgo .claude/skills/libox-outline-sync .claude/skills/libox-pr
git commit -m "feat(os-ia): skills Libox — versionar doc del canon, registrar hallazgo, outline-sync y PR

Procedimientos cortos que apuntan al canon en vez de copiarlo.
libox-outline-sync solo se invoca por humanos (publica fuera del repo)."
```

---

### Task 7: Agentes Libox

**Files:**
- Create: `.claude/agents/redactor-docs.md`
- Create: `.claude/agents/auditor-corpus.md`
- Create: `.claude/agents/revisor-pr.md`

**Interfaces:**
- Consumes: rules de la Tarea 1, skills de la Tarea 6.
- Produces: subagentes `redactor-docs`, `auditor-corpus`, `revisor-pr` (todos `model: opus`), referenciados por el manual (Tarea 8).

- [ ] **Step 1: Crear `.claude/agents/redactor-docs.md`**

```markdown
---
name: redactor-docs
description: Redacta o edita documentación no canónica del wiki (docs/equipo, docs/flujos, glosario, specs y planes) siguiendo el estilo del proyecto. Para documentos del canon solo prepara el borrador de la versión siguiente. Úsalo para tareas de escritura de más de un párrafo.
tools: Read, Grep, Glob, Write, Edit
model: opus
skills: [libox-versionar-doc]
---

Eres el redactor técnico del equipo Libox. Escribes en español, prosa directa y sin
relleno, siguiendo `docs/equipo/estilo-documentacion.md` y la rule `.claude/rules/docs.md`
(frontmatter completo, links markdown relativos, ~150 líneas por documento).

Reglas duras:
- El producto es **Libox**; "Sortibox" y "ALAZAR" son legacy y solo aparecen al enunciar esa regla.
- Nunca editas un documento de `docs/linea-base/` in-place. Si el brief pide cambiar el canon,
  produces el borrador completo como `X_V<n+1>.md` y devuelves el control para que el
  orquestador siga `libox-versionar-doc`.
- No citas `docs/archive/` como fuente vigente.
- Claims legales llevan `[LEGAL→ABOGADO]`.
- No tocas `src/`, no haces commits ni abres PRs.

Al terminar devuelve: rutas creadas o modificadas, un resumen de cinco líneas de lo que
cambió y cualquier duda que hayas resuelto con un supuesto (marcada como tal).
```

- [ ] **Step 2: Crear `.claude/agents/auditor-corpus.md`**

```markdown
---
name: auditor-corpus
description: Audita la coherencia del corpus canónico — ejecuta verify_corpus.py y cruza cifras, reglas y decisiones entre documentos para detectar contradicciones que el script no cubre. Solo lee; devuelve hallazgos clasificados. Úsalo antes de emitir una versión o cuando se sospeche una incoherencia.
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit, MultiEdit
model: opus
---

Eres el auditor documental de Libox. Trabajas solo en lectura sobre `docs/linea-base/`
(gobernado por el Registro Maestro V6; precedencia L0 > L2 > L3 > L4, VIES en marca).

Procedimiento:
1. Ejecuta `python3 verify_corpus.py --dir docs/linea-base` y anota el resultado literal.
2. Para el alcance del brief, cruza entre documentos: cifras compartidas (comisiones, plazos,
   límites), reglas de negocio, estados y transiciones, nombres de entidades del esquema SQL y
   rutas del OpenAPI, y decisiones (ASS-001 custodia, ASS-002 stack) frente a lo que cada
   documento afirma.
3. Cada hallazgo se reporta con: documento y sección de cada lado, cita textual mínima,
   por qué es contradicción (no estilo), severidad (`bloquea construcción` /
   `riesgo legal-patrimonial` / `menor`) y clasificación propuesta para
   `libox-registrar-hallazgo` (`ASS-`, `CHANGE-`, `RISK-`).

No propones redacciones nuevas ni modificas archivos. No confundes preferencia de estilo con
incoherencia. Devuelve el informe en español, ordenado por severidad, y termina con la
lista de lo que revisaste sin encontrar problemas (para que el orquestador sepa la cobertura).
```

- [ ] **Step 3: Crear `.claude/agents/revisor-pr.md`**

```markdown
---
name: revisor-pr
description: Revisa un Pull Request del repo Libox contra CONTRIBUTING.md y las rules del OS — convención de commits, correo de autoría, trailers de IA, links relativos, frontmatter, y que no toque el canon in-place ni src/ congelado. Solo lee. Úsalo antes de aprobar o mergear.
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit, MultiEdit
model: opus
---

Eres el revisor de PRs del equipo Libox. Recibes un número de PR o una rama. Solo lees:
`gh pr view <n> --json title,body,commits,files`, `gh pr diff <n>` o `git diff origin/main...<rama>`.

Lista de comprobación (marca cada punto como pasa / falla con evidencia):
1. Commits: Conventional Commits en español; sin `Co-Authored-By`, `Generated with Claude`
   ni `noreply@anthropic.com`; correos de autoría `@liboxapp.com`.
2. Cuerpo del PR con secciones Qué / Por qué / Verificación y sin menciones a la herramienta.
3. Ningún archivo `_V<n>` existente de `docs/linea-base/` modificado; si hay versión nueva,
   el mismo PR actualiza `BASELINE` en `verify_corpus.py` y el Registro Maestro (CD-11).
4. Nada bajo `src/` ni en la config del scaffold mientras exista `.claude/rules/src-congelado.md`
   (excepto `src/**/CLAUDE.md`), salvo que el PR declare la válvula de escape y el motivo.
5. Docs: frontmatter completo, links relativos que resuelven, español, sin "Sortibox"/"ALAZAR"
   fuera de la regla de naming y de `docs/archive/`.
6. Si toca `scripts/hooks/` o `.claude/settings.json`: tests presentes y `hooks.yml` verde.

Devuelve un veredicto `APROBAR` o `CAMBIOS` seguido de la lista puntual (archivo:línea →
qué corregir). No reescribes código ni docs; no comentas en GitHub.
```

- [ ] **Step 4: Verificar frontmatter de los tres agentes**

Run:

```bash

for a in redactor-docs auditor-corpus revisor-pr; do python3 - "$a" <<'PY'
import sys, re
p = ".claude/agents/%s.md" % sys.argv[1]
t = open(p, encoding="utf-8").read()
m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
fm = m.group(1) if m else ""
assert "name: " + sys.argv[1] in fm and "model: opus" in fm and "description:" in fm, p
print("ok", p)
PY
done

```

Expected: tres líneas `ok`.

- [ ] **Step 5: Commit**

```bash
git add .claude/agents/
git commit -m "feat(os-ia): agentes Libox en Opus — redactor de docs, auditor de corpus y revisor de PR

Encarnan la regla Fable orquesta / Opus ejecuta. Agnósticos al stack;
los agentes de desarrollo llegan con el cierre de ASS-002."
```

---

### Task 8: Manual del OS, migraciones de docs y referencias

**Files:**
- Create: `docs/equipo/sistema-operativo-ia.md`
- Create: `docs/equipo/estilo-documentacion.md` (contenido migrado desde `../Context/estilo-documentacion.md`, adaptado)
- Move: `docs/onboarding.md` → `docs/equipo/onboarding.md` (y actualizar)
- Modify: `docs/README.md` (fila `equipo/` y link de onboarding)
- Modify: `CONTRIBUTING.md:72`, `.github/CODEOWNERS`, `.github/workflows/commitlint.yml` (referencias a `docs/onboarding.md`)

**Interfaces:**
- Consumes: todo lo anterior (el manual lo describe).
- Produces: `docs/equipo/` como destino de la lectura obligatoria; `CLAUDE.md` (Tarea 9) apunta aquí.

- [ ] **Step 1: Crear `docs/equipo/sistema-operativo-ia.md`**

```markdown
---
title: Sistema operativo de IA — cómo trabaja Claude Code en Libox
status: vigente
tags: [equipo, claude-code, hooks, skills, agentes, memoria]
updated: 2026-08-30
description: Manual humano de la capa operativa de IA del repo — qué carga Claude, qué hace cumplir el harness, qué skills y agentes existen, cómo se orquesta y cómo se extiende.
---

# Sistema operativo de IA

Capa operativa de Claude Code del equipo Libox. Está **versionada en este repo** y se
aplica sola al clonar: cualquier integrante (y su Claude) trabaja con las mismas reglas,
guards, skills y agentes. Diseño completo en el
[spec](../superpowers/specs/2026-08-30-sistema-operativo-ia-design.md).

## Las cinco capas

| Capa | Dónde vive | Qué hace |
|---|---|---|
| Contexto | [`CLAUDE.md`](../../CLAUDE.md) (raíz, ~40 líneas) · `.claude/rules/*.md` | Lo que toda sesión sabe. Las rules con `paths:` se inyectan solo al tocar su zona: `linea-base.md` (canon), `docs.md`, `src-congelado.md` (ASS-002), `git.md`. |
| Enforcement | `.claude/settings.json` → `scripts/hooks/*.py` | Hooks nativos que bloquean lo bloqueante. Tests en `scripts/hooks/tests/`, CI en `hooks.yml`. Hookify se conserva como segunda línea. |
| Capacidades | `.claude/skills/libox-*` · `.claude/agents/*.md` | Procedimientos invocables y subagentes especializados. |
| Manual | `docs/equipo/` | Este documento, el [estilo](estilo-documentacion.md) y el [onboarding](onboarding.md). |
| Memoria | `docs/` · rules · auto-memory personal | Ver "Memoria: qué va dónde". |

## Cómo trabaja una sesión

1. Al arrancar, dos hooks imprimen el digest de actividad del equipo y el estado del OS
   (rama, freeze de `src/`, `verify_corpus`).
2. Lee [`docs/README.md`](../README.md); identifica la zona que vas a tocar. La rule de
   esa zona se carga sola cuando abres un archivo de ella.
3. Si existe un skill para la tarea, úsalo: `/libox-versionar-doc`, `/libox-registrar-hallazgo`,
   `/libox-pr`; `/libox-outline-sync` lo dispara solo un humano.
4. Para trabajo sustancial, delega en un agente (siguiente sección) y verifica su resultado.
5. Integra con `libox-pr`. `main` solo recibe PRs con rebase-and-merge.

## Orquestación: Fable orquesta, Opus ejecuta

Cuando el modelo de la sesión es Fable, **orquesta en lugar de teclear**: descompone,
delega el trabajo sustancial (redacción larga, auditorías, revisiones, y —cuando exista
código— features, refactors y suites de tests) en subagentes con `model: opus`, y sintetiza.

- **Brief autocontenido:** objetivo, archivos en alcance, reglas aplicables (o la rule que
  las contiene), criterios de aceptación y qué debe devolver.
- **No se delega** lo trivial, el análisis puro ni las operaciones de git/PR.
- **Gate de revisión:** nunca se releva un "listo" sin verificar — leer el diff, correr los
  checks. Si un worker falla dos veces con el mismo brief, el orquestador toma el control.
- Reconocimiento amplio del repo: agente `Explore` con `model: sonnet`.
- En sesiones con Opus o inferior, se trabaja directo.

Agentes disponibles: `redactor-docs` (escribe docs no canónicos y borradores de V(n+1)),
`auditor-corpus` (solo lectura; hallazgos clasificados), `revisor-pr` (solo lectura;
veredicto aprobar/cambios).

## Guards activos y válvulas de escape

| Guard | Bloquea | Válvula |
|---|---|---|
| B1 | `git commit` con trailer de co-autoría de IA | Ninguna: regla firme. |
| B2 | `git push` a `main` | Ninguna: abre PR. |
| B3 | commit que toca `docs/linea-base/` o `verify_corpus.py` con fallos (CD-10) | Corregir hasta cero fallos. |
| B4 | commit con correo fuera de `@liboxapp.com` | `git config user.email <tu>@liboxapp.com`. |
| E1 | editar in-place un archivo `_V<n>` existente del canon | `LIBOX_PERMITIR_INPLACE=1` (solo con acuerdo explícito). |
| E2 | escribir en `src/**` o en la config del scaffold (ASS-002); `src/**/CLAUDE.md` exento | `LIBOX_DESCONGELAR_SRC=1` para fixes al PR #15 o exigencias del CI. |
| E3 | pregunta si el contenido nuevo menciona Sortibox/ALAZAR fuera de `docs/archive/` | Confirmar en el prompt. |

Las variables se ponen en el entorno al lanzar Claude Code o en `"env"` de
`.claude/settings.local.json` (personal, gitignorado). Un fallo interno de un guard nunca
bloquea: ante error, permite.

## Memoria: qué va dónde

| Capa | Guarda | Autoridad |
|---|---|---|
| `docs/` (repo) | Hechos, decisiones y procedimientos del proyecto | Canónica |
| `.claude/rules/` | Reglas operativas por zona | Canónica |
| Auto-memory personal (`~/.claude/projects/<repo>/memory/`) | Preferencias de trabajo de cada persona | Personal; nunca hechos del proyecto |
| claude-mem, agentes GSD | — | Retirados ([ADR Z.8](../archive/decisions/Z8-roles-memoria-contexto.md)); desactivados a nivel proyecto |

Si algo valioso aparece en la memoria personal, se promueve a `docs/` por PR.

## Cómo extender el OS

- **Regla nueva:** archivo en `.claude/rules/` con `paths:` si es por zona; una regla, un lugar.
- **Guard nuevo:** función pura en `scripts/hooks/`, test rojo primero en `scripts/hooks/tests/`,
  wiring en `.claude/settings.json`; `hooks.yml` debe quedar verde.
- **Skill nuevo:** `.claude/skills/libox-<verbo>/SKILL.md`, menos de 80 líneas, apunta al canon.
- **Agente nuevo:** `.claude/agents/<rol>.md` con `model: opus`, herramientas mínimas y
  `disallowedTools` si solo lee.
- Todo entra por PR revisado por `revisor-pr` o por Diego (`CODEOWNERS`).

## Capa `dev` pendiente (ASS-002)

Cuando los socios ratifiquen el stack, el PR que cierre ASS-002 borra
`.claude/rules/src-congelado.md` y las constantes `FROZEN_*` de `guard_edit.py`, actualiza
`src/CLAUDE.md` y añade agentes `ejecutor-feature`, `tester` y `depurador` más una rule de
desarrollo para `src/`. Nada de esta capa cambia.
```

- [ ] **Step 2: Crear `docs/equipo/estilo-documentacion.md`** (migración adaptada: idioma de conversación en español, ADRs históricos, ruta del método)

````markdown
---
title: Estilo de documentación — Libox
status: vigente
tags: [estilo, documentacion, convenciones]
updated: 2026-08-30
description: Cómo escribimos la documentación del proyecto. Idioma, frontmatter, links, longitud, tono y cómo se registran las decisiones.
---

# Estilo de documentación — Libox

Reglas de *cómo* se escribe. Complementan el
[sistema operativo de IA](sistema-operativo-ia.md) y aplican a todo documento del proyecto.
La rule `.claude/rules/docs.md` es su versión condensada para Claude.

## Idioma

- **Documentación y conversación con el equipo: español** (mercado peruano).
- **Código, identificadores y nombres de archivo: inglés.** Commits: Conventional Commits
  con asunto y cuerpo en español.

## Frontmatter

Todo doc del wiki (salvo el corpus congelado de `docs/linea-base/`) lleva YAML al inicio:

```yaml
---
title: <título legible>
status: <vigente | borrador | obsoleto | aprobado>
tags: [<...>]
updated: <YYYY-MM-DD>
description: <una línea para decidir si vale la pena abrirlo>
---
```

## Links

- **Markdown estándar** `[texto](ruta.md)`, nunca wikilinks `[[...]]` (reservados a los
  archivos de memoria privada).
- Rutas **relativas al archivo** que las contiene; el CI (`lychee --offline`) falla si un
  link relativo no resuelve.

## Longitud y estructura

- Notas atómicas y enlazadas. Cuando un doc pasa de **~150 líneas**, partirlo.
- `CLAUDE.md` y `MEMORY.md` se mantienen magros: se cargan cada sesión. El contenido va en
  `docs/`; esos archivos solo llevan reglas y punteros.

## Tono

- Prosa clara y directa. Si una palabra se puede quitar sin perder sentido, se quita.
- Negritas, encabezados y listas solo cuando aportan claridad.
- Claims legales marcados `[LEGAL→ABOGADO]`; nunca presentarlos como asesoría cerrada.

## Decisiones

La línea de ADRs Z.1–Z.8 es **histórica** (`docs/archive/decisions/`). Las decisiones
nuevas siguen el control del corpus: hallazgo → `libox-registrar-hallazgo` (ASS-/CHANGE-/
RISK- en el doc 20 de Outline) → si se aprueba, nueva versión del documento del canon con
`libox-versionar-doc`. No se abren ADRs Z nuevos.
````

- [ ] **Step 3: Mover y actualizar el onboarding**

```bash
mkdir -p docs/equipo && git mv docs/onboarding.md docs/equipo/onboarding.md
```

Luego reemplazar el contenido completo de `docs/equipo/onboarding.md` por:

```markdown
---
title: Onboarding de desarrolladores
status: vigente
tags: [equipo, onboarding, claude-code]
updated: 2026-08-30
description: Checklist para incorporarte al equipo Libox con el entorno completo funcionando (accesos, repo, Claude Code, lectura obligatoria, flujo diario).
---

# Onboarding de desarrolladores

Checklist para incorporarte al equipo Libox con el entorno completo
funcionando. Tiempo estimado: ~30 minutos.

## 1. Accesos

- [ ] Añade y **verifica** tu correo **`@liboxapp.com`** en tu cuenta de
  GitHub (*Settings → Emails*). **Requisito previo a la invitación** — Diego
  no invita cuentas sin el correo de la org verificado.
- [ ] Desactiva *Settings → Emails → "Block command line pushes that expose
  my email"* — con ese toggle activo, GitHub rechaza tus pushes con el error
  **GH007** (este repo commitea con el correo corporativo visible).
- [ ] Invitación a la organización GitHub **`liboxapp`** (te la envía Diego).
- [ ] Seat en **Claude Team** con acceso a Claude Code (te lo asigna Diego).
- [ ] Cuenta en Outline (`liboxapp.getoutline.com`) — capa compartible del
  wiki con los socios.

## 2. Repo y entorno de Claude Code

- [ ] Clona el repo: `git clone https://github.com/liboxapp/libox.git`
- [ ] Configura el correo corporativo **local al repo**:
  `git config user.email "tu@liboxapp.com"`. El guard B4 bloquea commits con
  otro dominio y el CI rechaza PRs con commits fuera de `@liboxapp.com`.
- [ ] Python 3.9 o superior disponible como `python3` (lo usan los guards y
  `verify_corpus.py`).
- [ ] Instala [Claude Code](https://claude.com/claude-code) (CLI, app de
  escritorio o extensión del IDE).
- [ ] Abre el repo con Claude Code. El **sistema operativo de IA** está
  versionado y se aplica solo: reglas por ruta, guards (co-autoría, push a
  `main`, canon in-place, `src/` congelado, naming), skills `libox-*`, agentes
  y plugins del equipo. En el primer arranque acepta la instalación de los
  plugins y del marketplace `context-mode` cuando Claude Code lo pida. Cada
  sesión empieza con el digest de actividad y el bloque "Estado del OS de IA".
- [ ] Autentica GitHub CLI: `gh auth login` — sin esto, el digest falla en
  silencio y `gh pr create` no funciona.
- [ ] Conecta el **MCP de Outline** en tu cuenta de claude.ai (Settings →
  Connectors) para leer/escribir la capa compartible desde Claude.
- [ ] Tu configuración personal va en `.claude/settings.local.json` —
  **nunca se commitea** (ya está gitignorada). Ahí van también las válvulas
  de escape de los guards (`"env"`), solo con acuerdo explícito.

## 3. Lectura obligatoria (en este orden)

1. [`docs/README.md`](../README.md) — índice del wiki y mapa de documentos.
2. [`sistema-operativo-ia.md`](sistema-operativo-ia.md) — cómo trabaja Claude
   Code en este repo: capas, guards, skills, agentes, orquestación.
3. [`CONTRIBUTING.md`](../../CONTRIBUTING.md) — versionamiento, Conventional
   Commits en español, flujo de PRs, reglas de ingeniería duras.
4. [`CLAUDE.md`](../../CLAUDE.md) (raíz) — reglas firmes y punteros.
5. [`estilo-documentacion.md`](estilo-documentacion.md) — cómo se escribe.
6. [`src/CLAUDE.md`](../../src/CLAUDE.md) — reglas de código para cuando se
   levante el freeze de ASS-002.
7. Los 8 ADRs históricos de [`docs/archive/decisions/`](../archive/decisions/README.md)
   — contexto de las decisiones; no se reabren sin evidencia nueva.

## 4. Flujo de trabajo diario

- Rama por cambio: `<type>/<short-kebab-name>` desde `main` actualizado.
- Commits = Conventional Commits **en español** (los valida `commitlint`).
- PR con `/libox-pr` → checks (`commitlint`, `markdownlint`, `links`,
  `verify-corpus`, `hooks`) → **rebase-and-merge** (único método habilitado).
- El código es en inglés; todo lo user-facing y la conversación con Claude,
  en español (Perú).
- La verdad del proyecto vive en `docs/` (versionada). La memoria automática
  de Claude es **personal por máquina** — nada importante puede vivir solo
  ahí: se promueve a `docs/` por PR.

## 5. Para Diego al incorporar cada dev

- [ ] Verificar que el dev ya tiene su correo `@liboxapp.com` **verificado**
  en su cuenta GitHub (pedirle captura de *Settings → Emails*); solo
  entonces invitar.
- [ ] Invitar al team `core` de la org con rol *write*.
- [ ] Asignar seat de Claude Team.
- [ ] Al pasar de 1 colaborador: subir el ruleset de `main` a **1 approval
  requerido** y activar **require code owner review** (el
  [`CODEOWNERS`](../../.github/CODEOWNERS) ya está listo).
- [ ] Verificar que el secreto `RELEASE_PLEASE_TOKEN` (PAT fine-grained)
  sigue vigente; documentar fecha de expiración y rotación.
```

- [ ] **Step 4: Actualizar `docs/README.md`**

Reemplazar la fila:

```

| [`glosario.md`](glosario.md) · [`onboarding.md`](onboarding.md) · [`flujos/`](flujos/) | Documentos de trabajo, no normativos | Consulta |

```

por estas dos:

```

| [`equipo/`](equipo/) | Cómo trabaja el equipo: [sistema operativo de IA](equipo/sistema-operativo-ia.md) (capas, guards, skills, agentes, orquestación) · [estilo de documentación](equipo/estilo-documentacion.md) · [onboarding](equipo/onboarding.md) | Al incorporarte y cada vez que extiendas la configuración de Claude |
| [`glosario.md`](glosario.md) · [`flujos/`](flujos/) · [`superpowers/`](superpowers/) | Documentos de trabajo, no normativos (glosario, flujos, specs y planes aprobados) | Consulta |

```

Y en el frontmatter, `updated: 2026-08-30` se mantiene.

- [ ] **Step 5: Actualizar las referencias entrantes a `docs/onboarding.md`**

```bash
sed -i '' 's#docs/onboarding.md#docs/equipo/onboarding.md#g' .github/CODEOWNERS .github/workflows/commitlint.yml
sed -i '' 's#\[`docs/onboarding.md`\](docs/onboarding.md)#[`docs/equipo/onboarding.md`](docs/equipo/onboarding.md)#' CONTRIBUTING.md
printf '\n# Manual del equipo y del sistema operativo de IA\n/docs/equipo/       @DianCotrina\n' >> .github/CODEOWNERS
git grep -n "docs/onboarding.md" -- ':!docs/superpowers' ':!docs/archive' || echo "sin referencias viejas"

```

Expected: la última línea imprime `sin referencias viejas`.

- [ ] **Step 6: Lint y verificación de links relativos**

Run:

```bash

npx --no-install markdownlint-cli2 "docs/equipo/*.md" "docs/README.md" 2>&1 | tail -2
python3 - <<'PY'
import re, os, glob
bad = []
for f in glob.glob("docs/equipo/*.md") + ["docs/README.md"]:
    for m in re.finditer(r"\]\(([^)#\s]+)(#[^)]*)?\)", open(f, encoding="utf-8").read()):
        t = m.group(1)
        if t.startswith(("http://", "https://", "mailto:")):
            continue
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), t))):
            bad.append((f, t))
print("links rotos:", bad or "ninguno")
PY

```

Expected: `Summary: 0 issues` y `links rotos: ninguno`.

- [ ] **Step 7: Commit**

```bash
git add docs/equipo docs/README.md CONTRIBUTING.md .github/CODEOWNERS .github/workflows/commitlint.yml
git commit -m "docs(os-ia): manual del sistema operativo de IA en docs/equipo y migración del onboarding

Absorbe el método y el estilo que vivían fuera del repo (folder Context de
Cowork), actualiza el onboarding con los guards y la lectura obligatoria,
y mueve las referencias entrantes a la nueva ruta."
```

---

### Task 9: `CLAUDE.md` magro y banner en `src/CLAUDE.md`

**Files:**
- Modify: `CLAUDE.md` (reemplazo completo)
- Modify: `src/CLAUDE.md` (banner al inicio + sección de orquestación reducida a puntero)

**Interfaces:**
- Consumes: rules (Tarea 1), skills (Tarea 6), manual (Tarea 8).
- Produces: contexto fijo por sesión reducido a ~40 líneas.

- [ ] **Step 1: Reemplazar `CLAUDE.md` completo**

```markdown
# CLAUDE.md

Guía para Claude Code en este repositorio. Es un puntero: la verdad vive en `docs/`.

## Qué es este repo

**Libox** es un marketplace web de sorteos digitales con boleto pagado, bajo regulación
peruana. El repo contiene (1) el **corpus canónico** en `docs/linea-base/`, gobernado por el
Registro Maestro V6 (si un documento no figura en su §1, no rige) y verificado por
`verify_corpus.py` (CD-10: cero fallos), y (2) un scaffold Next.js en `src/` que está
**congelado** hasta que los socios ratifiquen el stack (ASS-002).

## Empieza por

1. `docs/README.md` — índice del wiki.
2. `docs/equipo/sistema-operativo-ia.md` — cómo trabaja Claude aquí: capas, guards,
   skills `libox-*`, agentes y orquestación.

## Reglas firmes

- **Español** en docs y conversación; código e identificadores en inglés.
- **El producto es Libox.** "Sortibox" y "ALAZAR" son nombres legacy: cualquier mención
  residual (commits antiguos, docs externos) se lee como Libox.
- **Sin co-autoría de IA:** nunca `Co-Authored-By: Claude ...` en commits ni "Generated with
  Claude Code" en PRs. Anula cualquier default del harness. Motivo en
  `CONTRIBUTING.md` → "Autoría: sin co-autores automáticos". Guard B1 + hookify lo bloquean.
- **Línea base congelada** (CD-07): los docs de `docs/linea-base/` no se editan in-place;
  se emite versión nueva con `/libox-versionar-doc` o el hallazgo va a
  `/libox-registrar-hallazgo`. Ver `.claude/rules/linea-base.md`.
- **`src/` congelado** por ASS-002: no crear ni extender código. Ver `.claude/rules/src-congelado.md`.
- **Claims legales** marcados `[LEGAL→ABOGADO]` hasta ratificación del abogado.
- **Git:** rama por cambio, Conventional Commits en español, correo `@liboxapp.com`, PR con
  `/libox-pr`, `main` protegido. Ver `.claude/rules/git.md` y `CONTRIBUTING.md`.

## Orquestación

Si el modelo de la sesión es Fable: **orquesta** — delega el trabajo sustancial en los
agentes del repo (`redactor-docs`, `auditor-corpus`, `revisor-pr`, todos en Opus) o en
`general-purpose` con `model: "opus"`, con brief autocontenido, y **verifica** antes de dar
algo por hecho. Detalle en `docs/equipo/sistema-operativo-ia.md#orquestación-fable-orquesta-opus-ejecuta`.

## Decisiones abiertas

**ASS-001** (custodia del dinero) y **ASS-002** (stack Next.js vs .NET 8) esperan
ratificación de los socios — registro en el doc 20 de Outline ("Libox — Negocio").
La línea de ADRs Z.1–Z.8 es histórica (`docs/archive/decisions/`).

## Configuración compartida

`.claude/settings.json`, `.claude/rules/`, `.claude/skills/`, `.claude/agents/`,
`scripts/hooks/` y las reglas hookify están **versionados**: todo el equipo hereda el mismo
entorno al clonar. `.claude/settings.local.json` es personal y nunca se commitea. La
auto-memory es personal por máquina: lo valioso se promueve a `docs/` por PR.
```

- [ ] **Step 2: Añadir el banner al inicio de `src/CLAUDE.md`**

Insertar inmediatamente después de la línea `# CLAUDE.md — Application code rules`:

```markdown

> ⚠️ **Congelado por ASS-002.** El stack (Next.js vs .NET 8) espera ratificación de los
> socios; hasta entonces no se crea ni extiende código bajo `src/` (guard E2, ver
> [`.claude/rules/src-congelado.md`](../.claude/rules/src-congelado.md)). Este archivo
> sigue siendo la spec de código para cuando se levante el freeze.
```

- [ ] **Step 3: Reducir la sección de orquestación de `src/CLAUDE.md` a un puntero**

Reemplazar toda la sección desde `## Model orchestration (Fable → Opus)` hasta la línea anterior a `## Hard engineering rules` por:

```markdown
## Model orchestration (Fable → Opus)

Canonical in [`docs/equipo/sistema-operativo-ia.md`](../docs/equipo/sistema-operativo-ia.md)
(section "Orquestación"): Fable orchestrates, Opus executes via the repo agents or a
`general-purpose` agent with `model: "opus"`; self-contained briefs; never relay a
worker's "done" unverified.

```

- [ ] **Step 4: Verificar tamaño, lint y links**

Run:

```bash

wc -l CLAUDE.md
npx --no-install markdownlint-cli2 CLAUDE.md src/CLAUDE.md 2>&1 | tail -1
test -f .claude/rules/src-congelado.md && test -f docs/equipo/sistema-operativo-ia.md && echo "links OK"

```

Expected: `CLAUDE.md` ≤ 60 líneas, `Summary: 0 issues`, `links OK`.

- [ ] **Step 5: Commit**

```bash
git add CLAUDE.md src/CLAUDE.md
git commit -m "docs(os-ia): CLAUDE.md raíz magro y banner de freeze en src/CLAUDE.md

El contexto fijo por sesión pasa de 96 líneas narrativas a reglas firmes y
punteros; el detalle vive en docs/equipo y en .claude/rules por zona."
```

---

### Task 10: Higiene del entorno local y memoria (sin commit)

**Files:**
- Delete (fuera del repo): `~/.claude/agents/gsd-*.md` (33 archivos)
- Delete (local, gitignorado): `.claude/worktrees/mvp1-dev-phases/`
- Modify (personal, gitignorado): `.claude/settings.local.json`
- Modify (fuera del repo): `~/.claude/projects/-Users-diegocotrina-Claude-Cowork-Liboxapp-Libox/memory/MEMORY.md`
- Modify (fuera del repo): `../Context/README.md`, `../Context/estilo-documentacion.md`

**Interfaces:** ninguna; todo es estado local de la máquina de Diego. **No tocar** `.agents/skills/outline-skills` (no autorizado).

- [ ] **Step 1: Retirar los agentes GSD a nivel usuario (autorizado por Diego)**

```bash
ls ~/.claude/agents/gsd-*.md | wc -l && rm ~/.claude/agents/gsd-*.md && ls ~/.claude/agents/ | wc -l

```

Expected: `33`, luego `0` (o solo archivos no-gsd si los hubiera).

- [ ] **Step 2: Retirar el worktree huérfano (autorizado)**

```bash
git worktree prune && git worktree list && rm -rf .claude/worktrees/mvp1-dev-phases && ls .claude/worktrees 2>/dev/null || echo "sin worktrees"

```

Expected: `git worktree list` muestra solo la raíz en `main`/rama actual; al final `sin worktrees` o directorio vacío.

- [ ] **Step 3: Calcular la poda de `settings.local.json` y mostrarla a Diego antes de aplicar**

```bash
python3 - <<'PY'
import json, re, os
p = ".claude/settings.local.json"
d = json.load(open(p))
allow = d["permissions"]["allow"]
STALE = re.compile(r"Desktop/liboxapp|ALAZAR|docs/plans/|docs/decisions/|docs/prd/|gsd|get-shit-done|claude-mem|Claude/Projects/|rm -rf \.claude/skills|rmdir \.claude/skills")
def dead_path(e):
    m = re.match(r"^(Read|Edit|Write)\(//(.+?)\**\)$", e)
    return bool(m) and not os.path.exists("/" + m.group(2).rstrip("/*"))
drop = [e for e in allow if STALE.search(e) or dead_path(e)]
keep = [e for e in allow if e not in drop]
print("Se quitarían %d de %d entradas:" % (len(drop), len(allow)))
for e in drop: print("  -", e)
json.dump(drop, open("/tmp/settings-local-drop.json", "w"))
PY
```

El orquestador muestra esa lista a Diego. **Solo tras su OK explícito:**

```bash
python3 - <<'PY'
import json
p = ".claude/settings.local.json"
d = json.load(open(p)); drop = set(json.load(open("/tmp/settings-local-drop.json")))
d["permissions"]["allow"] = [e for e in d["permissions"]["allow"] if e not in drop]
json.dump(d, open(p, "w"), indent=2, ensure_ascii=False); open(p, "a").write("\n")
print("entradas restantes:", len(d["permissions"]["allow"]))
PY
python3 -c "import json;json.load(open('.claude/settings.local.json'));print('JSON OK')"
```

- [ ] **Step 4: Reescribir `MEMORY.md` personal**

Contenido completo de `~/.claude/projects/-Users-diegocotrina-Claude-Cowork-Liboxapp-Libox/memory/MEMORY.md`:

```markdown
# MEMORY.md — índice de memoria del proyecto Libox

La verdad del proyecto vive en el repo: `docs/README.md` y `docs/equipo/sistema-operativo-ia.md`.
Aquí solo preferencias personales de trabajo.

- [Orquestación Fable/Opus](orquestacion-fable-opus.md) — preferencia de Diego; la regla canónica está en `docs/equipo/sistema-operativo-ia.md#orquestación-fable-orquesta-opus-ejecuta`
```

- [ ] **Step 5: Convertir `Context/` en puntero**

Contenido completo de `../Context/README.md`:

```markdown
---
title: Operación de Cowork — Libox
status: vigente
tags: [cowork, metodo]
updated: 2026-08-30
description: Puntero al manual del equipo, que ahora vive versionado en el repo.
---

# Operación de Cowork — Libox

El manual de operación y el estilo de documentación viven en el repo:
`Libox/docs/equipo/sistema-operativo-ia.md` y `Libox/docs/equipo/estilo-documentacion.md`.

En Cowork se mantienen los otros dos folders con su rol de siempre: **Cowork station**
(borradores y trabajo en curso, nada permanente) y **Output** (entregables terminados:
actas, reportes, exports). Lo canónico entra al repo por PR.
```

Contenido completo de `../Context/estilo-documentacion.md`:

```markdown
---
title: Estilo de documentación — puntero
status: obsoleto
tags: [estilo]
updated: 2026-08-30
description: Migrado al repo.
---

Migrado a `Libox/docs/equipo/estilo-documentacion.md` el 2026-08-30.
```

- [ ] **Step 6: Verificar que el repo sigue limpio (la higiene no genera cambios trackeados)**

Run: `git status --porcelain`
Expected: vacío.

---

### Task 11: Verificación final, push y Pull Request

**Files:** ninguno nuevo.

- [ ] **Step 1: Suite completa de verificación**

```bash
python3 -m unittest discover -s scripts/hooks/tests 2>&1 | tail -2
python3 verify_corpus.py --dir docs/linea-base | tail -1
npx --no-install markdownlint-cli2 2>&1 | tail -1
git log --format=%B origin/main..HEAD | grep -ciE "co-authored-by|generated with|noreply@anthropic" || true
git status --porcelain | wc -l
```

Expected, en orden: `OK` (41 tests) · `RESULTADO: sin fallos, 0 avisos...` · `Summary: 0 issues` · `0` · `0`.

- [ ] **Step 2: Revisión por `revisor-pr` (subagente) sobre la rama**

Lanzar el agente `revisor-pr` con el brief: "Revisa la rama `chore/sistema-operativo-ia` contra `origin/main` con tu lista de comprobación; el PR aún no existe, usa `git diff origin/main...HEAD` y `git log origin/main..HEAD`". Expected: veredicto `APROBAR`; si devuelve `CAMBIOS`, corregir y commitear antes de seguir.

- [ ] **Step 3: Push y PR (siguiendo `libox-pr`)**

```bash
git push -u origin chore/sistema-operativo-ia
cat > /tmp/pr-body.md <<'EOF'
## Qué
Capa operativa de Claude Code del equipo, versionada en el repo: `CLAUDE.md` magro + reglas por ruta, guards nativos testeados (co-autoría, push a `main`, CD-10, correo, canon in-place, `src/` congelado, naming), skills `libox-*`, agentes en Opus, manual en `docs/equipo/` y CI `hooks.yml`.

## Por qué
Reproducibilidad para nuevos devs, enforcement automático del canon y flujo orquestado Fable/Opus, sin depender de memoria personal ni del folder Context de Cowork. Agnóstico al stack hasta que se ratifique ASS-002. Spec: `docs/superpowers/specs/2026-08-30-sistema-operativo-ia-design.md`.

## Verificación
- [x] `python3 -m unittest discover -s scripts/hooks/tests` — 41 tests OK (3.9 local; CI 3.9 y 3.12)
- [x] `python3 verify_corpus.py --dir docs/linea-base` — sin fallos
- [x] `markdownlint-cli2` — 0 issues; links relativos de `docs/equipo/` resueltos
- [x] Sesión nueva: commit con trailer, push a `main`, edición de un doc `_V`, escritura en `src/` → bloqueados; escritura en `docs/equipo/` → pasa
- [x] Revisión de `revisor-pr`: APROBAR

Nota: el PR #16 (rate limiting) se rebasa después de este merge (acordado con Diego).
EOF
gh pr create --base main --title "chore(os-ia): sistema operativo de IA del equipo — rules, guards, skills, agentes y manual" --body-file /tmp/pr-body.md
```

Expected: URL del PR. Comprobar en GitHub que los checks `commitlint`, `markdownlint`, `links`, `hooks` (3.9 y 3.12) quedan verdes.

- [ ] **Step 4: Post-merge (humano)**

Tras el rebase-and-merge: (a) Diego corre `/libox-outline-sync docs/equipo/sistema-operativo-ia.md docs/equipo/estilo-documentacion.md docs/equipo/onboarding.md docs/README.md` para crear/mapear y publicar el espejo; (b) rebasar el PR #16 sobre `main` y resolver conflictos en `CLAUDE.md` / `src/CLAUDE.md` conservando la versión magra.

---

## Autorrevisión del plan contra el spec

- **§4.1 CLAUDE.md** → Tarea 9. **§4.2 rules** → Tarea 1. **§5.1 B1–B4** → Tarea 2. **§5.2 E1–E3** → Tarea 3 (E2 añade la exención `src/**/CLAUDE.md`, necesaria para que la Tarea 9 no quede bloqueada por el propio guard; se refleja en la rule y el manual). **§5.3 status** → Tarea 4. **§5.5 tests y CI** → Tareas 2–5. **§5.6 settings** → Tarea 5. **§6.1 skills** → Tarea 6. **§6.2 agentes** → Tarea 7. **§7.1–7.2 manual y migraciones** → Tarea 8 (más el puntero de `Context/` en Tarea 10). **§7.3 memoria** → Tarea 10. **§7.4 higiene** → Tareas 5 (plugins) y 10 (resto; `.agents/` intacto). **§8 entrega** → Tarea 11.
- Nombres consistentes entre tareas: `corpus_check.verify_corpus(root) -> (ok, tail)`, `guard_bash.decide(command, ctx)`, `guard_edit.decide(tool_input, root, env, exists)`, `session_status.status_lines(branch, frozen, verify_ok)`, variables `LIBOX_PERMITIR_INPLACE` / `LIBOX_DESCONGELAR_SRC`, constantes `FROZEN_PREFIX` / `FROZEN_FILES` / `FROZEN_EXEMPT_BASENAMES`.
- Conteo de tests: 17 (bash) + 20 (edit) + 4 (status) = 41.
