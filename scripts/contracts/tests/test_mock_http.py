"""Prueba HTTP de fixtures generados del contrato; no ejecuta reglas de negocio."""
import json
from pathlib import Path
import re
import sys
import threading
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mock_server import create_server
import test_openapi_draft


class MockHttpContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = test_openapi_draft.DraftContract()
        cls.doc = cls.contract.document()
        cls.server = create_server(cls.doc)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = 'http://127.0.0.1:%d/api/v2' % cls.server.server_port

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def test_all_61_examples_round_trip_over_http(self):
        for path, method, op in self.contract.operations(self.doc):
            url = re.sub(r'\{[^}]+\}', 'fixture', path)
            body = op.get('requestBody', {}).get('content', {}).get('application/json', {}).get('example')
            data = json.dumps(body).encode() if body is not None else None
            request = Request(self.base + url, data=data, method=method.upper(),
                              headers={'Content-Type':'application/json'})
            with self.subTest(operation=op['operationId']), urlopen(request, timeout=5) as response:
                schema = op['responses'][str(response.status)]['content']['application/json']['schema']
                actual = json.load(response)
                self.contract.validator(self.doc, schema).validate(actual)
                self.assertEqual(response.headers['X-Libox-Mock'], 'fixtures-only')
                self.assertEqual(response.headers['Cache-Control'], 'no-store')
                self.assertEqual(response.headers['X-Trace-Id'], actual['trace_id'])

    def test_invalid_body_and_unknown_route_do_not_succeed(self):
        for path, body, status in [('/orders', {}, 400), ('/not-a-route', None, 404)]:
            request = Request(self.base + path, data=json.dumps(body).encode(),
                              method='POST', headers={'Content-Type':'application/json'})
            with self.assertRaises(HTTPError) as raised:
                urlopen(request, timeout=5)
            self.assertEqual(raised.exception.code, status)
            raised.exception.close()
