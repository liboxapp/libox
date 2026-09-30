---
title: Manifiesto — auditoría del harness 20260925-203710
author: Claude coordinador (claude-opus-5-5)
status: vigente
tags: [auditoria, harness, manifiesto]
updated: 2026-09-25
description: Entrada común de la auditoría del harness de IA para decidir si está listo para arrancar R0. SHA, alcance, preguntas, modelos y decisiones abiertas.
---

# Manifiesto de ejecución

## Identificación

| Campo | Valor |
|---|---|
| `run_id` | `20260925-203710-harness` |
| Fecha y zona | 2026-09-25, preparación 20:32–20:40 UTC |
| Objetivo | `harness` (OS de IA y su capacidad de revisar system design) |
| SHA completo | `471a28d050a3f03c3b605649f7463822a8e157ad` |
| Rama de procedencia | `codex/activate-ai-audit` · 17 commits por delante y 1 por detrás de `origin/main` (`b4fb1dd`) · merge-base `b54f27d` |
| Estado del árbol | Archivos rastreados sin cambios. Un archivo sin rastrear **ajeno a este run**: `docs/audits/20260925-203250-harness-codex/codex-report.md`, de una ejecución concurrente de Codex aparecida a las 20:32:50 UTC. No se leyó ni se modificó |
| Claude Code | 2.1.282 (mínimo exigido 2.1.280) |
| Coordinador | Claude, sesión en `claude-opus-5-5` |

## Documentos que rigen

Según el Registro Maestro V6 §1 (`docs/linea-base/LIBOX_REGISTRO_MAESTRO_LINEA_BASE_V6.md`): LBPF V3 (L0), Product Strategy V3 (L1), PRD MVP V9 (L2, contrato de construcción), PRD Enterprise V3 (L2, no ejecutable), Especificación Técnica V7, Matriz de Casos de Uso V1 y Guía de Extensión V1 (L3), Design System V2 (L4), VIES V3, Backlog MVP V3, Dossier Legal V1. Auditorías y Evaluación V1 son histórico de decisión. Artefactos: `libox_schema_L3_V7.sql`, `libox_openapi_L3_V7.yaml`, tokens L4 V2, backlog xlsx V3, `verify_corpus.py` V1.

Documentos del harness al SHA: `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `.claude/rules/` (4), `.claude/agents/` (5), `.claude/skills/` (6), `.claude/settings.json`, `scripts/hooks/` y sus tests, `.github/workflows/` (6), `.github/CODEOWNERS`, `docs/equipo/ai-audit-harness.md` (vigente, 2026-09-25), `docs/superpowers/specs/2026-09-25-ai-audit-harness-design.md` (aprobado) y `docs/superpowers/specs/ai-audit-harness/` (contrato y plantilla, vigentes).

Una fecha más reciente no deroga por sí misma un documento del Registro.

## Alcance

**Incluido.** Los archivos del harness listados arriba, sus controles efectivos (qué capa impone cada restricción), su preparación para el trabajo de código de R0 y su capacidad de auditar system design según el contrato.

**Excluido.** Decidir la arquitectura de producto (queda para una ejecución `producto`). El contenido del corpus como producto; solo interesa su control. Configuración de cuentas externas salvo la lectura del ruleset registrada en `checks.md`. Outline. `.claude/worktrees/` y todo `docs/audits/` salvo `manifest.md` y `checks.md` de este run.

## Preguntas

1. ¿El harness está listo para arrancar R0, es decir, para desarrollar esquema, auth, RBAC, outbox y backend?
2. ¿Qué controles son efectivos, qué capa los impone y qué vías de escritura quedan sin control?
3. ¿Claude y Codex encuentran las mismas reglas y versiones vigentes?
4. ¿Qué falta en el harness para trabajo de código: CI, reglas de código backend, levantamiento del freeze, revisión de las zonas sin IA?
5. ¿El harness puede auditar system design con evidencia comparable (cobertura del contrato)?
6. ¿Qué cobertura tienen los escenarios H-01 a H-08?

## Límites, responsables y herramientas

- **Tiempo y gasto:** sin presupuesto aprobado; desconocido.
- **Responsables:** Diego decide alcance, riesgos aceptados y producto. El coordinador prepara y sintetiza; no emite dictamen propio.
- **Herramientas:** el coordinador tiene lectura, escritura, shell y delegación. Los revisores Claude tienen `Read, Grep, Glob`, sin shell ni edición. Codex usa su propio ejecutor.
- **Restricción:** la separación de informes es procedimiento, no aislamiento técnico.

## Modelos

| Revisor | Solicitado | Efectivo |
|---|---|---|
| `libox-audit-fable` | `claude-fable-5-1` | `claude-fable-5-1`: metadata de ejecución del subagente, 95 turnos de asistente, todos con ese modelo |
| `libox-audit-opus` | `claude-opus-5-5` | `claude-opus-5-5`: metadata de ejecución del subagente, 119 turnos de asistente, todos con ese modelo |
| Codex | el de su sesión | No verificado: su informe, en una ejecución separada, lo declara así |

Actualizado por el coordinador tras cerrar las revisiones. La misma metadata muestra que ambos subagentes usaron solo `Read`, `Glob`, `Grep` y la entrega. Eso acredita el uso, no la imposibilidad de cargar otras herramientas.

Sin overrides que lo impidan: `CLAUDE_CODE_SUBAGENT_MODEL` ausente, variables `ANTHROPIC_*` ausentes, sin claves de modelo en la configuración del proyecto. La configuración de usuario solo fija `model` para la sesión principal.

## Decisiones abiertas y supuestos

| Tema | Clase | Estado |
|---|---|---|
| ASS-001, custodia del dinero | Decisión abierta | Sin ratificar por los socios. [LEGAL→ABOGADO] |
| ASS-002, stack (backend .NET o TypeScript) | Decisión abierta | Sin ratificar; `src/` congelado. No se infiere de esta conversación |
| Documentación de API del backend con Scalar | Decisión comunicada por Diego el 2026-09-25 | No está en el snapshot; se incorpora por el flujo normal. No ratifica ASS-002 |
| Carga: 50 órdenes/s, 500 sorteos activos | Hipótesis | Capacidad de referencia del PRD §32.4, sin medición |
| Equipo: 4 personas a 32 SP por sprint | Hecho documental | Backlog V3 §1 |
| Recuperación (RPO/RTO) | Desconocido | L3 V7 no la define |
| Proveedores | Mercado Pago: hecho documental (L3 §0.3) sin contrato verificado. Baliza, KYC y comprobantes: desconocidos | — |

Outline (doc 20) **no se consultó**: la revisión se limita a la evidencia local.
