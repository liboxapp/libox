"""Contrato documental C1: estructura, cobertura, acceso y ejemplos sintéticos."""
from pathlib import Path
import re
import unittest

import yaml
from jsonschema import Draft202012Validator, FormatChecker, RefResolver
from openapi_spec_validator import validate

ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = ROOT / 'docs/superpowers/specs/c1-l3-v8/libox_openapi_L3_V8_DRAFT.yaml'


class DraftContract(unittest.TestCase):
    def document(self):
        self.assertTrue(ARTIFACT.is_file(), 'Falta el borrador OpenAPI completo de C1')
        return yaml.safe_load(ARTIFACT.read_text())

    def operations(self, doc):
        return [(path, method, operation) for path, item in doc['paths'].items()
                for method, operation in item.items() if method in ('get', 'post', 'put', 'patch', 'delete')]

    def validator(self, doc, schema):
        return Draft202012Validator(schema, resolver=RefResolver.from_schema(doc), format_checker=FormatChecker())

    def test_openapi_31_and_unique_coverage(self):
        doc = self.document()
        validate(doc)
        self.assertEqual(doc['openapi'], '3.1.0')
        operations = self.operations(doc)
        self.assertEqual(len(operations), 61)
        ids = [op['operationId'] for _, _, op in operations]
        self.assertEqual(len(set(ids)), 61)
        shapes = [re.sub(r'\{[^}]+\}', '{}', path) for path in doc['paths']]
        self.assertEqual(len(shapes), len(set(shapes)), 'Rutas equivalentes con nombres de parámetro distintos')
        inventory = (ROOT / 'docs/superpowers/specs/c1-l3-v8/contratos.md').read_text()
        expected = {(method.lower(), re.sub(r'\{[^}]+\}', '{}', path))
                    for method, path in re.findall(r'^\| (GET|POST|PUT|PATCH|DELETE) \| `([^`]+)`', inventory, re.M)}
        actual = {(method, re.sub(r'\{[^}]+\}', '{}', path)) for path, method, _ in operations}
        self.assertEqual(actual, expected)

    def test_public_auth_and_webhook_boundaries(self):
        doc = self.document()
        for path in ('/raffles', '/raffles/{raffle_ref}', '/public/draws/{slug}', '/public/draws/{slug}/pool'):
            self.assertEqual(doc['paths'][path]['get']['security'], [])
        webhook = doc['paths']['/webhooks/psp/{provider}']['post']
        self.assertNotIn({'bearerAuth': []}, webhook['security'])
        self.assertIn('pspSignature', str(webhook['security']))
        for path, method, op in self.operations(doc):
            if not op['security']:
                self.assertIn(op['x-access-class'], ('public', 'credential-exchange'))
            else:
                self.assertTrue(op['x-authorization'], (path, method))
            self.assertIn('X-Trace-Id', str(op['parameters']))

    def test_money_mutations_require_client_idempotency(self):
        doc = self.document()
        for path, method in [('/orders','post'),('/settlements/{id}/execute','post'),
                             ('/settlements/batch-execute','post'),('/me/refund-credit/withdrawals','post')]:
            params = doc['paths'][path][method]['parameters']
            self.assertTrue(any(p.get('name')=='Idempotency-Key' and p.get('required') for p in params), path)

    def test_finance_does_not_attest_and_only_finance_executes(self):
        doc = self.document()
        self.assertNotIn('ADMIN_FINANCE', doc['paths']['/rooms/{id}/attest']['post']['x-allowed-roles'])
        self.assertEqual(doc['paths']['/settlements/{id}/execute']['post']['x-allowed-roles'], ['ADMIN_FINANCE'])

    def test_examples_validate_and_requests_are_not_empty(self):
        doc = self.document()
        for path, method, op in self.operations(doc):
            entries = []
            if 'requestBody' in op:
                entries.extend(op['requestBody']['content'].values())
            if method in ('post', 'put', 'patch'):
                self.assertIn('requestBody', op, (path, method))
            success = [r for status, r in op['responses'].items() if str(status).startswith('2')]
            self.assertTrue(success, (path, method))
            for response in success:
                entries.extend(response['content'].values())
            for media in entries:
                self.assertIn('example', media, (path, method))
                with self.subTest(path=path, method=method, example=media['example']):
                    self.validator(doc, media['schema']).validate(media['example'])
            if 'requestBody' in op:
                schema=op['requestBody']['content']['application/json']['schema']
                self.assertFalse(self.validator(doc, schema).is_valid({}), (path, method))

    def test_money_wire_precision_and_invalid_values(self):
        doc = self.document()
        validator = self.validator(doc, doc['components']['schemas']['Money'])
        for amount in ('0','9007199254740993','9223372036854775807'):
            self.assertTrue(validator.is_valid({'amount':amount,'currency':'PEN'}))
        for amount in (500, 0.1, '-1', '01', '1.50', '9223372036854775808',
                       '1\n', '0\n', '9223372036854775807\n', ' 1', '1 ', '1\r', '1\t'):
            self.assertFalse(validator.is_valid({'amount':amount,'currency':'PEN'}), amount)

    def test_existing_pricing_and_protection_contracts_are_preserved(self):
        doc = self.document()
        schemas = doc['components']['schemas']
        self.assertIn('target_net_amount', schemas['PricingRequest']['properties'])
        for name in ('gross_required','libox_fee_amount','client_net_amount','ticket_price',
                     'total_tickets','max_days_to_payout'):
            self.assertIn(name, schemas['PricingResult']['properties'])
        self.assertEqual(schemas['SelfExclusionCreate']['properties']['duration_kind']['enum'],
                         ['D7','D30','D90','PERMANENT'])
        self.assertIn('level', schemas['MarketSuspend']['required'])

    def test_negative_inputs_and_response_invariants(self):
        doc = self.document()
        schemas = doc['components']['schemas']
        order = self.validator(doc, schemas['OrderCreate'])
        good = doc['paths']['/orders']['post']['requestBody']['content']['application/json']['example']
        for patch in ({'quantity':0}, {'quantity':1.5}, {'gross_amount':'1'}, {'user_id':'other'}):
            self.assertFalse(order.is_valid(dict(good, **patch)))
        limit = self.validator(doc, schemas['SpendingLimitChange'])
        self.assertFalse(limit.is_valid({'window_kind':'MONTH', 'amount':{'amount':'100','currency':'PEN'},
                                        'effective_at':'2026-01-01T00:00:00Z'}))
        settlement = self.validator(doc, schemas['Settlement'])
        example = dict(doc['paths']['/settlements/{id}']['get']['responses']['200']['content']['application/json']['example'])
        example.pop('trace_id')
        self.assertFalse(settlement.is_valid(dict(example, hold_reason=None)))
        raffle = self.validator(doc, schemas['RaffleDraft'])
        example = doc['paths']['/raffles']['post']['requestBody']['content']['application/json']['example']
        self.assertFalse(raffle.is_valid(dict(example, raffle_type='T8')))
        self.assertFalse(raffle.is_valid(dict(example, base_type='T1')))

    def test_private_responses_tracing_errors_and_examples(self):
        doc = self.document()
        for path, method, op in self.operations(doc):
            for status, response in op['responses'].items():
                if '$ref' in response:
                    response = doc['components']['responses'][response['$ref'].split('/')[-1]]
                self.assertIn('X-Trace-Id', response['headers'])
                media = response['content']['application/json']
                self.validator(doc, media['schema']).validate(media['example'])
                if str(status).startswith('2'):
                    self.assertIn('trace_id', media['example'])
                else:
                    self.assertIn('trace_id', media['example']['error'])
            if op['x-access-class'] == 'service':
                self.assertEqual(op['security'], [{'serviceAuth':[]}])
        request = doc['components']['schemas']['AttestationRequest']
        self.assertNotIn('gates', request['properties'])
        self.assertNotIn('winner_id', doc['components']['schemas']['DrawCommand']['properties'])

    def test_versioned_commands_expose_resource_versions(self):
        doc = self.document()
        schemas = doc['components']['schemas']
        for name in ('Settlement', 'Alarm', 'Dispute', 'ComplianceCase', 'PayoutStatus',
                     'ReconciliationResolution', 'MarketStatus'):
            self.assertIn('version', schemas[name]['required'], name)
        for path in ('/settlements/{id}', '/alarms', '/compliance/cases'):
            media = doc['paths'][path]['get']['responses']['200']['content']['application/json']
            items = media['example'].get('items', [media['example']])
            self.assertTrue(all('version' in item for item in items), path)

    def test_currency_and_descriptions_are_strict(self):
        doc = self.document()
        validator = self.validator(doc, doc['components']['schemas']['Money'])
        for currency in ('PEN\n', 'PEN ', ' PEN', 'pen', 'PE'):
            self.assertFalse(validator.is_valid({'amount':'1','currency':currency}))
        pool_hash = doc['components']['schemas']['DrawProof']['properties']['pool']['properties']['hash']
        self.assertFalse(self.validator(doc, pool_hash).is_valid('a' * 64 + '\n'))
        code = doc['components']['schemas']['RaffleSummary']['properties']['raffle_code']
        self.assertFalse(self.validator(doc, code).is_valid('LBX-202609-TEST1\n'))
        for name in ('RaffleSummary', 'GetRaffleResponse'):
            prop = doc['components']['schemas'][name]['properties']['claim_sla_days']
            self.assertIsInstance(prop['description'], str)
            self.assertNotIn('15 o 30 según valor aprobado', prop)

    def test_no_legacy_nullable_or_external_refs(self):
        doc=self.document()
        def walk(value):
            if isinstance(value,dict):
                self.assertNotIn('nullable',value)
                if '$ref' in value:
                    self.assertTrue(value['$ref'].startswith('#/components/'))
                for item in value.values(): walk(item)
            elif isinstance(value,list):
                for item in value: walk(item)
        walk(doc)


if __name__ == '__main__':
    unittest.main()
