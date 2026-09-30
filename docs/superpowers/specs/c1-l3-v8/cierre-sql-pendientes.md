---
title: C1 — pendientes y precondiciones del cierre SQL
status: borrador
tags: [r0, c1, l3-v8, sql, pendientes]
updated: 2026-09-30
description: Trabajo humano en zonas críticas, precondiciones bloqueantes para Supabase, decisiones abiertas y verificaciones no realizadas.
---

# Pendientes y precondiciones del cierre SQL

Anexo de [cierre SQL](cierre-sql.md). El dueño disponible es Diego. La revisión
humana obligatoria sigue suspendida, pero la prohibición de generar código de
las zonas críticas no. Aquí solo se especifica la aceptación.

## Implementación humana (zonas sin generación asistida)

| # | Qué | Aceptación mínima |
|---|---|---|
| 1 | **Particiones de `journal_lines`** (ledger). El overlay la inventaría como `humano` y no le crea hijos, DEFAULT ni ACL. H-05 queda en 11/12 | Arranque y rotación del dueño, con límites en UTC. Decidir si lleva DEFAULT (hoy su escritura falla sin partición, como en V7) y cuál es su ACL. `partition_status` la informa sin cobertura hasta entonces |
| 2 | INV-38 (H-07): se admite revocar al penúltimo `ADMIN_SUPER` (observado). También hay que corregir L3 V7 §14.3 l.4060 | Con 2 activos se rechaza; con 3 se admite. DELETE y suspensión también cuentan. Dos revocaciones concurrentes dejan al menos 2 |
| 3 | H-09: reactivar por UPDATE salta techo y segunda firma (observado) | Los mismos controles que el INSERT |
| 4 | Disparador de incompatibilidades y comprobaciones en ejecución | Antes, resolver la contradicción entre L3 V7 §3.16 l.2816 y §7.2 (INC-07, INC-10, INC-11) |
| 5 | Ruta única de `raffles.status` (§4.2) y semilla FSM | `actor_kind` no admite `USER_WINNER` (§4.3). "Estado anterior" necesita un estado persistido |
| 6 | Ledger H-01 a H-04: `ledger_accounts`, inmutabilidad y privilegios de asiento | Pendiente de confirmación contable |
| 7 | INV-06-b e INV-44: `raffles.substitute_guarantee_id` sin FK | Un UUID inexistente no satisface la garantía |
| 8 | Configuración financiera: `market_config_versions`, `fee_schedules` y valores de `platform_capabilities` | Valores confirmados por su dueño; no se infieren |
| 9 | Sorteo: resultados esperados de los 5 vectores (H-10, entregable de C1), `verify_draw` (H-11) y `server_seed` (H-12) | Implementación humana independiente |
| 10 | Pago tardío (H-16) y arranque de los dos primeros `ADMIN_SUPER` | Política ratificada; mecanismo sin cuentas ficticias reales |

## Precondiciones bloqueantes antes de aplicar en Supabase

El overlay **no está listo para producción** y no se ha aplicado a ningún
proyecto gestionado. Antes de hacerlo:

1. **Data API.** Desactivar la Data API o no exponer el esquema de dominio;
   comprobarlo en el proyecto.
2. **Privilegios por defecto.** Inventariar `pg_default_acl` de todos los roles
   (incluidos `postgres` y `supabase_admin`). El overlay solo revoca los que
   otorgó el rol que lo ejecuta; los demás deben quedar sin beneficiarios de API.
3. **`service_role`.** El overlay revoca sus privilegios sobre el esquema de
   dominio y sus particiones. Confirmar que ningún componente depende de ellos y
   que su `BYPASSRLS` no abre otra vía.
4. **RLS gestionado.** Validar si Supabase activa RLS o políticas por defecto en
   ese esquema. El overlay no depende de RLS ni lo configura.
5. **Ejecución real.** Aplicar V7 y el overlay con el rol real (`postgres` no
   superusuario) y repetir el runner o sus consultas de ACL contra ese proyecto.

## Decisiones abiertas (no críticas)

- **Matriz de privilegios** para las 67 tablas `pendiente_matriz`, y acceso a
  las 51 reservadas cuando exista su código humano. Ver
  [manifiesto](database/acl-manifest.json).
- **Logins y propiedad.** Logins técnicos por rol, gestión de secretos, y si
  `libox_migrate` pasa a ser dueño.
- **Planificador.** Trigger.dev o pg_cron con el rol dueño, una sola ejecución a
  la vez y horizonte 2. La alarma sale de `coverage_ok` (cobertura de la
  referencia más 30 días) y de `default_rows`.
- **Filas en DEFAULT.** Procedimiento aprobado para moverlas antes de crear el
  mes. Hoy la función falla sin moverlas.
- **Retención** de los 4 padres ausentes de L3 V7 §1.3; la de
  `operation_register` queda pendiente de [LEGAL→ABOGADO].
- **Borrador L3 V8 §1.3.** El revisor señala que dice que la escritura falla si
  falta el mes, lo que contradice la DEFAULT. Corresponde al dueño del borrador
  L3, no a este paquete.

**Semilla PE, ya resuelto:** `name = Perú` es el nombre visible del código `PE`.
Es una traducción trivial, no un dato contable ni normativo, así que no requiere
confirmación. La comprobación de deriva evalúa solo los literales de §10.1.

## Verificaciones no realizadas

- Proyecto Supabase Pro real, pooler, pg_cron y su build de PostgreSQL 17. Solo
  se probó la imagen oficial 17.11 arm64 en local; la imagen fijada es
  multiarquitectura.
- Verde de CI remoto. `hooks.yml` ya ejecuta `scripts/database/tests`.
- Migraciones numeradas del Anexo A. El overlay se aplica como bloque sobre V7.
- Markdownlint y lychee en local. Los enlaces relativos se comprobaron con un
  script.
