---
title: C1 — escenarios para decidir la garantía de T1
status: borrador
tags: [c1, t1, garantia, escenarios, viabilidad]
updated: 2026-10-04
description: Comparación didáctica de cancelación y cobertura con mínimo 1,45, separando ventas, garantía, comisión y entrega del premio.
---

# Escenarios para decidir la garantía

Diego pidió escenarios antes de ratificar el punto 5. El múltiplo 1,45 se registra
en las [decisiones del 04/10](decisiones-2026-10-04.md). La regla actual de
[C1](decisiones-c1-configuracion.md) cancela y reembolsa bajo el mínimo; la garantía
de Cowork sigue siendo una alternativa por decidir. [LEGAL→ABOGADO]

## Supuestos del ejemplo

Diego corrigió el término a **garantía**, el 2026-10-04. Estos escenarios
ilustran una garantía en dinero aportada por el organizador. La forma concreta
y las condiciones de esa garantía siguen por definir; el ejemplo no las ratifica.

- Premio con valor aprobado de **S/1.000**.
- Mínimo ilustrado: **S/1.450** (1,45 × S/1.000).
- Ticket de S/10: hacen falta 145 tickets pagados válidos para ese mínimo.
- Comisión ilustrativa: tasa base documentada del 20 %, sin aplicar descuentos
  de la escala. Impuestos, coste PSP, entrega y retenciones no se cuantifican.
- La brecha se ilustra contra el mínimo bruto; el importe final de garantía debe
  derivarse de la fórmula de caja/obligación aprobada, no de esta resta por sí sola.
- La ventana de cobertura no está decidida. Las 48 h son propuesta de origen.

## Resultado con y sin garantía

| Escenario al vencer | Regla actual sin garantía | Alternativa si se ratifica garantía |
|---|---|---|
| Ventas S/1.700, mínimo alcanzado | Continúa el sorteo si cumple las demás condiciones; comisión bruta ilustrativa S/340 | Igual; no necesita cobertura de brecha |
| Ventas S/1.200, organizador no aporta | Cancela y devuelve S/1.200 a los compradores | Puede ofrecer la ventana aprobada; al vencer sin cobertura válida, cancela y devuelve |
| Ventas S/1.200, el organizador promete S/250 pero no hay fondos confirmados | Cancela y reembolsa | La promesa no habilita el sorteo; requiere fondos acreditados y suficientes antes del deadline |
| Ventas S/1.200, depósito confirmado y cobertura suficiente | La política actual cancela; el depósito no cambia las bases | Puede continuar solo si identidad, moneda, custodia, saldo, disponibilidad y fórmula aprobada acreditan cobertura |

Las otras guardas siguen vigentes: elegibles suficientes, reglas del tipo,
premio completo, condiciones fijadas antes de comprar y ninguna transición
concurrente que invalide los fondos. Cumplir un mínimo no ejecuta automáticamente
el sorteo.

## Qué ocurre después de continuar con cobertura

1. **El organizador entrega el premio.** Se comprueba entrega/atestación y cierre.
   La garantía devuelve al destinatario debido por el procedimiento aprobado, una
   vez. No es ingreso de Libox ni una compra de tickets.
2. **El organizador incumple.** Los fondos se aplican al destino autorizado para
   entregar el premio. Hay que definir beneficiario, adquisición/entrega, gastos
   y sobrante. Una garantía de brecha no demuestra que pueda comprarse el bien entero.
3. **Otra causa obliga a cancelar.** Compradores y depósito tienen rutas de
   devolución explícitas; no se deja el depósito retenido sin destino.
4. **El pago del depósito llega tarde o duplicado.** No reabre un sorteo cancelado
   ni genera dos efectos. Hace falta una política de excepción/devolución.

El ejemplo S/250 solo ilustra la brecha S/1.450 − S/1.200. No garantiza entrega
de un premio de S/1.000 por sí solo. La cobertura debe considerar fondos retenidos,
costes, obligaciones y capacidad real de obtener/transferir el bien. ASS-001 sigue
abierto y la validación contable/legal no está recibida. [LEGAL→ABOGADO]

## Efecto sobre la comisión

Con ventas de S/1.200 y tasa base del 20 %, la comisión bruta ilustrativa de un
flujo que llegue a liquidar es S/240. El depósito no la eleva a S/290:
**S/1.200 vendidos y S/250 de garantía no son S/1.450 vendidos**.
La base/techo y escala están en
[PRD MVP §1.3](../../../linea-base/LIBOX_PRD_BLUEPRINT_MVP_V9.md).

En cancelación no se cobra la comisión de Libox. El coste de cobro PSP ya
devengado lo absorbe Libox conforme al PRD; importe y condiciones deben validarse
con Mercado Pago. No se da una tarifa hipotética por vigente.

## Opciones para ratificar

| Opción | Ventaja | Coste o condición |
|---|---|---|
| A. Mantener cancelación/reembolso bajo mínimo | Regla simple y consistente con C1; conserva el requisito de ventas efectivas | Se cancelan ventas parciales que podrían tener respaldo adicional |
| B. Permitir garantía desde la primera entrega | Puede conservar una venta parcial si hay respaldo acreditado y bases compatibles | Diseñar, implementar y probar depósito, custodia, devolución, ejecución, cancelación y carreras antes de habilitar |
| C. Mantener A en la primera entrega y preparar B como ampliación | Permite avanzar con la política actual sin descartar la garantía | Definir alcance/dependencias del backlog y una puerta de habilitación para el ciclo completo |

**Recomendación para Diego: C.** La cobertura tiene valor, pero requiere un ciclo
financiero adicional y no asegura la comisión mínima buscada con el múltiplo.
Esta recomendación no se adoptó: Diego eligió **B** el 04/10.

## Cierre de la decisión

**Decidido: B** (Diego, 2026-10-04), con el nombre **garantía del sorteo**. Falta
fijar ventana, aportante, fórmula de cobertura, custodia, devolución, ejecución,
cancelación y comunicación previa al comprador. No se declara operativo un
depósito cuyo ciclo completo no esté implementado y probado; ASS-001 bloquea su
uso con dinero real. Ver el [registro](decisiones-2026-10-04.md).
Controles de dinero/concurrencia y sus efectos son implementación humana.
Ver [aceptación de garantía](reconciliacion-aceptacion.md) y
[dependencias del backlog](reconciliacion-decisiones-planificacion.md).
