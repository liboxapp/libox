---
title: C1 — borrador de operación y recuperación
status: borrador
tags: [r0, c1, l3-v8]
updated: 2026-09-30
description: Propuesta para L3 §12–14, calendario cuantificado y aceptación pendiente de ejecución.
---

# Operación propuesta para L3 V8

Este borrador desarrolla §12–14. Las cifras son objetivos propuestos, no resultados
medidos ni garantías del proveedor. [Comparativa](proveedores.md).

## Monolito modular TypeScript

Next.js App Router contiene interfaz y adaptadores HTTP; módulos de órdenes,
pagos, boletos, sorteo y liquidaciones exponen operaciones de dominio. El proveedor
de workflows invoca esos módulos mediante adaptadores del mismo repositorio.
No duplicar las reglas en endpoints, jobs o cliente. PostgreSQL mantiene autoridad
sobre dinero e inventario. Los puertos de cobro y pago al organizador son distintos;
ASS-001 no se resuelve escogiendo un proveedor de infraestructura.

Los importes de dominio se mantienen exactos como BIGINT/bigint; la representación
JSON debe cerrarse en [contratos](contratos.md). No se convierte a punto flotante.
Runtime y dependencias se fijarán en D1 contra el Next.js instalado y soportado;
este borrador no introduce una versión de Node sin comprobar compatibilidad.

## Calendario y outbox

Inventario de L3 V7 §12.6: 30 trabajos. En un mes de 30 días:

| Frecuencia | Trabajos | Activaciones |
|---|---:|---:|
| Cada minuto |9 |388.800 |
| Cada 15 minutos |2 |5.760 |
| Cada hora |4 |2.880 |
| Cada día |14 |420 |
| Cada 10 segundos |1 |259.200 |
| **Total** |**30** |**657.060** |

Propuesta: 29 schedules en Trigger; un ticker de Supabase Cron cada 10 s llama un
endpoint privado de dispatcher. La opción está documentada: Cron admite segundos,
HTTP y SQL; recomienda como máximo 8 jobs concurrentes y 10 minutos por job.
No ejecutar los 30 jobs como funciones largas en Cron.
[Supabase Cron](https://supabase.com/docs/guides/cron).

Secuencia contractual del dispatcher, sin implementación de concurrencia:

1. Autenticar al emisor con secreto dedicado y rotación; nunca una publishable key.
2. Recuperar lotes acotados desde el outbox persistido en la transacción de dominio.
3. Publicar IDs y versión de evento; excluir documentos, semillas y credenciales.
4. Confirmar despacho solo después de aceptación durable. Caer entre publicar y
   confirmar puede repetir entrega; el consumidor debe producir un único efecto.
5. Recuperar desde la base después de un fallo; no desde memoria ni solo pg_net.

La integración Cron/HTTP puede guardar secretos en Vault. pg_net no es una cola
durable de negocio. La cadencia no garantiza entrega durante una caída.
[HTTP programado y Vault](https://supabase.com/docs/guides/functions/schedule-functions),
[pg_net](https://github.com/supabase/pg_net).

No usar cron Vercel para prometer 10 s: Pro tiene intervalo mínimo de un minuto.
[Vercel Cron](https://vercel.com/docs/cron-jobs/usage-and-pricing).

Los reintentos llevan deadline de negocio, backoff acotado y alarma. El timeout de
un intento no cancela efectos del PSP ni autoriza generar otra clave de cobro.
Los casos agotados pasan a consola interna con trace_id, estado real, última
respuesta y acción permitida. No reintentar sorteo ni pagos con SQL manual.

## Recuperación y observabilidad

| Activo | Objetivo propuesto R1 | Evidencia antes de operar |
|---|---|---|
| PostgreSQL | RPO ≤5 min; RTO ≤4 h; PITR de 7 días más copia independiente | Restauración aislada, integridad y reconciliación contra PSP/outbox |
| Evidencia recibida | Ninguna evidencia confirmada sin copia durable verificable | Restaurar original/hash/metadatos y verificar permisos |
| Secretos/seed cifrada | Recuperación de claves autorizada, separada de backups de datos | Ensayo sin imprimir secretos; controles de acceso y registro |
| Workflows | Reanudar desde estado persistente, sin duplicar efectos | F3/F6 y reentrega de eventos |

RPO cero absoluto entre proveedores no se afirma. Antes de confirmar recepción
de evidencia, deben existir objeto persistido y registro verificable; si se exige
supervivencia a pérdida total del proveedor, confirmar también copia independiente.
Si la copia es asíncrona, exponer estado PENDING y fijar RPO explícito antes de usarla.
RTO incluye objetos, credenciales y conciliación; medirlo, no inferirlo del PITR.

Conservar objetivos de L3: outbox <60 s en operación normal; alarma alta al superar
5min. Medir antigüedad máxima y percentiles, backlog, retries, webhooks fallidos,
conexiones DB, particiones futuras, gasto y vencimientos. El pequeño plan no compra
SLA de toda la aplicación. Programar ensayo de restore antes de R1 y periódicamente.

## Aceptación F1–F7

| Caso | Resultado exigido | Evidencia |
|---|---|---|
| F1 webhook duplicado serie/concurrente | Un procesamiento; respuestas 200 | DB real + evento PSP sandbox + conteo de efectos |
| F2 PSP acepta y llamada expira | Orden pendiente; consulta/conciliación resuelve sin doble cobro | Misma clave, consulta al proveedor, traza del timeout |
| F3 caída tras commit y antes de publicar | Outbox entrega al reanudar, sin pérdida | Reinicio real y trazas de persistencia/consumo |
| F4 reembolso repetido | Un efecto patrimonial | Contabilidad validada y estado PSP |
| F5 dos o más compras por último boleto | Exactamente una emisión; sin sobreventa | Concurrencia PostgreSQL, invariantes y respuesta a perdedores |
| F6 doble sorteo/reinicio/baliza tardía | Una ejecución y espera acotada con alarma | Implementación humana independiente y fixture de baliza |
| F7 pago posterior a reserva/pool | Sin insertar ticket tardío; conciliación y devolución definida | Política aprobada y caso PSP sandbox |

La consola interna explica y permite recuperar cada incidente con autorización y
auditoría, sin saltar los gates. Estos son criterios de prueba, **no pruebas pasadas**.
La implementación crítica sigue reservada a Diego. Revisión humana obligatoria
suspendida no suprime INV-38 ni las separaciones de funciones del producto.
