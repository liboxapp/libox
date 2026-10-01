---
title: C1 — decisiones de configuración y sorteo
status: aprobado
tags: [r0, c1, l3-v8, decisiones, configuracion]
updated: 2026-09-30
description: Expiración de T1, duración de T7, entrada de precio, régimen, costos, baliza drand y datos que no se proponen (C1–C4, D1, E).
---

# Configuración por tipo y sorteo

Parte del [paquete de decisiones de C1](decisiones-c1.md). Decidido por Diego el 2026-09-30.

## C. Configuración por tipo de sorteo

Fuente: [lecturas y configuración](cierre-contratos-lecturas-configuracion.md#configuración-por-tipo-de-sorteo-solo-diseño).
El diseño de `RaffleConfiguration` ya existe. Falta decidir:

### C1. Política de expiración de T1 (I-09)

**Conflicto.** `raffle_type_rules` de T1 exige `expiry_policy_required`, pero no
hay campo que la guarde.

- **(a)** Campo `expiry_policy` con `max_duration_days` y la acción al vencer. La
  acción es un enum que habrá que elegir entre cancelar con reembolso o pasar a la
  ruta declarada.
- **(b)** T1 sin expiración: retirar la bandera de V8.

**Recomendación: (a).** Un sold-out sin plazo puede dejar dinero de compradores
inmovilizado indefinidamente. El reembolso lo ejecuta el código patrimonial humano;
aquí solo se decide el campo.
**Decisión:** **(a)**, con plazo máximo. Al vencer **se sortea con lo vendido si se alcanzó un mínimo vendido; si no, se cancela con reembolso**. Ver la nota de C1 abajo. Diego, 2026-09-30.

**Nota de C1.** Sortear un T1 sin venderlo completo cambia lo que esperaba quien
compró en un sold-out y toca el rango de recaudación, que es zona crítica. Queda
por definir, como dueño humano:

- el mínimo vendido (porcentaje o número de boletos) y si lo fija la plataforma o
  el organizador dentro de unos límites;
- si el premio se entrega completo cuando se alcanza el mínimo;
- cómo se informa al comprador antes de pagar.

[LEGAL→ABOGADO]: protección al consumidor y reglas de sorteos promocionales.

### C2. Duración de cada edición en T7

- **(a)** Cada edición dura el intervalo de la recurrencia y `end_at` se calcula al
  crearla.
- **(b)** Duración explícita por edición, independiente del intervalo.

**Recomendación: (a).** Evita solapamientos entre ediciones y un campo más que
validar.
**Decisión:** **(b)**, duración propia, **sin solape**: la duración no supera el intervalo. Diego, 2026-09-30.

### C3. Entrada de precio

**Conflicto.** Puede fijarla el organizador como `ticket_price` o como neto
objetivo, a partir del cual se calcula el precio. Es solo la decisión de producto:
el cálculo de comisión e impuesto es zona crítica.

- **(a)** El organizador fija `ticket_price`; se le muestra el neto estimado.
- **(b)** El organizador fija el neto; el sistema deriva `ticket_price`.

**Recomendación: (a).** El precio que ve el comprador es estable y el contrato no
depende de la fórmula de comisión.
**Decisión:** **(a)**, el organizador fija `ticket_price`. Diego, 2026-09-30 (con visto del dueño contable)

### C4. Régimen económico (S-1) y enums de costos

- **Régimen.** Recomendación: solo `PAID` en el MVP. `FREE_ENTRY` y `PROMOTIONAL`
  necesitan diseñar la garantía sustitutiva (INV-06-b, INV-44). **Decisión:** solo `PAID` en el MVP. Diego, 2026-09-30.
- **`cost_kind`, `charge_kind`, `macrozone`.** Sustituyen el JSONB de V7. No se
  proponen valores: pedir la lista a Diego a partir de los costos reales que ya
  asume (envío, notaría, registro). **Lista:** `cost_kind` inicial: `SHIPPING`, `NOTARY`, `REGISTRY`; se amplía en V8. `charge_kind` y `macrozone` pendientes de Diego.

## D. Sorteo

### D1. Fuente de aleatoriedad pública

La [propuesta de baliza](baliza-propuesta.md) sugiere evaluar **drand quicknet**.

- **(a)** Ratificar drand quicknet como fuente para que Diego fije la codificación
  y calcule los resultados esperados de los 5 vectores (H-10).
- **(b)** Evaluar otra fuente antes.

**Recomendación: (a)**, si la evaluación de la propuesta no deja dudas abiertas.
Los vectores, `verify_draw` y `server_seed` siguen siendo implementación humana
independiente.
**Decisión:** **(a)**, drand quicknet ratificado como fuente. Diego, 2026-09-30.

## E. Datos que no se proponen

Estos valores no se infieren ni se proponen aquí. Deben venir de su dueño:

| Dato | Dueño | Bloquea |
|---|---|---|
| `fee_schedules`, `client_fee_levels` y valores financieros de `market_config_versions` | Diego y dueño contable | Configuración financiera (pendiente SQL #8) |
| Confirmación contable de H-01 a H-03 (`ledger_accounts`, inmutabilidad, privilegios de asiento) | Dueño contable | H-04 y el ledger |
| Política de pago tardío (H-16) | Diego | Pendiente SQL #10 |
| Secciones tributarias del documento de mercado | [LEGAL→ABOGADO] | `POST /markets/{code}/config` versionado |
| Custodia del dinero (ASS-001) | Diego | Dinero real |
