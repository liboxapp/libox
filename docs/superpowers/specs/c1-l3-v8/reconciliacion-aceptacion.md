---
title: C1 — aceptación de viabilidad, fianza y cierre
status: borrador
tags: [r0, c1, aceptacion, viabilidad]
updated: 2026-10-01
description: Requisitos candidatos y contraejemplos de la revisión Cowork, sin generar implementación financiera, concurrente o de sorteo.
---

# Aceptación de los cambios de Cowork

Complementa el [registro C1-V](reconciliacion-linea-base.md). Esta especificación
no entrega código de zonas protegidas. Diego implementa los controles de dinero,
concurrencia, transición e incompatibilidades; cada resultado se verificará
contra la migración completa, no solo con presencia de campos o fixtures.

## Publicación y mínimo — C1-V01/V02

La propuesta exige fecha final en todos los tipos, máximo definido por mercado y
`end_at > start_at`. Sin máximo aprobado no se publica. El cierre de venta es
efectivo aunque el worker llegue tarde; debe usar la misma referencia temporal
en compra, reserva, webhook y transición. Falta decidir inclusividad/precisión.

El mínimo protege la entrega de todos los premios, incluida la suma de T6. La
fuente propone importe derivado del valor aprobado y múltiplo de mercado, y
tickets derivados con redondeo hacia arriba. El múltiplo PE 1,25 es un dato de
la fuente, no una ratificación nueva de Diego. El dueño fija costes cubiertos,
moneda, unidades, redondeo y caja disponible después de retenciones/comisiones.

| Caso | Resultado exigido para cerrar la especificación |
|---|---|
| Tipo T1–T8 publicado sin fecha, con intervalo inválido o fuera del máximo | Rechazo; no basta condicionar el CHECK a `published_at` si existe otro camino a ACTIVE |
| Cambio de configuración del mercado tras publicar | Conserva precio, mínimo, premio y condiciones fijados; la versión pertenece al mismo mercado y está aprobada |
| Mínimo monetario alto con mínimo de tickets igual a 1 | Rechazo si no corresponde a la fórmula aprobada; documentar frontera y redondeo |
| T6 con varios premios | Incluye todos los valores/costes aprobados; no usa solo el primer premio |
| Tickets impagados, gratuitos o anulados | No incrementan la recaudación pagada válida; contadores no exceden sus relaciones admisibles |
| Piso bruto cumplido pero caja neta insuficiente | No acredita respaldo para entregar el premio; define fondos adicionales y disponibilidad |
| Cambio de mínimo después de cargar hitos T4 | Revalida el conjunto antes de publicar; no basta el trigger de insertar/editar un hito |

BR-09 y su KPI deberán expresar respaldo acreditado suficiente, compatible con
la fianza. No contabilizarla como recaudación, comisión o ingreso para reconciliar
una contradicción literal. Derecho de adquisición y capacidad de entrega del bien
requieren tratamiento separado de su valoración. [LEGAL→ABOGADO]

## Cobertura y ciclo de fianza — C1-V03

La fuente propone `VIABILITY_FAILED` y una ventana para cubrir el faltante con
`VIABILITY_GAP`. Propone 48 h; reloj, actor, suspensión y reanudación están
[pendientes de definición](reconciliacion-decisiones-planificacion.md).

La referencia de garantía no satisface el gate por ser no nula. Deben coincidir
existencia, clase, sorteo, aportante, moneda, saldo suficiente, fondos acreditados,
estado vigente/no liberado y trazabilidad del movimiento. Una FK no cubre todos
estos requisitos. Las sondas de Opus aceptaron referencias inventadas, ajenas o
insuficientes: quedan como contraejemplos de aceptación, no controles corregidos.

| Caso | Criterio de aceptación pendiente |
|---|---|
| Depósito solicitado, UUID inventado, pago pendiente o monto insuficiente | No habilita freeze ni sorteo |
| Garantía de otro sorteo/moneda/clase o ya devuelta | Rechazo; no puede respaldar dos obligaciones incompatibles |
| T-19: fondos confirmados | Custodia conciliada y auditable; no genera comisión ni ingreso |
| T-20: premio entregado y atestado/liquidación cumplidos | Devuelve al destinatario debido una sola vez; define gastos y evidencia de cierre |
| T-21: incumplimiento | Aplica fondos al destino autorizado para entregar el premio; define beneficiario, compra, conciliación y sobrante |
| Cancelación después del depósito por causa distinta del incumplimiento | Ruta explícita para depósito y compras; sin saldo retenido sin destino |
| Confirmación después de vencer la cobertura | Política expresa; no abre un sorteo ya cancelado por un webhook tardío |
| Duplicado o carrera entre devolución, ejecución y cancelación | Un solo efecto patrimonial; saldo y estado coherentes; firma/actor verificables |

T-20 y T-21 pueden compartir cuentas de débito/crédito. Eso no demuestra un error:
faltan tipo de operación, beneficiario, destino y evidencia. No se exige inventar
otra cuenta para diferenciar etiquetas. ASS-001 permanece abierto. [LEGAL→ABOGADO]

## Transición, inventario y cierre — C1-V04/V05/V06

| Caso | Criterio de aceptación pendiente |
|---|---|
| Comprobación de dinero seguida de anulación/pago/liberación concurrente | Snapshot coherente de caja, pool y garantía antes de freeze/compromiso; sin ventana de elusión |
| Pérdida de viabilidad estando READY_TO_DRAW | Ruta definida de recuperación/cancelación; no quedar bloqueado sin salida |
| PAUSED o SUSPENDED al vencer venta/cobertura | Reloj y estado de retorno admisible explícitos; no suspensión indefinida |
| ENDED_TIME con pool vacío, umbral T2 fallido y mínimo fallido | Precedencia determinista; causa y efecto reputacional coherentes |
| VIABILITY_FAILED sin deadline o retorno con estado no permitido | Rechazo por el punto único de transición; no aceptar solo presencia de campo |
| Falso positivo de inviabilidad anticipada | Corrección/recuperación declarada; decidir si puede volver a ACTIVE |
| T1 parcial viable | Sortea con las bases fijadas; bajo mínimo aplica el desenlace que se ratifique |
| T4 viable al plazo pero sin hito disparador | Decisión explícita antes de habilitar el tipo; no inferirla de una guarda general |
| T6 parcial con menos elegibles que ganadores sin reemplazo | No ejecuta un reparto imposible; condición adicional al mínimo económico |
| SOLD_OUT con anulaciones antes de freeze | Recalcula validez y respaldo; SOLD_OUT por sí solo no acredita solvencia |
| Contracargo después de ejecutar | Registra su efecto por la política T-13; no altera retrospectivamente el pool ejecutado |

`tickets_reserved` incluye emitidos. La fórmula anticipada nueva excluye reservas
pendientes aún pagables; **no duplica ventas**. Con 100 tickets todos reservados,
sin pagos, precio 1 y mínimo 100, calcula potencial cero aunque las reservas
puedan pagarse. El dueño debe definir potencial realizable y estados/TTL con casos
frontera. No se incorpora cancelación por velocidad de venta ni esperar TTL como
solución obligatoria. H-08 sigue abierto: 54 filas con guardas JSON no implementan
el intérprete ni la exclusión concurrente de transiciones.

## Contrato público y pruebas — C1-V07/V08/V10/V11

- Bases, checkout, sala, avisos y API deben comunicar mínimo, fecha, cobertura y
  desenlaces compatibles. La promesa de cancelación automática no puede coexistir
  con continuar por fianza sin explicarlo antes de comprar.
- Configuración y respuestas públicas distinguirán cantidad mínima, importe,
  versión fijada, estado y deadline. `ends_at` nullable y metadatos V8 no completan
  el contrato. No publicar importes ni saldos internos de custodia sin decidir su alcance.
- Canal habilitado requiere coste de cobro/reembolso, plazos y comisión declarados;
  participante recibe devolución íntegra según contrato. Validar coste/caja con
  datos del PSP; una tarifa hipotética no demuestra viabilidad del canal.
- Semilla: punto único/idempotente, cuentas referenciadas existentes (incluida
  `adjustment` para T-13), monedas y tipos coherentes. No ejecutar dos copias como
  si fueran migraciones independientes.
- Cada rechazo debe comprobar error/SQLSTATE esperado; todo fallo inesperado debe
  hacer fallar el runner. La suite recibida emite WARNING y admite cualquier
  excepción como rechazo: sus 39 OK no cierran estos controles.
- Mutación de gate que permita cualquier garantía debe hacer fallar una prueba
  semántica. `verify_corpus.py` verde no demuestra esa propiedad.

Primera aceptación: norma/contrato coherente en C1; controles críticos humanos y
migración completa antes de su emisión en C2. Backend, PSP, Supabase y F1–F7 se
prueban en D1/R1. No se declara ninguna de estas pruebas ejecutada en esta actualización.
