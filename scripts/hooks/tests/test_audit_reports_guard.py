"""E5 conecta el helper a herramientas de edición y escrituras shell visibles."""
import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import guard_edit
import guard_bash


class ReportGuard(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        (self.root / '.git').mkdir()
        self.report = self.root / 'docs/audits/run/codex-report.md'
        self.report.parent.mkdir(parents=True)
        self.report.write_text('original')

    def test_existing_report_cannot_be_overwritten_with_escapes(self):
        env = {'LIBOX_EDITAR_OS': '1', 'LIBOX_DESCONGELAR_SRC': '1', 'LIBOX_PERMITIR_INPLACE': '1'}
        for key in ('file_path', 'notebook_path', 'path'):
            decision, reason = guard_edit.decide({key: str(self.report)}, str(self.root), env)
            self.assertEqual(decision, 'deny')
            self.assertIn('E5', reason)
        self.assertEqual(self.report.read_text(), 'original')

    def test_new_attempt_and_auxiliary_files_allowed(self):
        for filename in ('codex-report-attempt-2.md', 'manifest.md', 'checks.md', 'codex-prompt.md'):
            path = self.report.parent / filename
            if filename != 'codex-report-attempt-2.md':
                path.write_text('before')
            self.assertEqual(guard_edit.decide({'file_path': str(path)}, str(self.root), {})[0], 'allow')

    def test_alias_and_shell_cannot_overwrite_existing_report(self):
        alias = self.root / 'docs/alias.md'
        alias.symlink_to(self.report)
        self.assertEqual(guard_edit.decide({'file_path': str(alias)}, str(self.root), {})[0], 'deny')
        decision, reason = guard_bash.decide('echo replacement > docs/audits/run/codex-report.md',
                                            {'root': str(self.root), 'env': {}})
        self.assertEqual(decision, 'deny')
        self.assertIn('E5', reason)


if __name__ == '__main__':
    unittest.main()
