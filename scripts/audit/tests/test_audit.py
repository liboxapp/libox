"""Pruebas de A4 con Git real y datos exclusivamente sintéticos."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts' / 'audit'))


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.DEVNULL).decode().strip()


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / 'repo'
        self.repo.mkdir()
        git(self.repo, 'init', '-q')
        git(self.repo, 'config', 'user.name', 'Prueba')
        git(self.repo, 'config', 'user.email', 'prueba@liboxapp.com')
        (self.repo / 'README.md').write_text('snapshot\n')
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-qm', 'fixture')
        self.assertTrue((ROOT / 'scripts/audit/run.py').exists(), 'Falta gestor reproducible A4')
        import run
        self.run = run

    def test_detached_separate_snapshots_and_resume(self):
        data = self.run.start(self.repo, 'test-harness', 'harness')
        sha = git(self.repo, 'rev-parse', 'HEAD')
        paths = list(data['reviewers'].values())
        self.assertEqual(len(set(paths)), 3)
        for path in paths:
            self.assertEqual(git(path, 'rev-parse', 'HEAD'), sha)
            self.assertEqual(git(path, 'branch', '--show-current'), '')
            self.assertFalse((Path(path) / 'docs/audits/test-harness').exists())
        self.assertEqual(self.run.resume(self.repo, 'test-harness', 'harness'), data)
        with self.assertRaises(ValueError):
            self.run.resume(self.repo, 'test-harness', 'producto')

    def test_dirty_start_and_concurrent_run_refused(self):
        (self.repo / 'dirty.txt').write_text('no perder')
        with self.assertRaises(ValueError):
            self.run.start(self.repo, 'one', 'harness')
        (self.repo / 'dirty.txt').unlink()
        self.run.start(self.repo, 'one', 'harness')
        with self.assertRaises(ValueError):
            self.run.start(self.repo, 'two', 'harness')
        with self.assertRaises((ValueError, FileExistsError)):
            self.run.start(self.repo, 'one', 'harness')
        self.assertFalse((self.repo / 'docs/audits/two').exists())

    def test_host_and_reviewer_drift_detected(self):
        data = self.run.start(self.repo, 'one', 'harness')
        report = self.repo / 'docs/audits/one/fable-report.md'
        report.write_text('evidencia')
        self.run.resume(self.repo, 'one', 'harness')
        (self.repo / 'README.md').write_text('cambio concurrente')
        with self.assertRaises(ValueError):
            self.run.resume(self.repo, 'one', 'harness')
        git(self.repo, 'checkout', '--', 'README.md')
        (Path(data['reviewers']['fable']) / 'README.md').write_text('mutación')
        with self.assertRaises(ValueError):
            self.run.resume(self.repo, 'one', 'harness')
        self.assertEqual(report.read_text(), 'evidencia')

    def test_resume_missing_never_creates(self):
        with self.assertRaises((ValueError, FileNotFoundError)):
            self.run.resume(self.repo, 'missing', 'harness')
        self.assertFalse((self.repo / 'docs/audits/missing').exists())
        with self.assertRaises(ValueError):
            self.run.start(self.repo, '../escape', 'harness')

    def test_host_worktree_and_sha_divergence(self):
        host = Path(self.tmp.name) / 'host'
        git(self.repo, 'worktree', 'add', '--detach', str(host), 'HEAD')
        data = self.run.start(host, 'host-run', 'producto')
        self.assertEqual(data['host'], str(host.resolve()))
        self.run.resume(host, 'host-run', 'producto')
        git(host, 'commit', '--allow-empty', '-qm', 'divergencia')
        with self.assertRaises(ValueError):
            self.run.resume(host, 'host-run', 'producto')

    def test_manifest_tampering_and_symlink_rejected(self):
        self.run.start(self.repo, 'one', 'harness')
        manifest = self.repo / 'docs/audits/one/run.json'
        original = manifest.read_text()
        manifest.write_text(original.replace('harness', 'producto'))
        with self.assertRaises(ValueError):
            self.run.resume(self.repo, 'one', 'producto')
        manifest.write_text(original)
        target = self.repo / 'docs/audits/one/fable-report.md'
        target.symlink_to(self.repo / 'README.md')
        with self.assertRaises(ValueError):
            self.run.resume(self.repo, 'one', 'harness')

    def test_exclusive_sanitized_reports(self):
        self.run.start(self.repo, 'one', 'harness')
        self.run.write_report(self.repo, 'one', 'harness', 'fable-report.md', 'API_KEY=synthetic-123')
        path = self.repo / 'docs/audits/one/fable-report.md'
        self.assertNotIn('synthetic-123', path.read_text())
        with self.assertRaises(FileExistsError):
            self.run.write_report(self.repo, 'one', 'harness', 'fable-report.md', 'overwrite')
        self.run.write_report(self.repo, 'one', 'harness', 'fable-report-attempt-2.md', 'segundo')
        self.assertNotEqual(path.read_text(), 'overwrite')
        with self.assertRaises(ValueError):
            self.run.write_report(self.repo, 'one', 'harness', '../README.md', 'escape')

    def test_attempt_ten_is_preserved(self):
        self.run.start(self.repo, 'one', 'harness')
        self.run.write_report(self.repo, 'one', 'harness', 'fable-report-attempt-10.md', 'décimo')
        self.assertEqual((self.repo / 'docs/audits/one/fable-report-attempt-10.md').read_text(), 'décimo')

    def test_fixture_preparation_does_not_claim_reviewer_result(self):
        for name in ('H-01', 'H-02'):
            fixture = json.loads((Path(__file__).parent / ('fixtures/' + name + '.json')).read_text())
            self.assertTrue(fixture['synthetic'])
            folder = self.repo / name
            folder.mkdir()
            for filename, content in fixture['files'].items():
                (folder / filename).write_text(content)
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-qm', 'fixtures sintéticas')
        data = self.run.start(self.repo, 'fixtures', 'harness')
        for checkout in data['reviewers'].values():
            self.assertIn('PRD_V2.md es vigente', (Path(checkout) / 'H-01/Registro.md').read_text())
            self.assertIn('.NET', (Path(checkout) / 'H-02/regla-local.md').read_text())
        self.assertFalse((self.repo / 'docs/audits/fixtures/fable-report.md').exists())

    def test_tracked_env_refused_without_copying(self):
        (self.repo / '.env').write_text('SYNTHETIC_ONLY=never-copy')
        git(self.repo, 'add', '.env')
        git(self.repo, 'commit', '-qm', 'credencial sintética')
        with self.assertRaises(ValueError):
            self.run.start(self.repo, 'one', 'harness')
        self.assertFalse((self.repo / 'docs/audits/one').exists())

    def test_ignored_reviewer_mutation_refused(self):
        (self.repo / '.gitignore').write_text('ignored.txt\n')
        git(self.repo, 'add', '.gitignore')
        git(self.repo, 'commit', '-qm', 'ignore fixture')
        data = self.run.start(self.repo, 'one', 'harness')
        (Path(data['reviewers']['opus']) / 'ignored.txt').write_text('cambio')
        with self.assertRaises(ValueError):
            self.run.resume(self.repo, 'one', 'harness')

    def test_cli_from_subdirectory(self):
        subdirectory = self.repo / 'nested'
        subdirectory.mkdir()
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/audit/run.py'),
                                 'start', 'cli-run', '--scope', 'harness'],
                                cwd=subdirectory, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['host'], str(self.repo.resolve()))

    def test_cli_failure_reports_nonzero_without_creating_run(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/audit/run.py'),
                                 'resume', 'missing', '--scope', 'harness', '--repo', str(self.repo)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('Auditoría rechazada', result.stderr)
        self.assertFalse((self.repo / 'docs/audits/missing').exists())

    def test_concurrent_creators_preserve_winner(self):
        command = [sys.executable, str(ROOT / 'scripts/audit/run.py'), 'start',
                   'same-id', '--scope', 'harness', '--repo', str(self.repo)]
        processes = [subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
        outputs = [process.communicate(timeout=20) for process in processes]
        self.assertEqual(sorted(process.returncode for process in processes), [0, 1])
        data = self.run.resume(self.repo, 'same-id', 'harness')
        self.assertEqual(len(data['reviewers']), 3)
        winner = outputs[[process.returncode for process in processes].index(0)][0]
        self.assertEqual(json.loads(winner), data)

    def test_sensitive_name_under_unicode_path_refused(self):
        folder = self.repo / 'café'
        folder.mkdir()
        (folder / '.env').write_text('SYNTHETIC_ONLY=never-copy')
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-qm', 'credencial sintética unicode')
        with self.assertRaises(ValueError):
            self.run.start(self.repo, 'one', 'harness')
        self.assertFalse((self.repo / 'docs/audits/one').exists())

    def test_sensitive_name_under_newline_path_refused(self):
        folder = self.repo / 'config\nquoted'
        folder.mkdir()
        (folder / '.env').write_text('SYNTHETIC_ONLY=never-copy')
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-qm', 'credencial sintética newline')
        with self.assertRaises(ValueError):
            self.run.start(self.repo, 'one', 'harness')
        self.assertFalse((self.repo / 'docs/audits/one').exists())


class SanitizerTests(unittest.TestCase):
    def test_synthetic_credentials_removed_preserving_evidence(self):
        path = ROOT / 'scripts/audit/sanitize.py'
        self.assertTrue(path.exists(), 'Falta saneador A4')
        from sanitize import sanitize
        fixture = json.loads((Path(__file__).parent / 'fixtures/credentials.json').read_text())
        result = sanitize(fixture['input'])
        for secret in fixture['secrets']:
            self.assertNotIn(secret, result)
        self.assertIn('exit_code=1', result)
        self.assertIn('docs/README.md:7', result)
        self.assertEqual(sanitize(result), result)

    def test_report_guard(self):
        path = ROOT / 'scripts/hooks/audit_reports.py'
        self.assertTrue(path.exists(), 'Falta predicado E5')
        spec = importlib.util.spec_from_file_location('audit_reports', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / 'docs/audits/run/fable-report-attempt-2.md'
            report.parent.mkdir(parents=True)
            report.write_text('original')
            self.assertTrue(module.is_existing_report(report))
            self.assertFalse(module.is_existing_report(report.with_name('new-report.md')))
            self.assertFalse(module.is_existing_report(Path(tmp) / 'README.md'))

    def test_e5_auxiliary_exceptions_and_symlink_loop(self):
        spec = importlib.util.spec_from_file_location('audit_reports', ROOT / 'scripts/hooks/audit_reports.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'docs/audits/run'
            folder.mkdir(parents=True)
            for filename in ('manifest.md', 'checks.md', 'codex-prompt.md'):
                path = folder / filename
                path.write_text('auxiliar')
                self.assertFalse(module.is_existing_report(path), filename)
            for filename in ('fable-report.md', 'opus-report.md', 'codex-report.md',
                             'synthesis.md', 'fable-report-attempt-10.md', 'brief.md', 'OTHER.MD'):
                path = folder / filename
                path.write_text('original')
                self.assertTrue(module.is_existing_report(path), filename)
            loop = folder / 'loop-report.md'
            loop.symlink_to(loop)
            self.assertTrue(module.is_existing_report(loop))
            alias = Path(tmp) / 'alias.md'
            alias.symlink_to(folder / 'fable-report.md')
            self.assertTrue(module.is_existing_report(alias))

    def test_escaped_quoted_secret_does_not_leave_suffix(self):
        from sanitize import sanitize
        value = 'synthetic-prefix"synthetic-suffix'
        for text in (json.dumps({'password': value}), 'API_KEY=' + json.dumps(value)):
            result = sanitize(text)
            self.assertNotIn('synthetic-prefix', result)
            self.assertNotIn('synthetic-suffix', result)
            self.assertEqual(sanitize(result), result)


if __name__ == '__main__':
    unittest.main()
