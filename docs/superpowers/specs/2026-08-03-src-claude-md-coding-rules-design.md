---
title: "Spec — src/CLAUDE.md: reglas de código para la app Libox"
status: aprobada-en-diseño
tags: [spec, claude, engineering]
updated: 2026-08-03
---

# Spec — `src/CLAUDE.md`: reglas de código

## Objetivo

Adaptar a Libox el CLAUDE.md de reglas de código que funcionó en el proyecto
keikogobierna, sin duplicar lo que ya es canónico aquí
([`CONTRIBUTING.md`](../../../CONTRIBUTING.md), ADR
[Z.6](../../decisions/Z6-stack-tecnologico.md), CLAUDE.md raíz), y codificando
el flujo **Superpowers SDD** (spec → plan → ejecución verificada) como método
de trabajo para todo el código de la app.

## Decisiones de diseño

1. **Ubicación: `src/CLAUDE.md`** (el archivo vacío existente se llena). Se
   carga solo al trabajar dentro de `src/`; el CLAUDE.md raíz sigue siendo la
   guía del wiki y manda en naming, idioma de conversación y decisiones.
2. **Idioma del archivo: inglés**, igual que el CLAUDE.md raíz (instrucciones
   para Claude, no wiki para socios).
3. **Política de idiomas del código**: identificadores, comentarios y nombres
   de archivo en **inglés**; todo string user-facing en **español (Perú)**;
   conversación, wiki y commits en **español**. Regla de desempate: si dudas
   si un string es user-facing, lo es → español.
4. **No se duplica lo canónico**: reglas de ingeniería duras y git flow se
   resumen con puntero a `CONTRIBUTING.md`; stack con puntero a Z.6.
5. **Plugins Anthropic en dos tandas** (análisis del marketplace oficial,
   278 plugins, 39 de Anthropic):
   - **Tanda 1 (ahora, en `.claude/settings.json` versionado)**: `hookify`
     (enforcement mecánico de reglas duras: sin co-author trailers, sin
     commits directos a `main`) y `claude-md-management` (mantenimiento de
     los CLAUDE.md).
   - **Tanda 2 (checklist de scaffold, primer PR de código)**:
     `security-guidance`, `claude-security`, `typescript-lsp`,
     `pr-review-toolkit`.
   - **Descartados por redundancia**: `feature-dev` (compite con superpowers
     SDD), `code-review` (existe `/code-review` integrado), `code-simplifier`
     (existe `/simplify`), `commit-commands` (chocaría con la regla de
     no-trailers), `claude-code-setup` (uso único, no permanente).

## Estructura de `src/CLAUDE.md`

1. **What this is** — reglas de código de la app (Next.js modular monolith);
   jerarquía respecto al CLAUDE.md raíz.
2. **Commands** — declarada *pending scaffold*: no hay `package.json`;
   prohibido inventar comandos; se llena en el primer PR de código.
3. **Language policy** — según decisión 3.
4. **Superpowers SDD** (núcleo) — brainstorming antes de todo trabajo
   creativo; specs aprobadas en `docs/superpowers/specs/`; `writing-plans` →
   ejecución (`subagent-driven-development` o `executing-plans`); TDD para
   toda feature/fix; `systematic-debugging` ante bugs;
   `verification-before-completion` antes de declarar terminado;
   `requesting-code-review` antes de mergear.
5. **Model orchestration (Fable → Opus)** — Fable orquesta, Opus implementa
   vía subagentes; briefs autocontenidos con las restricciones de este
   archivo + reglas de ingeniería; gate de revisión sobre el output de
   workers; ignorar si la sesión ya corre en Opus o menor.
6. **Hard engineering rules** — resumen de las 3 reglas (dinero solo vía
   transacción Drizzle server-side; webhooks ACK < 2 s + Inngest async;
   concurrencia resuelta en la DB) + puntero a `CONTRIBUTING.md` y a su
   checklist de scaffold.
7. **Stack (closed — Z.6)** — tabla mínima + regla: ninguna dependencia
   fuera del stack sin ADR.
8. **WAT architecture** — acotada a scripts operativos/de datos (`scripts/`,
   SOPs en `workflows/` cuando existan); la app la estructuran los bounded
   contexts de Z.6; se conserva el self-improvement loop.
9. **Frontend design** — invocar `frontend-design` antes de cualquier código
   frontend; guardrails anti-genérico (adaptados a Tailwind v4 + shadcn/ui);
   verificación por screenshot desde localhost, ≥2 rondas; assets reales
   antes que placeholders.
10. **Git workflow** — puntero a `CONTRIBUTING.md` + lo operativo: ramas
    `<type>/<kebab>`, rebase-and-merge único método, `--force-with-lease`,
    jamás co-author trailers.
11. **Plugin plan** — tanda 2 documentada como parte del checklist de
    scaffold; lista de descartados con motivo para no re-litigar.

## Descartes del original (keikogobierna)

Comandos Astro y validadores Python propios de ese repo, reglas de datos de
`tracking.json`, referencia a su ruleset `protect-main` (aquí ya documentado
en `CONTRIBUTING.md`).

## Implementación

| Archivo | Cambio |
|---|---|
| `src/CLAUDE.md` | Escribir el contenido según la estructura anterior. |
| `.claude/settings.json` | Añadir `hookify@claude-plugins-official` y `claude-md-management@claude-plugins-official` a `enabledPlugins`. |

## Criterios de aceptación

- `src/CLAUDE.md` no repite texto normativo de `CONTRIBUTING.md`/Z.6: resume
  y enlaza.
- Ninguna instrucción contradice al CLAUDE.md raíz (naming Libox, español en
  conversación, sin co-author trailers).
- La sección Commands no contiene comandos inventados.
- `markdownlint` y `links` (CI `docs`) pasan sobre la spec.
