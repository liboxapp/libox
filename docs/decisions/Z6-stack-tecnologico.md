---
title: Z.6 — Stack tecnológico
status: cerrada-en-direccion
tags: [libox, decision, stack, nextjs, arquitectura]
decided: 2026-06-06
relates: [docs/decisions/Z1-custodia-del-dinero.md, docs/decisions/Z2-eleccion-psp.md, docs/decisions/Z4-tipos-de-sorteo.md, docs/plans/libox-plan.md]
updated: 2026-06-06
---

# Z.6 — Stack tecnológico

**Estado**: Cerrada en dirección (2026-06-06). Sub-decisiones (ORM, auth, job runner) a confirmar al hacer el scaffold.
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
| DB | **PostgreSQL** (Neon/Supabase para MVP) | Transaccional, soporta el ledger y el append-only audit. |
| ORM | **Drizzle** (preferido) o Prisma | Drizzle por control fino del SQL y migraciones; confirmar al scaffold. |
| Job runner | **Inngest** o **Trigger.dev** | Necesario para outbox worker, ejecución de sorteo por deadline/umbral, conciliación PSP. Evita Redis+worker propio en MVP. |
| Auth | **Clerk** o **Supabase Auth** | MFA obligatorio para organizadores y staff (lo pide el PRD para Admin). |
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

## Sub-decisiones pendientes (al hacer scaffold)

1. ORM definitivo: **Drizzle** vs Prisma.
2. Job runner: **Inngest** vs Trigger.dev.
3. Auth: **Clerk** vs Supabase Auth.
4. DB host: **Neon** vs Supabase.
