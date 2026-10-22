---
title: Sistema operativo de IA — cómo trabaja Claude Code en Libox
status: vigente
tags: [equipo, claude-code, hooks, skills, agentes, memoria]
updated: 2026-10-18
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

El backend es Go (D-10) y el frontend TypeScript con
[ACT-R6-07](#act-r6-07-nextjs-16-y-turbopack). Tras emitir L3 V8, el PR de D1 retira
`.claude/rules/src-congelado.md` y las constantes `FROZEN_*` de `guard_edit.py`, actualiza
`src/CLAUDE.md` y añade agentes `ejecutor-feature`, `tester` y `depurador` más una rule de
desarrollo para `src/`. Este trabajo del harness no levanta el freeze.

## ACT-R6-07: Next.js 16 y Turbopack

Diego aprobó el 2026-10-18 **Next.js 16 + TypeScript para frontend y Turbopack
como compilador en desarrollo y producción**. Go continúa en API y worker.
La decisión consta en el [benchmark ACT-R6-07](https://liboxapp.getoutline.com/doc/act-r6-07-benchmark-nextjs-14-vs-16-KYfjxwCbDf)
y en [pendientes y decisiones técnicas Rev6](https://liboxapp.getoutline.com/doc/diego-pendientes-y-decisiones-tecnicas-rev6-dET6AASY9e).

- **Estado instalado al 18/10:** [`package.json`](../../package.json) y
  [`package-lock.json`](../../package-lock.json) fijan Next.js **16.3.0**. Registrar
  esta decisión no actualiza dependencias.
- **Candidato evaluado:** el benchmark probó **16.4.2**. Al ejecutar la actualización,
  verificar y fijar el parche estable mantenido de Next.js 16; el benchmark no
  acredita por sí solo la compatibilidad integral de Libox.
- **Pendiente de ejecución:** revisar compatibilidad de dependencias y configuración,
  actualizar y verificar el lockfile, ejecutar lint, build y tests, validar el
  despliegue e incorporar la decisión en L3 mediante su proceso de emisión.
- **Licencia y hosting:** Turbopack usa licencia MIT, sin coste de licencia ni
  obligación de alojarse en Vercel. Vercel Pro conserva la elección para frontend;
  Render aloja API y worker Go según las
  [decisiones del 12/10](../superpowers/specs/c1-l3-v8/decisiones-2026-10-12.md).

Es una decisión aprobada documentada en el OS AI; no emite el canon, completa D1
ni levanta el [freeze del scaffold](../../.claude/rules/src-congelado.md).
Todo agente que retome implementación debe conservar estas restricciones.

## ACT-R6-10: flujo y pruebas pendientes

Diego aprobó el 2026-10-18 el criterio de importes de órdenes y doble firma T-14,
y pidió conservarlo como trabajo pendiente de pruebas unitarias. Consultar el
[registro de pruebas Rev6](../desarrollo/pruebas-pendientes-rev6.md) antes de retomar
H22-06/H22-07: contiene el flujo aprobado y los IDs de pruebas unitarias e integración.
Implementación y pruebas siguen **PENDIENTES**; los unitarios no acreditan el control
en BD. Diego es el responsable humano de las zonas protegidas; ejecutor y fecha,
por confirmar. El registro no levanta el freeze ni emite el canon.

## ACT-P08: flujo actual y recorridos

El [flujo end-to-end rev6](../flujos/flujo-end-to-end.md) sustituye el diagrama del
19/06/2026 e incorpora los ocho criterios aprobados y las confirmaciones de Diego.
Tiene seis recorridos y casos E2E-P08-01 a E2E-P08-06 en el
[registro de pruebas](../desarrollo/pruebas-pendientes-rev6.md#act-p08-pruebas-del-flujo-completo).
Es una guía documental con pendientes explícitos; no acredita implementación,
no emite el canon ni levanta el freeze. Usarlo antes de retomar Desarrollo.
El [delivery aprobado](../flujos/delivery-premios-rev6.md), ACT-R6-14, conserva
recorrido, modalidades, evidencia, transición de servicios/registrables y segunda
firma registrable; diseño visual, implementación y pruebas siguen pendientes.

## ACT-R6-13/15/16: definición y ejecución futura

Por solicitud de Diego del 2026-10-18, consultar el [plan por regla](../desarrollo/plan-correcciones-rev6.md),
[contrato diario y privacidad](../desarrollo/controles-servicio-rev6.md) y
[alcance de entrega/manifiesto](../desarrollo/alcance-entrega-tecnica-rev6.md).
R6-15 tiene operación y privacidad aprobadas; ejecutores, cobertura, configuración
efectiva y pruebas se concretan antes de operar y durante desarrollo.
No generar código de zonas protegidas ni interpretar este plan como emisión o fin del freeze.

## Auditoría compartida

El [harness activo](ai-audit-harness.md) incorpora la skill
`libox-system-design-audit` y los agentes `libox-audit-fable` / `libox-audit-opus`.
Su selección explícita de modelos prevalece sobre la convención genérica de agentes
en esta tarea. Codex comparte el procedimiento mediante `AGENTS.md`.
