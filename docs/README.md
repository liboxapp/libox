---
title: Libox — Índice del wiki
status: vigente
tags: [libox, wiki, indice, linea-base]
updated: 2026-08-30
---

# Libox — Wiki del proyecto

Marketplace de sorteos donde terceros verificados publican oportunidades. LIBOX no organiza ni pone premios: cobra comisión sobre la recaudación, idéntica gane quien gane. Mercado inicial: Perú.

## Regla de uso

> **Si un documento no figura en el §1 del Registro Maestro, no rige.**

Empieza por [`linea-base/LIBOX_REGISTRO_MAESTRO_LINEA_BASE_V6.md`](linea-base/LIBOX_REGISTRO_MAESTRO_LINEA_BASE_V6.md). Toda versión distinta a las de la línea base está derogada, aunque siga circulando.

## Mapa

| Ruta | Contenido | Cuándo abrirlo |
|---|---|---|
| [`linea-base/`](linea-base/) | **El corpus canónico** (V6): Registro Maestro · LBPF V3 (L0) · Product Strategy V3 (L1) · **PRD MVP V9** · Enterprise V3 (L2) · Especificación Técnica V7 · Matriz de Casos de Uso V1 · Guía de Extensión V1 (L3) · Design System V2 (L4) · VIES V3 · Backlog V3 · Dossier Legal · Evaluación · 2 auditorías | Fuente autoritativa de todo: producto, técnica, plan y marca |
| [`linea-base/ARTEFACTOS/`](linea-base/ARTEFACTOS/) | `libox_schema_L3_V7.sql` (135 tablas, cero errores en PG16) · `libox_openapi_L3_V7.yaml` (16/~30 rutas, incompleto — T-1) · tokens L4 V2 · Backlog xlsx | Migraciones, generación de tipos, implementación de UI |
| [`../verify_corpus.py`](../verify_corpus.py) | Verificador de coherencia, 10 controles. `python3 verify_corpus.py --dir docs/linea-base` | En cada emisión y cada PR que toque el corpus (CD-10: cero fallos) |
| [`operacion/`](operacion/) | Vacío. Destino del futuro Manual de Operación (T-3, 13 SP) | Al redactarlo en R3 |
| [`archive/`](archive/) | **Histórico nulo o superseded** — no se consulta ni se cita (Registro §2) | Solo para trazabilidad |
| [`glosario.md`](glosario.md) · [`onboarding.md`](onboarding.md) · [`flujos/`](flujos/) | Documentos de trabajo, no normativos | Consulta |

## Precedencia ante conflicto

```
L0   sobre todo
L2   sobre L4 en materia de reglas
L3   sobre L4 en materia técnica
VIES sobre L4 en identidad de marca
```

## Versionado del corpus

V1 → V2 → V3, sin subversiones. Toda emisión: `verify_corpus.py` con cero fallos (CD-10) + alta en `BASELINE` y en Registro §1 + clasificación (CD-11), en el mismo acto. **La línea base está congelada** — hallazgos al backlog de cambio (CD-07); solo rompe el congelamiento lo que impida construir o exponga a riesgo legal/patrimonial.

## Espejo en Outline

La colección **Libox — Negocio** (liboxapp.getoutline.com) contiene el espejo navegable del corpus ("LIBOX — Línea Base documental"), la capa operativa de negocio (00–21) y el registro vivo de asunciones y cambios (doc 20: ASS-\*/CHANGE-\*). **Para el corpus, la fuente canónica es este repo**; se edita aquí vía PR y se republica el espejo.

## Pendientes críticos (ninguno documental)

1. **Dictamen legal L-01** — el Dossier está listo; falta encargarlo. Bloquea operar.
2. **F0: veinte conversaciones con organizadores** — cero a la fecha. Valida la hipótesis central.
3. `openapi.yaml` completo (~14 rutas, 8 SP) — bloquea sprint 4.
4. Diseño de 41/62 superficies — bloquea frontend.
5. Arte maestro de marca (VIES Anexo A).
6. Manual de operación (13 SP).
7. **ASS-001** (custodia) y **ASS-002** (stack) — ratificación de socios pendiente; ver doc 20 en Outline.
