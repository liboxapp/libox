---
title: Revisión de diseño de sistema — de lo construido al MVP
status: borrador
tags: [libox, arquitectura, mvp, revision, system-design]
updated: 2026-09-25
description: Revisión con el marco de system-design. Qué hay construido, qué exige el canon, las brechas y la ruta en tres etapas hasta el MVP lanzable.
---

# Revisión de diseño de sistema — de lo construido al MVP

Revisión hecha con el marco de *system-design* (requisitos, diseño de alto nivel, detalle, escala y confiabilidad, trade-offs) sobre el corpus V6, el scaffold de `src/` y la infraestructura del repo. No es normativa: sus hallazgos entran al canon solo por la vía de CD-07. La completan dos notas: [hallazgos técnicos del canon](2026-09-25-revision-sistema-hallazgos-l3.md) y [trade-offs de ASS-002 y ASS-001](2026-09-25-revision-sistema-decisiones-ass.md).

## Veredicto

- **El canon es una especificación funcional muy completa, pero todavía no una base técnica construible.** Hay defectos verificados que romperían R0: el ledger no cumple su propio control de suficiencia de reembolso, el SQL no se puede desplegar tal cual y el OpenAPI cubre una fracción de las rutas.
- **Código de producto: cero.** Existe un mock de front (dos pantallas con datos falsos) y un OS de IA sólido. Ninguna de las 16 operaciones del OpenAPI ni de las 135 tablas existe en código.
- **ASS-002 es una decisión de backend.** El cliente Next.js lo fija el canon, y L3 §0.3 fija .NET 8, que sale de soporte el 10-nov-2026. L3 hay que versionarlo de todos modos.
- **Recomendación:** una etapa corta de desbloqueo (2–3 semanas, sobre todo decisiones y L3 V8) antes de R0. Codificar sobre el canon actual es construir sobre defectos conocidos.

## 1. Requisitos

**Funcionales.** El [PRD MVP V9](../../linea-base/LIBOX_PRD_BLUEPRINT_MVP_V9.md) define un ciclo que no admite saltos: participante verificado compra, recibe tickets, el pool se congela con compromiso público, una baliza de ronda futura aporta la entropía, el sorteo se ejecuta y cualquier tercero lo reproduce. Después vienen la sala de resolución, la atestación de entrega, seis gates y la liquidación al organizador. Actores: participante, organizador (persona natural o jurídica), soporte, administración y el propio sistema (PRD §2 y §27).

**No funcionales** ([L3 V7](../../linea-base/LIBOX_ESPECIFICACION_TECNICA_L3_V7.md) §13.2 y PRD §32.4):

| Dimensión | Objetivo |
|---|---|
| Disponibilidad | 99,5 % mensual en superficies públicas |
| Latencia | p95 API < 500 ms · crear orden < 800 ms sin PSP · webhook < 5 s · outbox < 60 s |
| Capacidad de referencia | 500 sorteos activos · 50 órdenes/s · 600 tickets/min · 200 compradores concurrentes por sorteo |
| Correctitud (compromiso firme) | Cero sobreventa, cero doble emisión, cero doble ejecución, cero descuadre |
| Front | LCP < 2,5 s en gama media · bundle inicial < 200 KB |
| Recuperación | **No definida:** sin RPO, RTO ni backups |

**Restricciones.** Cuatro generalistas a 32 SP por sprint, con R0 al 60 % (condición T-5). 936 SP en 136 historias. 261 SP en zonas sin generación asistida: sorteo, asientos, concurrencia, incompatibilidades y comisión/impuesto. Dictámenes legales pendientes, ASS-001 y ASS-002 abiertos, `src/` congelado.

## 2. Diseño de alto nivel

L3 no declara estilo ni trae diagrama, pero todo apunta a un **monolito modular con puertos y adaptadores**: un runtime, una base de datos, outbox transaccional y adaptadores intercambiables ("la elección es dato; la integración es código").

```
                      Navegador / PWA
                             │
               ┌─────────────▼──────────────┐
               │ Cliente Next.js (canon)    │ catálogo SSR/ISR, verificación
               │                            │ pública, paneles por rol
               └─────────────┬──────────────┘
                             │ HTTPS /api/v1 · JWT 15 min · Idempotency-Key
               ┌─────────────▼──────────────┐     ┌──────────────────────────┐
 PSP webhook ─►│ API — runtime por ASS-002  │     │ Worker (mismo código)    │
 (firmado)     │ módulos: identidad, sorteo,│     │ 30 jobs + dispatcher del │
               │ orden/pago, ledger, sala…  │     │ outbox cada 10 s         │
               └─────────────┬──────────────┘     └────────────┬─────────────┘
                             │                                 │
               ┌─────────────▼─────────────────────────────────▼──┐
               │ PostgreSQL 16 — sistema de registro (135 tablas) │
               └──────────────────────────────────────────────────┘
  Redis: caché, nunca autoritativo en dinero · S3: evidencias con URL firmada
  Adaptadores: baliza pública · KYC · comprobantes · registro/notaría · correo/SMS
```

Camino crítico del dinero: el webhook del PSP entra firmado y se deduplica; en **una sola transacción** se confirma el pago, se emiten los tickets, se asienta el ledger y se escribe el evento en el outbox. El worker despacha los efectos (notificaciones, cierres, sorteos) de forma idempotente.

**Escala.** No es el riesgo del MVP: L1 enciende con 3 sorteos simultáneos en el mes 11, y la capacidad de referencia (50 órdenes/s) está órdenes de magnitud por debajo de lo que sostiene un Postgres primario. El riesgo es la **correctitud**: concurrencia sobre el inventario de un sorteo popular, idempotencia de webhooks y cuadre del ledger. Por eso las zonas sin IA están donde están.

## 3. Construido frente a lo que pide el canon

| Área | Hoy | Canon / MVP | Brecha |
|---|---|---|---|
| Corpus | V6, 15 documentos, `verify_corpus` 15/15 OK | Base de implementación | Defectos técnicos en L3 |
| API | 0 de 16 operaciones | ≥43 rutas en L3 §11 | OpenAPI incompleto (T-1) y sin código |
| Datos | 0 de 135 tablas | Esquema desplegable | SQL sin particiones ni GRANTs |
| Front | Mock de catálogo y detalle, 12 rifas, compra deshabilitada, 24 tests | ~62 superficies, 41 sin ficha (T-2) | Tipos a mano, 2 de 22 estados, sin auth |
| Backend | Nada: sin DB, auth, pagos ni jobs | Todo | Todo |
| CI | Docs, commits, corpus y guards | Build, test, contrato, migraciones | Ningún workflow compila código |
| Operación | Sin entornos ni despliegue | dev/staging/prod, backups, observabilidad | Todo |

Lo reutilizable es el front: el canon manda un cliente Next.js, así que el mock sobrevive con cualquier backend. Hay que remodelarlo contra tipos generados del OpenAPI (BR-03), ampliar los estados y alinear los tokens a L4 V2 (solo Manrope).

## 4. Ruta al MVP

"MVP-1" no existe en el canon, que planifica en entregas R0–R6. Propongo dos hitos con criterio de salida verificable, precedidos por una etapa de desbloqueo.

**Etapa 0 — Desbloqueo (2–3 semanas, antes de R0).**

1. Socios: ratificar ASS-002 con el encuadre de la [nota de trade-offs](2026-09-25-revision-sistema-decisiones-ass.md) y encargar los dictámenes L-01 y de custodia. [LEGAL→ABOGADO]
2. Registrar los [hallazgos](2026-09-25-revision-sistema-hallazgos-l3.md) por CD-07 y emitir **L3 V8**: runtime soportado, ledger corregido, SQL desplegable, RPO/RTO.
3. Completar el OpenAPI (T-1), condición bloqueante del equipo técnico.
4. Alinear gobernanza: `CONTRIBUTING.md` todavía exige Drizzle, Supabase e Inngest, contra el canon.
5. CI de código: build, lint, typecheck, test y migraciones contra una base efímera.
6. En paralelo, fuera de ingeniería: fichas de superficies (T-2) y F0 (20 conversaciones, hoy en cero).

**Hito 1 — MVP-1 técnico = gate de R1, "ensayo en entorno controlado".** El ciclo completo en sandbox: alta y KYC, publicar sorteo, comprar con el PSP de pruebas, tickets, compromiso, baliza, ejecución, prueba pública que un tercero reproduce, y reembolso a saldo si el sorteo falla. R0 + R1 = 345 SP ≈ 13 sprints ≈ 6 meses.

**Hito 2 — MVP lanzable.** Corte de lanzamiento (R0–R3 + E31/E32, idealmente E33/E34/E37: 607–683 SP ≈ 21–23 sprints ≈ 10–11 meses desde R0), más el ensayo con dinero real (US-111), el dictamen L-01 favorable y ASS-001 resuelta. El mes 11 de L1 solo cuadra con este corte y arrancando R0 pronto.

## 5. Qué revisaría al crecer

- Outbox por sondeo → broker, solo con varios consumidores o si el retraso supera el SLO.
- Réplicas de lectura para catálogo y verificación pública.
- Retención automatizada de las 12 tablas particionadas.
- Motor de sorteo como desplegable aislado, si una auditoría externa lo pide.
- `analytics_events` fuera de la base transaccional cuando su volumen compita con el dinero.
