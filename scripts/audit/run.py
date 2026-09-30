"""Gestiona snapshots de auditoría sin ejecutar revisores (Python 3.9+, Git, POSIX)."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import json
from pathlib import Path
import re
import subprocess
import sys

from sanitize import sanitize

REVIEWERS = ('fable', 'opus', 'codex')
REPORT = re.compile(r'(?:fable-report|opus-report|codex-report|synthesis)(?:-attempt-(?:[2-9]|[1-9][0-9]+))?\.md\Z')


def git(repo, *args):
    result = subprocess.run(['git', '-C', str(repo), *args], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    if result.returncode:
        # No volcar stderr: puede incluir configuración o rutas sensibles.
        raise ValueError('Git falló (código %s); operación %s' % (result.returncode, args[0]))
    return result.stdout.decode('utf-8', errors='surrogateescape')


def locations(repo, run_id):
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}', run_id):
        raise ValueError('run-id inválido')
    root = Path(git(repo, 'rev-parse', '--show-toplevel').strip()).resolve()
    common = Path(git(root, 'rev-parse', '--git-common-dir').strip())
    if not common.is_absolute():
        common = root / common
    state = common.resolve() / 'libox-audit-runs'
    run_dir = root / 'docs' / 'audits' / run_id
    for part in (root / 'docs', root / 'docs/audits', run_dir):
        if part.is_symlink():
            raise ValueError('Ruta de run enlazada no permitida')
    return root, state, run_dir


@contextmanager
def locked(state):
    state.mkdir(exist_ok=True)
    with (state / '.lock').open('a') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield


def check_host(root, run_id=None):
    status = git(root, 'status', '--porcelain=v1', '-z', '--untracked-files=all')
    prefix = 'docs/audits/%s/' % run_id if run_id else None
    for entry in filter(None, status.split('\0')):
        if not (prefix and entry.startswith('?? ' + prefix)):
            raise ValueError('Snapshot sucio o cambio concurrente fuera del run')
    if prefix:
        folder = root / prefix
        if any(path.is_symlink() for path in folder.rglob('*')):
            raise ValueError('Enlace simbólico dentro del run')


def exclusive(path, text):
    with path.open('x', encoding='utf-8') as handle:
        handle.write(text)


def start(repo, run_id, scope):
    root, state, run_dir = locations(repo, run_id)
    if scope not in ('harness', 'producto'):
        raise ValueError('Alcance inválido')
    with locked(state):
        if run_dir.exists() or (state / run_id).exists():
            raise FileExistsError('El run ya existe; usar resume')
        check_host(root)
        sha = git(root, 'rev-parse', 'HEAD').strip()
        # Rechazar nombres sensibles versionados sin abrir ni copiar su contenido.
        tracked = git(root, 'ls-tree', '-r', '--name-only', '-z', sha).split('\0')
        if any(Path(path).name == '.env' or Path(path).name.startswith('.env.') and
               Path(path).name not in ('.env.example', '.env.sample', '.env.template') or
               Path(path).suffix.lower() in ('.pem', '.key', '.p12', '.pfx') for path in tracked):
            raise ValueError('Snapshot contiene nombres de credenciales; revisar sin leer secretos')
        saved = state / run_id
        saved.mkdir()
        run_dir.mkdir(parents=True)
        data = {'schema': 1, 'run_id': run_id, 'scope': scope, 'sha': sha,
                'created_utc': datetime.now(timezone.utc).isoformat(), 'host': str(root),
                'branch': git(root, 'branch', '--show-current').strip(),
                'reviewers': {}, 'effective_models': {name: 'no verificado' for name in REVIEWERS}}
        # Fallos parciales se conservan; jamás se borran automáticamente para reintentar.
        for name in REVIEWERS:
            path = saved / name
            git(root, '-c', 'core.hooksPath=/dev/null', 'worktree', 'add', '--detach', str(path), sha)
            data['reviewers'][name] = str(path)
        encoded = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
        exclusive(saved / 'run.json', encoded)
        exclusive(run_dir / 'run.json', encoded)
        exclusive(run_dir / 'manifest.md', manifest(data))
        validate(root, run_id, scope)
        return data


def manifest(data):
    return '''---
title: Manifiesto de auditoría %s
status: borrador
tags: [auditoria, run]
updated: %s
description: Snapshot verificable; completar brief separado antes de lanzar revisores.
---

# Snapshot

- SHA: `%s`
- Alcance: `%s`
- Rama: `%s`
- Árbol inicial: limpio; modelos efectivos: no verificados.
- Fecha UTC: `%s`.
- Coordinador: pendiente de registrar; presupuesto y plazo: desconocidos.
- Revisores: Fable claude-fable-5-1, Opus claude-opus-5-5, Codex según sesión.
- Herramientas Claude: Read, Grep, Glob; MCP, shell y edición prohibidos.
- Outline no consultado. Solo evidencia local; no acredita aprobación del diseño.

Antes de delegar, crear `brief.md` nuevo con versiones normativas, alcance incluido
/excluido, preguntas, responsables, decisiones abiertas, hipótesis y límites según
el contrato. Este manifiesto automático no sustituye esas entradas. Compartir el
mismo brief y checks saneados, nunca los informes de primera pasada. Las rutas de
cada checkout y su SHA quedan en `run.json`. No son un sandbox de filesystem.
''' % (data['run_id'], data['created_utc'][:10], data['sha'], data['scope'],
       data['branch'], data['created_utc'])


def validate(repo, run_id, scope):
    root, state, run_dir = locations(repo, run_id)
    local = (run_dir / 'run.json').read_bytes()
    saved = state / run_id
    if local != (saved / 'run.json').read_bytes():
        raise ValueError('Manifiesto divergente de la copia de control')
    data = json.loads(local)
    if data['host'] != str(root) or data['scope'] != scope or data['run_id'] != run_id:
        raise ValueError('Host, alcance o run distintos al original')
    if git(root, 'rev-parse', 'HEAD').strip() != data['sha']:
        raise ValueError('SHA del host cambió')
    check_host(root, run_id)
    for name in REVIEWERS:
        path = Path(data['reviewers'][name])
        if path != saved / name or path.is_symlink():
            raise ValueError('Checkout de revisor no coincide')
        if git(path, 'rev-parse', 'HEAD').strip() != data['sha']:
            raise ValueError('SHA del revisor cambió')
        if git(path, 'branch', '--show-current').strip():
            raise ValueError('Checkout de revisor dejó de estar detached')
        if git(path, 'status', '--porcelain=v1', '--untracked-files=all', '--ignored').strip():
            raise ValueError('Checkout de revisor modificado')
    return data


def resume(repo, run_id, scope):
    _, state, _ = locations(repo, run_id)
    with locked(state):
        return validate(repo, run_id, scope)


def write_report(repo, run_id, scope, filename, text):
    if not REPORT.fullmatch(filename):
        raise ValueError('Nombre de informe inválido; usar revisor-report[-attempt-N].md')
    root, state, run_dir = locations(repo, run_id)
    with locked(state):
        validate(root, run_id, scope)
        exclusive(run_dir / filename, sanitize(text))
        validate(root, run_id, scope)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('start', 'resume', 'validate', 'report'))
    parser.add_argument('run_id')
    parser.add_argument('--scope', choices=('harness', 'producto'), required=True)
    parser.add_argument('--repo', default='.')
    parser.add_argument('--filename', help='Solo report: texto por stdin, sin abrir secretos')
    args = parser.parse_args()
    try:
        if args.action == 'report':
            if not args.filename:
                parser.error('report requiere --filename')
            write_report(args.repo, args.run_id, args.scope, args.filename, sys.stdin.read())
            print('Informe nuevo conservado; salida saneada.')
        else:
            fn = start if args.action == 'start' else resume
            print(json.dumps(fn(args.repo, args.run_id, args.scope), ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError) as error:
        # No imprimir entradas externas, rutas ni posibles credenciales de excepciones OS.
        print('Auditoría rechazada: %s' % (str(error) if isinstance(error, ValueError) else type(error).__name__), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
