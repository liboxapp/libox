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
El [borrador OpenAPI 3.1](libox_openapi_L3_V8_DRAFT.yaml) cubre esos 61 pares en
57 rutas normalizadas. Los métodos heredados se concretan en este borrador como
se indica en la tabla; su emisión normativa corresponde a C2.
Las [notas del contrato](notas-contractuales.md) delimitan cambios y decisiones abiertas.

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
| POST | `/auth/verify-contact` | 11.7 Identidad | heredado; concretado en borrador | no |
| POST | `/auth/login` | 11.7 Identidad | heredado; concretado en borrador | no |
| POST | `/auth/refresh` | 11.7 Identidad | heredado; concretado en borrador | no |
| POST | `/identity/verify` | 11.7 Identidad | heredado; concretado en borrador | no |
| POST | `/identity/liveness` | 11.7 Identidad | heredado; concretado en borrador | no |
| POST | `/clients` | 11.7 Organizador | explícito | no |
| POST | `/clients/{id}/kyb` | 11.7 Organizador | heredado; concretado en borrador | no |
| POST | `/clients/{id}/members` | 11.7 Organizador | heredado; concretado en borrador | no |
| PUT | `/clients/{id}/payout` | 11.7 Organizador | explícito | no |
| PUT | `/clients/{id}/capabilities` | 11.7 Organizador | heredado; concretado en borrador | no |
| GET | `/raffles` | 11.7 Catálogo | explícito | sí |
| GET | `/raffles/{slug}` | 11.7 Catálogo | heredado; concretado en borrador | sí |
| GET | `/raffles/{slug}/terms` | 11.7 Catálogo | heredado; concretado en borrador | no |
| POST | `/raffles` | 11.7 Sorteo | explícito | no |
| PATCH | `/raffles/{id}` | 11.7 Sorteo | explícito | no |
| POST | `/raffles/{id}/submit` | 11.7 Sorteo | explícito | no |
| POST | `/raffles/{id}/prize-valuation` | 11.7 Sorteo | heredado; concretado en borrador | no |
| POST | `/raffles/{id}/pc-stages/{stage}` | 11.7 Sorteo | heredado; concretado en borrador | no |
| POST | `/webhooks/psp/{provider}` | 11.7 Pagos | explícito | sí |
| GET | `/reconciliation/{date}` | 11.7 Pagos | explícito | no |
| POST | `/reconciliation/exceptions/{id}/resolve` | 11.7 Pagos | explícito | no |
| POST | `/raffles/{id}/freeze` | 11.7 Sorteo ejecutado | explícito | no |
| POST | `/raffles/{id}/execute-draw` | 11.7 Sorteo ejecutado | heredado; concretado en borrador | no |
| POST | `/raffles/{id}/redraw` | 11.7 Sorteo ejecutado | heredado; concretado en borrador | no |
| POST | `/disputes` | 11.7 Controversias | explícito | no |
| POST | `/disputes/{id}/evidence` | 11.7 Controversias | heredado; concretado en borrador | no |
| POST | `/disputes/{id}/adjudicate` | 11.7 Controversias | heredado; concretado en borrador | no |
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
| POST | `/alarms/{id}/resolve` | 11.7 Alarmas | heredado; concretado en borrador | no |
| GET | `/markets/{code}/config` | 11.7 Mercado | explícito | no |
| POST | `/markets/{code}/config` | 11.7 Mercado | explícito | no |
| POST | `/markets/{code}/suspend` | 11.7 Mercado | heredado; concretado en borrador | sí |
| POST | `/public/pricing-simulator` | 11.7 Simulador | explícito | sí |

## Reglas propuestas para el artefacto V8

- OpenAPI 3.1: reemplazar `nullable` por unión explícita con `null`; validar esquemas y referencias con un validador 3.1.
- Scalar consume el mismo artefacto que genera tipos y pruebas de contrato. Registrar PRD V9 y L3 V8 en metadatos al emitir.
- Cada operación lleva operationId único, rol/ámbito, parámetros, cuerpo, respuesta de éxito y catálogo de errores aplicables. Nada de esquemas genéricos vacíos para completar el conteo.
- Definir Idempotency-Key en mutaciones de dinero, trace_id/X-Trace-Id, cursor opaco y limit de 1 a 100. El webhook valida firma y repetición, no JWT del comprador.
- Acceso público explícito para catálogo y pruebas públicas; nunca heredar bearerAuth por accidente. Las evidencias y exports forenses requieren autorización por recurso.
- Ratificado por Diego el 2026-09-30: importes BIGINT como cadena decimal en JSON, moneda adyacente. Se validan rango y precisión; se propone `/api/v2` para evitar sustituir silenciosamente un contrato incompatible.
- Distinguir credenciales de proveedor de permisos Libox: el contrato no expone service-role, identificadores KYC sensibles ni datos de otros participantes.

## Cierre verificable

Validación disponible: estructura OpenAPI 3.1, ejemplos y entradas negativas, 61
intercambios HTTP con fixtures y cliente TypeScript con tipos generados del YAML.
El mock no implementa permisos, firma PSP ni lógica de negocio. Sus respuestas
no acreditan backend, migraciones, cálculos ni pruebas criptográficas correctas.
Persisten dependencias de adaptadores y decisiones descritas en las notas; C1 sigue abierto.
Los endpoints de dinero, sorteo y concurrencia especifican contratos; su implementación
continúa reservada al dueño humano según [zonas sin IA](../../../../.claude/rules/zonas-sin-ia.md).
