---
title: Revisión de sistema — hallazgos técnicos del canon
status: borrador
tags: [libox, arquitectura, linea-base, hallazgos, l3]
updated: 2026-09-25
description: Defectos de L3 V7, el SQL y el OpenAPI que impiden construir tal cual. Candidatos a registrar por CD-07 y a corregir en L3 V8.
---

# Revisión de sistema — hallazgos técnicos del canon

Parte de la [revisión de diseño de sistema](2026-09-25-revision-sistema-mvp-design.md). Nada se corrige aquí: la línea base está congelada (CD-07). Cada hallazgo se registra con `libox-registrar-hallazgo` y, si se aprueba, se corrige en una nueva versión de [L3](../../linea-base/LIBOX_ESPECIFICACION_TECNICA_L3_V7.md).

Los marcados **(v)** están verificados contra el texto; el resto sale de la lectura completa de L3 V7 y lleva la línea para contrastarlo. Severidad: **B** bloquea construir el módulo · **A** riesgo alto si se construye así · **M** corregir antes de su épica.

## Dinero y ledger

| # | Sev | Hallazgo | Referencia |
|---|---|---|---|
| H-01 | B | **(v)** El control L-04 (INV-16, suficiencia de reembolso) falla con cualquier orden pagada. Al aprobarse el pago, T-01 acredita `purchase_liability` por el bruto y, en el mismo momento, T-04 y T-05 lo debitan por comisión y neto. Como bruto = comisión + neto, el saldo queda en 0. | §6.3 (l.3194–3224, 3343) · L-04 (l.3357) |
| H-02 | B | **(v)** No existe T-03. Además, ninguna transacción debita `cash_clearing` ni asienta un reembolso al medio de pago original. | §6 |
| H-03 | A | Reconocer comisión e impuesto al cobrar, antes del sorteo y de la entrega, es un riesgo contable y tributario. [LEGAL→ABOGADO] | §6.3 |
| H-04 | M | El cuadre solo se valida al insertar la cabecera del asiento; `account_code` no tiene FK a `ledger_accounts`; la coherencia de moneda anunciada no está implementada. | l.2009, 2025–2042 |

Propuesta para H-01 y H-03: diferir T-04, T-05 y T-06 al momento "liquidación elegible". Mantiene la suficiencia de reembolso y alinea el reconocimiento de ingreso con la entrega. Requiere confirmación contable.

## Base de datos desplegable

| # | Sev | Hallazgo | Referencia |
|---|---|---|---|
| H-05 | B | **(v)** Las 12 tablas con `PARTITION BY` no tienen ninguna partición creada (0 `PARTITION OF`): todo `INSERT` en ellas falla, incluidas `audit_events`, `event_outbox` y `journal_lines`. | `libox_schema_L3_V7.sql` |
| H-06 | B | **(v)** Hay 5 `REVOKE` y 0 `GRANT`. Los roles son `NOLOGIN` y los revokes no protegen nada: el "solo agregar" de C-08 no rige en la base. | `libox_schema_L3_V7.sql` |
| H-07 | A | **(v)** INV-38: el changelog V6 promete "mínimo dos titulares activos" de ADMIN_SUPER y el trigger solo falla con `n < 1`. | l.36 · l.2787–2803 |
| H-08 | A | Faltan procedimientos y triggers que la prosa promete: cambio de estado único de `raffles` (§4.2), trigger de incompatibilidades INC y semillas de `fsm_transitions`, `ledger_accounts`, mercado PE y primer administrador. | §4.2 · Anexo A |
| H-09 | A | Re-otorgar un rol revocado es un `UPDATE` (por `UNIQUE(user_id, subrole)`) y se salta el trigger `BEFORE INSERT` de techo de privilegio y segunda firma. | l.2710, 2783 |

## Sorteo

| # | Sev | Hallazgo | Referencia |
|---|---|---|---|
| H-10 | B | Los 5 vectores de prueba no traen resultados esperados (`pool_hash`, `commitment`, ganadores): "debe reproducirlos exactamente" no se puede comprobar. | §5.7 (l.3113–3164) |
| H-11 | A | `verify_draw` confunde el identificador de ronda con el valor de la baliza; dos implementaciones honestas pueden divergir. | l.3085–3111 frente a §5.3 |
| H-12 | A | No hay dónde guardar `server_seed` cifrada entre compromiso y ejecución, ni timeout o respaldo si la baliza no publica la ronda. La fuente de baliza está sin elegir. | l.3004, 3691, 3712 |

## Contratos, seguridad y operación

| # | Sev | Hallazgo | Referencia |
|---|---|---|---|
| H-13 | B | **(v)** El OpenAPI tiene 16 operaciones y L3 §11 enumera al menos 43 rutas distintas. La Evaluación estimó ~30 y cotizó T-1 en 8 SP: probablemente subestimado. Usa `nullable`, que no existe en OpenAPI 3.1. | OpenAPI · §11 (l.3752–3864) |
| H-14 | A | **(v)** `document_number_hash` es un SHA-256 del documento. Con ~10⁸ DNI posibles se revierte por fuerza bruta: debe ser un HMAC con clave secreta. | l.379 |
| H-15 | A | **(v)** L3 no define RPO, RTO, backups ni recuperación ante desastres, en un sistema con ledger de solo agregación. | L3 completo |
| H-16 | M | Pago aprobado después de expirar la reserva o de congelar el pool: no hay política, con riesgo de ticket fuera del pool. | l.1492–1496, 3884 |
| H-17 | M | Sin política de rate limiting (solo el código `ERR_AUTH_RATE_LIMITED`); sin TLS, WAF ni CSP declarados. | l.3452 |

## Versiones

| # | Sev | Hallazgo | Referencia |
|---|---|---|---|
| H-18 | A | **(v)** §0.3 fija **.NET 8 LTS**, cuyo soporte termina el 10-nov-2026 según la política de Microsoft, antes de acabar R0. Fija Next.js 14; el código ya usa 16.3. | l.158–168 |
| H-19 | M | El pie de L3 cita "PRD BLUEPRINT MVP V4", el encabezado V8 y §0.1 V9; el OpenAPI declara PRD V8. | l.4133 · l.5 |

## Fuera de L3: repo y plan

- `CONTRIBUTING.md` exige Drizzle, Supabase e Inngest y nombra tablas que el SQL no tiene (`webhook_inbox`, `outbox`); `src/CLAUDE.md` dice "stack cerrado — ADR Z.6". Son dos fuentes de stack en conflicto con §0.3.
- `.github/CODEOWNERS` apunta a rutas que se movieron a `docs/archive/`.
- **(v)** Ningún workflow compila, testea ni linta código: al levantar el freeze, un PR puede romper `src/` sin que el CI lo note.
- Backlog: dos numeraciones L-xx incompatibles (Dossier L-01–L-22 frente a PRD Anexo C L-01–L-12), totales de 739, 745 y 936 SP mezclados, e historias sin traza para alta de organizador, notificaciones, reputación y cotización de envío.
- `verify_corpus.py` sin `--dir` apunta a `.` y reporta 15 fallos falsos.
