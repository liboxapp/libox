---
title: Rev6 — Flujos y pruebas pendientes de desarrollo
status: aprobado
tags: [desarrollo, rev6, pruebas, act-r6-10, act-p08, pendiente]
updated: 2026-10-18
description: Criterio ACT-R6-10 y recorridos ACT-P08, con casos unitarios, de integración y de extremo a extremo pendientes.
---

# Rev6 — Flujos y pruebas pendientes de desarrollo

**Fase de ejecución: desarrollo.** Diego aclaró el 2026-10-18 que la revisión
actual se centra en decisiones y documentación. Estos casos quedan en el plan de
desarrollo; su ejecución no se pide ahora ni bloquea el cierre de definiciones.
Se conservan como requisitos futuros de verificación de la implementación.

## ACT-R6-10: importes de órdenes y segunda firma de T-14

**Criterio aprobado por Diego el 2026-10-18. Implementación y pruebas: PENDIENTES.**
El estado `aprobado` corresponde al criterio y a su registro documental; ningún
caso de esta nota está ejecutado ni PASADO. Cubre H22-06 y H22-07.

Diego pidió: «Apruebo este criterio y anotarlo a test unitarios en la documentacion
de nuestro desarrollo para tener pendiente este flujo».

Fuentes operativas: [ficha de decisiones de Diego](https://liboxapp.getoutline.com/doc/diego-pendientes-y-decisiones-tecnicas-rev6-dET6AASY9e)
y [tablero de acciones](https://liboxapp.getoutline.com/doc/21-tablero-de-acciones-tasks-iCoCY5qOjR).
Antecedentes Rev6: PRD V22, RN-01-bis, RN-41, RN-46, INC-09 e INC-11;
L3 V21, §3.9 y matriz RBAC; Registro Maestro V24, H22-06/H22-07.
Esta nota no emite una nueva versión del canon ni acredita el cierre de los hallazgos.

## Criterio y flujo aprobado

1. Al crear una orden, el servidor obtiene la configuración publicada y congelada
   del sorteo y calcula sus importes. Los cambios posteriores del catálogo no
   sustituyen esa referencia; los importes enviados por el cliente no son autoridad.
2. La base de datos comprueba la correspondencia de comisión y neto con esa
   configuración y rechaza cualquier discordancia con error trazable, sin persistir
   la orden inválida ni corregirla silenciosamente.
3. Para un ajuste T-14, se registra el motivo y se verifica que el ejecutor tenga
   `ADMIN_FINANCE` vigente y la segunda firma corresponda a `ADMIN_SUPER` vigente.
4. Las firmas pertenecen a personas naturales distintas y a subroles distintos.
   Dos cuentas de una misma persona no satisfacen la separación. Solo con ambas
   autorizaciones válidas se admite el registro del ajuste.
5. Un rechazo conserva la traza del intento y no deja asientos, líneas ni cambios
   parciales de saldo. La aceptación conserva los importes y las autorizaciones
   comprobados para poder reconstruir la operación.

## Responsabilidad y límites

- **Responsable humano de las zonas protegidas: Diego.** Ejecutor de implementación
  y pruebas, y fecha de ejecución: **por confirmar**.
- La implementación afecta cálculo de comisión, asientos y comprobaciones de
  incompatibilidad. Aplican las [zonas sin generación asistida](../../.claude/rules/zonas-sin-ia.md).
  Esta aprobación documental no autoriza código financiero, migraciones ni tests ejecutables.
- La [suspensión de revisión humana obligatoria](../../.claude/rules/revision-humana.md)
  sigue vigente; la segunda firma de T-14 es un control del producto.
- Los fixtures monetarios se validarán contra el contrato antes de implementar
  las pruebas. Esta nota no fija tasas, fórmulas, redondeos ni conciliaciones nuevas.
- Se conserva el [freeze del scaffold](../../.claude/rules/src-congelado.md).

## Matriz de pruebas unitarias pendientes

Cada caso se ejecutará con las demás condiciones válidas para aislar la causa.
Se verificará el motivo del rechazo y su traza; una excepción ajena no prueba el control.

| ID estable | Caso | Resultado esperado | Estado |
|---|---|---|---|
| UT-R610-01 | Orden con comisión y neto correctos según fixture validado | Acepta la validación; conserva los importes calculados y el desglose contractual. | PENDIENTE |
| UT-R610-02 | Comisión de la orden alterada | Rechaza por discordancia de comisión, con error trazable. | PENDIENTE |
| UT-R610-03 | Neto de la orden alterado | Rechaza por discordancia de neto, con error trazable. | PENDIENTE |
| UT-R610-04 | Catálogo modificado después de publicar el sorteo | Usa el snapshot publicado; obtiene los importes del fixture de esa versión. | PENDIENTE |
| UT-R610-05 | T-14 sin motivo | Rechaza por motivo ausente, con error trazable. | PENDIENTE |
| UT-R610-06 | T-14 sin segunda firma | Rechaza por autorización incompleta, con error trazable. | PENDIENTE |
| UT-R610-07 | Dos cuentas firmantes de la misma persona natural | Rechaza por autofirma aunque los identificadores de cuenta sean distintos. | PENDIENTE |
| UT-R610-08 | Segundo firmante sin `ADMIN_SUPER` vigente | Rechaza por falta de competencia vigente para la segunda firma. | PENDIENTE |
| UT-R610-09 | Ejecutor sin `ADMIN_FINANCE` vigente | Rechaza por falta de competencia vigente para ejecutar el ajuste. | PENDIENTE |
| UT-R610-10 | T-14 con motivo, Finance y Super vigentes, personas distintas | Acepta la validación y conserva motivo, identidades y autorizaciones comprobadas. | PENDIENTE |

## Matriz de pruebas de integración pendientes

**Los unitarios no acreditan que la base de datos imponga el control.**
Las siguientes pruebas requieren integración aislada y evidencia de persistencia.

| ID estable | Caso | Resultado esperado | Estado |
|---|---|---|---|
| IT-R610-01 | Intentar escribir directamente en BD una orden con comisión o neto discordantes | La BD rechaza por la causa prevista, con traza y sin persistir la orden inválida. | PENDIENTE |
| IT-R610-02 | Intentar T-14 inválido por el servicio y directamente en BD | Cada vía rechaza por la causa prevista; no quedan asientos, líneas ni saldos parciales. Cubrir motivo, firmas, identidad y vigencia de los subroles. | PENDIENTE |
| IT-R610-03 | Crear una orden válida y registrar un T-14 válido en integración aislada | Acepta ambas operaciones; al releer, conserva importes de la orden y motivo, importes y autorizaciones del ajuste. | PENDIENTE |

## Evidencia necesaria para cerrar

Registrar por ID: ejecutor, fecha, versión evaluada, entorno, fixture contractual,
resultado observado y referencia al reporte. Los rechazos deben mostrar su causa
y ausencia de persistencia parcial; los caminos válidos deben demostrar aceptación.
Solo después se actualizan los estados y se solicita el cierre de H22-06/H22-07
en el tablero. La aprobación del criterio por sí sola no acredita implementación.

## ACT-P08: pruebas del flujo completo

El [flujo actual](../flujos/flujo-end-to-end.md) vincula actores, hechos, asientos,
gates y excepciones de rev6. Los seis recorridos siguientes son pruebas de extremo
a extremo pendientes; la comprobación documental del flujo no las ejecuta.
Conservar los casos UT-R610/IT-R610 anteriores y relacionar la evidencia compartida.

| ID estable | Caso | Resultado esperado | Estado |
|---|---|---|---|
| E2E-P08-01 | Compra, eventos duplicados/fuera de orden y pago tardío | Una orden coherente, sin duplicar tickets/T-05; tardíos conforme al contrato y sin alterar pool congelado. | PENDIENTE |
| E2E-P08-02 | Condición incumplida, cancelación y elección de devolución | 100% devuelto por ruta elegida; elección visible y vencimiento correctos, sin doble devolución. | PENDIENTE |
| E2E-P08-03 | Multi-ganador, controversia, contracargo, G4 y reserva | Sin comisión parcial; G1–G6 exigidos; plazo sin respaldo bloquea y genera incidencia; T-09 respeta vencimiento propio. | PENDIENTE |
| E2E-P08-04 | Incumplimiento, adquisición y eventual imposibilidad | Obligación y firmas válidas, tope agregado, T-19/proveedor/entrega vinculados; imposibilidad cancela y devuelve íntegramente. Fixtures contables pendientes de H22-01. | PENDIENTE |
| E2E-P08-05 | Re-sorteo permitido, no permitido y rodeo por DISPUTED | Causa probada, ruta/compromiso/permisos/límite válidos; rechaza exclusión del ganador con controversia abierta o incumplimiento del organizador. | PENDIENTE |
| E2E-P08-06 | Participación sin recaudación y régimen promocional | Requisitos, cupo, unicidad y garantías propios; entrega y cierre por conformidad; sin liquidación marketplace. | PENDIENTE |

Ejecutor y fecha por confirmar. Integración PSP sin iniciar y cuenta de pruebas aún
inexistente (ACT-P04); varios controles siguen abiertos en ACT-R6. El cierre real
requiere entorno, fixtures validados, commit, actor, resultado y evidencia por caso.

## ACT-R6-13/15/16: inventario y comprobaciones futuras

El [plan de trece reglas](plan-correcciones-rev6.md) conserva los 22 casos HUECO
y su orden de corrección. El [contrato del servicio](controles-servicio-rev6.md)
registra IT-R615-01…05, todos PENDIENTES; el [alcance de entrega](alcance-entrega-tecnica-rev6.md)
registra IT-R616-01 (RN-63/contracargo/G4), PENDIENTE. No se ejecutaron en esta
revisión. Las 400 verificaciones SQL históricas no acreditan estos controles.

## ACT-R6-11: catálogo, vencimientos y reserva

La [definición aprobada](r611-catalogo-plazos-reservas.md) conserva los casos de
verificación para desarrollo: parámetros ausentes, aprobación histórica del pago,
varios ganadores, vigencia de acreditaciones, disputas, límite temporal, cambios
de versión y liberación T-09 sin duplicación ni exceso. Todos siguen PENDIENTES.
No se ejecutan en esta etapa; los valores del PSP aún requieren confirmación.

## ACT-R6-12: estados y autorización del re-sorteo

La [matriz aprobada](r612-resorteo-estados-permisos.md) amplía E2E-P08-05 con los
dos estados nuevos, permiso de ADMIN_LEGAL_COMPLIANCE y bloqueo antes de ejecutar
si aparece una controversia pertinente después de autorizar. Verificación y
resultados PENDIENTES para desarrollo; H22-03/H22-11 conservan seguimiento.

## ACT-R6-15: operación y privacidad

La [definición aprobada](controles-servicio-rev6.md) conserva IT-R615-01…05 como
PENDIENTES para desarrollo: corte/reporte, bloqueos, reintentos/monitor independiente,
revocación desde la API y trazabilidad sin datos sensibles. Sin ejecución en esta etapa.
