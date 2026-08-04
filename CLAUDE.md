# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Libox is a **web marketplace for paid-ticket digital raffles** operating under Peruvian regulation. The repo is **still pre-code** — no application and no `package.json` yet — but it is **no longer bare planning**: it is a real git repository (`github.com/liboxapp/libox`) with versioning tooling already wired up (SemVer, Conventional Commits, release-please, markdownlint + commitlint CI — see Z.7). Its content is a **documentation wiki** capturing product decisions, architecture, stack, and regulatory analysis before the first line of app code.

Do not invent build/test commands or scaffold a stack unprompted. The **stack is already decided** (Z.6: Next.js App Router modular monolith + PostgreSQL) but **not yet scaffolded**. When code work begins, update this file with the real commands and architecture at that point.

> **Note on naming — STANDING RULE.** The product is **Libox**. **Sortibox** (prior name) and **ALAZAR** (older PRD name) are **legacy**. The GitHub repo now lives in the **liboxapp org** (`github.com/liboxapp/libox`, local `origin` already points there) and all tracked repo content has been renamed to Libox. **Any residual mention of "Sortibox" or "ALAZAR" — in older git commits or external/partner docs — must be read as "Libox".** All internal surfaces are renamed: the Outline collection is **"Libox — Desarrollo"** (2026-06-21) and the auto-memory was migrated and renamed (2026-08-03).

## Cowork session layout

When working in Cowork, four folders are mounted, each with a role. Read
`Context/README.md` at session start — it is the operating manual (folder roles,
work pipeline, session checklist).

- **Project** — this repo: canonical KB (`docs/`, decisions, plan, scripts). Source of truth.
- **Context** — operating manual for Claude: working method + `estilo-documentacion.md`. Rules, not deliverables.
- **Cowork station** — staging: drafts and WIP, built here before promotion. Nothing permanent.
- **Output** — finished deliverables (meeting transcripts, dev plans, reports).

Pipeline: build in **Cowork station** → promote to **Project** (canonical, plan first) or **Output** (deliverable).

## Wiki layout (`docs/`)

Start every session by reading `docs/README.md` — it is the index and explains how the documents relate.

| Path | Role |
|---|---|
| `docs/README.md` | Wiki index + map of how documents connect. Entry point. |
| `docs/prd/LIBOX PRD BLUEPRINT MVP V12 3.docx` + `ENTERPRISE V12 3.docx` | Partner's PRD **V12.3**, now split in two: **MVP** (modular monolith, Role Books USER/CLIENT/ADMIN/SUPPORT, Raffle Engine T1-T8, Anexo K Legal Perú-first, Anexo L investor readiness) and **Enterprise** (target state: 20 microservices, event-driven). Authoritative technical/product blueprint. ⚠️ V12.3 conflicts with closed ADRs (settlement gates vs Z.1, target-based pricing, T8 in MVP vs Z.5) — see the deltas analysis before treating any V12 mechanic as agreed. |
| `docs/prd/Libox PRD V11.pdf` | Previous PRD (historical). ADRs Z.1-Z.8 cite it; keep for traceability. Geographically agnostic — Peru compliance entered the PRD only in V12.3 (Anexo K). |
| `docs/plans/libox-plan.md` | Living plan: product, architecture, stack, roadmap. Contains **Anexo Z** — the running log of closed decisions. Mirrored at `~/.claude/plans/spicy-sparking-hopcroft.md`; the `docs/` copy is canonical for the team. |
| `docs/decisions/` | Self-contained ADRs, one per closed decision. The shareable canonical record for partners/investors. See `docs/decisions/README.md` for the convention. |
| `docs/compliance-peru.md` | Working doc for the Peruvian regulatory frame (SUNAT, municipal authorization, prize tax withholding, KYC, PLAFT, T&C). Deliberately kept **separate from the PRD**. Still a stub pending the lawyer. |

## Outline (shareable layer)

The team mirrors the wiki to **Outline** (`liboxapp.getoutline.com`), reachable via the Outline MCP (already configured — no setup needed per session). The **canonical source of truth is this git repo `docs/`**, not Outline. Two collections:

| Collection | Role |
|---|---|
| **Libox — Desarrollo** | **Read-only mirror** of `docs/` (ADRs Z.1–Z.8, plan, glosario, compliance, PRD). Each mirrored ADR banners: "fuente canónica vive en el repo GitHub… changes via PR, then republished here." Edit the repo, not the mirror. |
| **Libox — Negocio** | **Business operational layer** (born in Outline, not mirrored): governance, meetings, backlog, risk register, traceability matrix, roadmap, finances. Its per-decision docs are **business summaries** that point to the canonical dev ADR. |

When a decision changes, edit the canonical file in `docs/decisions/` (via PR), then republish the Outline mirror.

## Reading the PDF PRD

The native Read tool cannot render this PDF (poppler not installed). Extract text with Python instead:

```
python3 -m pip install --user --quiet pypdf
python3 -c "from pypdf import PdfReader; r=PdfReader('docs/prd/Libox PRD V11.pdf'); print('\n'.join(p.extract_text() for p in r.pages))"
```

## Decision workflow (important)

The core activity here is resolving conflicts between the partner's PRD and the Libox plan, **one at a time, in depth** — the user (Diego) explicitly does not want simplified summaries. When a decision is closed:

1. Document it as an entry **Z.N** in `docs/plans/libox-plan.md` (Anexo Z), and
2. Simultaneously create a self-contained ADR `docs/decisions/Z<n>-<slug>.md`, then
3. Update the indexes in `docs/README.md` and `docs/decisions/README.md`.

ADR structure: Decision · Alternatives evaluated · Why each was rejected · Implications the team must accept · Impact on the PRD · Pending external validations · Questions for partners.

### Decision status (Anexo Z)

**All four original PRD-vs-plan conflicts are now closed**, plus three further decisions (Z.6–Z.8). Current state:

- **Z.1 Custodia del dinero** → Modelo C (conceptual escrow). `docs/decisions/Z1-custodia-del-dinero.md`.
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

Rules: every closed decision is still documented as an ADR in `docs/decisions/` + Anexo Z mirror — never delegated to auto-capture. Auto-captured memory is not authoritative; ADRs/plan win on any discrepancy.

## Key product facts (closed with Diego, 2026-06-05)

- MVP scope: **paid-ticket raffles only** (no free promotional sweepstakes).
- Organizers: **any person or company with an active RUC** in MVP (companies, NGOs, freelancers, creators, formalized merchants); DNI-only excluded (Z.3).
- Monetization: **commission per ticket sold**.
- Payments: **fiat**, web responsive, **not** blockchain. "Auditable" = compliance with Peruvian financial law, achieved via the PRD's cryptographic draw proof + append-only audit ledger.
