---
title: C1 — decisión de Diego del 28 de octubre
status: aprobado
tags: [r0, c1, decisiones, l3, openapi, numeracion]
updated: 2026-10-28
description: Numeración de rev6, fusión de C1 en L3 V22 con OpenAPI 2.0 como base, frontera Trigger.dev/worker Go, eliminación de settlement_hold_days y subcasos de H22-10.
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

## Frontera entre Trigger.dev y el worker Go

Respuesta de Diego del mismo día. Completa el punto 2 del 04/10 («conservar
Trigger.dev y evaluarlo en los primeros meses») y HOST-05 de la
[aceptación técnica Go](aceptacion-tecnica-go.md). No consta una decisión
posterior de Adrián; rev6 nunca incluyó Trigger.dev.

- **El worker Go ejecuta todo trabajo crítico:** dinero, sorteo, liquidación,
  reservas y retenciones, outbox y conciliación diaria (R6-15). El trabajo
  pendiente vive en PostgreSQL (`scheduled_jobs`, RN-266) y la ejecución única
  por sorteo la garantiza el worker. **El sistema funciona completo sin
  Trigger.dev.**
- **Trigger.dev queda para trabajos no críticos:** correos, notificaciones,
  reportes y limpieza. Invoca operaciones de Go, no contiene lógica de dominio
  ni estado propio y se puede retirar sin tocar el núcleo.
- Se evalúa en los primeros meses con funcionalidad, fiabilidad, carga de
  mantenimiento y coste, dentro del techo de US$250/mes.

## `settlement_hold_days` se elimina (C-14)

Respuesta de Diego del mismo día. La clave `deadlines.settlement_hold_days: 7`
de L3 V21 §10.1 era la ventana contada desde la atestación de la lectura de
RN-103 derogada el 13/10 (opción C). No la lee el esquema V20 ni ningún gate
(Registro V24, H22-04). No consta decisión posterior de Adrián.

- **Se elimina de L3 §10.1 en V22.**
- Las ventanas de liquidación y de reserva salen solo del catálogo de
  [R6-11](../../../desarrollo/r611-catalogo-plazos-reservas.md): G4 desde el último pago
  aprobado y la reserva de RN-104 desde la última acreditación vigente de
  todos los ganadores.
- Cierra la parte de H22-04 que correspondía a Diego. El plazo concreto del
  catálogo sigue pendiente de las condiciones del PSP (ACT-R6-03).

## Subcasos de H22-10

Respuestas de Diego del mismo día a lo que los seis cierres del 13/10 no
cubrían (Registro V24 §5.2, «decisión de Diego por cada uno»). Huecos
verificados en el esquema V20. No consta decisión posterior de Adrián. La
separación de firmantes y adjudicadores en todas las salas y ambos órdenes
(INC-08) ya se decidió el 18/10 en R6-14.

| Regla | Definición para L3 V22 |
|---|---|
| RN-147 | `orders.quantity` es inmutable tras crear la orden; cambiarla exige otra orden |
| RN-147 | El contrato exige reintentar la transacción completa ante un fallo de serialización (40001) |
| RN-147 | `max_concentration_bp` se copia de `concentration.max_bp` de la configuración congelada al publicar y queda inmutable |
| RN-147 | **El límite se aplica por persona natural verificada**, sumando sus cuentas; sin identidad verificada, por cuenta |
| INV-25 | La renuncia se vincula a la versión vigente del documento de renuncia (módulo legal) |
| INV-25 | `signed_at` es sello del servidor: lo fija la base y descarta el valor que envíe la aplicación |
| INV-25 | **La inelegibilidad se acredita con un expediente de cumplimiento de causa tipificada** (AML, edad, residencia, incompatibilidad u otra catalogada), no solo con `aml_cases` |
| INV-01 | `published_at` es inmutable una vez fijado |
| INV-36 | Cada línea respeta el debe y el haber de su `transaction_types` |
| INV-36 | **La base calcula el IGV** desde la tasa de la configuración congelada y rechaza el asiento que no cuadre, con una regla de redondeo explícita en L3 V22 |

- La regla de redondeo y el emisor del comprobante quedan sujetos a L-05 y a la
  validación del contador. [LEGAL→ABOGADO]
- El límite por persona depende de la verificación de identidad (Truora en
  evaluación); sin ella rige el límite por cuenta.
- Estas cuatro reglas están en la excepción de zona del 13/10: Claude puede
  redactar su código y Diego confirma cada cambio. El cierre exige que la
  refutación imprima NO REPRODUCIDO y la batería siga verde en PostgreSQL 16 y 17.

## Qué queda pendiente

- Al promover el paquete al repo, el Registro V25 debe dejar constancia de que
  las versiones intermedias se emitieron en la línea de Cowork. La regla
  `V<n>` → `V<n+1>` de `.claude/rules/linea-base.md` no contempla ese salto;
  su texto requiere un cambio autorizado del OS (`LIBOX_EDITAR_OS=1`).
- Los documentos del programa R0 y de C1 que nombran «L3 V8» se conservan como
  historia; las referencias de puntero se actualizan a esta decisión.
