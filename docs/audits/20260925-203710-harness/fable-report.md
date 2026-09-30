---
title: Informe independiente Fable — auditoría del harness 20260925-203710
author: libox-audit-fable
status: vigente
tags: [auditoria, harness, fable, system-design]
updated: 2026-09-25
description: Primera pasada independiente del harness de IA de Libox al SHA 471a28d con foco en dominio, estados, contratos y simplicidad; dictamen, hallazgos FAB-01…FAB-10, verificaciones y cobertura.
---

# Informe independiente — revisor Fable

## Identificación

| Campo | Valor |
|---|---|
| Ejecución y objetivo | `20260925-203710-harness` · objetivo `harness` |
| Revisor | `libox-audit-fable` (definición en `/Users/diegocotrina/Claude/Cowork/Liboxapp/Libox/.claude/agents/libox-audit-fable.md`) |
| Modelo solicitado | `claude-fable-5-1` (`.claude/agents/libox-audit-fable.md:4`) |
| Modelo efectivo | **no verificado**. La autodeclaración de la sesión no lo acredita; lo acredita la metadata de ejecución que registre el coordinador |
| Ejecutor | Subagente de Claude Code lanzado por el coordinador |
| SHA | `471a28d050a3f03c3b605649f7463822a8e157ad` · rama `codex/activate-ai-audit` |
| Manifiesto | `/Users/diegocotrina/Claude/Cowork/Liboxapp/Libox/docs/audits/20260925-203710-harness/manifest.md` · evidencia ejecutada en `checks.md` del mismo run |
| Inicio, fin y zona | No registrados por el revisor (sin reloj ni shell); los registra el coordinador en su metadata. Fecha de trabajo: 2026-09-25 |
| Acceso y herramientas efectivas | Funciones invocables en la sesión: `Read`, `Grep`, `Glob` y `SubagentHandback`. Sin shell, sin edición, sin delegación. El prompt inyectó además guías de herramientas MCP diferidas (`mcp__plugin_context-mode_context-mode__ctx_*`, `mcp__computer-use__*`) que **no** estaban en la lista de funciones y que no intenté cargar (ver FAB-04) |
| Primera pasada | Confirmo que no leí `fable-report*`, `opus-report*`, `codex-report*`, `synthesis*` ni `docs/audits/20260925-203250-harness-codex/`. Tampoco leí `.claude/worktrees/`, `.env*` ni `.claude/settings.local.json` |
| Snapshot | No puedo ejecutar `git rev-parse`; verifiqué por lectura que el contenido de los archivos coincide con lo descrito en `manifest.md` y `checks.md` (rutas, conteos de workflows, agentes, skills, guards y tests). Acepto el SHA como lo acredita el coordinador |

Las rutas de este informe son relativas a `/Users/diegocotrina/Claude/Cowork/Liboxapp/Libox/`.

## Dictamen

**`requiere cambios`.**

Justificación: FAB-08 (el harness no está listo para R0: sin CI de código, sin reglas de backend neutras al stack, capa `dev` pendiente), FAB-02 (CD-10 no es gate de merge en CI: `verify-corpus` y `hooks` no son checks requeridos), FAB-03 (el propio harness contiene la contradicción de stack que el escenario H-02 debería exponer, en `CONTRIBUTING.md` y `src/CLAUDE.md`), FAB-01 (vías de escritura por shell sin control, acreditadas por el coordinador en `checks.md`) y FAB-04 (la allowlist de los revisores no acredita modo solo lectura frente a herramientas MCP de plugins; pendiente de prueba). Los hallazgos FAB-05, FAB-06, FAB-07, FAB-09 y FAB-10 son operativos o menores y no cambian el dictamen por sí solos.

El dictamen se limita al alcance `harness`. No ratifica ASS-001 ni ASS-002, no autoriza descongelar `src/` ni modificar el corpus.

## Hallazgos

### FAB-01 — Vías de escritura por shell y bypasses de guards sin control técnico

- **Severidad:** operativo. No bloquea R0 por sí solo porque el ruleset de `main` y el CI cubren la integración; sí deja el checkout local sin protección efectiva contra edición del canon y de `src/` por Bash.
- **Estado:** confirmado (ejecutado por el coordinador; verificado por lectura del código).
- **Naturaleza:** implementado (los guards) / no verificado (mi lectura de los bypasses no ensayados).
- **Evidencia:**
  - `checks.md:47-49` (S1–S3: `sed -i` sobre el canon, `>>` en `src/`, `python3 -c` que escribe en `src/`: exit 0); `checks.md:51` (B1b: trailer dentro de `-F msg.txt`: exit 0); `checks.md:53` (B2b: `git push` sin argumentos: exit 0); `checks.md:45-46` (W1/W2: rutas bajo `.claude/worktrees/`: exit 0).
  - `scripts/hooks/guard_bash.py:20-22` (B1 solo inspecciona el texto del comando); `:23-25` (B2 exige literal `origin main|main:main|HEAD:main`; `HEAD:refs/heads/main` no coincide); `:63-67,97` (B4 lee `git config user.email` del repo, no el comando: `git -c user.email=… commit` o `GIT_AUTHOR_EMAIL` no se detectan).
  - `scripts/hooks/guard_edit.py:54-62,84` (`relpath` + `startswith("src/")`: `.claude/worktrees/w/src/x.ts` no es `src/`).
  - `.claude/settings.json:17-38` (matcher `Edit|Write|MultiEdit`; `NotebookEdit` no está cubierto).
  - Capas que sí cubren: ruleset `main protection` (`checks.md:68-69`), correo en CI (`.github/workflows/commitlint.yml:21-30`).
- **Escenario:** una sesión con Bash ejecuta `sed -i` sobre `docs/linea-base/…_V9.md` o `printf >> src/app/page.tsx`; ambos guards permiten (exit 0). La integración se detiene solo si el PR falla `commitlint`/`docs` o si alguien mira el check no requerido `verify-corpus` (FAB-02).
- **Esperado frente a observado:** el contrato pide "rechazo por control efectivo o evidencia explícita de que falta ese control" (H-04, `audit-contract.md:35`) y registrar la capa que impone cada restricción (`:41-44`). Observado: E1/E2 son efectivos para `Edit|Write|MultiEdit` y B1/B2 para las formas literales; el resto es instrucción (`CLAUDE.md`, rules). El manual ya lo declara en parte (`docs/equipo/ai-audit-harness.md:33-34`), pero `docs/equipo/sistema-operativo-ia.md:55-69` presenta los guards sin enumerar estos límites.
- **Propuesta mínima:** (1) añadir a `sistema-operativo-ia.md` una fila "Lo que los guards no cubren" con las vías S1–S3, B1b, B2b, W1/W2 y `HEAD:refs/heads/main`, indicando que ahí la capa efectiva es CI + ruleset; (2) en `guard_bash.py`, extender B2 con `refs/heads/main` y B1 con `--trailer`, y añadir una regla textual conservadora (allow por defecto) para `sed -i|tee|>|>>` cuyo destino case con `docs/linea-base/.*[_-]V\d+\.` o `src/`; tests rojos primero en `scripts/hooks/tests/`. **Alternativa descartada:** denegar toda escritura por Bash o sandboxear el checkout: rompe trabajo legítimo (tests, `verify_corpus.py`, `gh`) y no lo justifica el riesgo mientras `main` esté protegido.
- **Validación:** repetir el ensayo de `checks.md` §3 con los casos nuevos; esperar exit 2 en S1 (canon), B1 con `--trailer` y `git push origin HEAD:refs/heads/main`.
- **Incertidumbre:** no ensayé nada (sin shell). Los bypasses que no están en `checks.md` (`refs/heads/main`, `git -c user.email`, `NotebookEdit`) los deduzco de las regex y del matcher; quedan `pendiente de prueba`.
- **Seguimiento:** responsable de hooks (Diego / `CODEOWNERS` `/scripts/`). Sin registro externo aún.

### FAB-02 — CD-10 no es gate de merge: `verify-corpus` y `hooks` no son checks requeridos

- **Severidad:** riesgo operativo con efecto patrimonial indirecto: una versión del canon con fallos puede entrar a `main` sin que el verificador lo impida.
- **Estado:** confirmado (lectura del ruleset por el coordinador + lectura de workflows).
- **Naturaleza:** implementado (workflows) / especificado (CD-10).
- **Evidencia:**
  - `checks.md:68`: checks obligatorios del ruleset: `commitlint`, `markdownlint`, `links`. No figuran `verify-corpus` ni `hooks`.
  - `.github/workflows/verify-corpus.yml:7-16` y `.github/workflows/hooks.yml:7-16`: filtrados por `paths`. `.github/workflows/docs.yml:4-7` explica por qué un check filtrado por ruta no puede ser requerido ("nunca corren… queda bloqueado para siempre").
  - `docs/linea-base/LIBOX_REGISTRO_MAESTRO_LINEA_BASE_V6.md:219`: "un fallo detiene la integración igual que una prueba en rojo". `CONTRIBUTING.md:62`: solo exige `commitlint` y `docs`. `docs/equipo/onboarding.md:69-70`: lista cinco checks como si todos gatearan.
  - La única barrera bloqueante de CD-10 es el hook B3 (`scripts/hooks/guard_bash.py:68-74`), que solo actúa en Claude Code y solo para commits vía tool Bash (FAB-01, FAB-05).
- **Escenario:** PR que emite `PRD MVP V10` sin actualizar `BASELINE`; `verify-corpus` falla en rojo; `commitlint`, `markdownlint` y `links` verdes; el ruleset permite el merge por rebase. Con un solo colaborador y sin approvals (`.github/CODEOWNERS:2-4`, `onboarding.md:84-86`) nadie lo detiene.
- **Esperado frente a observado:** CD-10/CD-11 exigen que la emisión sea "un solo acto" con cero fallos (`.claude/rules/linea-base.md:20-22`). Observado: en CI es informativo.
- **Propuesta mínima:** quitar el filtro `paths` de `verify-corpus.yml` y `hooks.yml` en `pull_request` (ambos tardan segundos) y añadirlos a los checks requeridos del ruleset; alinear `CONTRIBUTING.md:62` y `onboarding.md:69-70` con la lista real. **Alternativa descartada:** mantener el filtro y marcar "skipped = success": GitHub trata un check no reportado como pendiente, no como éxito, y bloquearía todo PR sin canon.
- **Validación:** abrir un PR de prueba que rompa `BASELINE` y comprobar que el merge queda bloqueado por `verify-corpus`.
- **Incertidumbre:** no leí el ruleset; me apoyo en `checks.md:68`. No sé si el ruleset exige "up to date" (`CONTRIBUTING.md:84`) — no lo lista `checks.md`.
- **Seguimiento:** Diego (configuración de GitHub) + PR de CI.

### FAB-03 — El harness contiene la contradicción de stack que H-02 debe exponer

- **Severidad:** riesgo operativo. Un ejecutor que lea `CONTRIBUTING.md` o `src/CLAUDE.md` como norma recibe un stack "cerrado" que el canon y `src-congelado.md` niegan.
- **Estado:** confirmado (lectura).
- **Naturaleza:** especificado (instrucciones contradictorias).
- **Evidencia:**
  - `src/CLAUDE.md:99` "## Stack (closed — ADR Z.6)" y `:101-108` (Next.js, Supabase, Drizzle, Inngest, Vercel; "No dependencies outside this stack without an ADR in `docs/decisions/`"). `docs/decisions/` no existe (Glob sin resultados; los ADR están en `docs/archive/decisions/`) y `.claude/rules/docs.md:15-17` dice que no se abren ADR Z nuevos.
  - `CONTRIBUTING.md:95` "Cuando entre el código (Next.js)" y `:97-126` "Reglas de ingeniería (vigentes desde el scaffold)… regla dura" con Drizzle, `supabase-js`, Inngest, Supavisor.
  - `AGENTS.md:8-16` bloque Next.js que Codex lee como entrada.
  - Frente a: `docs/linea-base/LIBOX_ESPECIFICACION_TECNICA_L3_V7.md:162` ".NET 8 LTS · Fijado en la historia de arranque"; `.claude/rules/src-congelado.md:15-17` (Z.6 derogado de facto sin ratificar); `src/CLAUDE.md:3-6` (banner de freeze, que convive con el "closed" de la línea 99).
  - `docs/archive/decisions/Z6-stack-tecnologico.md:14` "Documento canónico: este archivo", en un directorio que `docs.md:12` declara histórico.
- **Escenario (H-02 sobre el snapshot real, no una copia):** un ejecutor busca "qué stack uso" y encuentra tres respuestas: .NET 8 (canon), Next.js "closed" (`src/CLAUDE.md`), reglas duras TS (`CONTRIBUTING.md`). El harness espera que el revisor exponga ASS-002; el propio harness no lo hace en dos de sus tres archivos normativos de código.
- **Esperado frente a observado:** el contrato (`audit-contract.md:33`) exige exponer el conflicto y no cerrarlo por preferencia. Lo expongo; no propongo cerrar ASS-002. Observado: las instrucciones no son neutras al stack.
- **Propuesta mínima:** (1) en `CONTRIBUTING.md:97-126`, reescribir las tres reglas duras en términos neutros ("una sola transacción server-side: persistencia → `audit_events` → `event_outbox`", "inbox de webhooks con clave de idempotencia y ACK < 2 s", "concurrencia en la DB") y marcar los nombres de tecnología como "si se ratifica Next.js (ASS-002)"; (2) en `src/CLAUDE.md:99`, cambiar "closed — ADR Z.6" por "propuesto por Z.6; pendiente ASS-002" y corregir `docs/decisions/` por el flujo de `libox-registrar-hallazgo`. Ambos son docs no canónicos, editables por PR. **Alternativa descartada:** borrar `src/CLAUDE.md` y las reglas de `CONTRIBUTING.md` hasta cerrar ASS-002: se perdería el contenido de dominio (transacción única, inbox, unicidad) que es válido en cualquier stack.
- **Validación:** `revisor-pr` con el checklist 4-5 sobre el PR; grep de "closed" y "docs/decisions/" en `src/` y `CONTRIBUTING.md` sin resultados.
- **Incertidumbre:** no consulté Outline doc 20; si ASS-002 se ratificó allí después del snapshot, este hallazgo cambia de naturaleza (el manifiesto `:77` lo excluye).
- **Seguimiento:** `redactor-docs` + Diego. No es ASS- nuevo: es la misma ASS-002.

### FAB-04 — La allowlist de los revisores no acredita "sin shell" frente a herramientas MCP de plugins

- **Severidad:** operativo para el harness (independencia y reproducibilidad de los informes); no patrimonial.
- **Estado:** pendiente de prueba.
- **Naturaleza:** no verificado.
- **Evidencia:**
  - `.claude/agents/libox-audit-fable.md:6-7` y `libox-audit-opus.md:6-7`: `tools: Read, Grep, Glob` · `disallowedTools: Bash, Write, Edit, MultiEdit, Agent`. La lista no menciona herramientas `mcp__*`.
  - `.claude/settings.json:40-53` habilita a nivel proyecto `context-mode@context-mode` (cuya guía inyectada en mi prompt describe `ctx_batch_execute` como "runs commands in parallel" y `ctx_execute` como ejecución de código) y otros plugins. Mi sesión recibió además instrucciones de un MCP `computer-use` (configuración de usuario, fuera del repo).
  - Lo observable en mi sesión: la lista de funciones invocables fue `Read, Grep, Glob, SubagentHandback`; las `ctx_*` aparecían como "diferidas" y su carga exigía `ToolSearch`, que tampoco estaba disponible. No intenté cargarlas: sería un ensayo adversarial sobre el checkout real y el manual lo prohíbe (`ai-audit-harness.md:70-71`).
  - `audit-contract.md:42-44`: "Quitar una herramienta de edición no acredita modo solo lectura si otra herramienta todavía puede escribir".
- **Escenario:** un revisor con plugin `context-mode` activo carga `ctx_batch_execute` y ejecuta shell (lectura o escritura) fuera de la allowlist declarada; el informe seguiría declarando "sin shell".
- **Esperado frente a observado:** el manual afirma "no tienen shell, edición ni delegación" (`ai-audit-harness.md:31-32`). Observado: consistente con mi lista efectiva, pero no demostrado frente a MCP; la semántica de `tools:` vs. herramientas MCP en Claude Code 2.1.282 no está documentada en el repo.
- **Propuesta mínima:** que el coordinador registre en `checks.md` la lista de herramientas efectiva de cada subagente (metadata de ejecución) y, si `tools:` no excluye MCP, añadir `disallowedTools: …, mcp__*` (o los nombres concretos) a ambos agentes y anotarlo en el manual. **Alternativa descartada:** desactivar plugins del proyecto durante auditorías: afecta a todo el equipo y no es reproducible.
- **Validación:** lanzar un subagente de prueba con la misma definición que intente `ToolSearch` + `ctx_execute("echo x")` en una copia desechable; registrar si la herramienta se expone.
- **Incertidumbre:** total sobre el comportamiento real; solo puedo afirmar lo que vi en mi lista de funciones.
- **Seguimiento:** coordinador de la auditoría; PR en `.claude/agents/`.

### FAB-05 — Codex no tiene capa de enforcement; el criterio "controles probados en ambos ejecutores" no se cumple

- **Severidad:** operativo.
- **Estado:** confirmado (por ausencia) / pendiente de prueba (para Codex).
- **Naturaleza:** especificado (AGENTS.md) / no verificado (Codex).
- **Evidencia:**
  - `AGENTS.md:1-6`: entrada por punteros a `CLAUDE.md`, `.claude/rules/`, la skill y el manual. Correcto para descubrimiento (misma fuente, ver Cobertura Q3).
  - Hooks y agentes son nativos de Claude (`.claude/settings.json:17-38`; `sistema-operativo-ia.md:20-22`). Para Codex, E1/E2/E3/B1–B4 son instrucción; la capa efectiva es CI + ruleset (FAB-02 muestra que CD-10 no gatea allí).
  - `2026-09-25-ai-audit-harness-design.md:108`: "Los controles se prueban en ambos ejecutores". `checks.md` §5 no registra ensayo alguno desde Codex.
  - `.gitignore:52-55` deja fuera del ignore `.agents/skills/libox-system-design-audit`, que no existe (Glob: solo `.agents/skills/outline-skills/SKILL.md`). El "adaptador de descubrimiento por herramienta" (`design.md:81`) hoy es solo el puntero de `AGENTS.md`.
- **Escenario:** una sesión de Codex edita `docs/linea-base/…_V9.md` in-place; ningún hook actúa; el PR pasa `commitlint`/`docs`; `verify-corpus` falla sin gatear.
- **Esperado frente a observado:** paridad de controles o límite explícito. Observado: límite parcialmente explícito (`ai-audit-harness.md:33-35`) pero sin ensayo.
- **Propuesta mínima:** añadir a `checks.md` (o a un ensayo dedicado) la prueba H-04 desde Codex sobre copia desechable, y documentar en `AGENTS.md` una línea: "En Codex no hay guards: las restricciones de `.claude/rules/` son norma y las hace cumplir el CI". Quitar la línea muerta de `.gitignore` o crear el adaptador. **Alternativa descartada:** replicar hooks para Codex: sintaxis distinta por ejecutor, doble mantenimiento (`design.md:82`).
- **Validación:** informe `codex-report.md` con evidencia de intento de escritura y resultado.
- **Incertidumbre:** no sé qué mecanismos de permiso ofrece la sesión de Codex de Diego.
- **Seguimiento:** Diego (lanza Codex) + coordinador.

### FAB-06 — Versionar `docs/audits/` romperá `outline-sync` en `main`

- **Severidad:** menor (no bloquea merge; falla un workflow post-merge).
- **Estado:** confirmado (lectura).
- **Naturaleza:** implementado.
- **Evidencia:** `.github/workflows/outline-sync.yml:24-33` (todo `.md` bajo `docs/` debe estar en `outline-map.json` o en `outline-ignore.txt`, comparación exacta `grep -qxF`); `scripts/outline-ignore.txt:1-7` (solo dos rutas, sin soporte de prefijos); Grep de `audits` en `scripts/outline-map.json`: sin coincidencias. `ai-audit-harness.md:103`: "Los informes se versionan después del cierre mediante el flujo normal de PR". `docs.md` exige frontmatter (los informes lo llevan); `.markdownlint-cli2.yaml:21-32` no ignora `docs/audits/`, así que también deben pasar `markdownlint` (MD013 desactivada; tablas largas OK).
- **Escenario:** merge del PR con `manifest.md`, `checks.md`, tres informes y `synthesis.md`; el job `check-map` falla en `main` y `sync` no corre.
- **Esperado frente a observado:** el manual prevé versionar los runs; el CI no lo prevé.
- **Propuesta mínima:** que `check-map` acepte líneas de prefijo terminadas en `/` en `outline-ignore.txt` y añadir `docs/audits/`. **Alternativa descartada:** mapear cada informe a Outline: publica auditorías fuera del repo y obliga a crear placeholders por archivo.
- **Validación:** PR que incluya un `.md` bajo `docs/audits/` con el workflow modificado; `check-map` verde.
- **Incertidumbre:** ninguna relevante.
- **Seguimiento:** PR de CI; `CODEOWNERS` `/.github/`.

### FAB-07 — Metadatos y punteros desactualizados que confunden vigencia y controles

- **Severidad:** menor.
- **Estado:** confirmado (lectura).
- **Naturaleza:** especificado.
- **Evidencia:**
  - `docs/equipo/sistema-operativo-ia.md:5` `updated: 2026-08-30` pese a la sección "Auditoría compartida" (`:99-104`) del 2026-09-25.
  - `.github/CODEOWNERS:7-8` apunta a `/docs/decisions/` y `/docs/plans/` (el primero no existe; Glob vacío). No cubre `docs/linea-base/`, `verify_corpus.py`, `src/` ni `package.json` (`checks.md:67`). `CODEOWNERS:2-4`: sin efecto hasta activar "require code owner review".
  - `CLAUDE.md` raíz ("las reglas hookify están versionados") frente a archivos `.claude/hookify.no-ai-coauthor.local.md` y `.claude/hookify.no-push-main.local.md`: existen en el checkout; no puedo comprobar si están rastreados (sufijo `.local.md`; `.gitignore` no los excluye).
  - `verify_corpus.py:15` "python3 verify_corpus.py # verifica el corpus vigente" frente a `:384` `default="."`: la invocación del docstring produce 15 fallos (`checks.md:30`). Es evidencia H-03 real: un revisor que siga el docstring obtiene un rojo falso.
  - `docs/README.md:24` "10 controles" · Registro V6 `:193` "Los ocho controles" con nueve filas (`:195-205`).
  - `docs/README.md:1-6`: frontmatter sin `description`, exigido por `.claude/rules/docs.md:5-7`.
  - `docs/equipo/sistema-operativo-ia.md:20` dice que `docs.md` es rule por zona; `.claude/rules/docs.md` no tiene `paths:` (se carga siempre). Inocuo, pero inexacto.
- **Escenario:** un ejecutor nuevo (Claude o Codex) lee `updated` o `CODEOWNERS` para decidir vigencia o responsable y obtiene datos falsos.
- **Esperado frente a observado:** `docs.md:5-7` y `estilo-documentacion.md:21-33` exigen frontmatter completo y fechas reales.
- **Propuesta mínima:** corregir `updated`, `description`, `CODEOWNERS` (rutas reales y alta de `docs/linea-base/`, `verify_corpus.py`, `src/`, `package.json`), y el docstring de `verify_corpus.py` (o `default` a `docs/linea-base` si existe). **Atención:** `verify_corpus.py` es artefacto V1 del canon (Registro §1.1 `:62`) y `CANON_FILES` de B3 (`guard_bash.py:29`): cambiarlo exige valorar si requiere emisión V2 por CD-01/CD-11; corregir solo el docstring evita esa duda. **Alternativa descartada:** cambiar el `default` sin versionar: contradice CD-11.
- **Validación:** `markdownlint` + lectura; `python3 verify_corpus.py` sin `--dir` ya no confunde.
- **Incertidumbre:** rastreo git de los archivos hookify.
- **Seguimiento:** `redactor-docs`; Diego decide sobre `verify_corpus.py`.

### FAB-08 — El harness no está listo para arrancar R0 (esquema, auth, RBAC, outbox, backend)

- **Severidad:** bloquea la ejecución de R0 con este harness (no bloquea la auditoría).
- **Estado:** confirmado (por ausencia documentada).
- **Naturaleza:** especificado (lo pendiente está descrito) / no verificado (nada de código existe).
- **Evidencia:**
  - CI sin pasos de código (`checks.md:63`; workflows: `commitlint`, `docs`, `hooks`, `outline-sync`, `release-please`, `verify-corpus`). `CONTRIBUTING.md:95` promete `typecheck`, `test`, `build` "cuando entre el código (Next.js)".
  - Capa `dev` pendiente: `sistema-operativo-ia.md:92-97` (agentes `ejecutor-feature`, `tester`, `depurador` y rule de desarrollo se crean en el PR que cierre ASS-002); `src-congelado.md:26-29` describe el levantamiento (borrar la rule y `FROZEN_*` de `guard_edit.py:17-24` con tests).
  - No hay regla de código para un backend distinto de Next.js; `src/CLAUDE.md` es específico de Next/Supabase/Inngest (FAB-03). La documentación de API con Scalar (manifiesto `:71`) tampoco está en el snapshot.
  - El canon sí aporta lo que R0 necesita en dominio: máquina de estados (`L3_V7.md:2839-2870`, transición única `:2912-2924`), RBAC (`:2914-2916`, §7), outbox (`:2504-2519`, `:3917`), idempotencia (`:1318-1333`, `:3886-3896`), esquema V7 (`libox_schema_L3_V7.sql`, Registro `:58`).
  - Zonas sin IA: Outline doc 20 (ASS-001/002), ruleset y secretos (`onboarding.md:84-88`): fuera del repo; el harness solo puede leerlas vía `gh api` (como hizo el coordinador) y no las revisa de forma continua.
- **Escenario:** Diego ordena "empieza R0: migración 001 + auth"; el ejecutor choca con E2 (`guard_edit.py:85-86`), pide la válvula `LIBOX_DESCONGELAR_SRC=1` (`src-congelado.md:22-24`, reservada a fixes del PR #15 y CI) y, si la obtiene, escribe sin CI de código, sin tester y con reglas de stack contradictorias.
- **Esperado frente a observado:** pregunta 1 del manifiesto. Observado: el harness está listo para trabajo documental y para auditar; para código le faltan las piezas que el propio OS declara pendientes.
- **Propuesta mínima:** una lista de preparación R0 versionada en `docs/equipo/` (no en el canon), ligada al PR que cierre ASS-002: (a) rule `.claude/rules/backend.md` con `paths:` del directorio que se decida, redactada con las reglas de dominio neutras (transacción única, inbox, unicidad en DB, `trace_id`); (b) workflow `code.yml` (build, test, lint) requerido en el ruleset; (c) agentes `ejecutor`/`tester`; (d) borrado de `FROZEN_*` con sus tests; (e) alta de `src/`/backend en `CODEOWNERS`. **Alternativa descartada:** abrir la válvula E2 para "adelantar" R0 con Next.js: equivale a cerrar ASS-002 por la vía de los hechos, que el contrato prohíbe (`audit-contract.md:24-25`).
- **Validación:** `hooks.yml` verde tras borrar `FROZEN_*`; primer PR de código bloqueado si `code.yml` falla.
- **Incertidumbre:** desconozco el estado de ASS-002 en Outline (no consultado, manifiesto `:77`).
- **Seguimiento:** Diego (decisión) y el PR de cierre de ASS-002.

### FAB-09 — Seis de ocho escenarios H-xx sin evidencia ejecutada y sin fixtures versionadas

- **Severidad:** operativo para la reproducibilidad del harness.
- **Estado:** confirmado (`checks.md` §5).
- **Naturaleza:** no verificado.
- **Evidencia:** `checks.md:73-79` (H-01, H-02, H-06 "queda para un ensayo dedicado"; H-05 sin inyección; H-07 sin reintento; H-08 sin credencial sintética y saneo procedimental). El script del ensayo H-04 vive en el scratchpad del coordinador (`checks.md:36`), fuera del repo. `design.md:109-110`: "Los casos del contrato tienen evidencia o una limitación explícita" (cumplido como limitación) y "El intento de modificar un área protegida se prueba en una copia desechable" (cumplido para Claude, no para Codex: FAB-05). H-03 sí tiene evidencia real (`checks.md:30`, y FAB-07 sobre el docstring).
- **Escenario:** un run futuro no puede repetir H-04 con los mismos payloads; H-01/H-02 dependen de la lectura de cada revisor sobre el snapshot real (en este run, FAB-03 hace de H-02 y la comprobación Registro/BASELINE de la sección Cobertura hace de H-01, ambas sin copia manipulada).
- **Esperado frente a observado:** contrato `:28-39`. Observado: 2/8 ejecutados, 6/8 con limitación declarada.
- **Propuesta mínima:** versionar `scripts/audit/ensayo_guards.py` (payloads sintéticos, sin secretos) y un test en `scripts/hooks/tests/` que lo ejecute; documentar en el manual un procedimiento manual con fixtures para H-01 (copia con `…_V10.md` falso no listado en BASELINE) y H-02 (rule contradictoria) que el coordinador prepara en la copia desechable antes de lanzar. **Alternativa descartada:** automatizar H-01/H-02/H-06 con LLM en CI: coste y no determinismo.
- **Validación:** `hooks.yml` ejecuta el ensayo; un run posterior cita el mismo script.
- **Incertidumbre:** ninguna sobre el estado; sí sobre el coste de preparar fixtures.
- **Seguimiento:** coordinador + `/scripts/` (`CODEOWNERS`).

### FAB-10 — Sin mapa de evidencia para una ejecución `producto`: RPO/RTO ausentes y comparación .NET/TS asimétrica

- **Severidad:** menor para el harness; relevante para la comparabilidad de la futura revisión de producto.
- **Estado:** confirmado (lectura).
- **Naturaleza:** especificado (contrato) / no verificado (producto).
- **Evidencia:** `audit-contract.md:46-66` lista doce áreas y exige comparar .NET y TypeScript "sobre el mismo flujo y garantías". En el snapshot solo existe el lado TS (`CONTRIBUTING.md:97-126`, `src/CLAUDE.md`, scaffold Next.js); del lado .NET solo `L3_V7.md:162`. Grep en L3 V7 de `backup|restaur|PITR|RPO|RTO`: sin resultados para recuperación de base de datos (coincide con manifiesto `:74`); el único "punto de recuperación" es el de sesión de pago (`L3_V7.md:3788`, RN-218). La única mención a PITR está en `CONTRIBUTING.md:121` (checklist TS). El contrato no mapea área → documento/sección, así que cada revisor buscará por su cuenta (yo localicé: estados §4 `:2839-2924`, concurrencia §12 `:3862-3943`, operación §13 `:3945-3986`, pruebas de concurrencia §14.4 `:4065-4075`).
- **Escenario:** run `producto`: Fable, Opus y Codex citan secciones distintas para la misma área; la síntesis no puede cruzar evidencia.
- **Esperado frente a observado:** "evidencia comparable" (pregunta 5). Observado: comparable en procedimiento, no en localización de fuentes.
- **Propuesta mínima:** que el manifiesto `producto` incluya una tabla "área del contrato → documento y sección vigente (o `desconocido`)", preparada por el coordinador; registrar de antemano RPO/RTO y el lado .NET como desconocidos. **Alternativa descartada:** ampliar el contrato con las secciones: el contrato es estable y las secciones cambian con cada versión del canon.
- **Validación:** primera síntesis `producto` con una columna "evidencia decisiva" que cite la misma sección en los tres informes.
- **Incertidumbre:** no leí la Matriz de Casos de Uso V1 ni la Guía de Extensión V1, que podrían cubrir parte de "Operación" y "Recuperación".
- **Seguimiento:** coordinador del próximo run.

## Verificaciones

### Evidencia ejecutada (por el coordinador, `checks.md`; no reproducida por mí)

| Comando o prueba | Entorno y snapshot | Resultado y código de salida | Evidencia saneada |
|---|---|---|---|
| `python3 verify_corpus.py --dir docs/linea-base` | checkout real, `471a28d` | sin fallos, 0 avisos · exit 0 | `checks.md:28` |
| `python3 -m unittest discover -s scripts/hooks/tests -v` | checkout real | 53 tests OK · exit 0 | `checks.md:29` |
| `python3 verify_corpus.py` (sin `--dir`, H-03) | checkout real | 15 fallos · exit 1 | `checks.md:30`; explicado por `verify_corpus.py:384` |
| Ensayo E1–E3, OK1, W1–W2, S1–S3, B1–B2b, F1 | copia desechable (`git archive`) | ver `checks.md:38-55` | tabla saneada, sin secretos |
| Lectura del ruleset `main protection` (`gh api`) | cuenta GitHub | activo; checks requeridos `commitlint`, `markdownlint`, `links`; solo rebase | `checks.md:68-69` |
| Grep de pasos de código y saneo de secretos en hooks | checkout real | ninguno / 0 coincidencias | `checks.md:63-65` |

### Evidencia documental (mi lectura al SHA)

| Comprobación | Resultado |
|---|---|
| Conteo de tests por lectura: `test_guard_edit.py` (6+7+10+3 = 26), `test_guard_bash.py` (3+5+6+3+2 = 19), `test_corpus_check.py` (3), `test_session_status.py` (5) | 53, coincide con `checks.md:29` |
| Vigencia: `CLAUDE.md` (V6, V9), `docs/README.md:22`, Registro V6 §1 `:21-36`, `verify_corpus.py` BASELINE `:34-50`, manifiesto `:27` | Coinciden en documentos y versiones. Sin PRD con número mayor al vigente en `docs/linea-base/` (Glob: 16 archivos, ninguno `_V10+`) → H-01 sin falso positivo en el snapshot real |
| `AGENTS.md` → `CLAUDE.md` → `.claude/rules/` → Registro: misma cadena para Claude y Codex | Sí (`AGENTS.md:3-6`); diferencias solo en enforcement (FAB-05) |
| Hooks referencian scripts existentes (`settings.json:8,12,23,33`) | `scripts/team-digest.sh`, `session_status.py`, `guard_bash.py`, `guard_edit.py` existen |
| Guards fallan abiertos ante error propio (`guard_edit.py:97-98,103-105`; `guard_bash.py:75-76,88-90`) | Confirmado y testeado (`test_guard_edit.py:126-130`, `test_guard_bash.py:103-108`). Diseño deliberado; implica que F1 (payload no JSON) permite |
| Skill de auditoría < 80 líneas (`sistema-operativo-ia.md:87`) | Sí (≈40 líneas) |
| Referencias de `src/CLAUDE.md` a specs (`2026-08-11-rate-limiting-design.md`, Z6) | Existen (`docs/superpowers/specs/`, `docs/archive/decisions/`) |

### Pendiente (no ejecutable por mí)

| Prueba | Motivo |
|---|---|
| H-01, H-02, H-05, H-06, H-07, H-08 en copia manipulada | Sin shell; el coordinador no los ejecutó (`checks.md:73-79`) |
| Bypasses deducidos (`HEAD:refs/heads/main`, `git -c user.email`, `--trailer`, `NotebookEdit`) | Sin shell; deducción por regex (FAB-01) |
| Exposición de herramientas MCP a subagentes con `tools:` restringido | No intentado por política (FAB-04) |
| Controles desde Codex | No hay sesión Codex en este informe (FAB-05) |
| Estado de ASS-001/ASS-002 en Outline doc 20 | Excluido por el manifiesto `:77` |
| Rastreo git de `.claude/hookify.*.local.md` | Sin `git ls-files` |

## Cobertura y límites

### Preguntas del manifiesto

| Pregunta | Respuesta breve | Hallazgos |
|---|---|---|
| 1. ¿Listo para R0? | No como harness de código; sí como harness documental y de auditoría | FAB-08, FAB-03 |
| 2. Controles efectivos y capa | Ver tabla siguiente | FAB-01, FAB-02, FAB-05 |
| 3. ¿Claude y Codex ven lo mismo? | Sí en reglas y versiones (misma cadena de punteros y mismo Registro/BASELINE); no en enforcement | FAB-05, FAB-07 |
| 4. ¿Qué falta para código? | CI de código, rule backend neutra, capa `dev`, levantamiento ordenado del freeze, CODEOWNERS de código; zonas sin IA fuera del repo | FAB-08, FAB-07 |
| 5. ¿Puede auditar system design con evidencia comparable? | En procedimiento sí (manifiesto, contrato, plantilla, checks); falta mapa de evidencia y fixtures reproducibles | FAB-09, FAB-10 |
| 6. Cobertura H-01…H-08 | Ver tabla de escenarios | FAB-09 |

### Controles y capa que los impone

| Control | Capa efectiva | Límite observado |
|---|---|---|
| Canon in-place (E1) | Hook (`guard_edit.py:87-90`) solo para Edit/Write/MultiEdit en Claude | Shell (S1), worktrees (W2), Codex; CI `verify-corpus` no requerido (FAB-02) |
| `src/` congelado (E2) | Hook (`guard_edit.py:84-86`) | Shell (S2, S3), worktrees (W1), Codex; sin CODEOWNERS |
| Naming legacy (E3) | Hook (`guard_edit.py:91-95`), allowlist | Solo contenido nuevo por tool de edición |
| Sin trailers de IA (B1) | Hook textual (`guard_bash.py:20-22,59-60`) + hookify (`.claude/hookify.no-ai-coauthor.local.md`) | `-F archivo` (B1b); CI no lo valida (`checks.md:64`); `revisor-pr` lo revisa solo si se invoca |
| No push a `main` (B2) | Hook + hookify + **ruleset** (`pull_request`, `non_fast_forward`) | Hook: `push` sin args, `refs/heads/main`; el ruleset es la capa real |
| CD-10 al commitear (B3) | Hook (`guard_bash.py:68-74`) | Solo Claude/Bash; CI informativo (FAB-02) |
| Correo `@liboxapp.com` (B4) | Hook + **CI** (`commitlint.yml:21-30`) | Hook lee config, no el comando; CI es la capa real |
| Conventional Commits | CI requerido (`commitlint`) | — |
| Links y markdown | CI requerido (`docs`) | `docs/linea-base` y `.claude` excluidos del lint (`.markdownlint-cli2.yaml:23-32`) |
| Revisión de dueño | Instrucción (`CODEOWNERS` inactivo) | FAB-07 |
| Solo lectura de revisores | Permiso de agente (`tools:`) | MCP no verificado (FAB-04) |
| Claims legales, precedencia L0>L2>L3>L4, español | Instrucción | Sin control técnico; correcto por naturaleza |

### Escenarios del harness H-01…H-08

| ID | Revisado | Resultado | Falta comprobar |
|---|---|---|---|
| H-01 | Documental sobre snapshot real | Registro §1, BASELINE y README coinciden; sin PRD de número mayor presente | Copia con `…_V10.md` falso (FAB-09) |
| H-02 | Documental sobre snapshot real | Conflicto expuesto en el propio harness (FAB-03); no cerrado por preferencia | Copia con rule contradictoria |
| H-03 | Ejecutado por coordinador | `verify_corpus.py` sin `--dir` falla (15) y se registró como fallo, no como éxito; docstring engañoso (FAB-07) | — |
| H-04 | Ejecutado por coordinador (Claude) | E1/E2/E3 deniegan por tool; shell y worktrees permiten (FAB-01) | Desde Codex (FAB-05); MCP (FAB-04) |
| H-05 | No ejecutado | El manual exige recomprobar HEAD antes de sintetizar (`ai-audit-harness.md:92-95`); yo no puedo comprobarlo | Inyección de cambio de snapshot |
| H-06 | No ejecutado | Plantilla y diseño lo prescriben (`report-template.md:66-75`, `design.md:98`) | Ensayo con dos informes coincidentes sin fuente |
| H-07 | No ejecutado | Convención `-attempt-2.md` (`ai-audit-harness.md:78-79`) | Reintento real |
| H-08 | No ejecutado | Saneo procedimental; hooks sin secretos (`checks.md:65,78`) | Credencial sintética en flujo |

### Escenarios comunes del producto (evaluación de diseño sobre L3 V7; no se reporta ejecución)

| # | Escenario | Resultado esperado | Mecanismo en el canon | Evidencia | Prueba pendiente | Responsable |
|---|---|---|---|---|---|---|
| 1 | Dos compras por el último boleto | Exactamente una emitida | `UPDATE … WHERE tickets_reserved + qty <= total_tickets` atómico, sin lectura previa; `ck_raffles_reserved` | `L3_V7.md:3868-3880`, `:868`, `conc_last_tickets` `:4069` | Implementación y prueba de concurrencia con DB real | Equipo backend (R0) |
| 2 | Misma solicitud dos veces | Una orden; segunda devuelve respuesta almacenada o 409 | `idempotency_keys` con `ux_idem`, flujo IN_FLIGHT/COMPLETED, clave por intento generada por el cliente | `:1318-1333`, `:3886-3896`, `:3480-3481`, `conc_double_click` `:4071` | Contrato OpenAPI con `Idempotency-Key` obligatoria (`:3758`) en todas las mutaciones | Backend + contrato |
| 3 | Proveedor acepta el pago y la llamada agota el tiempo | Estado inequívoco por consulta; sin doble cobro ni ticket perdido | Consulta de estado como punto de recuperación (RN-218 `:3788`); conciliación diaria (`:3924`); runbook "webhooks no llegan" (`:3982`) | Parcial: no hay política explícita de timeout en la creación de orden ni de estado `IN_FLIGHT` frente al PSP | Definir timeout, reintento con la misma clave externa y cola de excepciones; ensayo con proveedor real, no mocks | Backend + producto |
| 4 | Webhook repetido, tardío o fuera de orden | Un procesamiento; monotonía de estado; 200 siempre | `psp_events` con dedupe por hash, `status_rank`, FAILED con reintento exponencial | `:3898-3906`, `conc_duplicate_webhooks` `:4070`, cross-month `:4074` | Firma y ventana anti-repetición del PSP real | Backend |
| 5 | Caída tras commit y antes de publicar | Evento publicado por outbox; sin pérdida | `event_outbox` en la misma transacción de toda transición (`:2912-2922`), `dispatch-outbox` 10 s (`:3917`), alerta > 5 min (`:3968`) | `:2504-2519` | Prueba de caída controlada; retención 90 días (`:209`) | Backend + operación |
| 6 | Expira la reserva y luego se confirma el pago | Sin ticket sin pago ni pago sin ticket; resolución definida | `orders.reserved_until` (RN-55 `:1353`), estados `PENDING_PAYMENT/PAID/EXPIRED` (`:1351`), `release-expired-reservations` (`:3912`) | Parcial: no localicé la regla para pago confirmado sobre orden `EXPIRED` (¿reemisión si hay inventario o reembolso automático?) | Confirmar la regla en PRD V9/L3 §3.4 o registrarla como CHANGE- vía `libox-registrar-hallazgo` | Producto |
| 7 | Doble reembolso o doble liquidación | Un solo efecto patrimonial | `ux_settlement_raffle UNIQUE` (`:1951`), gates (`:1955`), INV-16 (`:3357`), `conc_refund_credit` (`:4072`) | Reembolso de orden: estado `REFUNDED` (`:1352`) + idempotencia; sin prueba nombrada para "reembolso de la misma orden dos veces" | Añadir caso de prueba explícito | Backend |
| 8 | Cae Redis, el proveedor o el servicio de workflows | Sin pérdida de dinero; degradación declarada | RN-56 Redis nunca autoritativo (`:164`, `:3866`); runbook proveedor caído (`:3981`); trabajos idempotentes con bloqueo único (`:3943`) | Workflows: el canon usa trabajos programados; `src/CLAUDE.md:75-76` propone Inngest (ASS-002); rate limit "fail-open" (`src/CLAUDE.md:96`) es decisión TS no canónica | Definir modo de fallo por componente en el stack ratificado | Producto + Diego |
| 9 | Restauración de base y tareas ya procesadas reaparecen | Reejecución segura | Solo "todos idempotentes" (`:3943`); sin RPO/RTO ni ensayo de restauración | Ausente (FAB-10; manifiesto `:74`) | Definir RPO/RTO y ensayo coherente con auditoría y ledger | Diego + operación |
| 10 | Acumulación y diagnóstico por un operador | Trazas, alerta, reintento acotado | `trace_id` transversal (`:3949`), alertas (`:3965-3975`), runbooks (`:3977-3986`), `retry-audit-emergency` (`:3918`) | Sin superficie de operador para reintentar/inspeccionar colas | Manual de operación (README `:54`, T-3) | Operación |

### Áreas revisadas sin hallazgos

| Área | Revisado | Resultado |
|---|---|---|
| Skills `libox-pr`, `libox-versionar-doc`, `libox-registrar-hallazgo`, `libox-outline-sync` | Lectura completa | Coherentes con `linea-base.md`, CD-01…CD-11 y la regla de no-trailers; `libox-outline-sync` correctamente `disable-model-invocation` |
| Agentes `auditor-corpus`, `redactor-docs`, `revisor-pr` | Lectura completa | Herramientas mínimas; `revisor-pr` cubre trailers, canon, `src/`, hooks |
| `session_status.py`, `corpus_check.py`, `team-digest.sh` | Lectura completa | Fallan abiertos; sin secretos; salida breve |
| `hooks.yml`, `docs.yml`, `commitlint.yml`, `release-please.yml` | Lectura completa | Correctos en su alcance; `docs.yml` explica bien el problema de checks requeridos |
| `src/tools`, `src/workflows`, `src/tests` `CLAUDE.md` | Lectura completa | Exentos de E2 por diseño; contenido de proceso, no de stack (salvo `npm`/Vitest en `tests`) |
| Registro Maestro V6 §0–§4 | Lectura | Regla de uso, §1, §2, CD-01…CD-11 claros; verificados contra BASELINE |
| Skill `outline-skills` (tercero) | Lectura | Solo ejemplos `ol_api_xxx` de plantilla, no credenciales |

### Límites de esta revisión

- Sin shell: nada ejecutado por mí; la evidencia ejecutada es del coordinador.
- No leí en su totalidad L3 V7 (≈4.100 líneas): leí §0.3, §3.4, §4, §12, §13, §14.4 y greps dirigidos. No leí PRD MVP V9, Matriz V1, Guía V1, LBPF, L1, L4, VIES, Backlog ni Dossier: fuera del alcance `harness` salvo vigencia.
- No leí `docs/superpowers/specs/2026-08-30-sistema-operativo-ia-design.md`, `docs/flujos/`, `docs/glosario.md`, `scripts/outline-sync.sh` ni `scripts/outline-map.json` completo (solo grep).
- No consulté Outline ni ninguna fuente externa.
- Modelo efectivo no verificado; este informe no lo acredita.
- Ninguna afirmación de este informe ratifica ASS-001 o ASS-002. Los aspectos legales del producto no se tocaron; cualquier implicación de custodia queda `[LEGAL→ABOGADO]`.
