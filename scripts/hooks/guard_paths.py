"""Clasificación léxica y real de rutas; no ejecuta Git ni comandos de usuario."""
import os
from pathlib import Path
import sys


def warn(component):
    print('AVISO: ' + component + ' no pudo verificar; permite por política fail-open. Revise el CI.', file=sys.stderr)


def candidates(file_path, root):
    """Ambas vistas evitan perder protección al resolver symlinks hacia fuera."""
    root = os.path.abspath(root)
    lexical = os.path.abspath(os.path.join(root, file_path))
    result = []
    for target in (lexical, os.path.realpath(lexical)):
        anchor = root
        for parent in Path(target).parents:
            if (parent / '.git').exists():
                anchor = str(parent)
                break
        rel = os.path.relpath(target, anchor).replace(os.sep, '/')
        if rel != '..' and not rel.startswith('../'):
            pair = (rel, target)
            if pair not in result:
                result.append(pair)
    return result
