---
title: Estilo de documentación — Libox
status: vigente
tags: [estilo, documentacion, convenciones]
updated: 2026-08-30
description: Cómo escribimos la documentación del proyecto. Idioma, frontmatter, links, longitud, tono y cómo se registran las decisiones.
---

# Estilo de documentación — Libox

Reglas de *cómo* se escribe. Complementan el
[sistema operativo de IA](sistema-operativo-ia.md) y aplican a todo documento del proyecto.
La rule `.claude/rules/docs.md` es su versión condensada para Claude.

## Idioma

- **Documentación y conversación con el equipo: español** (mercado peruano).
- **Código, identificadores y nombres de archivo: inglés.** Commits: Conventional Commits
  con asunto y cuerpo en español.

## Frontmatter

Todo doc del wiki (salvo el corpus congelado de `docs/linea-base/`) lleva YAML al inicio:

```yaml
---
title: <título legible>
status: <vigente | borrador | obsoleto | aprobado>
tags: [<...>]
updated: <YYYY-MM-DD>
description: <una línea para decidir si vale la pena abrirlo>
---
```

## Links

- **Markdown estándar** `[texto](ruta.md)`, nunca wikilinks `[[...]]` (reservados a los
  archivos de memoria privada).
- Rutas **relativas al archivo** que las contiene; el CI (`lychee --offline`) falla si un
  link relativo no resuelve.

## Longitud y estructura

- Notas atómicas y enlazadas. Cuando un doc pasa de **~150 líneas**, partirlo.
- `CLAUDE.md` y `MEMORY.md` se mantienen magros: se cargan cada sesión. El contenido va en
  `docs/`; esos archivos solo llevan reglas y punteros.

## Tono

- Prosa clara y directa. Si una palabra se puede quitar sin perder sentido, se quita.
- Negritas, encabezados y listas solo cuando aportan claridad.
- Claims legales marcados `[LEGAL→ABOGADO]`; nunca presentarlos como asesoría cerrada.

## Decisiones

La línea de ADRs Z.1–Z.8 es **histórica** (`docs/archive/decisions/`). Las decisiones
nuevas siguen el control del corpus: hallazgo → `libox-registrar-hallazgo` (ASS-/CHANGE-/
RISK- en el doc 20 de Outline) → si se aprueba, nueva versión del documento del canon con
`libox-versionar-doc`. No se abren ADRs Z nuevos.
