---
title: C1 — comparación de proveedores y presupuesto
status: borrador
tags: [r0, c1, l3-v8]
updated: 2026-09-30
description: Fuentes oficiales al 2026-09-30 y escenarios de infraestructura dentro de US$250.
---

# Proveedores y presupuesto

**Elección de Diego, 2026-09-30:** Supabase Pro + Trigger.dev + Vercel Pro.
Comparativas conservadas como fundamento; precios son estimaciones, no contratación.

Consulta: 2026-09-30. USD/mes, tarifas publicadas sin impuestos. Una persona con
asiento de desarrollo; un proyecto de producción; local/CI para desarrollo.
No son cotizaciones ni pruebas de capacidad. Pagos, KYC, SMS y asesoría legal se
presupuestan aparte. El techo de Diego es US$250 y debe considerar cargos reales.

## PostgreSQL

| Opción | Ventajas | Costo y límite que cambian la decisión |
|---|---|---|
| Neon Launch | PostgreSQL 16 disponible; roles SQL; pooling; historial hasta 7 días | US$0,106/CU-h +0,35/GB datos +0,20/GB historial; sin mínimo mensual. A 0,25 CU durante 730 h: US$19,35 solo cómputo |
| Neon Scale | Historial hasta 30 días y SLA del plan | US$0,222/CU-h; 0,25 CU continuo: US$40,52 solo cómputo. No equivale a RPO/RTO de Libox |
| Supabase Pro | DB, Auth y Storage integrados; Cron subminuto | US$25 base con crédito de cómputo 10; Small≈15 y PITR de 7 días≈100: **≈130 total**. Backups de DB no restauran bytes de Storage |

Fuentes: [Neon precios](https://neon.com/pricing), [compatibilidad PG](https://neon.com/docs/reference/compatibility),
[Supabase precios](https://supabase.com/pricing), [compute](https://supabase.com/docs/guides/platform/compute-and-disk),
[backups/PITR](https://supabase.com/docs/guides/platform/backups).

El polling cada 10 s impide asumir scale-to-zero de Neon. Historial Neon pagado
por defecto de 1 día debe configurarse; 7 días no se obtiene solo al elegir Launch.
Supabase documenta actualizaciones de PostgreSQL 15 a 17; PostgreSQL 16 gestionado exacto queda sin verificar.
[Historial Neon](https://neon.com/docs/introduction/branching), [upgrades Supabase](https://supabase.com/docs/guides/platform/upgrading).

Ambos son PostgreSQL con transacciones y particiones; no asumir superuser ni
permisos seguros por defecto. Rol administrativo separado de app; migraciones
por conexión directa. Pool de transacción para tráfico serverless; no depender
de estado de sesión. Supavisor en ese modo no soporta prepared statements.
[Supabase conexión](https://supabase.com/docs/guides/database/connecting-to-postgres),
[Neon pooling](https://neon.com/docs/connect/connection-pooling), [roles Neon](https://neon.com/docs/manage/roles).

## Workflows y autenticación

| Opción | Base publicada | Evaluación para Libox |
|---|---|---|
| Trigger.dev Hobby | US$10 con 10 de consumo incluido; 100 schedules | Recomendado; cómputo y runs medidos. Cron sin segundos; outbox usa ticker externo |
| Inngest Pro | US$99; 1 millón de ejecuciones, run y steps cuentan | Con DB 130 + web 20 alcanza 249 antes de correo/rate/objetos. No encaja holgadamente |
| Supabase Auth | Incluido en Pro; TOTP y 100k MAU | Menos proveedores; contrato de sesión requiere cambios explícitos |
| Clerk Pro | US$25 mensual; 20 con pago anual; 50k MRU | Alternativa; token de 60 s y modelo de sesión distintos. MRU no equivale a MAU |

[Trigger precios](https://trigger.dev/pricing), [schedules](https://trigger.dev/docs/tasks/scheduled),
[Inngest precios](https://www.inngest.com/pricing), [límites](https://www.inngest.com/docs/usage-limits/inngest),
[Clerk precios](https://clerk.com/pricing), [sesiones Supabase](https://supabase.com/docs/guides/auth/sessions).

Cupo de concurrencia contradictorio entre pricing y docs consultados: Trigger
Hobby 50/25 e Inngest Pro 100/200. Diseñar provisionalmente para 25/100 y confirmar
el valor contratado. Ninguno sustituye idempotencia/transacciones patrimoniales.
[Límites Trigger](https://trigger.dev/docs/limits), [concurrencia Inngest](https://www.inngest.com/docs/guides/concurrency).

## Evidencias, correo y rate limiting

- Supabase Storage privado simplifica RLS y URLs firmadas, pero sin versioning ni
  Object Lock S3. Solo adoptarlo con copia independiente y restauración probada.
  [Compatibilidad](https://supabase.com/docs/guides/storage/s3/compatibility).
- S3 privado con Versioning/Object Lock es la alternativa para retención fuerte.
  Precio regional, requests y egress deben cotizarse; no se fija una tarifa universal.
  [Retención](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html), [precios](https://aws.amazon.com/s3/pricing/).
- R2 Standard: US$0,015/GB-mes, 4,50/millón de operaciones A y 0,36/millón B, egress gratis;
  cuota gratuita de 10 GB, un millón de operaciones A y diez millones B. Sus locks administrativos no equivalen a S3 Compliance.
  [Precios](https://developers.cloudflare.com/r2/pricing/), [locks](https://developers.cloudflare.com/r2/buckets/bucket-locks/).
- Upstash PAYG: US$0,20/100k comandos, sin usarlo como autoridad de dinero. Reservar
  US$5 iniciales; claves seudónimas efímeras. Prod Pack de US$200 queda fuera de este diseño.
  [Tarifas y topes](https://upstash.com/pricing/redis).
- Resend Pro: US$20 por 50k correos; exceso de US$0,90/1000. SMTP para verificación/recuperación;
  no atribuir entrega garantizada ni usar el envío gratuito como capacidad R1.
  [Precios](https://resend.com/pricing).

## Escenarios, sin doble contar créditos

| Concepto | R0 desarrollo compartido | R1 ilustrativo |
|---|---:|---:|
| Supabase Pro + compute |25 (Micro con crédito) |130 (Small+PITR de 7 días) |
| Vercel Pro un asiento |20 |20 |
| Trigger |10 si consumo≤10 |23,39 si 29 jobs promedian 1 s |
| Correo |0 dentro cuota dev |20 |
| Rate limiting |0 dentro cuota dev |5 (reserva) |
| Copias independientes de DB/objetos |0 con datos sintéticos |10 (reserva, no tarifa) |
| **Subtotal estimado** |**55** |**208,39** |
| **Margen hasta 250** |**195** |**41,61** |

[Vercel Pro](https://vercel.com/pricing) publica US$20 con US$20 de uso incluido; consumo
adicional, asientos, entornos duplicados, dominio, logging y tributos reducen el margen.
El dispatcher añade 259.200 llamadas HTTP mensuales al hosting elegido, además
de carga y tráfico de DB; su consumo no se ha medido. La reserva de copias incluye
DB y objetos, sin cotización cerrada.
En R0 no se almacenan evidencias reales ni se afirma recuperación transaccional.

Cálculo Trigger en máquina Small 1x: 397.860 runs/mes de 30 días ×(0,000025 + segundos×0,0000338).
Con 5 s de media son US$77,18 y el subtotal sube a 262,18: **excede el techo** incluso antes
de impuestos. Ejecuciones de negocio y reintentos son adicionales.
[Tarifas Trigger](https://trigger.dev/pricing). R1 requiere medir, reducir trabajo
vacío o ajustar presupuesto; no prometer 250 con cualquier tráfico.

Objetivo de gasto antes de impuestos≤215; alertas proyectadas a US$175/200/215.
Definir límites por proveedor y capacidad antes de contratar; no activar un corte
ciego de consumo que deje sin conciliación pagos ya aceptados. Si el costo proyectado
supera el techo, frenar nuevas ventas de forma operativa y conservar recuperación.
