---
title: C1 — decisiones técnicas del 4 de octubre (semilla, privilegios y ledger)
status: aprobado
tags: [r0, c1, decisiones, go, semilla, privilegios, ledger]
updated: 2026-10-12
description: D-14 custodia de la semilla, D-16 privilegios administrativos y D-17 cierres del ledger aprobados por Diego el 04/10; complementa el registro de doce puntos del mismo día.
---

# Decisiones técnicas del 4 de octubre de 2026

Origen: respuestas explícitas de Diego del 2026-10-04, tras analizar
`LIBOX_CICLO_DE_VIDA_Y_DECISIONES_V1.docx` de Cowork station. Diego autorizó
trasladarlas a la especificación y a sus criterios de aceptación. Los IDs D-14,
D-16, D-17, D-18, D-19 y D-22 pertenecen a ese documento de ciclo de vida; son
distintos de las decisiones D-01–D-10 del [programa R0](../2026-09-25-habilitar-r0-design.md).

El registro se escribió en trabajo local paralelo a `main` y se rescató el
2026-10-12 por instrucción de Diego, adaptado a las decisiones posteriores.
Aprueba enfoques: no declara completado C1, emitido el canon ni implementados
los controles. Los casos exigidos están en [aceptación técnica Go](aceptacion-tecnica-go.md).

## Relación con otros registros

Complementa las [decisiones del 04/10](decisiones-2026-10-04.md), que registran
la lista de doce puntos de Codex del mismo día; ninguna de las dos sustituye a la otra.

| ID de origen | Tema | Dónde está en `main` |
|---|---|---|
| D-14 | Persistencia y custodia de la semilla | Este registro |
| D-16 | Privilegios administrativos | Este registro |
| D-17 | Cierres del libro contable | Este registro |
| D-18 | Go como lenguaje del backend; API y worker con módulos compartidos | Ya registrada como D-10 del 2026-10-02: [decisión de stack](../2026-10-02-stack-go-frontend-ts.md) y [adaptación a Go](../2026-10-02-r0-backend-go-design.md) |
| D-19 | Tareas automáticas y alojamiento | Sustituida por las [decisiones del 12/10](decisiones-2026-10-12.md): Render aloja API y worker. Trigger.dev se conserva en evaluación (punto 2 del 04/10) |
| D-22 | Revisión del código | Ya vigente: [revisión humana suspendida](../../../../.claude/rules/revision-humana.md) y [zonas sin generación asistida](../../../../.claude/rules/zonas-sin-ia.md) |

## D-14 — persistencia y custodia de la semilla

Guardar la semilla cifrada en PostgreSQL. Custodiar la clave de cifrado en un
secreto del hosting, separado de PostgreSQL, con acceso limitado al worker y un
procedimiento seguro de recuperación. Persistir ciphertext y versión de clave
antes de publicar el compromiso.

Al reanudar se conservan la misma semilla, compromiso, pool y ronda de baliza.
La falta de clave o una baliza tardía no autoriza sustituirlos. El algoritmo,
serialización y portado del motor siguen bajo su dueño humano.

Esta elección no exige KMS para la semilla en la etapa inicial. Es independiente
del cifrado de datos personales B1-bis con AWS KMS, que conserva su decisión y
pendientes en [datos y cifrado](decisiones-c1-datos.md).

Desde el 12/10 el worker se aloja en Render, de modo que el secreto corresponde
a ese hosting. Su configuración, el acceso exclusivo del worker, la rotación y la
recuperación siguen entre las validaciones de despliegue y secretos del
[registro del 12/10](decisiones-2026-10-12.md#qué-falta-validar-antes-de-habilitar).

## D-16 — privilegios administrativos

Un servicio de dominio en Go concentra permisos, firmas y auditoría de cambios
administrativos. PostgreSQL impone los invariantes dentro de la transacción;
ningún endpoint, worker o acceso directo puede eludirlos.

Conservar las segundas firmas exigidas, la matriz de otorgamiento y las
incompatibilidades. Proteger el mínimo de dos `ADMIN_SUPER` activos (INV-38)
ante revocación, suspensión y borrado, incluidas operaciones simultáneas.
Tratar una reactivación como un nuevo otorgamiento, con los mismos controles.
La implementación de los controles críticos permanece humana.

## D-17 — cierres del libro contable

Registrar por separado el cierre técnico y la validación del modelo por el
contador. El cierre técnico prueba integridad cuenta/moneda y rechazo de asientos
en períodos cerrados contra PostgreSQL real, incluida la carrera entre el cierre
y una inserción, junto con el cuadre e integridad ya exigidos por H-04. El
contador valida el modelo y los hallazgos H-01–H-03.

Ambos cierres son necesarios antes de operar con dinero real. D-05 del programa
R0 sigue permitiendo conservar H-01–H-03 pendientes en C1/C2; esta separación
no adelanta la validación contable al gate documental. ASS-001 sigue abierta.

## Integración y trabajo pendiente

El acuerdo se traslada a §0.9 del [candidato L3](LIBOX_ESPECIFICACION_TECNICA_L3_V8_DRAFT.md),
a las notas de [seguridad](seguridad.md) y [baliza](baliza-propuesta.md), al
[registro CD-07](cambios.md), al [estado C1](estado-c1.md) y a la tarea 7 del
[plan C1](../../plans/2026-09-30-r0-c1.md). Las cinco zonas sin generación
asistida aplican al código: aquí solo hay requisitos en prosa y casos de aceptación.

La emisión canónica, la actualización del doc 20 de Outline y el levantamiento
del freeze siguen sus actos posteriores. No se asignan aquí números DEC/CHANGE
globales ni se ratifican parámetros económicos.
