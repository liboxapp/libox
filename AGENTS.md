Instrucciones compartidas de Libox.

Lee `CLAUDE.md` y las reglas aplicables en `.claude/rules/` antes de trabajar.
El corpus y el scaffold conservan sus restricciones de cambio.
Para auditorías usa `.claude/skills/libox-system-design-audit/SKILL.md` en modo
revisor Codex y `docs/equipo/ai-audit-harness.md`. No simules revisiones de Claude.

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
