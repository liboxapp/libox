---
title: C1 — decisiones de Diego del 4 de octubre
status: aprobado
tags: [r0, c1, decisiones, go, auditoria, viabilidad]
updated: 2026-10-04
description: Ratificaciones de Vercel, Trigger.dev, Auth administrada, mínimo 1,45, auditoría y presupuesto, con límites y pendientes explícitos.
---

# Decisiones del 4 de octubre de 2026

Origen: respuestas de Diego a la lista de doce pendientes de C1 en Codex.
Este registro aprueba las decisiones expresas; no declara completado C1,
emitido el canon ni implementados los controles. Conserva el alcance de las
[decisiones del 30/09](decisiones-c1.md) y el
[stack Go y frontend TypeScript](../2026-10-02-stack-go-frontend-ts.md).

## Terminología corregida

Diego precisó: «no seria fianza, seria garantia». El término de trabajo es
**garantía adicional del organizador**. Los ejemplos de depósito se presentan
como una garantía en dinero, sin dar por elegida su forma concreta. La corrección
no habilita todavía la alternativa ni cierra sus condiciones. El material recibido
de Cowork conserva su terminología de origen como evidencia histórica.

## Registro por punto

| Punto | Respuesta de Diego | Alcance registrado | Trabajo que continúa |
|---|---|---|---|
| 1 | «Vercel queda» | Vercel para alojar el backend Go; Vercel Pro conserva el frontend | Validar modalidad, runtime, región, conexiones, límites y despliegue antes de habilitarlo |
| 2 | «Conservaremos trigger dev pero vamos a seguir analizandolo para los primeros meses del startup y su funcionalidad» | Conservar Trigger.dev y evaluar su utilidad durante los primeros meses | Definir frontera con Go y revisar funcionalidades, fiabilidad, carga de mantenimiento y coste con evidencia de uso |
| 3 | «Todo queda» | Conservar dirección Go y contratos existentes | La lista no elegía un servidor HTTP, driver/ORM o migrador concreto; no se inventa esa elección |
| 4 | «Si, todo correcto» | Ratificar autenticación administrada con Supabase Auth y cifrado de dominio con KMS; Go valida identidad y aplica permisos | Inventario de atributos de Auth, excepción precisa, rotación, sesiones, MFA y revocación |
| 5 | «Necesito escenarios para entender mas esto» | Decisión sobre garantía pendiente de revisar escenarios | Mantener cancelación/reembolso de C1 mientras no se ratifique la ampliación |
| 6 | «El multiplo sera x1.45 para que asi Libox tenga mas comision» | Múltiplo de mínimo económico de 1,45 sobre el valor aprobado del premio, para el mercado inicial PE | Fórmula completa, costes, caja, redondeo, coherencia con el rango de recaudación y contrato comprador; no cambia por sí mismo la tasa de comisión |
| 7 | «Queda todo» | Conservar acuerdos de plazos y cierre existentes | Completar máximos por mercado, excepción Flash, precedencia, suspensión y pagos tardíos; ninguna duración nueva figuraba en la lista |
| 8 | «Queda» | Conservar el frente de reputación | Umbrales, duración, recuperación y apelación no tenían valores u opciones concretas para ratificar |
| 9 | «Operaciones sensibles tienen que ser totalmente auditables, en realidad mas detallademente estas, todo tiene que ser auditable» | Auditabilidad general de las operaciones y mayor detalle en las sensibles | Catálogo de eventos, campos, controles de integridad/acceso, correlación, alertas y pruebas; detalle abajo |
| 10 | «Queda todo» | Mantener coordinación de las validaciones externas | No acredita dictamen, lista P-C, custodia, confirmación contable ni condiciones comerciales recibidas |
| 11 | «Si» | Confirmar la necesidad de otra persona real para las segundas firmas | Identificar persona, subroles, disponibilidad y acceso; no se asigna un nombre por inferencia |
| 12 | «250$ mensuales quedan bien» | Mantener techo de infraestructura US$250/mes | Recalcular configuración Go, Trigger.dev, Supabase, KMS, copias y observabilidad; no es un coste ejecutado |

Los «queda» conservan el alcance existente. No crean números, nombres o reglas
que la lista no especificaba. No contratan proveedores ni autorizan por sí solos
una habilitación con dinero real. Las validaciones legales siguen
[LEGAL→ABOGADO].

## Relación entre múltiplo y comisión

El mínimo de 1,45 sustituye el valor de 1,25 **propuesto para el nuevo mínimo**.
La actualización de la línea base y su SQL protegido sigue pendiente de emisión
y del aporte humano. No confundirlo con `rounding_multiple` ni con la tasa de
`fee_schedules`.

El [PRD vigente §1.3](../../../linea-base/LIBOX_PRD_BLUEPRINT_MVP_V9.md)
documenta comisión base/techo del 20 % sobre ventas brutas y escala por volumen.
La respuesta de Diego no especifica otra tasa ni deroga esa escala.
Ejemplo didáctico con premio de S/1.000 y tasa base del 20 %, sin costes ni
impuestos en esta comparación:

| Ventas al mínimo ilustrado | Comisión bruta Libox | Neto del organizador antes de ajustes |
|---|---|---|
| S/1.250 (1,25) | S/250 | S/1.000 |
| S/1.450 (1,45) | S/290 | S/1.160 |

La diferencia de comisión bruta es S/40 cuando las ventas alcanzan S/1.450;
el excedente de S/450 sobre el premio no pertenece íntegramente a Libox.
No constituye una previsión de ingresos ni beneficio después de PSP/impuestos.
Una garantía reembolsable no es venta, recaudación ni comisión. Con ventas de
S/1.200, la comisión base ilustrativa sería S/240 si el flujo finalmente
liquida, aunque una garantía cubriera la brecha del mínimo.

## Auditabilidad aprobada y aceptación por concretar

La exigencia abarca operaciones de negocio, accesos a datos/evidencias y acciones
administrativas, tanto aceptadas como rechazadas; incluye API, procesos Go,
workflows, pagos, decisiones, firmas, exportaciones y accesos a la propia auditoría.
Las acciones sensibles deben permitir reconstruir la secuencia y su autorización.

Criterios de diseño para integrar y comprobar, sin afirmar implementación:

- Identificador de evento y correlación de operación/solicitud/job, fecha UTC,
  actor humano o servicio, acción, objeto, versión, resultado y motivo.
- En sensibles: contexto de autorización/reautenticación, solicitante y firmas,
  versión de política, cambio permitido antes/después o su referencia protegida,
  evidencia y relación con efectos de negocio.
- Integridad e inmutabilidad del registro, privilegios mínimos y trazabilidad de
  lecturas/exportaciones de auditoría; reconciliación ante fallos o duplicados.
- Auditar uso de datos personales y claves sin copiar el dato descifrado, claves,
  contraseñas, tokens o payloads indiscriminados al log.
- Separar auditoría de negocio de logs diagnósticos; definir campos, retención,
  archivo, alertas y política ante indisponibilidad por clase de operación.
- Probar eventos ausentes, rechazos, firmas, cambios de versión, correlación
  entre servicios, redacción de secretos y modificación/eliminación indebida.

La retención aprobada existente se conserva; los plazos legales pendientes siguen
al abogado. El detalle de logging se apoya en
[OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html).
No se promete auditoría completa por activar logs de Vercel o CloudTrail.

## Siguiente definición y entrega

Revisar los [escenarios T1/garantía](escenarios-t1-garantia.md) con Diego y elegir el
desenlace. Completar herramientas, parámetros y responsables pendientes, integrar
la prosa/contratos permitidos y delimitar aportes humanos del SQL/motor/dinero.
La ejecución y pruebas de servicios reales siguen en D1/R1; la emisión es C2.
