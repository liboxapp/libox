---
title: Benchmark de stack (julio 2026)
status: vigente
tags: [libox, stack, benchmark, supabase, drizzle, vercel]
updated: 2026-07-05
description: Comparativas de mercado que sustentan el cierre de las sub-decisiones de Z.6 (ORM, auth, DB host) — costos, escalabilidad y rutas de salida.
---

# Benchmark de stack — julio 2026

Análisis de mercado que sustenta el cierre de las sub-decisiones de
[Z.6 — Stack tecnológico](decisions/Z6-stack-tecnologico.md). Escala objetivo:
10k–100k usuarios en 12–18 meses. Criterio: costo como startup + escalabilidad
+ rutas de salida documentadas, no lo trending.

## DB host: Supabase vs Neon

Ambos son Postgres gestionado, pero productos distintos: Neon es solo la base
de datos (serverless, scale-to-zero, branching por PR); Supabase es un backend
completo sobre Postgres.

| Criterio | Supabase | Neon |
|---|---|---|
| Modelo | Compute fijo siempre activo | Serverless, scale-to-zero (~500ms cold start) |
| Pricing | Pro $25/mes (bundle completo) | $0.106/CU-hora + $0.35/GB-mes |
| Realtime | Incluido | No tiene |
| Storage archivos | Incluido | No tiene |
| Auth | Incluido (50k MAU gratis) | No tiene |
| Branching de DB | Básico | Excelente (por PR) |

**Veredicto: Supabase.** Libox necesita exactamente lo que Supabase bundlea:
realtime (contador de tickets, estado del sorteo), storage (imágenes de
premios) y auth. Con Neon serían 3-4 contratos adicionales por costo similar y
más superficie operativa para un equipo chico.

Condición operativa: el límite default es 100 conexiones — **Supavisor en modo
transacción + prepared statements deshabilitados desde el día 1** (obligatorio
con Vercel serverless). Es la causa #1 de incidentes "funcionaba en dev, cayó
en prod". Hay casos documentados de 50k+ usuarios activos en plan Pro.

## Auth: costos por MAU

| Servicio | Free tier | 50k MAU | 100k MAU |
|---|---|---|---|
| Clerk | 10k MAU | ~$825/mes | ~$1,825/mes |
| Supabase Auth | 50k MAU | ~$25/mes | ~$187/mes |
| WorkOS AuthKit | 1M MAU | $0 | $0 |
| Better Auth / Auth.js | ilimitado (self-hosted) | $0 | $0 |

**Veredicto: Supabase Auth.** ~10x más barato que Clerk a 100k MAU con
funcionalidad equivalente para este caso (email, OAuth social, MFA). RLS de
Postgres integrado con `auth.uid()` resuelve gran parte de la autorización sin
código de backend. Clerk solo se justifica con organizaciones B2B multi-tenant
y UI prefabricada — no es el caso.

**Ruta futura — WorkOS AuthKit**: gratis hasta 1M MAU (email, social, MFA);
cobra por SSO/SCIM enterprise ($125/conexión/mes) y dominio custom ($99/mes).
No se adopta de entrada porque auth es solo 1 de las 3 piezas que Supabase
bundlea y el ahorro (~$160/mes) aparece recién cerca de 100k MAU. Se reevalúa
al acercarse a ese umbral; Supabase soporta auth externo, así que la migración
no toca la DB.

## ORM: Drizzle vs Prisma

En serverless los cold starts mandan: Drizzle arranca en <500ms vs 1-3s de
Prisma pre-v7, con bundle ~90% menor. Prisma 7 cerró parte de la brecha, pero
Drizzle sigue ganando en bundle y es el default actual de T3 Stack, Epic Web y
Astro DB. SQL-first: útil para agregaciones del marketplace (tickets, rankings,
settlement) y coherente con Supavisor en modo transacción.

**Veredicto: Drizzle en servidor + `supabase-js` en cliente** (CRUD simple
protegido por RLS). Descartados TypeORM/MikroORM (orientados a servidor
persistente). Lock-in mínimo: esquema SQL estándar, migrar a Kysely o SQL crudo
sería mecánico.

## Hosting: Vercel con regla de salida

| Escenario | Vercel | Cloudflare Workers | Railway |
|---|---|---|---|
| MVP (Pro) | ~$67/mes mediana real | ~$5-15/mes | ~$20-50/mes |
| 250k visitas/mes | ~$305/mes | ~$15/mes | ~$116/mes |
| 1.5M visitas, 10TB egress | ~$3,100/mes | ~$150-300/mes | escala lineal |

El costo de Vercel a escala lo domina el bandwidth (Fast Data Transfer
$0.15/GB + Edge Requests $2/M), no el compute. **Regla de salida**: si el bill
supera ~$300/mes y es mayormente bandwidth, migrar a Cloudflare (Next.js corre
en Workers vía OpenNext) o Railway. Regla dura: el video en vivo (T8 LIVE,
[Z.5](decisions/Z5-t8-live.md), MVP-3) jamás pasa por Vercel — a $0.15/GB sería
ruinoso.

## Streaming (referencia para MVP-3 / Z.5)

Cloudflare Stream: $5/1,000 min almacenados + $1/1,000 min entregados, sin fee
de encoding (Mux es 5-8x más caro; LiveKit es para video bidireccional que no
se necesita). Stream Connect permite simulcast de 1 feed RTMPS/SRT hasta 50
destinos (Kick/YouTube/Twitch). Alternativa $0: embeber el player oficial de
esas plataformas; nunca capturar y redistribuir su feed (viola ToS).

## Proyección de costos del stack

| Etapa | Costo mensual estimado |
|---|---|
| MVP (<10k usuarios) | ~$45-70 |
| 50k usuarios | ~$150-350 |
| 100k usuarios | ~$300-600 |

Equivalente con Clerk + Vercel sin control de bandwidth: $2,500-4,000/mes.
Principio transversal: todo es Postgres estándar y cada pieza tiene salida
documentada (Vercel→Cloudflare, Supabase→cualquier Postgres, Drizzle→SQL).

## Fuentes principales

- Supabase vs Neon: [Bytebase](https://www.bytebase.com/blog/neon-vs-supabase/), [designrevision](https://designrevision.com/blog/supabase-vs-neon)
- Auth: [Makerkit — Better Auth vs Clerk vs Supabase](https://makerkit.dev/blog/tutorials/better-auth-vs-clerk), [WorkOS pricing](https://workos.com/pricing)
- Hosting: [Makerkit — Vercel cost](https://makerkit.dev/blog/saas/vercel-cost), [Cloudflare Workers vs Vercel](https://www.morphllm.com/comparisons/cloudflare-workers-vs-vercel)
- Supabase en producción: [arquitectura 2026](https://www.frontendtechlead.com/blog/supabase-production-architecture-2026), [connection management](https://supabase.com/docs/guides/database/connection-management)
- ORM: [Makerkit — Drizzle vs Prisma](https://makerkit.dev/blog/tutorials/drizzle-vs-prisma), [Bytebase](https://www.bytebase.com/blog/drizzle-vs-prisma/)
- Streaming: [Cloudflare Stream simulcasting](https://developers.cloudflare.com/stream/stream-live/simulcasting/), [comparativa de video](https://www.buildmvpfast.com/api-costs/video)
