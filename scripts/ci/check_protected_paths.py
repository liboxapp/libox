#!/usr/bin/env python3
"""Bloquea cambios al canon y scaffold usando el freeze de la base. Python 3.9+."""
import re
import subprocess
import sys

from git_objects import revisions, tree

FREEZE = '.claude/rules/src-congelado.md'
FROZEN_FILES = {
    'package.json', 'package-lock.json', 'next.config.ts', 'tsconfig.json',
    'components.json', 'eslint.config.mjs', 'postcss.config.mjs', 'vitest.config.ts',
}
VERSION = re.compile(r'[_-]V\d+\.')


def violations(base, head):
    changed = {path for path in base.keys() | head.keys()
               if base.get(path) != head.get(path)}
    archived = {entry for path, entry in head.items() if path.startswith('docs/archive/')}
    errors = []
    for path in sorted(changed):
        if (path in base and path.startswith('docs/linea-base/')
                and VERSION.search(path.rsplit('/', 1)[-1])):
            if path in head or base[path] not in archived:
                errors.append(('canon inmutable (CD-07/CD-08)', path))
        if FREEZE in base:
            source = path == 'src' or (path.startswith('src/')
                                      and path.rsplit('/', 1)[-1] != 'CLAUDE.md')
            if source or path in FROZEN_FILES or path == FREEZE:
                errors.append(('freeze de la base activo; requiere transición revisada de D1', path))
    return errors


def main():
    try:
        base, head = revisions()
        errors = violations(tree(base), tree(head))
    except (ValueError, OSError, subprocess.CalledProcessError):
        print('No se pudo verificar la política de rutas protegidas.', file=sys.stderr)
        return 2
    for reason, path in errors:
        # repr evita que nombres con saltos de línea inyecten comandos de Actions.
        print('DENY: ' + reason + ': ' + ascii(path))
    if not errors:
        print('Rutas protegidas: OK')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
