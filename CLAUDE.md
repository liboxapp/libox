# CLAUDE.md

Guía para Claude Code en este repositorio. Es un puntero: la verdad vive en `docs/`.

## Qué es este repo

**Libox** es un marketplace web de sorteos digitales con boleto pagado, bajo regulación
peruana. El repo contiene (1) el **corpus canónico** en `docs/linea-base/`, gobernado por el
Registro Maestro V6 (si un documento no figura en su §1, no rige) y verificado por
`verify_corpus.py` (CD-10: cero fallos), y (2) un scaffold Next.js en `src/` que está
**congelado** hasta completar L3 V8 y la transición de D1. El backend TypeScript
ya fue ratificado el 2026-09-29; ver el
[programa de R0](docs/superpowers/specs/2026-09-25-habilitar-r0-design.md).

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
  `CONTRIBUTING.md` → "Autoría: sin co-autores automáticos". El CI `commit-policy` lo comprueba; los hooks locales tienen límites.
- **Línea base congelada** (CD-07): los docs de `docs/linea-base/` no se editan in-place;
  se emite versión nueva con `/libox-versionar-doc` o el hallazgo va a
  `/libox-registrar-hallazgo`. Ver `.claude/rules/linea-base.md`.
- **`src/` congelado** hasta D1: no crear ni extender código. El texto antiguo de
  `.claude/rules/src-congelado.md` no reabre la decisión de TypeScript; su bloqueo
  sigue activo y el CI consulta la regla de la rama base.
- **Zonas sin generación asistida:** aplicar `.claude/rules/zonas-sin-ia.md`.
  La revisión humana obligatoria está suspendida hasta reactivación explícita
  de Diego: `.claude/rules/revision-humana.md`. Mantener CI y revisión automatizada.
- **Claims legales** marcados `[LEGAL→ABOGADO]` hasta ratificación del abogado.
- **Git:** rama por cambio, Conventional Commits en español, correo `@liboxapp.com`, PR con
  `/libox-pr`, `main` protegido. Ver `.claude/rules/git.md` y `CONTRIBUTING.md`.

## Orquestación

Si el modelo de la sesión es Fable: **orquesta** — delega el trabajo sustancial en los
agentes del repo (`redactor-docs`, `auditor-corpus`, `revisor-pr`, todos en Opus) o en
`general-purpose` con `model: "opus"`, con brief autocontenido, y **verifica** antes de dar
algo por hecho. Detalle en `docs/equipo/sistema-operativo-ia.md#orquestación-fable-orquesta-opus-ejecuta`.

## Decisiones abiertas

**ASS-001** (custodia del dinero) sigue abierta. **ASS-002** ya tiene ratificación
a TypeScript, registrada en el programa de R0 a partir del doc 20 de Outline
(revisión 23). Falta trasladarla al canon L3 V8 y completar D1. Supabase Pro, Trigger.dev y Vercel Pro fueron confirmados el 2026-09-30;
PostgreSQL 17 queda sujeto a validar migraciones. Ver la
[decisión C1](docs/superpowers/specs/2026-09-30-r0-c1-design.md).
Drizzle y las demás herramientas no quedan ratificadas por esta elección.
La línea de ADRs Z.1–Z.8 es histórica (`docs/archive/decisions/`).

## Configuración compartida

`.claude/settings.json`, `.claude/rules/`, `.claude/skills/`, `.claude/agents/`,
`scripts/hooks/` y las reglas hookify están **versionados**: todo el equipo hereda el mismo
entorno al clonar. `.claude/settings.local.json` es personal y nunca se commitea. La
auto-memory es personal por máquina: lo valioso se promueve a `docs/` por PR.

## Auditoría compartida activa

`/libox-system-design-audit` inicia el audit del harness; procedimiento en
[el manual](docs/equipo/ai-audit-harness.md). Para esta tarea se usan
`libox-audit-fable` y `libox-audit-opus` con sus modelos explícitos, como excepción
a la delegación genérica anterior. Codex aporta una revisión independiente.
