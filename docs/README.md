---
title: Libox — Índice del wiki
status: vivo
tags: [libox, indice, wiki]
updated: 2026-06-21
---

# Libox — Wiki del proyecto

Marketplace web de rifas digitales con boleto pagado, operado bajo regulación peruana. Estado actual: **pre-código** — sin aplicación todavía, pero ya con repositorio git y tooling de versionado (SemVer, Conventional Commits, release-please, CI). El contenido es un **wiki de documentación** que captura decisiones de producto, arquitectura, stack y análisis regulatorio antes de la primera línea de código.

## Mapa

| Carpeta / archivo | Contenido | Cuándo abrirlo |
|---|---|---|
| [`prd/`](prd/) | PRD Libox v11 del socio (48 páginas, PDF) | Fuente autoritativa de producto y arquitectura técnica. Léelo cuando necesites el "blueprint" completo: roles RBAC, modelo económico, Purchase/Draw/Delivery/Settlement engines, ledger bank-grade, auditoría, APIs, threat model, SLOs. |
| [`plans/libox-plan.md`](plans/libox-plan.md) | Plan inicial de producto, arquitectura, stack y roadmap. Incluye el **Anexo Z — Bitácora de decisiones cerradas**. | Léelo para el camino completo del MVP, dominios del sistema, decisiones pendientes, próximos pasos. |
| [`decisions/`](decisions/) | ADRs autocontenidos — uno por decisión cerrada. Versión canónica para compartir con socios e inversionistas. | Léelo cuando quieras compartir o consultar una decisión específica sin todo el contexto del plan. |
| [`compliance-peru.md`](compliance-peru.md) | Documento de trabajo sobre el marco regulatorio peruano (SUNAT, autorización municipal, retención de impuestos, KYC, PLAFT, T&C). | Léelo antes de cualquier conversación con el abogado, y para entender por qué el PRD por sí solo no cubre todo. |
| [`glosario.md`](glosario.md) | Glosario de términos técnicos, de producto y regulatorios (T1–T8, fairness del sorteo, arquitectura, pagos, compliance). | Consúltalo cuando un término no se entienda. |

## Cómo se relacionan los documentos

```
                    PRD Libox v11 (socio)
                  blueprint técnico, agnóstico geográfico
                              ↓
                         Plan Libox
                  hoja de ruta MVP + decisiones técnicas
                              │
              ┌───────────────┼───────────────┐
              ↓               ↓               ↓
        Anexo Z       compliance-peru   stack/roadmap
        (decisiones)  (vive aparte      (Next.js, PG,
                       del PRD)          PSP, etc.)
              │
              └→ decisions/<código>.md
                 (versión canónica compartible)
```

## Decisiones cerradas

El índice canónico de decisiones vive en **[decisions/README.md](decisions/README.md)** — ahí está la tabla completa y la convención para agregar nuevas. **Z.1–Z.8 cerradas** (custodia del dinero, PSP, tipo de organizador, motor de sorteo, T8 LIVE, stack, versionamiento, roles de memoria/contexto). La próxima es Z.9.

## Obsidian

Este wiki está pensado para abrirse como **vault de Obsidian** (abre la carpeta raíz del proyecto en Obsidian). El graph view y los backlinks te dan navegación visual entre documentos. La config compartida (`.obsidian/app.json`) **fuerza links en markdown estándar** (`[texto](ruta.md)`), no wikilinks `[[...]]`, para que los documentos sigan funcionando en GitHub y cualquier viewer cuando los compartas con socios o el abogado. El estado por-máquina de Obsidian está en `.gitignore`.

## Convenciones

- **Idioma**: español (mercado peruano).
- **Frontmatter**: cada documento lleva `title`, `status`, `tags` y `updated` en YAML para filtrar y buscar dentro de Obsidian.
- **Términos legales**: marcados `[LEGAL→ABOGADO]` cuando son lectura del autor sobre normativa pública y requieren ratificación.
- **Vínculos**: relativos al root de `docs/` para que el wiki funcione tanto en el editor como en cualquier renderer Markdown.
- **Decisiones**: cuando una se cierra, se documenta primero como entrada **Z.N** en el plan, y simultáneamente como ADR autocontenido en `decisions/`. La canonicidad la indica el propio ADR.

## Pendientes activos

- Los 4 conflictos originales PRD vs plan están **cerrados** (Z.1–Z.5), más Z.6–Z.8. Sigue Z.9.
- Validaciones externas pendientes: llamada comercial a Mercado Pago (split/Yape, Z.2) y ratificación legal `[LEGAL→ABOGADO]` (custodia Z.1, autorización municipal Z.3).
- Recortar el plan a un MVP-1 ejecutable en 8-12 semanas con 1 dev.
- Convertir [`compliance-peru.md`](compliance-peru.md) de stub a documento cerrado con apoyo del abogado.
- Wireframes de los 5 flujos críticos.
