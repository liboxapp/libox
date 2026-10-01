---
title: C1 — plantilla de documentos P-C y seguimiento
status: borrador
tags: [r0, c1, pc, seguimiento]
updated: 2026-10-01
description: Plantilla para que Diego y el abogado concreten la lista cerrada por etapa P-C, sin inventar claves ni emitir aprobación legal.
---

# Documentos P-C: plantilla y seguimiento

**Responsable de coordinación:** Diego. **Validación:** [LEGAL→ABOGADO].
**Fecha objetivo:** por acordar. **Estado:** pendiente de lista aprobada.
Revisar en cada avance de C1 y antes de habilitar P-C en el MVP, según
[A8](decisiones-c1-transiciones.md#a8-lista-cerrada-de-documentos-por-etapa-p-c-i-08).
No se ha contactado al abogado ni creado un recordatorio automático.

## Referencias para preparar la lista

La tabla resume entradas ya mencionadas en
[PRD MVP V9 §8](../../../linea-base/LIBOX_PRD_BLUEPRINT_MVP_V9.md).
Son referencias de producto que el abogado debe revisar; no sustituyen su lista,
no generan `checklist_key` y no son una semilla ejecutable. [LEGAL→ABOGADO]

| Etapa | Entradas del PRD para revisar |
|---|---|
| E1 Elegibilidad | Capacidad, KYB vigente, reputación y ausencia de disputas |
| E2 Titularidad | Copia literal, certificados de no adeudo, verificación física y declaración de estado civil |
| E3 Valoración | Tasación según categoría y referencias de mercado |
| E4 Instrumento y bloqueo | Instrumento notarial, constancia de bloqueo y vigencia de poderes cuando corresponda |
| E5 Publicación y venta | Divulgación y reconsulta registral; distinguir evidencia automática de documento aportado |
| E6 Preparación del ganador | Identidad, estado civil, capacidad legal, datos del acto y aceptación de cargas/costos |
| E7 Transferencia | Acto, tributos/derechos, presentación e inscripción, aceptación del organizador, confirmación del ganador y atestación |

## Ficha por documento o evidencia

Completar una ficha por elemento validado; no usar «otros» como categoría abierta.

| Campo | Valor por completar |
|---|---|
| Mercado y categoría | PE; precisar P-C1/P-C2 |
| Etapa | E1–E7 |
| Clave estable (`checklist_key`) | Pendiente de lista aprobada |
| Descripción y finalidad | Pendiente |
| Obligatorio y condición de aplicabilidad | Pendiente |
| Emisor/fuente y responsable de aportar | Pendiente |
| Verificación externa y evidencia resultante | Pendiente |
| Vigencia, caducidad y renovación | Pendiente |
| Datos personales y acceso permitido | Pendiente |
| Retención y disposición | Pendiente [LEGAL→ABOGADO] |
| Versión, aprobador y fecha | Pendiente |

## Criterio de cierre

Diego recibe la lista validada, con claves únicas y condiciones por etapa/categoría.
Después se integra en el contrato y la semilla correspondiente, se comprueba que
las decisiones de etapa referencian la misma versión y se prueba rechazo de claves
ajenas. Una plantilla rellenada sin aprobación no habilita P-C. Las firmas,
transiciones y controles críticos mantienen su implementación humana.

## Registro de seguimiento

| Revisión | Resultado | Próxima acción |
|---|---|---|
| 2026-10-01 | Plantilla preparada; lista no recibida | Diego acuerda fecha y solicita validación al abogado |
