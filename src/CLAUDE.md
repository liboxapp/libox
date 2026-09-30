# CLAUDE.md — Application code rules

> **Freeze activo hasta D1.** TypeScript ya fue ratificado el 2026-09-29.
> Faltan L3 V8 y la transición revisada del freeze; no crear ni extender código.
> El estado vigente está en el [programa de R0](../docs/superpowers/specs/2026-09-25-habilitar-r0-design.md).
> La regla antigua conserva el bloqueo, aunque su texto aún diga ASS-002 abierto.

La aplicación será un monolito modular TypeScript con Next.js App Router y
PostgreSQL; endpoints delgados que invocan módulos de dominio.

The root [CLAUDE.md](../CLAUDE.md) is the wiki/operations guide and wins on
naming (**Libox**), conversation language (Spanish), and the no-AI-co-author
rule. Normative engineering and git rules live in
[CONTRIBUTING.md](../CONTRIBUTING.md); this file summarizes and points — it
never forks them.

Folder-specific rules live in nested CLAUDE.md files, loaded on demand:
[workflows/](workflows/CLAUDE.md) (WAT SOPs), [tools/](tools/CLAUDE.md)
(deterministic scripts + self-improvement loop), [tests/](tests/CLAUDE.md)
(TDD rules).

## Commands

Run from the repo root (`package.json` lives there; app code in `src/`):

- `npm run dev` — dev server at `http://localhost:3000`
- `npm run build` — production build
- `npm run start` — production server after a build
- `npm run lint` — ESLint over the repo
- `npm run typecheck` — `tsc --noEmit`
- `npm test` — Vitest suite (single run)
- `npm test -- src/tests/unit/raffle.test.ts` — a single test file
- `npm run test:watch` — Vitest in watch mode
- On a clean clone, run `npm run build` once before `npm run typecheck` —
  Next 16 generates route types (`LayoutProps`) during build; without them
  typecheck fails with `TS2304`.
- `AGENTS.md` at the repo root hosts the Next-managed `nextjs-agent-rules`
  block: `next dev` upserts it there (never into CLAUDE.md); it will
  legitimately change when Next is upgraded — commit that diff with the
  upgrade PR.

## Language policy

- **Code is in English**: identifiers, comments, file and directory names,
  workflows and tools.
- **Everything user-facing is in Spanish (Peru)**: titles, meta tags,
  headings, buttons, labels, body copy, placeholders, error messages,
  transactional emails, alt text. Never mix languages in the UI; if unsure
  whether a string is user-facing, it probably is — write it in Spanish.
- **Conversation, wiki docs, and commit messages are in Spanish** (root rule).

## Development workflow — Superpowers SDD

All app work follows the Superpowers flow, in order: **brainstorming** before
any creative work (no implementation before an approved design) → approved
spec committed to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` →
**writing-plans** → execute via **subagent-driven-development** (same
session) or **executing-plans** (fresh session) → **test-driven-development**
for every feature/fix → **systematic-debugging** before proposing fixes →
**verification-before-completion** before claiming done →
**requesting-code-review** before merging substantial work.

## Model orchestration (Fable → Opus)

Canonical in [`docs/equipo/sistema-operativo-ia.md`](../docs/equipo/sistema-operativo-ia.md)
(section "Orquestación"): Fable orchestrates, Opus executes via the repo agents or a
`general-purpose` agent with `model: "opus"`; self-contained briefs; never relay a
worker's "done" unverified.

## Reglas de backend y zonas humanas

Aplicar las [reglas de CONTRIBUTING](../CONTRIBUTING.md#reglas-de-backend-independientes-del-proveedor),
extraídas de L3 V7 §12: atomicidad de estado/auditoría/outbox, bloqueo autoritativo
en DB, idempotencia por intento y webhooks autenticados, durables y deduplicados.
Los nombres canónicos son `psp_events` y `event_outbox`; C1/C2 resuelve sus defectos
sin sustituirlos por convenciones de proveedores. No generar código en las
[cinco zonas humanas](../.claude/rules/zonas-sin-ia.md), aunque la tarea se presente
como migración, refactor o adaptación a TypeScript.

## Stack y rate limiting

**Ratificado:** TypeScript, Next.js App Router, monolito modular, PostgreSQL
gestionado y workflows administrados. Scalar para documentación de API.

**A confirmar en C1:** Drizzle, Supabase, Inngest y los proveedores de auth,
almacenamiento y rate limiting. La especificación previa de rate limiting sirve
como antecedente; no impone hoy Upstash, Vercel WAF ni un fallo abierto universal.
C1 debe concretar identidad, límites por operación, excepciones y modo de fallo.
No introducir dependencias para esas decisiones antes de cerrarlas.

L3 V8 incorporará las decisiones y contratos. Los ADR Z son históricos; no abrir
nuevos ADR en `docs/decisions/`. Seguir el control de cambios del corpus.

## Frontend design

Invoke the **frontend-design** skill before writing any frontend code, every
session. Never ship generic, templated-looking UI: brand-derived colors
(never default Tailwind palette), layered tinted shadows, paired typefaces,
`transform`/`opacity` animations only, full interactive states
(`hover`/`focus-visible`/`active`), deliberate depth layering. Use real
assets when they exist. Verify visually from localhost (never `file:///`)
with ≥ 2 screenshot-compare rounds; with a reference image, match it exactly.
Mobile-first. At scaffold these rules move to the app folder's CLAUDE.md.

## Git workflow

Canonical in [CONTRIBUTING.md](../CONTRIBUTING.md): one branch per feature
(`<type>/<kebab>` off latest `main`), rebase-and-merge only, Conventional
Commits in Spanish, keep in-flight branches rebased (`--force-with-lease`
after rebasing pushed branches), `main` protected. **Never add AI co-author
trailers or "Generated with Claude Code"** — root standing rule.

## Plugin plan

- **Batch 1 (enabled)**: `hookify`, `claude-md-management`.
- **Batch 2 (first scaffold PR)**: `security-guidance`, `claude-security`,
  `typescript-lsp`, `pr-review-toolkit`, `vercel` (returns when
  there is an app to deploy).
- **Removed in the 2026-08-03 team audit**: GSD skills (overlapped
  Superpowers SDD), `claude-mem` (Z.8 probation resolved: it duplicated
  MEMORY.md without added value), `vercel-plugin` (premature pre-code).
- **Rejected — don't re-litigate without new evidence**: `feature-dev`
  (competes with Superpowers SDD), `code-review` and `code-simplifier`
  (built-ins exist), `commit-commands` (no-trailer rule),
  `claude-code-setup` (one-shot).

## Bottom line

You sit between what the user wants (specs and workflows) and what actually
gets done (code and tools). Read the instructions, make smart decisions,
call the right tools, recover from errors, and keep improving the system.

Stay pragmatic. Stay reliable. Keep learning.
