---
title: C1 — paquete de decisiones para el cierre
status: borrador
tags: [r0, c1, l3-v8, decisiones]
updated: 2026-09-30
description: Decisiones de dominio pendientes de C1 con contexto, opciones y recomendación, para resolverlas en una sesión e integrarlas en el borrador L3 V8.
---

# Paquete de decisiones de C1

Reúne en un solo lugar las decisiones abiertas de [estado de C1](estado-c1.md) que
bloquean integrar contratos, SQL y configuración en el borrador L3 V8. Cada ficha
trae el conflicto, las opciones, una recomendación y lo que desbloquea.

**Qué no es.** No decide nada por sí mismo ni cambia el canon (CD-07). No propone
importes, porcentajes, comisiones, impuestos ni reglas patrimoniales: esos valores
son del dueño contable y se piden en el [bloque E](#e-datos-que-no-se-proponen).
Tampoco reemplaza la implementación humana de las
[zonas sin IA](../../../../.claude/rules/zonas-sin-ia.md): donde una decisión
alimenta código crítico, aquí solo se decide la regla; el código lo escribe Diego.

## Cómo responder

En cada ficha, completa la línea **Decisión** con la letra elegida, `R`
(recomendación tal cual) o un texto propio. Las fichas marcadas
[LEGAL→ABOGADO] pueden decidirse de forma provisional; quedan con esa marca hasta
la ratificación. Con las respuestas, se integran en el borrador OpenAPI, el
overlay SQL y L3 V8, con pruebas, en un PR aparte.

| Bloque | Fichas | Desbloquea |
|---|---|---|
| [A. Roles, firmas y transiciones](#a-roles-firmas-y-transiciones) | A1–A11 | Política de firmantes, operaciones P-C, rechazos y KYB en el contrato |
| [B. Base de datos](#b-base-de-datos) | B1–B6 | H-05 completo, H-06 y la matriz de privilegios V8 |
| [C. Configuración por tipo](#c-configuración-por-tipo-de-sorteo) | C1–C4 | `RaffleConfiguration` T1–T8 en el contrato |
| [D. Sorteo](#d-sorteo) | D1 | Entrada de H-10 a H-12 |
| [E. Datos que no se proponen](#e-datos-que-no-se-proponen) | — | Configuración financiera y ledger |

**Orden sugerido:** A1 primero, porque A2, A7, A8 y B1 dependen de él.

## A. Roles, firmas y transiciones

Fuente de roles: [L3 V7 §7.1–7.2](../../../linea-base/LIBOX_ESPECIFICACION_TECNICA_L3_V7.md).
Detalle de los conflictos I-xx: [cierre contractual](cierre-contratos.md#hallazgos-del-canon-cd-07).

### A1. Quién firma en segundo lugar (I-04)

**Conflicto.** §7.1 da "Segunda firma" solo a `ADMIN_SUPER`. INC-09 exige que la
segunda firma sea de otra persona **y otro subrol**. Si quien solicita es
`ADMIN_SUPER`, ambas reglas no pueden cumplirse a la vez. El contrato hoy falla
cerrado: sin política, ninguna solicitud es firmable.

- **(a)** Aplicar §7.1 literal: siempre firma `ADMIN_SUPER`. INC-09 se relaja a
  "otra persona".
- **(b)** Aplicar INC-09 literal: siempre otra persona y otro subrol. Las acciones
  que solo puede iniciar `ADMIN_SUPER` quedan sin firmante posible.
- **(c)** Política por `action_code` como dato: otra persona siempre; otro subrol
  salvo cuando la acción es propia de `ADMIN_SUPER`, en cuyo caso firma otro
  `ADMIN_SUPER`. Es coherente con INV-38, que existe para que siempre haya dos.

**Recomendación: (c)**, con esta tabla inicial para los 11 códigos del contrato:

| `action_code` | Solicita normalmente | Firmantes elegibles (propuesta) |
|---|---|---|
| `VALUATION_V2_COSIGN` | `SUPPORT_VALUATOR` | `ADMIN_MODERATION` (ver A2) |
| `VALUATION_V4` | `SUPPORT_VALUATOR` | `ADMIN_LEGAL_COMPLIANCE` |
| `VALUATION_EXCEPTION` | `SUPPORT_VALUATOR` o `ADMIN_LEGAL_COMPLIANCE` | El otro de los dos; `ADMIN_SUPER` |
| `PC_STAGE_E3` | `ADMIN_LEGAL_COMPLIANCE` | `ADMIN_SUPER` |
| `PC_STAGE_E7` | `ADMIN_LEGAL_COMPLIANCE` | `ADMIN_SUPER` |
| `ATTEST_PC` | `ADMIN_LEGAL_COMPLIANCE` | `ADMIN_SUPER` |
| `CAPABILITY_PLATFORM_DISABLE` | `ADMIN_SUPER` | Otro `ADMIN_SUPER` |
| `MARKET_RESUME` | `ADMIN_SUPER` | Otro `ADMIN_SUPER` |
| `MULTIPLE_OVERRIDE` | `ADMIN_COMPLIANCE` | `ADMIN_SUPER` |
| `SUBROLE_GRANT` | `ADMIN_SUPER` | Otro `ADMIN_SUPER` |
| `MFA_RESET_INTERNAL` | `ADMIN_SUPER` | Otro `ADMIN_SUPER` |

INC-11 se mantiene: nadie firma su propia acción. `MULTIPLE_OVERRIDE` toca el rango
de recaudación: aquí solo se decide el firmante, no la regla del múltiplo.

**Desbloquea:** firma de las 11 solicitudes y el apagado global de capacidad.
**Decisión:** ______

### A2. Cofirma de la banda V2 por `ADMIN_MODERATION` (I-01)

**Conflicto.** La banda V2 exige cofirma de `ADMIN_MODERATION`, pero §7.1 le da
solo `R` en "Valoración de premio".

- **(a)** Añadir en la matriz V8 una fila "Cofirma de valoración V2" con `A` para
  `ADMIN_MODERATION`. Cofirmar no le da escritura sobre la valoración.
- **(b)** Mover la cofirma a `ADMIN_LEGAL_COMPLIANCE`, que ya tiene `A`.

**Recomendación: (a).** Conserva la separación que buscaba la regla: quien modera
el sorteo no es quien valora. Ya está modelado así en el contrato.
**Decisión:** ______

### A3. Actor de `VALUATION_OBSERVED` (I-03)

**Conflicto.** El canon asigna la observación a un "Verificador", que no es un subrol.

- **(a)** Limitarla a quienes aprueban la banda: `SUPPORT_VALUATOR` y
  `ADMIN_LEGAL_COMPLIANCE`.
- **(b)** Crear el subrol `SUPPORT_VERIFIER`.

**Recomendación: (a).** Es lo que ya aplica el contrato y evita un subrol nuevo con
su fila de matriz e incompatibilidades.
**Decisión:** ______

### A4. Quién decide cada etapa P-C (I-02)

**Conflicto.** El PRD V9 asigna actores distintos por etapa. §7.1 tiene una sola
fila "Etapas P-C" con `A` solo para `ADMIN_LEGAL_COMPLIANCE`.

| Etapa | Aprueba según PRD V9 | Firma (A1) |
|---|---|---|
| E1 Elegibilidad | `ADMIN_RISK` | — |
| E2 Titularidad | `ADMIN_LEGAL_COMPLIANCE` | — |
| E3 Valoración | `ADMIN_LEGAL_COMPLIANCE` | `PC_STAGE_E3` |
| E4 Instrumento y bloqueo | `ADMIN_LEGAL_COMPLIANCE` | — |
| E5 Publicación y venta | Sin aprobador (automática) | — |
| E6 Preparación del ganador | `SUPPORT_L2` verifica; `ADMIN_LEGAL_COMPLIANCE` habilita | — |
| E7 Transferencia | `ADMIN_LEGAL_COMPLIANCE` | `PC_STAGE_E7` |

- **(a)** Partir la fila de §7.1 en una matriz por etapa igual a la tabla de arriba.
  E6 en dos pasos: verificación y habilitación.
- **(b)** Todo a `ADMIN_LEGAL_COMPLIANCE`, con `ADMIN_RISK` y `SUPPORT_L2` como
  asesores sin decisión.

**Recomendación: (a).** Respeta el PRD, que es la fuente de producto, y mantiene
la elegibilidad (reputación, KYB) en el rol de riesgo. [LEGAL→ABOGADO] para E2, E4
y E7.
**Desbloquea:** operaciones de decisión de etapa, junto con A8.
**Decisión:** ______

### A5. Capacidad `LIVE` y categorías P-C (I-05)

**Conflicto.** `client_capabilities.capability` admite `T8` y `LIVE`. El PRD
define T8 como "Live": modo de presentación, no motor. Además, `P_C1` y `P_C2` no
son tipos de sorteo y no deben ir en `enabled_raffle_types`.

- **(a)** Retirar `LIVE`; `T8` es la única capacidad para sorteos en vivo. Mover
  `P_C1` y `P_C2` a un campo `enabled_categories`.
- **(b)** Conservar ambos: `T8` habilita el tipo y `LIVE` la transmisión.

**Recomendación: (a).** Hoy no hay caso que necesite habilitar uno sin el otro.
**Decisión:** ______

### A6. Transiciones de rechazo manual (I-06)

**Conflicto.** La FSM no tiene transición para rechazar manualmente una valoración
ni para observar o rechazar el gate legal. El contrato solo expone resultados con
transición.

Hoy la FSM del sorteo (§4.1) solo sale de `PENDING_VALUATION` hacia `REJECTED` por
`AUTO_REJECT_DEVIATION`, aunque `prize_valuations.outcome` ya admite `REJECTED`.
De `PENDING_LEGAL` solo sale `LEGAL_GATE_PASSED`.

- **(a)** Añadir en V8 tres transiciones con motivo obligatorio:
  - `PENDING_VALUATION → REJECTED` por `VALUATION_REJECTED`, con los mismos actores
    que la aprobación;
  - `PENDING_LEGAL → DRAFT` por `LEGAL_GATE_OBSERVED` (subsanable);
  - `PENDING_LEGAL → REJECTED` por `LEGAL_GATE_REJECTED` (terminal).
  Las dos últimas, con `ADMIN_LEGAL_COMPLIANCE`.
- **(b)** No añadir: los rechazos solo ocurren por las reglas automáticas.

**Recomendación: (a).** Sin rechazo manual, un caso dudoso queda indefinidamente
en revisión. Replica el patrón de `VALUATION_OBSERVED`, que ya vuelve a `DRAFT`.
El punto único de transición sigue siendo implementación humana (H-08).
[LEGAL→ABOGADO] para el gate legal.
**Decisión:** ______

### A7. Quién decide KYB (I-07)

**Conflicto.** §7.1 no tiene fila para decidir KYB. El contrato no expone la
operación.

- **(a)** `ADMIN_COMPLIANCE` decide (`A`); `ADMIN_RISK` lee (`R`).
- **(b)** `ADMIN_RISK` decide, porque ya gestiona las capacidades del cliente.

**Recomendación: (a).** KYB es parte del expediente de cumplimiento, donde
`ADMIN_COMPLIANCE` ya tiene `A`, y separa quien verifica al cliente de quien le
habilita capacidades. El proveedor (Truora) sigue en evaluación.
**Decisión:** ______

### A8. Lista cerrada de documentos por etapa P-C (I-08)

**Conflicto.** RN-29 exige `checklist_key` de lista cerrada por etapa, sin semilla.
**Bloquea todo P-C.**

- **(a)** Diego y el abogado entregan la lista por etapa (clave, descripción,
  obligatoria sí/no). Se integra como semilla y enum.
- **(b)** Posponer P-C del MVP y lanzar sin categorías P-C1/P-C2.

**Recomendación:** decidir primero si P-C entra en el MVP. Si entra, **(a)**: se
puede preparar una plantilla con las claves que ya menciona el PRD V9 §7 para que
el abogado la corrija, pero no inventar la lista. [LEGAL→ABOGADO].
**Decisión:** ______

### A9. Atestación sin `second_signer_id` (CC-08)

**Conflicto.** §11.5 define la atestación con `second_signer_id` en el cuerpo. El
resto de segundas firmas usa `SignatureRequest`.

- **(a)** Migrar a `SignatureRequest` con `ATTEST_PC`. Cambia un cuerpo del inventario.
- **(b)** Mantener `second_signer_id` en la atestación como excepción.

**Recomendación: (a).** Un solo mecanismo de firma, con INC-09 e INC-11 comprobados
en un único punto. El cambio va en V8 con su nota de migración del contrato.
**Decisión:** ______

### A10. Ventana de reautenticación (S-3)

- **(a)** 5 minutos para acciones sensibles (supuesto actual).
- **(b)** Otro valor.

**Recomendación: (a).** Es corta frente a la sesión interna de 30 minutos (§7.3) y
suficiente para una firma.
**Decisión:** ______

### A11. Motivos de rechazo en moderación y dónde se comprueban las incompatibilidades

**A11.1 `REJECT` en moderación.** Falta el enum del "motivo estructurado" de §4.1.
Propuesta inicial, para corregir: `CONTENT_POLICY`, `PRIZE_INELIGIBLE`,
`TERMS_INCOMPLETE`, `MEDIA_INVALID`, `LEGAL_REQUIREMENT`, `OTHER` (este último con
texto obligatorio). **Decisión:** ______

**A11.2 Incompatibilidades.** §3.16 l.2816 y §7.2 se contradicen:

| Regla | §3.16 dice | §7.2 dice | Propuesta |
|---|---|---|---|
| INC-07 | Ejecución | Asignación y ejecución | Ejecución: `ADMIN_FINANCE` no tiene `A` en atestar; no hay par de subroles que bloquear |
| INC-10 | Ejecución | Organizativo, auditado | Organizativo: no hay comprobación en DB |
| INC-11 | Asignación | Ejecución | Ejecución: depende de la acción concreta |

**Recomendación:** §7.2 prevalece, con INC-07 solo en ejecución; §3.16 se corrige
en V8. Los disparadores y comprobaciones siguen siendo implementación humana.
**Decisión:** ______

## B. Base de datos

Fuente: [cierre SQL](cierre-sql.md), [pendientes SQL](cierre-sql-pendientes.md) y
[manifiesto de ACL](database/acl-manifest.json).

### B1. Matriz de privilegios de las 67 tablas `pendiente_matriz`

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
**Decisión:** ______

### B2. Logins y propiedad

- **(a)** `libox_migrate` (NOLOGIN) es dueño del esquema de dominio. Logins por
  componente, cada uno miembro de un solo rol de grupo: `libox_api` → `libox_app`;
  `libox_worker` → `libox_app` y `libox_append`; `libox_reporting` → `libox_read`;
  `libox_deployer` → `libox_migrate`, usado solo en CI de migraciones. Secretos en
  el gestor de Vercel y Trigger.dev, con rotación cada 90 días.
- **(b)** Un único login de aplicación con todos los roles de grupo.

**Recomendación: (a).** Limita el daño de una credencial filtrada y deja rastro por
componente. Pendiente de comprobar en Supabase: que `postgres` puede crear los
logins y ceder la propiedad (precondición 5 de
[pendientes SQL](cierre-sql-pendientes.md#precondiciones-bloqueantes-antes-de-aplicar-en-supabase)).
**Decisión:** ______

### B3. Planificador de particiones

- **(a)** `pg_cron` en Supabase con el rol dueño, una ejecución diaria de
  `ensure_monthly_partitions(horizonte 2)`. Una tarea de Trigger.dev lee
  `partition_status` y emite la alarma si `coverage_ok` es falso o
  `default_rows > 0`.
- **(b)** Todo en Trigger.dev, que se conecta con credencial del dueño.

**Recomendación: (a).** El DDL corre dentro de la base sin sacar la credencial del
dueño a un servicio externo, y Trigger.dev solo necesita leer. Condición: verificar
que Supabase Pro permite `pg_cron` con ese rol.
**Decisión:** ______

### B4. Filas que caen en la partición DEFAULT

Hoy, si la DEFAULT tiene filas de un mes, crear ese mes falla con
`LIBOX_PARTITION_DEFAULT_HAS_ROWS` y no se mueve nada.

- **(a)** Procedimiento de operación en una transacción, ejecutado por el dueño
  tras la alarma: crear la tabla del mes suelta, mover las filas desde la DEFAULT,
  adjuntarla. Queda como función separada con registro en `audit_events`, nunca
  automática.
- **(b)** Mantener el fallo y resolver cada caso a mano.

**Recomendación: (a).** La alarma ya avisa. Un procedimiento escrito evita
improvisar bajo presión.
**Decisión:** ______

### B5. Partición DEFAULT y ACL de `journal_lines`

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
**Decisión:** ______

### B6. Retención de los 4 padres sin regla

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
**Decisión:** ______

## C. Configuración por tipo de sorteo

Fuente: [lecturas y configuración](cierre-contratos-lecturas-configuracion.md#configuración-por-tipo-de-sorteo-solo-diseño).
El diseño de `RaffleConfiguration` ya existe. Falta decidir:

### C1. Política de expiración de T1 (I-09)

**Conflicto.** `raffle_type_rules` de T1 exige `expiry_policy_required`, pero no
hay campo que la guarde.

- **(a)** Campo `expiry_policy` con `max_duration_days` y la acción al vencer. La
  acción es un enum que habrá que elegir entre cancelar con reembolso o pasar a la
  ruta declarada.
- **(b)** T1 sin expiración: retirar la bandera de V8.

**Recomendación: (a).** Un sold-out sin plazo puede dejar dinero de compradores
inmovilizado indefinidamente. El reembolso lo ejecuta el código patrimonial humano;
aquí solo se decide el campo.
**Decisión:** ______

### C2. Duración de cada edición en T7

- **(a)** Cada edición dura el intervalo de la recurrencia y `end_at` se calcula al
  crearla.
- **(b)** Duración explícita por edición, independiente del intervalo.

**Recomendación: (a).** Evita solapamientos entre ediciones y un campo más que
validar.
**Decisión:** ______

### C3. Entrada de precio

**Conflicto.** Puede fijarla el organizador como `ticket_price` o como neto
objetivo, a partir del cual se calcula el precio. Es solo la decisión de producto:
el cálculo de comisión e impuesto es zona crítica.

- **(a)** El organizador fija `ticket_price`; se le muestra el neto estimado.
- **(b)** El organizador fija el neto; el sistema deriva `ticket_price`.

**Recomendación: (a).** El precio que ve el comprador es estable y el contrato no
depende de la fórmula de comisión.
**Decisión:** ______ (con visto del dueño contable)

### C4. Régimen económico (S-1) y enums de costos

- **Régimen.** Recomendación: solo `PAID` en el MVP. `FREE_ENTRY` y `PROMOTIONAL`
  necesitan diseñar la garantía sustitutiva (INV-06-b, INV-44). **Decisión:** ______
- **`cost_kind`, `charge_kind`, `macrozone`.** Sustituyen el JSONB de V7. No se
  proponen valores: pedir la lista a Diego a partir de los costos reales que ya
  asume (envío, notaría, registro). **Lista:** ______

## D. Sorteo

### D1. Fuente de aleatoriedad pública

La [propuesta de baliza](baliza-propuesta.md) sugiere evaluar **drand quicknet**.

- **(a)** Ratificar drand quicknet como fuente para que Diego fije la codificación
  y calcule los resultados esperados de los 5 vectores (H-10).
- **(b)** Evaluar otra fuente antes.

**Recomendación: (a)**, si la evaluación de la propuesta no deja dudas abiertas.
Los vectores, `verify_draw` y `server_seed` siguen siendo implementación humana
independiente.
**Decisión:** ______

## E. Datos que no se proponen

Estos valores no se infieren ni se proponen aquí. Deben venir de su dueño:

| Dato | Dueño | Bloquea |
|---|---|---|
| `fee_schedules`, `client_fee_levels` y valores financieros de `market_config_versions` | Diego y dueño contable | Configuración financiera (pendiente SQL #8) |
| Confirmación contable de H-01 a H-03 (`ledger_accounts`, inmutabilidad, privilegios de asiento) | Dueño contable | H-04 y el ledger |
| Política de pago tardío (H-16) | Diego | Pendiente SQL #10 |
| Secciones tributarias del documento de mercado | [LEGAL→ABOGADO] | `POST /markets/{code}/config` versionado |
| Custodia del dinero (ASS-001) | Diego | Dinero real |

## Después de decidir

1. Integrar las respuestas de A y C en el borrador OpenAPI y L3 V8, con pruebas.
2. Integrar B1 a B4 y B6 en el overlay y el manifiesto, y volver a ejecutar el runner.
3. Registrar como hallazgos de V8 las correcciones del canon: §3.16, §7.1, §1.3 y §11.5.
4. Actualizar [estado de C1](estado-c1.md). Lo que queda por cerrar C1 es la
   implementación humana y los datos del bloque E.
