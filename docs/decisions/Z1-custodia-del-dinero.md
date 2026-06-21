---
title: Z.1 — Custodia del dinero
status: cerrada-en-direccion
tags: [libox, decision, custodia, pagos, compliance]
decided: 2026-06-05
relates: [docs/compliance-peru.md, docs/plans/libox-plan.md]
updated: 2026-06-05
---

# Z.1 — Custodia del dinero

**Estado**: Cerrada en dirección (2026-06-05). Pendiente de ratificación con abogado y comercial PSP.
**Decisor**: Diego (con conformidad pendiente de socios y abogado).
**Documento canónico**: este archivo. Hay un mirror en [`docs/plans/libox-plan.md`](../plans/libox-plan.md#z1--custodia-del-dinero-cerrada-el-2026-06-05) (Anexo Z.1); ante divergencia, este archivo manda.

> ⚠️ Los puntos marcados `[LEGAL→ABOGADO]` son lectura del autor sobre normativa pública peruana, **no asesoría legal**, y deben ratificarse con el abogado del equipo antes de tomar acción operativa.

---

## Decisión

Libox opera el MVP-1 bajo **Modelo C — escrow conceptual**:

- **Operativamente**: split directo vía PSP marketplace (probable Mercado Pago). El dinero del participante nunca pasa por cuentas controladas por Libox.
- **Internamente**: Libox lleva el **ledger doble entrada del PRD Libox v11** desde día 1, registrando conceptualmente los flujos como si custodiara el dinero, incluso cuando no lo hace.

---

## Las tres opciones evaluadas

| Modelo | Operativa del dinero | Comerciante de registro frente al participante |
|---|---|---|
| **A — Split directo puro** | Participante → PSP → cuentas separadas de organizador y Libox. Libox nunca toca el dinero. | Organizador (o PSP como agregador) |
| **B — Escrow real** | Participante → PSP → cuenta Libox; Libox custodia y libera al organizador tras cumplir gates. | Libox |
| **C — Escrow conceptual** (elegida) | Operativa idéntica a A; ledger doble entrada interno como si fuera B. | Organizador (operativo); Libox para reportería y reconciliación |

---

## Por qué se descartó el Modelo A puro

A puro reduce el ledger interno a un log de pagos. Esto tiene tres consecuencias indeseables para una plataforma con ambición fintech-grade como la del PRD:

1. **Sin reconciliación robusta contra el PSP**: si Mercado Pago reporta un payout distinto al esperado, no hay fuente de verdad interna que detecte el desfase. Tiene que descubrirse manualmente revisando los reports de MP.
2. **Sin evidencia auditada ante disputas**: cuando un participante o un auditor pida la trazabilidad de un pago concreto, Libox solo puede mostrar lo que el PSP reportó, no su propia contabilidad.
3. **Migración futura a escrow real (B) requiere reescribir contabilidad**: si más adelante Libox justifica operar como custodio, no tiene el modelo contable ya validado. Es deuda técnica diferida.

El costo incremental de implementar el ledger del PRD sobre operativa A es **bajo** (es disciplina de código, no requiere infraestructura adicional). Saltarlo es una falsa economía.

---

## Por qué se descartó el Modelo B en MVP

B (escrow real) tiene dos caminos, ambos incompatibles con el plazo de 8-12 semanas y con la etapa "idea pura" del proyecto.

### B.1 — Licencia EEDE propia ante SBS `[LEGAL→ABOGADO]`

- Capital mínimo histórico aproximado S/ 2.25M (confirmar monto vigente con el abogado).
- Plan de negocios aprobado por SBS.
- Tecnología auditada por SBS antes de operar.
- Oficial de cumplimiento PLAFT con titulación reconocida.
- Auditoría externa anual.
- Reportes mensuales a SBS.
- **Timeline realista: 12-24 meses de licenciamiento + 4-6 meses de build técnico = 18-30 meses al primer organizador real**.

### B.2 — Partnership con EEDE existente o banco fiduciario `[LEGAL→ABOGADO + COMERCIAL]`

- Libox se asocia con una EEDE ya autorizada (ej. Bim) o un banco que ofrezca cuentas escrow bajo su licencia.
- Libox da las órdenes de liberación; la EEDE/banco las ejecuta.
- Fees típicos de 0.3-1% sobre el monto custodiado, encima del fee PSP.
- **Timeline: 3-6 meses de negociación legal/comercial + 2-3 meses de integración técnica = 5-9 meses al primer organizador**.

Ninguno cabe en MVP-1. **B queda como opción explícita para post-MVP** cuando la tracción justifique el capital regulatorio y el costo operativo.

---

## Por qué Modelo C es la elección correcta para MVP-1

C combina cuatro propiedades que ningún otro modelo combina:

1. **Tiempo al mercado de A** (8-12 semanas, igual que cualquier marketplace estándar).
2. **Disciplina contable de B** (ledger doble entrada con cuentas Cash Clearing, Purchase Liability, Platform Revenue, Payment Expense, Client Payable, Refund Reserve, Chargeback Loss, Settlement Freeze).
3. **Perfil regulatorio de A** (Libox nunca capta fondos del público; el dinero fluye por el PSP autorizado).
4. **Compatibilidad con migración futura a B** sin reescribir contabilidad. Solo cambian los conectores externos (de "ledger interno con dinero en MP" a "ledger interno con dinero en cuenta escrow propia").

C es además el único modelo que preserva la intención arquitectónica del PRD Libox v11 (settlement gates, audit-first, ledger bank-grade) sin forzar al MVP a un modelo regulatorio inviable.

---

## Implicaciones concretas que los socios deben aceptar

C no es gratis. Los socios deben aceptar conscientemente las siguientes limitaciones del MVP:

1. **Los "settlement gates" del PRD son conceptuales en MVP, no operativos**. El PRD asume implícitamente que Libox puede bloquear el payout al organizador ante una disputa abierta. **En Modelo C esto no es posible**: el dinero fluye según las reglas del PSP, no las de Libox. Los gates internos registran el estado pero no congelan dinero real. Esta conversación se debe tener antes de presentar la plataforma a inversionistas o stakeholders para evitar que el PRD genere expectativas equivocadas.

2. **Si un organizador desaparece o se niega a entregar el premio, Libox no puede revertir el pago unilateralmente**. La protección al participante se basa en tres capas:
   - **KYC RUC robusto** y revisión manual de organizadores antes de habilitarlos.
   - **Proceso de disputa del PSP** (chargeback dirigido al organizador, no a Libox).
   - **Reputación pública** del organizador en el marketplace + capacidad de baneo.

3. **Refunds operativos requieren la cooperación del organizador o del PSP**. Libox no puede ejecutar reembolsos desde fondos propios. En Modelo B esto sería trivial; en C no.

4. **El chargeback risk lo absorbe el PSP primero**, no Libox. Esto es un beneficio neto del modelo en términos de capital de trabajo, pero significa que Libox depende del PSP para esa protección.

5. **La contabilidad interna debe conciliarse periódicamente contra los reports del PSP**. Si MP reporta un payout que no coincide con el ledger interno, se abre un caso de reconciliation (ya modelado en el PRD). Esto requiere un proceso operativo continuo, no solo código.

---

## Implicaciones sobre el PRD Libox v11

El PRD asume implícitamente Modelo B (escrow real) en varios lugares. Bajo Modelo C, las siguientes partes se reinterpretan:

| Sección del PRD | Reinterpretación bajo Modelo C |
|---|---|
| Settlement gates (Parte V, Anexo F.2) | Existen como gates internos de estado; no controlan dinero real en MVP. Cuando se migre a B, sí lo controlarán sin cambios de código. |
| Cuenta `Settlement Freeze` (E.1, XI.2) | Existe en el ledger interno como contra-liability; representa estado lógico de bloqueo, no dinero realmente congelado. |
| Cuenta `Refund Reserve` | Existe conceptualmente para cuando Libox absorba refunds (post-MVP). En MVP no se carga porque los refunds los ejecuta el PSP. |
| Cuenta `Chargeback Loss` | En MVP el riesgo lo absorbe el PSP primero; la cuenta existe para registrar los casos excepcionales que escalen a Libox. |
| Gate `PSP_RECONCILED` | **Operativamente vinculante** en C: si el ledger interno no concilia contra MP, no se reconoce el revenue del fee. |

El **resto del PRD (Purchase Engine, Draw Engine, Delivery, Auditoría, APIs, Observabilidad)** queda **plenamente aplicable** bajo Modelo C. La decisión de custodia no contamina esas piezas.

---

## Validaciones externas pendientes antes de escribir código

La decisión está cerrada en dirección, pero antes de empezar a codificar el módulo de pagos hay que validar:

1. **[ABOGADO]** ¿Operar un marketplace de rifas con boleto pagado bajo organizador RUC califica a Libox como **sujeto obligado UIF-Perú** independientemente del modelo de custodia? Define si Libox necesita oficial de cumplimiento PLAFT y manual desde día 1, sin importar A, B o C.
2. **[ABOGADO]** Confirmar que bajo Modelo C la actividad de Libox NO califica como **captación de fondos del público** regulada por SBS (Ley 26702, Ley 29985 de Dinero Electrónico).
3. **[ABOGADO]** Análisis explícito del riesgo de la "zona gris": que Libox nunca tenga una cuenta bancaria propia que reciba dinero del participante **incluso por minutos**. Si la integración con MP terminara enrutando dinero por una cuenta intermedia controlada por Libox, eso debería rechazarse.
4. **[COMERCIAL MERCADO PAGO PERÚ]** Confirmar que la API Marketplace Sellers está disponible operativamente en Perú, con cobertura de Yape como método de pago para el participante final.
5. **[COMERCIAL MP]** Confirmar tiempos reales de payout al organizador, % de reserva por seguridad, proceso de disputa, y disponibilidad (si existe) de "release on command" para retener payout hasta orden de Libox.
6. **[COMERCIAL — ALTERNATIVOS]** Validar si Culqi, Izipay o Niubiz ofrecen un modelo marketplace equivalente, como contingencia ante limitaciones de MP en Perú.

---

## Preguntas para discutir con socios

Si los socios cuestionan la decisión, estos son los pivotes de discusión:

1. ¿Aceptamos que el MVP no tenga capacidad de bloquear payouts ante disputas, como compensación por llegar al mercado en 3 meses en lugar de 12-30?
2. ¿Aceptamos que la protección al participante en MVP se base en **KYC + curaduría manual + disputa PSP**, en lugar de escrow real?
3. ¿Estamos dispuestos a **documentar transparentemente esto** al primer organizador (en el contrato B2B) y al participante (vía Términos y Condiciones) para evitar falsas expectativas?
4. ¿Queremos comprometer en el roadmap una **fecha tentativa para migrar a Modelo B** (escrow real con partnership EEDE), o lo dejamos como "evaluación post-MVP" sin fecha?
5. Si el abogado dictaminara que **incluso Modelo C requiere oficial de cumplimiento PLAFT** desde día 1 (por la naturaleza de "rifa" como actividad regulada), ¿quién del equipo asume ese rol o se contrata externamente?
