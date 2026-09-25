---
title: Revisión de sistema — trade-offs de ASS-002 (stack) y ASS-001 (custodia)
status: borrador
tags: [libox, arquitectura, stack, custodia, decisiones]
updated: 2026-09-25
description: Encuadre técnico de las dos decisiones abiertas de los socios, con el costo de cada opción y una recomendación. Insumo para ratificar; no decide.
---

# Revisión de sistema — trade-offs de ASS-002 y ASS-001

Parte de la [revisión de diseño de sistema](2026-09-25-revision-sistema-mvp-design.md). Ambas decisiones son de los socios y se registran en el doc 20 de Outline; esta nota solo ordena el costo técnico de cada opción.

## ASS-002: stack

### Son dos ejes independientes

El cliente Next.js lo fija el canon en cualquier escenario ([L3](../../linea-base/LIBOX_ESPECIFICACION_TECNICA_L3_V7.md) §0.3). ASS-002 decide, por lo tanto, el **backend**, y tiene dos ejes que conviene no mezclar:

1. **Modelo de ejecución:** servicio de larga vida (API y worker en contenedores) o serverless (la vía Next.js full-stack sobre Vercel, Supabase e Inngest que asumían los ADR archivados).
2. **Lenguaje del backend:** .NET o TypeScript.

### Eje 1: el diseño de L3 exige un servicio de larga vida

Con cualquier lenguaje, L3 está pensado para un proceso que vive:

- un dispatcher de outbox cada 10 s y 30 jobs programados "con bloqueo de ejecución única" (l.3910–3943);
- auth propia con familias de refresh tokens rotatorios, argon2id y MFA para roles internos (l.3418–3427), no un proveedor gestionado;
- roles y privilegios en Postgres, 12 tablas particionadas y Redis para bloqueo oportunista;
- Docker Compose en local (§0.3).

En serverless cada punto pide un rodeo: cron externo, jobs en un tercero, auth gestionada que contradice el diseño de identidad. **Recomendación firme: servicio de larga vida**, un monolito modular con dos procesos (API y worker) desde el mismo código, sobre Postgres 16 gestionado. Neon sigue siendo válido como host: es Postgres estándar (particiones, roles, GRANTs) y su branching por PR sirve para probar las migraciones del esquema de 135 tablas.

### Eje 2: lenguaje

| Criterio | .NET 10 LTS | TypeScript (Node: NestJS o Fastify) |
|---|---|---|
| Alineación con el canon | §0.3 ya dice .NET; solo cambia la versión | Cambia §0.3 y la convención de nombres de puertos |
| Lenguajes en el equipo | Dos: C# en backend, TypeScript en el cliente obligatorio | Uno de punta a punta |
| Tipos del contrato | Generados del OpenAPI en ambos lados | Generados una vez y compartidos |
| Jobs y workers | Nativo (`BackgroundService`, Hangfire, Quartz) | Maduro (pg-boss, BullMQ) |
| Dinero | Tipado fuerte, `long` en céntimos | TS estricto; exige `bigint` o enteros validados, nunca `number` flotante |
| Contratación en Perú | Amplia en banca y enterprise | Amplia en startups |

Dos datos cambian el peso de la columna izquierda:

- **L3 hay que versionarlo igual.** Según la política de Microsoft, .NET 8 LTS termina soporte el 10-nov-2026, antes de acabar R0; el LTS vigente es .NET 10, con soporte hasta noviembre de 2028. El argumento "no tocar el canon" se reduce a no cambiar convenciones.
- **El cliente ya obliga a TypeScript.** Con cuatro generalistas, .NET duplica toolchains, suites de prueba y pipelines de CI.

**Recomendación:** decide la fluidez real de quienes van a escribir las zonas sin IA (261 SP de sorteo, asientos y concurrencia). Si el equipo es TS-first, TypeScript de punta a punta. Si tiene más oficio en .NET, .NET 10 LTS. Con fluidez pareja, TypeScript, por el costo de sostener dos ecosistemas en un equipo de cuatro.

## ASS-001: custodia

### Qué asume el canon

Custodia real: LIBOX retiene la recaudación hasta verificar la entrega ([LBPF V3](../../linea-base/LIBOX_BEHAVIORAL_PRODUCT_FRAMEWORK_LBPF_V3.md) §5.4; [PRD V9](../../linea-base/LIBOX_PRD_BLUEPRINT_MVP_V9.md) INV-06-a, INV-16, RN-38 y los seis gates). El [Dossier Legal](../../linea-base/LIBOX_DOSSIER_LEGAL_V1.md) pregunta si retener fondos configura actividad financiera regulada y si LIBOX actúa como agente o como principal (L-06, L-07). [LEGAL→ABOGADO]

### Impacto técnico de cada salida

| Salida | Qué cambia en el sistema |
|---|---|
| Custodia real admitida | Nada de diseño. Hace falta un PSP con retención y liberación a demanda, o una entidad regulada aliada; el pago al organizador (T-08) mueve dinero real |
| Split en la fuente por el PSP | Los gates pasan a ser lógicos: no pueden frenar un pago ya dividido. INV-06-a, INV-16 y RN-38 dejan de ser cumplibles y hay que versionar LBPF, PRD y L3 |

### Recomendación de arquitectura

Construir el ledger, los gates y el saldo de reembolso tal como los especifica el canon: sirven como registro interno con cualquier salida. Aislar el movimiento de dinero detrás de puertos: el de cobro (`IPaymentProvider`) ya existe; falta uno de **pago al organizador**, que L3 no define. Así ASS-001 cambia adaptadores y un subconjunto de asientos, no el núcleo.

El hito MVP-1 técnico (sandbox) no necesita esta decisión; el MVP lanzable sí.
