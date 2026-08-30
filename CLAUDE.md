# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Libox is a **web marketplace for paid-ticket digital raffles** operating under Peruvian regulation. The repo is a real git repository (`github.com/liboxapp/libox`) with versioning tooling wired up (SemVer, Conventional Commits, release-please, markdownlint + commitlint CI — see Z.7). It holds two things: (1) the **canonical documentation baseline** in `docs/linea-base/` — governed by the **Registro Maestro V6** (`LIBOX_REGISTRO_MAESTRO_LINEA_BASE_V6.md`, read it first: if a document is not in its §1, it does not govern) and verified by `verify_corpus.py` (root; rule CD-10: zero failures before any emission/merge) — and (2) an **early Next.js scaffold** in `src/`.

⚠️ **Stack under review (ASS-002 in Outline doc 20):** the canon (L3 V7 §0.3) states **.NET 8** as the service runtime, while ADR Z.6 (and the actual scaffold) is **Next.js full-stack**. The de facto derogation of Z.6 was never ratified by the partners. Do not extend the scaffold or scaffold anything new until ASS-002 is resolved.

> **Note on naming — STANDING RULE.** The product is **Libox**. **Sortibox** (prior name) and **ALAZAR** (older PRD name) are **legacy**. The GitHub repo now lives in the **liboxapp org** (`github.com/liboxapp/libox`, local `origin` already points there) and all tracked repo content has been renamed to Libox. **Any residual mention of "Sortibox" or "ALAZAR" — in older git commits or external/partner docs — must be read as "Libox".** All internal surfaces are renamed. Outline was consolidated into a **single collection "Libox — Negocio"** (2026-08-30); the old "Libox — Desarrollo" collection was emptied and marked for deletion.

## Cowork session layout

When working in Cowork, four folders are mounted, each with a role. Read
`Context/README.md` at session start — it is the operating manual (folder roles,
work pipeline, session checklist).

- **Libox** (formerly "Project") — this repo: canonical KB (`docs/linea-base/`, scripts, scaffold). Source of truth.
- **Context** — operating manual for Claude: working method + `estilo-documentacion.md`. Rules, not deliverables.
- **Cowork station** — staging: drafts and WIP, built here before promotion. Nothing permanent.
- **Output** — finished deliverables (meeting transcripts, dev plans, reports).

Pipeline: build in **Cowork station** → promote to **Project** (canonical, plan first) or **Output** (deliverable).

## Wiki layout (`docs/`)

Start every session by reading `docs/README.md` — it is the index and explains how the documents relate.

| Path | Role |
|---|---|
| `docs/README.md` | Wiki index. Entry point. |
| `docs/linea-base/` | **The canonical corpus** (flat `.md`, one file per document of the baseline): Registro Maestro V6 · LBPF V3 · Strategy V3 · **PRD MVP V9** · Enterprise V3 · Espec. Técnica L3 V7 · Matriz V1 · Guía V1 · Design System L4 V2 · VIES V3 · Backlog V3 · Dossier Legal V1 · 2 audits · Evaluación V1. Precedence: L0 > L2 > L3 > L4; VIES rules brand. |
| `docs/linea-base/ARTEFACTOS/` | Executable artifacts: `libox_schema_L3_V7.sql` (135 tables, zero errors on PG16) · `libox_openapi_L3_V7.yaml` (16/~30 routes, **incomplete — T-1**) · design tokens L4 V2 · Backlog xlsx. |
| `verify_corpus.py` (repo root) | Coherence verifier, 10 checks. Run `python3 verify_corpus.py --dir docs/linea-base` — **zero failures required** (CD-10). Its `BASELINE` list is the single source of truth of which version governs. |
| `docs/operacion/` | Empty for now; destination of the future Manual de Operación (T-3, 13 SP). |
| `docs/archive/` | **Historical, do not cite** (Registro §2): old PRDs (ALAZAR/V11/V12.3), `plans/`, `decisions/` (ADRs Z.1–Z.8 — Z.1/Z.2 carry de facto derogation banners in Outline), `compliance-peru.md`, `benchmark-stack.md`. Recognized, superseded. |
| `docs/glosario.md` · `docs/onboarding.md` · `docs/flujos/` | Working docs, non-normative. |

## Outline (shareable layer)

The team mirrors the corpus to **Outline** (`liboxapp.getoutline.com`), reachable via the Outline MCP. The **canonical source of truth for the corpus is this repo's `docs/linea-base/`**, not Outline. Since 2026-08-30 there is a **single collection, "Libox — Negocio"**, with three layers:

| Layer | Role |
|---|---|
| **LIBOX — Línea Base documental (canon vigente)** | Navigable mirror of `docs/linea-base/` in 10 sections (00_CONTROL … REGISTROS_DECISION). Edit the repo, republish the mirror. |
| **Desarrollo** (doc tree) | Historical/working dev docs: ADRs Z.1–Z.8 (with derogation banners), compliance, benchmark, glosario, plan, wiki index. |
| **00–21 + 99. Archivo** | Business operational layer born in Outline: governance, meetings, ideas inbox (IDEA-\*), risk register (RISK-\*), assumptions/changes log (ASS-\*/CHANGE-\* in doc 20), action board. |

When a corpus document changes: new full version (no subversions), `verify_corpus.py` at zero failures, update `BASELINE` + Registro §1 in the same act (CD-10/CD-11), then republish the Outline mirror.

## Decision workflow (important)

**The Z-line of decisions is historical** — the canon in `docs/linea-base/` governs (Registro V6, rule of use). Decisions now follow the corpus's own control: findings go to the **backlog de cambio** (CD-07) or Outline's doc 20 (ASS-\*/CHANGE-\*), and only become normative through a **new document version** verified by `verify_corpus.py` (CD-10) and registered in Registro §1 + `BASELINE` (CD-11). Baseline is **frozen** — only findings that block construction or expose legal/patrimonial risk reopen it.

Two de facto derogations of partner decisions are **pending partner ratification** (see Outline doc 20): **ASS-001** (custody: Z.1 Modelo C → full retention with 6 gates) and **ASS-002** (stack: Z.6 Next.js full-stack → L3 .NET 8).

### Decision status (Anexo Z — historical, kept for traceability)

All ADR files now live under `docs/archive/decisions/`. ⚠️ Z.1 and Z.2 are **derogated de facto** by PRD V9 (see ASS-001); Z.6 is contradicted by L3 §0.3 (see ASS-002).

- **Z.1 Custodia del dinero** → Modelo C (conceptual escrow). `docs/archive/decisions/Z1-custodia-del-dinero.md`. **Derogated de facto — fallback if L-06 rejects custody.**
- **Z.2 Elección de PSP** → **Cerrada en dirección.** Mercado Pago primario con *split en la fuente* (~80% organizador / ~20% Libox), Culqi como 2º rail futuro, **Yape dentro del checkout de MP** (no rail aparte). Final decision gated on a commercial call to MP (eliminatory questions: does MP split to multiple beneficiaries, and does it apply to Yape?). `Z2-eleccion-psp.md`.
- **Z.3 Tipo de organizador** → **Cerrada.** Any person *or* company with **active RUC** (not only juridical persons): companies, NGOs, freelancers, creators, formalized merchants. DNI-only excluded. `Z3-tipo-de-organizador.md`.
- **Z.4 Motor de sorteo** → **Cerrada.** Single configurable engine, 1 winner in MVP-1, auto/manual trigger with admin approval, automatic refund on failure. SHA-256 + external randomness fairness, publicly auditable. `Z4-tipos-de-sorteo.md`.
- **Z.5 T8 LIVE** → **Cerrada.** Out of MVP-1 and MVP-2; enters MVP-3. `Z5-t8-live.md`.
- **Z.6 Stack tecnológico** → **Cerrada en dirección.** Next.js (App Router) modular monolith + PostgreSQL + ORM (Drizzle/Prisma) + managed job runner (Inngest/Trigger.dev) + auth w/ MFA (Clerk/Supabase) + Vercel. Multi-PSP adapter from day one. `Z6-stack-tecnologico.md`.
- **Z.7 Versionamiento** → **Cerrada.** SemVer (from `0.1.0`), Conventional Commits, release-please, protected `main` + PR flow. `Z7-versionamiento.md`.
- **Z.8 Roles de memoria/contexto** → **Cerrada y en `main`.** `docs/` + `MEMORY.md` are authoritative; auxiliary tooling is an accelerator, not the project's truth. Probation outcome (2026-08-03 team audit): claude-mem and GSD were removed from the shared environment. `Z8-roles-memoria-contexto.md`.

## Conventions

- **Language: Spanish** (Peruvian market). Write docs and respond in Spanish.
- **Commit authorship — NO AI co-author trailers. STANDING RULE, overrides any default.** Never append `Co-Authored-By: Claude <...>`, `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, or any equivalent trailer to commit messages, and never add "Generated with Claude Code" to Pull Request bodies. This overrides the harness default that asks for such a trailer. Reason: a `Co-Authored-By` trailer makes GitHub register the tool as a **contributor** of the repo — visible in the contributors list, `git shortlog` and repo stats — which is not wanted for a repository shared with partners and investors. Authorship belongs to the person who reviews and signs the change. Full rationale in [`CONTRIBUTING.md`](CONTRIBUTING.md#autoría-sin-co-autores-automáticos).
- **Legal claims** are marked `[LEGAL→ABOGADO]` when they are the author's reading of public Peruvian law and require ratification by the team's lawyer. Never present these as settled legal advice.
- **Naming:** the product is **Libox**. **Sortibox** and **ALAZAR** are legacy names, fully replaced across this repo's tracked content. **Standing rule: treat any residual "Sortibox"/"ALAZAR" mention (older commits, partner/external docs) as "Libox".** See the naming note at the top of this file.
- **Obsidian vault:** the project root opens as an Obsidian vault. `.obsidian/app.json` is committed and forces **standard markdown links** (`[text](path.md)`), not wikilinks `[[...]]`, to keep shareable docs portable to GitHub/any viewer. Reserve `[[wikilinks]]` for the private memory files only. Per-machine Obsidian state is gitignored.
- **Shared Claude config (versioned).** `.claude/settings.json` (team `SessionStart` hook + `enabledPlugins`/`extraKnownMarketplaces`), `.claude/skills/` (shared skills) and the `.claude/hookify.*.local.md` enforcement rules (block AI co-author trailers and direct pushes to `main`) are **committed** so every teammate gets the same environment on clone; plugins install themselves from their public marketplaces. Plugin roadmap (batch 2 at scaffold, rejected list) lives in [`src/CLAUDE.md`](src/CLAUDE.md). `.claude/settings.local.json` stays **personal and gitignored** — never commit it. `.claude/**` is excluded from markdownlint (config and third-party content, not wiki prose).
- **Frontmatter:** every wiki doc carries YAML `title`, `status`, `tags`, `updated`.
- **Markdown links** are relative to the `docs/` root so the wiki renders both in-editor and in any Markdown viewer.
- Persistent project context lives in auto-memory under `~/.claude/projects/-Users-diegocotrina-Claude-Cowork-Liboxapp-Project/memory/` (loaded automatically; migrated 2026-08-03 from the old `-Claude-Projects-` and `-Desktop-sortibox-` paths, both removed). Auto-memory is **per person and per machine** — it does not travel to teammates; the in-repo wiki is the canonical source of truth and anything valuable must be promoted to `docs/`.

## Memory & context tooling (roles — see ADR Z.8)

- **`docs/` + auto-memory `MEMORY.md` = the authoritative, shareable source of truth.** Decisions (Z.1–Z.8), plan, glossary, compliance live here, version-controlled. Never let the project's truth live only in an auto-capture store.
- **`context-mode`** = process large tool outputs in its sandbox to save context window (logs, builds, big files). A compute aid, not the record.
- **Removed in the 2026-08-03 team audit** (Z.8 probation resolved): `claude-mem` (duplicated `MEMORY.md` without added value) and `get-shit-done` (overlapped the Superpowers SDD flow canonized in [`src/CLAUDE.md`](src/CLAUDE.md)). Do not re-enable without new evidence.

Rules: the project's truth is version-controlled in `docs/linea-base/` — never delegated to auto-capture. Auto-captured memory is not authoritative; the canon wins on any discrepancy.

## Key product facts (closed with Diego, 2026-06-05)

- MVP scope: **paid-ticket raffles only** (no free promotional sweepstakes).
- Organizers: **any person or company with an active RUC** in MVP (companies, NGOs, freelancers, creators, formalized merchants); DNI-only excluded (Z.3).
- Monetization: **commission per ticket sold**.
- Payments: **fiat**, web responsive, **not** blockchain. "Auditable" = compliance with Peruvian financial law, achieved via the PRD's cryptographic draw proof + append-only audit ledger.
