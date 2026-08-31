---
paths:
  - "docs/**"
---

# Documentación (`docs/`)

Referencia completa: `docs/equipo/estilo-documentacion.md`. Reglas mínimas:

- **Español.** Prosa directa, sin relleno; negritas y listas solo cuando aportan.
- **Frontmatter obligatorio** en todo `.md` de `docs/` (salvo `docs/linea-base/`):
  `title`, `status` (`vigente | borrador | obsoleto | aprobado`), `tags`, `updated`
  (`YYYY-MM-DD`), `description` (una línea para decidir si abrirlo).
- **Links markdown estándar** `[texto](ruta.md)`, relativos al archivo; nunca
  wikilinks `[[...]]`. El CI (`lychee --offline`) rompe si un link relativo no resuelve.
- **~150 líneas** por documento; si crece, partir en notas enlazadas.
- **`docs/archive/` es histórico**: no se cita como fuente vigente.
- **Claims legales** marcados `[LEGAL→ABOGADO]` hasta ratificación del abogado.
- **Decisiones**: ya no se abren ADRs Z nuevos; los hallazgos van al backlog de
  cambio o al doc 20 de Outline y se vuelven normativos solo con una versión nueva
  del documento del canon (ver `.claude/rules/linea-base.md`).
- `CLAUDE.md` y `MEMORY.md` se mantienen magros: reglas y punteros, el contenido va en `docs/`.
