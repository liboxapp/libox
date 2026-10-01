---
title: C1 — cierre de brechas contractuales auxiliares
status: borrador
tags: [r0, c1, openapi, l3-v8]
updated: 2026-10-01
description: Contratos auxiliares y decisiones A/C integrados en el borrador OpenAPI draft.3 (93 operaciones), lo que sigue pendiente y por qué, con hallazgos I-01 a I-11 y evidencia real.
---

# Cierre de brechas contractuales auxiliares

Las [notas del contrato](notas-contractuales.md) dejaban fuera operaciones que el inventario de
L3 §11 omite. Este paquete integra en el [borrador OpenAPI](libox_openapi_L3_V8_DRAFT.yaml) las
que se pueden cerrar sin decisiones de dominio pendientes y, desde draft.3, las
[decisiones A/C](decisiones-c1.md) aprobadas el 30/09. El resto queda delimitado. Fuentes:
[L3 V7](../../../linea-base/LIBOX_ESPECIFICACION_TECNICA_L3_V7.md) §2–4, §7, §10–11 y
[PRD V9](../../../linea-base/LIBOX_PRD_BLUEPRINT_MVP_V9.md) §2.6, §7, §8 y §27.3.
Es un borrador: no cambia el canon.

| Nota | Contenido |
|---|---|
| [Lecturas y configuración](cierre-contratos-lecturas-configuracion.md) | 9 GET versionados; T1, T7, precio, régimen y costos (C1–C4) integrados; T2–T6 y `market_config` solo como diseño |
| [Decisiones privilegiadas](cierre-contratos-decisiones.md) | Valoración, gate legal, moderación con rechazos, KYB y segunda firma por acción integrados; decisión de etapa P-C pendiente de A8 |
| [Identidad y evidencias](cierre-contratos-identidad-evidencias.md) | MFA con ventana de 5 minutos, recuperación y subidas integrados; adaptador KYC/KYB pendiente de proveedor |
| [Aceptación Cowork](reconciliacion-aceptacion.md) | Propuesta no ratificada: mínimo económico, cobertura, fechas y desenlaces **no** contratados en el YAML |

## Estado del YAML

- **Versión** `2.0.0-draft.3`. `info.x-c1-decisions-integrated` lista A1–A7, A9–A11 y C1–C4;
  `info.x-c1-pending` enumera lo que falta y no se anuncia completo.
- **Operaciones.** 93 en total.
  - 61 llevan `x-origin: l3-inventory`. Son el inventario de L3 §11, que no cambia.
  - 32 llevan `x-origin: c1-auxiliary` y `x-authorization-status: proposed`. La única nueva en
    draft.3 es `decideKyb` (A7); el resto de decisiones cambia cuerpos y extensiones existentes.
  - `info` declara ambos valores de `x-origin`.
- **PSP.** `receivePspWebhook` declara `x-origin: l3-inventory`; no hay excepción temporal
  en las pruebas. Mercado Pago tiene payload y entradas de firma documentados.
- **Correcciones alineadas al canon:**
  - `RaffleDraft.title` y `RaffleUpdate.title`: máximo 140, como `VARCHAR(140)`.
  - `reason` de `CapabilitiesUpdate` y `MarketConfigUpdate`: mínimo 20, como `feature_toggle_log`.
- **Errores nuevos** en el enum de `Error`: `ERR_AUTH_REAUTH_REQUIRED` y `ERR_EVIDENCE_NOT_ACCEPTED`,
  más siete respuestas de error compuestas con códigos que ya existían. Draft.3 no añade códigos.
- **`Money`** sin cambios: cadena decimal de unidad mínima; los costos declarados lo reutilizan.

## Decisiones transversales aplicadas

- **CC-01 Identidad del artefacto.** Base `/api/v2`. `info.version` es `2.0.0-draft.3`.
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
- **CC-07 Acción sensible.** Exige `aal2` y reautenticación en los últimos 5 minutos (A10); si
  falta, responde 401 `ERR_AUTH_REAUTH_REQUIRED`. Las nueve operaciones con esa respuesta declaran
  `x-reauthentication-max-age-seconds: 300`. Qué operaciones del inventario L3 son sensibles sigue
  sin decidir.
- **CC-08 Segunda firma.** Es un recurso aparte (`SignatureRequest`) con elegibilidad por
  `action_code` (A1). La atestación (§11.5) ya no lleva `second_signer_id`: en P-C crea la
  solicitud `ATTEST_PC` (A9). `adjudicateDispute` conserva su `second_signer_id`, fuera de A9.

## Integrado frente a pendiente

| Brecha | Integrado en el YAML | Pendiente, con motivo | Dueño |
|---|---|---|---|
| Lecturas versionadas | 9 GET | Resolución de capacidades en tres capas | Diego |
| Configuración | T1 `expiry_policy`, T7 `recurrence`, `ticket_price` del organizador, solo `PAID`, `cost_kind` | Mínimo de T1, premio y aviso; `charge_kind`/`macrozone`; T2–T6 y fechas; `market_config` | Diego; contabilidad y abogado según materia |
| Aprobaciones | 4 decisiones, matriz P-C, política de 11 firmas y 4 operaciones de firma | Decisión de etapa P-C hasta la lista A8 | Diego; [LEGAL→ABOGADO] |
| MFA y recuperación | 11 operaciones; ventana de 5 minutos | Adaptador TOTP de Supabase y correo (R1) | Diego |
| Subidas | 4 operaciones | Tipos y tamaños por propósito, antimalware, copia independiente (R1) | Diego |
| KYC/KYB | `decideKyb` por `ADMIN_COMPLIANCE` (A7) | Truora en evaluación; estados submitKyb alineados, adaptador pendiente | Diego |
| PSP | Payload `payment` y entradas de firma Mercado Pago | Sandbox y adaptador real | Diego |
| Cowork | — | Propuesta no ratificada; no se contrata | Diego, contabilidad y abogado |

## Evidencia

Pruebas escritas antes de editar el YAML:

- **`scripts/contracts/tests/test_auxiliary_contracts.py`**. Comprueba:
  - el subconjunto L3 frente a `contratos.md`, que las auxiliares son exactamente las 32 y que
    los IDs son únicos;
  - nombres de parámetros normalizados;
  - que las lecturas devuelven versión;
  - reautenticación, MFA, recuperación genérica y subidas;
  - que las decisiones rechazan firmantes y campos calculados;
  - que los schemas nuevos son cerrados y que los errores están declarados.
- **`test_c1_decisions.py`**, nueva en draft.3. Lee las tablas A1 y A4 de la
  [ficha de firmas](decisiones-c1-firmas.md) y los CHECK del SQL V7 para comprobar política de
  firma, matriz P-C, estados de destino, resultados KYB, frecuencias T7 y `borne_by`. También
  comprueba que no hay `LIVE`, mínimo de T1 inventado, enum de `macrozone` ni marcas Cowork.
- **`test_openapi_draft.py`** limita el conteo de 61 a `l3-inventory` y exige IDs únicos en todo
  el documento.
- **`test_mock_http.py`** recorre todas las operaciones.

**Ejecución local del 2026-10-01 (draft.3):** el RED previo dio 11 fallos y 13 errores en 46
pruebas. La comprobación adicional de estados de `submitKyb` detectó el enum heredado
incorrecto (RED); corregido, pasan 50 pruebas, con 93 intercambios HTTP y 13 del cliente
TypeScript generado. Catorce mutaciones en memoria del YAML hacen fallar al menos una prueba.
El mock no prueba permisos, firma PSP, decisiones ni seguridad del backend.

## Hallazgos del canon (CD-07)

La "propuesta segura" conserva la resolución de revisión. Draft.3 integra en el YAML las
decisiones A/C del 30/09; la corrección del canon sigue pendiente de la versión V8. No
declara que el flujo Cowork esté contratado.

| ID | Conflicto | Propuesta segura | Estado en draft.3 |
|---|---|---|---|
| I-01 | La banda V2 exige cofirma `ADMIN_MODERATION`, pero §7.1 solo le da R | `SignatureRequest` `VALUATION_V2_COSIGN`; firmar no concede escritura | A2 integrada; fila de §7.1 en V8 |
| I-02 | E1 la aprueba `ADMIN_RISK` y E6 la verifica `SUPPORT_L2`, pero §7.1 da A solo a `ADMIN_LEGAL_COMPLIANCE` | Matriz por etapa | A4 integrada como `x-pc-stage-approvers` [LEGAL→ABOGADO] |
| I-03 | El actor de `VALUATION_OBSERVED` es "Verificador", que no es un subrol | `OBSERVED` limitado a los aprobadores de banda | A3 integrada |
| I-04 | §7.1 da la segunda firma solo a `ADMIN_SUPER`; INC-09 pide otro subrol | Política por `action_code` como dato | A1 integrada como `x-second-signature-policy` |
| I-05 | `client_capabilities` lista `T8` y `LIVE` | Retirar `LIVE`; categorías aparte | A5 integrada: `enabled_categories` |
| I-06 | Sin transición FSM para rechazo manual de valoración ni gate legal | Rutas de rechazo y observación | A6 integrada en `x-outcome-transitions` [LEGAL→ABOGADO] |
| I-07 | §7.1 no tiene rol para decidir KYB | Operación con el rol decidido | A7 integrada: `decideKyb` |
| I-08 | Lista cerrada `checklist_key` por etapa (RN-29) sin semilla | **Bloquea P-C** hasta contar con documentos | Pendiente de Diego y abogado |
| I-09 | `expiry_policy_required` de T1 sin campo | Campo con plazo y desenlace | C1 integrada; mínimo pendiente, T1 no publicable |
| I-10 | **Resuelto.** Diego eligió Mercado Pago como PSP (ratificado); coincide con `psp.pe.mercadopago` | — | — |
| I-11 | **Resuelto en el borrador.** Los cuatro estados de recurso se alinean con sus CHECK del SQL canónico; ejemplos y respuestas coherentes | Prueba automática compara vocabularios; no implementa transiciones | No requiere decisión de negocio nueva |

## Supuestos

- **S-1.** Solo `PAID`, aprobado en C4. **Integrado** en `RaffleDraft` y en la lectura de gestión.
- **S-2.** MFA y recuperación pasan por la API de Libox. **Integrado.**
- **S-3.** Ventana de reautenticación de 5 minutos, aprobada en A10. **Integrado.**
- **S-4.** Se descartó mostrar `allowed_raffle_types` en `GET /clients/{id}` porque contradice §7.1.

## Zonas sin generación asistida

No se generó lógica de dominio. Siguen siendo implementación humana de Diego, según las
[zonas sin IA](../../../../.claude/rules/zonas-sin-ia.md):

- las comprobaciones INC-06, INC-08, INC-09 e INC-11;
- el cálculo de banda, desviación y múltiplo;
- los valores de comisión e impuesto;
- el desenlace patrimonial de T1 al vencer y el reembolso;
- las transiciones que liberan las decisiones.
