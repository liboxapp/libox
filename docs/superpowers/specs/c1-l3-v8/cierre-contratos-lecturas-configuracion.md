---
title: C1 — lecturas versionadas y configuración T1–T8
status: borrador
tags: [r0, c1, openapi, l3-v8]
updated: 2026-09-30
description: Nueve GET versionados integrados en el borrador; configuración por tipo, documento de mercado y capacidades en tres capas quedan como diseño pendiente.
---

# Lecturas versionadas y configuración

Parte del [diseño de cierre](cierre-contratos.md). Las lecturas de firmas, subidas y factores
MFA están en sus notas.

## Lecturas integradas

Todas son `x-origin: c1-auxiliary`, están marcadas `proposed`, responden con
`Cache-Control: no-store` y declaran `x-internal-session` con `aal2` cuando admiten roles
internos. Los roles salen de la fila de
[L3 §7.1](../../../linea-base/LIBOX_ESPECIFICACION_TECNICA_L3_V7.md) indicada.

| `operationId` | Ruta | Devuelve | Roles (fila §7.1) |
|---|---|---|---|
| `getClient` | `GET /clients/{id}` | Estado, tipo, mercado, `kyb_status`, `version` | Los cuatro `CLIENT_*`, `ADMIN_RISK`, `ADMIN_COMPLIANCE`, `ADMIN_SUPER` (sin fila propia) |
| `getPayout` | `GET /clients/{id}/payout` | Mismo cuerpo que `updatePayout`, con cuenta enmascarada | "Datos de cobro" |
| `getCapabilities` | `GET /clients/{id}/capabilities` | Mismo cuerpo que `updateCapabilities` (solo la capa cliente) | "Capacidades del cliente" |
| `getRaffleManagement` | `GET /raffles/{raffle_ref}/management` | Campos de `RaffleDraft`, estado FSM, `config_version`, `version`; exige UUID | "Sorteo propio" |
| `getValuation` | `GET /valuations/{id}` | Banda, desviación, resultado según el canon, `approved_value`, `version` | "Valoración de premio" |
| `listPcStages` | `GET /raffles/{raffle_ref}/pc-stages` | E1–E7 con el estado del canon, plazos y `version` por etapa | "Etapas P-C" |
| `getDispute` | `GET /disputes/{id}` | `Dispute` con `version` | Parte, `ADMIN_LEGAL_COMPLIANCE`, `ADMIN_SUPER` |
| `getMarketConfigVersion` | `GET /markets/{code}/config/versions/{version}` | Vigencia, `config_hash` y `MarketConfig` congelada | "Configuración de mercado" |
| `listPlatformCapabilities` | `GET /platform/capabilities` | Capacidades de plataforma según L3 §2.1, con alcance del apagado | `ADMIN_SUPER` (derivado) |

Reglas de las lecturas:

- `version` pertenece al agregado de la ruta. Una decisión de etapa usará la versión de la etapa,
  no la del sorteo.
- Fuera de ámbito, la respuesta es 404.
- El pago nunca expone número ni titular en claro.
- `getValuation` y `listPcStages` usan los enums del canon: `prize_valuations.outcome` y
  `pc_workflow_stages.status`. Los comandos que ya existían, `submitPrizeValuation` y
  `submitPcStage`, responden con otros enums (I-11) y hay que reconciliarlos al consolidar.

Diferencias frente al diseño anterior, y su motivo:

- **`getCapabilities`** devuelve solo la capa cliente. La resolución en tres capas de INV-45
  necesita las capas de plataforma y mercado combinadas por servidor. Queda pendiente, igual que
  el apagado global con firma: la política de firmantes está abierta (I-04).
- **`getRaffleManagement`** no incluye la configuración por tipo: no se integra a medias.
- **`getMarketConfigVersion`** expone el `MarketConfig` que ya existe, que es parcial frente a
  L3 §10.1.
- **Se retiró `allowed_raffle_types` de `getClient`** porque contradice §7.1 (S-4).

## Configuración por tipo de sorteo: solo diseño

**No se integró.** Quedan enums sin norma, así que integrarla ahora sería un cierre a medias.
Lo que falta decidir antes de hacerlo:

| Punto | Qué falta | Dueño |
|---|---|---|
| Costos y cargas del premio | Enums `cost_kind`, `charge_kind`, `macrozone` que sustituyen el JSONB de V7 | Diego |
| Entrada de precio | Si el organizador fija `ticket_price` o el neto objetivo. Toca comisión, que es zona crítica | Diego; dueño contable sin asignar |
| T1 | Campo de la política de expiración (I-09) | Diego |
| T7 | Duración de cada edición y relación con `end_at` | Diego |
| Régimen económico | `FREE_ENTRY` y `PROMOTIONAL` necesitan diseñar la garantía sustitutiva (S-1) | Diego |

Diseño que se mantiene para cuando esos puntos se cierren:

- **Estructura.** `RaffleConfiguration` como `oneOf` discriminado por `raffle_type`. Bloque
  común: título (≤140), bases, `total_tickets`, `unclaimed_route`, `shipping_paid_by`,
  `starts_at`, premios por posición y costos tipados.
- **Campos por variante:**

  | Tipo | Campos | Tope del esquema |
  |---|---|---|
  | T2 | `end_at`, `min_threshold` | — |
  | T3 | `end_at` | — |
  | T4 | `milestones` | 2..6 |
  | T5 | `starts_at`, `end_at` | — |
  | T6 | `winners_count` | 2..10 |
  | T7 | `recurrence` | `max_editions` ≤52 |
  | T8 | `base_type` y variante base | — |

- **Reglas del servidor, fuera de JSON Schema.** El último hito es el disparador, el número de
  premios coincide con el de ganadores, la duración de T5 respeta la configuración congelada y
  el umbral no supera el total. Se declararán como `x-server-rule`.
- **Operación.** `PUT /raffles/{raffle_ref}/configuration`, con reemplazo completo y
  `expected_version`, solo en `DRAFT`.

## Documento de mercado: solo diseño

`POST /markets/{code}/config` sigue igual. La propuesta es que cree una versión nueva:
`expected_current_version`, `effective_from` futuro, `reason` ≥20 y el documento de L3 §10.1
tipado sección a sección. Los importes irían como `Money` y los puntos base como enteros de 0 a
10000. Queda pendiente porque las secciones de comisión, impuesto y liquidación necesitan
confirmación contable ([LEGAL→ABOGADO] en lo tributario) y la de sorteo depende de la baliza
(H-11/H-12). El proveedor de identidad sigue `PENDING_CONTRACT`. `psp.primary_adapter` coincide
con la elección de Mercado Pago (I-10).

## Capacidades

- Ya aplicado: `reason` ≥20 en `CapabilitiesUpdate`.
- Corrección de diseño: `P_C1` y `P_C2` **no** van en `enabled_raffle_types`, porque no son
  tipos de sorteo. Necesitan un campo propio de capacidades de categoría, que queda pendiente de
  la decisión de Diego junto con `LIVE` (I-05).
