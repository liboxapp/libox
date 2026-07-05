---
title: Índice de decisiones (ADRs)
status: vivo
tags: [libox, decisiones, indice]
updated: 2026-06-05
---

# Decisiones (ADRs)

Esta carpeta guarda las decisiones cerradas del proyecto Libox, cada una en su propio archivo, en formato **ADR (Architecture Decision Record)**.

## Propósito

- **Compartibilidad**: cada ADR es autocontenido y puede compartirse con socios, inversionistas, abogado o nuevos miembros del equipo sin necesidad de leer el plan completo.
- **Trazabilidad**: el _por qué_ de una decisión queda registrado en el momento en que se tomó, con las alternativas que se evaluaron y las restricciones vigentes.
- **No-divergencia**: cada ADR aclara cuál es su versión canónica (este archivo, o el Anexo Z correspondiente en [`../plans/libox-plan.md`](../plans/libox-plan.md)).

## Convención de nombres

`<código>-<slug-en-español>.md` — el código sigue la numeración del Anexo Z del plan (Z.1, Z.2, etc.). Si una decisión es lo bastante grande para justificar varias páginas, se usa el mismo código.

## Índice de decisiones

| Código | Decisión | Estado | Fecha |
|---|---|---|---|
| [Z.1](Z1-custodia-del-dinero.md) | Custodia del dinero — Modelo C (escrow conceptual) | Cerrada en dirección; pendiente ratificación legal | 2026-06-05 |
| [Z.2](Z2-eleccion-psp.md) | Elección de PSP — Mercado Pago primario, split en la fuente, Culqi 2º rail | Cerrada en dirección; pendiente verificación comercial | 2026-06-05 |
| [Z.3](Z3-tipo-de-organizador.md) | Tipo de organizador — cualquiera con RUC (natural o jurídica) | Cerrada; pendiente validación legal de autorización municipal | 2026-06-05 |
| [Z.4](Z4-tipos-de-sorteo.md) | Tipos de sorteo MVP-1 — motor configurable 1 ganador (T1–T4 presets) | Cerrada | 2026-06-05 |
| [Z.5](Z5-t8-live.md) | T8 LIVE — diferido a MVP-3 | Cerrada | 2026-06-05 |
| [Z.6](Z6-stack-tecnologico.md) | Stack tecnológico — Next.js para todo (descarta Astro); Drizzle + Supabase (Auth y DB host) cerrados con [benchmark](../benchmark-stack.md) | Cerrada en dirección; job runner al scaffold | 2026-07-05 |
| [Z.7](Z7-versionamiento.md) | Versionamiento — semver + Conventional Commits + release-please | Cerrada | 2026-06-06 |
| [Z.8](Z8-roles-memoria-contexto.md) | Roles de memoria y contexto — docs/MEMORY = verdad; context-mode/claude-mem/GSD encarrilados | Cerrada | 2026-06-06 |

## Cómo agregar una nueva decisión

1. Confirmar con Diego que la decisión está lista para cerrarse.
2. Crear archivo nuevo con el formato `Z<n>-<slug>.md`.
3. Estructura sugerida: **Decisión** · **Alternativas evaluadas** · **Por qué se descartó cada una** · **Implicaciones que el equipo debe aceptar** · **Impacto sobre el PRD** · **Validaciones externas pendientes** · **Preguntas para socios**.
4. Mirror corto en el Anexo Z del [plan](../plans/libox-plan.md), apuntando al ADR como canónico.
5. Actualizar este índice.
