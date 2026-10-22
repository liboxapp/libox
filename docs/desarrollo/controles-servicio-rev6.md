---
title: Rev6 — Operación del worker y privacidad de entrega
status: aprobado
tags: [desarrollo, rev6, act-r6-15, worker, privacidad]
updated: 2026-10-18
description: Parámetros y controles aprobados de ejecución diaria, incidencias y revocación de datos de entrega.
---

# ACT-R6-15 — Operación del worker y privacidad

**Definición aprobada por Diego el 18/10/2026.** Evidencia: «Apruebo, déjalo
documentado en Outline y dame el resumen de lo que queda pendiente de mi lado».
La aprobación fija los parámetros iniciales y controles siguientes. Implementación,
configuración efectiva, pruebas y cobertura operativa siguen pendientes.
El corpus de trabajo rev6 conserva su proceso de aceptación/emisión y sus freezes.

## Ejecución diaria y recuperación

El worker Go comprobará L-01…L-07 sobre Postgres/Supabase y la información del PSP
disponible. Declarar el trabajo en `scheduled_jobs` o escribir un log de inicio
no acredita que se haya ejecutado ni que el ledger esté correcto.

| Elemento | Parámetro o control aprobado |
|---|---|
| Horario inicial | Todos los días a las **02:00, America/Lima**. Antes de operar se ajustará si lo exige la disponibilidad del reporte del PSP. |
| Corte | Registrar el corte evaluado y usar información consistente. Si falta el reporte correspondiente del PSP, el control es **INCOMPLETO**, nunca satisfactorio. |
| Reintentos técnicos | Un intento inicial y hasta **3 reintentos**, con esperas sucesivas de **1, 5 y 15 minutos**. |
| Tiempo por intento | Máximo **5 minutos**. Los reintentos anteriores son para fallos técnicos; una divergencia contable no se trata como transitoria. |
| Monitor de ausencia | Proceso independiente del worker, cada **5 minutos**. Alertar si una hora después de la corrida programada no existe verificación completa. |
| Alertas | Panel operativo y correo operativo por designar. Motivo, ámbito y trazas; sin direcciones, documentos ni otros datos sensibles. |
| Coordinación | Diego coordina recuperación técnica. Las divergencias contables se atienden con el rol financiero competente y controles ya aprobados. |

La hora de referencia del atraso es la corrida programada: con el horario inicial,
el umbral es las 03:00 de Lima. El monitor no depende de que el worker que vigila
esté funcionando. No se fija aquí un proveedor de hosting, correo o monitorización.

La vista actual de trabajos vencidos mide antigüedad desde `last_success_at`.
Implementar «una hora después de la corrida programada» exige alinear registro,
planificación y monitor; **no equivale a poner 60 minutos en el campo actual sin
considerar su semántica**. Esa adecuación pertenece a la futura emisión/desarrollo.

## Controles, evidencia y consecuencias

| Control | Contenido conservado |
|---|---|
| L-01 | Cuadre de cada asiento. |
| L-02/L-03 | Pasivo de reembolsos, saldo agregado y caché frente a entradas canónicas. |
| L-04 | Suficiencia de reembolso por sorteo activo; sin tolerancia. |
| L-05/L-06 | Correspondencia de tickets/pagos y cuadre de liquidación. |
| L-07 | Conciliación con el proveedor y excepciones abiertas identificadas. |

Cada corrida registra inicio, fin, corte, ámbito, parámetros/versión, resultado por
control, diferencias, referencias e intentos con su traza. Distinguir ejecución
completa, resultado conforme o divergente, incompleto, fallo y ausencia. Conservar
el último resultado válido y su antigüedad; un fallo posterior no lo refresca.

- **Divergencia:** congelar liquidaciones del ámbito afectado y generar alerta
  inmediata de familia `LEDGER`, severidad alta, conforme al runbook.
- **Fallo definitivo o control vencido:** bloquear preventivamente nuevas
  liberaciones del ámbito no verificado. Registrar el motivo operativo sin
  presentarlo como divergencia económica demostrada.
- **Corrección:** seguir `trace_id` y los controles autorizados. T-14 conserva
  motivo, Finance y segunda firma Super de otra persona/subrol según R6-10.
  Nunca editar `journal_lines` ni hacer que el worker ajuste asientos para cuadrar.
- **Recuperación:** ejecutar nuevamente y conservar evidencia. Recuperar el
  proceso no abre G6: se requieren cuadre, excepciones resueltas y demás gates.

G6 conserva ledger cuadrado y cero excepciones de conciliación abiertas, con
evaluación automática y determinista. El bloqueo por control no verificado y una
divergencia contable son causas distintas; no se incorpora una excepción manual
de liberación. Los demás trabajos mantienen sus cadencias contractuales.

## Minimización y revocación del consentimiento

La API Go comprueba actor autorizado, pertenencia a la entrega y consentimiento
vigente **en cada acceso**. Durante el reclamo se presentan finalidad, destinatario,
datos concretos y mecanismo de revocación. Conservar sujeto, entrega/sorteo,
versión, fecha de sistema, alcance, huella del texto y traza conforme al contrato.

| Situación | Comportamiento aprobado |
|---|---|
| Organizador autorizado | Sólo datos necesarios: nombre y apellido inicial; dirección únicamente para premio físico y con consentimiento explícito vigente. Documento completo, correo y teléfono no se entregan. Contacto telefónico necesario intermediado/enmascarado. |
| Revocación | Efectiva desde la confirmación de la API, **sin esperar al worker**. Bloquear nuevas exposiciones al organizador e invalidar accesos/enlaces dependientes de ese consentimiento. |
| Trabajo asíncrono | El worker registra incidencias y avisa al responsable de delivery para coordinar una alternativa; no convierte la revocación en renuncia automática. |
| Información ya recibida por terceros | Seguir el protocolo de privacidad; una revocación técnica no retira por sí sola las copias ya recibidas. |
| Historial y observabilidad | Conservar trazabilidad con acceso restringido. No copiar dirección, documento ni otros datos sensibles en alertas o telemetría. |

Los enlaces o accesos que dependan del consentimiento deben respetar la revocación;
no basta con retirar un botón mientras una URL anterior sigue exponiendo datos al
organizador. La autorización vigente se comprueba también para la entrega concreta,
no por conocer un identificador o pertenecer genéricamente a una sala.

El worker gestiona las consecuencias asíncronas; la protección de acceso es de la
API. Se conserva el [delivery aprobado](../flujos/delivery-premios-rev6.md), sin
trasladar a este consentimiento las consecuencias del consentimiento biométrico.
No se borra automáticamente el expediente al revocar.

## Condiciones pendientes antes de operar

- Destinatarios, correo operativo y cobertura humana de atención/escalamiento.
  Diego coordina lo técnico; no se presume una disponibilidad personal permanente.
- Disponibilidad/corte del reporte PSP y validación del horario efectivo.
- Política legal de retención/supresión y protocolo para datos ya compartidos.
  No se fija un número de días mediante esta aprobación.
- Configuración efectiva, ejecutores, estimación y fechas; implementación humana
  donde corresponda y verificación durante desarrollo, sin levantar los freezes.

## Verificaciones pendientes para desarrollo

| ID | Caso | Estado |
|---|---|---|
| IT-R615-01 | Corrida diaria, corte consistente y resultado por control; reporte PSP ausente produce incompleto. | PENDIENTE |
| IT-R615-02 | Divergencia, alerta inmediata y congelamiento del ámbito; recuperación sin apertura automática de G6. | PENDIENTE |
| IT-R615-03 | Reintentos/tiempo máximo, monitor independiente, ausencia y fallo definitivo; bloqueo y registro correctos. | PENDIENTE |
| IT-R615-04 | Acceso ajeno, consentimiento ausente/revocado y enlaces anteriores; protección desde la API incluso sin worker. | PENDIENTE |
| IT-R615-05 | Trazabilidad de aceptación/revocación/acceso e incidencias sin filtrar datos sensibles. | PENDIENTE |

Conservar versión/commit, entorno, ejecutor, fecha y evidencia por caso.
Estos casos no se ejecutan en esta etapa documental.

## Fuentes

- [PRD V22](https://liboxapp.getoutline.com/doc/libox-prd-blueprint-mvp-v22-wp9CiWihnf): RN-47/48, RN-82/83, RN-266 y §15.1. [L3 V21](https://liboxapp.getoutline.com/doc/libox-especificacion-tecnica-l3-v21-yC2vKLLNbN): L-01…L-07, trabajos programados, consentimiento y runbook.
- [Ficha de Diego](https://liboxapp.getoutline.com/doc/diego-pendientes-y-decisiones-tecnicas-rev6-dET6AASY9e) y [tablero](https://liboxapp.getoutline.com/doc/21-tablero-de-acciones-tasks-iCoCY5qOjR): aprobación del 18/10/2026; [pruebas pendientes](pruebas-pendientes-rev6.md).
- [OWASP sobre autorización](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html#validate-the-permissions-on-every-request): comprobar permisos en cada solicitud. Los parámetros horarios y reintentos de esta nota son decisiones de LIBOX.
