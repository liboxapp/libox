# CLAUDE.md — Workflows (WAT layer 1)

Markdown SOPs for recurring operational tasks — the instructions layer of
the Workflows → Agents → Tools architecture. The app itself is **not** WAT;
it follows the modular TypeScript monolith ratified in the
[R0 program](../../docs/superpowers/specs/2026-09-25-habilitar-r0-design.md).

## Rules

- Each workflow defines: objective, required inputs, which tools from
  [../tools/](../tools/CLAUDE.md) to use, expected outputs, and how to
  handle edge cases. Written in plain English, the way you'd brief a
  teammate.
- **Read the relevant workflow before acting.** If a task has a workflow,
  follow it instead of improvising; connect intent to execution without
  trying to do everything yourself.
- **Keep workflows current.** When you find better methods, discover
  constraints (rate limits, timing quirks, API surprises), or hit recurring
  issues, update the workflow so the learning survives the session.
- **Don't create or overwrite workflows without asking** unless explicitly
  told to — they are instructions to be preserved and refined, not tossed
  after one use.
