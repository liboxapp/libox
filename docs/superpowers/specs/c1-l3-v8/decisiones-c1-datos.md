---
title: C1 — decisiones de base de datos y cifrado
status: aprobado
tags: [r0, c1, l3-v8, decisiones, sql]
updated: 2026-09-30
description: Privilegios de las 67 tablas, cifrado de datos personales con AWS KMS, logins, particiones y retención (B1–B6).
---

# Base de datos y cifrado

Parte del [paquete de decisiones de C1](decisiones-c1.md). Decidido por Diego el 2026-09-30.

Fuente: [cierre SQL](cierre-sql.md), [pendientes SQL](cierre-sql-pendientes.md) y
[manifiesto de ACL](database/acl-manifest.json).

## B1. Matriz de privilegios de las 67 tablas `pendiente_matriz`

Roles de grupo: `libox_app` (backend), `libox_append` (agregación) y `libox_read`
(reportería). No se concede `DELETE` en ninguna. Las 51 `reservado_humano` no se tocan.

**Propuesta por clase.** Las clases nuevas se añaden al manifiesto; la prueba de
concesiones exactas ya existe.

| Clase propuesta | `libox_app` | `libox_read` | Tablas |
|---|---|---|---|
| `operativa` | S, I, U | S | `alarms`, `benefits`, `client_capabilities`, `client_kyb_documents`, `client_members`, `client_reputation`, `clients`, `devices`, `disputes`, `featured_placements`, `notarial_instruments`, `notification_preferences`, `partners`, `pc_stage_documents`, `pc_workflow_stages`, `prize_valuation_documents`, `raffle_media`, `raffle_recurrences`, `registrable_assets`, `registry_blocks`, `resolution_rooms`, `risk_rules`, `room_assignments`, `room_participants`, `sla_extensions`, `transfer_acts`, `user_devices`, `user_reputation`, `waitlists`, `winner_legal_readiness`, `audit_emergency_queue` |
| `registro_inmutable` | S, I | S | `alarm_resolutions`, `attribution_touches`, `benefit_redemptions`, `client_reputation_history`, `client_transfer_acceptances`, `daily_codes`, `dispute_evidence`, `feature_toggle_log`, `kpi_snapshots`, `organizer_referral_codes`, `prize_market_references`, `raffle_terms`, `registry_queries`, `responsible_play_events`, `risk_events`, `room_evidence`, `survey_responses`, `user_attributions` |
| `sensible` | S, I, U | — | `users`, `credentials`, `refresh_tokens`, `identity_documents`, `client_kyb`, `aml_cases`, `blocked_documents`, `leads` |
| `sensible_inmutable` | S, I | — | `identity_verifications`, `age_verifications`, `aml_case_documents` |
| `catalogo_lectura` (existente) | S | S | `aml_thresholds` (cambia por migración, con su versión) |
| Candidatas a `reservado_humano` | — | — | Ver abajo |

`sensible` sin `libox_read`: la reportería sobre datos personales irá por vistas
seudonimizadas, que se definen aparte.

**Candidatas a reclasificar como `reservado_humano`**, porque su comportamiento
puede caer en una zona crítica aunque su nombre no lo sugiera:

| Tabla | Motivo |
|---|---|
| `spending_limits`, `spending_limit_changes`, `self_exclusions` | Si se comprueban dentro de la compra, forman parte de la reserva y el bloqueo de saldo |
| `operation_register` | Registro AML con importes; retención [LEGAL→ABOGADO] |
| `transfer_costs` | Importes y quién los asume; puede afectar la liquidación |
| `raffle_milestones` | Desbloquea premios al alcanzar un número de tickets vendidos (inventario y concurrencia) |

**Recomendación:** aprobar las clases tal cual y reclasificar las seis candidatas
como `reservado_humano`. Es más barato abrir una tabla después que descubrir que
la app escribía en una zona crítica sin control.
**Desbloquea:** H-06 para las tablas no críticas.
**Decisión:** clases aprobadas y las seis candidatas pasan a `reservado_humano`. Además, ver [cifrado de datos personales](#b1-bis-cifrado-de-datos-personales). Diego, 2026-09-30.

## B1-bis. Cifrado de datos personales

Decisión de Diego del 2026-09-30, a raíz de B1: **la base no guarda datos
personales en claro**; se cifran con un servicio externo de claves.

- **Servicio:** AWS KMS. La clave maestra no sale de KMS y la base nunca la ve.
- **Esquema:** cifrado de sobre. El backend pide a KMS una clave de datos, cifra el
  valor con ella (AES-256-GCM) y guarda el texto cifrado junto con la clave de datos
  cifrada. CloudTrail registra las llamadas a KMS; los usos locales de claves de datos requieren auditoría aplicativa.
- **Alcance: todo dato personal.** Lo que V7 ya cifra (documento, nombre, secreto
  MFA, beneficiario final, datos bancarios) más email, teléfono, fecha de
  nacimiento, nombres de contacto de `leads` y datos del representante legal.
- **Búsquedas:** donde haya que buscar o detectar duplicados (email en el login,
  número de documento), se guarda además una huella HMAC con clave propia, igual
  que el `document_number_hash` de V7.
- **Permisos:** el cifrado no sustituye a B1. Protege ante el robo de la base; los
  permisos limitan qué componente lee qué.

**Pendiente de decidir al integrar:**

- **Compatibilidad con Supabase obligatoria**, confirmada por Diego el 2026-09-30.
  Antes de implementar, definir el alcance de Supabase Auth y el inventario de
  datos personales, incluidos documentos, logs y exportaciones. La excepción
  para email/teléfono en `auth.users` sigue pendiente: exigir compatibilidad no
  autoriza esa excepción ni ratifica reemplazar Auth con autenticación propia.
- **Rotación** de la clave maestra y de la clave HMAC, y cómo se recifran los datos.
- **Reportería:** qué vistas seudonimizadas necesita `libox_read`.
- **Coste y latencia:** caché de claves de datos en el backend, con su tiempo de vida.

El [alcance de compatibilidad](compatibilidad-supabase-kms.md) separa lo aprobado de la excepción Auth pendiente.
El canon V8 debe recoger estos puntos en §1 y §7.3. Las columnas `*_enc` nuevas
se añaden al SQL V8, no al overlay de V7.

## B2. Logins y propiedad

- **(a)** `libox_migrate` (NOLOGIN) es dueño del esquema de dominio. Logins por
  componente, con membresías explícitas por función: `libox_api` → `libox_app`;
  `libox_worker` → `libox_app` y `libox_append`; `libox_reporting` → `libox_read`;
  `libox_deployer` → `libox_migrate`, usado solo en CI de migraciones. Secretos en
  el gestor de Vercel y Trigger.dev, con rotación cada 90 días.
- **(b)** Un único login de aplicación con todos los roles de grupo.

**Recomendación: (a).** Limita el daño de una credencial filtrada y deja rastro por
componente. Pendiente de comprobar en Supabase: que `postgres` puede crear los
logins y ceder la propiedad (precondición 5 de
[pendientes SQL](cierre-sql-pendientes.md#precondiciones-bloqueantes-antes-de-aplicar-en-supabase)).
**Decisión:** **(a)**, un login por componente. Diego, 2026-09-30.

## B3. Planificador de particiones

- **(a)** `pg_cron` en Supabase con el rol dueño, una ejecución diaria de
  `ensure_monthly_partitions(horizonte 2)`. Una tarea de Trigger.dev lee
  `partition_status` y emite la alarma si `coverage_ok` es falso o
  `default_rows > 0`.
- **(b)** Todo en Trigger.dev, que se conecta con credencial del dueño.

**Recomendación: (a).** El DDL corre dentro de la base sin sacar la credencial del
dueño a un servicio externo, y Trigger.dev solo necesita leer. Condición: verificar
que Supabase Pro permite `pg_cron` con ese rol.
**Decisión:** **(a)**, `pg_cron` con alarma en Trigger.dev. Diego, 2026-09-30.

## B4. Filas que caen en la partición DEFAULT

Hoy, si la DEFAULT tiene filas de un mes, crear ese mes falla con
`LIBOX_PARTITION_DEFAULT_HAS_ROWS` y no se mueve nada.

- **(a)** Procedimiento de operación en una transacción, ejecutado por el dueño
  tras la alarma: crear la tabla del mes suelta, mover las filas desde la DEFAULT,
  adjuntarla. Queda como función separada con registro en `audit_events`, nunca
  automática.
- **(b)** Mantener el fallo y resolver cada caso a mano.

**Recomendación: (a).** La alarma ya avisa. Un procedimiento escrito evita
improvisar bajo presión.
**Decisión:** **(a)**, procedimiento escrito, nunca automático. Diego, 2026-09-30.

## B5. Partición DEFAULT y ACL de `journal_lines`

Solo se decide la regla. Las particiones del ledger las implementa Diego.

**Conflicto.** L3 V7 §1.3 dice que la falta de partición "es una alarma de
severidad alta, no un error en tiempo de escritura". Sin DEFAULT, hoy la
escritura del ledger falla, lo que contradice esa regla.

- **(a)** DEFAULT también en `journal_lines`, como en los otros 11 padres, con la
  misma alarma. `libox_append` solo INSERT; nadie UPDATE ni DELETE.
- **(b)** Sin DEFAULT: el ledger no escribe fuera de un mes creado (falla cerrado).

**Recomendación: (a).** Cumple el canon y no bloquea cobros por un fallo del
planificador. La inmutabilidad y los privilegios de asiento (H-01 a H-04) siguen
siendo trabajo humano.
**Decisión:** **(a)**, DEFAULT también en `journal_lines`. Implementación humana. Diego, 2026-09-30.

## B6. Retención de los 4 padres sin regla

L3 V7 §1.3 no fija retención para `psp_events`, `operation_register`,
`risk_events` y `audit_access_events`.

| Tabla | Propuesta |
|---|---|
| `audit_access_events` | Igual que `audit_events`: indefinida, archivo en frío desde 24 meses |
| `risk_events` | Indefinida, archivo en frío desde 24 meses |
| `psp_events` | La misma que el soporte contable del pago. [LEGAL→ABOGADO] (plazo tributario) |
| `operation_register` | [LEGAL→ABOGADO] (plazo del registro de operaciones) |

**Recomendación:** aprobar las dos primeras y pedir al abogado los dos plazos
legales. Nada se borra mientras no haya plazo aprobado.
**Decisión:** aprobadas las dos primeras; `psp_events` y `operation_register` al abogado, sin borrado hasta entonces. Diego, 2026-09-30.
