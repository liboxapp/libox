---
title: Z.8 — Roles de memoria y contexto
status: cerrada
tags: [libox, decision, tooling, memoria, contexto, plugins]
decided: 2026-06-06
relates: [docs/plans/libox-plan.md]
updated: 2026-06-06
---

# Z.8 — Roles de memoria y contexto

**Estado**: Cerrada (2026-06-06).
**Decisor**: Diego.
**Documento canónico**: este archivo. Mirror en [`docs/plans/libox-plan.md`](../plans/libox-plan.md) (Anexo Z.8). Versión operativa en [`CLAUDE.md`](../../CLAUDE.md).

---

## Contexto

Tras instalar plugins de Claude Code (skill-creator, superpowers, context-mode, claude-mem, frontend-design, get-shit-done), quedaron **varios mecanismos de memoria/contexto corriendo en paralelo** en las sesiones de Libox. Sin roles definidos, compiten, duplican trabajo y pueden generar divergencia sobre "cuál es la verdad" del proyecto.

Mecanismos activos detectados:
- **`MEMORY.md` + `docs/`** — memoria curada del proyecto (auto-memoria + wiki versionado).
- **`context-mode`** — hook `SessionStart` + inyección de guía; indexa outputs en su base FTS5.
- **`claude-mem`** — captura cross-sesión vía su MCP + runtime del plugin (sin hooks en `settings.json`).
- **`get-shit-done` (GSD)** — framework de workflow con guard/monitor hooks (PreToolUse/PostToolUse/SessionStart). No es memoria, pero añade comportamiento automático que conviene encuadrar.

## Decisión

Se asignan **carriles (roles) explícitos** para que cada herramienta haga una sola cosa y no se pisen:

| Herramienta | Rol asignado | Es la verdad del proyecto |
|---|---|---|
| **`docs/` + `MEMORY.md`** | **Fuente curada y compartible**: decisiones (Z.1–Z.8), plan, glosario, compliance. Versionada en git, shareable con socios/abogado. | **Sí — autoritativa.** |
| **`context-mode`** | **Procesar outputs grandes** sin gastar ventana de contexto (logs, builds, archivos grandes, data, fetch de docs). Ayuda de cómputo. | No — es caché/herramienta. |
| **`claude-mem`** | **Captura cross-sesión general**, secundaria. Útil para "¿ya resolvimos esto antes?" entre sesiones. | No — secundaria; se reconcilia contra `docs/`. |
| **`get-shit-done` (GSD)** | **Framework de workflow** (planificación/ejecución), no memoria. Se usa si aporta a una fase concreta; no es fuente de verdad. | No. |

## Reglas de oro

1. **La verdad de Libox vive en `docs/` + `MEMORY.md`**, nunca solo en `claude-mem` o `context-mode`. Esos son aceleradores, no el registro.
2. Toda **decisión cerrada** se documenta como ADR en `docs/decisions/` + mirror en el Anexo Z (flujo de siempre). No se delega ese registro a la captura automática.
3. Para **procesar outputs grandes** (cuando entre el código: builds, tests, logs), preferir las tools de `context-mode` para no inflar el contexto.
4. La **memoria auto-capturada no es autoritativa**: ante discrepancia, mandan los ADRs/plan.

## Implicaciones que aceptamos

- Hay redundancia consciente: tres mecanismos de memoria/contexto. Se tolera mientras cada uno aporte en su carril.
- `claude-mem` queda **a prueba**: si tras unas sesiones no aporta sobre lo que ya da `MEMORY.md`, se desactiva para reducir aparato.
- GSD añade hooks que interceptan herramientas; si generan fricción en el flujo de planificación de Libox, se revisa su configuración.

## Pendiente

- Reevaluar en 2-3 sesiones si `claude-mem` se queda o se desactiva.
- Si GSD se adopta como framework de ejecución del MVP, documentarlo como decisión aparte (cómo encaja con nuestro flujo de fases y ADRs).
