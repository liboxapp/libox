"""Contratos auxiliares de C1: subconjunto L3, lecturas versionadas, MFA, subidas y firmas.

Validan estructura y ejemplos del borrador. No prueban permisos, seguridad, firma PSP
ni reglas de dominio; los ejemplos son sintéticos.
"""
from pathlib import Path
import re
import unittest

import test_openapi_draft

ROOT = Path(__file__).resolve().parents[3]
INVENTORY_DOC = ROOT / 'docs/superpowers/specs/c1-l3-v8/contratos.md'

VERSIONED_READS = {
    ('get', '/clients/{id}'): 'getClient',
    ('get', '/clients/{id}/payout'): 'getPayout',
    ('get', '/clients/{id}/capabilities'): 'getCapabilities',
    ('get', '/raffles/{raffle_ref}/management'): 'getRaffleManagement',
    ('get', '/valuations/{id}'): 'getValuation',
    ('get', '/raffles/{raffle_ref}/pc-stages'): 'listPcStages',
    ('get', '/disputes/{id}'): 'getDispute',
    ('get', '/markets/{code}/config/versions/{version}'): 'getMarketConfigVersion',
    ('get', '/platform/capabilities'): 'listPlatformCapabilities',
}
AUTH_OPS = {
    ('get', '/auth/mfa/factors'): 'listMfaFactors',
    ('post', '/auth/mfa/factors'): 'enrollMfaFactor',
    ('post', '/auth/mfa/factors/{id}/verify'): 'verifyMfaFactor',
    ('post', '/auth/mfa/factors/{id}/revoke'): 'revokeMfaFactor',
    ('post', '/auth/mfa/challenge'): 'challengeMfa',
    ('post', '/auth/reauthenticate'): 'reauthenticate',
    ('post', '/auth/sessions/revoke'): 'revokeSessions',
    ('post', '/auth/recovery'): 'requestRecovery',
    ('post', '/auth/recovery/complete'): 'completeRecovery',
    ('post', '/auth/password/change'): 'changePassword',
    ('post', '/internal-users/{id}/mfa-reset'): 'requestInternalMfaReset',
}
UPLOAD_OPS = {
    ('post', '/uploads'): 'createUpload',
    ('post', '/uploads/{id}/complete'): 'completeUpload',
    ('get', '/uploads/{id}'): 'getUpload',
    ('get', '/evidence/{id}/download-url'): 'getEvidenceDownloadUrl',
}
DECISION_OPS = {
    ('post', '/valuations/{id}/decisions'): 'decideValuation',
    ('post', '/raffles/{raffle_ref}/legal-gate/decisions'): 'decideLegalGate',
    ('post', '/raffles/{raffle_ref}/moderation/decisions'): 'decideModeration',
    ('post', '/clients/{id}/kyb/decisions'): 'decideKyb',
}
SIGNATURE_OPS = {
    ('get', '/signature-requests'): 'listSignatureRequests',
    ('get', '/signature-requests/{id}'): 'getSignatureRequest',
    ('post', '/signature-requests/{id}/sign'): 'signSignatureRequest',
    ('post', '/signature-requests/{id}/cancel'): 'cancelSignatureRequest',
}
AUXILIARY = {}
for group in (VERSIONED_READS, AUTH_OPS, UPLOAD_OPS, DECISION_OPS, SIGNATURE_OPS):
    AUXILIARY.update(group)

SENSITIVE = ('enrollMfaFactor', 'revokeMfaFactor', 'requestInternalMfaReset', 'decideValuation',
             'decideLegalGate', 'decideModeration', 'decideKyb', 'signSignatureRequest')
UPLOAD_PURPOSES = ['ROOM_EVIDENCE', 'DISPUTE_EVIDENCE', 'KYB_DOCUMENT', 'VALUATION_EVIDENCE',
                   'MARKET_REFERENCE_CAPTURE', 'PC_STAGE_DOCUMENT', 'LEGAL_GATE_DOCUMENT']
ACTION_CODES = ['VALUATION_V2_COSIGN', 'VALUATION_V4', 'VALUATION_EXCEPTION', 'PC_STAGE_E3',
                'PC_STAGE_E7', 'ATTEST_PC', 'CAPABILITY_PLATFORM_DISABLE', 'MARKET_RESUME',
                'MULTIPLE_OVERRIDE', 'SUBROLE_GRANT', 'MFA_RESET_INTERNAL']
NEW_ERROR_CODES = ('ERR_AUTH_REAUTH_REQUIRED', 'ERR_EVIDENCE_NOT_ACCEPTED')
UUID = '00000000-0000-4000-8000-000000000001'


def shape(path):
    return re.sub(r'\{[^}]+\}', '{}', path)


class AuxiliaryContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = test_openapi_draft.DraftContract()
        cls.doc = cls.contract.document()
        cls.schemas = cls.doc['components']['schemas']

    def op(self, key):
        method, path = key
        return self.doc['paths'][path][method]

    def by_id(self, operation_id):
        key = next(k for k, v in AUXILIARY.items() if v == operation_id)
        return self.op(key)

    def resolve(self, schema):
        while '$ref' in schema:
            schema = self.doc['components'][schema['$ref'].split('/')[-2]][schema['$ref'].split('/')[-1]]
        return schema

    def response(self, op, status):
        response = op['responses'][status]
        if '$ref' in response:
            response = self.doc['components']['responses'][response['$ref'].split('/')[-1]]
        return response['content']['application/json']

    def request(self, op):
        return op['requestBody']['content']['application/json']

    def valid(self, schema, value):
        return self.contract.validator(self.doc, schema).is_valid(value)

    def test_l3_subset_is_exactly_the_61_inventoried_operations(self):
        inventory = {(m.lower(), shape(p)) for m, p in re.findall(
            r'^\| (GET|POST|PUT|PATCH|DELETE) \| `([^`]+)`', INVENTORY_DOC.read_text(), re.M)}
        l3, aux, ids = set(), set(), []
        for path, method, op in self.contract.operations(self.doc):
            ids.append(op['operationId'])
            origin = op.get('x-origin')
            self.assertIn(origin, ('l3-inventory', 'c1-auxiliary'), op['operationId'])
            (l3 if origin == 'l3-inventory' else aux).add((method, shape(path)))
        self.assertEqual(len(inventory), 61)
        self.assertEqual(l3, inventory)
        self.assertEqual(aux, {(m, shape(p)) for m, p in AUXILIARY})
        self.assertFalse(l3 & aux)
        self.assertEqual(len(ids), len(set(ids)), 'operationId duplicado')
        for key, operation_id in AUXILIARY.items():
            self.assertEqual(self.op(key)['operationId'], operation_id, key)

    def test_path_parameter_names_are_normalized(self):
        names = {}
        for path, item in self.doc['paths'].items():
            segments = path.strip('/').split('/')
            for index, segment in enumerate(segments):
                if segment.startswith('{'):
                    names.setdefault((segments[0], index), set()).add(segment)
            template = set(re.findall(r'\{([^}]+)\}', path))
            for method, op in item.items():
                declared = {p['name'] for p in op.get('parameters', []) if p.get('in') == 'path'}
                self.assertEqual(declared, template, (path, method))
        for key, found in names.items():
            self.assertEqual(len(found), 1, (key, found))

    def test_auxiliary_operations_are_proposed_json_and_internal_sessions_declared(self):
        for key, operation_id in AUXILIARY.items():
            op = self.op(key)
            self.assertEqual(op['x-origin'], 'c1-auxiliary', operation_id)
            self.assertEqual(op['x-authorization-status'], 'proposed', operation_id)
            if 'requestBody' in op:
                self.assertEqual(set(op['requestBody']['content']), {'application/json'})
            for status, response in op['responses'].items():
                if '$ref' not in response:
                    self.assertEqual(set(response['content']), {'application/json'}, (operation_id, status))
            if any(r.startswith(('ADMIN_', 'SUPPORT_')) for r in op['x-allowed-roles']):
                self.assertIn('aal2', op['x-internal-session'], operation_id)

    def test_versioned_reads_return_resource_versions(self):
        for key, operation_id in VERSIONED_READS.items():
            op = self.op(key)
            self.assertNotIn('requestBody', op)
            media = self.response(op, '200')
            schema = self.resolve(media['schema'])
            if 'items' in schema['properties']:
                item = self.resolve(schema['properties']['items']['items'])
                self.assertIn('version', item['required'], operation_id)
                self.assertTrue(media['example']['items'], operation_id)
                self.assertTrue(all('version' in i for i in media['example']['items']), operation_id)
            else:
                self.assertIn('version', schema['required'], operation_id)
                self.assertIn('version', media['example'], operation_id)
            for param in op['parameters']:
                if param['in'] == 'path' and param['name'] == 'code':
                    self.assertIn('pattern', param['schema'])
                elif param['in'] == 'path' and param['name'] == 'version':
                    self.assertEqual(param['schema']['type'], 'integer')
                elif param['in'] == 'path':
                    self.assertEqual(param['schema'].get('format'), 'uuid', (operation_id, param['name']))

    def test_mfa_reauthentication_and_recovery_contracts(self):
        code = self.schemas['MfaCode']
        self.assertTrue(self.valid(code, {'code': '123456'}))
        for bad in ('12345', '1234567', '12a456', '123456\n', 123456):
            self.assertFalse(self.valid(code, {'code': bad}), bad)
        reauth = self.schemas['Reauthentication']
        self.assertTrue(self.valid(reauth, {'method': 'TOTP', 'factor_id': UUID, 'code': '123456'}))
        self.assertTrue(self.valid(reauth, {'method': 'PASSWORD', 'password': 'synthetic-not-a-secret-123'}))
        self.assertFalse(self.valid(reauth, {'method': 'PASSWORD'}))
        self.assertFalse(self.valid(reauth, {'method': 'TOTP', 'factor_id': UUID, 'code': '123456',
                                             'password': 'x'}))
        for operation_id in ('verifyMfaFactor', 'challengeMfa'):
            session = self.resolve(self.response(self.by_id(operation_id), '200')['schema'])
            self.assertEqual(session['properties']['aal']['enum'], ['aal2'])
        for operation_id in ('requestRecovery', 'completeRecovery'):
            op = self.by_id(operation_id)
            self.assertEqual(op['security'], [])
            self.assertEqual(op['x-access-class'], 'credential-exchange')
        generic = self.resolve(self.response(self.by_id('requestRecovery'), '202')['schema'])
        self.assertEqual(set(generic['properties']), {'message', 'trace_id'})
        reset = self.resolve(self.response(self.by_id('completeRecovery'), '200')['schema'])
        self.assertFalse({'access_token', 'refresh_token'} & set(reset['properties']))
        for operation_id in ('enrollMfaFactor', 'verifyMfaFactor', 'revokeMfaFactor', 'challengeMfa',
                             'reauthenticate', 'revokeSessions', 'changePassword', 'listMfaFactors'):
            self.assertEqual(self.by_id(operation_id)['security'], [{'bearerAuth': []}], operation_id)
        mfa_reset = self.by_id('requestInternalMfaReset')
        self.assertEqual(mfa_reset['x-allowed-roles'], ['ADMIN_SUPER'])
        receipt = self.resolve(self.response(mfa_reset, '202')['schema'])
        self.assertEqual(receipt['properties']['action_code']['enum'], ['MFA_RESET_INTERNAL'])
        for operation_id in SENSITIVE:
            codes = self.response(self.by_id(operation_id), '401')['schema']['properties']['error']
            self.assertIn('ERR_AUTH_REAUTH_REQUIRED', codes['properties']['code']['enum'], operation_id)

    def test_upload_lifecycle_contract(self):
        create = self.by_id('createUpload')
        self.assertTrue(any(p['name'] == 'Idempotency-Key' and p.get('required') for p in create['parameters']))
        schema = self.schemas['UploadCreate']
        self.assertEqual(schema['properties']['purpose']['enum'], UPLOAD_PURPOSES)
        good = self.request(create)['example']
        self.assertTrue(self.valid(schema, good))
        for patch in ({'purpose': 'OTHER'}, {'sha256': 'A' * 64}, {'sha256': 'a' * 63},
                      {'size_bytes': 0}, {'object_key': 'raw/key'}, {'content_type': 'text'}):
            self.assertFalse(self.valid(schema, dict(good, **patch)), patch)
        missing = dict(good)
        missing.pop('target_id')
        self.assertFalse(self.valid(schema, missing))
        view = self.schemas['UploadView']
        self.assertEqual(view['properties']['status']['enum'],
                         ['PENDING_UPLOAD', 'QUARANTINED', 'ACCEPTED', 'REJECTED'])
        self.assertIn(None, view['properties']['rejection_reason']['enum'])
        self.assertIn('expected_version', self.schemas['UploadComplete']['required'])
        download = self.resolve(self.response(self.by_id('getEvidenceDownloadUrl'), '200')['schema'])
        self.assertIn('expires_at', download['required'])

    def test_privileged_decisions_reject_signers_and_computed_fields(self):
        forbidden = {'second_signer_id', 'signer_id', 'band', 'deviation_bp', 'median_reference',
                     'libox_fee_amount', 'gross_required', 'collection_multiple_bp'}
        for key, operation_id in AUXILIARY.items():
            op = self.op(key)
            if 'requestBody' in op:
                props = set(self.resolve(self.request(op)['schema']).get('properties', {}))
                self.assertFalse(forbidden & props, operation_id)
        valuation = self.schemas['ValuationDecisionCreate']
        # Rechazos manuales de A6 y REJECT de A11: detalle en test_c1_decisions.
        self.assertEqual(valuation['properties']['outcome']['enum'], ['APPROVED', 'OBSERVED', 'REJECTED'])
        approved = self.request(self.by_id('decideValuation'))['example']
        self.assertTrue(self.valid(valuation, approved))
        without_value = dict(approved)
        without_value.pop('approved_value')
        self.assertFalse(self.valid(valuation, without_value))
        self.assertFalse(self.valid(valuation, dict(approved, outcome='OBSERVED')))
        self.assertFalse(self.valid(valuation, dict(approved, outcome='REJECTED')))
        self.assertFalse(self.valid(valuation, dict(approved, deviation_bp=100)))
        self.assertEqual(self.schemas['LegalGateDecisionCreate']['properties']['outcome']['enum'],
                         ['PASSED', 'OBSERVED', 'REJECTED'])
        self.assertEqual(self.schemas['ModerationDecisionCreate']['properties']['outcome']['enum'],
                         ['APPROVE_SCHEDULED', 'APPROVE_IMMEDIATE', 'REJECT'])
        self.assertEqual(self.by_id('decideKyb')['x-allowed-roles'], ['ADMIN_COMPLIANCE'])
        self.assertEqual(set(self.by_id('decideValuation')['x-allowed-roles']),
                         {'SUPPORT_VALUATOR', 'ADMIN_LEGAL_COMPLIANCE'})
        self.assertEqual(self.by_id('decideLegalGate')['x-allowed-roles'], ['ADMIN_LEGAL_COMPLIANCE'])
        self.assertEqual(self.by_id('decideModeration')['x-allowed-roles'], ['ADMIN_MODERATION'])
        receipt = self.schemas['DecisionReceipt']
        pending = {'decision_id': UUID, 'status': 'PENDING_SECOND_SIGNATURE', 'signature_request_id': None,
                   'subject_version': 2}
        self.assertFalse(self.valid(receipt, pending))
        self.assertTrue(self.valid(receipt, dict(pending, signature_request_id=UUID)))
        self.assertFalse(self.valid(receipt, dict(pending, status='RECORDED', signature_request_id=UUID)))

    def test_signature_requests_are_separate_resources(self):
        request = self.schemas['SignatureRequest']
        self.assertEqual(request['properties']['action_code']['enum'], ACTION_CODES)
        self.assertTrue({'version', 'subject_version', 'requested_by'} <= set(request['required']))
        sign = self.schemas['SignatureDecision']
        good = self.request(self.by_id('signSignatureRequest'))['example']
        self.assertEqual(sign['properties']['decision']['enum'], ['SIGN', 'DECLINE'])
        for extra in ({'signer_id': UUID}, {'second_signer_id': UUID}, {'decision': 'APPROVE'}):
            self.assertFalse(self.valid(sign, dict(good, **extra)), extra)
        cancel = self.request(self.by_id('cancelSignatureRequest'))['schema']
        self.assertEqual(cancel, {'$ref': '#/components/schemas/ActionRequest'})

    def test_existing_contract_corrections_follow_the_canon(self):
        for name in ('RaffleDraft', 'RaffleUpdate'):
            self.assertEqual(self.schemas[name]['properties']['title']['maxLength'], 140, name)
        for name in ('CapabilitiesUpdate', 'MarketConfigUpdate'):
            self.assertEqual(self.schemas[name]['properties']['reason']['minLength'], 20, name)

    def test_auxiliary_schemas_are_closed_and_errors_declared(self):
        def walk(value, where):
            if isinstance(value, dict):
                kind = value.get('type')
                if kind == 'object' or (isinstance(kind, list) and 'object' in kind):
                    self.assertIn('properties', value, where)
                    self.assertIs(value.get('additionalProperties'), False, where)
                for item in value.values():
                    walk(item, where)
            elif isinstance(value, list):
                for item in value:
                    walk(item, where)
        enum = set(self.schemas['Error']['properties']['error']['properties']['code']['enum'])
        self.assertTrue(set(NEW_ERROR_CODES) <= enum)
        for key, operation_id in AUXILIARY.items():
            op = self.op(key)
            for status, response in op['responses'].items():
                media = self.response(op, status)
                walk(self.resolve(media['schema']), (operation_id, status))
                if not str(status).startswith('2'):
                    codes = set(media['schema']['properties']['error']['properties']['code']['enum'])
                    self.assertTrue(codes <= enum, (operation_id, status, codes - enum))
            if 'requestBody' in op:
                walk(self.resolve(self.request(op)['schema']), (operation_id, 'request'))
        for name in ('Reauthentication', 'PasswordReauthentication', 'TotpReauthentication',
                     'UploadView', 'SignatureRequest', 'PlatformCapability', 'PcStageView', 'MfaFactor'):
            walk(self.schemas[name], name)


if __name__ == '__main__':
    unittest.main()
