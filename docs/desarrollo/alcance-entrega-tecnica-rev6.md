---
title: Rev6 — Alcance y trazabilidad de la entrega técnica
status: vigente
tags: [desarrollo, rev6, act-r6-16, artefactos, pendiente]
updated: 2026-10-18
description: Inclusión del dossier de concurrencia, referencias históricas y caso negativo RN-63 para desarrollo.
---

# ACT-R6-16 — Artefactos y verificación pendientes

Definición documentada el 2026-10-18 por solicitud de Diego. Coordinación técnica:
Diego; ejecutor y fecha de desarrollo por designar. El alcance de la próxima
entrega técnica incluirá el dossier existente de concurrencia como **anexo de
reproducibilidad**, con sus dependencias y evidencias. No se emite ni recompone
ahora el paquete canónico y no se ejecutan pruebas del producto.

## Qué forma parte de la entrega

| Conjunto | Alcance y tratamiento |
|---|---|
| Paquete integrado rev6 existente | Esquema V20, tests V20, refutaciones V20, OpenAPI V17 y controles documentales. Conservar bytes y versiones. |
| Anexo técnico existente | `VERIFICACION_TECNICA_REV6`: README, `reproducir.py`, `run_pg.py`, arnés RN-147 y resultados. Incorporarlo completo, separado del corpus normativo. |
| Manifiesto | Ruta/origen, tamaño, SHA-256 y condición del artefacto. Ver [manifiesto técnico](manifiesto-artefactos-tecnicos-rev6.json). Una huella acredita identidad del archivo, no corrección funcional. |
| Evidencia histórica | Conservar ejecuciones originales y reproducción posterior separadas. No sobrescribirlas con una ejecución nueva. |
| Nueva emisión formal | Incorporación al Registro/BASELINE y comprobaciones de emisión cuando se tramite la versión correspondiente. La inclusión en este plan no modifica el canon vigente. |

Hay dos arneses RN-147 recuperados con huellas distintas. El anexo seleccionado
es el de `VERIFICACION_TECNICA_REV6`, preparado para recibir rutas explícitas
mediante `reproducir.py`; el de `tests-stage` queda como antecedente. No mezclarlos.
El dossier existente registra 400 resultados OK por PG16/17, 22 casos HUECO en
13 reglas y concurrencia con dos conexiones en **READ COMMITTED**. Esta nota no
repite esas ejecuciones ni extiende el resultado a REPEATABLE READ o SERIALIZABLE.

## Referencias históricas — H22-12

| Referencia anterior | Resolución para la entrega |
|---|---|
| Seis `diff_<regla>.sql` ratificados | Los cambios ya están embebidos en el esquema, delimitados por bloques V18. No se localizaron sus seis archivos independientes en la búsqueda de esta revisión. Registrar la correspondencia; no reconstruirlos ni afirmar que se entregan. |
| INV-01, INV-36, RN-45, RN-96, RN-147, INV-25 | Son las seis reglas de los bloques humanos ratificados. No equivalen a las trece reglas con HUECO actuales ni cubren automáticamente los subcasos restantes H22-10. |
| Arnés citado pero ausente del paquete integrado | Incluir el dossier recuperado como anexo técnico; el manifiesto identifica la copia concreta y sus dependencias. |
| Comentarios con versiones previas, INV-25 HUECO o rótulo R-12 desactualizado | Mantener el SQL ratificado intacto y añadir esta tabla de correspondencias al dossier. Corregir el texto normativo en una futura emisión si corresponde. |
| Estado vigente de las reproducciones | Usar el estado efectivo del Registro V24 y las salidas finales: RN-89 parcial; RN-179 cubierto; RN-103/104 siguen con HUECO. |

No se declara H22-12 técnicamente cerrado hasta que el manifiesto y el anexo
formen parte de la entrega concreta y sus referencias se comprueben al emitirla.

## Caso negativo pendiente — H22-09 / RN-63

**IT-R616-01 — PENDIENTE para desarrollo.** Preparar un escenario contractual
válido donde las demás compuertas estén satisfechas y G4 esté abierto; abrir un
contracargo pertinente y comprobar que G4 se cierre. Intentar la liberación y
demostrar que se rechaza por el contracargo, sin movimiento contable parcial.
Conservar identidad del evento, estado antes/después, causa, `trace_id`, fixture,
versión/commit, entorno, ejecutor, fecha y evidencia. El escenario deberá respetar
el catálogo/ventanas de ACT-R6-11; no inventar plazos adversariales como política.

C01 de la batería anterior verifica derivación/ventana; no demuestra este caso
negativo. Los 400 OK históricos no cierran H22-09. Las correcciones o fixtures
ejecutables que afecten asientos, concurrencia u otras zonas protegidas mantienen
la propiedad humana de Diego y la [restricción de generación](../../.claude/rules/zonas-sin-ia.md).

## Criterio de cierre posterior

1. Asignar ejecución y preparar entorno/fixtures en desarrollo.
2. Registrar IT-R616-01 con resultado y evidencia de su causa, sin ejecución ahora.
3. Entregar anexo íntegro, manifiesto verificable y correspondencias históricas.
4. Validar identidad de archivos y coherencia de referencias en la entrega real.
5. Tramitar la emisión correspondiente y actualizar H22-09/12 sólo con evidencia.

Fuentes: [Registro V24](https://liboxapp.getoutline.com/doc/libox-registro-maestro-de-linea-base-v24-TBDcjlR1hE),
H22-09/10/12; README y resultados del dossier técnico existente;
[plan de correcciones](plan-correcciones-rev6.md) y
[tablero](https://liboxapp.getoutline.com/doc/21-tablero-de-acciones-tasks-iCoCY5qOjR).
