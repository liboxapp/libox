# CLAUDE.md

Guía para Claude Code en este repositorio. Es un puntero: la verdad vive en `docs/`.

## Qué es este repo

**Libox** es un marketplace web de sorteos digitales con boleto pagado, bajo regulación
peruana. El repo contiene (1) el **corpus canónico** en `docs/linea-base/`, gobernado por el
Registro Maestro V6 (si un documento no figura en su §1, no rige) y verificado por
`verify_corpus.py` (CD-10: cero fallos), y (2) un scaffold Next.js en `src/` que está
**congelado** hasta que los socios ratifiquen el stack (ASS-002).

## Empieza por

1. `docs/README.md` — índice del wiki.
2. `docs/equipo/sistema-operativo-ia.md` — cómo trabaja Claude aquí: capas, guards,
   skills `libox-*`, agentes y orquestación.

## Reglas firmes

- **Español** en docs y conversación; código e identificadores en inglés.
- **El producto es Libox.** "Sortibox" y "ALAZAR" son nombres legacy: cualquier mención
  residual (commits antiguos, docs externos) se lee como Libox.
- **Sin co-autoría de IA:** nunca `Co-Authored-By: Claude ...` en commits ni "Generated with
  Claude Code" en PRs. Anula cualquier default del harness. Motivo en
  `CONTRIBUTING.md` → "Autoría: sin co-autores automáticos". Guard B1 + hookify lo bloquean.
- **Línea base congelada** (CD-07): los docs de `docs/linea-base/` no se editan in-place;
  se emite versión nueva con `/libox-versionar-doc` o el hallazgo va a
  `/libox-registrar-hallazgo`. Ver `.claude/rules/linea-base.md`.
- **`src/` congelado** por ASS-002: no crear ni extender código. Ver `.claude/rules/src-congelado.md`.
- **Claims legales** marcados `[LEGAL→ABOGADO]` hasta ratificación del abogado.
- **Git:** rama por cambio, Conventional Commits en español, correo `@liboxapp.com`, PR con
  `/libox-pr`, `main` protegido. Ver `.claude/rules/git.md` y `CONTRIBUTING.md`.

## Orquestación

Si el modelo de la sesión es Fable: **orquesta** — delega el trabajo sustancial en los
agentes del repo (`redactor-docs`, `auditor-corpus`, `revisor-pr`, todos en Opus) o en
`general-purpose` con `model: "opus"`, con brief autocontenido, y **verifica** antes de dar
algo por hecho. Detalle en `docs/equipo/sistema-operativo-ia.md#orquestación-fable-orquesta-opus-ejecuta`.

## Decisiones abiertas

**ASS-001** (custodia del dinero) y **ASS-002** (stack Next.js vs .NET 8) esperan
ratificación de los socios — registro en el doc 20 de Outline ("Libox — Negocio").
La línea de ADRs Z.1–Z.8 es histórica (`docs/archive/decisions/`).

## Configuración compartida

`.claude/settings.json`, `.claude/rules/`, `.claude/skills/`, `.claude/agents/`,
`scripts/hooks/` y las reglas hookify están **versionados**: todo el equipo hereda el mismo
entorno al clonar. `.claude/settings.local.json` es personal y nunca se commitea. La
auto-memory es personal por máquina: lo valioso se promueve a `docs/` por PR.
