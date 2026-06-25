---
title: Plan Libox
status: vivo
tags: [libox, plan, roadmap]
canonical: docs/plans/libox-plan.md
mirror: ~/.claude/plans/spicy-sparking-hopcroft.md
updated: 2026-06-21
---

# Libox — Plan inicial de producto y arquitectura

## Contexto

Libox es un **marketplace web de rifas digitales con boleto pagado** operado bajo regulación peruana. Estado actual: **pre-código** — repositorio git con tooling de versionado ya cableado (SemVer, Conventional Commits, release-please, CI), stack ya decidido (Z.6: Next.js App Router + PostgreSQL) pero **aún sin scaffold**; sin wireframes todavía. Diego (full stack engineer) y socios van a contratar abogado para el marco legal.

Este documento NO es un implementation plan de código. Es la hoja de ruta de producto + arquitectura que sirve como base para empezar a construir. Su objetivo:

1. Fijar las decisiones de producto cerradas hoy.
2. Resolver las decisiones pendientes que bloquean cualquier diseño técnico.
3. Proponer un primer corte de dominios, stack e integraciones para discusión.
4. Definir los próximos pasos concretos antes de escribir la primera línea de código.

---

## 1. Decisiones de producto cerradas

| Decisión | Valor |
|---|---|
| Tipo de sorteo soportado en MVP | **Rifa con boleto pagado** (no sorteos promocionales gratuitos) |
| Usuarios | Organizadores + participantes |
| Organizadores en MVP | **Cualquier persona (natural o jurídica) con RUC activo** — ver Anexo Z.3 |
| Modelo de monetización | **Comisión por boleto vendido** |
| Pagos | **Fiat** (tarjeta + transferencias Yape/Plin, contexto Perú) |
| Plataforma | Web (responsive móvil + desktop), sin app nativa en MVP |
| Postura sobre "auditable" | Cumplimiento con leyes financieras peruanas, **NO** blockchain |

**Implicación de exigir RUC (no solo jurídicas):** el ancla es que Libox factura su comisión como servicio B2B al organizador, lo que exige que el organizador tenga RUC. Esto incluye personas naturales con negocio / RUC activo, no solo personas jurídicas — corrige una imprecisión del plan original. Se descarta para MVP la persona natural solo-DNI (sin RUC) por la restricción de facturación + riesgo PLAFT. Detalle en **[Anexo Z.3](#z3--tipo-de-organizador-cerrada-el-2026-06-05)**.

**Implicación de "solo rifa pagada":** el marco legal aplicable es el de rifas con autorización municipal, no sorteos promocionales MINCETUR. Estandarizar en un solo régimen reduce superficie regulatoria en V1.

---

## 2. Decisiones pendientes que bloquean diseño técnico

### 2.1. Custodia del dinero — **CERRADA (2026-06-05) → ver Anexo Z.1**

Decisión: **Modelo C — escrow conceptual**. Operativa de split directo vía PSP marketplace (el dinero del participante nunca pasa por Libox), pero con el ledger doble entrada del PRD Libox v11 corriendo desde día 1 como si Libox fuera escrow. Justificación completa, alternativas evaluadas (A puro, B real), implicaciones que los socios deben aceptar, y validaciones externas pendientes con abogado y comerciales PSP: ver **[Anexo Z.1](#z1--custodia-del-dinero-cerrada-el-2026-06-05)**.

### 2.2. PSP / Gateway de pagos — **CERRADA EN DIRECCIÓN (2026-06-05) → ver Anexo Z.2**

Decisión: **Mercado Pago como PSP primario** con mecanismo de comisión **split en la fuente** (application fee / marketplace). **Culqi** queda como **segundo rail a implementar en una fase posterior del MVP** (qué fase exactamente = decisión de socios). Decisión final supeditada a verificación comercial: las preguntas eliminatorias son (1) ¿soporta split a múltiples beneficiarios? y (2) ¿ese split aplica a pagos **Yape**? Detalle, alternativas, insight Yape-dentro-del-checkout, y script de llamadas comerciales: ver **[Anexo Z.2](#z2--elección-de-psp-cerrada-en-dirección-el-2026-06-05)** y el ADR [`decisions/Z2-eleccion-psp.md`](../decisions/Z2-eleccion-psp.md).

### 2.3. PSE de facturación electrónica SUNAT

Para emitir factura electrónica por cada venta. Candidatos: **Nubefact**, **Defontana**, **Bizlinks**, **Facturador SUNAT** (gratuito pero limitado). Decisión depende de volumen esperado y necesidad de white-label.

### 2.4. Mecanismo de aleatoriedad verificable del sorteo

Aunque Diego confirmó que "auditable" no significa blockchain, el sorteo necesita ser **demostrablemente justo** ante un auditor o notario. Opciones:

- **Commit-reveal con semilla externa** (ej. hash de bloque de Bitcoin futuro, beacon NIST, drand) publicada en el sorteo antes de su ejecución → reveal al ejecutarse. Verificable por cualquier tercero sin necesidad de blockchain propia.
- **Notario digital firma el acta del sorteo** con la semilla y el algoritmo de selección.
- Combinar ambas para máxima defensibilidad.

→ **Acción pendiente:** discutir con el abogado si SUNAT/municipalidad aceptan esta evidencia digital o si requieren acta notarial física tradicional.

### 2.5. Alcance geográfico y de moneda

Asumo Perú-only, PEN. Confirmar.

---

## 3. Dominios del sistema (bounded contexts)

Antes de pensar en stack, mapeo los módulos lógicos. Esto guía la estructura del repo y permite identificar dónde están las integraciones críticas.

1. **Identidad & Onboarding**
   - Auth (participantes + organizadores + staff).
   - KYC de organizadores: validación de RUC contra padrón SUNAT, representante legal, documentos.
   - KYC ligero de participantes (DNI para premios altos).

2. **Catálogo de sorteos**
   - CRUD de sorteos por organizador.
   - Estados: borrador → en revisión → aprobado → activo → cerrado → ejecutado → liquidado.
   - Reglas: precio por boleto, cantidad máxima, fecha de ejecución, descripción del premio, autorización municipal adjunta.

3. **Venta de boletos**
   - Carrito, checkout, asignación de número de boleto, idempotencia (crítico para no vender el mismo número dos veces bajo concurrencia).

4. **Pagos & Facturación**
   - Integración con gateway (split o escrow según decisión 2.1).
   - Emisión de factura electrónica vía PSE.
   - Conciliación, reembolsos, manejo de webhooks.

5. **Ejecución del sorteo**
   - Cierre de venta, congelación de boletos vendidos.
   - Generación y publicación del commit (semilla, algoritmo).
   - Ejecución programada con la semilla revelada.
   - Generación del acta firmada.

6. **Liquidación de premios**
   - Notificación al ganador, KYC del ganador si aplica.
   - Cálculo y retención de IR 2da categoría si supera el umbral legal.
   - Coordinación de entrega del premio (organizador → ganador).

7. **Auditoría & Reportería**
   - Bitácora inmutable de eventos (append-only, idealmente hash-chain).
   - Reportes SUNAT periódicos.
   - Endpoint público de verificación por sorteo (semilla, algoritmo, lista de boletos, ganador).

8. **Backoffice**
   - Aprobación de organizadores y sorteos por staff de Libox.
   - Resolución de disputas.
   - Métricas operativas.

---

## 4. Stack tecnológico recomendado para discusión

Optimizo por: velocidad de iteración en MVP, idiomas que un full stack engineer maneja, ecosistema con buenas integraciones locales, y baja fricción para sumar 1–2 devs después.

### Frontend

- **Next.js (App Router) + TypeScript + Tailwind + shadcn/ui**
- Server components para SEO de la landing de sorteos públicos.
- Una sola codebase para landing pública, dashboard de organizador, dashboard de participante, y backoffice (con segmentación por rol).

### Backend

Dos alternativas razonables:

- **Opción 1 — Next.js full stack (API routes + Server Actions)**: una sola codebase, despliegue simple en Vercel o similar. Riesgo: pagos/webhooks/jobs requieren más cuidado al escalar. Bueno para validar.
- **Opción 2 — Next.js (frontend) + API separada en NestJS o Fastify (TypeScript)**: separa concerns, más fácil de escalar, mejor para integrar workers y jobs. Más overhead inicial.

**DECISIÓN CERRADA (Z.6): Next.js para todo (Opción 1).** Un solo framework cubre la superficie pública (SEO vía RSC/ISR) y la app autenticada (dashboards, checkout, backoffice). Libox **no es web estática** — es app transaccional con una superficie de contenido; por eso se descartó Astro. Se prevé extraer un servicio backend dedicado cuando los jobs/carga lo justifiquen. Detalle: **[Anexo Z.6](#z6--stack-tecnológico-cerrada-en-dirección-el-2026-06-06)** y ADR [`decisions/Z6-stack-tecnologico.md`](../decisions/Z6-stack-tecnologico.md).

### Base de datos

- **PostgreSQL** (Supabase o Neon para acelerar el MVP, autogestionado en V1).
- **Drizzle** (preferido) o Prisma como ORM — confirmar al scaffold.
- Tabla `audit_events` append-only con `trace_id` + `payload_hash` (modelo del PRD).

### Jobs y colas

- **Inngest** o **Trigger.dev** — **infraestructura crítica, no opcional**: ejecuta el outbox worker, el disparo de sorteo por umbral/deadline (Z.4) y la conciliación PSP. Evita Redis + worker propio en MVP.

### Auth

- **Clerk** o **Supabase Auth** para arrancar. MFA obligatorio para organizadores y staff (lo exige el PRD para Admin).

### Pagos

- **Mercado Pago** primario, **split en la fuente**, adaptador **multi-PSP** desde el inicio (Culqi 2º rail). Ver Z.2.

### Facturación SUNAT

- PSE vía API REST (Nubefact/Bizlinks/…). El **organizador** (con RUC, Z.3) es merchant of record y emite el comprobante. Detalle fiscal pendiente con abogado (compliance-peru.md).

### Hosting

- **Vercel** (frontend + API routes) + **Neon/Supabase** (DB). Migrar a infraestructura propia (AWS/GCP) cuando haya tracción y se necesite control fino de costos y compliance.

### Observabilidad

- **Sentry** (errores), **Axiom** o **Better Stack** (logs estructurados), **PostHog** (producto/analítica).

---

## 5. Modelo de datos inicial — entidades core

Esbozo de alto nivel (no es schema final):

```
Organization (organizador)
  - ruc, razon_social, representante_legal, estado_kyc, ...

User
  - email, rol (participant | organizer_member | staff), ...

Raffle (sorteo)
  - organization_id, titulo, descripcion, precio_boleto_pen,
    total_boletos, fecha_ejecucion, autorizacion_municipal_url,
    estado, commit_hash, semilla_revelada, ...

Ticket
  - raffle_id, numero, owner_user_id (nullable hasta vender),
    sale_id (nullable), estado, ...

Sale
  - user_id, raffle_id, monto_total, gateway_payment_id,
    factura_id, estado, ...

Draw (ejecución del sorteo)
  - raffle_id, semilla, algoritmo, ticket_ganador_id,
    acta_pdf_url, firma_digital, ejecutado_at, ...

AuditEvent (bitácora append-only)
  - id, prev_hash, hash, payload_json, created_at
```

---

## 6. Roadmap por fases

### Fase 0 — Pre-código (próximas 1–2 semanas)

- Cerrar decisión de custodia con el abogado (2.1).
- Comparar Culqi vs MercadoPago Marketplace con sus comerciales (2.2).
- Elegir PSE de facturación electrónica (2.3).
- Definir si SUNAT/municipalidad acepta acta digital (2.4).
- Wireframes de los 5 flujos críticos: registro de organizador, creación de sorteo, compra de boleto, ejecución de sorteo, vista pública de auditoría.

### MVP-1 — Núcleo: comprar → sortear (8–12 semanas, 1 dev full-time)

Refleja Z.1–Z.7. Alcance:
- Onboarding + KYC de organizadores: **dos plantillas (jurídica / natural-con-RUC)**, validación contra padrón SUNAT (Z.3).
- CRUD de sorteos con aprobación manual desde backoffice; `draw_config` versionado.
- **Motor de sorteo configurable, 1 ganador, AUTO+Admin, umbral+fecha** → presets T1–T4 (Z.4).
- **Ruta de fallo-y-refund** del sorteo (acopla con pagos; refund vía PSP, Z.4).
- Compra de boletos con **Mercado Pago, split en la fuente**, idempotencia + webhooks firmados (Z.2).
- **Ledger doble entrada** con las 8 cuentas del PRD (Modelo C conceptual, Z.1).
- Emisión de comprobante por el organizador vía PSE.
- Fairness verificable: `pool_hash → entropía externa → seed → random_value`, draw proof reproducible.
- Página pública de auditoría por sorteo + `audit_events` append-only con `trace_id`.
- **Outbox worker + job runner** para disparo de sorteo y conciliación.
- Onboarding manual de los primeros 3–5 organizadores.

### MVP-2 — Cierre del ciclo económico

- **Delivery** (evidencia del organizador → confirmación del usuario).
- **Settlement** con gates conceptuales + **disputas**.
- Reembolsos y conciliación PSP más robustos.
- Métricas y dashboards operativos.

### MVP-3 — Crecimiento y enterprise

- **T8 LIVE** (Z.5): ejecución en vivo con autorización Admin + capa realtime.
- **Multi-ganador (T6)** y **progresivo (T7)** como configuraciones del mismo motor.
- **Culqi como 2º rail PSP** (fase exacta = decisión socios, Z.2).
- APIs enterprise + observabilidad ampliada + reportes automáticos.

### Post-MVP — Escala

- Reevaluar custodia → **Modelo B (escrow real)** con partnership EEDE (Z.1).
- App móvil si la analítica lo justifica.
- Expansión LATAM (multi-moneda, multi-PSP, multi-país).

---

## 7. Próximos pasos concretos (post-aprobación de este plan)

1. **Diego + socios + abogado**: cerrar 2.1, 2.4, y validar la postura general de "rifa pagada con organizadores RUC".
2. **Diego**: llamadas comerciales a Culqi, MercadoPago, e Izipay para cerrar 2.2.
3. **Diego**: contactar 2 PSEs para evaluar 2.3.
4. **Próxima sesión con Claude**: una vez cerradas las decisiones pendientes, scaffold del repo (Next.js + Postgres + Prisma + Clerk) y definición del schema inicial completo de la DB.

---

## Z. Bitácora de decisiones cerradas con justificación para socios

Este anexo crece incrementalmente conforme se cierra cada **conflicto** (plan vs PRD vs mercado peruano) o **decisión de arquitectura** del proyecto. Cada entrada documenta: qué se decidió, por qué se descartaron las alternativas, qué implicaciones tiene que los socios deben aceptar conscientemente, y qué queda pendiente de validación externa.

El propósito es ser **extraíble**: cada entrada Z.X es autocontenida y puede compartirse con socios sin necesidad de explicar contexto previo.

⚠️ Los puntos marcados `[LEGAL→ABOGADO]` son lectura del autor sobre normativa pública peruana, **no asesoría legal**, y deben ratificarse con el abogado del equipo antes de tomar acción operativa.

---

### Z.1 — Custodia del dinero (cerrada el 2026-06-05)

**Decisión**: Libox opera el MVP-1 bajo **Modelo C — escrow conceptual**.
- **Operativamente**: split directo vía PSP marketplace (probable Mercado Pago). El dinero del participante nunca pasa por cuentas controladas por Libox.
- **Internamente**: Libox lleva el **ledger doble entrada del PRD Libox v11** desde día 1, registrando conceptualmente los flujos como si custodiara el dinero, incluso cuando no lo hace.

**Estado**: cerrada en dirección con Diego. Pendiente de ratificación con abogado contratado y comercial PSP (ver Z.1.7).

#### Z.1.1 — Las tres opciones evaluadas

| Modelo | Operativa del dinero | Comerciante de registro frente al participante |
|---|---|---|
| **A — Split directo puro** | Participante → PSP → cuentas separadas de organizador y Libox. Libox nunca toca el dinero. | Organizador (o PSP como agregador) |
| **B — Escrow real** | Participante → PSP → cuenta Libox; Libox custodia y libera al organizador tras cumplir gates. | Libox |
| **C — Escrow conceptual** (elegida) | Operativa idéntica a A; ledger doble entrada interno como si fuera B. | Organizador (operativo); Libox para reportería y reconciliación |

#### Z.1.2 — Por qué se descartó el Modelo A puro

A puro reduce el ledger interno a un log de pagos. Esto tiene tres consecuencias indeseables para una plataforma con ambición fintech-grade como la del PRD:

1. **Sin reconciliación robusta contra el PSP**: si Mercado Pago reporta un payout distinto al esperado, no hay fuente de verdad interna que detecte el desfase. Tiene que descubrirse manualmente revisando los reports de MP.
2. **Sin evidencia auditada ante disputas**: cuando un participante o un auditor pida la trazabilidad de un pago concreto, Libox solo puede mostrar lo que el PSP reportó, no su propia contabilidad.
3. **Migración futura a escrow real (B) requiere reescribir contabilidad**: si más adelante Libox justifica operar como custodio, no tiene el modelo contable ya validado. Eso es deuda técnica diferida.

El costo incremental de implementar el ledger del PRD sobre operativa A es **bajo** (es disciplina de código, no requiere infraestructura adicional). Saltarlo es una falsa economía.

#### Z.1.3 — Por qué se descartó el Modelo B en MVP

B (escrow real) tiene dos caminos posibles, ambos incompatibles con el plazo de 8-12 semanas y con la etapa "idea pura" del proyecto.

**B.1 — Licencia EEDE propia ante SBS** `[LEGAL→ABOGADO]`:
- Capital mínimo histórico aproximado S/ 2.25M (confirmar monto vigente con el abogado).
- Plan de negocios aprobado por SBS.
- Tecnología auditada por SBS antes de operar.
- Oficial de cumplimiento PLAFT con titulación reconocida.
- Auditoría externa anual.
- Reportes mensuales a SBS.
- Timeline realista: **12-24 meses de licenciamiento + 4-6 meses de build técnico = 18-30 meses al primer organizador real**.

**B.2 — Partnership con EEDE existente o banco fiduciario** `[LEGAL→ABOGADO + COMERCIAL]`:
- Libox se asocia con una EEDE ya autorizada (ej. Bim) o un banco que ofrezca cuentas escrow bajo su licencia.
- Libox da las órdenes de liberación; la EEDE/banco las ejecuta.
- Fees típicos de 0.3-1% sobre el monto custodiado, encima del fee PSP.
- Timeline: **3-6 meses de negociación legal/comercial + 2-3 meses de integración técnica = 5-9 meses al primer organizador**.

Ninguno cabe en MVP-1. **B queda como opción explícita para post-MVP** cuando la tracción justifique el capital regulatorio y el costo operativo.

#### Z.1.4 — Por qué Modelo C es la elección correcta para MVP-1

C combina cuatro propiedades que ningún otro modelo combina:

1. **Tiempo al mercado de A** (8-12 semanas, igual que cualquier marketplace estándar).
2. **Disciplina contable de B** (ledger doble entrada con cuentas Cash Clearing, Purchase Liability, Platform Revenue, Payment Expense, Client Payable, Refund Reserve, Chargeback Loss, Settlement Freeze).
3. **Perfil regulatorio de A** (Libox nunca capta fondos del público; el dinero fluye por el PSP autorizado).
4. **Compatibilidad con migración futura a B** sin reescribir contabilidad. Solo cambian los conectores externos (de "ledger interno con dinero en MP" a "ledger interno con dinero en cuenta escrow propia").

Además, C es el único modelo que preserva la intención arquitectónica del PRD Libox v11 (settlement gates, audit-first, ledger bank-grade) sin forzar al MVP a un modelo regulatorio inviable.

#### Z.1.5 — Implicaciones concretas que los socios deben aceptar

C no es gratis. Los socios deben aceptar conscientemente las siguientes limitaciones del MVP:

1. **Los "settlement gates" del PRD son conceptuales en MVP, no operativos**. El PRD asume implícitamente que Libox puede bloquear el payout al organizador ante una disputa abierta. **En Modelo C esto no es posible**: el dinero fluye según las reglas del PSP, no las de Libox. Los gates internos registran el estado pero no congelan dinero real. Esta conversación se debe tener antes de presentar la plataforma a inversionistas o stakeholders, para evitar que el PRD genere expectativas equivocadas.

2. **Si un organizador desaparece o se niega a entregar el premio, Libox no puede revertir el pago unilateralmente**. La protección al participante se basa en tres capas:
   - **KYC RUC robusto** y revisión manual de organizadores antes de habilitarlos.
   - **Proceso de disputa del PSP** (chargeback dirigido al organizador, no a Libox).
   - **Reputación pública** del organizador en el marketplace + capacidad de baneo.

3. **Refunds operativos requieren la cooperación del organizador o del PSP**. Libox no puede ejecutar reembolsos desde fondos propios. En Modelo B esto sería trivial; en C no.

4. **El chargeback risk lo absorbe el PSP primero**, no Libox. Esto es un beneficio neto del modelo en términos de capital de trabajo, pero significa que Libox depende del PSP para esa protección.

5. **La contabilidad interna debe conciliarse periódicamente contra los reports del PSP**. Si MP reporta un payout que no coincide con el ledger interno, se abre un caso de reconciliation (ya modelado en el PRD). Esto requiere un proceso operativo continuo, no solo código.

#### Z.1.6 — Implicaciones sobre el PRD Libox v11

El PRD asume implícitamente Modelo B (escrow real) en varios lugares. Bajo Modelo C, las siguientes partes se reinterpretan:

| Sección del PRD | Reinterpretación bajo Modelo C |
|---|---|
| Settlement gates (Parte V, Anexo F.2) | Existen como gates internos de estado; no controlan dinero real en MVP. Cuando se migre a B, sí lo controlarán sin cambios de código. |
| Cuenta `Settlement Freeze` (E.1, XI.2) | Existe en el ledger interno como contra-liability; representa estado lógico de bloqueo, no dinero realmente congelado. |
| Cuenta `Refund Reserve` | Existe conceptualmente para cuando Libox absorba refunds (post-MVP). En MVP no se carga porque los refunds los ejecuta el PSP. |
| Cuenta `Chargeback Loss` | En MVP el riesgo lo absorbe el PSP primero; la cuenta existe para registrar los casos excepcionales que escalen a Libox. |
| Gate `PSP_RECONCILED` | **Operativamente vinculante** en C: si el ledger interno no concilia contra MP, no se reconoce el revenue del fee. |

El **resto del PRD (Purchase Engine, Draw Engine, Delivery, Auditoría, APIs, Observabilidad)** queda **plenamente aplicable** bajo Modelo C. La decisión de custodia no contamina esas piezas.

#### Z.1.7 — Validaciones externas pendientes antes de escribir código

La decisión está cerrada en dirección, pero antes de empezar a codificar el módulo de pagos hay que validar:

1. **[ABOGADO]** ¿Operar un marketplace de rifas con boleto pagado bajo organizador RUC califica a Libox como **sujeto obligado UIF-Perú** independientemente del modelo de custodia? Esto define si Libox necesita oficial de cumplimiento PLAFT y manual desde día 1, sin importar A, B o C.
2. **[ABOGADO]** Confirmar que bajo Modelo C la actividad de Libox NO califica como **captación de fondos del público** regulada por SBS (Ley 26702, Ley 29985 de Dinero Electrónico).
3. **[ABOGADO]** Análisis explícito del riesgo de la "zona gris": que Libox nunca tenga una cuenta bancaria propia que reciba dinero del participante **incluso por minutos**. Si la integración con MP terminara enrutando dinero por una cuenta intermedia controlada por Libox, eso debería rechazarse.
4. **[COMERCIAL MERCADO PAGO PERÚ]** Confirmar que la API Marketplace Sellers está disponible operativamente en Perú, con cobertura de Yape como método de pago para el participante final.
5. **[COMERCIAL MP]** Confirmar tiempos reales de payout al organizador, % de reserva por seguridad, proceso de disputa y disponibilidad (si existe) de "release on command" para retener payout hasta orden de Libox.
6. **[COMERCIAL — ALTERNATIVOS]** Validar si Culqi, Izipay o Niubiz ofrecen un modelo marketplace equivalente, como contingencia ante limitaciones de MP en Perú.

#### Z.1.8 — Preguntas para discutir con socios

Si los socios cuestionan la decisión, estos son los pivotes de discusión:

1. ¿Aceptamos que el MVP no tenga capacidad de bloquear payouts ante disputas, como compensación por llegar al mercado en 3 meses en lugar de 12-30?
2. ¿Aceptamos que la protección al participante en MVP se base en **KYC + curaduría manual + disputa PSP**, en lugar de escrow real?
3. ¿Estamos dispuestos a **documentar transparentemente esto** al primer organizador (en el contrato B2B) y al participante (vía Términos y Condiciones) para evitar falsas expectativas?
4. ¿Queremos comprometer en el roadmap una **fecha tentativa para migrar a Modelo B** (escrow real con partnership EEDE), o lo dejamos como "evaluación post-MVP" sin fecha?
5. Si el abogado dictaminara que **incluso Modelo C requiere oficial de cumplimiento PLAFT** desde día 1 (por la naturaleza de "rifa" como actividad regulada), ¿quién del equipo asume ese rol o se contrata externamente?

---

### Z.2 — Elección de PSP (cerrada en dirección el 2026-06-05)

**Decisión**: **Mercado Pago como PSP primario**, mecanismo de comisión **split en la fuente** (application fee / marketplace). **Culqi** como **segundo rail a implementar en una fase posterior del MVP** — qué fase exactamente queda como **decisión de socios**. Decisión final supeditada a verificación comercial (ver Z.2.5). ADR canónico autocontenido: [`decisions/Z2-eleccion-psp.md`](../decisions/Z2-eleccion-psp.md).

#### Z.2.1 — Por qué el PSP se volvió un problema (no era preferencia)

El cierre de Z.1 (custodia = Modelo C) impuso una restricción dura: **Libox nunca toca el dinero pero igual cobra su 20%**. Eso solo es posible si el pago se **divide en la fuente** (split / application fee), capacidad que **no todos los PSP peruanos tienen**. Así, la elección de PSP dejó de ser preferencia de DX y pasó a ser satisfacción de una restricción. La "Mercado Pago" del PRD podía ser correcta, pero por una razón que el PRD no enuncia (es de los pocos con marketplace maduro).

#### Z.2.2 — Inputs de Diego que afinaron la decisión (2026-06-05)

- **Mecanismo de comisión: split en la fuente** (confirmado, no postpago). Evita riesgo de cobranza; coherente con Modelo C.
- **Precio de ticket: mixto (S/1–50)** → se necesita tarjeta **y** Yape bien cubiertos.
- **Sin relación bancaria/PSP previa** → se elige por mérito de producto, sin sesgo hacia Culqi/Izipay por tarifas.

#### Z.2.3 — El insight decisivo: Yape debe ir DENTRO del checkout marketplace

Yape directo paga a **un** solo comercio; no se divide. Por lo tanto **no se puede "agregar Yape" como rail lateral** sin romper el split del Modelo C. Para que el split aplique también a pagos Yape, **Yape tiene que venir integrado en el checkout del PSP marketplace**. Esto reduce toda la elección a una pregunta: *¿qué PSP ofrece split marketplace que TAMBIÉN aplique a pagos Yape?*

#### Z.2.4 — Por qué MP primario y Culqi como segundo rail

- **Mercado Pago**: único con split marketplace que se puede afirmar con confianza razonable. Penetración local menor y posible brecha en Yape (a verificar), pero es el camino que satisface la restricción hoy.
- **Culqi (familia BCP/Krealo)**: mejor posicionado para Yape integrado y DX local, **pero su capacidad de split es la incógnita**. Si la confirma, es el retador natural. Se decide implementarlo como **segundo rail en fase posterior** para: (a) cobertura Yape si MP cojea ahí, (b) redundancia ante caídas de un PSP, (c) poder comcompetitivo en fees.
- **Izipay / Niubiz / PagoEfectivo**: fuera como rail primario (Niubiz no hace split; PagoEfectivo es complemento de efectivo para no bancarizados).

#### Z.2.5 — Validaciones comerciales pendientes (compuerta) `[VERIFICAR→COMERCIAL]`

Misma batería a **Mercado Pago Perú** y a **Culqi**; las preguntas 1 y 2 son **eliminatorias**:

1. ¿Soportan **split a múltiples beneficiarios** (marketplace / application fee) con un comercio facilitador que cobra comisión, en una sola transacción?
2. ¿Ese split **aplica a pagos con Yape**, o solo a tarjeta?
3. ¿El **vendedor (organizador RUC)** debe crear cuenta + KYC con el PSP para recibir su parte? ¿Cómo es ese onboarding?
4. **Fees** por método (tarjeta / Yape / transferencia) y por volumen.
5. **Tiempos de payout** al vendedor y **reservas/retenciones** por riesgo.
6. **Webhooks firmados, idempotencia y reportes de settlement** descargables (para conciliar contra el ledger interno — gate `PSP_RECONCILED`).
7. Manejo de **refunds y chargebacks** en modelo marketplace: ¿quién absorbe primero?

> Contingencia: si MP **no** aplica split a Yape y Culqi **sí**, se reevalúa cuál es el primario. La dirección "MP primario" asume que MP pasa las preguntas 1 y 2.

#### Z.2.6 — Implicaciones que los socios deben aceptar

1. **Cada organizador deberá crear cuenta y pasar KYC con el PSP** (MP) para cobrar. Es el punto más débil del modelo marketplace: fricción de onboarding del lado del organizador. Aceptable para organizadores RUC, pero hay que diseñarlo en el flujo.
2. El dinero del organizador **aterriza primero en su wallet del PSP**, no directo en su banco; él retira después. Libox no controla ese paso.
3. La **fecha/fase de entrada de Culqi** queda abierta y es decisión de socios; no bloquea el MVP-1.

#### Z.2.7 — Impacto sobre el PRD

El PRD ya asume Mercado Pago y webhooks `mercadopago` (Parte III, Anexo D). La decisión **confirma y aterriza** esa asunción, añadiendo: split en la fuente como mecanismo, Yape como requisito de checkout, y Culqi como segundo rail futuro (el PRD es mono-PSP; el adaptador PSP debe diseñarse multi-PSP desde el inicio para no refactorizar al sumar Culqi).

---

### Z.3 — Tipo de organizador (cerrada el 2026-06-05)

**Decisión**: organizador en MVP = **cualquier persona, natural o jurídica, con RUC activo** (Opción 2). Incluye empresas/ONGs/instituciones **y** personas naturales con negocio / RUC activo. Se **descarta** la persona solo-DNI sin RUC (Opción 3). ADR canónico autocontenido: [`decisions/Z3-tipo-de-organizador.md`](../decisions/Z3-tipo-de-organizador.md).

#### Z.3.1 — No era contradicción, sino un corte a elegir

El PRD es agnóstico ("Cliente" genérico). El plan había elegido "solo personas jurídicas". El trabajo fue elegir el corte correcto, no resolver una oposición.

#### Z.3.2 — La imprecisión corregida: "solo RUC" ≠ "solo personas jurídicas"

En Perú el RUC lo tienen también las personas naturales (con negocio / RUC activo). "Tener RUC" es más amplio que "ser persona jurídica". Eso abre 3 opciones: (1) solo jurídicas, (2) cualquiera con RUC, (3) cualquier persona natural con DNI.

#### Z.3.3 — Restricciones y por qué se descarta la Opción 3

Ancla dura: Libox factura su comisión 20% como **servicio B2B** → el organizador **necesita RUC** sí o sí. Eso descarta la Opción 3 (solo-DNI) por imposibilidad de facturación + riesgo PLAFT. Autorización municipal para personas naturales = `[LEGAL→ABOGADO]` pendiente.

#### Z.3.4 — Por qué Opción 2 (inputs de Diego)

Target incluye **individuos formalizados con RUC**; postura **máximo alcance legal**. La Opción 2 es solo marginalmente más riesgosa que la 1 (sigue exigiendo RUC) pero abre mercado bastante mayor. Costo: una segunda plantilla de KYC.

#### Z.3.5 — Implicaciones de build

- `Organization.tipo` (`juridica` | `natural_con_ruc`) — no hardcodear; expansión futura = configuración.
- Dos plantillas KYC: jurídica (RUC + representante legal + vigencia de poderes) y natural-con-RUC (RUC + DNI). Ambas validan RUC activo/habido contra padrón SUNAT.
- Comprobante al participante lo emite el organizador (merchant of record bajo Modelo C).

#### Z.3.6 — Validaciones pendientes y preguntas para socios

`[LEGAL→ABOGADO]`: ¿persona natural con RUC puede obtener autorización municipal de rifa? (si no, restringe por jurisdicción, no global). Tratamiento fiscal del boleto. Impacto PLAFT de incluir naturales. Preguntas para socios: ¿go-to-market inicial solo empresas aunque el sistema permita ambos?; ¿construir doble KYC desde MVP-1 o sumar naturales en fase siguiente?

---

### Z.4 — Tipos de sorteo en MVP-1 (cerrada el 2026-06-05)

**Decisión**: el MVP-1 construye **un solo motor de sorteo configurable**, de **1 ganador**, modo **AUTO + Admin**, con dos disparadores combinables — **umbral opcional + fecha opcional** — y **ruta de fallo-y-refund**. Esto entrega **T1, T2, T3 y T4 como presets** del mismo motor. Se **difiere**: T5 (UX flash), T6 (multi-ganador), T7 (progresivo), T8 (LIVE → [Z.5]). ADR canónico: [`decisions/Z4-tipos-de-sorteo.md`](../decisions/Z4-tipos-de-sorteo.md).

#### Z.4.1 — Reframe: los tipos son presets, no motores

Los 8 tipos del PRD se descomponen en 3 ejes ortogonales: **disparo** (sold-out / umbral / fecha / umbral-o-fecha / ventana corta / milestones), **n° de ganadores** (1 / N) y **modo** (AUTO / Admin / LIVE). T1–T4 son el mismo motor con el eje "disparo" en distintas posiciones. La pregunta correcta no es "cuántos tipos", sino "qué posiciones de cada eje soporta el MVP". El PRD ya lo pide: "configuraciones ejecutables".

#### Z.4.2 — El acople con el refund (Modelo C)

Soportar umbral/fecha obliga a definir qué pasa si el sorteo no se completa → **falla y se devuelve a todos**. Bajo Modelo C ([Z.1](../decisions/Z1-custodia-del-dinero.md)) los refunds los ejecuta el organizador/PSP, así que construir umbral/fecha **arrastra la ruta de fallo-y-refund** (toca el módulo de pagos). T1 puro lo evitaría pero arriesga deadlock; T3 puro lo evitaría pero arriesga sortear con pool diminuto. Un MVP creíble necesita umbral + fecha + refund.

#### Z.4.3 — Inputs de Diego (2026-06-05)

Disparo: **motor configurable umbral+fecha+refund** (no solo un preset). Ganadores: **solo 1** en MVP-1.

#### Z.4.4 — Implicaciones de build

- **`draw_config`** con campos: `trigger_threshold` (nullable), `trigger_deadline` (nullable), `winners=1` (fijo en MVP-1), `mode ∈ {AUTO, ADMIN}`. Motor evalúa "elegible para sortear" y "fallido" a partir de esos campos.
- **Ruta de fallo-y-refund**: estado `FAILED` del sorteo + disparo de refund vía PSP a todos los participantes. Dependencia explícita del módulo de pagos.
- **Proof** cubre 1 ganador (más simple). Diseñar el motor para que extender a N ganadores (T6) sea agregar iteración sin repetición, no reescritura.
- T5 (flash) sale "gratis" como fecha cercana; se difiere solo la UX de urgencia.

#### Z.4.5 — Impacto sobre el PRD

Se respeta el diseño "tipos = `draw_config` versionado". MVP-1 implementa el subconjunto {T1–T4, 1 ganador, AUTO/Admin}. T6/T7/T8 quedan como configuraciones futuras del mismo motor, no como reescrituras. El algoritmo de fairness (pool_hash → entropía → seed → random_value) es idéntico para todos los tipos.

---

### Z.5 — T8 LIVE (cerrada el 2026-06-05)

**Decisión**: **T8 LIVE se difiere a MVP-3**. En MVP-1/2 el sorteo se ejecuta solo en modo AUTO (sistema) y Admin. ADR canónico: [`decisions/Z5-t8-live.md`](../decisions/Z5-t8-live.md).

#### Z.5.1 — Qué agrega LIVE (y qué no)

LIVE es el eje "modo" de [Z.4](../decisions/Z4-tipos-de-sorteo.md): el **organizador ejecuta el sorteo en vivo** (streaming), solo con autorización previa de Admin. **No cambia el algoritmo** — pool_hash, entropía externa, seed y proof son idénticos al modo AUTO. Lo que agrega es capa de experiencia y control: streaming/tiempo real, flujo de autorización (`LIVE_AUTHORIZED` / `LIVE_TRIGGER_REJECTED`), y controles anti-manipulación percibida.

#### Z.5.2 — Por qué diferir, y por qué a MVP-3

- Es un **diferenciador de crecimiento**, no parte del core-loop (comprar → sortear → entregar → liquidar). El core debe estar sólido primero.
- Depende de que el **ciclo económico esté cerrado** (Delivery + Settlement + disputa = MVP-2). Recién sobre esa base tiene sentido sumar la capa LIVE → de ahí **MVP-3**, no MVP-2.
- Suma infraestructura de tiempo real y superficie de soporte (latencia, caídas en vivo) que no conviene cargar en un MVP que aún valida el mercado.
- Riesgo de **manipulación percibida** (un host en vivo "podría" parecer que arregla el sorteo); se mitiga con el proof reproducible, pero requiere comunicación y UX cuidada que no es prioridad temprana.

#### Z.5.3 — Implicación de build

El motor de [Z.4](../decisions/Z4-tipos-de-sorteo.md) ya modela `mode ∈ {AUTO, ADMIN}`. LIVE es **un tercer valor del mismo enum** que reutiliza el algoritmo; sumarlo en MVP-3 es additivo (autorización + capa realtime), no reescritura. Mantener el campo `mode` desde MVP-1 evita refactor.

---

### Z.6 — Stack tecnológico (cerrada en dirección el 2026-06-06)

**Decisión**: **Next.js (App Router) para todo**. Libox **no es web estática** (solo 2-3 de 8 superficies lo son; el core comprar→sortear→entregar→liquidar es dinámico y transaccional), por lo que se descartó Astro — optimizado para el caso inverso (contenido + islas). Next cubre la superficie pública (SEO vía RSC/ISR) y la app autenticada con un solo framework maduro. Stack: Next.js+TS, Tailwind+shadcn/ui, PostgreSQL, Drizzle (preferido), job runner gestionado (Inngest/Trigger), auth con MFA (Clerk/Supabase), Mercado Pago multi-PSP, Vercel, Sentry+PostHog. El job runner es **crítico** (outbox, disparo de sorteo, conciliación). ADR canónico: [`decisions/Z6-stack-tecnologico.md`](../decisions/Z6-stack-tecnologico.md). Sub-decisiones al scaffold: ORM, job runner, auth, DB host.

### Z.7 — Versionamiento y flujo de repositorio (cerrada el 2026-06-06)

**Decisión**: desde ya (pre-código) — **Semantic Versioning** (arranca `0.1.0`), **Conventional Commits**, **release-please** (versión + CHANGELOG automáticos), **CHANGELOG.md** Keep a Changelog, **`main` protegida** + PRs, y **GitHub Actions** de alcance creciente (hoy: commitlint + lint/links de docs; con código: typecheck/test/build). Matiz: el repo es hoy solo-docs, así que se adoptan las convenciones ahora y el semver formal madura con el código (`release-type: simple` → `node`). Branch protection y creación del remoto las hace Diego en GitHub (pasos en `CONTRIBUTING.md`). ADR canónico: [`decisions/Z7-versionamiento.md`](../decisions/Z7-versionamiento.md).

### Z.8 — Roles de memoria y contexto (cerrada el 2026-06-06)

**Decisión**: tras instalar plugins (context-mode, claude-mem, get-shit-done…), se asignan **carriles** para que los mecanismos de memoria/contexto no compitan: **`docs/` + `MEMORY.md`** = fuente curada y compartible (la verdad del proyecto, versionada); **`context-mode`** = procesar outputs grandes sin gastar contexto; **`claude-mem`** = captura cross-sesión secundaria (a prueba; se desactiva si duplica sin aportar); **GSD** = framework de workflow, no memoria. Regla de oro: toda decisión cerrada se documenta como ADR + Anexo Z, nunca se delega a la captura automática; la memoria auto-capturada no es autoritativa. ADR canónico: [`decisions/Z8-roles-memoria-contexto.md`](../decisions/Z8-roles-memoria-contexto.md). Versión operativa en [`CLAUDE.md`](../../CLAUDE.md).

---

## 8. Verificación de este plan

No hay código que correr todavía. Validación = revisión humana:

- Diego revisa este documento y comparte el **Anexo Z** con los socios.
- Los 4 conflictos originales PRD vs plan están **cerrados** (Z.1–Z.5), más Z.6–Z.8. Cada decisión nueva se discute caso por caso y se cierra como entrada en el **Anexo Z** (sigue Z.9).
- Las validaciones marcadas `[LEGAL→ABOGADO]` y `[COMERCIAL]` se cierran antes de escribir código del módulo correspondiente.
- Las decisiones cerradas se reflejan en `docs/README.md` y se espejan a la colección Outline "Libox — Desarrollo".
- El `CLAUDE.md` del repo ya existe y opera como guía de sesión.
