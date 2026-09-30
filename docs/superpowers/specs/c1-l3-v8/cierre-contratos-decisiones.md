---
title: C1 — decisiones privilegiadas y segunda firma
status: borrador
tags: [r0, c1, openapi, l3-v8]
updated: 2026-09-30
description: Decisiones de valoración, gate legal y moderación y solicitudes de segunda firma integradas en el borrador; etapas P-C, rechazos y código del día pendientes.
---

# Decisiones privilegiadas

Parte del [diseño de cierre](cierre-contratos.md). `submitPrizeValuation` y `submitPcStage` solo
presentan evidencias. Estas operaciones cubren las transiciones de
[L3 §4.1](../../../linea-base/LIBOX_ESPECIFICACION_TECNICA_L3_V7.md) que exigen una persona y
que el canon permite cerrar hoy.

## Forma común, integrada

- **Petición.** `expected_version` del recurso decidido, un `outcome` de enum cerrado y un
  `reason` (10..2000). No lleva `second_signer_id`, banda, desviación ni campos de comisión.
- **Respuesta 201: `DecisionReceiptResponse`.** Contiene `decision_id`, `status`
  (`RECORDED` | `PENDING_SECOND_SIGNATURE`), `signature_request_id` y `subject_version`.
  `signature_request_id` es obligatorio si falta firma y nulo en caso contrario.
- **Sesión.** `aal2` y reautenticación reciente; si falta, 401 `ERR_AUTH_REAUTH_REQUIRED`.
  Incompatibilidad: 403 `ERR_RBAC_INCOMPATIBLE_SUBROLE`.

## Operaciones integradas

| `operationId` | Ruta | `outcome` | Roles | Errores propios |
|---|---|---|---|---|
| `decideValuation` | `POST /valuations/{id}/decisions` | `APPROVED`, `OBSERVED` | `SUPPORT_VALUATOR`, `ADMIN_LEGAL_COMPLIANCE` | 409 versión; 422 `ERR_PRIZE_DEVIATION_REJECTED`, `ERR_PRIZE_EVIDENCE_INCOMPLETE`, `ERR_PRIZE_REFERENCE_STALE` |
| `decideLegalGate` | `POST /raffles/{raffle_ref}/legal-gate/decisions` | `PASSED` | `ADMIN_LEGAL_COMPLIANCE` | 409 `ERR_LEGAL_GATE`, `ERR_RAFFLE_INVALID_TRANSITION`, `ERR_REGISTRABLE_STAGE_INCOMPLETE`, versión |
| `decideModeration` | `POST /raffles/{raffle_ref}/moderation/decisions` | `APPROVE_SCHEDULED`, `APPROVE_IMMEDIATE` | `ADMIN_MODERATION` | 409 transición, bases congeladas o versión |

Detalle por operación:

- **Valoración.**
  - `approved_value` (`Money`) es obligatorio con `APPROVED` y está prohibido con `OBSERVED`.
  - `exception_justification` (≥50, RN-22) solo se admite con `APPROVED`.
  - El servidor decide si la banda o la desviación exigen cofirma o segunda firma; en ese caso,
    la respuesta es `PENDING_SECOND_SIGNATURE`.
  - El cálculo y su efecto sobre el rango de recaudación son implementación humana.
- **Gate legal.**
  - `requirement_results[]` lleva `requirement_key` (1..60, clave de
    `market_legal_requirements`, sin lista cerrada) y `document_upload_id`.
  - El ejemplo usa una clave sintética.
  - La autoridad está `PENDING_LEGAL_OPINION` [LEGAL→ABOGADO].
- **Moderación.** Valida capacidad y categoría efectivas.

## Solicitudes de segunda firma, integradas

| `operationId` | Ruta | Contrato |
|---|---|---|
| `listSignatureRequests` | `GET /signature-requests` | Filtros `status`, `cursor` y `limit`; solo las que quien llama podría firmar |
| `getSignatureRequest` | `GET /signature-requests/{id}` | Solicitante o firmante elegible |
| `signSignatureRequest` | `POST /signature-requests/{id}/sign` | `expected_version`, `decision` (`SIGN` \| `DECLINE`), `reason`; 409 `ERR_RBAC_SELF_SIGNATURE` o versión |
| `cancelSignatureRequest` | `POST /signature-requests/{id}/cancel` | `ActionRequest`; solo el solicitante, mientras esté `PENDING` |

`SignatureRequest` tiene:

- `action_code`, enum de 11 códigos con respaldo en el canon o en este diseño:
  - valoración: `VALUATION_V2_COSIGN`, `VALUATION_V4`, `VALUATION_EXCEPTION`;
  - etapas P-C: `PC_STAGE_E3`, `PC_STAGE_E7`, `ATTEST_PC`;
  - mercado: `CAPABILITY_PLATFORM_DISABLE`, `MARKET_RESUME`;
  - recaudación: `MULTIPLE_OVERRIDE`;
  - cuentas internas: `SUBROLE_GRANT`, `MFA_RESET_INTERNAL`.
- `subject_kind` (enum) y `subject_id`.
- `subject_version`, `requested_by`, `status`, `expires_at` y `version`.

**Decisión de diseño.** El sujeto no se copia dentro de la solicitud: el firmante lo lee con su
propia lectura versionada. Así se evitan tanto el objeto genérico como el `oneOf` por código
que el diseño anterior proponía. La firma se rechaza si el sujeto cambió desde `subject_version`.

Qué subroles firman cada código es un dato de la política por acción (I-04). Mientras esa
política no exista, ninguna solicitud es firmable (falla cerrado). La comprobación de INC-09 e
INC-11 en ejecución es zona crítica, de implementación humana.

## Pendiente, con motivo

| Pendiente | Motivo | Dueño |
|---|---|---|
| Rechazo manual de valoración; observar o rechazar el gate legal | Sin transición FSM (I-06) | Diego; [LEGAL→ABOGADO] |
| `REJECT` en moderación | Falta el enum del "motivo estructurado" de §4.1 | Diego |
| Actor de `VALUATION_OBSERVED` | "Verificador" no es un subrol (I-03); el contrato lo limita a los aprobadores de banda | Diego |
| Cofirma V2 por `ADMIN_MODERATION` | Choca con §7.1 (I-01); modelada como firma, no como escritura | Diego |
| Decisiones de etapa P-C | Actores en conflicto (I-02) y `checklist_key` sin semilla (I-08) | Diego y [LEGAL→ABOGADO] |
| `submitPcStage` con `documents[]` por `checklist_key` | Misma causa (I-08). La operación del inventario no se toca | Diego |
| Código del día (`POST /raffles/{raffle_ref}/daily-codes`) y retirar `daily_code` de `PrizeValuation` | Cambiaría una operación del inventario junto con el insumo por premio de T6; se hará al integrar T1–T8 | Diego |
| `market_references[]` tipadas en la presentación de valoración | Misma dependencia que el punto anterior | Diego |
| Atestación sin `second_signer_id` | Cambia un cuerpo explícito de §11.5 (CC-08) | Diego |
| Apagado global de capacidad con firma | Política de firmantes (I-04) | Diego |
