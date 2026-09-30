---
title: C1 — Mercado Pago como PSP elegido
status: borrador
tags: [r0, c1, psp, mercado-pago]
updated: 2026-09-30
description: Elección ratificada, contrato de notificación payment y evidencia pendiente del adaptador.
---

# Mercado Pago

**Decisión de Diego, 2026-09-30:** Mercado Pago será el PSP. Acceso a sandbox aún
sin confirmar. No se han contratado servicios, creado cuentas ni usado credenciales.
La propuesta de producto es Checkout Pro, consistente con `preference_id` del
corpus; elegir PSP no confirma automáticamente modalidad de cobro, tarifas ni custodia.
[Checkout Pro](https://www.mercadopago.com.pe/developers/es/docs/checkout-pro-preferences/overview).

## Contrato de notificación

El [OpenAPI candidato](libox_openapi_L3_V8_DRAFT.yaml) concreta
`POST /api/v2/webhooks/psp/mercadopago` para el tópico `payment`:

- `id` del evento es entero JSON nativo del PSP; `data.id` del recurso es cadena.
- `live_mode`, `date_created`, `user_id`, `api_version` y `action` conservan sus tipos
  publicados. Se toleran campos externos adicionales, sin convertirlos en autoridad.
- Firma `x-signature`: componentes `ts` y `v1`; HMAC-SHA256 del manifiesto con
  `data.id` del query, `x-request-id` y timestamp. No se firma todo el cuerpo.
- Se consulta el pago mediante la API autenticada; la notificación sola no acredita
  su resultado. Mercado Pago espera 200/201 en 22 s y reintenta si falta confirmación.

Fuentes: [esquema oficial](https://github.com/mercadopago/openapi/blob/main/schemas/webhooks.yaml)
y [Webhooks](https://www.mercadopago.com.pe/developers/en/docs/subscriptions/additional-content/your-integrations/notifications/webhooks).
El contrato modela el header como `apiKey` solo por OpenAPI: no es una clave estática.

## Requisitos propuestos del adaptador de Libox

1. Comprobar firma con las entradas exactas de Mercado Pago y normalización oficial;
   exigir coherencia del identificador del query y del cuerpo. No usar `body.id`
   como sustituto de `data.id`. No aceptar parámetros duplicados ambiguos.
2. Preservar precisión de IDs numéricos externos al parsear TypeScript; no aplicar
   aritmética monetaria binaria a importes devueltos por el PSP. La API de Libox
   conserva `Money.amount` como cadena en unidad mínima.
3. Confirmar cuenta/aplicación receptora y separación test/live; consultar por un
   endpoint fijo de Mercado Pago, nunca una URL enviada por el callback.
4. Contrastar referencia de orden, moneda e importe con datos del servidor. El
   redirect del navegador y el cuerpo del callback no emiten boletos por sí solos.
5. Persistir recepción e identidad estable del evento antes de responder 200;
   duplicado válido devuelve 200. Fallo de persistencia devuelve 503. Procesamiento
   posterior recuperable; la ejecución única pertenece a la zona humana de concurrencia.
6. Definir política de timestamp/replay con reentrega real de sandbox: no imponer
   una ventana arbitraria que descarte pagos legítimos retrasados. Firma y consulta
   autenticada no sustituyen la idempotencia patrimonial.
7. Conciliar y recuperar notificaciones faltantes, cambios posteriores y pagos
   tardíos conforme F7. Contracargos y otros tópicos requieren contrato separado;
   el esquema `payment` no los cubre automáticamente.

Son criterios de diseño; el mock no ejecuta firma, pagos, deduplicación ni conciliación.
No se han inventado callbacks firmados ni resultados de pruebas PSP.
El receptor propuesto exige `x-request-id` y acepta solo `payment`: configurar
únicamente ese tópico en su URL. Antes de habilitarlo, confirmar el header con
sandbox; si el PSP entrega una variante legítima sin él, ajustar el manifiesto
y el contrato. Otros tópicos requieren recepción y contrato separados, no
configurarlos aquí para generar reintentos permanentes.

## Evidencia pendiente

| Evidencia | Responsable y momento |
|---|---|
| Confirmar cuenta de pruebas y modalidad Checkout | Diego; antes del ensayo del adaptador |
| Payloads sanitizados y firma válida/inválida; query discordante; separación test/live | Integración D1/R1, antes de habilitar recepción real |
| Duplicados, entrega tardía y fuera de orden; caída entre persistencia y ACK | Dueño humano de concurrencia; pruebas de integración R1 |
| Aprobado, rechazado, pendiente, devolución total/parcial y conciliación | Integración PSP/finanzas; no simular dinero real |
| Aceptación comercial del negocio y condiciones de cuenta | Diego con proveedor; antes de producción |
| Custodia, liberación y devolución bajo ASS-001 | Diego y asesoría `[LEGAL→ABOGADO]` |

Mercado Pago publica información técnica para la industria
[gambling](https://www.mercadopago.com.pe/developers/es/docs/checkout-api-payments/how-tos/improve-payment-approval/industry-data/gambling).
Esa página no demuestra aceptación comercial de Libox ni autorización legal de sus
sorteos. Tampoco permite afirmar que estén prohibidos. Confirmar el caso concreto.
El PSP elegido no cierra ASS-001 ni la política contable T-03.
