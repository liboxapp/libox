---
title: C1 — cierre SQL no crítico (overlay sobre V7)
status: borrador
tags: [r0, c1, l3-v8, sql]
updated: 2026-10-01
description: Particiones de 11/12 padres, ACL con la matriz B1, semilla PE y logins B2 simulados sobre V7 intacto, verificados en PostgreSQL 17 efímero; qué cierra y qué no.
---

# Cierre SQL no crítico de C1

**Estado:** borrador. Es un overlay sobre `libox_schema_L3_V7.sql` intacto
(sha256 `9ff3d07f…af937a43`). **No es el SQL de L3 V8**, no es una migración
completa y no acredita que funcione en Supabase gestionado. El canon V7 no se
modifica.

Anexos: [alcance C1/R1](cierre-sql-alcance.md) · [pendientes y precondiciones](cierre-sql-pendientes.md) ·
[riesgos de ACL B1](cierre-sql-riesgos-acl.md) · [artefactos](database/README.md).

## Qué se entrega

| Hallazgo | Entrega | Estado |
|---|---|---|
| H-05 particiones | Arranque idempotente para **11 de los 12 padres**: mes actual y dos siguientes en UTC, más una DEFAULT por padre, y una función de estado con cobertura de 30 días. B3–B6 [especificados](database/planificador-default.md) y retención B6 en el inventario como metadato | **Parcial (11/12).** `journal_lines` está en el inventario pero sin particiones: las aporta su dueño humano (ledger, B5). Planificador y procedimiento B4 especificados, no implementados |
| H-06 permisos | Denegación a PUBLIC, `anon`, `authenticated` y `service_role`. Matriz B1 aprobada: privilegios exactos en 78 tablas no patrimoniales, sin `DELETE`. Las seis candidatas de B1 pasan a `reservado_humano`. Logins B2 simulados en transacción revertida. Ningún beneficiario, salvo el dueño, en las particiones gestionadas | **Parcial.** Las 57 tablas reservadas quedan sin privilegios. Faltan logins reales, secretos, propiedad por `libox_migrate` (requisito del SQL V8), vistas seudonimizadas y cifrado KMS (B1-bis) |
| H-08 semillas | `markets` PE con los literales de L3 V7 §10.1 | Solo PE. No siembra FSM, ledger, incompatibilidades, configuración financiera ni administradores |
| H-07 / H-09 | Sondas de observación dentro de transacciones revertidas | **Siguen abiertos** (ver resultado) |

## Diseño

- **`journal_lines` es de aporte humano.** El inventario la marca
  `provisioning = humano`, así que `ensure_monthly_partitions` no le crea hijos,
  ni DEFAULT, ni ACL. Su escritura sigue fallando como en V7
  (`PT-JOURNAL-LINES-HUMANO`). El inventario conserva los 12 padres para detectar
  cualquier deriva del catálogo.
- **Horizonte de 2 meses (mes actual y dos siguientes)** para cumplir los 30 días
  de antelación de L3 V7 §1.3. Con horizonte 1, un trabajo del 30 de enero de 2027
  deja marzo sin crear aunque faltan 30 días; con horizonte 2 no ocurre.
  `partition_status` informa `covered_until` y `coverage_ok`, que exige cubrir
  la referencia más 30 días.
- **UTC explícito.** Las funciones fijan `TimeZone = UTC` y `search_path`. Con
  la sesión en `America/Lima`, el 30 de junio a las 22:00 local crea julio.
- **DEFAULT como respaldo** en los 11 padres gestionados: la fila se conserva y
  el estado la informa. Si la DEFAULT ya tiene filas de un mes, crear ese mes
  falla con `LIBOX_PARTITION_DEFAULT_HAS_ROWS`, sin mover ni borrar nada.
- **Espera acotada.** `lock_timeout = 5s` dentro de `ensure_monthly_partitions`:
  no espera indefinidamente detrás de una transacción larga. No hay bloqueo
  distribuido. Debe correr desde un único planificador.
- **ACL de particiones.** Se revoca a PUBLIC y a todo beneficiario distinto del
  dueño que aparezca en la ACL (`aclexplode`), sin lista fija de roles. Si queda
  alguno que no se pueda revocar, falla con `LIBOX_PARTITION_ACL_RESIDUAL`.
- **Fallos claros**, sin efectos parciales: inventario distinto, relación con
  otros límites, horizonte fuera de 0 a 12, y DEFAULT con filas.

## Cómo se ejecuta

```bash
python3 -m unittest discover -s scripts/database/tests          # sin Docker: se omiten 2
LIBOX_DB_DOCKER=1 python3 -m unittest discover -s scripts/database/tests
python3 scripts/database/c1_sql_check.py --escenario todos      # reescribe evidencia/
```

- **Imagen fijada:** `postgres@sha256:d74eeac9…2ec46f` (PostgreSQL 17.11). Otra
  imagen exige `--imagen` explícito y queda registrada. Por defecto usa
  `--pull never`.
- **Contenedor:** nombre único, sin red, sin puertos, usuario 999, solo lectura y
  `--cap-drop ALL`. Se elimina al terminar, también si falla el arranque.
- **Sin credenciales:** autenticación `trust` por socket local dentro del
  contenedor aislado.
- **CI:** `.github/workflows/hooks.yml` ya ejecuta la suite (configurado por el
  coordinador). El verde remoto está pendiente.

## Resultado de la ejecución local del 2026-10-01

Evidencia (esquema 2): [superusuario](database/evidencia/superusuario.json),
[dueño con CREATEROLE](database/evidencia/dueno-createrole.json) y
[privilegios de API simulados](database/evidencia/privilegios-api-simulados.json).
Cada JSON registra la fecha, el sha256 de cada fuente, la imagen, el
aislamiento, el rol instalador y el valor observado de cada comprobación.

- **Comprobaciones:** 100, 100 y 104 pasan. El tercer escenario simula privilegios
  por defecto para `anon`, `authenticated` y `service_role` (**no es Supabase
  gestionado**). Sin el overlay, `anon` lee y `service_role` modifica
  `journal_lines`.
- **Matriz B1:** `ACL-MATRIZ` compara 1120 pares tabla-rol (1568 con los roles de
  API) con el manifiesto. 35 sondas `ACL-B1-*` ejercen una concesión y una denegación
  por clase, incluidas las seis tablas reclasificadas para `libox_app`, `libox_read`
  y `libox_append`.
- **Logins B2:** el instalador del escenario, también sin `SUPERUSER`, crea los cuatro
  logins sin contraseña. Cada uno hereda exactamente la unión de sus roles de grupo y
  `libox_deployer` no recibe privilegios de datos. Todo se revierte.
  `B2-PROPIEDAD-V7-SIN-CAMBIO` confirma que la propiedad sigue en el instalador: la
  cesión a `libox_migrate` cambiaría la huella de V7 y queda como requisito del SQL V8.
- **Particiones:** los 11 padres tienen mes actual, dos siguientes y DEFAULT, y
  `journal_lines` no tiene hijos. `lock_timeout` saltó a los 5,1 s con
  `audit_events` bloqueada, sin crear particiones.
- **Privilegios por defecto:** con privilegios por defecto para `service_role` y
  un rol propio, las 11 particiones nuevas quedan sin beneficiarios distintos del
  dueño. Una tabla y una función creadas después tampoco reciben privilegios de
  PUBLIC ni de otros roles.
- **Beneficiarios:** revisados 144, todos roles de grupo permitidos sobre tablas
  padre o el esquema `public`.
- **Integridad de V7:** la huella no cambia. Ahora incluye dueño, RLS, políticas,
  reglas y procedimientos.
- **H-07 y H-09 siguen abiertos.**
- **Pruebas:** 27 recolectadas.
  - Sin Docker: 25 OK y 2 omitidas.
  - Con Docker: 27 OK en 63 s, con `ResourceWarning` tratado como error.
  - Las pruebas estáticas contrastan el manifiesto con la tabla B1 de
    [decisiones](decisiones-c1-datos.md#b1-matriz-de-privilegios-de-las-67-tablas-pendiente_matriz)
    (67 tablas) y comprueban el alcance de B2, B4 y B6.
  - La prueba de mutaciones exige fallo ante cada una de estas situaciones:
    - privilegios indebidos (reservado, partición, PUBLIC, `libox_ops`);
    - privilegios fuera de B1: `UPDATE` en registro inmutable, lectura de `users`
      por `libox_read`, `DELETE`, acceso a `spending_limits` y escritura en
      `aml_thresholds`;
    - manifiesto alterado (`users`, `spending_limits` o `alarm_resolutions` como
      `operativa`);
    - un login B2 que hereda acceso a una tabla reservada y una cesión de propiedad
      simulada;
    - un rol ajeno al manifiesto en una partición;
    - EXECUTE por defecto a PUBLIC (con `pg_default_acl` sin filas visibles);
    - `journal_lines` marcada como `overlay` en el inventario;
    - un mes equivocado;
    - seis cambios de esquema: columna, RLS, política, regla, procedimiento y dueño.
