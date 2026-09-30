"""Mock local generado del OpenAPI: solo fixtures, sin auth ni lógica de dominio.

No usar como backend ni exponer en red. Cada llamada devuelve el ejemplo estático
correspondiente. Solo comprueba el cuerpo JSON; no valida permisos ni PSP.
"""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
from uuid import uuid4

import yaml
from jsonschema import Draft202012Validator, FormatChecker, RefResolver

ARTIFACT = Path(__file__).resolve().parents[2] / 'docs/superpowers/specs/c1-l3-v8/libox_openapi_L3_V8_DRAFT.yaml'


def create_server(document, port=0):
    routes = []
    for path, item in sorted(document['paths'].items(), key=lambda entry: entry[0].count('{')):
        pattern = '^/api/v2' + re.sub(r'\\\{[^}]+\\\}', '[^/]+', re.escape(path)) + '$'
        for method, op in item.items():
            if method in ('get', 'post', 'put', 'patch', 'delete'):
                routes.append((method.upper(), re.compile(pattern), op))

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass  # Los cuerpos pueden contener credenciales sintéticas; no registrar solicitudes.

        def send_json(self, status, body):
            data = json.dumps(body).encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Libox-Mock', 'fixtures-only')
            self.send_header('X-Trace-Id', body.get('trace_id') or body['error']['trace_id'])
            self.end_headers()
            self.wfile.write(data)

        def fail(self, status, code):
            self.send_json(status, {'error': {'code': code, 'message': 'Solicitud no válida para el mock.',
                                              'trace_id': str(uuid4())}})

        def handle_fixture(self):
            route = next((op for method, pattern, op in routes
                          if method == self.command and pattern.fullmatch(self.path.split('?')[0])), None)
            if route is None:
                self.fail(404, 'ERR_RESOURCE_NOT_FOUND')
                return
            if 'requestBody' in route:
                try:
                    size = int(self.headers.get('Content-Length', '0'))
                    if size < 1 or size > 1024 * 1024:
                        raise ValueError('body length')
                    body = json.loads(self.rfile.read(size))
                    schema = route['requestBody']['content']['application/json']['schema']
                    validator = Draft202012Validator(schema, resolver=RefResolver.from_schema(document),
                                                     format_checker=FormatChecker())
                    if not validator.is_valid(body):
                        raise ValueError('invalid schema')
                except (ValueError, UnicodeError):
                    self.fail(400, 'ERR_REQUEST_INVALID')
                    return
            status, response = next((status, value) for status, value in route['responses'].items()
                                    if str(status).startswith('2'))
            self.send_json(int(status), response['content']['application/json']['example'])

        do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = handle_fixture

    return ThreadingHTTPServer(('127.0.0.1', port), Handler)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=0)
    args = parser.parse_args()
    server = create_server(yaml.safe_load(ARTIFACT.read_text()), args.port)
    print('Mock de fixtures únicamente: http://127.0.0.1:%d/api/v2' % server.server_port, flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
