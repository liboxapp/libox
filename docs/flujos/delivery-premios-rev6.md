---
title: Rev6 — Delivery de premios y evidencia de entrega
description: Recorrido, modalidades, permisos y verificaciones aprobados de delivery; implementación pendiente.
status: aprobado
tags: [libox, rev6, delivery, evidencia, act-r6-14]
updated: 2026-10-18
---

# Delivery de premios y evidencia

**ACT-R6-14 · Definición operativa aprobada por Diego el 18/10/2026.** Evidencia:
«Apruebo, déjalo documentado en Outline y sigamos con worker y privacidad R6-15».
Amplía los criterios ya aprobados de evidencia y separación de firmantes/adjudicadores.
El recorrido describe el comportamiento objetivo; no acredita implementación,
pantallas terminadas ni cierre de los restantes subcasos de H22-10.

La Sala de Resolución es el expediente. Cada evidencia y acreditación se vincula
con entrega, premio y ganador. El [mapa general](flujo-end-to-end.md) conserva su
cierre documental ACT-P08. El corpus de trabajo rev6 mantiene su proceso de
aceptación/emisión; esta nota no modifica el canon congelado.

## Recorrido aprobado y acciones de las pantallas

| Etapa | Actor y acciones | Condición o resultado |
|---|---|---|
| Reclamar | El ganador acepta el premio y participar en la entrega. | Después se habilita el acceso correspondiente al organizador; no se exponen datos antes del reclamo/consentimiento. |
| Coordinar | Las partes registran modalidad, condiciones y fechas conforme a las bases. | Dirección sólo cuando corresponde y con consentimiento vigente. El acuerdo aporta hechos para las transiciones, no concede a las partes permiso de cambiar estados. |
| Aportar evidencia | Organizador y ganador presentan documentos o hechos. | Conservar origen, aportante, versión y recepción; una carga no acredita automáticamente la entrega. |
| Revisar | El rol competente registra las verificaciones realizadas. | Acreditar, pedir subsanación o escalar según la fuerza y suficiencia de la evidencia. |
| Resolver incidencias | Solicitud de información, subsanación o reclamo estructurado. | Plazos y pausas del contrato; controversia resuelta por persona competente e independiente. |
| Acreditar y cerrar | Identificar ganador y quién cumplió la entrega. | Cierre y trazabilidad de la sala; G2 exige acreditaciones vigentes de todos los ganadores. |

Las pantallas deben ofrecer estas acciones según actor y estado. Su diseño visual
y su implementación siguen en ACT-R6-05/Desarrollo. El cierre de una entrega no
equivale al cierre de todas las entregas ni autoriza por sí solo la liquidación.

## Modalidades y evidencia de cumplimiento

| Modalidad | Recorrido y comprobación |
|---|---|
| Envío físico | Opciones exigidas de transporte; elección/pago cuando corresponda a las bases; seguimiento y constancia de recepción verificable. Se conservan RN-84 y sus plazos. |
| Retiro | Coordinación y acta de entrega vinculada a ambas partes, conforme al catálogo de evidencia aplicable. |
| Servicio o canje | Constancia de prestación o canje con localizador verificable; comprobar el origen y su correspondencia con el premio/ganador. |
| Registrable | Consulta directa de inscripción, aceptación del organizador, confirmación del ganador y doble firma competente. |

**Transición nueva aprobada para servicios y registrables:**
`CLAIMED → AWAITING_DELIVERY` cuando exista un plan de entrega aceptado y registrado.
El sistema comprueba esas condiciones y realiza la transición; no fuerza a estas
modalidades a pasar por estados de envío físico. El plan conserva modalidad,
condiciones, fechas y aceptación trazable. Esta transición debe incorporarse en
L3 y la implementación; no se presenta como existente en el esquema V20.

## Revisión, acreditación y permisos

Organizador y ganador aportan hechos/evidencia; el rol competente y las
transiciones automáticas cambian el estado según las reglas. Se conservan la
asignación del caso y los permisos del contrato: no basta pertenecer al equipo
o consultar una cola de sólo lectura para acreditar una entrega.

| Acto | Competencia |
|---|---|
| Revisión y atestación ordinaria | Rol competente asignado según PRD/L3; la ruta ordinaria usa SUPPORT_L2 y mantiene la supervisión permitida por el contrato. |
| Atestación registrable | `ADMIN_LEGAL_COMPLIANCE` emite la acreditación. SUPPORT no la sustituye. |
| Segunda firma registrable | **Otra persona con `ADMIN_LEGAL_COMPLIANCE` vigente**, según la decisión del 18/10/2026. |
| Subsanación | El revisor competente solicita lo necesario y conserva motivo, aportaciones y plazos aplicables. |
| Adjudicación de controversia | `ADMIN_LEGAL_COMPLIANCE` competente e independiente, con evidencia y decisión motivada. |

Quien adjudica no puede haber firmado valoración o entrega del mismo sorteo,
incluidas segundas firmas: aplica por persona natural, en todas sus salas y en
ambos órdenes de intervención. Cambiar de cuenta o subrol no elimina la
incompatibilidad. La segunda firma registrable es control del producto; no
reactiva la revisión humana obligatoria de código suspendida por Diego.

## Evidencia, subsanación y controversias

- Cada evidencia identifica entrega/ganador, aportante, origen, versión y recepción
  de sistema. Antes de acreditar, el rol competente registra sus verificaciones.
  El hash comprueba integridad del archivo; por sí solo no prueba el cumplimiento.
- Se conserva la jerarquía del catálogo: **DÉBIL no acredita una entrega**;
  registrables exigen **FUERTE**. Las demás categorías usan evidencia MEDIA o
  FUERTE cuando sea aplicable y suficiente según su catálogo.
- Los archivos conservan tipo validado, análisis antivirus, límites de tamaño y
  acceso privado con expiración. Las notas internas permanecen separadas de lo
  visible a las partes; mensajes y correcciones conservan su trazabilidad.
- La falta de información verificable pasa a revisión/subsanación con los estados,
  plazos, pausas y extensiones autorizadas del contrato. Un archivo incompleto no
  declara automáticamente incumplimiento del organizador ni entrega acreditada.
- El reclamo es estructurado según el contrato. Si se controvierte evidencia
  FUERTE del organizador, SUPPORT no cierra el caso: escala al adjudicador
  competente e independiente.
- El incumplimiento de entrega confirmado conserva la ruta de adquisición
  sustitutiva, o imposibilidad y cancelación según contrato. No se transforma en
  una causa de re-sorteo; aplicar la [matriz R6-12](../desarrollo/r612-resorteo-estados-permisos.md).

## Consentimiento y datos de entrega

El organizador accede después del reclamo y consentimiento correspondientes.
Recibe sólo los datos necesarios según RN-82/83; la dirección requiere premio
físico y consentimiento explícito vigente. Documento completo, correo y teléfono
no se entregan al organizador; el contacto telefónico necesario se intermedia
y enmascara desde la plataforma.

Si se retira el consentimiento de dirección, detener nuevas exposiciones y
coordinar una alternativa; no convertirlo automáticamente en renuncia al premio.
La [operación de worker y privacidad aprobada](../desarrollo/controles-servicio-rev6.md)
define comprobación por acceso, revocación desde la API e incidencias asíncronas.
Configuración efectiva y desarrollo siguen pendientes. Retención de datos y tratamiento externo de información
ya recibida mantienen su definición legal/operativa pendiente.

## Cierre y continuidad de desarrollo

La acreditación identifica al ganador y a quien cumplió: organizador o LIBOX por
adquisición sustitutiva respaldada. La sala conserva su cierre, sólo lectura y
trazabilidad conforme al contrato. G2 exige todas las acreditaciones vigentes;
comisión e impuesto conservan el momento aprobado en R6-09 y la liquidación
mantiene los demás gates. La reserva usa la [definición R6-11](../desarrollo/r611-catalogo-plazos-reservas.md).

Quedan pendientes la emisión/alineación de PRD/L3/interfaz, diseño visual,
implementación y verificación en desarrollo, ejecutor y fechas. No se selecciona
proveedor logístico ni se contrata servicio. Los demás subcasos de H22-10 mantienen
seguimiento y no se declaran resueltos por esta aprobación del recorrido.

Fuentes: [PRD V22](https://liboxapp.getoutline.com/doc/libox-prd-blueprint-mvp-v22-wp9CiWihnf),
§§13–16, RN-72…96 y RN-263; [L3 V21](https://liboxapp.getoutline.com/doc/libox-especificacion-tecnica-l3-v21-yC2vKLLNbN),
§4.3 y §6.5; [ficha de Diego](https://liboxapp.getoutline.com/doc/diego-pendientes-y-decisiones-tecnicas-rev6-dET6AASY9e)
y [tablero](https://liboxapp.getoutline.com/doc/21-tablero-de-acciones-tasks-iCoCY5qOjR).
