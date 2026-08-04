# CLAUDE.md — Tests

## Rules

- **Test-driven development** (superpowers:test-driven-development) for
  every feature and bugfix: write the failing test first, watch it fail,
  then write the code that makes it pass.
- **Commands pending scaffold** — there is no test runner yet. When the app
  is scaffolded, document here the real commands (full suite + single test)
  in the same PR.
- Tests are code: English names and comments, one clear behavior per test,
  arrange–act–assert.
- Money, tickets, draw, settlement, and audit paths get priority coverage —
  including concurrency (unique constraints, idempotency, double-webhook
  delivery) per the hard engineering rules in
  [CONTRIBUTING.md](../../CONTRIBUTING.md).
- **Never claim a test passes without running it** and seeing the output
  (verification-before-completion).
