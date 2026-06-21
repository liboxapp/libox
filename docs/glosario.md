---
title: Glosario de términos
status: vivo
tags: [libox, glosario, referencia]
updated: 2026-06-05
---

# Glosario de términos

Referencia de los términos técnicos, de producto y regulatorios que aparecen en el [PRD](prd/), el [plan](plans/libox-plan.md) y las [decisiones](decisions/). Pensado para consultar cuando un término no se entienda. Se actualiza a medida que aparecen términos nuevos.

---

## 1. Tipos de sorteo (T1–T8)

El PRD modela 8 "tipos" de sorteo. **No son 8 motores distintos**: son **presets** de un mismo motor configurable (`draw_config`), que combinan unos pocos ejes ortogonales (condición de disparo, número de ganadores, quién ejecuta). Ver análisis en [Z.4](decisions/Z4-tipos-de-sorteo.md).

| Tipo | Nombre | Cuándo se sortea | Ganadores | Quién dispara |
|---|---|---|---|---|
| **T1** | Estándar | Cuando se vende el **100%** de los boletos | 1 | Sistema (AUTO) / Admin |
| **T2** | Threshold (umbral) | Cuando se vende un **mínimo** definido (no hace falta el 100%) | 1 | AUTO / Admin / Organizador autorizado |
| **T3** | Tiempo fijo | En una **fecha/hora** fija, se haya vendido lo que se haya vendido | 1 | AUTO / Admin |
| **T4** | Híbrido | Lo que ocurra **primero**: umbral alcanzado **o** fecha límite | 1 | AUTO / Admin |
| **T5** | Flash | Igual que T3 pero en una **ventana muy corta** (urgencia) | 1 | AUTO / Admin |
| **T6** | Multi-ganador | Una condición definida, pero se eligen **N ganadores** de un mismo pool | N | AUTO / Admin |
| **T7** | Progresivo | Se desbloquean premios por **fases / milestones** (ej. al llegar a 250, 500, 1000 boletos) | N / por fases | AUTO / Admin |
| **T8** | LIVE | El **organizador ejecuta el sorteo en vivo** (streaming), solo con autorización previa de Admin. El algoritmo es idéntico al modo AUTO | 1 o N | Organizador autorizado / Admin |

**Ejes ortogonales que componen los tipos** (clave para entender que se solapan):
- **Condición de disparo**: sold-out (T1) · umbral (T2) · fecha (T3) · umbral-o-fecha (T4) · ventana corta (T5) · milestones por fases (T7).
- **N° de ganadores**: 1 (T1–T5, T8) · N (T6, T7, T8).
- **Modo de ejecución**: AUTO (sistema) · ADMIN (manual) · LIVE (organizador en vivo, T8).

---

## 2. Motor de sorteo y fairness (imparcialidad verificable)

- **`draw_config`** — la configuración versionada que define cómo se comporta un sorteo (condición, ganadores, modo). El motor de sorteo **solo** ejecuta lo que dice el config; no tiene comportamiento implícito.
- **`canonical_pool`** — la lista de boletos válidos, ordenada de forma determinística (canónica) justo antes del sorteo. Que sea canónica garantiza que cualquiera que la reconstruya obtenga el mismo orden.
- **`pool_hash`** — huella criptográfica (SHA-256) del `canonical_pool`. Prueba qué boletos entraron al sorteo sin poder alterarlos después.
- **`external_entropy`** (entropía externa) — un valor aleatorio de una **fuente pública verificable** (ej. drand, beacon NIST, hash de un bloque futuro de blockchain) que nadie controla. Evita que Libox o el organizador "elijan" el ganador.
- **`seed_material`** — material derivado: `sha256(pool_hash + external_entropy + raffle_id)`. Mezcla el pool con la entropía externa.
- **`random_value`** — el valor final de cálculo: `sha256(seed_material + pool_hash)`. De aquí sale el ganador.
- **`winner_index`** — la posición del ganador: `random_value (como número) % cantidad_de_boletos`.
- **commit-reveal** — esquema en dos tiempos: primero se **publica** (commit) un compromiso (ej. el hash) antes de conocer el resultado, y luego se **revela** la semilla. Permite probar que nada se manipuló entre el cierre y el sorteo.
- **draw proof / `draw_proofs`** — el paquete de evidencia (pool_hash, entropía, seed, random_value, versión del algoritmo) que permite a **cualquier tercero reproducir** el sorteo y verificar el ganador.
- **`algorithm_version`** — versión del algoritmo de sorteo. Se versiona para que los sorteos viejos sigan siendo verificables aunque el algoritmo cambie.
- **Determinismo** — propiedad central: con el mismo `canonical_pool`, la misma `external_entropy` y la misma `algorithm_version`, el resultado es **siempre idéntico**. Es lo que hace el sorteo auditable.

---

## 3. Arquitectura del sistema

- **Monolito modular** — una sola aplicación desplegable, pero internamente dividida en módulos con fronteras claras. Simple de operar al inicio, sin perder orden.
- **Bounded context** (contexto delimitado) — un dominio con responsabilidad propia y fronteras explícitas (ej. Purchase, Draw, Settlement). Cada uno tiene sus eventos y reglas.
- **Event-driven** (orientado a eventos) — los módulos se comunican emitiendo **eventos** (ej. `PURCHASE_COMPLETED`) en vez de llamarse directamente. Desacopla el core de los consumidores (notificaciones, riesgo, dashboards).
- **Outbox pattern** — para publicar eventos de forma confiable: dentro de la **misma transacción** de base de datos se escribe el cambio + el evento en una tabla `outbox`; un worker los publica después. Evita perder o duplicar eventos si algo falla.
- **DLQ (Dead Letter Queue)** — cola donde van los eventos que fallaron N veces, para revisarlos sin frenar el resto.
- **Idempotencia** — propiedad de que repetir la misma operación no cause efectos duplicados. Se logra con `Idempotency-Key`. Crítico para que un doble-click o un webhook repetido no cobre/emita dos veces.
- **`trace_id`** — identificador único que acompaña una operación de punta a punta (API → DB → logs → webhooks → ledger). Permite reconstruir todo lo que pasó con una compra/sorteo sin buscar manualmente.
- **audit event append-only** — registro de auditoría al que **solo se agrega**, nunca se edita ni borra. Cada acción sensible genera uno. Es la base de la trazabilidad forense.
- **state machine** (máquina de estados) — modelo donde una entidad solo puede transitar entre estados permitidos (ej. sorteo: borrador → revisión → aprobado → activo → ejecutado). Evita estados inválidos.

---

## 4. Pagos, custodia y contabilidad

- **PSP (Payment Service Provider)** — proveedor que procesa los pagos (ej. Mercado Pago, Culqi). Ver [Z.2](decisions/Z2-eleccion-psp.md).
- **split payment / application fee** — capacidad del PSP de **dividir un pago** entre varios beneficiarios en una sola transacción (ej. 80% al organizador, 20% a Libox). Es la restricción dura que define qué PSP sirve.
- **marketplace (modelo)** — arquitectura donde una plataforma facilita pagos entre compradores y múltiples vendedores, cobrando una comisión vía split.
- **merchant of record** — el comercio que figura legalmente como vendedor ante el participante y emite el comprobante. Bajo Modelo C, es el **organizador**.
- **escrow** — figura donde un tercero custodia el dinero hasta que se cumplan condiciones, y recién entonces lo libera.
- **Modelo A / B / C** — las tres formas de custodia evaluadas en [Z.1](decisions/Z1-custodia-del-dinero.md): **A** = split directo puro (Libox no toca el dinero); **B** = escrow real (Libox custodia, requiere licencia); **C** = escrow conceptual (opera como A pero lleva contabilidad como B). **Libox usa C.**
- **payout** — el desembolso del dinero al organizador.
- **chargeback (contracargo)** — cuando un participante reclama a su banco/tarjeta y se revierte el cobro. Bajo Modelo C lo absorbe primero el PSP.
- **reconciliation (conciliación)** — cruzar lo que reporta el PSP contra el ledger interno para detectar diferencias. Gate `PSP_RECONCILED`.
- **ledger doble entrada** — contabilidad donde cada movimiento se registra en dos cuentas (debe = haber). Garantiza que las cuentas siempre cuadren.
- **settlement (liquidación)** — el proceso de cerrar las obligaciones económicas tras el sorteo y la entrega: pagar al organizador, reconocer la comisión, manejar refunds.
- **settlement gates** — condiciones obligatorias que deben cumplirse antes de liberar dinero (draw ejecutado, entrega resuelta, sin disputa, ledger cuadrado, PSP conciliado). Bajo Modelo C son **conceptuales** (registran estado, no congelan dinero real).
- **Cuentas del ledger** (PRD): *Cash Clearing* (dinero capturado pendiente de conciliar), *Purchase Liability* (obligación por boletos vendidos), *Platform Revenue* (comisión Libox), *Payment Expense* (costo PSP), *Client Payable* (neto a pagar al organizador), *Refund Reserve* (reserva de devoluciones), *Chargeback Loss* (pérdida por contracargos), *Settlement Freeze* (bloqueo por disputa).

---

## 5. Roles (RBAC)

- **RBAC (Role-Based Access Control)** — control de acceso según el rol del actor.
- **Usuario / Participante** — quien compra boletos y participa.
- **Cliente / Organizador** — quien crea el sorteo y entrega el premio. (En el PRD se llama "Cliente"; en Libox lo llamamos **organizador**.)
- **Admin** — rol soberano de Libox: aprueba, ejecuta excepciones, resuelve disputas, libera settlement. Cada acción sensible exige **motivo** (`reason_required`) y queda auditada.

---

## 6. Marco regulatorio Perú

Ver detalle en [compliance-peru.md](compliance-peru.md). Todo aquí es referencia, no asesoría legal.

- **RUC (Registro Único de Contribuyentes)** — identificador tributario. Lo tienen **tanto personas jurídicas como naturales con negocio**. Requisito para ser organizador (ver [Z.3](decisions/Z3-tipo-de-organizador.md)).
- **SUNAT** — autoridad tributaria y aduanera de Perú.
- **PSE (Proveedor de Servicios Electrónicos)** — empresa autorizada para emitir comprobantes electrónicos en nombre de un contribuyente (ej. Nubefact, Bizlinks).
- **factura / boleta** — comprobantes electrónicos. **Factura** = operación B2B (receptor con RUC). **Boleta** = consumidor final (persona natural).
- **SBS (Superintendencia de Banca, Seguros y AFP)** — regula a quienes captan fondos del público. Relevante porque el escrow real (Modelo B) caería bajo su ámbito.
- **EEDE (Empresa Emisora de Dinero Electrónico)** — entidad autorizada por la SBS para emitir dinero electrónico. Licencia con capital mínimo y requisitos fuertes.
- **UIF-Perú (Unidad de Inteligencia Financiera)** — recibe reportes de operaciones sospechosas para prevención de lavado.
- **PLAFT (Prevención de Lavado de Activos y Financiamiento del Terrorismo)** — régimen de obligaciones (oficial de cumplimiento, manual, reportes) para los "sujetos obligados".
- **sujeto obligado** — entidad que la ley obliga a cumplir PLAFT. Pregunta abierta clave: ¿un marketplace de rifas lo es?
- **autorización municipal de rifa** — permiso que (típicamente) exige la municipalidad para realizar una rifa con boleto pagado.
- **IR de 2da categoría** — impuesto a la renta que aplica (sobre cierto monto) a premios obtenidos en sorteos.
- **KYC (Know Your Customer)** — proceso de verificar la identidad de un cliente (organizador o ganador).
- **Ley 26702** — Ley General del Sistema Financiero. **Ley 29985** — Ley de Dinero Electrónico.

---

## 7. Ciclo de negocio (entidades y estados)

- **Raffle (sorteo)** — la campaña: premio, precio de boleto, total de boletos, condición de sorteo. Estados: borrador → revisión → aprobado → activo → cerrado → ejecutado → liquidado.
- **Ticket (boleto)** — unidad de participación. Tiene número único dentro del sorteo. No existe boleto válido sin pago consolidado.
- **Order (orden)** — la compra de uno o más boletos por un participante.
- **Draw (ejecución del sorteo)** — el acto de calcular el ganador, con su proof.
- **Delivery (entrega)** — el ciclo de entregar el premio al ganador: evidencia del organizador → confirmación del usuario → o disputa.
- **Dispute (disputa)** — mecanismo de protección: el participante cuestiona la entrega; congela el settlement hasta que Admin resuelve.
