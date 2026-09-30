"""Ejecuta el cliente TypeScript generado contra el mock local del mismo YAML."""
import os
from pathlib import Path
import subprocess
import threading
import yaml
from mock_server import ARTIFACT, create_server


def main():
    server = create_server(yaml.safe_load(ARTIFACT.read_text()))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    env = dict(os.environ, LIBOX_CONTRACT_MOCK_URL='http://127.0.0.1:%d/api/v2' % server.server_port)
    try:
        return subprocess.run(['npm', 'run', 'check'], cwd=Path(__file__).parent / 'typescript', env=env).returncode
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


if __name__ == '__main__':
    raise SystemExit(main())
