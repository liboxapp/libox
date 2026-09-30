#!/usr/bin/env python3
"""B1–B4 y escrituras obvias: heurística local, no sandbox. Python 3.9+.

No ejecuta el comando inspeccionado. Ante error propio permite con AVISO.
El CI y ruleset siguen siendo la barrera de integración común.
"""
import json
import os
import re
import shlex
import stat
import subprocess
import sys
import time
from pathlib import Path

from corpus_check import verify_corpus
from guard_paths import warn
import guard_edit

AI_RE = re.compile(r'co-authored-by\s*:.*(?:claude|codex|openai|chatgpt|copilot|gemini|cursor|\bbot\b)|generated\s+with|noreply@anthropic\.com', re.I)
MSG_B1 = 'B1: co-autoría de IA detectada; reescriba el mensaje sin atribución automática.'
MSG_B2 = 'B2: main solo recibe cambios por PR con rebase-and-merge.'
MSG_B3 = 'B3: el corpus tiene fallos; ejecute verify_corpus.py antes del commit.\n{tail}'
MSG_B4 = 'B4: correo fuera de la organización; use git config user.email <tu>@liboxapp.com.'
ORG_DOMAIN = '@liboxapp.com'
CANON_PREFIX = 'docs/linea-base/'
CANON_FILES = {'verify_corpus.py'}
Ctx = dict


def segments(command):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=';&|<>\n')
    lexer.whitespace = ' \t\r'
    lexer.whitespace_split = True
    lexer.commenters = '#'
    current = []
    for token in lexer:
        if re.fullmatch(r'[;&|\n]+', token):
            if current:
                yield current
            current = []
        else:
            current.append(token)
    if current:
        yield current


def git_command(tokens, root):
    """Devuelve verbo, args, cwd y config inline; no interpreta expansiones."""
    try:
        start = next(i for i, t in enumerate(tokens) if os.path.basename(t) == 'git')
    except StopIteration:
        return None
    options = {}
    i = start + 1
    while i < len(tokens):
        t = tokens[i]
        if t in ('-C', '-c', '--git-dir', '--work-tree'):
            value = tokens[i + 1]
            if t == '-C':
                root = os.path.abspath(os.path.join(root, value))
            elif t == '-c':
                k, _, v = value.partition('='); options[k] = v
            else:
                options['unsupported'] = True
            i += 2
        elif t.startswith('-c') and len(t) > 2:
            k, _, v = t[2:].partition('='); options[k] = v; i += 1
        elif t.startswith('-C') and len(t) > 2:
            root = os.path.abspath(os.path.join(root, t[2:])); i += 1
        elif t.startswith('--git-dir=') or t.startswith('--work-tree=') or t.startswith('--config-env'):
            options['unsupported'] = True; i += 1
        elif t.startswith('-'):
            i += 1
        else:
            return t, tokens[i + 1:], root, options, tokens[:start]
    return None


def values(args, long_name, short_name=None):
    for i, token in enumerate(args):
        if token == '--':
            break
        if token == long_name or token == short_name:
            yield args[i + 1]
        elif token.startswith(long_name + '='):
            yield token.split('=', 1)[1]
        elif short_name and token.startswith(short_name) and len(token) > len(short_name):
            yield token[len(short_name):]


def has_pathspec(args):
    """Detecta operandos sin confundir el texto de -m/-F con rutas."""
    takes_value = {'-m', '--message', '-F', '--file', '-C', '--reuse-message',
                   '-c', '--reedit-message', '--author', '--date', '--trailer',
                   '-t', '--template', '--cleanup', '--fixup', '--squash',
                   '--pathspec-from-file'}
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == '--' or arg.startswith('--pathspec-from-file='):
            return True
        if arg == '--pathspec-from-file':
            return True
        if arg in takes_value:
            i += 2
            continue
        if not arg.startswith('-'):
            return True
        i += 1
    return False


def message_file(root, name):
    if name == '-':
        raise ValueError('stdin no verificable')
    path = Path(root) / name
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_size > 65536:
        raise ValueError('mensaje no regular o demasiado grande')
    return path.read_text(encoding='utf-8')


def shell_write(tokens, ctx):
    root = ctx.get('root', '/repo')
    env = ctx.get('env', {})
    targets = []
    for i, token in enumerate(tokens[:-1]):
        if token in ('>', '>>', '>|', '<>'):
            targets.append(tokens[i + 1])
    if not tokens:
        return None
    name = os.path.basename(tokens[0])
    args = [t for t in tokens[1:] if not t.startswith('-')]
    if name in ('cp', 'mv', 'install') and args:
        targets.extend(args[-2:] if name == 'mv' else args[-1:])
    elif name in ('rm', 'touch', 'mkdir', 'truncate', 'tee', 'chmod', 'chown'):
        targets.extend(args)
    elif name == 'sed' and any(t == '-i' or t.startswith('-i') for t in tokens[1:]):
        targets.extend(args[1:])
    # Intérpretes: solo literales visibles. No pretende analizar código arbitrario.
    elif name.startswith(('python', 'node', 'ruby', 'perl')):
        code = ' '.join(tokens[1:])
        if re.search(r'open\(|write|unlink|remove|rename', code):
            targets.extend(re.findall(r'[\'\"]([^\'\"]+)[\'\"]', code))
    for path in targets:
        if path.startswith('&') or path == '/dev/null':
            continue
        kind, reason = guard_edit.decide({'file_path': path}, root, env)
        if kind == 'deny':
            return 'deny', 'Escritura shell detectada (heurística): ' + reason
    return None


def decide(command: str, ctx: Ctx):
    try:
        chained = False
        for tokens in segments(command):
            denial = shell_write(tokens, ctx)
            if denial:
                return denial
            parsed = git_command(tokens, ctx.get('root', os.getcwd()))
            if not parsed:
                continue
            verb, args, root, options, prefix = parsed
            if verb == 'add':
                chained = True
            if verb not in ('commit', 'push'):
                continue
            if options.get('unsupported'):
                return 'deny', 'Opciones de repositorio/configuración no verificables; use git -C y configuración explícita.'
            effective = ctx.get('context_at', lambda _root: ctx)(root)
            if verb == 'push':
                if any(t in ('--all', '--mirror') for t in args):
                    return 'deny', MSG_B2
                for arg in args:
                    dest = arg.lstrip('+').split(':')[-1]
                    if dest in ('main', 'refs/heads/main'):
                        return 'deny', MSG_B2
                # Push sin refspec depende de push.default/remoto: denegar main actual.
                if len([a for a in args if not a.startswith('-')]) < 2:
                    branch = effective.get('branch', lambda: '')()
                    if branch == 'main':
                        return 'deny', MSG_B2
                continue
            if AI_RE.search(' '.join(args)):
                return 'deny', MSG_B1
            for filename in values(args, '--file', '-F'):
                try:
                    content = message_file(root, filename)
                except (ValueError, OSError, UnicodeError):
                    return 'deny', 'B1: no se puede comprobar el archivo del mensaje; use -m o un archivo regular.'
                if AI_RE.search(content):
                    return 'deny', MSG_B1
            for ref in list(values(args, '--reuse-message', '-C')) + list(values(args, '--reedit-message', '-c')):
                if not re.fullmatch(r'[A-Za-z0-9_./~^{}-]+', ref) or ref.startswith('-'):
                    return 'deny', 'B1: referencia de mensaje no verificable.'
                reader = effective.get('commit_message')
                if reader is None or AI_RE.search(reader(ref)):
                    return 'deny', MSG_B1
            email = (effective['user_email']() or '').strip()
            if 'user.email' in options:
                email = options['user.email']
            author_email = effective.get('author_email', lambda: None)()
            if author_email is not None:
                email = author_email.strip()
            if 'author.email' in options:
                email = options['author.email']
            environment = dict(ctx.get('env', {}))
            for item in prefix:
                key, sep, value = item.partition('=')
                if sep:
                    environment[key] = value
            email = environment.get('GIT_AUTHOR_EMAIL', email)
            for author in values(args, '--author'):
                match = re.search(r'<([^<>]+)>', author)
                email = match.group(1) if match else ''
            if not email.casefold().endswith(ORG_DOMAIN):
                return 'deny', MSG_B4
            files = set(effective['staged_files']())
            # Une cambios rastreados y no rastreados ante add/commit -a/pathspec.
            if chained or has_pathspec(args) or any(a in ('--all', '--include', '--only', '--') or re.match(r'^-[^-]*a', a) for a in args):
                files |= set(effective['changed_files']())
            files |= {a for a in args if a.startswith(CANON_PREFIX) or a in CANON_FILES}
            if any(f.startswith(CANON_PREFIX) or f in CANON_FILES for f in files):
                ok, tail = effective['verify_corpus']()
                if not ok:
                    return 'deny', MSG_B3.format(tail=tail)
        return 'allow', ''
    except Exception:
        warn('guard_bash')
        return 'allow', ''


def main():
    try:
        payload = json.load(sys.stdin)
        command = (payload.get('tool_input') or {}).get('command') or ''
        root = payload.get('cwd') or os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd()
        deadline = time.monotonic() + 35

        def context_at(where):
            def git(*args, optional=False):
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError()
                r = subprocess.run(['git', '-C', where, *args], capture_output=True,
                                   timeout=min(3, remaining))
                if optional and r.returncode == 1:
                    return None
                r.check_returncode()
                return r.stdout.decode('utf-8', errors='surrogateescape')
            def verify():
                repository = git('rev-parse', '--show-toplevel').strip()
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError()
                return verify_corpus(repository, timeout=min(20, remaining))
            return {'root': where, 'env': dict(os.environ), 'context_at': context_at,
                    'staged_files': lambda: git('diff', '--cached', '--name-only', '-z').split('\0'),
                    'changed_files': lambda: git('ls-files', '--full-name', '-m', '-o', '--exclude-standard', '-z').split('\0'),
                    'user_email': lambda: (git('config', 'user.email', optional=True) or '').strip(),
                    'author_email': lambda: git('config', '--get', 'author.email', optional=True),
                    'branch': lambda: git('branch', '--show-current').strip(),
                    'commit_message': lambda ref: git('show', '-s', '--format=%B', ref),
                    'verify_corpus': verify}
        kind, reason = decide(command, context_at(root))
        if kind == 'deny':
            print(reason, file=sys.stderr)
            return 2
    except Exception:
        warn('guard_bash: payload o contexto')
    return 0


if __name__ == '__main__':
    sys.exit(main())
