---
title: C1 — cierre de brechas contractuales auxiliares
status: borrador
tags: [r0, c1, openapi, l3-v8]
updated: 2026-09-30
description: Qué contratos auxiliares quedaron integrados en el borrador OpenAPI, cuáles no y por qué, con hallazgos I-01 a I-11 y evidencia real.
---

# Cierre de brechas contractuales auxiliares

Las [notas del contrato](notas-contractuales.md) dejaban fuera operaciones que el inventario de
L3 §11 omite. Este paquete integra en el [borrador OpenAPI](libox_openapi_L3_V8_DRAFT.yaml) las
que se pueden cerrar sin decisiones de dominio pendientes. El resto queda delimitado. Fuentes:
[L3 V7](../../../linea-base/LIBOX_ESPECIFICACION_TECNICA_L3_V7.md) §2–4, §7, §10–11 y
[PRD V9](../../../linea-base/LIBOX_PRD_BLUEPRINT_MVP_V9.md) §2.6, §7, §8 y §27.3.
Es un borrador: no cambia el canon.

| Nota | Contenido |
|---|---|
| [Lecturas y configuración](cierre-contratos-lecturas-configuracion.md) | 9 GET versionados integrados; T1–T8 y `market_config` solo como diseño |
| [Decisiones privilegiadas](cierre-contratos-decisiones.md) | Valoración, gate legal, moderación y segunda firma integrados; P-C pendiente |
| [Identidad y evidencias](cierre-contratos-identidad-evidencias.md) | MFA, recuperación y subidas integrados; KYC/KYB pendiente de proveedor |

## Estado del YAML

- **Operaciones.** 92 en total.
  - 61 llevan `x-origin: l3-inventory`. Son el inventario de L3 §11, que no cambia.
  - 31 llevan `x-origin: c1-auxiliary` y `x-authorization-status: proposed`.
  - `info` declara ambos valores de `x-origin`.
- **PSP.** `receivePspWebhook` declara `x-origin: l3-inventory`; no hay excepción temporal
  en las pruebas. Mercado Pago tiene payload y entradas de firma documentados.
- **Correcciones alineadas al canon:**
  - `RaffleDraft.title` y `RaffleUpdate.title`: máximo 140, como `VARCHAR(140)`.
  - `reason` de `CapabilitiesUpdate` y `MarketConfigUpdate`: mínimo 20, como `feature_toggle_log`.
- **Errores nuevos** en el enum de `Error`: `ERR_AUTH_REAUTH_REQUIRED` y `ERR_EVIDENCE_NOT_ACCEPTED`,
  más siete respuestas de error compuestas con códigos que ya existían.

## Decisiones transversales aplicadas

- **CC-01 Identidad del artefacto.** Base `/api/v2`. `info.version` es `2.0.0-draft.2`.
- **CC-02 Métodos.** GET lee, POST ejecuta comandos o crea recursos, PUT reemplaza.
  `PATCH /raffles/{id}` sigue con `application/json`: no se declara `merge-patch+json` mientras
  las pruebas no lo soporten. La revocación de un factor usa POST porque lleva motivo.
- **CC-03 Versión.** El recurso se lee con `version` y el comando envía `expected_version`. Si no
  coinciden, responde 409 `ERR_RESOURCE_VERSION_CONFLICT`. Sin ETag.
- **CC-04 Identificadores.** Lo público recibe slug. Lo privado recibe UUID.
- **CC-05 Nombres de ruta.** Se normalizaron los parámetros: `{id}` en todos los recursos nuevos,
  `{raffle_ref}` en sorteos y `{code}` en mercados. Los GET nuevos de `payout` y `capabilities` se
  añadieron a los path items que ya existían, no a rutas duplicadas.
- **CC-06 Sin esquemas genéricos ni campos calculados.** Todo objeto nuevo es cerrado.
  Las peticiones no aceptan banda, desviación, comisión ni firmante.
- **CC-07 Acción sensible.** Exige `aal2` y reautenticación reciente; si falta, responde 401
  `ERR_AUTH_REAUTH_REQUIRED`. La ventana de 5 minutos es un supuesto (S-3).
- **CC-08 Segunda firma.** Es un recurso aparte (`SignatureRequest`). La atestación (§11.5)
  conserva por ahora `second_signer_id`. Migrarla cambia un cuerpo que el canon define
  explícitamente y requiere decisión de Diego.

## Integrado frente a pendiente

| Brecha | Integrado en el YAML | Pendiente, con motivo | Dueño |
|---|---|---|---|
| Lecturas versionadas | 9 GET | Resolución de capacidades en tres capas | Diego |
| T1–T8 y `market_config` | — | Enums de costos, T1 (I-09), duración T7 e insumo de precio | Diego; contable sin asignar |
| Aprobaciones | 3 decisiones y 4 operaciones de firma | Rechazos (I-06), etapas P-C (I-02, I-08), política de firmantes (I-04) | Diego; [LEGAL→ABOGADO] |
| MFA y recuperación | 11 operaciones | Adaptador TOTP de Supabase y correo (R1) | Diego |
| Subidas | 4 operaciones | Tipos y tamaños por propósito, antimalware, copia independiente (R1) | Diego |
| KYC/KYB | — | Truora priorizado para evaluar; alcance KYB y rol pendientes (I-07) | Diego |
| PSP | Payload `payment` y entradas de firma Mercado Pago | Sandbox y adaptador real | Diego |

## Evidencia

Pruebas escritas antes de editar el YAML:

- **`scripts/contracts/tests/test_auxiliary_contracts.py`**, nueva. Comprueba:
  - el subconjunto L3 frente a `contratos.md`, que las auxiliares son exactamente las 31 y que
    los IDs son únicos;
  - nombres de parámetros normalizados;
  - que las lecturas devuelven versión;
  - reautenticación, MFA, recuperación genérica y subidas;
  - que las decisiones rechazan firmantes y campos calculados;
  - que los schemas nuevos son cerrados y que los errores están declarados.
- **`test_openapi_draft.py`** limita el conteo de 61 a `l3-inventory` y exige IDs únicos en todo
  el documento.
- **`test_mock_http.py`** recorre todas las operaciones.

**Ejecución local del 2026-09-30:** pasan 29 pruebas de contratos y preservación,
92 intercambios HTTP de fixtures y 11 del cliente TypeScript generado. Se corrigieron
cuatro hashes de ejemplo que YAML interpretaba como números en lugar de cadenas.
El mock no prueba permisos, firma PSP, decisiones ni seguridad del backend.

## Hallazgos del canon (CD-07)

La "propuesta segura" es lo que el borrador ya aplica o puede aplicar sin decidir dominio.
"Requiere aprobación" indica quién debe decidir antes de llevarlo a V8.

| ID | Conflicto | Propuesta segura | Requiere aprobación |
|---|---|---|---|
| I-01 | La banda V2 exige cofirma `ADMIN_MODERATION`, pero §7.1 solo le da R | Cofirma como `SignatureRequest` `VALUATION_V2_COSIGN`; firmar no concede escritura | Diego: fila de cofirma en la matriz V8 |
| I-02 | E1 la aprueba `ADMIN_RISK` y E6 la verifica `SUPPORT_L2`, pero §7.1 da A solo a `ADMIN_LEGAL_COMPLIANCE` | No integrar decisiones de etapa | Diego: matriz por etapa |
| I-03 | El actor de `VALUATION_OBSERVED` es "Verificador", que no es un subrol | `OBSERVED` limitado a los aprobadores de banda | Diego: confirmar o crear subrol |
| I-04 | §7.1 da la segunda firma solo a `ADMIN_SUPER`; INC-09 pide otro subrol | Política por `action_code` como dato; sin política, ninguna firma es elegible (falla cerrado) | Diego: firmantes por acción |
| I-05 | `client_capabilities` lista `T8` y `LIVE` | Se mantiene fuera `LIVE` | Diego: retirar o distinguir |
| I-06 | Sin transición FSM para el rechazo manual de valoración ni para rechazar u observar el gate legal | Solo se exponen resultados con transición | Diego; gate legal [LEGAL→ABOGADO] |
| I-07 | §7.1 no tiene rol para decidir KYB | Sin operación de decisión KYB | Diego |
| I-08 | La lista cerrada de `checklist_key` por etapa (RN-29) no tiene semilla | Sin checklist en `listPcStages`; `submitPcStage` intacto. **Bloquea P-C** | Diego y [LEGAL→ABOGADO] |
| I-09 | `expiry_policy_required` de T1 no tiene campo | Configuración T1–T8 no integrada | Diego |
| I-10 | **Resuelto.** Diego eligió Mercado Pago como PSP (ratificado); coincide con `psp.pe.mercadopago` | — | — |
| I-11 | **Resuelto en el borrador.** Los cuatro estados de recurso se alinean con sus CHECK del SQL canónico; ejemplos y respuestas coherentes | Prueba automática compara vocabularios; no implementa transiciones | No requiere decisión de negocio nueva |

## Supuestos

- **S-1.** El régimen económico queda solo en `PAID`. No aplica mientras T1–T8 no se integre.
- **S-2.** MFA y recuperación pasan por la API de Libox. **Integrado.**
- **S-3.** Ventana de reautenticación de 5 minutos, sin ratificar.
- **S-4.** Se descartó mostrar `allowed_raffle_types` en `GET /clients/{id}` porque contradice §7.1.

## Zonas sin generación asistida

No se generó lógica de dominio. Siguen siendo implementación humana de Diego, según las
[zonas sin IA](../../../../.claude/rules/zonas-sin-ia.md):

- las comprobaciones INC-06, INC-08, INC-09 e INC-11;
- el cálculo de banda, desviación y múltiplo;
- los valores de comisión e impuesto;
- las transiciones que liberan las decisiones.
