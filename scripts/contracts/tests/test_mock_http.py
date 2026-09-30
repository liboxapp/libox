"""Prueba HTTP de fixtures generados del contrato; no ejecuta reglas de negocio."""
import json
from pathlib import Path
import re
import sys
import threading
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode

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

    def test_all_examples_round_trip_over_http(self):
        """Inventario L3 y auxiliares C1; el mock no prueba permisos ni seguridad."""
        for path, method, op in self.contract.operations(self.doc):
            url = path
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer synthetic-fixture'}
            query = {}
            for parameter in op['parameters']:
                if not parameter.get('required') and parameter['name'] != 'x-request-id':
                    continue
                schema = parameter['schema']
                if 'enum' in schema:
                    value = schema['enum'][0]
                elif schema.get('type') == 'integer':
                    value = schema.get('minimum', 1)
                elif schema.get('format') == 'uuid':
                    value = '00000000-0000-4000-8000-000000000001'
                elif schema.get('format') == 'date':
                    value = '2026-09-30'
                elif parameter['name'] == 'code':
                    value = 'PE'
                elif parameter['name'] == 'data.id':
                    value = '999999999'
                else:
                    value = 'synthetic-fixture'
                self.contract.validator(self.doc, schema).validate(value)
                if parameter['in'] == 'path':
                    url = url.replace('{' + parameter['name'] + '}', str(value))
                elif parameter['in'] == 'header':
                    headers[parameter['name']] = str(value)
                elif parameter['in'] == 'query':
                    query[parameter['name']] = str(value)
            if query:
                url += '?' + urlencode(query)
            if op['operationId'] == 'receivePspWebhook':
                headers['x-signature'] = 'ts=0,v1=' + '0' * 64  # No firma auténtica.
            self.assertNotIn('{', url)
            body = op.get('requestBody', {}).get('content', {}).get('application/json', {}).get('example')
            data = json.dumps(body).encode() if body is not None else None
            request = Request(self.base + url, data=data, method=method.upper(),
                              headers=headers)
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
