---
title: Sistema operativo de IA — capa operativa de Claude Code para el equipo
status: aprobado
tags: [libox, equipo, claude-code, hooks, skills, agentes, spec]
updated: 2026-08-30
description: Diseño de la capa operativa de IA del repo (contexto, enforcement, capacidades, manual, memoria). Versionada, reproducible al clonar, agnóstica al stack hasta que se ratifique ASS-002.
---

# Sistema operativo de IA — capa operativa de Claude Code para el equipo

Aprobado por Diego (2026-08-30), sección por sección, en sesión de
brainstorming. Define cómo Claude Code trabaja en este repo para **cualquier**
integrante del equipo, no solo para quien lo configuró: qué contexto carga,
qué reglas hace cumplir el harness (no la buena voluntad del modelo), qué
procedimientos y subagentes propios existen, dónde vive el manual y qué papel
juega la memoria personal.

## 1. Problema y objetivos

Hoy la capa de IA del repo está repartida entre un `CLAUDE.md` narrativo de
96 líneas, [`src/CLAUDE.md`](../../../src/CLAUDE.md), dos reglas hookify, un
skill compartido, la memoria personal de Diego y el folder `Context/` de
Cowork (fuera del repo). Varias reglas están repetidas en tres o cuatro sitios
y ninguna de las reglas del canon (CD-01…CD-11) la hace cumplir el harness.

Objetivos, en orden de importancia acordado:

1. **Reproducibilidad.** Al clonar, cualquier dev y su Claude trabajan con las
   mismas reglas, guards, skills y agentes, sin depender de memoria personal
   ni de `Context/`.
2. **Enforcement automático del canon.** Lo bloqueante lo bloquea un hook con
   script testeado: CD-10 (`verify_corpus.py` a cero), no editar la línea base
   in-place, no extender `src/` mientras ASS-002 siga abierto, naming Libox,
   sin co-autor de IA.
3. **Flujo orquestado y barato.** Operacionalizar "Fable orquesta / Opus
   ejecuta" con agentes y skills propios, y pagar contexto solo donde aplica.
4. **Higiene.** Alinear el estado real de la máquina y del repo con lo que
   dicen `CLAUDE.md` y [ADR Z.8](../../archive/decisions/Z8-roles-memoria-contexto.md).

### Restricciones

- **Agnóstico al stack.** ASS-002 (Next.js vs .NET 8) sigue sin ratificar.
  Nada en esta capa presupone un stack; los agentes de desarrollo llegan
  después, como una capa `dev` adicional, sin reescribir esta.
- **El repo es la fuente de verdad.** Ni Outline ni la auto-memory ni
  `Context/` gobiernan. Todo lo que aquí se decide se versiona.
- **Idioma español** en todo lo que lee un humano; identificadores técnicos
  en inglés donde el harness lo exige.

## 2. Enfoque elegido

Se evaluaron tres:

| | A. Repo como OS, primitivas nativas (elegido) | B. Plugin `libox` instalable | C. Mínimo incremental |
|---|---|---|---|
| Dónde vive | `CLAUDE.md` + `.claude/{rules,skills,agents,settings.json}` + `scripts/hooks/` + `docs/equipo/` | Marketplace propio de la org | Solo `.claude/rules/` y 2–3 skills |
| Dependencias para los guards | Ninguna (hooks nativos + Python stdlib) | Plugin instalado | Plugin hookify |
| Testeable | Sí (`unittest`) | Sí | Parcial |
| Sincronía con el canon | Inmediata (mismo repo) | Se desincroniza fácil | Inmediata |
| Cumple objetivos 2 y 3 | Sí | Sí | No |

Ajuste aprobado sobre A: **hookify se conserva** como segunda línea para
co-autor y push a `main` (redundancia deliberada); los hooks nativos cubren lo
mismo y añaden el resto.

## 3. Arquitectura: cinco capas, todas en el repo

```
Libox/
├── CLAUDE.md                        [1] contexto: ~40 líneas, reglas + punteros
├── src/CLAUDE.md                        se conserva; banner "congelado por ASS-002"
├── .claude/
│   ├── settings.json                [2] hooks nativos + plugins del equipo
│   ├── rules/                       [1] reglas por ruta
│   │   ├── linea-base.md              docs/linea-base/**
│   │   ├── docs.md                    docs/**
│   │   ├── src-congelado.md           src/** + config del scaffold
│   │   └── git.md                     global
│   ├── skills/                      [3] procedimientos Libox
│   │   ├── libox-versionar-doc/
│   │   ├── libox-registrar-hallazgo/
│   │   ├── libox-outline-sync/
│   │   ├── libox-pr/
│   │   └── outline-skills/            (existente)
│   └── agents/                      [3] subagentes Libox, model: opus
│       ├── redactor-docs.md
│       ├── auditor-corpus.md
│       └── revisor-pr.md
├── scripts/hooks/                   [2] un script por evento + tests
│   ├── guard_bash.py
│   ├── guard_edit.py
│   ├── session_status.py
│   └── tests/test_guards.py
├── .github/workflows/hooks.yml      [2] CI de los guards
└── docs/equipo/                     [4] manual humano del OS
    ├── sistema-operativo-ia.md
    ├── estilo-documentacion.md        (migra desde Context/)
    └── onboarding.md                  (migra desde docs/onboarding.md)
[5] Memoria: auto-memory personal = preferencias del individuo;
    hechos del proyecto se promueven a docs/. Sin claude-mem ni GSD (Z.8).
```

Principios:

1. **Una regla, un lugar.** Cada regla vive en un archivo; `CLAUDE.md` apunta.
2. **Enforcement > exhortación.** El texto explica el porqué; el hook bloquea.
3. **Contexto pagado solo donde aplica.** Rules con `paths:` se inyectan
   cuando Claude lee un archivo coincidente, no al arrancar.
4. **Agnóstico al stack** (ver restricciones).
5. **Cero dependencia de plugins para lo crítico.**
6. **`Context/` deja de ser fuente**: migra a `docs/equipo/` y queda como
   puntero para las sesiones de Cowork.

## 4. Capa de contexto

### 4.1 `CLAUDE.md` raíz (~40 líneas)

| Bloque | Contenido |
|---|---|
| Qué es el repo | 3 líneas: marketplace de sorteos con boleto pagado; canon en `docs/linea-base/` gobernado por el Registro Maestro V6; scaffold `src/` congelado por ASS-002. |
| Empieza por | `docs/README.md` → `docs/equipo/sistema-operativo-ia.md`. |
| Reglas firmes | Una línea cada una, con puntero: español · naming Libox (Sortibox/ALAZAR = legacy, léase Libox) · sin co-autor de IA · `[LEGAL→ABOGADO]` · línea base congelada (CD-07). |
| Orquestación | Fable orquesta / Opus ejecuta → puntero al manual. |
| Decisiones abiertas | ASS-001 y ASS-002 con puntero a Outline doc 20. |

Sale de `CLAUDE.md`: el listado de las 8 decisiones Z (ya está en
[`docs/archive/decisions/README.md`](../../archive/decisions/README.md)), la
capa Outline (ya está en [`docs/README.md`](../../README.md)), el layout de
Cowork y los roles de memoria (van al manual), los "key product facts" (están
en el PRD V9; `CLAUDE.md` solo apunta).

### 4.2 `.claude/rules/`

| Archivo | `paths` | Contenido |
|---|---|---|
| `linea-base.md` | `docs/linea-base/**` | Nunca editar un doc vigente in-place: nueva versión completa V(n+1) (CD-01/02/08). Identidad en cuatro lugares (CD-03). Changelog interno (CD-04). Autonomía (CD-06). Emisión = `verify_corpus.py` a cero + `BASELINE` + Registro §1 en el mismo commit (CD-10/11). Hallazgos → backlog de cambio (CD-07). Precedencia L0 > L2 > L3 > L4; VIES en marca. Usar `libox-versionar-doc`. |
| `docs.md` | `docs/**` | Español. Frontmatter `title/status/tags/updated/description`. Links markdown relativos a `docs/`, nunca wikilinks. ~150 líneas → partir. Tono directo. `docs/archive/` no se cita. Estructura de ADR. Condensa `estilo-documentacion.md`. |
| `src-congelado.md` | `src/**`, `package.json`, `next.config.ts`, `tsconfig.json`, `components.json`, `eslint.config.mjs`, `postcss.config.mjs` | ASS-002 abierto: no crear ni extender código. Excepciones: fixes al PR #15 ya abierto y lo que exija el CI, con la válvula de escape del guard E2. Cómo se levanta el freeze. |
| `git.md` | (global) | Rama `<type>/<kebab>` desde `main`; Conventional Commits en español; correo `@liboxapp.com`; sin trailers de IA; `gh pr create` sin "Generated with"; rebase-and-merge; `main` protegido. Puntero a `CONTRIBUTING.md`. |

`src/CLAUDE.md` se conserva como spec de código para cuando se descongele, con
un banner de tres líneas que remite a `src-congelado.md`; su sección de
orquestación se reduce a un puntero al manual.

## 5. Capa de enforcement

Scripts en **Python 3 stdlib** (ya es requisito por `verify_corpus.py`; evita
`jq`). Protocolo de hooks: leen JSON por stdin; bloquean con exit 2 y mensaje
por stderr; la decisión "preguntar" se emite como JSON de
`hookSpecificOutput`. Los guards aceptan tanto `file_path`/`content` como
`path`/`file_text` en `tool_input`, y los nombres exactos se fijan con
fixtures capturados de una sesión real antes de escribir el código.

### 5.1 `guard_bash.py` — `PreToolUse`, matcher `Bash`

| # | Detecta en `tool_input.command` | Acción |
|---|---|---|
| B1 | `git commit` con `Co-Authored-By`, `Generated with Claude` o `noreply@anthropic.com` | Bloquea. |
| B2 | `git push` hacia `main` (misma regex que la regla hookify `no-push-main`) | Bloquea. |
| B3 | `git commit` con archivos staged bajo `docs/linea-base/**` o `verify_corpus.py` | Corre `python3 verify_corpus.py --dir docs/linea-base`; si hay fallos, bloquea y muestra las últimas líneas. Cubre "doc nuevo sin alta en `BASELINE`" (check `documento-no-declarado`). |
| B4 | `git commit` con `git config user.email` fuera de `@liboxapp.com` | Bloquea e indica el `git config` a ejecutar. |

### 5.2 `guard_edit.py` — `PreToolUse`, matcher `Edit|Write|MultiEdit`

| # | Detecta | Acción | Válvula de escape |
|---|---|---|---|
| E1 | Escritura sobre un archivo **existente** cuyo nombre contiene `_V<n>` bajo `docs/linea-base/` (incluye `ARTEFACTOS/`) | Bloquea: "los docs vigentes no se editan; emite V(n+1) con `libox-versionar-doc`". Archivos nuevos y `LEEME.md` pasan. | Variable de entorno `LIBOX_PERMITIR_INPLACE=1`. |
| E2 | Cualquier escritura bajo `src/**` o en los archivos de config listados en `src-congelado.md` | Bloquea: "ASS-002 abierto" + cómo se levanta. | `LIBOX_DESCONGELAR_SRC=1`. El freeze se retira en el PR que cierre ASS-002 borrando la rule y la constante del script. |
| E3 | Contenido nuevo con `Sortibox` o `ALAZAR` (palabra completa, sin distinguir mayúsculas) fuera de `docs/archive/**` | **Pregunta** al usuario en lugar de bloquear: hay archivos legítimos que nombran la regla. Si la versión del harness no soporta la decisión de preguntar, bloquea con allowlist (`CLAUDE.md`, `CONTRIBUTING.md`, `.claude/rules/*`, `docs/equipo/*`). | Confirmar en el prompt. |

### 5.3 `session_status.py` — `SessionStart`

Se ejecuta después de `scripts/team-digest.sh`. Imprime tres líneas: rama
actual · "ASS-002 abierto — `src/` congelado" (deducido de la existencia de
`src-congelado.md`) · resultado de `verify_corpus.py` en una línea. Coste
aproximado: 60 tokens por sesión.

### 5.4 Lo que deliberadamente no hay

Hooks en `Stop` o `UserPromptSubmit` (coste por turno sin beneficio claro) y
guards sobre Outline (el MCP no pasa por Bash; la disciplina queda en el skill
`libox-outline-sync`).

### 5.5 Tests y CI

`scripts/hooks/tests/test_guards.py` con `unittest`: cada fila de 5.1 y 5.2
tiene al menos un caso "debe bloquear" y uno "debe pasar", con fixtures JSON
idénticos a los que envía Claude Code. Se ejecuta con
`python3 -m unittest discover scripts/hooks/tests` y en CI con
`.github/workflows/hooks.yml` (dispara ante cambios en `scripts/hooks/**` y
`.claude/**`). Los guards se escriben con TDD: primero el test rojo, luego el
script.

### 5.6 `settings.json`

Registra los tres hooks (con `$CLAUDE_PROJECT_DIR` en las rutas) junto al
digest existente. `enabledPlugins` mantiene la lista actual y añade
`"claude-mem@thedotmack": false` y `"vercel-plugin@vercel": false` para que
queden desactivados a nivel de proyecto aunque alguien los tenga a nivel de
usuario (Z.8; el audit de 2026-08-03 los retiró).

## 6. Capa de capacidades

### 6.1 Skills (`.claude/skills/libox-*/SKILL.md`)

Procedimientos cortos (< 80 líneas) que apuntan al canon en lugar de copiarlo.

| Skill | Cuándo | Pasos | Invocación |
|---|---|---|---|
| `libox-versionar-doc` | Hay que cambiar un doc de `docs/linea-base/` | 1) Verifica que el cambio justifica romper el freeze (CD-07); si no, deriva a `libox-registrar-hallazgo`. 2) Copia `X_V<n>` → `X_V<n+1>`, actualiza identidad en cuatro lugares (CD-03) y changelog (CD-04). 3) Actualiza `BASELINE` y Registro §1 (CD-11); si el Registro cambia, también sube de versión. 4) `verify_corpus.py` a cero. 5) Rama + PR con `libox-pr`. 6) Tras merge, `libox-outline-sync`. | Modelo o humano |
| `libox-registrar-hallazgo` | Observación, supuesto, riesgo o idea que no genera versión | Clasifica (ASS-/CHANGE-/RISK-/IDEA-), redacta con la plantilla del doc 20 de Outline y la crea vía MCP; si es CHANGE-, anota también en el backlog de cambio (CD-07). Devuelve el ID. | Modelo o humano |
| `libox-outline-sync` | Se mergeó un cambio en `docs/` con espejo | Envuelve `scripts/outline-sync.sh` y `outline-map.json`: detecta qué cambió desde el último sync, publica, reporta. Requiere `OUTLINE_API_KEY`. | Solo humano (`disable-model-invocation: true`): publica fuera del repo |
| `libox-pr` | Trabajo listo para integrar | Comprueba rama ≠ `main`, correo, commits convencionales en español sin trailer; `git push -u`; `gh pr create` con plantilla (qué / por qué / verificación) sin "Generated with". | Modelo o humano |
| `outline-skills` | (existente) | Operaciones genéricas sobre Outline. | — |

### 6.2 Agentes (`.claude/agents/*.md`)

Encarnan "Fable orquesta / Opus ejecuta": `model: opus`, herramientas mínimas,
brief autocontenido. El orquestador nunca releva un "listo" sin verificar.

| Agente | `tools` | Misión | Devuelve |
|---|---|---|---|
| `redactor-docs` | Read, Grep, Glob, Write, Edit | Redactar o editar documentación **no canónica** (`docs/equipo`, `docs/flujos`, glosario, specs) siguiendo `rules/docs.md`. Para canon, solo prepara el borrador de V(n+1) que luego pasa por `libox-versionar-doc`. | Rutas tocadas + resumen de cinco líneas |
| `auditor-corpus` | Read, Grep, Glob, Bash · `disallowedTools: Write, Edit` | Corre `verify_corpus.py`, cruza cifras y reglas entre docs, detecta contradicciones que el script no cubre (p. ej. L3 §0.3 vs Z.6), propone hallazgos ya clasificados para `libox-registrar-hallazgo`. | Informe con hallazgos, sin tocar archivos |
| `revisor-pr` | Read, Grep, Glob, Bash · sin escritura | Revisa un PR contra `CONTRIBUTING.md` y las rules: commits, correo, trailers, links relativos, frontmatter, que no toque `linea-base` in-place ni `src/`. | Veredicto aprobar / cambios, con lista puntual |

**Capa `dev` diferida** hasta que cierre ASS-002: `ejecutor-feature`,
`tester`, `depurador` y una rule de desarrollo para `src/`. Se documenta como
pendiente en el manual.

## 7. Manual, migraciones, memoria e higiene

### 7.1 `docs/equipo/sistema-operativo-ia.md` (~120 líneas)

Secciones: qué es y por qué · las cinco capas y dónde vive cada una · cómo
trabaja una sesión (leer README → identificar zona → rule aplicable → skill si
existe) · orquestación Fable/Opus (cuándo delegar, forma del brief, gate de
revisión, "si un worker falla dos veces con el mismo brief, el orquestador toma
el control") · guards activos y sus válvulas de escape · memoria: qué va dónde
· cómo extender el OS (rule/skill/agente/guard = PR con test) · capa `dev`
pendiente de ASS-002.

### 7.2 Migraciones

- `Context/estilo-documentacion.md` → `docs/equipo/estilo-documentacion.md`
  (referencia completa; `rules/docs.md` es su condensado).
- `docs/onboarding.md` → `docs/equipo/onboarding.md`, actualizado: la sección
  2 menciona los guards, el status de sesión y qué aceptar en el primer
  arranque; la sección 3 añade el manual a la lectura obligatoria.
- `Context/README.md` (fuera del repo) queda en cinco líneas: el manual vive en
  `Libox/docs/equipo/`; Cowork sigue usando Cowork station y Output.
- `docs/README.md` gana la fila `equipo/`; `scripts/outline-map.json` gana las
  entradas de `docs/equipo/` para el espejo en la capa Desarrollo de Outline.

### 7.3 Memoria

| Capa | Qué guarda | Autoridad |
|---|---|---|
| `docs/` (repo) | Hechos y decisiones del proyecto | Canónica |
| `.claude/rules/` | Reglas operativas por zona | Canónica |
| Auto-memory personal | Preferencias de trabajo del individuo | Personal; nunca hechos del proyecto |
| claude-mem, GSD | — | Retirados (Z.8) |

`MEMORY.md` personal de Diego se reescribe para apuntar a `docs/equipo/`; la
entrada de orquestación se conserva como preferencia.

### 7.4 Higiene aprobada

| Ítem | Acción |
|---|---|
| 33 agentes `gsd-*.md` en `~/.claude/agents/` | Borrar (máquina de Diego; retirados por Z.8, se inyectan en cada sesión). |
| `claude-mem@thedotmack`, `vercel-plugin@vercel` | Desactivar a nivel proyecto en `settings.json` (5.6). |
| `.claude/worktrees/mvp1-dev-phases` | Borrar (huérfano: `git worktree list` solo ve `main`; gitignorado). |
| `.claude/settings.local.json` | Podar permisos muertos; el diff se muestra a Diego antes de aplicar. |
| `.agents/skills/outline-skills` | **No se toca** (no autorizado). |

## 8. Entrega y verificación

- Rama `chore/sistema-operativo-ia` desde `main`; **un PR** con commits
  atómicos por capa: rules → hooks + tests → skills → agentes → settings →
  docs → higiene. Rebase-and-merge los preserva.
- Orden respecto al PR #16 (rate limiting): **el OS entra primero**; #16 se
  rebasa después y resuelve los conflictos en `CLAUDE.md` / `src/CLAUDE.md`.
- Verificación antes de declarar listo: `unittest` verde ·
  `verify_corpus.py` a cero · `markdownlint` (workflow `docs.yml`) verde ·
  prueba manual en una sesión nueva: commit con trailer, push a `main`,
  edición de un doc `_V`, escritura en `src/` → los cuatro bloqueados;
  escritura en `docs/equipo/` → pasa.
- Post-merge: `libox-outline-sync` publica `docs/equipo/` en Outline.

## 9. Fuera de alcance

- Agentes y skills de desarrollo (dependen de ASS-002).
- Automatizaciones sobre la capa de negocio de Outline (actas, digests,
  registro de decisiones) más allá de `libox-registrar-hallazgo`.
- Empaquetar la capa como plugin instalable (enfoque B): se reconsidera si
  aparece un segundo repo en la org.
