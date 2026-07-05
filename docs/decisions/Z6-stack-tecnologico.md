---
title: Z.6 — Stack tecnológico
status: cerrada-en-direccion
tags: [libox, decision, stack, nextjs, arquitectura]
decided: 2026-06-06
relates: [docs/decisions/Z1-custodia-del-dinero.md, docs/decisions/Z2-eleccion-psp.md, docs/decisions/Z4-tipos-de-sorteo.md, docs/plans/libox-plan.md, docs/benchmark-stack.md]
updated: 2026-07-05
---

# Z.6 — Stack tecnológico

**Estado**: Cerrada en dirección (2026-06-06). Sub-decisiones ORM, auth y DB host **cerradas el 2026-07-05** con benchmark de mercado ([`benchmark-stack.md`](../benchmark-stack.md)). Pendiente al scaffold: job runner.
**Decisor**: Diego.
**Documento canónico**: este archivo. Mirror en [`docs/plans/libox-plan.md`](../plans/libox-plan.md) (sección 4 + Anexo Z.6).

---

## Decisión

**Next.js (App Router) como framework único** para todo Libox: superficie pública (SEO) y aplicación autenticada (dashboards, checkout, backoffice). Sobre ese núcleo: **PostgreSQL** + ORM TypeScript, un **job runner gestionado** para el trabajo en background (outbox, sorteos programados, conciliación), y un proveedor de **auth** con MFA.

---

## La pregunta que disparó la decisión: ¿Libox es una "web estática"?

Una web estática es HTML pre-generado, sin lógica de servidor por request ni datos tras login. Evaluando Libox superficie por superficie:

| Superficie | ¿Estática? |
|---|---|
| Landing / marketing | Sí |
| Catálogo público de sorteos | Casi (ISR/SSR; cambia con ventas) |
| Página pública de auditoría (post-sorteo) | Sí (proof inmutable) |
| Checkout / compra | No (transaccional, webhooks, idempotencia) |
| Dashboard organizador | No (autenticado, dinámico) |
| Dashboard participante | No (autenticado) |
| Backoffice admin | No (aprobaciones, disputas, settlement) |
| Motor sorteo / ledger / settlement | No (backend transaccional) |

**Conclusión: Libox NO es una web estática.** Es una **aplicación transaccional fintech-grade con una superficie de contenido estático**. Solo 2-3 de 8 superficies son estáticas; el core (comprar → sortear → entregar → liquidar) es dinámico y server-driven.

## Por qué no Astro

[Astro](https://astro.build) está optimizado para el caso **inverso**: sitios mayormente de contenido con "islas" de interactividad (manda 0 JS por defecto). Brilla en blogs, docs, marketing, catálogos. Aunque Astro 4+ soporta SSR y apps autenticadas, su sweet spot no es un producto que es 80% dashboards autenticados + backend transaccional, y su ecosistema para apps complejas (auth, estado, pagos) es **menos maduro** que el de Next.js.

Opciones evaluadas:

| Opción | Veredicto |
|---|---|
| **A. Next.js para todo** (elegida) | Next cubre la superficie estática (RSC + ISR → buen SEO) **y** las dashboards dinámicas, con un solo modelo mental y ecosistema maduro. |
| B. Astro (público) + app aparte | Dos frameworks que mantener; overhead alto para MVP de fundador solo. Solo valdría si el contenido fuera enorme. |
| C. Astro para todo | A contracorriente de su diseño; descartada. |

Next.js ya entrega lo que se buscaba de Astro (páginas públicas rápidas y SEO-friendly), y además es el tool correcto para el grueso del producto. Astro vuelve a ser candidato solo si más adelante se quiere un **sitio de marketing separado**.

---

## Stack recomendado

| Capa | Elección | Nota |
|---|---|---|
| Framework | **Next.js (App Router) + TypeScript** | Una sola codebase: público + app + backoffice por rol. |
| UI | **Tailwind + shadcn/ui** | Rápido, accesible. |
| DB | **PostgreSQL en Supabase** (cerrada 2026-07-05) | Transaccional, soporta el ledger y el append-only audit. Supavisor en **modo transacción** obligatorio desde el día 1 (serverless). |
| ORM | **Drizzle** (cerrada 2026-07-05) | Control fino del SQL, migraciones incluidas, cold starts 3-5x menores que Prisma en serverless. |
| Job runner | **Inngest** o **Trigger.dev** | Necesario para outbox worker, ejecución de sorteo por deadline/umbral, conciliación PSP. Evita Redis+worker propio en MVP. Confirmar al scaffold. |
| Auth | **Supabase Auth** (cerrada 2026-07-05) | MFA obligatorio para organizadores y staff (lo pide el PRD para Admin). RLS integrado. Ruta de migración: WorkOS al acercarse a ~100k MAU. |
| Pagos | **Mercado Pago** (ver [Z.2](Z2-eleccion-psp.md)) | Adaptador **multi-PSP** desde el inicio (Culqi 2º rail). |
| Hosting | **Vercel** + DB gestionada | Migrar a infra propia con tracción/compliance. |
| Observabilidad | **Sentry** + logs estructurados + **PostHog** | `trace_id` transversal (PRD). |

---

## Por qué Next.js full-stack (y no un backend separado ya)

El PRD pide outbox, ledger doble entrada, webhooks firmados, draw engine y multi-PSP — mucho backend transaccional. Aun así, para un MVP de 8-12 semanas con un dev, **Next.js full-stack (API routes + Server Actions) + job runner gestionado** es lo pragmático. El propio plan prevé **extraer un servicio dedicado** (NestJS/Fastify) cuando los jobs y la carga lo justifiquen. Diseñar los dominios con fronteras limpias (bounded contexts del PRD) hace esa extracción futura mecánica.

---

## Implicaciones de build

- **Monolito modular** con módulos = bounded contexts del PRD (Raffle, Pricing, Purchase, Draw, Delivery, Settlement, Risk, Audit, Notification, PSP Adapter, Backoffice).
- **El job runner es infraestructura crítica, no opcional**: la ejecución del sorteo por deadline/umbral ([Z.4](Z4-tipos-de-sorteo.md)) y el outbox worker dependen de él.
- Superficie pública (landing, catálogo, audit page) como **RSC + ISR/SSG**; app autenticada como componentes dinámicos. Misma codebase.

---

## Sub-decisiones cerradas (2026-07-05)

Cerradas con benchmark de mercado a julio 2026 — comparativas completas, costos y fuentes en [`benchmark-stack.md`](../benchmark-stack.md).

1. **ORM: Drizzle** (descarta Prisma). Cold starts 3-5x menores y bundle ~90% más chico en serverless (Vercel Functions). SQL-first — útil para las agregaciones del marketplace (tickets, rankings, settlement). Riesgo de lock-in mínimo: el esquema es SQL estándar, migrar a Kysely o SQL crudo sería mecánico. En cliente se complementa con `supabase-js` para CRUD simple protegido por RLS.
2. **Auth: Supabase Auth** (descarta Clerk). A 100k MAU: ~$187/mes vs ~$1,825/mes de Clerk — ~10x de diferencia para funcionalidad equivalente en este caso (email, OAuth social, MFA). Bonus: RLS de Postgres integrado con `auth.uid()` resuelve gran parte de la autorización sin código de backend. **Ruta de migración futura**: WorkOS AuthKit (gratis hasta 1M MAU) se reevalúa al acercarse a ~100k MAU; Supabase soporta proveedores de auth externos, así que la migración no obliga a cambiar de DB.
3. **DB host: Supabase** (descarta Neon). Neon es excelente Postgres serverless, pero solo DB: Libox necesita además realtime (contadores de tickets, estado del sorteo) y storage (imágenes de premios), que Supabase incluye en el plan Pro ($25/mes) junto con auth. Con Neon serían 3-4 proveedores adicionales por costo similar. Condición operativa: **Supavisor en modo transacción + prepared statements deshabilitados** desde el día 1 — causa #1 de incidentes Postgres-serverless en producción.

## Sub-decisión pendiente (al hacer scaffold)

1. Job runner: **Inngest** vs Trigger.dev.
