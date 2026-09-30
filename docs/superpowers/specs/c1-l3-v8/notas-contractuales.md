---
title: C1 — decisiones y verificación del contrato API
author: Diego Cotrina
status: borrador
tags: [r0, c1, openapi, typescript]
updated: 2026-09-30
description: Alcance de las 92 operaciones, cambios frente a V7 y pruebas reproducibles sin backend de dominio.
---

# Contrato API de C1

El [YAML](libox_openapi_L3_V8_DRAFT.yaml) es un borrador completo respecto al
[inventario de 61 operaciones](contratos.md), no una API desplegable ni una emisión
canónica. Conserva las 57 rutas del inventario y añade rutas auxiliares: se comparten los métodos del mismo recurso y se
normalizan `/raffles/{slug}` y `/raffles/{id}` como `/raffles/{raffle_ref}`.
GET recibe slug; las mutaciones reciben UUID. Los métodos omitidos en L3 §11.7
se concretan según la acción: consultas GET, comandos POST y reemplazos PUT.

La versión `2.0.0-draft.2` incluye **92 operaciones**: 61 del inventario y 31
auxiliares. `x-origin` separa ambos conjuntos; ver [cierre auxiliar](cierre-contratos.md).
Los ejemplos no prueban autenticación, autorización ni decisiones de negocio.

## Decisiones y compatibilidad

- Diego ratificó el 2026-09-30 `Money.amount` como cadena decimal de unidad mínima
  con moneda: `{"amount":"2500","currency":"PEN"}` representa S/25.00.
  El esquema acepta 0..9223372036854775807 y rechaza signos, ceros iniciales,
  fracciones, números JSON y desbordamientos. La validación no calcula dinero.
- El cambio es incompatible con V7. Se propone versión `2.0.0-draft.2` y base
  `/api/v2`; C2 debe emitir y registrar esta identidad. No reemplazar `/api/v1`
  silenciosamente ni presentar el borrador como norma vigente.
- Los roles usan nombres completos, como `USER_VERIFIED`; los permisos proceden
  de L3 §7.1. Las decisiones nuevas o con alcance inferido se marcan
  `x-authorization-status: proposed`. Esa marca impide considerarlas ratificadas.
- `x-authorization` describe pertenencia al recurso, estado y separación de
  funciones; la lista de roles no basta. El contrato no implementa esos controles.
  Atestación excluye finanzas y ejecución de liquidación es exclusiva de finanzas.
- Los comandos de sorteo requieren identidad de servicio separada del usuario;
  no reciben ganadores, seed ni pool elegidos por quien llama. La política de
  re-sorteo y sus causales sigue pendiente de cerrar con el dueño del motor.
- Mutaciones patrimoniales llevan `Idempotency-Key`; el cliente no decide gates,
  precio calculado de orden, fecha efectiva de límites ni estado de pago.
  Toda respuesta lleva trazabilidad; las privadas requieren `Cache-Control: no-store`.
- Registro responde de forma genérica para evitar enumeración. Identidad/KYB
  usan referencias a sesiones del proveedor vinculadas por el servidor, no DNI
  ni documentos crudos en respuestas. Tokens de fixtures son sintéticos.

## Dependencias que no cierra este artefacto

| Dependencia | Trabajo pendiente antes de habilitarla |
|---|---|
| PSP | Mercado Pago elegido; `PspNotification` ya tipa `payment` y entradas de firma. Faltan fixtures firmados y ensayos de timestamp, consulta autenticada y duplicados en sandbox; ver [PSP](mercado-pago.md) |
| KYC/KYB y objetos | Cerrar creación de sesiones/capturas, subida privada, cuarentena y comprobación de pertenencia de referencias con adaptador elegido |
| MFA | Contratos auxiliares integrados; falta adaptador TOTP de Supabase y prueba real. `aal1` no habilita rutas internas |
| Sorteo público | Cerrar H-10/H-11/H-12: baliza, codificación canónica, snapshot y valores independientes. Los ejemplos son deliberadamente sintéticos, no pruebas criptográficas |
| Valoración y etapas | Los comandos propuestos presentan evidencias; no suplantan la aprobación del valuador/legal. Cerrar contrato de decisión privilegiada y completar campos de configuración por tipo antes de D1 |
| Dinero y conciliación | T-03, ASS-001 y política contable siguen abiertos. Los ejemplos de liquidación/simulador no acreditan fórmulas, asientos ni PSP reales |
| Lecturas de versión | Nueve lecturas auxiliares integradas con `version`; comandos usan `expected_version` y conflicto 409. I-11 alineado con estados del canon; falta comprobar autorización contra backend |
| Permisos y estados | Reconciliar propuestas con FSM y flujo completo del producto; verificar aislamiento por cliente, firmas e incompatibilidades con el backend real |

El conteo de 61 mide cobertura del inventario L3 §11, no suficiencia funcional de
toda la aplicación: dicho inventario omite operaciones auxiliares de proveedores
y configuración. No marcar H-13 cerrado por alcanzar el conteo.
La suspensión de revisión humana del repositorio no elimina las segundas firmas
ni las incompatibilidades del producto.

## Verificación reproducible

Herramientas aisladas en `scripts/contracts/`, sin cambios en `src/` ni en el
paquete raíz. Dependencias Python fijadas; herramientas TypeScript con lockfile.

```sh
python3 -m venv /tmp/libox-contracts
/tmp/libox-contracts/bin/pip install -r scripts/contracts/requirements.txt
/tmp/libox-contracts/bin/python -m unittest discover -s scripts/contracts/tests -v
npm ci --prefix scripts/contracts/typescript --ignore-scripts --no-audit --no-fund
/tmp/libox-contracts/bin/python scripts/contracts/check_typescript.py
```

Las pruebas comprueban estructura 3.1, referencias, rutas sin ambigüedad, ejemplos
de éxito/error, límites monetarios, entradas inválidas y campos calculados no
aceptados del cliente. Recorren las 92 operaciones por HTTP sobre un mock ligado
solo a `127.0.0.1`; el cliente TypeScript realiza once intercambios con tipos generados, incluido lectura → comando
con la versión recibida.
También se comprueba en compilación que `Money.amount` no acepte `number`.

La prueba HTTP envía parámetros de ruta/query/cabecera conformes al esquema.
El mock devuelve fixtures, valida solo el cuerpo y **no valida parámetros, permisos, firma
PSP, cabeceras de seguridad ni reglas de negocio**. No usar como backend ni como
prueba de seguridad. Las extensiones `x-*` son requisitos documentales: un
validador OpenAPI no demuestra que se cumplan. CI los verifica estructuralmente
en `test (3.9)` y `test (3.12)`; el cliente se comprueba en el segundo.

Fuentes de herramientas: [OpenAPI 3.1](https://spec.openapis.org/oas/v3.1.0.html)
y [generación de tipos](https://openapi-ts.dev/cli). La validación no modifica ni
emite la línea base; existe el [candidato completo de L3](LIBOX_ESPECIFICACION_TECNICA_L3_V8_DRAFT.md),
con aportes críticos y decisiones aún pendientes.
