"""Políticas de integración contra objetos y commits Git reales, sin mocks."""
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = pathlib.Path(__file__).resolve().parents[1]
FREEZE = '.claude/rules/src-congelado.md'
CANON = 'docs/linea-base/Contrato con espacios_V1.md'


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.git('init', '-q')
        self.git('config', 'user.name', 'Test')
        self.git('config', 'user.email', 'test@liboxapp.com')
        for path, content in {FREEZE: 'freeze', CANON: 'canon',
                              'src/app/page.tsx': 'page',
                              'package.json': '{}', 'vitest.config.ts': 'config',
                              'README.md': 'readme'}.items():
            self.write(path, content)
        self.base = self.commit()

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root).decode().strip()

    def write(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)

    def commit(self, message='docs: cambio de prueba'):
        self.git('add', '-A')
        self.git('commit', '-qm', message, '--allow-empty')
        return self.git('rev-parse', 'HEAD')

    def check(self, expected, script='check_protected_paths.py', head=None):
        path = SCRIPTS / script
        self.assertTrue(path.is_file(), 'Falta implementar ' + script)
        result = subprocess.run([sys.executable, str(path), '--base', self.base,
                                 '--head', head or self.commit()], cwd=self.root,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def test_docs_change_and_new_version_allowed(self):
        self.write('README.md', 'new')
        self.write('docs/linea-base/Contrato_V2.md', 'new version')
        self.check(0)

    def test_canon_modification_denied(self):
        self.write(CANON, 'changed')
        self.check(1)

    def test_canon_deletion_denied(self):
        (self.root / CANON).unlink()
        self.check(1)

    def test_canon_archived_unchanged_allowed(self):
        content = (self.root / CANON).read_text()
        (self.root / CANON).unlink()
        self.write('docs/archive/Contrato_V1.md', content)
        self.check(0)

    def test_canon_archived_modified_denied(self):
        (self.root / CANON).unlink()
        self.write('docs/archive/Contrato_V1.md', 'changed')
        self.check(1)

    def test_canon_renamed_within_baseline_denied(self):
        (self.root / CANON).rename(self.root / 'docs/linea-base/Otro_V1.md')
        self.check(1)

    def test_canon_mode_change_denied(self):
        (self.root / CANON).chmod(0o755)
        self.check(1)

    def test_canon_with_newline_filename_denied(self):
        path = 'docs/linea-base/Contrato\n_V1.md'
        self.write(path, 'canon')
        self.base = self.commit()
        self.write(path, 'changed')
        result = self.check(1)
        self.assertEqual(len(result.stdout.splitlines()), 1)

    def test_canon_symlink_replacement_denied(self):
        (self.root / CANON).unlink()
        (self.root / CANON).symlink_to('../../README.md')
        self.check(1)

    def test_source_rename_outside_src_denied(self):
        (self.root / 'src/app/page.tsx').rename(self.root / 'page.tsx')
        self.check(1)

    def test_source_change_denied(self):
        self.write('src/app/page.tsx', 'new page')
        self.check(1)

    def test_source_docs_allowed(self):
        self.write('src/domain/CLAUDE.md', 'rules')
        self.check(0)

    def test_scaffold_config_denied(self):
        for path in ['package.json', 'vitest.config.ts', 'tsconfig.json']:
            with self.subTest(path=path):
                self.git('reset', '--hard', self.base)
                self.write(path, 'changed')
                self.check(1)

    def test_deleting_freeze_and_changing_source_denied(self):
        (self.root / FREEZE).unlink()
        self.write('src/app/page.tsx', 'new page')
        self.check(1)

    def test_deleting_freeze_alone_denied(self):
        (self.root / FREEZE).unlink()
        self.check(1)

    def test_editing_freeze_denied(self):
        self.write(FREEZE, 'no freeze')
        self.check(1)

    def test_unfrozen_base_allows_code_but_protects_canon(self):
        (self.root / FREEZE).unlink()
        self.base = self.commit()
        self.write('src/app/page.tsx', 'new page')
        self.check(0)
        self.write(CANON, 'changed')
        self.check(1)

    def test_invalid_revision_fails_closed(self):
        self.check(2, head='0' * 40)

    def test_human_coauthor_allowed(self):
        head = self.commit('docs: prueba\n\nCo-Authored-By: Ana <ana@liboxapp.com>')
        self.check(0, 'check_commit_messages.py', head)

    def test_ai_attribution_denied_without_echoing_message(self):
        for trailer in ['Co-Authored-By: Claude Opus <test@example.com>',
                        'co-authored-by: OpenAI Codex <test@example.com>',
                        'Co-Authored-By: helper[bot] <test@example.com>',
                        'Co-Authored-By: Test <noreply@anthropic.com>',
                        'Generated with Claude Code', 'Generated with Codex']:
            with self.subTest(trailer=trailer):
                self.git('reset', '--hard', self.base)
                head = self.commit('docs: prueba\n\n' + trailer + '\nSECRET_SENTINEL')
                result = self.check(1, 'check_commit_messages.py', head)
                self.assertNotIn('SECRET_SENTINEL', result.stdout + result.stderr)

    def test_commit_policy_invalid_revision_fails_closed(self):
        self.check(2, 'check_commit_messages.py', '0' * 40)


if __name__ == '__main__':
    unittest.main()
