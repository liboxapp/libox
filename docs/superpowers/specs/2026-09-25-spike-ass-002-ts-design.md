---
title: Spike de ASS-002 — flujo de compra en TypeScript con fallos deliberados
status: borrador
tags: [libox, ass-002, spike, stack, spec]
updated: 2026-09-25
description: Diseño del spike que produce la evidencia para ratificar o descartar el backend TypeScript. Pregunta, alcance, siete fallos deliberados, criterio de ratificación y reglas de desecho.
---

# Spike de ASS-002

Parte del [programa para habilitar R0](2026-09-25-habilitar-r0-design.md) (stream B). Se origina en la propuesta de Codex que Diego adoptó el 2026-09-25 como proceso (D-01): elegir TypeScript de forma provisional y validarlo con fallos deliberados antes de ratificar. La ratificación es de los socios; el spike solo aporta evidencia.

## Pregunta

¿Puede un equipo pequeño **construir y operar** el flujo de compra de Libox con TypeScript, PostgreSQL y un servicio de workflows administrado, de modo que se recupere solo de los fallos típicos y se diagnostique sin SQL manual?

El lenguaje no vuelve correctos los pagos. Lo que se mide es el costo de infraestructura y de operación en este stack, con las mismas garantías que exige L3.

## Alcance

**Stack del spike:** Next.js 16 (App Router) con TypeScript estricto y módulos de dominio separados (órdenes, pagos, boletos, sorteo y ledger); los endpoints solo invocan a los módulos. PostgreSQL 16, local o en una rama de Neon. Inngest como workflows administrados. Un PSP **simulado** con fallos controlables, porque los fallos tienen que ser deterministas.

**Modelo mínimo:** un subconjunto del esquema L3 V7 con sus nombres de tabla (`raffles`, `orders`, `payments`, `psp_events`, `processed_psp_events`, `tickets`, `idempotency_keys`, `journal_entries`/`journal_lines` con cuadre, `event_outbox`, `draw_executions`).

**Flujo:**

1. Crear la orden y reservar boletos en una sola transacción de PostgreSQL.
2. Solicitar el pago fuera de esa transacción, con una clave de idempotencia.
3. Recibir la confirmación: verificarla y guardarla de forma durable antes de responder.
4. Procesarla de forma atómica: pago, boletos, asientos y evento.
5. Enviar el comprobante en segundo plano. Si el correo falla, la compra no se revierte.
6. Conciliar periódicamente los pagos pendientes o discrepantes.
7. Disparar el sorteo por la ronda de la baliza, con ejecución única.

**Consola mínima (`/ops`):** buscar una orden, ver su línea de tiempo (transiciones, eventos del PSP, outbox y ejecuciones de workflow), identificar el paso fallido y reintentar de forma segura.

**Excluido:** auth completa, KYC, UI de catálogo, correo real y dinero real.

## Fallos deliberados

| ID | Fallo inyectado | Resultado esperado |
|---|---|---|
| F1 | El webhook llega dos veces, en serie y en concurrencia | Un solo procesamiento; ambas llamadas responden 200 |
| F2 | El PSP acepta el pago y la llamada agota el tiempo | La orden queda pendiente y se resuelve por consulta o conciliación; reintentar con la misma clave no duplica el cobro |
| F3 | El proceso muere después del commit y antes de publicar el evento | El outbox lo publica al reanudar; no se pierde nada |
| F4 | Se pide dos veces el mismo reembolso | Un solo efecto patrimonial |
| F5 | N compras concurrentes por el último boleto | Exactamente una emitida; cero sobreventa |
| F6 | Disparo duplicado del sorteo, reinicio del worker o baliza que se retrasa | Una sola ejecución; espera acotada y alarma si vence el timeout |
| F7 | Expira la reserva y después se confirma el pago | Resultado definido: reembolso a saldo o reemisión si hay inventario. Como L3 no lo define (H-16), el spike fija una política provisional y la deja registrada |

## Criterio de ratificación

Para recomendar TypeScript a los socios se exigen las cinco condiciones:

1. **Correctitud.** F1–F7 terminan en el estado esperado, y se cumplen los invariantes: ningún ticket sin orden `PAID`, un solo efecto por acción idempotente, ledger cuadrado y una sola ejecución por sorteo.
2. **Operación.** Cada incidente se diagnostica desde `/ops` en menos de 5 minutos y sin SQL, y el reintento desde la consola es seguro.
3. **SLO plausibles** en el despliegue de preview: el acuse del webhook tarda menos de 5 s, incluido el arranque en frío, y la creación de la orden es de orden de magnitud compatible con el p95 < 800 ms. Es indicativo, no una prueba de carga.
4. **Proveedor.** Límites documentados de Inngest (pasos, concurrencia, timeouts, plan necesario para R0 y R1), sin que ninguno impida los 30 jobs, la ejecución única ni la cadencia de 10 s del outbox.
5. **Huella operativa.** Cuántos servicios y proveedores hay que operar, y quién se ocupa de qué.

Si falla un criterio, se registra por qué y se decide entre repetir el mismo flujo en .NET 10 o cambiar el modelo de ejecución (servicio de larga vida). Dos opiniones no sustituyen esta evidencia.

## Entregables y reglas

- **Informe** versionado en `docs/audits/<fecha>-spike-ass-002/`, con evidencia de cada fallo: comandos, salidas saneadas y capturas de `/ops`. Es la entrada de `/libox-system-design-audit producto`, en la que Fable, Opus y Codex lo revisan antes de que lo vean los socios.
- **El código es desechable.** Vive en la rama `spike/ass-002-ts`, bajo `spikes/ass-002-ts/`, y nunca se mergea: el job `protected-paths` de A1 lo rechaza. El código de las zonas sin IA se reescribe a mano en R0.
- **Sin dinero ni datos reales.** Se usan PSP simulado y sandbox. Los secretos van solo en variables de entorno de la cuenta de prueba, nunca en el repo.
- **Timebox: dos semanas.** Si vence, se decide con lo obtenido, con los criterios incumplidos a la vista.
- **Dependencias:** cuentas de prueba en Vercel e Inngest (plan gratuito) y una base de datos de pruebas. Diego las crea o autoriza antes de empezar.
