---
title: Sistema operativo de IA — cómo trabaja Claude Code en Libox
status: vigente
tags: [equipo, claude-code, hooks, skills, agentes, memoria]
updated: 2026-09-29
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
| Contexto | [`CLAUDE.md`](../../CLAUDE.md) (raíz) · `.claude/rules/*.md` | Lo que toda sesión sabe. Las rules con `paths:` se inyectan solo al tocar su zona: `linea-base.md` (canon), `docs.md`, `src-congelado.md` (hasta D1), `git.md`. |
| Enforcement | `.claude/settings.json` → `scripts/hooks/*.py` | Guards locales heurísticos; CI obligatorio es la barrera común. Tests en `scripts/hooks/tests/`, CI en `hooks.yml`. Hookify se conserva como segunda línea. |
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
| E2 | escribir fuera del allowlist de documentación/infraestructura durante el freeze C2/D1; incluye `src/**`, scaffold y `vitest.config.ts`; `src/**/CLAUDE.md` exento | `LIBOX_DESCONGELAR_SRC=1` solo con autorización; no exime CI. |
| E3 | escribir Sortibox/ALAZAR en contenido nuevo fuera de los archivos que enuncian la regla (`CLAUDE.md`, `CONTRIBUTING.md`, `.claude/rules\|agents\|skills`, `docs/equipo`, `docs/superpowers`) y de `docs/archive/` | `LIBOX_PERMITIR_LEGACY=1` (solo con acuerdo explícito). |

| E4 | modificar hooks, políticas CI, scripts de auditoría, settings, rules, agentes o skills | `LIBOX_EDITAR_OS=1`, con autorización y aviso en stderr. |

| E5 | sobrescribir un informe existente bajo `docs/audits/<run-id>/` | Ninguna; crear otro intento. Excluye manifest, checks y codex-prompt. |

Las variables se ponen en el entorno al lanzar Claude Code o en `"env"` de
`.claude/settings.local.json` (personal, gitignorado). Un fallo interno de un guard nunca
bloquea: ante error, permite con **AVISO** visible, sin volcar el payload.

Se comprueban rutas léxicas y reales, worktrees y mayúsculas. La inspección de Bash
no ejecuta el comando: reconoce formas Git y escrituras obvias; no es un parser
completo ni un sandbox. Un script opaco puede eludir la heurística. Codex no ejecuta
estos hooks automáticamente; aplica las mismas reglas y los checks de CI.
Los timeouts de hooks son 15 s (edición/digest), 35 s (estado) y 45 s (Bash);
Bash reserva 35 s para sus comprobaciones y limita la verificación del corpus a 20 s.

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
- Todo entra por PR con CI y revisión automatizada. La revisión humana sigue
  suspendida hasta que Diego la reactive explícitamente.

## Capa `dev` pendiente (C2/D1)

El backend es Go (D-10) y el frontend TypeScript. Tras emitir L3 V8, el PR de D1 retira
`.claude/rules/src-congelado.md` y las constantes `FROZEN_*` de `guard_edit.py`, actualiza
`src/CLAUDE.md` y añade agentes `ejecutor-feature`, `tester` y `depurador` más una rule de
desarrollo para `src/`. Este trabajo del harness no levanta el freeze.

## Auditoría compartida

El [harness activo](ai-audit-harness.md) incorpora la skill
`libox-system-design-audit` y los agentes `libox-audit-fable` / `libox-audit-opus`.
Su selección explícita de modelos prevalece sobre la convención genérica de agentes
en esta tarea. Codex comparte el procedimiento mediante `AGENTS.md`.
