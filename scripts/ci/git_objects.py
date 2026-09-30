"""Lectura de objetos Git sin checkout ni ejecución de contenido del PR."""
import argparse
import re
import subprocess


def git(*args):
    return subprocess.check_output(['git', *args], stderr=subprocess.PIPE)


def revisions():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', required=True)
    parser.add_argument('--head', required=True)
    args = parser.parse_args()
    for revision in (args.base, args.head):
        if not re.fullmatch(r'[0-9a-fA-F]{40}', revision):
            raise ValueError('Se requiere un SHA completo')
        git('cat-file', '-e', revision + '^{commit}')
    return args.base, args.head


def tree(revision):
    entries = {}
    for record in git('ls-tree', '-rz', revision).split(b'\0'):
        if record:
            metadata, path = record.split(b'\t', 1)
            mode, kind, oid = metadata.split()
            entries[path.decode('utf-8', errors='surrogateescape')] = (mode, kind, oid)
    return entries
