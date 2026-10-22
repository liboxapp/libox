---
title: Rev6 — Catálogo de plazos y control de reservas
status: aprobado
tags: [rev6, act-r6-11, g4, contracargos, reservas]
updated: 2026-10-18
description: Estructura y controles aprobados de G4 y RN-104, con valores del PSP pendientes de confirmación.
---

# ACT-R6-11 — Catálogo de plazos y control de reservas

**Estructura y controles aprobados por Diego el 18/10/2026.** Evidencia: «Apruebo,
déjalo documentado en Outline y sigamos con re-sorteo R6-12». El estado aprobado
corresponde a esta definición; valores del PSP, implementación y pruebas siguen
pendientes. La base de trabajo es rev6, cuya aceptación formal y emisión siguen
su proceso. Esta nota no modifica el corpus congelado ni acredita cierre técnico.

## Reglas conservadas

- G4 se cuenta desde el último pago aprobado del sorteo, no desde la entrega.
- La reserva RN-104 tiene su propia ventana desde la acreditación de entrega.
- Ante un plazo faltante, usar el mayor aplicable de un catálogo vigente validado
  con condiciones del proveedor. Sin respaldo suficiente, bloquear y abrir incidencia.
- Los seis gates de liquidación conservan su evaluación automática. El vencimiento
  de una ventana no sustituye los demás requisitos de liberación.

## Estructura aprobada del catálogo

| Grupo | Datos que deben conservarse |
|---|---|
| Aplicación | Mercado, PSP, medio de pago y alcance de la condición respaldada. |
| Plazos | Ventana principal, ventana extendida y unidad de tiempo de cada una. |
| Vigencia | Versión y período en que la condición resulta aplicable. |
| Respaldo | Documento de origen, fecha y referencia verificable del proveedor. |
| Validación | Persona que validó el dato y trazabilidad de la validación. |

La selección debe cubrir los pagos del sorteo. Un valor de otro proveedor o de
una condición que no corresponda no satisface el criterio de «mayor aplicable».
La unidad, el cómputo y el alcance deben ser verificables; no se convierte una
ambigüedad de la condición comercial en un vencimiento permitido.

Se conservan las claves declaradas en L3 V21 §10.1:

| Clave | Función |
|---|---|
| `chargeback_window_days` | Ventana principal de G4, desde el último pago aprobado. |
| `deadlines.chargeback_reserve_days` | Ventana extendida de RN-104, desde la acreditación. |

El catálogo es una definición de trabajo a implementar, no una tabla o servicio
ya existente acreditado. El esquema V20 aún utiliza 120 días fijos ante ausencia
de clave y no impone íntegramente RN-104. **No se aprueba ese sustituto fijo ni
los 400 días usados en una reproducción adversarial como política comercial.**

## Determinación de los vencimientos

**G4:** fecha histórica del último pago aprobado del sorteo más el mayor plazo
principal aplicable a sus pagos. Cambiar después el estado de un pago no debe
borrar su aprobación histórica ni adelantar el vencimiento por ese motivo.
La comprobación de contracargos y disputas abiertos permanece separada del reloj.

**Reserva RN-104, para el MVP:** última acreditación vigente de entrega entre
todos los ganadores del sorteo más el mayor plazo extendido aplicable. Una
entrega temprana no permite liberar la reserva de todos. Si falta acreditación
exigible o deja de estar vigente, no se acredita la condición de entrega para
liberar; debe reevaluarse el vínculo y la condición aplicable.

Los vencimientos deben poder reconstruirse con las fechas de origen, parámetros
y versiones usados. Si no puede comprobarse un plazo válido, aplicar bloqueo e
incidencia; no sustituir el anclaje de una ventana por el de la otra.

## Objeto de control de la reserva

| Dato o vínculo | Qué permite comprobar |
|---|---|
| Sorteo | Qué recaudación y qué conjunto de ganadores respaldan la reserva. |
| Importe y moneda | Cuánto se retuvo y qué saldo queda por liberar. |
| Asiento T-07 | Evidencia contable de la constitución de la reserva. |
| Acreditaciones de entrega | Identidades, vigencia y fecha que determina el anclaje. |
| Versión del catálogo | Condiciones y respaldo usados para determinar el plazo. |
| Vencimiento | Momento a partir del cual puede evaluarse su liberación. |
| Liberación T-09 y traza | Cuánto se liberó, cuándo y con qué comprobaciones. |

El control debe impedir liberar anticipadamente, duplicar T-09 o liberar más de
lo efectivamente retenido y pendiente. T-09 devuelve la reserva al pasivo con el
organizador; no equivale por sí sola al pago T-08.

## Comprobación antes de liberar y cambios del catálogo

Antes de liberar, volver a comprobar plazo, saldo y condiciones correspondientes,
incluida la ausencia de contracargos o disputas abiertos. Para el pago T-08 se
mantienen G1…G6. Una lectura anterior favorable no autoriza liberar cuando un
nuevo hecho haya vuelto a bloquear la operación.

Conservar la configuración aplicada y su trazabilidad. Una versión nueva no
acorta automáticamente una retención calculada. Una corrección pertinente que
pueda afectar su seguridad exige revisión y recálculo registrado. Esto no autoriza
editar silenciosamente la configuración congelada del sorteo ni cambiar su comisión.

Mercado Pago documenta que el importe disputado permanece retenido durante la
resolución. Esa documentación respalda distinguir vencimiento y caso abierto;
no confirma los plazos ni la aceptación comercial del modelo LIBOX.

## Responsabilidad y pendientes explícitos

Diego coordina el catálogo y las incidencias técnicas. Las condiciones del PSP
proceden de la gestión comercial ya registrada en ACT-R6-03. Horario y escalamiento
se concretarán en ACT-R6-15; esta definición no fija una guardia personal permanente.

Quedan por confirmar los días concretos, el porcentaje y base de cálculo de la
reserva, las condiciones aplicables y su respaldo/validación con el proveedor.
Ejecutor de desarrollo y fechas por designar. T-09 y los controles de dinero o
concurrencia conservan la propiedad humana de Diego y las restricciones del repo.

Implementación y verificaciones se ejecutarán durante desarrollo: ausencia de
parámetros; pagos con condiciones distintas; cambio de estado del último pago;
varios ganadores; acreditación revocada; disputa abierta; límite temporal; versiones
del catálogo; saldo insuficiente y repetición de T-09. RN-103/RN-104 y los dos casos
HUECO de R-17 siguen abiertos hasta la evidencia de su corrección.

## Fuentes

- [Ficha de Diego](https://liboxapp.getoutline.com/doc/diego-pendientes-y-decisiones-tecnicas-rev6-dET6AASY9e) y [tablero](https://liboxapp.getoutline.com/doc/21-tablero-de-acciones-tasks-iCoCY5qOjR): aprobaciones y seguimiento de ACT-R6-11.
- [PRD V22](https://liboxapp.getoutline.com/doc/libox-prd-blueprint-mvp-v22-wp9CiWihnf), §15.1 y RN-63/103/104; [L3 V21](https://liboxapp.getoutline.com/doc/libox-especificacion-tecnica-l3-v21-yC2vKLLNbN), §6.2, §6.3 y §10.1.
- [Registro V24](https://liboxapp.getoutline.com/doc/libox-registro-maestro-de-linea-base-v24-TBDcjlR1hE), H22-04/05 y estado efectivo de RN-103/RN-104.
- [Mercado Pago, introducción a contracargos](https://www.mercadopago.com.pe/developers/es/docs/checkout-api-orders/payment-management/chargebacks/introduction?scope=prod): retención durante la resolución; consulta del 18/10/2026.
