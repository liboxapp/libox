---
title: Programa para habilitar R0 — diseño
status: borrador
tags: [libox, r0, harness, programa, spec]
updated: 2026-09-25
description: Programa aprobado por Diego para resolver la auditoría del harness (SY-01 a SY-16) y los defectos del canon, y dejar R0 listo para arrancar. Streams, decisiones, secuencia y criterio de éxito.
---

# Programa para habilitar R0

## Origen

- **Auditoría del harness** `20260925-203710-harness`: dictamen `requiere cambios` con 16 temas (SY-01 a SY-16). La síntesis está en `docs/audits/20260925-203710-harness/synthesis.md`, en el run todavía sin versionar.
- **Revisión de sistema**: 19 hallazgos técnicos del canon en la [nota de hallazgos](2026-09-25-revision-sistema-hallazgos-l3.md) y el encuadre de las decisiones abiertas en la [nota de trade-offs](2026-09-25-revision-sistema-decisiones-ass.md).

Este programa no ratifica ASS-001 ni ASS-002. Tampoco edita el canon en su lugar: el canon cambia solo con `libox-versionar-doc`.

## Decisiones de Diego (2026-09-25)

| ID | Decisión | Alcance |
|---|---|---|
| D-01 | ASS-002 sigue **abierta** y se decide con un spike en TypeScript, con fallos deliberados y un criterio explícito ([diseño del spike](2026-09-25-spike-ass-002-ts-design.md)) | Es una decisión de proceso: la ratificación sigue siendo de los socios |
| D-02 | Revisores: Arom B. y Martin G. Diego los invita desde GitHub, y la revisión obligatoria se activa cuando acepten | Ruleset y CODEOWNERS |
| D-03 | Escrituras por shell: el CI es la garantía y el hook añade una heurística | Guards y CI |
| D-04 | Un guard que falla sigue permitiendo, pero con aviso visible | Guards |
| D-05 | L3 V8 incluirá el stack y las correcciones técnicas. El ledger (H-01, H-03) queda como hallazgo hasta tener confirmación contable. [LEGAL→ABOGADO] | Canon |
| D-06 | Secuencia en streams paralelos con PRs chicos | Programa |
| D-07 | Scalar como documentación de la API del backend | Canon §0.3 y backend |

## Criterio de éxito

R0 queda habilitado cuando se cumplen las cinco condiciones:

1. La auditoría del harness, re-ejecutada, da `sin bloqueos en el alcance revisado`.
2. Los socios ratifican ASS-002 con la evidencia del spike.
3. L3 V8 está emitida con `verify_corpus.py` en cero fallos.
4. El freeze se levanta en el PR de cierre de ASS-002, con CI de código obligatorio.
5. La revisión de una segunda persona está activa en el ruleset.

**Fuera de alcance:** construir historias de R0 y decidir ASS-001 (custodia). ASS-001 no bloquea el gate de R0, pero sí R1 y R2, y se sigue en el doc 20.

## Streams y sub-proyectos

Cada sub-proyecto tiene su propio plan de implementación y su propio PR.

### Stream A — Harness (neutral al stack; empieza ya)

| ID | Qué entra | Temas | Verificación |
|---|---|---|---|
| A0 | PR del OS de IA (rama local `codex/activate-ai-audit`) con el run de auditoría. Soporte de prefijos en `outline-ignore.txt` y alta de `docs/audits/`. PR aparte para el commit de Scalar (`7ca542f`), que quedó fuera de `main` | SY-16 (parte) | CI verde. `outline-sync` en verde en `main` |
| A1 | `verify-corpus` y `hooks` corren siempre y pasan a ser obligatorios. Job `protected-paths` que falla si se modifica un `docs/linea-base/*_V<n>.*` existente, si entra `spikes/**`, o si se toca `src/` (salvo los `CLAUDE.md`) o la config del scaffold mientras la regla del freeze exista en la rama del PR. Así el PR de cierre, que borra la regla, puede pasar. Control de trailers de IA en `commitlint` | SY-02, SY-05 | PRs sintéticos rechazados en un repo de prueba |
| A2 | CODEOWNERS con rutas reales, dueño y revisor fijo por zona sin IA, canon y OS. Regla `zonas-sin-ia.md` replicada en `AGENTS.md`. `CONTRIBUTING.md` y `src/CLAUDE.md` con lo específico de un stack marcado "condicionado a ASS-002" y reglas de backend neutrales extraídas de L3 §12. `AGENTS.md` aclara que en Codex no hay guards y que aplica el CI. Ruleset con al menos una aprobación y revisión de dueños, **después** de que acepten los invitados | SY-07, SY-08, SY-09 | `revisor-pr` sobre el PR. Un PR de zona sin aprobación queda bloqueado |
| A3 | `guard_edit`: rutas normalizadas (worktree, `realpath`, mayúsculas); allowlist de escritura durante el freeze, con `spikes/**` permitido; E4 que protege los archivos del OS (`scripts/hooks/`, `.claude/settings.json`, `.claude/rules/`, `.claude/agents/`), con una válvula `LIBOX_EDITAR_OS=1` cuyo uso queda avisado en stderr. `guard_bash`: heurística de escrituras por shell y regex B1–B4 endurecidas. Ambos: aviso visible si fallan y timeouts por debajo de 90 s. `session_status`: "regla ausente, verificar el doc 20" | SY-03, SY-04, SY-05, SY-06, SY-10 | Tests rojos primero en `scripts/hooks/tests/`. El ensayo de guards da DENY en S1–S3, W1–W2, B1b, symlink y `vitest.config.ts` |
| A4 | `mcp__*` en `disallowedTools` de los revisores. Un worktree fijo al SHA auditado por revisor. Regla para runs concurrentes y modo `resume <run-id>`. Ensayo de guards versionado con fixtures H-01 y H-02. Saneador de credenciales. E5 contra la sobrescritura de informes | SY-11, SY-12, SY-13 | Tests del saneador y de E5. H-01 a H-08 con evidencia o un límite explícito |
| A5 | `outline-kb-cli` con versión fijada y actions fijadas por SHA. Marketplace de terceros con versión fijada. `outline-skills` limitada a lectura y sin `--api-key` en los ejemplos. Títulos de PR tratados como datos no confiables en el digest. Confirmación humana en `libox-registrar-hallazgo`. Metadata, conteos y docstrings al día | SY-14, SY-15, SY-16 | CI verde con las versiones fijadas |

### Stream B — Decisión de ASS-002 (en paralelo a A2–A5)

**B1.** Spike del flujo de compra sobre TypeScript, PostgreSQL y workflows administrados, en la rama `spike/ass-002-ts`, **no mergeable**. Solo se versiona el informe. El detalle está en el [diseño del spike](2026-09-25-spike-ass-002-ts-design.md).

### Stream C — Canon L3 V8 (se prepara en paralelo; se emite tras B1)

- **C1.** Registrar los hallazgos por CD-07 y preparar el borrador de L3 V8:
  - SQL desplegable: particiones, GRANTs, semillas, triggers prometidos e INV-38.
  - OpenAPI completo (T-1), con al menos las 43 rutas de §11, válido en 3.1.
  - Vectores de prueba con resultado esperado, y `verify_draw` sin ambigüedad.
  - HMAC del DNI, RPO/RTO y backups, almacenamiento de `server_seed`, política de pago tardío y timeout de la baliza.
  - Scalar.
  - El ledger (H-01, H-02, H-03) queda registrado y pendiente de confirmación contable.
- **C2.** Emitir L3 V8 con §0.3 ya ratificado, usando `libox-versionar-doc` (CD-01 a CD-11): `verify_corpus` en cero, Registro §1 y `BASELINE`. Registrar el cierre de ASS-002 en el doc 20.

### Stream D — Preparación de R0 (tras C2)

**D1.** Es el PR de cierre de ASS-002, y hace cinco cosas:

- Borra la regla del freeze, las constantes `FROZEN_*` y sus tests.
- Añade el CI de código del stack elegido: build, lint, typecheck, test, migraciones sobre PostgreSQL efímero con el esquema V8 y contrato OpenAPI.
- Añade la capa `dev`: agentes `ejecutor`, `tester` y `depurador`, y una regla de backend del stack.
- Suma las rutas de código a CODEOWNERS.
- Registra la consola interna de operación como épica de R0.

## Secuencia

```
A0 ─► A1 ─► A2 ─► A3 ─► A4 ─► A5 ─────────────┐
       │                                        ▼
       ├─► B1 spike ─► ratificación socios ─► C2 ─► D1 ─► re-auditoría
       └─► C1 borrador L3 V8 ──────────────────┘
```

B1 y C1 arrancan después de A1: el canon y el spike ya corren bajo el gate de CI. A2 activa la revisión obligatoria solo cuando los invitados hayan aceptado. El cierre re-ejecuta `/libox-system-design-audit` (harness) y `/libox-system-design-audit producto`.

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Activar la revisión obligatoria con una sola persona bloquea todos los PRs | Activarla al aceptar los invitados, y dejarlo verificado en A2 |
| Construir sobre el OS sin integrar | A0 va primero; los PRs posteriores se rebasan sobre `main` |
| El código del spike llega a `main` o se reutiliza en zonas sin IA | Rama no mergeable y el job `protected-paths` rechaza `spikes/**`. Las zonas sin IA se reescriben a mano en R0 |
| L3 V8 es grande (OpenAPI de 16 a 43 o más operaciones) | Se prepara en paralelo y se estima en el plan de C1. T-1 cotizado en 8 SP es probablemente bajo |
| Dependencia de proveedor en los workflows | El spike mide límites, timeouts y conexiones antes de ratificar |
