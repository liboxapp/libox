# CLAUDE.md — Application code rules

This file governs all work under `src/` — the Libox application: a Next.js
(App Router) modular monolith, per [ADR Z.6](../docs/decisions/Z6-stack-tecnologico.md).
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

When the session model is Fable, orchestrate instead of typing: delegate
substantial hands-on work (multi-file features, refactors, UI builds, test
suites, debugging) to a `general-purpose` agent with `model: "opus"` — this
is standing authorization. Briefs must be self-contained: goal, files in
scope, the rules from this file, acceptance checks, what to report back.
Don't delegate trivial edits, pure analysis, or git/PR operations; if a
worker fails the same brief twice, take over. **Review gate**: never relay a
worker's "done" unverified — read the diff, rerun the checks. Broad recon can
use the `Explore` agent with `model: "sonnet"`. On Opus or lower, ignore
this section and work directly.

## Hard engineering rules

Canonical text in [CONTRIBUTING.md](../CONTRIBUTING.md). Summary:

1. **Money writes only via a single server-side Drizzle transaction**
   (`persist → audit_event → outbox`, same commit); `supabase-js` never
   writes money, tickets, draw, settlement, or audit.
2. **Webhooks ACK fast (< 2 s), process async** via `webhook_inbox` +
   idempotency key + Inngest; zero inline business logic.
3. **Concurrency is solved in the database**: constraints, TTL reservations,
   explicit locks on draw execution; idempotency keys are the second barrier.

The CONTRIBUTING scaffold checklist ships with the first code PR.

## Rate limiting (standing policy)

Canonical design:
[rate-limiting spec](../docs/superpowers/specs/2026-08-11-rate-limiting-design.md)
(+ ADR Z.6 sub-decision 5). Two layers: Vercel WAF as the coarse per-IP
shield (rules staged log → enforce, mirrored in the repo) and
`@upstash/ratelimit` on Upstash Redis as the fine layer in code. Every new
Route Handler or Server Action that mutates state or calls a paid external
API declares its policy in the rate-limit registry
(`src/lib/rate-limit.ts`) — or its explicit exemption; an endpoint with
neither does not pass review. Key by `auth.uid()` when authenticated, else
IP. Route Handlers return `429` + `Retry-After`; Server Actions return a
typed rejection (es-PE copy). Fail-open with a Sentry alert if Redis is
unreachable. Webhooks and Inngest jobs are exempt — their protection is
signature + anti-replay (hard rule 2), never a counter.

## Stack (closed — ADR Z.6)

Next.js (App Router) + TypeScript · Tailwind CSS + shadcn/ui · PostgreSQL on
Supabase (Supavisor transaction mode) · Drizzle · Inngest · Supabase Auth
(MFA) · Upstash Redis (rate limiting) · Mercado Pago behind a multi-PSP
adapter · Vercel · Sentry +
structured logs + PostHog with cross-cutting `trace_id`.

No dependencies outside this stack without an ADR in `docs/decisions/`.
Module boundaries follow the Z.6 bounded contexts.

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
  `typescript-lsp`, `pr-review-toolkit`, `vercel-plugin` (returns when
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
