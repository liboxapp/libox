---
title: Z.5 — T8 LIVE
status: cerrada
tags: [sortibox, decision, sorteo, live, roadmap, mvp]
decided: 2026-06-05
relates: [docs/decisions/Z4-tipos-de-sorteo.md, docs/glosario.md, docs/plans/sortibox-plan.md]
updated: 2026-06-05
---

# Z.5 — T8 LIVE

**Estado**: Cerrada (2026-06-05).
**Decisor**: Diego.
**Documento canónico**: este archivo. Mirror en [`docs/plans/sortibox-plan.md`](../plans/sortibox-plan.md#z5--t8-live-cerrada-el-2026-06-05) (Anexo Z.5).
**Relacionada**: continúa el eje "modo" de [Z.4](Z4-tipos-de-sorteo.md).

---

## Decisión

**T8 LIVE se difiere a MVP-3.** En MVP-1 y MVP-2 el sorteo se ejecuta únicamente en modo **AUTO** (sistema) y **Admin**. El modo **LIVE** (organizador ejecuta en vivo) entra en MVP-3.

---

## Qué agrega LIVE (y qué no)

LIVE es la tercera posición del eje "modo" identificado en [Z.4](Z4-tipos-de-sorteo.md). Permite que el **organizador ejecute el sorteo en vivo** (streaming), **solo con autorización previa de Admin**.

Lo que **no** cambia: el algoritmo de fairness. `canonical_pool → pool_hash → external_entropy → seed_material → random_value → winner_index` es **idéntico** al modo AUTO. El ganador es igual de reproducible y verificable.

Lo que **sí** agrega:
- **Streaming / tiempo real**: transmitir la ejecución en vivo.
- **Flujo de autorización**: `LIVE_AUTHORIZED` (Admin habilita), `LIVE_TRIGGER_REJECTED` (intento sin permiso → rechazo auditado).
- **Controles anti-manipulación percibida**: que el público confíe en que el host no "arregló" el resultado.

---

## Por qué diferir

- **No es core-loop.** El bucle esencial es comprar → sortear → entregar → liquidar. LIVE es un **diferenciador de crecimiento**, no una pieza del bucle. El core debe estar sólido antes.
- **Suma infraestructura de tiempo real** y superficie de soporte (latencia, caídas durante una transmisión en vivo) que no conviene cargar en un MVP que todavía valida mercado.
- **Riesgo de manipulación percibida**: un host en vivo "podría" parecer que manipula el sorteo. Se mitiga con el proof reproducible, pero exige comunicación y UX cuidadas que no son prioridad temprana.

## Por qué MVP-3 y no MVP-2

LIVE solo tiene sentido **sobre un ciclo económico ya cerrado**: Delivery + Settlement + disputa se construyen en **MVP-2**. Recién con esa base operando vale la pena sumar la capa LIVE encima. Por eso entra en **MVP-3** (capa de APIs enterprise + observabilidad + features de crecimiento), no antes.

---

## Implicación de build

El motor de [Z.4](Z4-tipos-de-sorteo.md) ya modela `mode ∈ {AUTO, ADMIN}`. **LIVE es un tercer valor del mismo enum** que reutiliza el algoritmo existente. Sumarlo en MVP-3 es **additivo** (flujo de autorización + capa realtime + UX), no una reescritura. Conservar el campo `mode` desde MVP-1 evita refactor cuando llegue LIVE.

---

## Impacto sobre el PRD ALAZAR v11

El PRD presenta T8 LIVE como un diferenciador relevante y dedica sección a su anti-manipulación. La decisión **no lo descarta**: lo **secuencia** en el roadmap (MVP-3), respetando la regla del PRD de "expandir sin destruir". El diseño del PRD (mismo algoritmo para AUTO y LIVE) es justamente lo que hace barato diferirlo.

---

## Preguntas para discutir con socios

1. ¿LIVE es parte del **pitch a inversionistas** como diferenciador, aunque se construya en MVP-3? (Conviene alinear narrativa vs roadmap.)
2. ¿Algún organizador ancla temprano **exige** LIVE y justificaría adelantarlo? Si aparece, se reabre esta decisión.
3. ¿La capa de streaming se construye in-house o se apoya en un tercero (ej. integración con una plataforma de video)? — definición para cuando llegue MVP-3.
