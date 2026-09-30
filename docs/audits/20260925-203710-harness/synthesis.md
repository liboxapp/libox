---
title: Síntesis — auditoría del harness 20260925-203710
author: Claude coordinador (claude-opus-5-5)
status: vigente
tags: [auditoria, harness, sintesis]
updated: 2026-09-25
description: Conciliación por evidencia de las revisiones de Fable, Opus y Codex sobre el SHA 471a28d. Dictamen consolidado, desacuerdos, cambios propuestos y condiciones de cierre.
---

# Síntesis del coordinador

Se redactó después de cerrar las revisiones independientes: [Fable](fable-report.md), [Opus](opus-report.md) y la revisión de Codex en su propia ejecución (`docs/audits/20260925-203250-harness-codex/codex-report.md`). Entradas comunes: [manifiesto](manifest.md) y [verificaciones](checks.md). La síntesis no ratifica el stack ni la custodia. Tampoco autoriza descongelar `src/`, cambiar el corpus, desplegar ni operar dinero real.

## Identificación y validez

| Campo | Valor |
|---|---|
| Snapshot | `471a28d050a3f03c3b605649f7463822a8e157ad` · rama `codex/activate-ai-audit` |
| Verificación antes de sintetizar | `HEAD` igual al SHA inicial y sin archivos rastreados modificados. `git status` solo muestra archivos de carpetas de run (esta y la de Codex, previa). Comparación válida |
| Fable | Solicitado y efectivo: `claude-fable-5-1`, acreditado por la metadata de ejecución (95 turnos). Usó solo `Read`, `Glob` y `Grep` |
| Opus | Solicitado y efectivo: `claude-opus-5-5`, acreditado por la metadata de ejecución (119 turnos). Usó solo `Read`, `Glob` y `Grep` |
| Codex | Mismo SHA y objetivo, pero **en una ejecución separada**, lanzada antes de este manifiesto y sin su brief. Modelo no verificado. **Independencia limitada**: Codex implementó el harness en el turno anterior (su informe, líneas 23–24). Su comparabilidad es parcial |

## Dictamen consolidado

**`requiere cambios`. El harness no está listo para arrancar R0.** Sí sirve hoy para trabajo documental y para auditar, con los límites que se describen abajo.

Los tres revisores coinciden en el dictamen, pero la coincidencia no es la prueba. La base decisiva es la evidencia ejecutada:

- Ningún workflow compila ni prueba código.
- `verify-corpus` y `hooks` no son checks obligatorios en `main`.
- Hay escrituras por shell que modifican archivos protegidos (ejecutado por el coordinador y por Codex).
- Las rutas dentro de worktrees y los alias por symlink eluden E1 y E2.
- El trailer de IA en `-F` elude B1.

A eso se suman hallazgos documentales verificados por el coordinador: las zonas sin generación asistida no existen en el harness, y hay instrucciones de stack contradictorias.

## Temas consolidados

IDs locales de esta ejecución (`SY-`). Los prefijos `FAB-`, `OPU-` y `CX-` conservan la procedencia.

| ID | Tema | Fable | Opus | Codex | Evidencia decisiva | Resolución y responsable |
|---|---|---|---|---|---|---|
| SY-01 | Harness no apto para código de R0 | FAB-08 | OPU-15 | No lo certifica listo | `checks.md` §4: sin pasos de código; capa `dev` pendiente (`sistema-operativo-ia.md:92-97`) | Lista de preparación de R0 ligada al PR que cierre ASS-002. Diego |
| SY-02 | CD-10, inmutabilidad del canon y freeze no bloquean el merge | FAB-02 | OPU-01 | — | Ruleset: obligatorios solo `commitlint`, `markdownlint` y `links` (`checks.md` §4). `verify-corpus.yml:8-11` con filtro `paths` | Checks obligatorios y job anti in-place y anti freeze en CI. Diego (ruleset) + PR |
| SY-03 | Escrituras sin control local | FAB-01 | OPU-03 | CX-02 | **Ejecutado**: S1–S3 permitidos (`checks.md` §3). Codex: la escritura se ejecutó | CI como barrera común; la garantía local está en desacuerdo (D1). Diego |
| SY-04 | Worktrees y symlinks eluden E1 y E2 | FAB-01 | OPU-03, OPU-05 | CX-01 | **Ejecutado**: W1 y W2 permitidos (coordinador); alias por symlink permitido (Codex) | Normalizar rutas (worktree y `realpath`) en `guard_edit.py`, con tests. OS de IA |
| SY-05 | Bypasses textuales de B1–B4; hookify no es una segunda línea | FAB-01 | OPU-04 | — | **Ejecutado**: B1b permitido. Hookify usa la misma regex (verificado). Sin control de trailers en CI | Control de trailers en `commitlint.yml`. Casos `-C`, `add &&`, pathspec y `--trailer` pendientes de prueba |
| SY-06 | El freeze no cubre `vitest.config.ts` ni directorios nuevos de código | — | OPU-05 | CX-01 (parcial) | `FROZEN_FILES` sin `vitest.config.ts` (`guard_edit.py:19-22`, leído). `backend/` fuera del prefijo | Allowlist de escritura durante el freeze. OS de IA |
| SY-07 | Stack contradictorio dentro del harness (H-02 real) | FAB-03 | OPU-08 | Considera H-02 cubierto (D3) | `src/CLAUDE.md:99` "Stack (closed — ADR Z.6)"; `CONTRIBUTING.md:97` frente a L3 V7 §0.3 (verificado) | Marcar "condicionado a ASS-002" y extraer reglas neutras de L3 §12. `redactor-docs` + Diego |
| SY-08 | Zonas sin generación asistida (261 SP) ausentes del harness | — | OPU-02 | — | Backlog V3 §1.3 las declara; 0 coincidencias en el harness (verificado). R0 toca E02 y E04 | Regla por zona, CODEOWNERS y aprobación obligatoria. Diego + dueños de zona |
| SY-09 | Paridad Claude/Codex: mismas reglas, distinta aplicación | FAB-05 | OPU-09 | Allowlist verificada solo en archivos | `AGENTS.md:1-6` (punteros, sin guards). `.gitignore` reincluye un adaptador inexistente | `AGENTS.md` explícito ("en Codex no hay guards; aplica el CI"). Ensayar H-04 desde Codex |
| SY-10 | El OS se puede modificar desde la sesión; ASS-002 se infiere de un archivo | — | OPU-06 | — | `session_status.py:33-34` (verificado) | E4 que proteja el OS y un aviso "regla ausente, verificar doc 20". OS de IA |
| SY-11 | La solo-lectura de los revisores no está probada frente a MCP | FAB-04 | Allowlist observada | Solo en archivos | Metadata: solo `Read/Glob/Grep` usados (uso, no capacidad) | Probar o añadir `mcp__*` a `disallowedTools`. Coordinador |
| SY-12 | Validez del run: concurrencia, lectura del árbol, reanudación | FAB-09 | OPU-10, OPU-11 | CX-03 | Run concurrente de Codex; copias del corpus en `.claude/worktrees/` aparecen en las búsquedas (verificado); sin modo `resume` | Worktree `--detach` por revisor, regla para runs concurrentes y `resume <run-id>`. Coordinador |
| SY-13 | Escenarios H: 2 de 8 con evidencia ejecutada; sin fixtures ni saneador | FAB-09, FAB-10 | OPU-11 | Tabla propia | `checks.md` §5; Codex añade H-04 (symlink, Bash) | Versionar el ensayo, fixtures H-01/H-02, saneador, E5 contra sobrescritura y mapa de evidencia para `producto` |
| SY-14 | Cadena de suministro y secretos | Sin hallazgo en `outline-skills` (D4) | OPU-12 | — | `pip install outline-kb-cli` sin versión; `allowed-tools: Bash(outline-cli *)`; actions fijadas por tag (verificado) | Fijar versiones y SHA, restringir la skill y tratar títulos de PR como no confiables. Diego |
| SY-15 | `libox-registrar-hallazgo` escribe en el doc 20 sin confirmación | Sin hallazgo (D4) | OPU-13 | — | Skill sin `disable-model-invocation` (lectura de Opus) | Confirmación humana antes de escribir. Diego |
| SY-16 | Deriva documental y `outline-sync` en rojo al versionar `docs/audits/` | FAB-06, FAB-07 | OPU-14 | — | `outline-ignore.txt` sin prefijos; `check-map` exige coincidencia exacta (verificado) | Soporte de prefijos + `docs/audits/` **antes** de versionar este run. Corregir `CODEOWNERS` y docstrings |

## Desacuerdos que se mantienen

- **D1. Garantía local frente a escrituras por shell.** Opus y Fable proponen heurísticas en `guard_bash.py` con el CI como barrera definitiva. Codex sostiene que una regex no cubre intérpretes ni aliases, y propone aislamiento del sistema de archivos o aceptar el freeze como procedimental. Decide Diego.
- **D2. Fallo abierto de los guards.** Opus lo reporta (OPU-07: sin alerta, y timeouts que pueden superar los 90 s). Fable y Codex lo tratan como diseño aceptado. Decide Diego: riesgo aceptado o aviso visible.
- **D3. Cobertura de H-02.** Codex la da por cubierta porque la regla de ASS-002 es explícita. Fable y Opus encuentran el conflicto dentro del propio harness. La evidencia de la tabla (SY-07) respalda a Fable y Opus.
- **D4. Skills de Outline.** Fable no encontró hallazgos; Opus sí (SY-14, SY-15). Lo verificado por el coordinador respalda a Opus en la preautorización y en la versión sin fijar.
- **D5. Peso de Codex.** Coincide con los hallazgos ejecutados, pero es una autorrevisión en una ejecución separada. Para comparabilidad plena, ver [el prompt de este run](codex-prompt.md).

## Cambios propuestos (para un cambio posterior)

Orden recomendado para habilitar R0. Nada de esto se aplicó durante la auditoría.

1. **Gate de CI (SY-02, SY-05).** `verify-corpus` y `hooks` obligatorios, sin filtro de rutas. Un job que falle ante edición in-place de un `_V<n>` o cambios en `src/` durante el freeze. Control de trailers en `commitlint`.
2. **Zonas sin generación asistida (SY-08).** Regla, CODEOWNERS por zona y aprobación humana obligatoria antes del primer PR de R0.
3. **Reglas de backend neutras (SY-07).** Salen de L3 §12. Lo específico de un stack queda condicionado a ASS-002.
4. **Preparación de R0 (SY-01).** CI de código (build, test y migraciones sobre base efímera), capa `dev` y levantamiento del freeze con sus tests. Se instancia en el PR que cierre ASS-002, que siguen decidiendo los socios.
5. **Guards locales (SY-04, SY-06, SY-10).** Normalizar rutas, allowlist de escritura durante el freeze y protección del OS.
6. **Paridad y proceso (SY-09, SY-11, SY-12, SY-13).** `AGENTS.md` explícito, revisores sobre worktree `--detach`, `resume`, ensayo versionado, saneador y E5.
7. **Higiene (SY-14, SY-15, SY-16).** Versiones fijadas, skills acotadas, prefijos en `outline-ignore` y `CODEOWNERS`. `verify_corpus.py` es artefacto V1 del canon: cambiar su `default` exige evaluar CD-01 y CD-11; corregir el docstring no.

## Pruebas pendientes

- H-01, H-02, H-06, H-07 y H-08 sobre una copia manipulada; H-04 desde una sesión real de Codex.
- Bypasses deducidos y no ejecutados: `git -C … commit`, `git add … && git commit`, commit por pathspec, `--trailer`, `HEAD:refs/heads/main`, `git -c user.email`, rutas con mayúsculas y `NotebookEdit`.
- Exposición de herramientas MCP a subagentes con `tools:` restringido.
- Parámetros completos del ruleset y actores con bypass.
- `git fsck` sobre los `tmp_obj` señalados por Opus, y hash de las fuentes citadas frente a `git ls-tree 471a28d`.
- Estado real de `outline-sync` en `main` y de ASS-001 y ASS-002 en el doc 20 (Outline no consultado).

## Condiciones de cierre

- Diego resuelve cada tema SY con una de tres opciones: corregir, aceptar el riesgo (con fecha y alcance) o descartar con evidencia. La falta de respuesta no es aprobación.
- Lo que requiera tocar el canon va por `libox-registrar-hallazgo` y una versión nueva. Esta síntesis no crea IDs ASS-, CHANGE- ni RISK-.
- El run se versiona por PR solo después de SY-16; si no, `outline-sync` falla en `main`.
- Decisión registrada fuera del snapshot: Diego eligió Scalar como documentación de API del backend el 2026-09-25. Está incorporada en la revisión de sistema (PR #18) y no altera este dictamen.
