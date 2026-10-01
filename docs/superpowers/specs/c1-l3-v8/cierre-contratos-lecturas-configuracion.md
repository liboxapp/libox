---
title: C1 — lecturas versionadas y configuración T1–T8
status: borrador
tags: [r0, c1, openapi, l3-v8]
updated: 2026-10-01
description: Nueve GET versionados; C1–C4 (T1, T7, precio, régimen y costos) y capacidades A5 integradas en draft.3; T2–T6, documento de mercado y capacidades en tres capas siguen como diseño.
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
| `getRaffleManagement` | `GET /raffles/{raffle_ref}/management` | Campos de `RaffleDraft`, régimen, `expiry_policy`, `recurrence`, estado FSM, `config_version`, `version`; exige UUID | "Sorteo propio" |
| `getValuation` | `GET /valuations/{id}` | Banda, desviación, resultado según el canon, `approved_value`, `version` | "Valoración de premio" |
| `listPcStages` | `GET /raffles/{raffle_ref}/pc-stages` | E1–E7 con el estado del canon, plazos y `version` por etapa; matriz A4 | "Etapas P-C" |
| `getDispute` | `GET /disputes/{id}` | `Dispute` con `version` | Parte, `ADMIN_LEGAL_COMPLIANCE`, `ADMIN_SUPER` |
| `getMarketConfigVersion` | `GET /markets/{code}/config/versions/{version}` | Vigencia, `config_hash` y `MarketConfig` congelada | "Configuración de mercado" |
| `listPlatformCapabilities` | `GET /platform/capabilities` | Capacidades de plataforma según L3 §2.1, con alcance del apagado | `ADMIN_SUPER` (derivado) |

Reglas de las lecturas:

- `version` pertenece al agregado de la ruta. Una decisión de etapa usará la versión de la etapa,
  no la del sorteo. `decideKyb` usa la `version` de `getClient`.
- Fuera de ámbito, la respuesta es 404.
- El pago nunca expone número ni titular en claro.
- `getValuation` y `listPcStages` usan los enums del canon: `prize_valuations.outcome` y
  `pc_workflow_stages.status`. I-11 ya alineó los comandos correspondientes; no
  implica implementar esas transiciones.

Diferencias frente al diseño anterior, y su motivo:

- **`getCapabilities`** devuelve solo la capa cliente. La resolución en tres capas de INV-45
  necesita las capas de plataforma y mercado combinadas por servidor. Queda pendiente, igual que
  la operación de apagado global, que A1 ya desbloquea con `CAPABILITY_PLATFORM_DISABLE`.
- **`getMarketConfigVersion`** expone el `MarketConfig` que ya existe, que es parcial frente a
  L3 §10.1.
- **Se retiró `allowed_raffle_types` de `getClient`** porque contradice §7.1 (S-4).

## Configuración integrada en draft.3 (C1–C4)

Aplica los [acuerdos C1–C4](decisiones-c1-configuracion.md) del 30/09 en `RaffleDraft` (alta del
sorteo), `PrizeValuation` y la lectura de gestión. El tipo efectivo es `raffle_type` o, en T8,
`base_type`. No implementa reembolsos, sorteo ni cálculo de comisión.

| Decisión | Contrato | Lo que no se inventa |
|---|---|---|
| C1 T1 | `expiry_policy` obligatorio en T1 y prohibido en el resto: `max_duration_days` y `on_expiry: DRAW_IF_MINIMUM_REACHED_ELSE_REFUND` | Mínimo vendido, su unidad y quién lo fija; premio con mínimo; aviso al comprador. `x-requirement-status: incomplete-pending-threshold`: un T1 no es publicable hasta fijarlos |
| C2 T7 | `recurrence` obligatorio en T7: `frequency` del CHECK canónico, `interval_count`, `edition_duration_minutes`, `max_editions`; `x-server-rule` sin solape | Medición del intervalo `MONTHLY` con calendario |
| C3 Precio | `ticket_price` obligatorio y fijado por el organizador; se rechazan `target_net_amount` y los importes derivados | El simulador mantiene `target_net_amount` obligatorio y `ticket_price` opcional; decidir la entrada principal |
| C4 Régimen | `economic_regime` solo `PAID` (por defecto) | `FREE_ENTRY` y `PROMOTIONAL` siguen fuera hasta diseñar la garantía sustitutiva |
| C4 Costos | `declared_costs[]` en `PrizeValuation`: `cost_kind` (`SHIPPING`, `NOTARY`, `REGISTRY`), `estimated_amount` (`Money`) y `borne_by` del canon | `charge_kind` y `macrozone` (DP-25); `recurring_charges` y `shipping_estimates` no se contratan |

`macrozone` ya aparecía como texto libre en `shipping_estimates` de las lecturas públicas; se
mantiene sin enum hasta que Diego lo defina. La aclaración aprobada de C1 rige: mínimo, premio y
condiciones se fijan antes de publicar y no cambian tras la primera compra.

## Resto de la configuración por tipo: solo diseño

T2–T6, las fechas de venta y el bloque común de `RaffleConfiguration` no se integraron. Los
[deltas Cowork](reconciliacion-linea-base.md) son una propuesta no ratificada: mínimo
económico, cobertura, ventanas y desenlaces públicos no entran en el contrato.

| Punto | Qué falta | Dueño |
|---|---|---|
| T2–T6 y fechas | `end_at`, `min_threshold`, hitos, ganadores y variante T8 | Diego |
| Cowork | Fecha final T1–T8, ventana de mercado/tipo, mínimo/configuración fijada, cobertura y desenlace público | Diego; contabilidad/abogado según materia |

Diseño que se mantiene para cuando esos puntos se cierren:

La ampliación exige fecha final común a T1–T8, mínimo y condiciones publicados
con versión aprobada e inmutable. Mapear una sola nomenclatura entre `end_at` de
dominio y `ends_at` del contrato actual; declarar cobertura/desenlaces antes de
comprar. La tabla de variantes heredada no constituye esa ampliación terminada.

- **Estructura.** `RaffleConfiguration` como `oneOf` discriminado por `raffle_type`. Bloque
  común: título (≤140), bases, `total_tickets`, `unclaimed_route`, `shipping_paid_by`,
  `starts_at`, premios por posición y costos tipados. Debe reutilizar `T1ExpiryPolicy`,
  `EditionRecurrence` y `DeclaredCost`.
- **Campos por variante:**

  | Tipo | Campos | Tope del esquema |
  |---|---|---|
  | T2 | `end_at`, `min_threshold` | — |
  | T3 | `end_at` | — |
  | T4 | `milestones` | 2..6 |
  | T5 | `starts_at`, `end_at` | — |
  | T6 | `winners_count` | 2..10 |
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
- **Integrado (A5).** `LIVE` no existe en ningún enum: T8 es la única capacidad de sorteo en
  vivo. `P_C1` y `P_C2` van en `enabled_categories`, obligatorio en `CapabilitiesUpdate`,
  `Capabilities` y sus respuestas; ambos arrays son de elementos únicos. Habilitar la
  categoría no levanta el bloqueo P-C de A8.
