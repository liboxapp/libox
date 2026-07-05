---
title: MVP-1 — Fases de desarrollo
status: propuesta
tags: [libox, mvp1, fases, arquitectura, ejecucion]
updated: 2026-07-03
---

# MVP-1 — Fases de desarrollo

Plan de ejecución del **MVP-1 "comprar → sortear"** definido en el [plan](libox-plan.md) (sección 6) y las decisiones Z.1–Z.8. Este documento no redefine alcance: lo **ordena en fases construibles**, con criterios de salida (DoD) y dependencias, para que un dev full-time pueda arrancar.

> **Estado: propuesta.** Las sub-decisiones de stack (sección 2) requieren decisión de socios/Diego antes de la Fase 1. Una vez decididas, se cierran según la convención de ADRs (amendment a Z.6 o Z.9 nueva).

---

## 1. Evaluación de la arquitectura actual (¿es segura para arrancar?)

**Veredicto: el stack de Z.6 es adecuado para MVP-1. No se necesita rediseño.** Next.js modular monolith + PostgreSQL + job runner gestionado es un patrón probado para productos transaccionales de este tamaño. El riesgo de Libox **no está en el stack, está en la disciplina de implementación**: idempotencia, transacciones, append-only y los dos gates externos (MP y abogado). Lo que sigue es lo que hay que hacer *bien* dentro del stack elegido — no cambiarlo.

### 1.1 Fortalezas que ya tenemos

- **Cero alcance PCI**: con Checkout de Mercado Pago (hosted/redirect), los datos de tarjeta **nunca tocan nuestros servidores**. No hay que certificar PCI-DSS; solo proteger tokens y webhooks.
- **Modelo C (Z.1) reduce riesgo regulatorio y de seguridad**: al no custodiar dinero, no somos objetivo de robo de fondos; el split lo ejecuta el PSP.
- **PRD fintech-grade como guía**: invariantes, outbox, ledger y draw proof ya están especificados — no hay que inventar arquitectura, hay que implementarla.

### 1.2 Puntos que exigen disciplina (mejoras dentro del stack)

| # | Riesgo | Mitigación (se implementa en las fases) |
|---|---|---|
| 1 | **Webhooks en serverless** (timeouts, cold starts, replays) | Patrón *ack-then-process*: el endpoint verifica firma (`x-signature` MP, ventana ≤300s), persiste el evento crudo, responde 200 y delega el procesamiento al job runner. `processed_webhooks UNIQUE(payment_id)`. |
| 2 | **Concurrencia en últimos boletos** | Asignación atómica en Postgres: `UPDATE … WHERE status='available' … FOR UPDATE SKIP LOCKED` + `UNIQUE(raffle_id, numero)`. Nunca lógica de reserva en memoria. |
| 3 | **Conexiones DB desde serverless** | Driver HTTP/pooler del proveedor (Neon serverless driver o pooler de Supabase). Prohibido abrir conexiones TCP directas por request. |
| 4 | **Atomicidad dinero-boleto-ledger** | Ticket, asiento de ledger y evento outbox se escriben **en la misma transacción**. El invariante `debit=credit` se verifica por job de conciliación. |
| 5 | **Append-only real, no por convención** | `audit_events` sin permisos de `UPDATE/DELETE` para el rol de la app (revoke a nivel DB + trigger de rechazo), hash-chain (`prev_hash`), `trace_id` propagado vía middleware. |
| 6 | **Disparo de sorteo por deadline/umbral** | El job runner es **infraestructura crítica** (Z.6): cron + steps con retries. Jamás depender de un request de usuario para ejecutar un sorteo. |
| 7 | **Secretos y entornos** | 3 entornos (dev / staging / prod) con DB y credenciales MP separadas (sandbox en dev/staging). Secretos solo en env vars de Vercel; nunca en el repo (ya cubierto por `.gitignore` + secret scanning de la org). |
| 8 | **MFA y roles** | MFA obligatorio para organizadores y staff desde el día 1 (lo exige el PRD para Admin). RBAC en capa de aplicación con middleware por rol; el backoffice vive bajo el mismo monolito pero con guard dedicado y `reason_required` en overrides. |

### 1.3 Lo que NO haríamos ahora (sobre-ingeniería para esta etapa)

- Microservicios o backend separado (NestJS/Fastify) — el plan ya prevé extraerlo *cuando los jobs lo justifiquen*; hoy añade costo sin beneficio.
- Escrow real / cuentas propias (eso es post-MVP, Z.1).
- Kubernetes/infra propia, colas Redis propias, event bus dedicado — el outbox sobre Postgres + job runner cubre MVP-1.

---

## 2. Sub-decisiones de stack a cerrar ANTES de Fase 1 (decisión de socios)

Z.6 dejó 4 sub-decisiones "al scaffold". Recomiendo cerrarlas como **bundle** para minimizar fricción de integración:

| Sub-decisión | Bundle A — recomendado | Bundle B — alternativa |
|---|---|---|
| Auth | **Clerk** (MFA out-of-the-box, orgs nativas) | Supabase Auth (más barato, MFA manual) |
| DB host | **Neon** (branching de DB por PR, driver serverless) | Supabase (DB+Auth+Storage en un vendor) |
| ORM | **Drizzle** (ya preferido en Z.6) | Drizzle (igual en ambos) |
| Job runner | **Inngest** (steps, cron, retries; DX Vercel) | Trigger.dev |

- **Bundle A** (Clerk + Neon + Drizzle + Inngest): mejor separación de responsabilidades y mejor DX para el patrón webhook/jobs. Costo algo mayor (~$0 en tiers free al inicio; escala por MAU de Clerk).
- **Bundle B** (Supabase todo-en-uno + Trigger.dev): menos vendors y menor costo a mediano plazo; MFA y organizaciones requieren más trabajo manual.

**Decisiones adicionales chicas** (no bloquean Fase 1, sí bloquean su fase):

1. **Fuente de entropía externa** (bloquea F5): recomiendo **drand (League of Entropy)** — beacon público, verificable por cualquiera vía HTTP, sin dependencia de blockchain. Alternativa: NIST Randomness Beacon.
2. **Proveedor de consulta RUC/padrón SUNAT** (bloquea F2): apisperu / apis.net.pe / Migo — elegir por SLA y costo; el adaptador se diseña intercambiable.
3. **PSE de facturación** (bloquea F6): Nubefact como candidato principal (plan §2.3). `[LEGAL→ABOGADO]` el modelo de emisión (organizador = merchant of record) debe ratificarse antes de integrar.
4. **Fecha de la llamada comercial a MP** (bloquea F4): las preguntas eliminatorias de Z.2 siguen abiertas. **Es el mayor riesgo del cronograma.**

---

## 3. Fases

Cada fase tiene: objetivo, entregables, criterio de salida (DoD) y dependencias. Duraciones para **1 dev full-time**.

### Fase 0 — Gates y fundación del repo (1 semana, parcialmente en paralelo con F1)

**Objetivo:** despejar los bloqueos externos y dejar el terreno listo.

- Llamada comercial a **Mercado Pago** (batería de Z.2; preguntas 1-2 eliminatorias). Contingencia: si MP falla split+Yape → misma batería a Culqi y se reevalúa el primario (gate de F4, no de F1-F3).
- Cerrar **bundle de stack** (sección 2) → registrar como amendment de Z.6 / ADR nuevo.
- Crear cuentas/proyectos: Vercel (team liboxapp), DB (Neon/Supabase), auth, job runner, Sentry, PostHog. Sandbox de MP.
- **Scaffold** Next.js (App Router + TS + Tailwind + shadcn/ui) con layout de monolito modular: `src/modules/<bounded-context>/` (raffle, purchase, draw, ledger, audit, identity, psp, backoffice) con fronteras explícitas (el PRD §II manda los contexts).
- CI ampliada (Z.7 §Evolución): `typecheck`, `test`, `build` como required checks junto a los actuales; `release-type` → `node`.
- **DoD:** repo despliega "hello world" autenticable en staging; CI verde con los 6 checks; bundle decidido y documentado.

### Fase 1 — Fundaciones transversales (1.5 semanas)

**Objetivo:** los cimientos que todos los módulos consumen. Es la fase que más caro cuesta corregir después.

- Esquema base Drizzle + migraciones versionadas (`organizations`, `users`, `roles`).
- **Auth + RBAC**: roles participante / organizador / staff-admin; MFA activable (obligatorio organizador+staff); guards por segmento de ruta.
- **`audit_events` append-only**: tabla con `trace_id`, `payload_hash`, `prev_hash` (hash-chain), `previous_state/new_state`, `event_version`; permisos DB sin UPDATE/DELETE; helper `audit()` usable desde cualquier módulo.
- **`trace_id` transversal**: middleware + AsyncLocalStorage; presente en logs, DB y respuestas.
- **Outbox**: tabla `event_outbox` + worker en el job runner con retries y DLQ.
- Observabilidad: Sentry + logs estructurados JSON; PostHog básico.
- **DoD:** un evento de dominio de prueba viaja `acción → tx con outbox → worker → audit_event` con el mismo `trace_id` visible en logs; tests de la hash-chain.

### Fase 2 — Identidad y onboarding de organizadores (1.5 semanas) — [Z.3]

**Objetivo:** cualquier persona/empresa con RUC activo puede registrarse y quedar aprobada.

- Registro de organización con **2 plantillas KYC** (jurídica / natural-con-RUC); `Organization.tipo` no hardcodeado.
- Validación de RUC contra padrón SUNAT (adaptador intercambiable por proveedor).
- Carga de documentos (autorización municipal, representante legal) a storage privado.
- **Backoffice v0**: cola de aprobación de organizadores con `reason_required` y auditoría de cada cambio de estado.
- Máquina de estados del organizador: `draft → en_revision → aprobado / rechazado / suspendido`.
- **DoD:** flujo E2E manual: registro → validación RUC → aprobación por staff → organizador puede entrar a su dashboard. Todo auditado.

### Fase 3 — Catálogo y ciclo de vida del sorteo (1.5 semanas) — [Z.4 parcial]

**Objetivo:** el organizador crea sorteos; el público los ve.

- CRUD de sorteo con `draw_config` **versionado** (disparo umbral/fecha/ambos, precio, total de boletos — presets T1-T4 como configuración, no como motores).
- Máquina de estados del sorteo: `borrador → en_revision → aprobado → activo → cerrado → ejecutado / fallido → liquidado`.
- Aprobación manual desde backoffice (extiende F2).
- **Catálogo público** con ISR/SSR (SEO) + página de detalle.
- **DoD:** sorteo creado, aprobado y visible públicamente; `draw_config` inmutable una vez activo (nueva versión si cambia antes de aprobar); property tests de la máquina de estados.

### Fase 4 — Compra, pagos y ledger (3 semanas) — [Z.1, Z.2] ⚠️ fase crítica

**Objetivo:** vender boletos con dinero real dividido en la fuente, sin perder ni duplicar un céntimo.

> **Gate de entrada:** verificación comercial MP aprobada (F0). Sin eso, esta fase solo puede avanzar en sandbox y con el adaptador abstracto.

- **Adaptador PSP multi-proveedor** (interfaz común; MP primera implementación — Z.2 exige diseño multi-PSP desde día 1).
- Onboarding del organizador a MP (OAuth/cuenta vendedor + KYC del PSP) integrado al flujo de F2.
- Checkout con **split en la fuente** (~80/20) usando el checkout hosted de MP (Yape incluido dentro).
- **Asignación de boletos concurrente-segura**: `FOR UPDATE SKIP LOCKED` + unique constraints; `Idempotency-Key` en todos los commands.
- **Webhooks**: verificación de firma, ventana anti-replay ≤300s, `processed_webhooks` único, patrón ack-then-process vía job runner.
- **Ledger doble entrada** con las 8 cuentas del PRD; asientos en la misma tx que el boleto; job de conciliación `debit=credit` por lote + contra reportes de settlement del PSP (gate `PSP_RECONCILED`).
- **Refunds**: ruta de devolución vía PSP (la consume F5 cuando un sorteo falla).
- **DoD:** invariante "no existe ticket sin order PAID" cubierto por tests; compra E2E en sandbox con split verificado; doble webhook del mismo pago = un solo efecto; ledger balancea; refund E2E en sandbox.

### Fase 5 — Motor de sorteo y fairness (2 semanas) — [Z.4, Z.5-compatible]

**Objetivo:** ejecutar sorteos demostrablemente justos, automáticos o manuales, con refund si fallan.

- **Pool freeze**: `POOL_FROZEN` como estado y evento; `canonical_pool` ordenado + `pool_hash = sha256(...)` publicado **antes** de la entropía.
- **Entropía externa** (drand): commit del round futuro al congelar; reveal al ejecutar. `seed_material` y `random_value` según fórmula del PRD; `algorithm_version` versionado.
- Disparo **AUTO** por job runner (umbral alcanzado / fecha límite) y **manual con aprobación admin** (`reason_required`).
- **Fallo del sorteo** (no se alcanzó condición): transición a `fallido` + refunds automáticos masivos vía F4.
- `mode` enum con `LIVE` previsto pero deshabilitado (Z.5: additivo en MVP-3).
- **Draw proof reproducible**: artefacto JSON con pool_hash, entropía, seed, random_value, winner_index — verificable offline por un tercero.
- **DoD:** property-based tests del algoritmo (release gate del PRD); "no existe draw sin POOL_FROZEN" cubierto; sorteo E2E: venta → freeze → entropía → ganador → proof publicado; sorteo fallido E2E con refunds.

### Fase 6 — Auditoría pública y comprobantes (1.5 semanas)

**Objetivo:** cerrar el ciclo de confianza (público) y el fiscal (SUNAT).

- **Página pública de auditoría por sorteo**: proof descargable, verificación reproducible explicada, lista de boletos hasheada. SSG/ISR (es inmutable post-sorteo).
- Integración **PSE** (Nubefact u otro): comprobante emitido por el organizador por cada venta. `[LEGAL→ABOGADO]` ratificar modelo de emisión antes de activar en prod.
- Notificaciones transaccionales mínimas (email): compra confirmada, sorteo ejecutado, ganador.
- Dashboard mínimo del organizador: ventas, estado del sorteo, link de auditoría.
- **DoD:** un tercero sin acceso al sistema puede verificar un ganador con el proof público; comprobante de prueba emitido en sandbox del PSE.

### Fase 7 — Hardening y piloto (1.5 semanas)

**Objetivo:** de "funciona" a "confiable frente a terceros".

- Suite E2E de los 5 flujos críticos (los mismos de los wireframes del plan).
- Los **7 invariantes del PRD** como suite de release gate en CI.
- Revisión de seguridad: rate limiting en endpoints sensibles, headers, validación de inputs (zod en todos los boundaries), revisión de permisos DB, dependencias (`npm audit` en CI).
- Runbooks mínimos: webhook caído, sorteo no disparado, conciliación descuadrada.
- **Piloto**: onboarding manual de 3–5 organizadores reales en staging/producción limitada.
- Checklist legal previo a lanzamiento (compliance-peru con abogado) — gate de **lanzamiento**, no de construcción.
- **DoD:** piloto ejecuta al menos 1 sorteo real de punta a punta; postmortem del piloto documentado.

---

## 4. Secuencia y estimación

```
F0 Gates+scaffold ─┬─► F1 Fundaciones ─► F2 Onboarding ─► F3 Sorteos ─► F4 Pagos ─► F5 Draw ─► F6 Audit+PSE ─► F7 Piloto
                   │                                                      ▲
   llamada MP ─────┴──────────────────────────── gate de entrada ─────────┘
```

- F2/F3 pueden solaparse parcialmente si F1 quedó sólida.
- **Total: ~13 semanas** de trabajo efectivo (1 dev full-time). El rango honesto es **12–16 semanas**: la estimación de 8–12 del plan es alcanzable solo si la llamada MP sale a la primera y no hay retrabajos en F4. El nivel de exigencia del PRD (ledger, outbox, proof) está en F4-F5; ahí es donde no se recorta.
- Qué se puede recortar si urge fecha: F6 (PSE puede entrar post-piloto si el abogado lo permite) y el dashboard del organizador (mínimo viable). Qué **no** se recorta: idempotencia, ledger, append-only, proof.

## 5. Calidad como política transversal

- **TDD en los caminos de dinero y sorteo** (F4-F5): tests primero para asignación concurrente, webhooks duplicados, ledger, algoritmo de draw.
- **Property-based testing** del motor de sorteo (release gate, PRD §IX).
- Los 7 invariantes del PRD viven como tests en CI desde la fase que los introduce.
- Cada PR: rebase-and-merge, Conventional Commits, checks verdes (política Z.7 + ruleset).

## 6. Decisiones que los socios deben tomar ahora

1. **Bundle de stack A o B** (sección 2) — bloquea F0/F1. *Recomendación: A.*
2. **Responsable y fecha de la llamada a MP** — bloquea F4; mayor riesgo del cronograma.
3. Fuente de entropía (*drand* recomendado) — bloquea F5.
4. Proveedor de consulta RUC — bloquea F2.
5. PSE + ratificación legal del modelo de emisión — bloquea F6.
