---
title: C1 — decisiones de firmas y aprobadores
status: aprobado
tags: [r0, c1, l3-v8, decisiones, rbac]
updated: 2026-09-30
description: Segunda firma por acción, cofirma V2, observación de valoraciones y aprobadores por etapa P-C (A1–A4).
---

# Firmas y aprobadores

Parte del [paquete de decisiones de C1](decisiones-c1.md). Decidido por Diego el 2026-09-30.

Fuente de roles: [L3 V7 §7.1–7.2](../../../linea-base/LIBOX_ESPECIFICACION_TECNICA_L3_V7.md).
Detalle de los conflictos I-xx: [cierre contractual](cierre-contratos.md#hallazgos-del-canon-cd-07).

## A1. Quién firma en segundo lugar (I-04)

**Conflicto.** §7.1 da "Segunda firma" solo a `ADMIN_SUPER`. INC-09 exige que la
segunda firma sea de otra persona **y otro subrol**. Si quien solicita es
`ADMIN_SUPER`, ambas reglas no pueden cumplirse a la vez. El contrato hoy falla
cerrado: sin política, ninguna solicitud es firmable.

- **(a)** Aplicar §7.1 literal: siempre firma `ADMIN_SUPER`. INC-09 se relaja a
  "otra persona".
- **(b)** Aplicar INC-09 literal: siempre otra persona y otro subrol. Las acciones
  que solo puede iniciar `ADMIN_SUPER` quedan sin firmante posible.
- **(c)** Política por `action_code` como dato: otra persona siempre; otro subrol
  salvo cuando la acción es propia de `ADMIN_SUPER`, en cuyo caso firma otro
  `ADMIN_SUPER`. Es coherente con INV-38, que existe para que siempre haya dos.

**Recomendación: (c)**, con esta tabla inicial para los 11 códigos del contrato:

| `action_code` | Solicita normalmente | Firmantes elegibles (propuesta) |
|---|---|---|
| `VALUATION_V2_COSIGN` | `SUPPORT_VALUATOR` | `ADMIN_MODERATION` (ver A2) |
| `VALUATION_V4` | `SUPPORT_VALUATOR` | `ADMIN_LEGAL_COMPLIANCE` |
| `VALUATION_EXCEPTION` | `SUPPORT_VALUATOR` o `ADMIN_LEGAL_COMPLIANCE` | El otro de los dos; `ADMIN_SUPER` |
| `PC_STAGE_E3` | `ADMIN_LEGAL_COMPLIANCE` | `ADMIN_SUPER` |
| `PC_STAGE_E7` | `ADMIN_LEGAL_COMPLIANCE` | `ADMIN_SUPER` |
| `ATTEST_PC` | `ADMIN_LEGAL_COMPLIANCE` | `ADMIN_SUPER` |
| `CAPABILITY_PLATFORM_DISABLE` | `ADMIN_SUPER` | Otro `ADMIN_SUPER` |
| `MARKET_RESUME` | `ADMIN_SUPER` | Otro `ADMIN_SUPER` |
| `MULTIPLE_OVERRIDE` | `ADMIN_COMPLIANCE` | `ADMIN_SUPER` |
| `SUBROLE_GRANT` | `ADMIN_SUPER` | Otro `ADMIN_SUPER` |
| `MFA_RESET_INTERNAL` | `ADMIN_SUPER` | Otro `ADMIN_SUPER` |

INC-11 se mantiene: nadie firma su propia acción. `MULTIPLE_OVERRIDE` toca el rango
de recaudación: aquí solo se decide el firmante, no la regla del múltiplo.

**Desbloquea:** firma de las 11 solicitudes y el apagado global de capacidad.
**Decisión:** **(c)**, política por acción con la tabla inicial. Diego, 2026-09-30.

**Operación pendiente:** actualmente solo Diego está incorporado. Las acciones
con segunda firma no pueden operar con una única persona ni con dos cuentas
de esa persona. Resolver la incorporación y el bootstrap antes de habilitarlas;
la suspensión de revisión humana del desarrollo no modifica esta regla.

## A2. Cofirma de la banda V2 por `ADMIN_MODERATION` (I-01)

**Conflicto.** La banda V2 exige cofirma de `ADMIN_MODERATION`, pero §7.1 le da
solo `R` en "Valoración de premio".

- **(a)** Añadir en la matriz V8 una fila "Cofirma de valoración V2" con `A` para
  `ADMIN_MODERATION`. Cofirmar no le da escritura sobre la valoración.
- **(b)** Mover la cofirma a `ADMIN_LEGAL_COMPLIANCE`, que ya tiene `A`.

**Recomendación: (a).** Conserva la separación que buscaba la regla: quien modera
el sorteo no es quien valora. Ya está modelado así en el contrato.
**Decisión:** **(a)**, `ADMIN_MODERATION` cofirma. Diego, 2026-09-30.

## A3. Actor de `VALUATION_OBSERVED` (I-03)

**Conflicto.** El canon asigna la observación a un "Verificador", que no es un subrol.

- **(a)** Limitarla a quienes aprueban la banda: `SUPPORT_VALUATOR` y
  `ADMIN_LEGAL_COMPLIANCE`.
- **(b)** Crear el subrol `SUPPORT_VERIFIER`.

**Recomendación: (a).** Es lo que ya aplica el contrato y evita un subrol nuevo con
su fila de matriz e incompatibilidades.
**Decisión:** **(a)**, quienes aprueban la banda. Diego, 2026-09-30.

## A4. Quién decide cada etapa P-C (I-02)

**Conflicto.** El PRD V9 asigna actores distintos por etapa. §7.1 tiene una sola
fila "Etapas P-C" con `A` solo para `ADMIN_LEGAL_COMPLIANCE`.

| Etapa | Aprueba según PRD V9 | Firma (A1) |
|---|---|---|
| E1 Elegibilidad | `ADMIN_RISK` | — |
| E2 Titularidad | `ADMIN_LEGAL_COMPLIANCE` | — |
| E3 Valoración | `ADMIN_LEGAL_COMPLIANCE` | `PC_STAGE_E3` |
| E4 Instrumento y bloqueo | `ADMIN_LEGAL_COMPLIANCE` | — |
| E5 Publicación y venta | Sin aprobador (automática) | — |
| E6 Preparación del ganador | `SUPPORT_L2` verifica; `ADMIN_LEGAL_COMPLIANCE` habilita | — |
| E7 Transferencia | `ADMIN_LEGAL_COMPLIANCE` | `PC_STAGE_E7` |

- **(a)** Partir la fila de §7.1 en una matriz por etapa igual a la tabla de arriba.
  E6 en dos pasos: verificación y habilitación.
- **(b)** Todo a `ADMIN_LEGAL_COMPLIANCE`, con `ADMIN_RISK` y `SUPPORT_L2` como
  asesores sin decisión.

**Recomendación: (a).** Respeta el PRD, que es la fuente de producto, y mantiene
la elegibilidad (reputación, KYB) en el rol de riesgo. [LEGAL→ABOGADO] para E2, E4
y E7.
**Desbloquea:** operaciones de decisión de etapa, junto con A8.
**Decisión:** **(a)**, matriz por etapa según el PRD. Diego, 2026-09-30; [LEGAL→ABOGADO] en E2, E4 y E7.
