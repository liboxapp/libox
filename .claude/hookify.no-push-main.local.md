---
name: no-push-main
enabled: true
event: bash
pattern: git\s+push\s+(?!--delete)[^\n]*\b(origin\s+main|main:main|HEAD:main|--force\S*\s+origin\s+main)\b
action: block
---

🚫 **Push directo a `main` bloqueado.**

`main` solo recibe cambios vía Pull Request con rebase-and-merge (ver
`CONTRIBUTING.md`). Flujo correcto:

1. `git checkout -b <type>/<short-kebab-name>`
2. Commits convencionales en español
3. `git push -u origin <rama>` y abre el PR con `gh pr create`
