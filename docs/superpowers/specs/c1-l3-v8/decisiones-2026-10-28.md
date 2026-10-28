---
title: C1 — decisión de Diego del 28 de octubre
status: aprobado
tags: [r0, c1, decisiones, l3, openapi, numeracion]
updated: 2026-10-28
description: La numeración de rev6 rige; la próxima L3 es V22 y fusiona el borrador C1; el OpenAPI 2.0 de C1 es la base del contrato.
---

# Decisión del 28 de octubre de 2026

Origen: respuestas de Diego del 2026-10-28 al conciliar la contradicción C-12
del inventario de documentación: dos líneas de L3 con numeración incompatible.

## Hechos que la motivan

- El repo prepara un «L3 V8» (borrador C1) sobre el canon L3 V7.
- La línea de Adrián ya emitió su propia L3 V8 y siguió hasta L3 V21, PRD V22
  y Registro V24 (paquete rev6). El nombre «L3 V8» designa ya otro documento.
- Las dos líneas se complementan. rev6 cubre dominio, reglas, ledger y el
  esquema V20 con su batería. C1 cubre proveedores, Supabase Auth y KMS,
  Mercado Pago, Truora, sesiones y F1–F7, y un OpenAPI de 93 operaciones frente
  a las 37 de rev6.
- No consta una decisión de Adrián sobre la reconciliación de las líneas.

## Qué se decide

1. **Rige la numeración de rev6** para todo el corpus. La próxima emisión
   conjunta es PRD V23, L3 V22, Matriz V11 y Registro V25.
2. **L3 V22 parte de L3 V21 y fusiona el contenido único del borrador C1** en
   sus secciones: pila (§0.3), operación (§12–14), seguridad y sesiones.
3. **El nombre «L3 V8» del repo se retira.** El
   [borrador](LIBOX_ESPECIFICACION_TECNICA_L3_V8_DRAFT.md) queda como insumo.
4. **El OpenAPI 2.0.0-draft.3 de C1 es la base del contrato.** Se le añade lo
   que solo esté en OpenAPI V17 y lo decidido después (re-sorteo, T-22,
   revocación), y se emite como OpenAPI V18.
5. **El gate de D1 pasa a ser** la emisión conjunta (L3 V22 y documentos
   asociados) y el acta de aceptación (ACT-R6-01), en lugar de «emitir L3 V8».

## Qué queda pendiente

- Al promover el paquete al repo, el Registro V25 debe dejar constancia de que
  las versiones intermedias se emitieron en la línea de Cowork. La regla
  `V<n>` → `V<n+1>` de `.claude/rules/linea-base.md` no contempla ese salto;
  su texto requiere un cambio autorizado del OS (`LIBOX_EDITAR_OS=1`).
- Los documentos del programa R0 y de C1 que nombran «L3 V8» se conservan como
  historia; las referencias de puntero se actualizan a esta decisión.
