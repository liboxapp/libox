---
title: C1 — decisión de Diego del 27 de octubre
status: aprobado
tags: [r0, c1, decisiones, viabilidad, garantia]
updated: 2026-10-27
description: La garantía del sorteo (opción B del 04/10) queda sustituida por la regla del 05/10 de rev6; bajo el mínimo el sorteo se cancela y reembolsa.
---

# Decisión del 27 de octubre de 2026

Origen: respuesta de Diego del 2026-10-27, al conciliar la contradicción C-2
entre las [decisiones del 04/10](decisiones-2026-10-04.md) y el paquete rev6:
«si es posterior a la mía entonces esa es la que se decidirá».

## Qué se decide

La **garantía del sorteo (opción B, 04/10) queda sustituida** por la regla
posterior del 2026-10-05, recogida en rev6 (Respuestas al Cuestionario V2 §0.1,
PRD V22 BR-09, INV-47, INV-48, §5.8.1 y §16.7):

> Si el sorteo no llega al mínimo o a sus hitos, se cancela y se devuelve a
> todos. Si el organizador no entrega el premio, LIBOX usa el dinero para
> comprar ese activo y entregarlo. El desembolso al organizador y a LIBOX se
> ejecuta después de liquidar la entrega.

Bajo el mínimo no hay cobertura de brecha: el sorteo se cancela y reembolsa.
El MVP no tiene depósito, custodia ni transacciones de garantía.

## Por qué prevalece

Es la decisión posterior y la que rev6 ya construye en contrato, especificación
y esquema. Sus motivos, verificados en rev6: incumplir costaba menos que
cumplir; el gate aceptaba cualquier fila de garantía; la custodia exigida no
existe (ASS-001); y el instrumento atraía a quien no puede vender su bien.

## Qué cambia y qué no

- Se retiran los pendientes de la opción B: plazo, aportante, fórmula,
  custodia, devolución y ejecución de la garantía. No entran en la emisión.
- El [análisis de escenarios](escenarios-t1-garantia.md) se conserva como
  antecedente.
- Reabrir una garantía requiere una decisión nueva, con custodia legal resuelta
  y un diseño que corrija los defectos anteriores. [LEGAL→ABOGADO]
- No cambia el mínimo ni el suelo de 1,45×: siguen en discusión con Adrián
  (contradicción C-1).
