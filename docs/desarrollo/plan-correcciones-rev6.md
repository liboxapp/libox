---
title: Rev6 — Plan de corrección de las trece reglas con hueco
status: vigente
tags: [desarrollo, rev6, act-r6-13, pendiente]
updated: 2026-10-18
description: Inventario de trece reglas, secuencia de corrección y evidencia exigida en desarrollo.
---

# ACT-R6-13 — Plan de correcciones

Definición documentada el 2026-10-18 por solicitud de Diego de completar los tres
pendientes restantes. Es un plan de trabajo; las correcciones y sus pruebas se
ejecutarán durante desarrollo. No registra una nueva ratificación del corpus.

**Coordinación técnica: Diego. Ejecutor y fecha de cada corrección: por designar
al preparar desarrollo.** No se asigna trabajo a un socio por ser accionista.
Diego conserva la propiedad humana de las cinco zonas protegidas. La suspensión
de revisión humana obligatoria sigue vigente; no se exige un segundo revisor.

## Inventario y orden de ejecución

Las salidas finales de PG16/17 registran **22 casos HUECO en 13 reglas**. El orden
organiza dependencias; ningún control pendiente se considera habilitado para operar.
Cada fila debe adquirir ejecutor, estimación y evidencia antes de su cierre técnico.

| Orden | Regla | Casos | Qué se debe corregir | Coordinación y límite |
|---|---|---:|---|---|
| B1.1 | RN-103 | 1 | G4 no puede sustituir un plazo ausente por 120 días fijos. | ACT-R6-11: catálogo validado; sin plazo verificable, bloqueo e incidencia. |
| B1.2 | RN-104 | 1 | T-09 debe respetar el vencimiento propio de la reserva y su ventana extendida. | ACT-R6-11; los asientos quedan en la zona humana de Diego. |
| B1.3 | RN-60 | 2 | Impedir borrar o ignorar un evento FAILED sin la gestión y alarma exigidas. | Coordinar API/worker con ACT-R6-15; no confundir con el control diario RN-48. |
| B2.1 | RN-151 | 3 | Impedir compra/publicación cuando comprador, titular u organizador está congelado. | Control de admisión; comprobar los tres actores. |
| B2.2 | RN-125 | 1 | Rechazar la compra con documento vencido. | Control de admisión. |
| B2.3 | RN-116 | 2 | Exigir prueba de vida para L2 y primera compra según contrato. | Control de identidad; no inventar proveedor ni plazos. |
| B2.4 | INV-27 | 1 | Impedir emitir tickets en el tramo AML sin declaración de origen. | La acumulación concurrente queda bajo propiedad humana de Diego. |
| B2.5 | RN-131 | 2 | Impedir anular tickets del autoexcluido mediante variantes del texto del motivo. | Validar la causa admitida, sin depender de una cadena manipulable. |
| B3.1 | RN-154 | 2 | Exigir revisión, firma y motivo correspondientes a valoración V3/V4. | ACT-R6-14 para incompatibilidades de personas y firmantes. |
| B3.2 | INV-28 | 1 | Impedir publicar al organizador N3 con valoración pendiente. | Después de RN-154; comprobar estado válido de valoración. |
| B3.3 | RN-89 | 1 | Impedir publicar un plazo inicial inferior al mínimo de categoría. | Mantener el cierre parcial del congelamiento posterior. |
| B4.1 | RN-84 | 2 | Exigir cotizaciones y elección más gracia antes de admitir abandono. | Coordinar controversias y re-sorteo con ACT-R6-12. |
| B4.2 | INV-22 | 3 | Rechazar adjudicación sin evidencia válida, con afirmación débil o referencia inexistente. | ACT-R6-14 y detalle operativo de delivery. |

RN-89 sigue parcialmente abierto: el intento de reducir un plazo ya publicado
fue rechazado; el plazo inicial insuficiente conserva su HUECO. **RN-179 está
cubierto y no pertenece a las trece reglas pendientes.** H22-05 cerró la corrección
de la reproducción RN-103/104, no las dos deficiencias que esta demuestra.

## Responsabilidad y evidencia

La clasificación histórica «trece fuera de zona» no autoriza generar código en
zonas protegidas. RN-104 afecta directamente asientos; INV-27 puede afectar
concurrencia; RN-154/INV-22 deben separar la suficiencia de evidencia de las
comprobaciones protegidas de incompatibilidad. La frontera se aplica por conducta.
Consultar [zonas sin IA](../../.claude/rules/zonas-sin-ia.md) y
[revisión humana](../../.claude/rules/revision-humana.md).

Para cada regla se registrará: ejecutor, versión/commit, caso y fixture contractual,
resultado anterior, causa del rechazo o aceptación esperado, resultado posterior
y enlace a evidencia. Verificar también un camino válido: un error ajeno a la
regla no demuestra corrección. Relacionar la misma evidencia con ACT-R6-11/12/14/15
cuando corresponda, sin crear implementaciones duplicadas.

Los seis bloques humanos ratificados INV-01, INV-36, RN-45, RN-96, RN-147 e INV-25
son un inventario distinto. Los subcasos restantes H22-10 conservan seguimiento;
no quedan resueltos por este plan ni por la batería histórica de 400 resultados OK.

## Fuentes y continuidad

- [Tablero de acciones](https://liboxapp.getoutline.com/doc/21-tablero-de-acciones-tasks-iCoCY5qOjR).
- [Registro V24](https://liboxapp.getoutline.com/doc/libox-registro-maestro-de-linea-base-v24-TBDcjlR1hE), estado efectivo, H22-04/05/10 y reproducciones RN-103/104.
- `L3_Artefactos_ejecutables/refutaciones_v20.sql` y salidas finales PG16/17 del dossier rev6.
- [Controles de servicio](controles-servicio-rev6.md) y [alcance de entrega técnica](alcance-entrega-tecnica-rev6.md).

El inventario de archivos y huellas del dossier se conserva en el
[manifiesto técnico](manifiesto-artefactos-tecnicos-rev6.json). No se cambian el
canon, SQL ratificado, código del producto, freeze ni estados de pruebas.
