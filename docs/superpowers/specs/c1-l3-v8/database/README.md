---
title: C1 — artefactos SQL no críticos (overlay sobre V7)
status: borrador
tags: [r0, c1, l3-v8, sql]
updated: 2026-10-01
description: Índice del overlay borrador, manifiesto de ACL y evidencia de PostgreSQL 17 efímero.
---

# Artefactos SQL no críticos de C1

Borrador sobre `libox_schema_L3_V7.sql` intacto. **No es el SQL de L3 V8** ni una
migración completa. Contexto y resultado: [cierre SQL](../cierre-sql.md).

| Ruta | Contenido |
|---|---|
| [overlay/010_libox_ops_particiones.sql](overlay/010_libox_ops_particiones.sql) | Esquema `libox_ops`, inventario de los 12 padres (`journal_lines` marcada `humano`), particiones mensuales en UTC con horizonte 2, DEFAULT, ACL sin beneficiarios salvo el dueño y estado con cobertura de 30 días, solo para los 11 gestionados |
| [overlay/020_acl_base.sql](overlay/020_acl_base.sql) | Denegación a PUBLIC, `anon`, `authenticated` y `service_role`; concesiones del manifiesto, incluida la matriz B1 |
| [overlay/030_semilla_mercado_pe.sql](overlay/030_semilla_mercado_pe.sql) | `markets` PE con literales de L3 V7 §10.1 |
| [overlay/040_arranque_particiones.sql](overlay/040_arranque_particiones.sql) | Mes actual y dos siguientes (UTC) para los 11 gestionados, idempotente |
| [acl-manifest.json](acl-manifest.json) | Clasificación de las 135 tablas (B1: 78 con privilegios, 57 reservadas), logins B2 y alcance B4 |
| [planificador-default.md](planificador-default.md) | Especificación de B3–B6: pg_cron, filas en DEFAULT, `journal_lines` y retención |
| [evidencia/](evidencia/superusuario.json) | JSON por escenario, regenerado en cada ejecución |

Ejecución y pruebas: [runner](../../../../../scripts/database/c1_sql_check.py),
[contenedor](../../../../../scripts/database/pgdocker.py) y
[pruebas](../../../../../scripts/database/tests/test_overlay_static.py).

El overlay no contiene disparadores, cálculo de dinero, SQL del ledger (tampoco
las particiones de `journal_lines`), RBAC, sorteo, concurrencia de negocio ni
incompatibilidades. Lo comprueban `test_overlay_static.py` (construcciones
prohibidas, inventario y concesiones exactas) y `PT-JOURNAL-LINES-HUMANO`.
