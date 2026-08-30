---
title: Rate limiting — estándar transversal
status: aprobado
tags: [libox, seguridad, rate-limiting, spec]
updated: 2026-08-11
description: Diseño en capas del rate limiting (Vercel WAF + Upstash Redis). Entra como fundación en Fase 1 y rige como política estándar para todo endpoint nuevo.
---

# Rate limiting — estándar transversal

Aprobado por Diego (2026-08-11). Hasta ahora el rate limiting existía solo
como bullet de revisión en Fase 7 (hardening) del
[plan de fases](../../archive/plans/mvp1-fases-desarrollo.md); con el backend
entrando en las próximas rebanadas, se adelanta como **fundación de Fase 1**
y queda como **política estándar** en
[`src/CLAUDE.md`](../../../src/CLAUDE.md). La pieza nueva de stack
(Upstash Redis) se registra como sub-decisión en
[ADR Z.6](../../archive/decisions/Z6-stack-tecnologico.md).

## Decisión de enfoque

Se evaluaron tres enfoques para la capa fina:

| | A. Solo WAF | B. WAF + Upstash Redis (elegido) | C. WAF + limiter en Postgres |
|---|---|---|---|
| Límites por usuario | No (solo IP/JA4) | Sí, contador global exacto | Sí |
| Vendor nuevo | No | Sí (free tier ~500k comandos/mes) | No |
| Costo en hot path | Ninguno | ~1-5 ms por chequeo | Un write en la DB por request |
| Políticas en el repo | No (config dashboard) | Sí, junto a cada endpoint | Sí, pero código propenso a races |

**Se elige B.** A no puede expresar "10 intentos de checkout por usuario
por minuto": el WAF de Vercel (no-Enterprise) solo cuenta por IP o JA4 y sus
contadores son por región del edge, así que N regiones pueden exceder el
límite configurado ~N veces. C carga con el tráfico abusivo a la misma base
que se busca proteger (más presión sobre Supavisor). B usa el patrón
estándar del stack (`@upstash/ratelimit`) con contador global exacto y
políticas declaradas en código, testeables con Vitest.

## Arquitectura en 4 capas

1. **L0 — Mitigación DDoS de la plataforma.** Automática en Vercel para
   todos los planes, gratis. No hay nada que construir.
2. **L1 — Reglas WAF de Vercel (config, no código).** Límite grueso por IP
   sobre la superficie API + reglas `deny` para rutas de exploit
   (`/wp-admin`, `/.env`, …). Se gestionan con el CLI `vercel firewall`
   (drafts + publish) y el set de reglas se espeja como script en el repo
   para que la config no derive en silencio. Entra en **modo log** con
   Fase 1 y se endurece con datos reales en Fase 7. El tráfico bloqueado
   por el WAF no se factura.
3. **L2 — Limiter de aplicación (código; el núcleo de este diseño).**
   `@upstash/ratelimit` + Upstash Redis (integración del marketplace de
   Vercel), ventana deslizante. Un helper (`src/lib/rate-limit.ts`) + un
   **registro de políticas**: cada endpoint sensible declara la suya junto
   a su código, o su **exención explícita**.
4. **L3 — Guardas de dominio (ya especificadas en F4 del plan).**
   Idempotency keys, firma + anti-replay ≤300s en webhooks, máximo de
   boletos por orden (Z.4) y los rate limits integrados de Supabase Auth
   para OTP/email — se configuran, no se reimplementan.

## Semántica del limiter (L2)

- **Clave**: `auth.uid()` si hay sesión; IP (cabecera confiable de Vercel)
  si no.
- **Route Handlers**: responden `429` + `Retry-After`.
- **Server Actions**: devuelven un rechazo tipado que la UI renderiza
  (copy es-PE).
- **Fail-open**: si Redis no responde, la request pasa (el WAF sigue
  protegiendo; una caída del limiter no puede bloquear el checkout) y se
  emite alerta a Sentry.
- **Webhooks exentos de L2**: un burst del PSP es legítimo; su protección
  es la firma y el anti-replay, no un contador.
- **Jobs de Inngest exentos**: tráfico interno, no de usuarios.

## Políticas iniciales

Valores iniciales deliberados — se ajustan en Fase 7 con datos del modo log.

| Endpoint | Política | Capa |
|---|---|---|
| Checkout / creación de orden (POST) | 10/min por usuario | L2 |
| Consulta RUC (API SUNAT pagada, F2) | 5/min y 20/día por usuario | L2 |
| Auth (login, signup, OTP) | Defaults de Supabase Auth; revisar en F2 | L3 |
| Catálogo público (GET) | Solo WAF (es ISR/caché) | L1 |
| Verificación pública del sorteo | WAF + 60/min por IP | L1/L2 |
| Webhooks PSP | Exentos de L2; firma + anti-replay | L3 |
| Baseline API (`/api/*`) | 300 req/60s por IP, modo log inicial | L1 |

## Qué entra ahora vs Fase 1

**Ahora (este PR, solo docs)**: este spec; edición del plan de fases
(bullet en F1, política transversal en §5, F7 pasa de "agregar" a
"auditar"); sub-decisión 5 en Z.6; política estándar en `src/CLAUDE.md`.

**Al arrancar Fase 1 (código, vía writing-plans)**:

1. Provisionar Upstash Redis por el marketplace de Vercel (env vars
   `UPSTASH_REDIS_REST_URL` / `UPSTASH_REDIS_REST_TOKEN`).
2. Helper `src/lib/rate-limit.ts` + registro de políticas tipado.
3. Reglas WAF baseline (script espejo en el repo) en modo log.
4. Aplicar políticas a los endpoints que la propia F1 exponga.

### Criterios de aceptación (implementación en F1)

- Tests unitarios de derivación de clave y selección de política.
- Test de integración del camino 429 (limiter mockeado).
- Un endpoint sin política declarada ni exención **no pasa review** —
  regla en `src/CLAUDE.md`.
- Reglas WAF visibles con `vercel firewall rules list` y espejadas en el
  repo.

## Rollout de reglas WAF (staged)

`log` en todas partes → revisar tráfico en el dashboard → enforce en
preview → enforce en producción. Nunca publicar una regla nueva
directamente en `deny`/`rate_limit` sin pasar por modo log.

## Pendientes de verificación

- Allotment de reglas `rate_limit` del plan de Vercel del team (verificar
  al crear las reglas en F1).
- Límites reales del free tier de Upstash al provisionar (~500k
  comandos/mes a la fecha).

## Notas de ejecución

- El código de este diseño NO se implementa en este PR (pre-Fase 1). Al
  arrancar F1: **writing-plans** sobre este spec y ejecución con TDD según
  [`src/CLAUDE.md`](../../../src/CLAUDE.md).
