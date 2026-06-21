---
title: Z.3 — Tipo de organizador
status: cerrada
tags: [libox, decision, organizador, kyc, ruc, compliance]
decided: 2026-06-05
relates: [docs/decisions/Z1-custodia-del-dinero.md, docs/decisions/Z2-eleccion-psp.md, docs/compliance-peru.md, docs/plans/libox-plan.md]
updated: 2026-06-05
---

# Z.3 — Tipo de organizador

**Estado**: Cerrada (2026-06-05). Una validación legal pendiente (autorización municipal para personas naturales) que ajusta el borde, no la dirección.
**Decisor**: Diego (con conformidad pendiente de socios).
**Documento canónico**: este archivo. Mirror corto en [`docs/plans/libox-plan.md`](../plans/libox-plan.md#z3--tipo-de-organizador-cerrada-el-2026-06-05) (Anexo Z.3).

> ⚠️ Puntos marcados `[LEGAL→ABOGADO]`: lectura del autor sobre normativa pública peruana, **no asesoría legal**; ratificar con el abogado.

---

## Decisión

Organizador en MVP = **cualquier persona, natural o jurídica, con RUC activo** (Opción 2). Esto incluye empresas, ONGs e instituciones, **y también** personas naturales con negocio / RUC activo (creadores, freelancers, pequeños comerciantes formalizados).

Se **descarta para el MVP** la persona natural solo con DNI, sin RUC (Opción 3).

---

## Por qué no era una contradicción, sino un corte a elegir

A diferencia de Z.1 y Z.2, aquí **el PRD es agnóstico**: habla de "Cliente" genérico, sin distinguir persona natural de jurídica. El plan sí había elegido un corte ("solo personas jurídicas (RUC)"). El trabajo no fue resolver una oposición, sino **elegir el corte correcto** sobre un espectro y justificarlo.

---

## La imprecisión que se corrigió: "solo RUC" ≠ "solo personas jurídicas"

El plan original colapsó dos cosas distintas. En Perú **el RUC lo tienen también las personas naturales** (persona natural con negocio, profesional independiente, pequeño comerciante). "Tener RUC" es un conjunto **más amplio** que "ser persona jurídica". Esto abre tres opciones reales:

| Opción | Quién puede ser organizador | Mercado | Superficie regulatoria |
|---|---|---|---|
| 1. Solo personas jurídicas | Empresas, ONGs, instituciones con RUC | Más chico | Mínima |
| **2. Cualquiera con RUC** (elegida) | Opción 1 + personas naturales con RUC activo | Medio | Baja-media |
| 3. Cualquier persona natural (DNI) | Cualquiera, sin exigir RUC | Más grande | Alta |

---

## Restricciones que acotan el espectro

- **A. Recibir el split en MP** ([Z.2](Z2-eleccion-psp.md)): naturales y jurídicas pueden ser sellers en MP. *Poco restrictiva.*
- **B. RUC para facturar la comisión — ancla dura**: Libox cobra su 20% como **servicio B2B** al organizador; facturarlo exige que el organizador tenga RUC. Esto es independiente del tratamiento fiscal del boleto en sí, así que es un ancla limpia: **el organizador necesita RUC sí o sí**.
- **C. Autorización municipal de la rifa** `[LEGAL→ABOGADO]`: ¿una persona natural puede obtener licencia municipal de rifa, o solo entidades formales? Abierto, varía por municipalidad. Puede ajustar el borde de la Opción 2.
- **D. Riesgo PLAFT/fraude**: las personas naturales son más difíciles de perseguir y más expuestas a multi-accounting; argumenta hacia formalidad.

---

## Por qué se descartó la Opción 3

La restricción **B** descarta en la práctica a la persona solo-DNI: sin RUC no se le puede facturar la comisión, y no podría emitir comprobante al participante si resultara obligatorio. Sumado a **D**, es demasiada exposición para un MVP. Queda fuera **por restricción, no por visión**. (Reentra como opción futura si se migra a escrow real y se construye soporte de retención/identidad reforzada.)

---

## Por qué Opción 2 sobre Opción 1

Inputs de Diego (2026-06-05):

- **Organizador objetivo**: además de empresas, **individuos formalizados con RUC** (creadores, freelancers, comerciantes).
- **Postura MVP**: **máximo alcance legal**, no máxima cautela.

La Opción 2 es solo **marginalmente más riesgosa** que la 1 (sigue exigiendo RUC → identidad fiscal + facturación + trazabilidad), pero abre un mercado **bastante mayor**. El costo técnico es una segunda plantilla de KYC. Dado que el target explícitamente incluye individuos formalizados, restringir a jurídicas dejaría fuera parte del mercado objetivo sin ganar protección proporcional.

---

## Implicaciones de build

1. **`Organization.tipo`** (`juridica` | `natural_con_ruc`) — modelar el tipo, **no hardcodear** la restricción. Pasar a Opción 3 en el futuro (con escrow real) debe ser configuración, no refactor. Mismo principio que el adaptador multi-PSP de [Z.2](Z2-eleccion-psp.md).
2. **Dos plantillas de KYC**:
   - *Jurídica*: RUC + razón social + representante legal (DNI) + vigencia de poderes.
   - *Natural con RUC*: RUC + DNI del titular.
   - Ambas: validación de RUC activo/habido contra el padrón SUNAT.
3. El **comprobante al participante** lo emite el organizador (merchant of record bajo Modelo C); por eso necesita RUC. El tratamiento fiscal exacto del boleto queda como pregunta para el abogado (no bloquea la dirección).

---

## Validaciones externas pendientes

1. `[LEGAL→ABOGADO]` ¿Una **persona natural con RUC** puede obtener autorización municipal de rifa en las jurisdicciones objetivo? Si en alguna no puede, la Opción 2 se restringe a jurídicas **solo en esa jurisdicción**, no globalmente.
2. `[LEGAL→ABOGADO]` Tratamiento fiscal del boleto de rifa (¿venta afecta a IGV? ¿comprobante obligatorio? ¿categoría especial?) — afecta qué comprobante emite el organizador, no quién puede serlo.
3. `[LEGAL→ABOGADO]` ¿La inclusión de personas naturales con RUC cambia el análisis de sujeto obligado PLAFT respecto al de solo jurídicas?

---

## Preguntas para discutir con socios

1. ¿Confirmamos que el target incluye individuos formalizados, o en la práctica el go-to-market inicial será solo empresas (aunque el sistema permita ambos)?
2. Si el abogado dice que en alguna municipalidad las personas naturales no pueden organizar rifas, ¿restringimos por jurisdicción o esperamos a tener cobertura legal nacional?
3. ¿El onboarding diferenciado (dos plantillas de KYC) lo construimos desde MVP-1 o arrancamos solo con jurídicas y sumamos naturales en una fase siguiente, aunque el modelo de datos ya lo soporte?
