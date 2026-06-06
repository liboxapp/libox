---
title: Z.4 — Tipos de sorteo en MVP-1
status: cerrada
tags: [sortibox, decision, sorteo, draw-engine, mvp]
decided: 2026-06-05
relates: [docs/decisions/Z1-custodia-del-dinero.md, docs/glosario.md, docs/plans/sortibox-plan.md]
updated: 2026-06-05
---

# Z.4 — Tipos de sorteo en MVP-1

**Estado**: Cerrada (2026-06-05).
**Decisor**: Diego.
**Documento canónico**: este archivo. Mirror en [`docs/plans/sortibox-plan.md`](../plans/sortibox-plan.md#z4--tipos-de-sorteo-en-mvp-1-cerrada-el-2026-06-05) (Anexo Z.4).
**Glosario**: la definición de T1–T8 y de los términos de fairness está en [glosario.md](../glosario.md).
**Relacionada**: T8 (LIVE) se decide aparte en [Z.5](Z5-t8-live.md).

---

## Decisión

El MVP-1 construye **un único motor de sorteo configurable**, con:

- **1 ganador** (single-winner).
- Modo **AUTO + Admin** (sin LIVE).
- Dos disparadores **combinables**: **umbral opcional** (`trigger_threshold`) + **fecha opcional** (`trigger_deadline`).
- **Ruta de fallo-y-refund**: si no se cumple la condición, el sorteo pasa a `FAILED` y se reembolsa a todos.

Esto entrega **T1, T2, T3 y T4 como presets** del mismo motor.

**Se difiere**: T5 (UX flash), T6 (multi-ganador), T7 (progresivo), T8 (LIVE → [Z.5](Z5-t8-live.md)).

---

## El reframe: los tipos no son motores, son presets

El error de plantear "¿cuántos de los 8 tipos construimos?" es asumir que son 8 piezas de trabajo separadas. **No lo son.** El propio PRD dice que los tipos son "configuraciones ejecutables" de un `draw_config` versionado.

Los 8 tipos se descomponen en **3 ejes ortogonales**:

| Eje | Posiciones | Tipos que genera |
|---|---|---|
| **Disparo** (¿cuándo se sortea?) | sold-out / umbral / fecha / umbral-o-fecha / ventana corta / milestones | T1 / T2 / T3 / T4 / T5 / T7 |
| **N° de ganadores** | 1 / N | T1–T5,T8 / T6,T7,T8 |
| **Modo** (¿quién ejecuta?) | AUTO / Admin / LIVE | — / — / T8 |

Consecuencias:

- **T1, T2, T3, T4** son **el mismo motor** con el eje "disparo" en distintas posiciones (todos 1 ganador, modo automático). Un motor que acepte "umbral opcional + fecha opcional" los produce a los cuatro como presets — **menos código, más cobertura**.
- **T5 (Flash)** es T3 con fecha cercana: el mecanismo es gratis; lo que cuesta es la UX de urgencia (cuenta regresiva). Se difiere solo la UX.
- **T6 (Multi-ganador)** es girar el eje 2 a "N": trabajo real (selección sin repetición, ranking, N premios, proof extendido).
- **T7 (Progresivo)** es lo más complejo: fases, sorteos parciales, máquina de estados de milestones.
- **T8 (LIVE)** es girar el eje 3: mismo algoritmo, pero suma streaming, autorización y UX en tiempo real → se decide en [Z.5](Z5-t8-live.md).

Por eso la pregunta correcta fue **"¿qué posiciones de cada eje soporta el MVP-1?"**, no "¿cuántos tipos?".

---

## El acople invisible: la ruta de refund

Permitir umbral o fecha obliga a responder **qué pasa si el sorteo no se completa** (no llega al umbral antes de la fecha). La respuesta sana: el sorteo **falla y se devuelve a todos**.

Bajo el [Modelo C](Z1-custodia-del-dinero.md), los refunds los ejecuta el organizador/PSP, no Sortibox. Por lo tanto, construir umbral/fecha **arrastra construir la ruta de fallo-y-refund**, que toca el módulo de pagos.

Alternativas que la evitarían, y por qué no convencen:

| Preset puro | Evita refund | Pero arriesga |
|---|---|---|
| T1 solo sold-out | Sí | **Deadlock**: el sorteo se cuelga si nunca se vende el 100%. |
| T3 solo fecha, sin mínimo | Sí | **Pool diminuto**: sortear con 2 boletos vendidos. |

Un MVP creíble necesita umbral + fecha + refund: ningún organizador real acepta "vende todo o se cuelga", ni ningún participante acepta "sortearon con 3 boletos".

---

## Inputs de Diego (2026-06-05)

- **Disparo**: motor configurable **umbral + fecha + refund** (no un preset suelto).
- **Ganadores**: **solo 1** en MVP-1.

---

## Implicaciones de build

- **`draw_config`** (MVP-1): `trigger_threshold` (nullable), `trigger_deadline` (nullable), `winners = 1` (fijo), `mode ∈ {AUTO, ADMIN}`. El motor deriva de esos campos los estados "elegible para sortear" y "fallido".
- **Estado `FAILED` + refund**: el sorteo que no cumple condición pasa a `FAILED` y dispara refund vía PSP a todos los participantes. **Dependencia explícita del módulo de pagos** — el motor de sorteo y el de pagos se cruzan acá.
- **Proof single-winner**: el draw proof cubre 1 ganador. Diseñar la selección para que pasar a N ganadores (T6) sea **agregar iteración sin repetición**, no reescribir.
- **T5 gratis**: una fecha cercana ya es un "flash" a nivel mecánico; solo se difiere la UX.
- El algoritmo de fairness (`pool_hash → external_entropy → seed_material → random_value → winner_index`) es **idéntico para todos los tipos**; no cambia entre presets ni modos.

---

## Impacto sobre el PRD ALAZAR v11

Se respeta el diseño del PRD ("tipos = `draw_config` versionado consumido por el Draw Engine"). MVP-1 implementa el subconjunto **{T1–T4, 1 ganador, AUTO/Admin}**. T5/T6/T7/T8 quedan como **configuraciones futuras del mismo motor**, no como reescrituras. Esto mantiene la coherencia con la regla del PRD de "expandir sin destruir".

---

## Preguntas para discutir con socios

1. ¿La **ruta de refund** (sorteo fallido → devolver a todos) es aceptable operativamente bajo Modelo C en MVP-1, sabiendo que depende del PSP para ejecutar las devoluciones?
2. ¿Hay algún caso de negocio temprano que **exija multi-ganador (T6)** y obligue a adelantarlo? (Ej. sorteos con varios premios.)
3. ¿La **UX de "flash" (T5)** aporta diferenciación temprana suficiente para adelantarla, o espera?
4. Política de refund: si el sorteo falla, ¿se devuelve el 100% al participante incluyendo lo que habría sido comisión de Sortibox, o Sortibox retiene algo? (Tiene implicación contable en el ledger.)
