---
title: Rev6 — Estados, causas y autorización del re-sorteo
status: aprobado
tags: [rev6, act-r6-12, resorteo, estados, permisos]
updated: 2026-10-18
description: Matriz y controles aprobados de re-sorteo, con renuncia validada e inelegibilidad confirmada.
---

# ACT-R6-12 — Estados, causas y autorización del re-sorteo

**Definición aprobada por Diego el 18/10/2026.** Evidencia: «Apruebo, déjalo
documentado en Outline y sigamos con delivery R6-14». Amplía el bloqueo por
controversia abierta aprobado anteriormente. La matriz describe el comportamiento
objetivo; los dos estados nuevos y los controles aún requieren implementación.
El corpus reconciliado conserva su proceso de aceptación/emisión. H22-03/H22-11
siguen abiertos hasta el cierre técnico acreditado durante desarrollo.

## Matriz aprobada de causas y estados

| Causa | Estado previo a autorizar | Evidencia exigida |
|---|---|---|
| `WINNER_NO_CLAIM` | `NO_CLAIM_EXPIRED` | Plazo de reclamo vencido, contacto agotado y documentado, organizador sin incorporarse a la sala. |
| `SHIPPING_ABANDONED` | `SHIPPING_ABANDONED` | Opciones de transporte exigidas y plazos de elección/pago y gracia agotados. |
| `WINNER_DECLINED` | **Renuncia validada**, nuevo | Renuncia del propio ganador, firmada, vinculada al premio y conservada con trazabilidad. |
| `WINNER_INELIGIBLE` | **Inelegibilidad confirmada**, nuevo | Expediente de cumplimiento resuelto como rechazado, con motivo y decisor competente. |

Para el envío se conservan las exigencias de RN-84; este acuerdo no cambia sus
plazos. Los estados de renuncia e inelegibilidad son denominaciones funcionales
nuevas: sus identificadores técnicos se definirán al incorporar la máquina.

Los dos estados nuevos sólo se alcanzan desde una sala **no terminal**, antes de
una entrega acreditada y después de verificar la evidencia correspondiente. La
transición autorizada de las cuatro filas termina en `RESOLVED_REDRAW` cuando
se cumplen todos los controles. Entrar en un estado nuevo no elimina los hechos
ni las restricciones del expediente.

## Permisos y responsabilidades del producto

| Actor | Acción |
|---|---|
| Ganador | Reclamar y aportar o firmar la renuncia que le corresponde; no autorizar el re-sorteo. |
| SUPPORT | Documentar contacto, aportar/verificar lo que corresponda a su función y preparar el expediente; no autorizar. |
| Rol competente de cumplimiento | Resolver el expediente de inelegibilidad con motivo e identidad del decisor. |
| `ADMIN_LEGAL_COMPLIANCE` | Autorizar el re-sorteo con permiso explícito y vigente, evidencia y controles satisfechos. |
| SYSTEM | Ejecutar las transiciones automáticas y la ejecución programada conforme a la autorización válida. |

La autorización queda reservada a `ADMIN_LEGAL_COMPLIANCE`: pertenecer a otro
subrol ADMIN no concede este permiso por sí solo. Las incompatibilidades aplicables
por persona se conservan; la autorización no permite saltar una condición.
Estos son roles del producto, no asignaciones de trabajo a los socios.

## Bloqueos por hechos del expediente

Antes de autorizar y antes de ejecutar se comprueba, para cada ganador que se
pretende excluir, que no exista:

- Controversia de entrega abierta que le corresponda.
- Incumplimiento de entrega del organizador confirmado.
- Adquisición sustitutiva registrada para cumplirle el premio.

Los controles se mantienen aunque cambie el estado de la sala. En particular,
`NO_DELIVERY → DISPUTED` no habilita un re-sorteo prohibido. No se admite
re-sortear por un incumplimiento de entrega del organizador; corresponde la
ruta de adquisición sustitutiva o imposibilidad con cancelación según el contrato.

Si un reclamo se descarta, todavía debe acreditarse una de las cuatro causas y
los demás requisitos. Una controversia de otro ganador no bloquea automáticamente
este reemplazo: el control identifica a quienes serían excluidos.

## Requisitos conservados y secuencia

1. Verificar identidad de sorteo, ejecución original, ganador/premio afectados,
   causa y prueba. La ruta `REDRAW` debe estar declarada en las bases publicadas.
   Se mantienen las restricciones de categoría y la salida contractual aplicable.
2. Comprobar estados admitidos, bloqueos por hechos y permiso vigente de quien
   autoriza. Registrar causa, evidencia, actor, momento y traza de la autorización.
3. Derivar el pool excluyendo los tickets del ganador sustituido; preservar la
   relación con la ejecución original y el alcance del reemplazo.
4. Publicar un compromiso nuevo y completo: hash de nueva semilla y ronda futura
   de baliza, **con al menos 24 horas de anticipación**, conforme a RN-108.
5. Antes de ejecutar, volver a comprobar los bloqueos vigentes. Una controversia
   pertinente aparecida después de autorizar **pausa la ejecución** y conserva
   la traza; no se ejecuta basándose sólo en una comprobación anterior favorable.
6. Ejecutar una sola vez, publicar la cadena completa y motivo, reevaluar plazos
   y comunicarlos a los participantes. Sigue el recorrido de reclamo y entrega.

Se conserva **máximo un re-sorteo por sorteo**. Un segundo fallo lleva a cancelación
y devolución íntegra conforme al contrato. Rechazar una solicitud no equivale a
cancelar automáticamente en cualquier caso. Una repetición de evento o solicitud
no crea una segunda autorización efectiva ni una segunda ejecución.

La evidencia de causa y del estado de origen se conserva con la autorización.
Al ejecutar no se exige que la sala siga en un estado que ya dejó legítimamente
al autorizar; sí se vuelven a comprobar los bloqueos y las condiciones vigentes.
El cierre y la integridad de la sala original mantienen sus reglas de trazabilidad.

## Continuidad y pendientes de desarrollo

Actualizar en la futura emisión L3 §4.3, permisos y contrato de interfaz con los
dos estados y el subrol aprobados. La renuncia conserva los controles de firma,
identidad y trazabilidad; su vínculo documental y los demás subcasos de H22-10
mantienen el seguimiento de ACT-R6-14. La inelegibilidad requiere el expediente
de cumplimiento previsto: no se reemplaza por una etiqueta de riesgo sin resolver.

Diego conserva la propiedad humana del motor, admisión de re-sorteo y controles
protegidos. Ejecutor y fecha por designar. La revisión humana obligatoria sigue
suspendida hasta una instrucción expresa; esta aprobación no la reactiva ni levanta
el freeze del scaffold o del corpus. No se genera código ni se ejecutan pruebas ahora.

Durante desarrollo se verifican las cuatro causas válidas e inválidas, transición
a los dos estados nuevos, permisos, bloqueos por controversia, rutas por `DISPUTED`,
incidencias posteriores a autorizar, pool, compromiso, límite y repetición. La
aprobación documental no acredita el cierre de H22-03/H22-11 ni los demás hallazgos.

## Fuentes

- [Ficha de Diego](https://liboxapp.getoutline.com/doc/diego-pendientes-y-decisiones-tecnicas-rev6-dET6AASY9e) y [tablero](https://liboxapp.getoutline.com/doc/21-tablero-de-acciones-tasks-iCoCY5qOjR): aprobación anterior y ampliación del 18/10/2026.
- [PRD V22](https://liboxapp.getoutline.com/doc/libox-prd-blueprint-mvp-v22-wp9CiWihnf), RN-84 y §16.4; [L3 V21](https://liboxapp.getoutline.com/doc/libox-especificacion-tecnica-l3-v21-yC2vKLLNbN), §3.6 y §4.3.
- [Registro V24](https://liboxapp.getoutline.com/doc/libox-registro-maestro-de-linea-base-v24-TBDcjlR1hE), H22-03/10/11.
- [Recorrido de premios](../flujos/recorridos-premios-rev6.md#05-re-sorteo) y [delivery](../flujos/delivery-premios-rev6.md): continuidad del ganador y evidencia.
