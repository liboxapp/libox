---
title: C1 — decisiones de capacidades, transiciones y roles
status: aprobado
tags: [r0, c1, l3-v8, decisiones, rbac]
updated: 2026-09-30
description: Capacidad LIVE, rechazos manuales, KYB, P-C en el MVP, atestación, reautenticación, motivos e incompatibilidades (A5–A11).
---

# Capacidades, transiciones y roles

Parte del [paquete de decisiones de C1](decisiones-c1.md). Decidido por Diego el 2026-09-30.

Fuente de roles: [L3 V7 §7.1–7.2](../../../linea-base/LIBOX_ESPECIFICACION_TECNICA_L3_V7.md).

## A5. Capacidad `LIVE` y categorías P-C (I-05)

**Conflicto.** `client_capabilities.capability` admite `T8` y `LIVE`. El PRD
define T8 como "Live": modo de presentación, no motor. Además, `P_C1` y `P_C2` no
son tipos de sorteo y no deben ir en `enabled_raffle_types`.

- **(a)** Retirar `LIVE`; `T8` es la única capacidad para sorteos en vivo. Mover
  `P_C1` y `P_C2` a un campo `enabled_categories`.
- **(b)** Conservar ambos: `T8` habilita el tipo y `LIVE` la transmisión.

**Recomendación: (a).** Hoy no hay caso que necesite habilitar uno sin el otro.
**Decisión:** **(a)**, se retira `LIVE` y las categorías P-C van en campo propio. Diego, 2026-09-30.

## A6. Transiciones de rechazo manual (I-06)

**Conflicto.** La FSM no tiene transición para rechazar manualmente una valoración
ni para observar o rechazar el gate legal. El contrato solo expone resultados con
transición.

Hoy la FSM del sorteo (§4.1) solo sale de `PENDING_VALUATION` hacia `REJECTED` por
`AUTO_REJECT_DEVIATION`, aunque `prize_valuations.outcome` ya admite `REJECTED`.
De `PENDING_LEGAL` solo sale `LEGAL_GATE_PASSED`.

- **(a)** Añadir en V8 tres transiciones con motivo obligatorio:
  - `PENDING_VALUATION → REJECTED` por `VALUATION_REJECTED`, con los mismos actores
    que la aprobación;
  - `PENDING_LEGAL → DRAFT` por `LEGAL_GATE_OBSERVED` (subsanable);
  - `PENDING_LEGAL → REJECTED` por `LEGAL_GATE_REJECTED` (terminal).
  Las dos últimas, con `ADMIN_LEGAL_COMPLIANCE`.
- **(b)** No añadir: los rechazos solo ocurren por las reglas automáticas.

**Recomendación: (a).** Sin rechazo manual, un caso dudoso queda indefinidamente
en revisión. Replica el patrón de `VALUATION_OBSERVED`, que ya vuelve a `DRAFT`.
El punto único de transición sigue siendo implementación humana (H-08).
[LEGAL→ABOGADO] para el gate legal.
**Decisión:** **(a)**, se añaden las tres transiciones. Diego, 2026-09-30; [LEGAL→ABOGADO] en el gate legal.

## A7. Quién decide KYB (I-07)

**Conflicto.** §7.1 no tiene fila para decidir KYB. El contrato no expone la
operación.

- **(a)** `ADMIN_COMPLIANCE` decide (`A`); `ADMIN_RISK` lee (`R`).
- **(b)** `ADMIN_RISK` decide, porque ya gestiona las capacidades del cliente.

**Recomendación: (a).** KYB es parte del expediente de cumplimiento, donde
`ADMIN_COMPLIANCE` ya tiene `A`, y separa quien verifica al cliente de quien le
habilita capacidades. El proveedor (Truora) sigue en evaluación.
**Decisión:** **(a)**, `ADMIN_COMPLIANCE` decide. Diego, 2026-09-30.

## A8. Lista cerrada de documentos por etapa P-C (I-08)

**Conflicto.** RN-29 exige `checklist_key` de lista cerrada por etapa, sin semilla.
**Bloquea todo P-C.**

- **(a)** Diego y el abogado entregan la lista por etapa (clave, descripción,
  obligatoria sí/no). Se integra como semilla y enum.
- **(b)** Posponer P-C del MVP y lanzar sin categorías P-C1/P-C2.

**Recomendación:** decidir primero si P-C entra en el MVP. Si entra, **(a)**: se
puede preparar una plantilla con las claves que ya menciona el PRD V9 §7 para que
el abogado la corrija, pero no inventar la lista. [LEGAL→ABOGADO].
**Decisión:** P-C **entra en el MVP**, con la lista del abogado (a). Se prepara la plantilla; P-C sigue bloqueado hasta recibirla. Diego, 2026-09-30.

## A9. Atestación sin `second_signer_id` (CC-08)

**Conflicto.** §11.5 define la atestación con `second_signer_id` en el cuerpo. El
resto de segundas firmas usa `SignatureRequest`.

- **(a)** Migrar a `SignatureRequest` con `ATTEST_PC`. Cambia un cuerpo del inventario.
- **(b)** Mantener `second_signer_id` en la atestación como excepción.

**Recomendación: (a).** Un solo mecanismo de firma, con INC-09 e INC-11 comprobados
en un único punto. El cambio va en V8 con su nota de migración del contrato.
**Decisión:** **(a)**, se unifica en `SignatureRequest`. Diego, 2026-09-30.

## A10. Ventana de reautenticación (S-3)

- **(a)** 5 minutos para acciones sensibles (supuesto actual).
- **(b)** Otro valor.

**Recomendación: (a).** Es corta frente a la sesión interna de 30 minutos (§7.3) y
suficiente para una firma.
**Decisión:** **(a)**, 5 minutos. Diego, 2026-09-30.

## A11. Motivos de rechazo en moderación y dónde se comprueban las incompatibilidades

**A11.1 `REJECT` en moderación.** Falta el enum del "motivo estructurado" de §4.1.
Propuesta inicial, para corregir: `CONTENT_POLICY`, `PRIZE_INELIGIBLE`,
`TERMS_INCOMPLETE`, `MEDIA_INVALID`, `LEGAL_REQUIREMENT`, `OTHER` (este último con
texto obligatorio). **Decisión:** lista aprobada tal cual. Diego, 2026-09-30.

**A11.2 Incompatibilidades.** §3.16 l.2816 y §7.2 se contradicen:

| Regla | §3.16 dice | §7.2 dice | Propuesta |
|---|---|---|---|
| INC-07 | Ejecución | Asignación y ejecución | Ejecución: `ADMIN_FINANCE` no tiene `A` en atestar; no hay par de subroles que bloquear |
| INC-10 | Ejecución | Organizativo, auditado | Organizativo: no hay comprobación en DB |
| INC-11 | Asignación | Ejecución | Ejecución: depende de la acción concreta |

**Recomendación:** §7.2 prevalece, con INC-07 solo en ejecución; §3.16 se corrige
en V8. Los disparadores y comprobaciones siguen siendo implementación humana.
**Decisión:** **§7.2 ajustada**, INC-07 solo en ejecución. Diego, 2026-09-30.
