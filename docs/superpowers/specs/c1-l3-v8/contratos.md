---
title: C1 — inventario contractual de L3 V8
status: borrador
tags: [r0, c1, openapi]
updated: 2026-09-30
description: Operaciones extraídas de L3 §11, cobertura V7 y requisitos de cierre del contrato.
---

# Inventario contractual para L3 V8

Base común `/api/v1`. Extracción de [L3 V7 §11](../../../linea-base/LIBOX_ESPECIFICACION_TECNICA_L3_V7.md).
Se identifican **61 pares método/ruta**, frente a **16 operaciones** del YAML V7.
Los métodos omitidos en §11.7 se heredan del último explícito solo para este inventario;
deben ratificarse al redactar cada operación. No es un OpenAPI completo ni validado.

| Método propuesto | Ruta | Origen | Método | En YAML V7 |
|---|---|---|---|---|
| POST | `/orders` | 11.2 Compra | explícito | sí |
| GET | `/orders/{id}` | 11.2 Compra | explícito | sí |
| GET | `/me/tickets` | 11.3 Tickets y participación | explícito | sí |
| GET | `/me/tickets/{raffle_id}` | 11.3 Tickets y participación | explícito | no |
| GET | `/public/draws/{slug}` | 11.4 Verificación pública | explícito | sí |
| GET | `/public/draws/{slug}/pool` | 11.4 Verificación pública | explícito | sí |
| POST | `/rooms/{id}/messages` | 11.5 Resolución | explícito | no |
| POST | `/rooms/{id}/evidence` | 11.5 Resolución | explícito | no |
| POST | `/rooms/{id}/claim` | 11.5 Resolución | explícito | no |
| POST | `/rooms/{id}/shipping-quotes` | 11.5 Resolución | explícito | no |
| POST | `/rooms/{id}/shipping-selection` | 11.5 Resolución | explícito | no |
| POST | `/rooms/{id}/attest` | 11.5 Resolución | explícito | sí |
| POST | `/rooms/{id}/sla-extension` | 11.5 Resolución | explícito | no |
| GET | `/rooms/{id}/forensic-export` | 11.5 Resolución | explícito | no |
| GET | `/clients/{id}/settlements` | 11.6 Liquidación | explícito | no |
| GET | `/settlements/{id}` | 11.6 Liquidación | explícito | sí |
| POST | `/settlements/{id}/execute` | 11.6 Liquidación | explícito | sí |
| POST | `/settlements/batch-execute` | 11.6 Liquidación | explícito | no |
| POST | `/auth/register` | 11.7 Identidad | explícito | no |
| POST | `/auth/verify-contact` | 11.7 Identidad | heredado; confirmar | no |
| POST | `/auth/login` | 11.7 Identidad | heredado; confirmar | no |
| POST | `/auth/refresh` | 11.7 Identidad | heredado; confirmar | no |
| POST | `/identity/verify` | 11.7 Identidad | heredado; confirmar | no |
| POST | `/identity/liveness` | 11.7 Identidad | heredado; confirmar | no |
| POST | `/clients` | 11.7 Organizador | explícito | no |
| POST | `/clients/{id}/kyb` | 11.7 Organizador | heredado; confirmar | no |
| POST | `/clients/{id}/members` | 11.7 Organizador | heredado; confirmar | no |
| PUT | `/clients/{id}/payout` | 11.7 Organizador | explícito | no |
| PUT | `/clients/{id}/capabilities` | 11.7 Organizador | heredado; confirmar | no |
| GET | `/raffles` | 11.7 Catálogo | explícito | sí |
| GET | `/raffles/{slug}` | 11.7 Catálogo | heredado; confirmar | sí |
| GET | `/raffles/{slug}/terms` | 11.7 Catálogo | heredado; confirmar | no |
| POST | `/raffles` | 11.7 Sorteo | explícito | no |
| PATCH | `/raffles/{id}` | 11.7 Sorteo | explícito | no |
| POST | `/raffles/{id}/submit` | 11.7 Sorteo | explícito | no |
| POST | `/raffles/{id}/prize-valuation` | 11.7 Sorteo | heredado; confirmar | no |
| POST | `/raffles/{id}/pc-stages/{stage}` | 11.7 Sorteo | heredado; confirmar | no |
| POST | `/webhooks/psp/{provider}` | 11.7 Pagos | explícito | sí |
| GET | `/reconciliation/{date}` | 11.7 Pagos | explícito | no |
| POST | `/reconciliation/exceptions/{id}/resolve` | 11.7 Pagos | explícito | no |
| POST | `/raffles/{id}/freeze` | 11.7 Sorteo ejecutado | explícito | no |
| POST | `/raffles/{id}/execute-draw` | 11.7 Sorteo ejecutado | heredado; confirmar | no |
| POST | `/raffles/{id}/redraw` | 11.7 Sorteo ejecutado | heredado; confirmar | no |
| POST | `/disputes` | 11.7 Controversias | explícito | no |
| POST | `/disputes/{id}/evidence` | 11.7 Controversias | heredado; confirmar | no |
| POST | `/disputes/{id}/adjudicate` | 11.7 Controversias | heredado; confirmar | no |
| GET | `/me/refund-credit` | 11.7 Saldo | explícito | sí |
| POST | `/me/refund-credit/withdrawals` | 11.7 Saldo | explícito | no |
| GET | `/me/limits` | 11.7 Protección | explícito | no |
| PUT | `/me/limits` | 11.7 Protección | explícito | sí |
| POST | `/me/self-exclusion` | 11.7 Protección | explícito | sí |
| GET | `/me/spend-panel` | 11.7 Protección | explícito | no |
| GET | `/compliance/cases` | 11.7 Cumplimiento | explícito | no |
| POST | `/compliance/cases/{id}/decide` | 11.7 Cumplimiento | explícito | no |
| GET | `/alarms` | 11.7 Alarmas | explícito | no |
| POST | `/alarms/{id}/acknowledge` | 11.7 Alarmas | explícito | no |
| POST | `/alarms/{id}/resolve` | 11.7 Alarmas | heredado; confirmar | no |
| GET | `/markets/{code}/config` | 11.7 Mercado | explícito | no |
| POST | `/markets/{code}/config` | 11.7 Mercado | explícito | no |
| POST | `/markets/{code}/suspend` | 11.7 Mercado | heredado; confirmar | sí |
| POST | `/public/pricing-simulator` | 11.7 Simulador | explícito | sí |

## Reglas propuestas para el artefacto V8

- OpenAPI 3.1: reemplazar `nullable` por unión explícita con `null`; validar esquemas y referencias con un validador 3.1.
- Scalar consume el mismo artefacto que genera tipos y pruebas de contrato. Registrar PRD V9 y L3 V8 en metadatos al emitir.
- Cada operación lleva operationId único, rol/ámbito, parámetros, cuerpo, respuesta de éxito y catálogo de errores aplicables. Nada de esquemas genéricos vacíos para completar el conteo.
- Definir Idempotency-Key en mutaciones de dinero, trace_id/X-Trace-Id, cursor opaco y limit de 1 a 100. El webhook valida firma y repetición, no JWT del comprador.
- Acceso público explícito para catálogo y pruebas públicas; nunca heredar bearerAuth por accidente. Las evidencias y exports forenses requieren autorización por recurso.
- Propuesta pendiente: importes BIGINT como cadena decimal en JSON para preservar precisión en TypeScript; moneda adyacente. Es cambio del contrato previo y requiere decisión antes de emitir, incluyendo ejemplos/clientes.
- Distinguir credenciales de proveedor de permisos Libox: el contrato no expone service-role, identificadores KYC sensibles ni datos de otros participantes.

## Cierre verificable

La matriz debe reconciliar las 61 operaciones y resolver los métodos heredados.
Después, validar el archivo completo, generar cliente/servidor simulado y comprobar
respuestas contra el esquema. C1 no acredita estas pruebas mientras solo exista esta matriz.
Los endpoints de dinero, sorteo y concurrencia especifican contratos; su implementación
continúa reservada al dueño humano según [zonas sin IA](../../../../.claude/rules/zonas-sin-ia.md).
