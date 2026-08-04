# CLAUDE.md — Tools (WAT layer 3)

Deterministic scripts that do the actual work: API calls, data
transformations, file operations, database queries. Consistent, testable,
fast. Credentials and API keys live in `.env` — never hardcoded, never
committed.

## Rules

- **Look for an existing tool first.** Only create a new script when nothing
  here covers the task the workflow requires.
- Offloading execution to deterministic scripts is the point: if each
  ad-hoc step is 90% accurate, five steps compound to ~59%. Scripts keep
  you at the orchestration layer where you excel.
- If a rerun burns paid API calls or credits, check with the user before
  running again.

## The self-improvement loop

Every failure is a chance to make the system stronger:

1. Identify what broke — read the full error message and trace, no guessing.
2. Fix the tool, the code, or the process that let it break.
3. Verify the fix actually works (run it; see
   verification-before-completion).
4. Record the learning where the next session will find it: the affected
   [workflow](../workflows/CLAUDE.md), this file, or the root CLAUDE.md —
   whichever owns the rule. Recurring constraints must not live only in the
   conversation.
5. Move on with a more robust system.

Example: you get rate-limited on an API → dig into the docs, discover a
batch endpoint, refactor the tool to use it, verify it works, then update
the workflow so it never happens again.
