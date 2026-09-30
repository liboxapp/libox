---
title: Verificaciones — auditoría del harness 20260925-203710
author: Claude coordinador (claude-opus-5-5)
status: vigente
tags: [auditoria, harness, evidencia]
updated: 2026-09-25
description: Comandos ejecutados por el coordinador, con entorno, código de salida y salida saneada. Incluye el ensayo de guards en copia desechable y lo no ejecutado.
---

# Verificaciones del coordinador

Snapshot: `471a28d050a3f03c3b605649f7463822a8e157ad` ([manifiesto](manifest.md)). Salidas recortadas; sin secretos ni valores de entorno. Las pruebas de Python corrieron con `PYTHONDONTWRITEBYTECODE=1` para no ensuciar el árbol.

## 1. Snapshot y entorno (checkout real, solo lectura)

| Comando | Resultado | Exit |
|---|---|---|
| `claude --version` | `2.1.282 (Claude Code)` | 0 |
| `git rev-parse HEAD` | `471a28d050a3f03c3b605649f7463822a8e157ad` | 0 |
| `git branch --show-current` | `codex/activate-ai-audit` | 0 |
| `git status --porcelain=v1 --untracked-files=all` | Una sola línea: `?? docs/audits/20260925-203250-harness-codex/codex-report.md` (run concurrente de Codex). Una lectura anterior, a las 20:32 UTC, estaba vacía | 0 |
| Presencia de `CLAUDE_CODE_SUBAGENT_MODEL` y `ANTHROPIC_*` | Ausentes (solo presencia; sin valores) | — |

## 2. Verificaciones del manual (checkout real)

| Comando | Resultado | Exit |
|---|---|---|
| `python3 verify_corpus.py --dir docs/linea-base` | `RESULTADO: sin fallos, 0 avisos. La versión puede emitirse.` | 0 |
| `python3 -m unittest discover -s scripts/hooks/tests -v` | `Ran 53 tests … OK` | 0 |
| `python3 verify_corpus.py` (sin `--dir`, caso H-03) | `RESULTADO: 15 fallos, 0 avisos. La versión NO puede emitirse (regla CD-10).` El directorio por defecto es `.` | 1 |

Tras las pruebas, `git status` no mostró archivos nuevos del checkout.

## 3. Ensayo de guards en copia desechable (H-04 y vías de escritura)

Copia: `git archive 471a28d` en el scratchpad del coordinador, más `git init` con correo sintético `@liboxapp.com`. Cada caso envía un payload sintético al hook con `CLAUDE_PROJECT_DIR=<copia>`. `exit=2` equivale a denegar. Script: `ensayo_guards.py` (scratchpad, fuera del repo).

| ID | Hook | Caso | Exit | Decisión |
|---|---|---|---|---|
| E1 | `guard_edit.py` | Editar in-place `docs/linea-base/…_V9.md` | 2 | DENY |
| E2 | `guard_edit.py` | Escribir `src/app/page.tsx` | 2 | DENY |
| E2b | `guard_edit.py` | Escribir `package.json` | 2 | DENY |
| E3 | `guard_edit.py` | Nombre legacy sintético en `docs/nota.md` | 2 | DENY |
| OK1 | `guard_edit.py` | Escribir `docs/audits/x/manifest.md` (control) | 0 | allow |
| W1 | `guard_edit.py` | `src/app/page.tsx` dentro de `.claude/worktrees/w/` (ruta absoluta) | 0 | allow |
| W2 | `guard_edit.py` | Canon `…_V9.md` dentro de `.claude/worktrees/w/` (existente) | 0 | allow |
| S1 | `guard_bash.py` | `sed -i` sobre el canon | 0 | allow |
| S2 | `guard_bash.py` | `printf x >> src/app/page.tsx` | 0 | allow |
| S3 | `guard_bash.py` | `python3 -c` que escribe en `src/` | 0 | allow |
| B1 | `guard_bash.py` | Commit con trailer de co-autoría en `-m` | 2 | DENY |
| B1b | `guard_bash.py` | Commit `-F msg.txt` con el trailer dentro del archivo | 0 | allow |
| B2 | `guard_bash.py` | `git push origin main` | 2 | DENY |
| B2b | `guard_bash.py` | `git push` sin argumentos | 0 | allow |
| F1 | `guard_edit.py` | Payload que no es JSON | 0 | allow |

**Evento en la sesión real.** El primer intento del coordinador de lanzar este ensayo fue bloqueado por el hook B1 de la sesión (`PreToolUse:Bash hook error: Blocked by hook`). El comando no hacía commit: solo *contenía* el texto de un payload con trailer. El control actuó en vivo y su detección es textual sobre el comando completo.

## 4. CI, entrada de Codex y controles remotos

| Comprobación | Resultado |
|---|---|
| Workflows (`.github/workflows/`) | `commitlint`, `docs`, `hooks`, `outline-sync`, `release-please`, `verify-corpus` |
| Pasos de código en workflows (`npm`, `setup-node`, `dotnet`, `tsc`, `vitest`) | Ninguno |
| Control de trailers de IA en CI o `commitlint.config.cjs` | Ninguno |
| Saneo de secretos en `scripts/hooks/*.py` (H-08) | 0 coincidencias por archivo |
| `AGENTS.md` | Entrada para Codex: remite a `CLAUDE.md`, `.claude/rules/`, la skill de auditoría y el manual; conserva el bloque de Next.js (16 líneas) |
| `.github/CODEOWNERS` | Cubre `/docs/decisions/`, `/docs/plans/`, `/CONTRIBUTING.md`, `/CLAUDE.md`, `/.claude/`, `/.github/`, `/scripts/`, `/docs/equipo/`. No lista `docs/linea-base/`, `src/` ni `package.json` |
| Ruleset `main protection` (`gh api`, lectura) | Activo: `deletion`, `non_fast_forward`, `required_status_checks`, `required_linear_history`, `pull_request`. Checks obligatorios: `commitlint`, `markdownlint`, `links` |
| Métodos de merge | Solo rebase (`merge_commit=false`, `squash=false`) |

## 5. No ejecutado

| Escenario | Motivo |
|---|---|
| H-01, H-02, H-06 | Exigen correr un revisor sobre una copia manipulada; queda para un ensayo dedicado del harness |
| H-05 | No se inyectó un cambio de snapshot. Se comprobará HEAD y estado antes de sintetizar |
| H-07 | Sin reintentos por ahora. Si ocurre, se conservará el intento anterior |
| H-08 | Sin credencial sintética en flujo real: no hay saneador automatizado y el saneo es procedimental (sección 4) |
| Build, lint y typecheck de `src/` | Fuera del alcance `harness`; se registra solo que el CI no los corre |
