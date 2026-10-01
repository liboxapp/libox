---
title: C1 — decisiones privilegiadas y segunda firma
status: borrador
tags: [r0, c1, openapi, l3-v8]
updated: 2026-10-01
description: Decisiones de valoración, gate legal, moderación y KYB, política de segunda firma por acción y matriz P-C integradas en draft.3; decisión de etapa P-C y código del día pendientes.
---

# Decisiones privilegiadas

Parte del [diseño de cierre](cierre-contratos.md). `submitPrizeValuation` y `submitPcStage` solo
presentan evidencias. Estas operaciones cubren las transiciones de
[L3 §4.1](../../../linea-base/LIBOX_ESPECIFICACION_TECNICA_L3_V7.md) que exigen una persona y
las que añadieron los [acuerdos A1–A11](decisiones-c1.md) del 30/09, integrados en draft.3.
El flujo [Cowork](reconciliacion-aceptacion.md) es una propuesta no ratificada: no define
actores ni firmas de cobertura, devolución o ejecución, y no extiende otros permisos.

## Forma común, integrada

- **Petición.** `expected_version` del recurso decidido, un `outcome` de enum cerrado y un
  `reason` (10..2000). No lleva `second_signer_id`, banda, desviación ni campos de comisión.
- **Respuesta 201: `DecisionReceiptResponse`.** Contiene `decision_id`, `status`
  (`RECORDED` | `PENDING_SECOND_SIGNATURE`), `signature_request_id` y `subject_version`.
  `signature_request_id` es obligatorio si falta firma y nulo en caso contrario.
- **Sesión.** `aal2` y reautenticación en los últimos 5 minutos (A10); si falta, 401
  `ERR_AUTH_REAUTH_REQUIRED`. Incompatibilidad: 403 `ERR_RBAC_INCOMPATIBLE_SUBROLE`.
- **`x-outcome-transitions`.** Cada `outcome` declara origen, destino, disparador y actores.
  Solo usa estados de `ck_raffles_status` del SQL V7; los disparadores nuevos son de A6.

## Operaciones integradas

| `operationId` | Ruta | `outcome` | Roles | Errores propios |
|---|---|---|---|---|
| `decideValuation` | `POST /valuations/{id}/decisions` | `APPROVED`, `OBSERVED`, `REJECTED` | `SUPPORT_VALUATOR`, `ADMIN_LEGAL_COMPLIANCE` | 409 versión; 422 `ERR_PRIZE_DEVIATION_REJECTED`, `ERR_PRIZE_EVIDENCE_INCOMPLETE`, `ERR_PRIZE_REFERENCE_STALE` |
| `decideLegalGate` | `POST /raffles/{raffle_ref}/legal-gate/decisions` | `PASSED`, `OBSERVED`, `REJECTED` | `ADMIN_LEGAL_COMPLIANCE` | 409 `ERR_LEGAL_GATE`, `ERR_RAFFLE_INVALID_TRANSITION`, `ERR_REGISTRABLE_STAGE_INCOMPLETE`, versión |
| `decideModeration` | `POST /raffles/{raffle_ref}/moderation/decisions` | `APPROVE_SCHEDULED`, `APPROVE_IMMEDIATE`, `REJECT` | `ADMIN_MODERATION` | 409 transición, bases congeladas o versión |
| `decideKyb` | `POST /clients/{id}/kyb/decisions` | `APPROVED`, `REJECTED` | `ADMIN_COMPLIANCE` | 409 versión |

Detalle por operación:

- **Valoración.**
  - `approved_value` (`Money`) es obligatorio con `APPROVED` y está prohibido en el resto.
  - `exception_justification` (≥50, RN-22) solo se admite con `APPROVED`.
  - `REJECTED` (A6) lleva a `REJECTED` por `VALUATION_REJECTED`; `OBSERVED` vuelve a `DRAFT`.
    Ambos, con los aprobadores de banda (A3).
  - El servidor decide si la banda o la desviación exigen cofirma o segunda firma; en ese caso,
    la respuesta es `PENDING_SECOND_SIGNATURE`. La cofirma V2 la firma `ADMIN_MODERATION` sin
    escritura (A2).
  - El cálculo y su efecto sobre el rango de recaudación son implementación humana.
- **Gate legal.**
  - `requirement_results[]` es obligatorio con `PASSED` y opcional al observar o rechazar.
    Lleva `requirement_key` (1..60, clave de `market_legal_requirements`, sin lista cerrada) y
    `document_upload_id`. El ejemplo usa una clave sintética.
  - `OBSERVED` vuelve a `DRAFT` (`LEGAL_GATE_OBSERVED`, subsanable); `REJECTED` es terminal
    (`LEGAL_GATE_REJECTED`). Ambos de A6, [LEGAL→ABOGADO].
- **Moderación.** Valida capacidad y categoría efectivas. `REJECT` exige
  `rejection_reason_code` de `ModerationRejectionReason` (A11.1): `CONTENT_POLICY`,
  `PRIZE_INELIGIBLE`, `TERMS_INCOMPLETE`, `MEDIA_INVALID`, `LEGAL_REQUIREMENT`, `OTHER`. Con
  `OTHER`, `reason` es el texto obligatorio. El código está prohibido al aprobar.
- **KYB.** `expected_version` es la `version` de `getClient`. Resultados limitados a
  `client_kyb.status`; `EXPIRED` lo marca el vencimiento. `ADMIN_RISK` solo lee (A7). La
  decisión no depende del adaptador de Truora, todavía en evaluación.

## Solicitudes de segunda firma, integradas

| `operationId` | Ruta | Contrato |
|---|---|---|
| `listSignatureRequests` | `GET /signature-requests` | Filtros `status`, `cursor` y `limit`; solo las que quien llama podría firmar |
| `getSignatureRequest` | `GET /signature-requests/{id}` | Solicitante o firmante elegible |
| `signSignatureRequest` | `POST /signature-requests/{id}/sign` | `expected_version`, `decision` (`SIGN` \| `DECLINE`), `reason`; 409 `ERR_RBAC_SELF_SIGNATURE` o versión |
| `cancelSignatureRequest` | `POST /signature-requests/{id}/cancel` | `ActionRequest`; solo el solicitante, mientras esté `PENDING` |

`SignatureRequest` tiene `action_code` (11 códigos), `subject_kind`, `subject_id`,
`subject_version`, `requested_by`, `eligible_signer_subroles`, `status`, `expires_at` y `version`.

**Política A1 como dato.** `x-second-signature-policy` reproduce la tabla aprobada: por código,
subroles que solicitan, subroles que firman, regla de subrol y `grants_write: false`. Otra persona
siempre; otro subrol salvo en acciones propias de `ADMIN_SUPER`, donde firma otro `ADMIN_SUPER`.
`eligible_signer_subroles` solo admite subroles de la fila de su código; en
`VALUATION_EXCEPTION` el servidor excluye el del solicitante. Los `x-allowed-roles` de las
operaciones de firma se derivan de la política: firman `SUPPORT_VALUATOR`, `ADMIN_MODERATION`,
`ADMIN_LEGAL_COMPLIANCE` y `ADMIN_SUPER`; `ADMIN_FINANCE` no participa.
`MULTIPLE_OVERRIDE` solo fija el firmante, no la regla del múltiplo.

**Decisión de diseño.** El sujeto no se copia dentro de la solicitud: el firmante lo lee con su
propia lectura versionada. La firma se rechaza si el sujeto cambió desde `subject_version`.
INC-09 e INC-11 en ejecución son zona crítica, de implementación humana.

## Etapas P-C

`listPcStages` y `submitPcStage` declaran `x-pc-stage-approvers` con la matriz A4: E1
`ADMIN_RISK`; E2–E4 y E7 `ADMIN_LEGAL_COMPLIANCE`; E5 automática; E6 verifica `SUPPORT_L2` y
habilita `ADMIN_LEGAL_COMPLIANCE`; firmas `PC_STAGE_E3` y `PC_STAGE_E7`. E2, E4 y E7 quedan
[LEGAL→ABOGADO]. No hay operación de decisión de etapa: P-C entra en el MVP (A8), pero sigue
bloqueado hasta recibir la lista de documentos.

## Pendiente, con motivo

| Pendiente | Motivo | Dueño |
|---|---|---|
| Decisiones de etapa P-C | Lista de documentos por etapa A8 (I-08) | Diego y [LEGAL→ABOGADO] |
| `submitPcStage` con `documents[]` por `checklist_key` | Misma causa (I-08). La operación del inventario no se toca | Diego |
| Código del día (`POST /raffles/{raffle_ref}/daily-codes`) y retirar `daily_code` de `PrizeValuation` | Cambiaría una operación del inventario junto con el insumo por premio de T6 | Diego |
| `market_references[]` tipadas en la presentación de valoración | Misma dependencia que el punto anterior | Diego |
| Apagado global de capacidad con firma | A1 lo desbloquea; falta diseñar la operación | Diego |
| `second_signer_id` en `adjudicateDispute` | No figura entre los 11 códigos ni en A9 | Diego |
