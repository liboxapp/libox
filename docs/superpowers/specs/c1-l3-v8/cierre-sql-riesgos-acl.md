---
title: C1 — riesgos de la matriz B1 en clases operativas
status: borrador
tags: [r0, c1, l3-v8, sql, acl, datos-personales]
updated: 2026-10-01
description: Columnas con datos personales, documentos o controles que B1 deja legibles o modificables fuera de las clases sensibles; sin ampliar privilegios.
---

# Riesgos de la matriz B1

Anexo de [pendientes SQL](cierre-sql-pendientes.md). La [matriz B1](decisiones-c1-datos.md#b1-matriz-de-privilegios-de-las-67-tablas-pendiente_matriz)
se aplica tal como se aprobó. Este anexo **no cambia ni amplía privilegios**: registra
columnas de V7 que pueden chocar con B1-bis ("la base no guarda datos personales en
claro" y reportería por vistas seudonimizadas). Decide Diego; si procede, la clase se
corrige en el manifiesto y en el SQL V8.

## Datos personales legibles por `libox_read`

| Tabla (clase) | Columnas | Riesgo |
|---|---|---|
| `client_transfer_acceptances` (registro inmutable) | `ip_address`, `accepted_by`, `device_id` | IP de una persona identificada |
| `risk_events` (registro inmutable) | `ip_address`, `device_id`, `context` JSONB | IP y contexto libre por sujeto |
| `devices`, `user_devices` (operativa) | `fingerprint`, `user_agent`, `user_id` | Huella de dispositivo vinculable a usuarios |
| `clients` (operativa) | `legal_name`, `trade_name`, `owner_user_id`, `owner_document_hash` | En persona natural, `legal_name` es el nombre del titular |
| `winner_legal_readiness` (operativa) | `marital_status`, `winner_user_id`, `decline_reason` | Estado civil del ganador |
| `responsible_play_events` (registro inmutable) | `user_id`, `event_kind`, `context` | Conducta de juego. `self_exclusions` es ahora reservada, pero sus eventos quedan legibles |
| `survey_responses`, `transfer_acts`, `pc_stage_documents`, `alarms`, `audit_emergency_queue` | `answer_text`, `observation_notes`, `notes`, `context`, `payload` | Texto o JSONB libre que puede contener datos personales |
| `benefit_redemptions`, `waitlists`, `attribution_touches`, `user_attributions` | `user_id` con actividad | Perfilado por usuario sin seudonimizar |

## Claves de documentos fuera de las clases sensibles

`client_kyb_documents.object_key` es operativa y legible por `libox_read`, mientras
su padre `client_kyb` es sensible. Lo mismo ocurre con las claves de
`notarial_instruments`, `pc_stage_documents`, `prize_valuation_documents`,
`registry_blocks`, `room_evidence`, `raffle_terms.pdf_object_key`,
`prize_market_references.screenshot_key` y `registry_queries.raw_response_key`.
La clave sola no abre el objeto si el almacenamiento es privado, pero identifica
documentos de identidad o KYB. Precondición: el bucket debe ser privado y servirse
con URL firmada emitida por la app.

## Controles modificables por `libox_app`

- `risk_rules` (operativa, `UPDATE`): la app puede cambiar `expression` o poner
  `enabled = false` en reglas de riesgo y AML.
- `client_members` (operativa, `UPDATE`): cambia subroles de cliente
  (`CLIENT_OWNER`, `CLIENT_MANAGER`). El disparador V7 `trg_natural_single_member`
  sigue activo, pero las comprobaciones de incompatibilidad en ejecución son zona
  humana.
- `registrable_assets`, `pc_workflow_stages`, `winner_legal_readiness` y
  `transfer_acts` (operativa, `UPDATE`): forman el proceso de premios registrables.
  Si alguna etapa habilita la liberación de fondos (INV-44), por comportamiento
  caería en zona crítica.
- `daily_codes` (registro inmutable): `libox_read` lee el código vigente de cada
  sorteo antes de `expires_at`.

## Qué no cambia

Las sondas `ACL-B1-*` y `ACL-MATRIZ` exigen exactamente la matriz aprobada. Cualquier
reclasificación debe ir en la decisión antes que en el manifiesto; la prueba
`test_b1_matches_decision_doc` falla si divergen.
