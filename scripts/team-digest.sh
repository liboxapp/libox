#!/usr/bin/env bash
# Compact team-activity digest, injected into every Claude Code session start
# via the committed SessionStart hook (.claude/settings.json).
# Kept deliberately short: this output is paid in tokens every session.
set -uo pipefail
root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
cd "$root"
git fetch -q --prune origin 2>/dev/null || true

echo "## Team activity digest (auto)"

echo "### Open PRs"
gh pr list --limit 5 \
  --json number,title,author,headRefName \
  --template '{{range .}}- #{{.number}} {{.title}} — {{.author.login}} ({{.headRefName}}){{"\n"}}{{end}}' \
  2>/dev/null || echo "- (gh CLI not authenticated — run: gh auth login)"

echo "### Commits on main — last 7 days"
git log origin/main --since=7.days --pretty='- %h %an: %s' 2>/dev/null | head -8
[ -z "$(git log origin/main --since=7.days -1 2>/dev/null)" ] && echo "- (none)"

echo "### Most recent branches"
git for-each-ref --sort=-committerdate refs/remotes/origin \
  --format='- %(refname:short) — %(authorname), %(committerdate:relative)' 2>/dev/null \
  | grep -v 'origin/HEAD' | head -4
