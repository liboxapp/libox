# CLAUDE.md — Application code rules

This file governs all work under `src/` — the Libox application: a Next.js
(App Router) modular monolith, per [ADR Z.6](../docs/decisions/Z6-stack-tecnologico.md).
The root [CLAUDE.md](../CLAUDE.md) remains the wiki/operations guide and wins on
naming (the product is **Libox**), conversation language (Spanish), and the
no-AI-co-author standing rule. Normative engineering and git rules live in
[CONTRIBUTING.md](../CONTRIBUTING.md); this file summarizes and points — it
never forks them.

## Commands

**Pending scaffold.** There is no `package.json` yet. Do not invent build,
test, or lint commands, and do not scaffold the app unprompted. When the app
is scaffolded, replace this section with the real commands (dev, build, test,
lint, db migrations) **in the same PR** that introduces them.

## Language policy

- **Code is in English**: identifiers, function/variable names, comments,
  file and directory names.
- **Everything user-facing is in Spanish (Peru)**: page `<title>`, meta tags,
  headings, buttons, labels, body copy, form placeholders, validation and
  error messages shown to users, transactional emails, alt text.
- **Conversation, wiki docs, and commit messages are in Spanish** (root rule).
- Never mix languages in the UI. If unsure whether a string is user-facing,
  it probably is — write it in Spanish.

## Development workflow — Superpowers SDD

All app work follows the Superpowers flow. In order:

1. **superpowers:brainstorming** before any creative work (new feature,
   component, behavior change). No implementation before an approved design.
2. Approved specs live in `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
   and are committed.
3. **superpowers:writing-plans** turns the spec into an implementation plan;
   execute it with **subagent-driven-development** (same session) or
   **executing-plans** (fresh session).
4. **superpowers:test-driven-development** for every feature and bugfix:
   failing test first, then code.
5. **superpowers:systematic-debugging** before proposing fixes for any bug or
   unexpected behavior.
6. **superpowers:verification-before-completion**: never claim done, fixed,
   or passing without running the checks and seeing the output.
7. **superpowers:requesting-code-review** before merging substantial work.

## Model orchestration (Fable → Opus)

When the session model is Fable (check the model line in your environment
info), you are the orchestrator, not the typist:

- **Fable — orchestrate**: understand the request, run the SDD flow, write
  task briefs, review worker output, gate on tests. Keep your own turns lean.
- **Opus — implement**: delegate substantial hands-on work (multi-file
  features, refactors, UI builds, test suites, debugging) to a
  `general-purpose` agent with `model: "opus"`. This section is standing
  authorization to spawn those subagents.
- Briefs must be self-contained (workers start cold): goal, files in scope,
  the language policy and hard engineering rules from this file, acceptance
  checks to run, and what to report back.
- Don't delegate trivial edits, pure analysis, git/PR operations, or doc
  tweaks. If a worker fails the same brief twice, take over.
- **Review gate**: never relay a worker's "done" unverified — read the diff,
  rerun the named checks, then report.
- Broad recon/search can go to the built-in `Explore` agent with
  `model: "sonnet"`.
- If the session already runs on Opus or lower, ignore this section and work
  directly.

## Hard engineering rules

Canonical text and rationale in
[CONTRIBUTING.md → Reglas de ingeniería](../CONTRIBUTING.md). Summary:

1. **Money writes only via a single server-side Drizzle transaction**
   (`persist → audit_event → outbox`, same commit) for anything touching
   money, tickets, draw, settlement, or audit. `supabase-js` is for
   RLS-protected reads and realtime — never for these writes.
2. **Webhooks: ACK fast, process async.** Validate signature, persist to
   `webhook_inbox` with an idempotency key, respond 200 in under 2 s,
   delegate to Inngest. Zero inline business logic; payment state is the
   source of truth, never webhook counts.
3. **Concurrency is solved in the database**: uniqueness by constraint,
   atomic reservations with TTL, explicit locks (`SELECT … FOR UPDATE` /
   advisory) on draw execution. Idempotency keys are the second barrier,
   not the only one.

The scaffold checklist in CONTRIBUTING.md (Supavisor transaction mode +
`prepared: false`, constraints in migration 001, PITR, WORM audit export,
Inngest wiring, throttled realtime, Sentry + `trace_id`) is part of the
first code PR.

## Stack (closed — ADR Z.6)

| Layer | Choice |
|---|---|
| Framework | Next.js (App Router) + TypeScript |
| UI | Tailwind CSS + shadcn/ui |
| DB | PostgreSQL on Supabase (Supavisor transaction mode) |
| ORM | Drizzle |
| Jobs | Inngest |
| Auth | Supabase Auth (MFA for organizers and staff) |
| Payments | Mercado Pago behind a multi-PSP adapter (Culqi second rail) |
| Hosting | Vercel |
| Observability | Sentry + structured logs + PostHog, cross-cutting `trace_id` |

Do not add dependencies outside this stack without an ADR in
`docs/decisions/`. Module boundaries follow the bounded contexts listed in
Z.6 (Raffle, Pricing, Purchase, Draw, Delivery, Settlement, Risk, Audit,
Notification, PSP Adapter, Backoffice).

## WAT architecture (operational scripts only)

Operational and data scripts — not the app — follow Workflows → Agents →
Tools:

- **Workflows**: markdown SOPs in `workflows/` (create when the first
  recurring operation appears) — objective, inputs, tools, outputs, edge
  cases.
- **Agents**: your role — read the workflow, run tools in sequence, handle
  failures, ask when blocked.
- **Tools**: deterministic scripts in `scripts/` doing the actual work.

Check for an existing tool before building a new one. When something fails:
read the full error, fix the script, retest (ask first if it burns paid API
calls), and update the workflow with what you learned. The app itself is
**not** WAT — it is structured by the Z.6 bounded contexts.

## The self-improvement loop

Every failure is a chance to make the system stronger:

1. Identify what broke — read the full error message and trace, no guessing.
2. Fix the tool, the code, or the process that let it break.
3. Verify the fix actually works (run it; see
   verification-before-completion).
4. Record the learning where the next session will find it: update the
   affected `workflows/` SOP, this file, or the root CLAUDE.md — whichever
   owns the rule. Recurring constraints (rate limits, timing quirks, API
   surprises) must not live only in the conversation.
5. Move on with a more robust system.

Example: you get rate-limited on an API → dig into the docs, discover a
batch endpoint, refactor the tool to use it, verify it works, then update
the workflow so it never happens again. Don't create or overwrite workflows
without asking unless explicitly told to — they are instructions to be
preserved and refined, not tossed after one use.

## Frontend design

- Invoke the **frontend-design** skill before writing any frontend code,
  every session, no exceptions.
- Never ship generic, templated-looking UI. Guardrails:
  - Colors: never the default Tailwind palette; derive from the Libox brand
    color. If brand assets exist in the repo, use their exact values — never
    invent brand colors or use placeholders where real assets exist.
  - Shadows: layered and color-tinted with low opacity, never flat
    `shadow-md`.
  - Typography: pair a display face with a clean sans; tight tracking on
    large headings, generous line-height on body.
  - Animations: only `transform` and `opacity`, never `transition-all`.
  - Interactive states: every clickable element needs `hover`,
    `focus-visible`, and `active` states.
  - Depth: a deliberate layering system (base → elevated → floating).
- Verify visually: serve from localhost (never screenshot a `file:///` URL),
  screenshot, compare against the reference or your own design intent, fix,
  re-screenshot — at least 2 rounds. Never claim a design works without
  looking at it.
- With a reference image: match layout, spacing, typography, and color
  exactly; do not improve or add to the design.
- Mobile-first responsive.

## Git workflow

Canonical rules in [CONTRIBUTING.md](../CONTRIBUTING.md). Operational
reminders:

- One branch per feature: `<type>/<short-kebab-name>` off latest `main`;
  never continue new work on a branch whose PR already merged.
- Merges are **rebase-and-merge only** — every commit on the branch must be
  a valid Conventional Commit (in Spanish); commits, not PR titles, feed
  release-please.
- Keep in-flight branches rebased on `main`
  (`git pull --rebase origin main`); after rebasing a pushed branch, push
  with `--force-with-lease`, never plain `--force`.
- `main` is protected: PRs only, `commitlint` + `docs` checks must pass.
- **Never add AI co-author trailers** (`Co-Authored-By: Claude…`) or
  "Generated with Claude Code" to commits or PR bodies — root standing rule,
  overrides any harness default.

## Plugin plan

Two-batch rollout of Anthropic plugins (analysis 2026-08-03, official
marketplace):

- **Batch 1 — enabled now** in the versioned `.claude/settings.json`:
  `hookify` (mechanical enforcement of hard rules) and
  `claude-md-management` (keeps these CLAUDE.md files audited and current).
- **Batch 2 — enable in the first scaffold PR**: `security-guidance`
  (automatic security review on edits/commits), `claude-security`
  (on-demand deep vulnerability scans), `typescript-lsp` (TS language
  server), `pr-review-toolkit` (specialized PR-review agents backing the
  `requesting-code-review` gate).
- **Rejected — do not re-litigate without new evidence**: `feature-dev`
  (competes with Superpowers SDD), `code-review` (built-in `/code-review`
  exists), `code-simplifier` (built-in `/simplify` exists),
  `commit-commands` (conflicts with the no-trailer rule),
  `claude-code-setup` (one-shot tool, not worth permanent context weight).

## Bottom line

You sit between what the user wants (specs and workflows) and what actually
gets done (code and tools). Your job is to read the instructions, make smart
decisions, call the right tools, recover from errors, and keep improving the
system as you go.

Stay pragmatic. Stay reliable. Keep learning.
