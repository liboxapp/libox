---
title: C1 — pendientes y precondiciones del cierre SQL
status: borrador
tags: [r0, c1, l3-v8, sql, pendientes]
updated: 2026-10-01
description: Trabajo humano en zonas críticas, precondiciones bloqueantes para Supabase, decisiones abiertas y verificaciones no realizadas.
---

# Pendientes y precondiciones del cierre SQL

Anexo de [cierre SQL](cierre-sql.md). El dueño disponible es Diego. La revisión
humana obligatoria sigue suspendida, pero la prohibición de generar código de
las zonas críticas no. Aquí solo se especifica la aceptación.

La [reconciliación Cowork](reconciliacion-linea-base.md) amplía esta entrega.
Su SQL V8 no es la migración consolidada de C1: instalarlo y cargar 54 transiciones
no cierra H-04/H-08 ni las sondas de garantía/mínimo aceptadas indebidamente.

## Implementación humana (zonas sin generación asistida)

| # | Qué | Aceptación mínima |
|---|---|---|
| 1 | **Particiones de `journal_lines`** (ledger). El overlay la inventaría como `humano` y no le crea hijos, DEFAULT ni ACL. H-05 queda en 11/12 | B4–B5 aprueban DEFAULT; integrar arranque, rotación UTC y movimiento humano, con ACL por definir. Hoy falla la escritura sin partición y `partition_status` informa falta de cobertura |
| 2 | INV-38 (H-07): se admite revocar al penúltimo `ADMIN_SUPER` (observado). También hay que corregir L3 V7 §14.3 l.4060 | Con 2 activos se rechaza; con 3 se admite. DELETE y suspensión también cuentan. Dos revocaciones concurrentes dejan al menos 2 |
| 3 | H-09: reactivar por UPDATE salta techo y segunda firma (observado) | Los mismos controles que el INSERT |
| 4 | Disparador de incompatibilidades y comprobaciones en ejecución | Integrar A11 aprobada: §7.2 prevalece e INC-07 solo en ejecución; no basta editar una matriz |
| 5 | Ruta única de `raffles.status` (§4.2) y semilla FSM | `actor_kind` no admite `USER_WINNER` (§4.3). "Estado anterior" necesita un estado persistido |
| 6 | Ledger H-01 a H-04: `ledger_accounts`, inmutabilidad y privilegios de asiento | H-04 exige integridad humana en DB; H-01–H-03 pueden quedar registrados para C2 por D-05, sin afirmar dinero real listo |
| 7 | INV-06-b e INV-44: `raffles.substitute_guarantee_id` sin FK | Un UUID inexistente no satisface la garantía |
| 8 | Configuración financiera: `market_config_versions`, `fee_schedules` y valores de `platform_capabilities` | Valores confirmados por su dueño; no se infieren |
| 9 | Sorteo: resultados esperados de los 5 vectores (H-10, entregable de C1), `verify_draw` (H-11) y `server_seed` (H-12) | Implementación humana independiente |
| 10 | Pago tardío (H-16) y arranque de los dos primeros `ADMIN_SUPER` | Ratificar política pendiente de F7; mecanismo sin cuentas ficticias reales |
| 11 | C1-V02/V03: mínimo, versión fijada, caja y garantía de brecha | Rechaza mínimo de tickets incoherente y fianza inexistente/ajena/insuficiente/liberada; fondos y moneda vinculados; no copiar el gate defectuoso |
| 12 | C1-V04/V05: FSM, inventario y cobertura | Snapshot atómico, relojes y salidas por estado/tipo; reservas pagables incluidas; recuperación definida |
| 13 | C1-V03/V10: T-19/20/21 y semilla financiera | Un punto de entrada idempotente, cuentas completas, destino/sobrante/cancelación y efectos únicos; ciclo definido antes de habilitar fianza |

Los casos y límites están en [aceptación Cowork](reconciliacion-aceptacion.md).
No se añade aprobación contable general como gate nuevo de C1 ni código generado.

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
   Incluye comprobar que ese rol crea los logins de B2 y cede la propiedad; en
   local solo se probó con un instalador `CREATEROLE` sin `SUPERUSER`.
6. **pg_cron.** Confirmar que Supabase Pro permite programar el trabajo de B3 con
   el rol dueño, como pide la condición de B3.

## Acuerdos integrados y decisiones restantes

Estado tras integrar las [fichas B](decisiones-c1-datos.md) el 2026-10-01:

- **B1, matriz de privilegios. Integrada.** Las 67 tablas tienen clase y el
  [manifiesto](database/acl-manifest.json) coincide con la tabla de la decisión
  (lo comprueba una prueba estática). Las seis candidatas pasan a reserva humana
  sin privilegios: 57 reservadas en total. Riesgos detectados sin ampliar
  privilegios: [riesgos de ACL](cierre-sql-riesgos-acl.md).
- **B1-bis, cifrado con AWS KMS. Pendiente del SQL V8.** Las columnas `*_enc`, las
  huellas HMAC nuevas, la rotación, las vistas seudonimizadas para `libox_read` y
  la caché de claves no se simulan en el overlay. La compatibilidad obligatoria
  con Supabase y su alcance Auth siguen por concretar; la excepción para email y
  teléfono en `auth.users` sigue sin decidir y no se infiere.
- **B2, logins y propiedad. Simulada en local.** Los cuatro logins se crean con
  el instalador del escenario dentro de una transacción revertida, sin
  contraseña. Falta crearlos en Supabase, guardar sus secretos en Vercel y
  Trigger.dev y rotarlos cada 90 días. La cesión de propiedad a `libox_migrate`
  cambiaría la huella del esquema V7 protegido: es **requisito del SQL V8** y no
  se da por cerrada. Sin esa cesión, `libox_deployer` no puede migrar.
  B2 ya precisa membresías explícitas por componente: el worker hereda ambos
  roles aprobados, `libox_app` y `libox_append`.
- **B3, planificador. Especificado** en [planificador y DEFAULT](database/planificador-default.md).
  La lectura de `partition_status` desde Trigger.dev necesita una concesión que
  B1 no decide; no se añade.
- **B4, filas en DEFAULT. Especificado**, nunca automático y solo para los 8
  padres no críticos. Los de `event_outbox`, `journal_lines`,
  `operation_register` y `psp_events` son traslado humano.
- **B5, `journal_lines`. Sin cambios en el overlay.** La DEFAULT aprobada, su ACL
  y su arranque siguen siendo implementación humana (fila 1 de la tabla anterior).
- **B6, retención. Integrada como metadato** del inventario. No hay borrado ni
  archivo. `psp_events` y `operation_register` siguen con [LEGAL→ABOGADO].
- **Borrador L3 V8 §1.3.** Describe DEFAULT para los padres gestionados y conserva
  la excepción del ledger: su aporte humano sigue pendiente. La norma y el
  estado del overlay se distinguen explícitamente.

**Semilla PE, ya resuelto:** `name = Perú` es el nombre visible del código `PE`.
Es una traducción trivial, no un dato contable ni normativo, así que no requiere
confirmación. La comprobación de deriva evalúa solo los literales de §10.1.

## Verificaciones no realizadas

- Logins reales, secretos, rotación y cesión de propiedad (B2). AWS KMS (B1-bis).
- Proyecto Supabase Pro real, pooler, pg_cron y su build de PostgreSQL 17. Solo
  se probó la imagen oficial 17.11 arm64 en local; la imagen fijada es
  multiarquitectura.
- Verde de CI remoto. `hooks.yml` ya ejecuta `scripts/database/tests`.
- Migraciones numeradas del Anexo A. El overlay se aplica como bloque sobre V7.
- Lychee en local. Markdownlint pasa; los enlaces relativos se comprobaron con un
  script.
