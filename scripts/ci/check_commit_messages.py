#!/usr/bin/env python3
"""Rechaza atribución automática de IA sin imprimir mensajes de commits."""
import re
import subprocess
import sys

from git_objects import git, revisions

ATTRIBUTION = re.compile(
    r'^\s*co-authored-by\s*:.*(?:\bclaude\b|\bcodex\b|\bopenai\b|\bchatgpt\b|'
    r'\bcopilot\b|\bgemini\b|\bcursor\b|\bai\b|\bbot\b|noreply@anthropic\.com)',
    re.IGNORECASE | re.MULTILINE,
)
GENERATED = re.compile(r'generated\s+with\b', re.IGNORECASE)


def main():
    try:
        base, head = revisions()
        rejected = []
        for oid in git('rev-list', base + '..' + head).decode('ascii').splitlines():
            message = git('show', '-s', '--format=%B', oid).decode('utf-8', errors='replace')
            if ATTRIBUTION.search(message) or GENERATED.search(message):
                rejected.append(oid)
    except (ValueError, OSError, subprocess.CalledProcessError):
        print('No se pudieron verificar los mensajes de commits.', file=sys.stderr)
        return 2
    for oid in rejected:
        print('DENY: atribución automática de IA en commit ' + oid)
    if not rejected:
        print('Autoría de commits: OK')
    return 1 if rejected else 0


if __name__ == '__main__':
    sys.exit(main())
