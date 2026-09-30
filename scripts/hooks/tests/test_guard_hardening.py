"""Regresiones A3: filesystem real y comandos inspeccionados sin ejecución."""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import guard_edit as edit
import guard_bash as bash
from test_guard_bash import ctx


class Paths(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        (self.root / '.git').mkdir()
        (self.root / 'src').mkdir()
        (self.root / 'src/file.ts').write_text('before')
        (self.root / 'alias').symlink_to(self.root / 'src')

    def check(self, path, env=None):
        return edit.decide({'file_path': str(path), 'content': 'after'}, str(self.root), env or {})[0]

    def test_symlink_to_frozen_existing_and_new(self):
        for name in ('file.ts', 'new.ts'):
            self.assertEqual(self.check(self.root / 'alias' / name), 'deny')

    def test_lexical_protection_of_external_symlink(self):
        with tempfile.TemporaryDirectory() as outside:
            (self.root / 'src/external').symlink_to(outside)
            self.assertEqual(self.check(self.root / 'src/external/new.ts'), 'deny')

    def test_worktree_root_instead_of_main_root(self):
        root = self.root / '.claude/worktrees/test'
        root.mkdir(parents=True)
        (root / '.git').write_text('gitdir: unused')
        self.assertEqual(self.check(root / 'src/new.ts'), 'deny')

    def test_worktree_canon_and_shell_s1(self):
        work = self.root / '.claude/worktrees/canon'
        work.mkdir(parents=True)
        (work / '.git').write_text('gitdir: unused')
        file = work / 'docs/linea-base/Contract_V1.md'
        file.parent.mkdir(parents=True)
        file.write_text('before')
        self.assertEqual(self.check(file), 'deny')
        context = ctx(); context['root'] = str(work)
        self.assertEqual(bash.decide('sed -i "s/before/after/" docs/linea-base/Contract_V1.md', context)[0], 'deny')
        self.assertEqual(file.read_text(), 'before')

    def test_casefold_and_allowlist(self):
        for path in ('SRC/new.ts', 'vitest.config.ts', 'backend/new.ts', '../escape.ts'):
            self.assertEqual(self.check(path), 'deny', path)

    def test_os_requires_explicit_escape_with_warning(self):
        for path in ('scripts/hooks/guard_edit.py', '.claude/settings.json', '.claude/rules/git.md', '.claude/agents/x.md'):
            self.assertEqual(self.check(self.root / path), 'deny')
        out=io.StringIO()
        with contextlib.redirect_stderr(out):
            self.assertEqual(self.check(self.root / '.claude/rules/git.md', {'LIBOX_EDITAR_OS':'1'}), 'allow')
        self.assertIn('LIBOX_EDITAR_OS', out.getvalue())

    def test_malformed_payload_warns_without_echoing(self):
        for script in ('guard_edit.py', 'guard_bash.py'):
            p=subprocess.run([sys.executable, str(Path(edit.__file__).parent / script)],
                             input='{SECRET_SENTINEL', text=True, capture_output=True)
            self.assertEqual(p.returncode, 0)
            self.assertIn('AVISO', p.stderr)
            self.assertNotIn('SECRET_SENTINEL', p.stderr)


class Commands(unittest.TestCase):
    def test_push_global_options_and_full_refs(self):
        for command in ('git -C /repo push origin HEAD:refs/heads/main',
                        'git push origin +HEAD:main', 'git push origin :main',
                        'git push --mirror origin', 'git push origin --all',
                        'git -c x=y push origin refs/heads/main'):
            self.assertEqual(bash.decide(command, ctx())[0], 'deny', command)

    def test_commit_email_override(self):
        self.assertEqual(bash.decide('git -c user.email=bad@example.com commit -m x', ctx())[0], 'deny')
        self.assertEqual(bash.decide('GIT_AUTHOR_EMAIL=bad@example.com git commit -m x', ctx())[0], 'deny')
        self.assertEqual(bash.decide('git commit --author="Bad <bad@example.com>" -m x', ctx())[0], 'deny')

    def test_commit_from_file_and_trailer(self):
        with tempfile.TemporaryDirectory() as tmp:
            f=Path(tmp)/'message'; f.write_text('docs: x\n\nCo-Authored-By: Claude <x@y>')
            self.assertEqual(bash.decide('git commit -F "'+str(f)+'"', ctx())[0], 'deny')
        self.assertEqual(bash.decide('git commit --trailer "Co-Authored-By: Codex <x@y>"',ctx())[0], 'deny')

    def test_chained_add_and_pathspec_verify(self):
        c=ctx(changed=['docs/linea-base/X_V2.md'], verify=(False,'fallos'))
        self.assertEqual(bash.decide('git add . && git commit -m x',c)[0], 'deny')
        self.assertEqual(bash.decide('git commit -m x -- docs/linea-base/X_V2.md',c)[0], 'deny')

    def test_obvious_shell_writes(self):
        for command in ('printf after > src/probe.ts', 'echo x >> vitest.config.ts',
                        'sed -i "s/a/b/" src/probe.ts', 'cp /tmp/probe src/probe.ts',
                        'python3 -c "open(\'src/probe.ts\',\'w\').write(\'x\')"'):
            self.assertEqual(bash.decide(command,ctx())[0], 'deny', command)

    def test_newline_commands_are_checked(self):
        self.assertEqual(bash.decide('git status\ngit push origin main', ctx())[0], 'deny')
        self.assertEqual(bash.decide('git add .\ngit commit -m x',
            ctx(changed=['docs/linea-base/X_V2.md'], verify=(False, 'fallos')))[0], 'deny')

    def test_mixed_newline_separators(self):
        for separator in (' &&\n', ';\n'):
            with self.subTest(separator=separator):
                self.assertEqual(bash.decide('git add .' + separator + 'git commit -m x',
                    ctx(changed=['docs/linea-base/X_V2.md'], verify=(False, 'fallos')))[0], 'deny')
        self.assertEqual(bash.decide('git commit -m "docs: first\nsecond"', ctx())[0], 'allow')

    def test_bare_directory_pathspec(self):
        c = ctx(changed=['docs/linea-base/X_V2.md'], verify=(False, 'fallos'))
        self.assertEqual(bash.decide('git commit -m x docs', c)[0], 'deny')
        self.assertEqual(bash.decide('git commit -m docs', c)[0], 'allow')

    def test_author_email_inline(self):
        self.assertEqual(bash.decide('git -c author.email=bad@example.com commit -m x', ctx())[0], 'deny')

    def test_repository_context_and_author_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
            env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)
            def git(*args):
                return subprocess.run(['git', '-C', tmp, *args], env=env,
                    check=True, capture_output=True, text=True)
            def hook(command):
                return subprocess.run([sys.executable, bash.__file__], env=env,
                    input=json.dumps({'cwd': tmp, 'tool_input': {'command': command}}),
                    capture_output=True, text=True)
            git('init', '-q')
            git('config', 'user.name', 'Fixture')
            git('config', 'user.email', 'fixture@liboxapp.com')
            (root / 'docs/linea-base').mkdir(parents=True)
            (root / 'docs/linea-base/X.md').write_text('fixture')
            (root / 'verify_corpus.py').write_text('print("fallos"); raise SystemExit(1)')
            git('add', '.')
            for command in ('git commit -m x', 'git -C docs commit -m x'):
                with self.subTest(command=command):
                    result = hook(command)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn('B3:', result.stderr)
            git('config', 'author.email', 'outside@example.com')
            result = hook('git commit -m x')
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn('B4:', result.stderr)
            # author.email overrides even an inline user.email.
            result = hook('git -c user.email=inside@liboxapp.com commit -m x')
            self.assertIn('B4:', result.stderr)

    def test_internal_error_warns(self):
        c=ctx(); c['user_email']=lambda: (_ for _ in ()).throw(RuntimeError('SECRET_SENTINEL'))
        out=io.StringIO()
        with contextlib.redirect_stderr(out):
            self.assertEqual(bash.decide('git commit -m x',c)[0],'allow')
        self.assertIn('AVISO',out.getvalue())
        self.assertNotIn('SECRET_SENTINEL',out.getvalue())

if __name__ == '__main__':
    unittest.main()
