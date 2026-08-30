---
title: Z.2 — Elección de PSP
status: cerrada-en-direccion
tags: [libox, decision, psp, pagos, mercadopago, culqi, yape]
decided: 2026-06-05
relates: [docs/decisions/Z1-custodia-del-dinero.md, docs/plans/libox-plan.md, docs/compliance-peru.md]
updated: 2026-06-05
---

# Z.2 — Elección de PSP

**Estado**: Cerrada en dirección (2026-06-05). Decisión final supeditada a verificación comercial (ver más abajo).
**Decisor**: Diego (con conformidad pendiente de socios para la fase de entrada de Culqi).
**Documento canónico**: este archivo. Mirror corto en [`docs/plans/libox-plan.md`](../plans/libox-plan.md#z2--elección-de-psp-cerrada-en-dirección-el-2026-06-05) (Anexo Z.2).
**Depende de**: [Z.1 — Custodia del dinero](Z1-custodia-del-dinero.md) (Modelo C es la causa de la restricción de split).

> ⚠️ Los puntos marcados `[VERIFICAR→COMERCIAL]` son conocimiento general de mercado que puede estar desactualizado y deben confirmarse con el comercial del PSP antes de comprometer integración.

---

## Decisión

- **PSP primario**: **Mercado Pago**.
- **Mecanismo de comisión**: **split en la fuente** (application fee / marketplace). El pago del participante se divide en la misma transacción: ~80% a la cuenta del organizador, ~20% a Libox. Libox nunca custodia el dinero (coherente con [Modelo C](Z1-custodia-del-dinero.md)).
- **Segundo rail**: **Culqi**, a implementar en una **fase posterior del MVP**. Qué fase exactamente = **decisión de socios**. No bloquea MVP-1.
- **Compuerta**: la decisión final está supeditada a verificación comercial; las preguntas 1 y 2 del cuestionario (ver abajo) son **eliminatorias**.

---

## Por qué el PSP se volvió un problema (no era preferencia)

En la superficie el conflicto era trivial: el PRD dice "Mercado Pago", el plan decía "comparemos". Parecía preferencia. No lo era.

El cierre de [Z.1](Z1-custodia-del-dinero.md) (custodia = Modelo C) impuso una restricción dura: **Libox nunca toca el dinero, pero igual cobra su 20%**. Eso solo es posible si el pago se **divide en la fuente** (split / application fee), una capacidad técnica que **no todos los PSP peruanos tienen** — la mayoría son acquirers de un solo comercio.

Por eso la elección dejó de ser preferencia de DX y pasó a ser **satisfacción de una restricción**. La "Mercado Pago" del PRD podía ser correcta, pero por una razón que el PRD no enuncia: es de los pocos con producto marketplace maduro.

Si se eligiera un PSP sin split nativo, solo quedarían dos salidas, ambas malas:
1. Libox recibe el 100% y luego paga al organizador → eso **es** Modelo B (escrow real) → reactiva el riesgo SBS/captación de fondos que evitamos.
2. El organizador recibe el 100% y Libox le factura la comisión después → riesgo de cobranza + peor cashflow.

---

## Inputs de Diego que afinaron la decisión (2026-06-05)

| Input | Valor | Consecuencia |
|---|---|---|
| Mecanismo de comisión | **Split en la fuente** (no postpago) | Exige PSP con producto marketplace. Descarta acquirers de comercio único. |
| Precio de ticket | **Mixto (S/1–50)** | Se necesita tarjeta **y** Yape bien cubiertos; un rail solo-tarjeta cojea en la mitad baja. |
| Relación bancaria previa | **Ninguna** | Se elige por mérito de producto, sin sesgo de tarifas hacia Culqi/Izipay. |

---

## El insight decisivo: Yape debe ir DENTRO del checkout marketplace

Yape directo paga a **un** solo comercio; el monto no se divide. Por lo tanto **no se puede "agregar Yape" como rail lateral** junto al PSP de tarjetas — si se hace, los pagos Yape irían 100% a una cuenta y romperían el split del Modelo C.

Para que el split aplique también a los pagos Yape, **Yape tiene que venir integrado dentro del checkout del PSP marketplace**, de modo que el mismo motor que divide la tarjeta divida también el Yape.

Esto reduce toda la elección a una sola pregunta:

> **¿Qué PSP ofrece split marketplace que TAMBIÉN aplique a pagos Yape dentro de su checkout?**

No "quién tiene Yape" ni "quién tiene split" por separado — quién tiene **las dos cosas integradas**.

---

## Candidatos evaluados

Confianza limitada: conocimiento general de mercado, puede estar desactualizado. Todo "split marketplace" en PSP local debe verificarse `[VERIFICAR→COMERCIAL]`.

| PSP | Grupo | Split marketplace | Yape | Veredicto |
|---|---|---|---|---|
| **Mercado Pago** | MercadoLibre | **Sí, maduro** en LATAM `[VERIFICAR Perú]` | ¿En checkout PE? `[VERIFICAR]` | **Primario.** Único con split probado. |
| **Culqi** | Krealo (Credicorp/BCP) | **Incierto** `[VERIFICAR]` | **Fuerte** (familia BCP) | **Segundo rail futuro.** Retador si confirma split. |
| **Izipay** | Interbank + Scotiabank | Incierto `[VERIFICAR]` | Sí `[VERIFICAR]` | Fuera del MVP. |
| **Niubiz** (ex-VisaNet) | Bancos PE | Acquirer puro, probablemente no | Vía checkout | Fuera (no split). |
| **PagoEfectivo** | — | No es marketplace | N/A | Complemento de efectivo para no bancarizados, no rail principal. |

---

## Por qué MP primario y Culqi como segundo rail

- **Mercado Pago**: único con split marketplace afirmable con confianza razonable. Penetración local menor y posible brecha en Yape (a verificar), pero es el camino que satisface la restricción **hoy**.
- **Culqi**: mejor posicionado para Yape integrado y DX local, pero su split es la incógnita. Se implementa como **segundo rail en fase posterior** para: (a) cobertura Yape si MP cojea ahí, (b) redundancia ante caídas de un PSP, (c) poder de negociación en fees.

---

## Validaciones comerciales pendientes (compuerta) `[VERIFICAR→COMERCIAL]`

Misma batería a **Mercado Pago Perú** y a **Culqi**. Las preguntas 1 y 2 son **eliminatorias**:

1. ¿Soportan **split a múltiples beneficiarios** (marketplace / application fee), con un comercio facilitador que cobra comisión y el resto va al vendedor, en una sola transacción?
2. ¿Ese split **aplica a pagos con Yape**, o solo a tarjeta?
3. ¿El **vendedor (organizador RUC)** debe crear cuenta + KYC con el PSP para recibir su parte? ¿Cómo es ese onboarding?
4. **Fees** por método (tarjeta / Yape / transferencia) y por volumen.
5. **Tiempos de payout** al vendedor y **reservas/retenciones** por riesgo.
6. **Webhooks firmados, idempotencia y reportes de settlement** descargables (para conciliar contra el ledger interno — gate `PSP_RECONCILED` del PRD).
7. Manejo de **refunds y chargebacks** en modelo marketplace: ¿quién absorbe primero?

> **Contingencia**: si MP **no** aplica split a Yape y Culqi **sí**, se reevalúa cuál es el primario. La dirección "MP primario" asume que MP pasa las preguntas 1 y 2.

---

## Implicaciones que los socios deben aceptar

1. **Cada organizador deberá crear cuenta y pasar KYC con el PSP** (MP) para cobrar. Es el punto más débil del modelo marketplace: fricción de onboarding del lado del organizador. Aceptable para organizadores RUC, pero hay que diseñarlo explícitamente en el flujo de alta.
2. El dinero del organizador **aterriza primero en su wallet del PSP**, no directo en su banco; él retira después. Libox no controla ese paso.
3. La **fecha/fase de entrada de Culqi** queda abierta y es **decisión de socios**; no bloquea el MVP-1.

---

## Impacto sobre el PRD Libox v11

El PRD ya asume Mercado Pago y nombra webhooks `mercadopago` (Parte III, Anexo D). Esta decisión **confirma y aterriza** esa asunción, añadiendo:

- **Split en la fuente** como mecanismo explícito de comisión.
- **Yape como requisito de checkout**, no como rail aparte.
- **Culqi como segundo rail futuro**: el PRD es mono-PSP, así que el **adaptador PSP debe diseñarse multi-PSP desde el inicio** (interfaz común, implementaciones intercambiables) para no refactorizar al sumar Culqi.

---

## Preguntas para discutir con socios

1. ¿En qué **fase del MVP** entra Culqi como segundo rail? (Depende de si MP cubre Yape bien; si lo cubre, Culqi puede esperar más.)
2. ¿Aceptamos la **fricción de onboarding** de que cada organizador cree cuenta + KYC con MP para cobrar? ¿Cómo lo comunicamos en el alta?
3. ¿Quién del equipo hace las **llamadas comerciales** a MP y Culqi y para cuándo? (Bloquea el inicio del módulo de pagos.)
4. Si ambos PSP pasan las preguntas eliminatorias, ¿el criterio de desempate es **fees**, **cobertura Yape**, o **calidad de API**?
