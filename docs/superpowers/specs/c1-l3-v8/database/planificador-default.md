---
title: C1 — planificador de particiones, filas en DEFAULT y retención (B3–B6)
status: borrador
tags: [r0, c1, l3-v8, sql, particiones]
updated: 2026-10-01
description: Especificación de pg_cron con alarma en Trigger.dev, procedimiento escrito para filas en DEFAULT, regla de journal_lines y retención como metadato.
---

# Planificador, filas en DEFAULT y retención

Especificación de las [decisiones B3–B6](../decisiones-c1-datos.md#b3-planificador-de-particiones).
**No se implementa en el overlay**: no hay `pg_cron`, ni función que mueva filas, ni
borrado o archivo. La prueba estática `test_b6_retention_is_metadata_only` lo comprueba.
Contexto: [cierre SQL](../cierre-sql.md) y [pendientes](../cierre-sql-pendientes.md).

## B3. Planificador con pg_cron y alarma en Trigger.dev

| Elemento | Especificación |
|---|---|
| Tarea | `SELECT count(*) FROM libox_ops.ensure_monthly_partitions(now(), 2);` una vez al día, en UTC |
| Rol | El dueño de los padres particionados. En V7 es el instalador; en V8 será `libox_migrate` (B2), que hoy es `NOLOGIN` |
| Ejecución única | `pg_cron` no solapa dos ejecuciones del mismo trabajo. `lock_timeout = 5s` acota la espera. No se programa desde otro sitio |
| Fallo | `LIBOX_PARTITION_*` aborta sin efectos parciales y queda en `cron.job_run_details` |
| Alarma (Trigger.dev) | Alta si algún padre gestionado tiene `coverage_ok = false` o `default_rows > 0`, o si la última ejecución del trabajo falló |

Precondiciones sin verificar en Supabase Pro:

1. Que `pg_cron` admite programar el trabajo con el rol dueño y que un rol `NOLOGIN`
   puede ejecutarlo (con conexión libpq necesita `LOGIN`).
2. Cómo lee Trigger.dev el estado. `partition_status` no es `SECURITY DEFINER` y cuenta
   filas de las DEFAULT, que no tienen beneficiarios; `libox_worker` no tiene `EXECUTE`
   ni acceso a `cron.job_run_details`. Cualquier vía (función de lectura con propietario
   fijo, instantánea escrita por el trabajo o rol de monitorización) es una concesión
   nueva no decidida en B1. **No se añade aquí.**
3. `journal_lines` informará `coverage_ok = false` hasta que exista su aporte humano
   (B5). La alarma no debe silenciarla.

## B4. Filas en la DEFAULT: procedimiento escrito, nunca automático

Hoy `ensure_monthly_partitions` falla con `LIBOX_PARTITION_DEFAULT_HAS_ROWS` y no
mueve nada. El procedimiento lo ejecuta el dueño tras la alarma. Solo se permite en
los 8 padres no críticos de `procedimiento_default_b4.padres_permitidos` del
[manifiesto](acl-manifest.json): `analytics_events`, `audit_access_events`,
`audit_events`, `notification_attempts`, `registry_queries`, `risk_events`,
`room_messages` y `state_transitions`.

`event_outbox`, `journal_lines`, `operation_register` y `psp_events` son
`reservado_humano`: el traslado de sus filas lo define y ejecuta su dueño humano.
`test_b4_default_procedure_scope` exige que ambas listas cubran los 12 padres sin
solaparse.

Pausar el trabajo de `pg_cron` antes del traslado y asegurar su reanudación también
si el traslado falla. La pausa del planificador no detiene escrituras de aplicación.
El traslado exige una única transacción, con `lock_timeout = 5s`:

1. Comprobar el padre permitido y bloquear padre y DEFAULT contra escrituras y DDL
   concurrentes antes de leer filas. Revalidar bajo esos bloqueos que el mes `M`
   no existe. Si no se obtienen los bloqueos, abortar sin trasladar filas.
2. Registrar el conjunto exacto de claves y contenido de las filas de `M` y su recuento.
3. Crear la tabla suelta del mes con estructura e índices requeridos, copiar ese
   conjunto, retirar exactamente esas filas de DEFAULT y adjuntar con límites UTC.
4. Aplicar `restrict_partition_acl` a la nueva partición.
5. Comparar claves, contenido y recuento del conjunto trasladado; cualquier diferencia
   revierte toda la transacción. No confiar solo en un recuento o una huella agregada.
6. Insertar la auditoría y confirmar. Después reanudar el trabajo del planificador.

Si se implementa en V8 como función, debe rechazar padres fuera de la lista, no
concederse `EXECUTE` a nadie salvo al dueño y no invocarse desde `pg_cron`. Pruebas
mínimas: filas y recuento iguales, inserción concurrente bloqueada o rechazada sin
pérdida, timeout sin efectos, reversión ante diferencia, rechazo de padres
humanos, rechazo si el mes ya existe, ACL sin beneficiarios y entrada de auditoría.

## B5. `journal_lines`

B5 aprueba DEFAULT también en `journal_lines`, pero su implementación es humana. El
inventario la mantiene en `provisioning = humano`. El overlay no le crea hijos,
DEFAULT ni ACL, y `PT-JOURNAL-LINES-HUMANO` sigue exigiendo que su escritura falle
hasta ese aporte. Su traslado desde la DEFAULT queda fuera del procedimiento B4.

## B6. Retención

La columna `retention` del inventario recoge B6 como metadato:

| Padre | Retención |
|---|---|
| `audit_access_events`, `risk_events` | Indefinida; archivo en frío desde 24 meses |
| `psp_events` | La del soporte contable del pago, [LEGAL→ABOGADO]; sin borrado hasta plazo aprobado |
| `operation_register` | Plazo del registro de operaciones, [LEGAL→ABOGADO]; sin borrado hasta plazo aprobado |

No se implementa borrado, `DETACH` ni archivo en frío. El archivo en frío de los
padres indefinidos necesita diseño propio.
