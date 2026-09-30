"""No dejar contenedores propios cuando falla el arranque o la espera."""
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pgdocker


class ContainerCleanup(unittest.TestCase):
    def test_startup_timeout_removes_only_its_container(self):
        pg = pgdocker.PgContainer(tag='failure-test')
        calls = []

        def command(argv, **kwargs):
            calls.append(argv)
            if argv[:2] == ['docker', 'run']:
                raise subprocess.TimeoutExpired(argv, 120)
            return subprocess.CompletedProcess(argv, 0, b'', b'')

        with patch.object(pgdocker, 'run_command', side_effect=command):
            with self.assertRaises(subprocess.TimeoutExpired):
                with pg:
                    self.fail('No debe entrar')
        self.assertEqual(calls[-1], ['docker', 'rm', '--force', pg.name])
        self.assertFalse(pg.started)

    def test_readiness_failure_removes_container(self):
        pg = pgdocker.PgContainer(tag='readiness-test')

        def fail_start():
            pg.started = True
            raise pgdocker.DockerUnavailable('no quedó listo')

        with patch.object(pg, 'start', side_effect=fail_start):
            with patch.object(pgdocker, 'run_command', return_value=subprocess.CompletedProcess([], 0, b'', b'')) as run:
                with self.assertRaises(pgdocker.DockerUnavailable):
                    with pg:
                        self.fail('No debe entrar')
                run.assert_called_once_with(['docker', 'rm', '--force', pg.name], timeout=60)
        self.assertFalse(pg.started)
