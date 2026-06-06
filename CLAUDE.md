# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Sortibox is a **web marketplace for paid-ticket digital raffles** operating under Peruvian regulation. The repo is currently in **pure planning stage — there is no code yet**: no application, no `package.json`, no build/lint/test tooling, and no git repository. It is a **documentation wiki** that captures product decisions, architecture, and regulatory analysis before the first line of code is written.

Do not invent build/test commands or scaffold a stack unprompted. When code work begins, this file should be updated with the real commands and architecture at that point.

## Wiki layout (`docs/`)

Start every session by reading `docs/README.md` — it is the index and explains how the documents relate.

| Path | Role |
|---|---|
| `docs/README.md` | Wiki index + map of how documents connect. Entry point. |
| `docs/prd/ALAZAR LIBOX PRD V11.pdf` | Partner's 48-page PRD. Authoritative **technical/product blueprint** (fintech-grade: RBAC, Purchase/Draw/Delivery/Settlement engines, double-entry ledger, audit-first, APIs, threat model). Geographically agnostic — does **not** cover Peru compliance. |
| `docs/plans/sortibox-plan.md` | Living plan: product, architecture, stack, roadmap. Contains **Anexo Z** — the running log of closed decisions. Mirrored at `~/.claude/plans/spicy-sparking-hopcroft.md`; the `docs/` copy is canonical for the team. |
| `docs/decisions/` | Self-contained ADRs, one per closed decision. The shareable canonical record for partners/investors. See `docs/decisions/README.md` for the convention. |
| `docs/compliance-peru.md` | Working doc for the Peruvian regulatory frame (SUNAT, municipal authorization, prize tax withholding, KYC, PLAFT, T&C). Deliberately kept **separate from the PRD**. Still a stub pending the lawyer. |

## Reading the PDF PRD

The native Read tool cannot render this PDF (poppler not installed). Extract text with Python instead:

```
python3 -m pip install --user --quiet pypdf
python3 -c "from pypdf import PdfReader; r=PdfReader('docs/prd/ALAZAR LIBOX PRD V11.pdf'); print('\n'.join(p.extract_text() for p in r.pages))"
```

## Decision workflow (important)

The core activity here is resolving conflicts between the partner's PRD and the Sortibox plan, **one at a time, in depth** — the user (Diego) explicitly does not want simplified summaries. When a decision is closed:

1. Document it as an entry **Z.N** in `docs/plans/sortibox-plan.md` (Anexo Z), and
2. Simultaneously create a self-contained ADR `docs/decisions/Z<n>-<slug>.md`, then
3. Update the indexes in `docs/README.md` and `docs/decisions/README.md`.

ADR structure: Decision · Alternatives evaluated · Why each was rejected · Implications the team must accept · Impact on the PRD · Pending external validations · Questions for partners.

### Conflict status (PRD vs plan)

- **Closed:** Z.1 Custodia del dinero → Modelo C (conceptual escrow). See `docs/decisions/Z1-custodia-del-dinero.md`.
- **Open:** PSP choice, organizer type (natural vs juridical), how many raffle types in MVP-1, T8 LIVE inclusion.

## Conventions

- **Language: Spanish** (Peruvian market). Write docs and respond in Spanish.
- **Legal claims** are marked `[LEGAL→ABOGADO]` when they are the author's reading of public Peruvian law and require ratification by the team's lawyer. Never present these as settled legal advice.
- **Naming:** the product is **Sortibox**. The PRD says "ALAZAR" and the PDF "LIBOX" — those are legacy names and do not prevail.
- **Obsidian vault:** the project root opens as an Obsidian vault. `.obsidian/app.json` is committed and forces **standard markdown links** (`[text](path.md)`), not wikilinks `[[...]]`, to keep shareable docs portable to GitHub/any viewer. Reserve `[[wikilinks]]` for the private memory files only. Per-machine Obsidian state is gitignored.
- **Frontmatter:** every wiki doc carries YAML `title`, `status`, `tags`, `updated`.
- **Markdown links** are relative to the `docs/` root so the wiki renders both in-editor and in any Markdown viewer.
- Persistent project context lives in auto-memory under `~/.claude/projects/-Users-diegocotrina-Desktop-sortibox/memory/` (loaded automatically); the in-repo wiki is the shareable source of truth.

## Key product facts (closed with Diego, 2026-06-05)

- MVP scope: **paid-ticket raffles only** (no free promotional sweepstakes).
- Organizers: **juridical persons with RUC only** in MVP.
- Monetization: **commission per ticket sold**.
- Payments: **fiat**, web responsive, **not** blockchain. "Auditable" = compliance with Peruvian financial law, achieved via the PRD's cryptographic draw proof + append-only audit ledger.
