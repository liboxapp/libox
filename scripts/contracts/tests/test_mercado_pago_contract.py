"""Payload PSP: estructura documental, no autenticación ni aprobación de pagos."""
import unittest
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

DRAFT = Path(__file__).resolve().parents[3] / 'docs/superpowers/specs/c1-l3-v8/libox_openapi_L3_V8_DRAFT.yaml'


class MercadoPagoContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = yaml.safe_load(DRAFT.read_text())
        cls.op = cls.doc['paths']['/webhooks/psp/{provider}']['post']

    def test_native_notification_identifier_and_resource(self):
        validator = Draft202012Validator(self.doc['components']['schemas']['PspNotification'])
        valid = {'id': 12345, 'type': 'payment', 'data': {'id': '999999999'},
                 'live_mode': False, 'date_created': '2026-09-30T12:00:00Z',
                 'user_id': 44444, 'api_version': 'v1', 'action': 'payment.updated'}
        self.assertTrue(validator.is_valid(valid))
        for invalid in ({**valid, 'id': 'synthetic-event'}, {**valid, 'data': {'id': 123}},
                        {**valid, 'live_mode': 'false'}, {**valid, 'type': 'unknown'}):
            self.assertFalse(validator.is_valid(invalid), invalid)
        self.assertTrue(validator.is_valid({**valid, 'future_vendor_field': True}))

    def test_signature_inputs_are_explicit(self):
        params = {(p['in'], p['name']): p for p in self.op['parameters']}
        for key in (('header', 'x-request-id'), ('query', 'data.id')):
            self.assertTrue(params[key]['required'])
            self.assertEqual(params[key]['schema']['type'], 'string')
        provider = params['path', 'provider']['schema']
        self.assertEqual(provider['enum'], ['mercadopago'])
        signature = self.doc['components']['securitySchemes']['pspSignature']
        self.assertEqual(signature['name'], 'x-signature')
        self.assertEqual(self.op['x-signature-inputs'], ['data.id', 'x-request-id', 'ts'])
        self.assertFalse(self.op['x-signature-covers-body'])
        self.assertIn('503', self.op['responses'])
