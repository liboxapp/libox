"""Decisiones A1–A11 y C1–C4 aprobadas el 2026-09-30, integradas en el borrador.

Comprueban forma del contrato, ejemplos y trazabilidad con las fichas aprobadas y
con los CHECK del SQL canónico. No prueban autorización en ejecución, reglas
patrimoniales ni transiciones reales: siguen siendo implementación humana.
"""
from datetime import datetime
from pathlib import Path
import re
import unittest

import test_openapi_draft

ROOT = Path(__file__).resolve().parents[3]
SPECS = ROOT / 'docs/superpowers/specs/c1-l3-v8'
SQL_V7 = ROOT / 'docs/linea-base/ARTEFACTOS/libox_schema_L3_V7.sql'
UUID = '00000000-0000-4000-8000-000000000001'
MONEY = {'amount': '2500', 'currency': 'PEN'}
A11_REASONS = ['CONTENT_POLICY', 'PRIZE_INELIGIBLE', 'TERMS_INCOMPLETE', 'MEDIA_INVALID',
               'LEGAL_REQUIREMENT', 'OTHER']
CAPABILITY_SCHEMAS = ('CapabilitiesUpdate', 'Capabilities', 'GetCapabilitiesResponse',
                      'UpdateCapabilitiesResponse')


def backticked(text):
    return re.findall(r'`([A-Z_0-9]+)`', text)


def approved_signature_table():
    """Tabla A1 de la ficha aprobada: action_code -> (solicitantes, firmantes)."""
    text = (SPECS / 'decisiones-c1-firmas.md').read_text()
    section = text.split('## A1.', 1)[1].split('## A2.', 1)[0]
    table = {}
    for row in re.findall(r'^\| `([A-Z_0-9]+)` \|([^|]+)\|([^|]+)\|', section, re.M):
        code, requesters, signers = row
        requester_roles = backticked(requesters)
        signer_roles = backticked(signers)
        if 'El otro de los dos' in signers:
            signer_roles = requester_roles + signer_roles
        table[code] = (set(requester_roles), set(signer_roles))
    return table


def approved_pc_stage_table():
    """Tabla A4: etapa -> (roles que verifican o aprueban, código de firma o None)."""
    text = (SPECS / 'decisiones-c1-firmas.md').read_text()
    section = text.split('## A4.', 1)[1]
    table = {}
    for stage, approvers, signature in re.findall(r'^\| (E\d) [^|]+\|([^|]+)\|([^|]+)\|', section, re.M):
        codes = backticked(signature)
        table[stage] = (set(backticked(approvers)), codes[0] if codes else None)
    return table


def canon_check(table, field):
    sql = SQL_V7.read_text()
    block = sql.split('CREATE TABLE ' + table + ' (', 1)[1].split('\n);', 1)[0]
    match = re.search(field + r'\s+VARCHAR\(\d+\)[^,]*?CHECK \(' + field + r' IN \((.*?)\)\)', block, re.S)
    if match is None:
        match = re.search(r'CHECK \(' + field + r' IN \((.*?)\)\)', block, re.S)
    return set(re.findall(r"'([^']+)'", match.group(1)))


def raffle_statuses():
    sql = SQL_V7.read_text()
    block = sql.split('CONSTRAINT ck_raffles_status CHECK (status IN (', 1)[1].split('))', 1)[0]
    return set(re.findall(r"'([^']+)'", block))


class C1Decisions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = test_openapi_draft.DraftContract()
        cls.doc = cls.contract.document()
        cls.schemas = cls.doc['components']['schemas']

    def valid(self, schema, value):
        if isinstance(schema, str):
            schema = self.schemas[schema]
        return self.contract.validator(self.doc, schema).is_valid(value)

    def op(self, path, method='post'):
        return self.doc['paths'][path][method]

    def request_example(self, path, method='post'):
        return self.op(path, method)['requestBody']['content']['application/json']['example']

    def response_example(self, path, method, status):
        return self.op(path, method)['responses'][status]['content']['application/json']['example']

    # Identidad del artefacto ------------------------------------------------

    def test_contract_identity_is_draft3_with_one_new_operation(self):
        self.assertEqual(self.doc['info']['version'], '2.0.0-draft.3')
        operations = self.contract.operations(self.doc)
        self.assertEqual(len(operations), 93, 'Solo decideKyb (A7) se añade a las 92')
        integrated = self.doc['info']['x-c1-decisions-integrated']
        self.assertEqual(integrated, ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9', 'A10', 'A11',
                                      'C1', 'C2', 'C3', 'C4'])
        pending = ' '.join(self.doc['info']['x-c1-pending'])
        for item in ('A8', 'mínimo', 'charge_kind', 'macrozone', 'Cowork'):
            self.assertIn(item, pending)

    # A1–A2 Segunda firma --------------------------------------------------

    def test_signature_policy_matches_approved_a1_table(self):
        approved = approved_signature_table()
        self.assertEqual(len(approved), 11)
        request = self.schemas['SignatureRequest']
        policy = request['x-second-signature-policy']
        self.assertEqual(list(policy), request['properties']['action_code']['enum'])
        for code, (requesters, signers) in approved.items():
            with self.subTest(action_code=code):
                entry = policy[code]
                self.assertEqual(set(entry['requester_subroles']), requesters)
                self.assertEqual(set(entry['signer_subroles']), signers)
                self.assertTrue(entry['signer_must_be_other_person'])
                expected_rule = ('SAME_SUBROLE_ALLOWED' if requesters == signers == {'ADMIN_SUPER'}
                                 else 'DIFFERENT_SUBROLE')
                self.assertEqual(entry['signer_subrole_rule'], expected_rule)
        self.assertEqual(policy['VALUATION_V2_COSIGN']['signer_subroles'], ['ADMIN_MODERATION'])
        self.assertFalse(policy['VALUATION_V2_COSIGN']['grants_write'])

    def test_eligible_signers_are_constrained_by_action_code(self):
        for name in ('SignatureRequest', 'SignatureRequestResponse'):
            schema = self.schemas[name]
            self.assertIn('eligible_signer_subroles', schema['required'], name)
        example = self.response_example('/signature-requests/{id}', 'get', '200')
        self.assertTrue(self.valid('SignatureRequestResponse', example))
        cases = [
            ('SUBROLE_GRANT', ['ADMIN_SUPER'], True),
            ('SUBROLE_GRANT', ['ADMIN_COMPLIANCE'], False),
            ('VALUATION_V2_COSIGN', ['ADMIN_MODERATION'], True),
            ('VALUATION_V2_COSIGN', ['SUPPORT_VALUATOR'], False),
            ('VALUATION_EXCEPTION', ['ADMIN_LEGAL_COMPLIANCE', 'ADMIN_SUPER'], True),
            ('MULTIPLE_OVERRIDE', ['ADMIN_COMPLIANCE'], False),
            ('ATTEST_PC', [], False),
            ('ATTEST_PC', ['ADMIN_SUPER', 'ADMIN_SUPER'], False),
        ]
        for code, signers, ok in cases:
            value = dict(example, action_code=code, eligible_signer_subroles=signers)
            self.assertEqual(self.valid('SignatureRequestResponse', value), ok, (code, signers))

    def test_signature_operation_roles_follow_the_policy(self):
        policy = self.schemas['SignatureRequest']['x-second-signature-policy']
        signers = {r for entry in policy.values() for r in entry['signer_subroles']}
        requesters = {r for entry in policy.values() for r in entry['requester_subroles']}
        self.assertEqual(set(self.op('/signature-requests/{id}/sign')['x-allowed-roles']), signers)
        self.assertEqual(set(self.op('/signature-requests/{id}/cancel')['x-allowed-roles']), requesters)
        for path in ('/signature-requests', '/signature-requests/{id}'):
            self.assertEqual(set(self.op(path, 'get')['x-allowed-roles']), signers | requesters, path)
        self.assertNotIn('ADMIN_FINANCE', signers | requesters)

    # A3 Observación ---------------------------------------------------------

    def test_valuation_observation_limited_to_band_approvers(self):
        transitions = self.op('/valuations/{id}/decisions')['x-outcome-transitions']
        self.assertEqual(set(transitions['OBSERVED']['actor_subroles']),
                         {'SUPPORT_VALUATOR', 'ADMIN_LEGAL_COMPLIANCE'})

    # A4/A8 Etapas P-C -------------------------------------------------------

    def test_pc_stage_approver_matrix_matches_a4_and_checklist_stays_pending(self):
        approved = approved_pc_stage_table()
        self.assertEqual(sorted(approved), ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7'])
        for path, method in (('/raffles/{raffle_ref}/pc-stages', 'get'),
                             ('/raffles/{raffle_ref}/pc-stages/{stage}', 'post')):
            matrix = self.op(path, method)['x-pc-stage-approvers']
            for stage, (roles, signature) in approved.items():
                with self.subTest(path=path, stage=stage):
                    entry = matrix[stage]
                    self.assertEqual(set(entry['verifier_subroles']) | set(entry['approver_subroles']), roles)
                    self.assertEqual(entry['signature_action_code'], signature)
            self.assertTrue(matrix['E5']['automatic'])
            self.assertEqual(matrix['E6']['verifier_subroles'], ['SUPPORT_L2'])
            self.assertEqual({s for s, e in matrix.items() if e['legal_review_pending']}, {'E2', 'E4', 'E7'})
            self.assertIn('A8', self.op(path, method)['x-pending'])
        for path in self.doc['paths']:
            self.assertNotRegex(path, r'pc-stages/\{[^}]+\}/decisions', 'Sin lista A8 no hay decisión de etapa')
        self.assertNotIn('checklist_key', str(self.schemas['PcStageSubmit']))

    def test_submit_kyb_response_uses_domain_states(self):
        expected = canon_check('client_kyb', 'status')
        schema = self.schemas['SubmitKybResponse']
        self.assertEqual(set(schema['properties']['status']['enum']), expected)
        example = self.response_example('/clients/{id}/kyb', 'post', '202')
        self.assertTrue(self.valid(schema, example))
        self.assertFalse(self.valid(schema, dict(example, status='VERIFIED')))

    # A5 Capacidades ---------------------------------------------------------

    def test_capabilities_drop_live_and_separate_pc_categories(self):
        for name in CAPABILITY_SCHEMAS:
            schema = self.schemas[name]
            with self.subTest(schema=name):
                self.assertIn('enabled_categories', schema['required'])
                base = {'enabled_raffle_types': ['T1', 'T8'], 'enabled_categories': ['P_C1', 'P_C2'],
                        'expected_version': 1, 'version': 1, 'trace_id': UUID,
                        'reason': 'Motivo sintético documentado para la operación.'}
                base = {k: v for k, v in base.items() if k in schema['properties']}
                self.assertTrue(self.valid(schema, base))
                for patch in ({'enabled_raffle_types': ['LIVE']}, {'enabled_raffle_types': ['P_C1']},
                              {'enabled_raffle_types': ['T1', 'T1']}, {'enabled_categories': ['LIVE']},
                              {'enabled_categories': ['T8']}, {'enabled_categories': ['P_C1', 'P_C1']},
                              {'enabled_categories': ['P_A']}):
                    self.assertFalse(self.valid(schema, dict(base, **patch)), patch)
                missing = dict(base)
                missing.pop('enabled_categories')
                self.assertFalse(self.valid(schema, missing))

        def walk(value):
            if isinstance(value, dict):
                self.assertNotIn('LIVE', value.get('enum', []) or [])
                for item in value.values():
                    walk(item)
            elif isinstance(value, list):
                for item in value:
                    walk(item)
        walk(self.doc)

    # A6 Rechazos manuales y A11 Motivos ------------------------------------

    def test_manual_rejections_use_canonical_states_only(self):
        statuses = raffle_statuses()
        expected = {
            '/valuations/{id}/decisions': {
                'APPROVED': ('PENDING_VALUATION', 'PENDING_LEGAL', 'VALUATION_APPROVED'),
                'OBSERVED': ('PENDING_VALUATION', 'DRAFT', 'VALUATION_OBSERVED'),
                'REJECTED': ('PENDING_VALUATION', 'REJECTED', 'VALUATION_REJECTED')},
            '/raffles/{raffle_ref}/legal-gate/decisions': {
                'PASSED': ('PENDING_LEGAL', 'PENDING_APPROVAL', 'LEGAL_GATE_PASSED'),
                'OBSERVED': ('PENDING_LEGAL', 'DRAFT', 'LEGAL_GATE_OBSERVED'),
                'REJECTED': ('PENDING_LEGAL', 'REJECTED', 'LEGAL_GATE_REJECTED')},
            '/raffles/{raffle_ref}/moderation/decisions': {
                'APPROVE_SCHEDULED': ('PENDING_APPROVAL', 'SCHEDULED', 'APPROVE_SCHEDULED'),
                'APPROVE_IMMEDIATE': ('PENDING_APPROVAL', 'ACTIVE', 'APPROVE_IMMEDIATE'),
                'REJECT': ('PENDING_APPROVAL', 'REJECTED', 'REJECT')},
        }
        for path, outcomes in expected.items():
            op = self.op(path)
            schema = self.schemas[op['requestBody']['content']['application/json']['schema']['$ref'].split('/')[-1]]
            self.assertEqual(schema['properties']['outcome']['enum'], list(outcomes), path)
            transitions = op['x-outcome-transitions']
            self.assertEqual(list(transitions), list(outcomes))
            for outcome, (source, target, trigger) in outcomes.items():
                entry = transitions[outcome]
                self.assertEqual((entry['from'], entry['to'], entry['trigger']), (source, target, trigger))
                self.assertTrue({source, target} <= statuses, (path, outcome))
        self.assertIn('REJECTED', canon_check('prize_valuations', 'outcome'))
        legal = self.op('/raffles/{raffle_ref}/legal-gate/decisions')
        self.assertIn('[LEGAL→ABOGADO]', legal['x-authorization'])

    def test_rejection_bodies_require_reason_without_approval_fields(self):
        valuation = self.request_example('/valuations/{id}/decisions')
        rejected = {'expected_version': 1, 'outcome': 'REJECTED', 'reason': 'Referencias insuficientes.'}
        self.assertTrue(self.valid('ValuationDecisionCreate', rejected))
        self.assertFalse(self.valid('ValuationDecisionCreate', dict(rejected, approved_value=MONEY)))
        self.assertFalse(self.valid('ValuationDecisionCreate', {'expected_version': 1, 'outcome': 'REJECTED'}))
        self.assertTrue(self.valid('ValuationDecisionCreate', valuation))

        gate = self.request_example('/raffles/{raffle_ref}/legal-gate/decisions')
        for outcome in ('OBSERVED', 'REJECTED'):
            body = {'expected_version': 3, 'outcome': outcome, 'reason': 'Falta el documento habilitante.'}
            self.assertTrue(self.valid('LegalGateDecisionCreate', body), outcome)
            self.assertFalse(self.valid('LegalGateDecisionCreate', dict(body, reason='corto')), outcome)
        passed = dict(gate)
        passed.pop('requirement_results')
        self.assertFalse(self.valid('LegalGateDecisionCreate', passed))

        moderation = self.schemas['ModerationDecisionCreate']
        self.assertEqual(self.schemas['ModerationRejectionReason']['enum'], A11_REASONS)
        reject = {'expected_version': 4, 'outcome': 'REJECT', 'rejection_reason_code': 'OTHER',
                  'reason': 'Texto obligatorio del motivo.'}
        self.assertTrue(self.valid(moderation, reject))
        without_code = dict(reject)
        without_code.pop('rejection_reason_code')
        self.assertFalse(self.valid(moderation, without_code))
        self.assertFalse(self.valid(moderation, dict(reject, rejection_reason_code='SPAM')))
        without_text = dict(reject)
        without_text.pop('reason')
        self.assertFalse(self.valid(moderation, without_text), 'OTHER exige texto')
        approve = self.request_example('/raffles/{raffle_ref}/moderation/decisions')
        self.assertTrue(self.valid(moderation, approve))
        self.assertFalse(self.valid(moderation, dict(approve, rejection_reason_code='CONTENT_POLICY')))

    # A7 KYB -----------------------------------------------------------------

    def test_kyb_decision_by_admin_compliance_with_canonical_outcomes(self):
        op = self.op('/clients/{id}/kyb/decisions')
        self.assertEqual(op['operationId'], 'decideKyb')
        self.assertEqual(op['x-origin'], 'c1-auxiliary')
        self.assertEqual(op['x-allowed-roles'], ['ADMIN_COMPLIANCE'])
        self.assertIn('ADMIN_RISK', self.op('/clients/{id}', 'get')['x-allowed-roles'])
        outcomes = self.schemas['KybDecisionCreate']['properties']['outcome']['enum']
        self.assertEqual(outcomes, ['APPROVED', 'REJECTED'])
        self.assertTrue(set(outcomes) <= canon_check('client_kyb', 'status'))
        self.assertEqual(op['responses']['401'], {'$ref': '#/components/responses/Error401_reauth_required'})
        body = self.request_example('/clients/{id}/kyb/decisions')
        self.assertTrue(self.valid('KybDecisionCreate', body))
        for patch in ({'outcome': 'EXPIRED'}, {'outcome': 'VERIFIED'}, {'reviewer_id': UUID}):
            self.assertFalse(self.valid('KybDecisionCreate', dict(body, **patch)), patch)

    # A9 Atestación ----------------------------------------------------------

    def test_attestation_uses_signature_request_instead_of_second_signer(self):
        request = self.schemas['AttestationRequest']
        self.assertNotIn('second_signer_id', request['properties'])
        example = self.request_example('/rooms/{id}/attest')
        self.assertNotIn('second_signer_id', example)
        self.assertFalse(self.valid(request, dict(example, second_signer_id=UUID)))
        op = self.op('/rooms/{id}/attest')
        self.assertIn('ATTEST_PC', op['x-authorization'])
        self.assertNotIn('ADMIN_FINANCE', op['x-allowed-roles'])
        for name in ('AttestDeliveryResponse', 'AttestationResult'):
            schema = self.schemas[name]
            base = {'attestation_id': UUID, 'gates': self.response_example('/rooms/{id}/attest', 'post', '201')['gates'],
                    'created_at': '2026-09-30T12:00:00-05:00', 'trace_id': UUID,
                    'status': 'PENDING_SECOND_SIGNATURE', 'signature_request_id': UUID}
            base = {k: v for k, v in base.items() if k in schema['properties']}
            self.assertTrue(self.valid(schema, base), name)
            self.assertFalse(self.valid(schema, dict(base, signature_request_id=None)), name)
            self.assertFalse(self.valid(schema, dict(base, status='RECORDED')), name)
            self.assertTrue(self.valid(schema, dict(base, status='RECORDED', signature_request_id=None)), name)

    def test_pc_attestation_requester_matches_signature_policy(self):
        op = self.op('/rooms/{id}/attest')
        policy = op['x-pc-attestation-policy']
        approved = self.schemas['SignatureRequest']['x-second-signature-policy']['ATTEST_PC']
        self.assertEqual(policy['categories'], ['P_C1', 'P_C2'])
        self.assertEqual(policy['requester_subroles'], approved['requester_subroles'])
        self.assertTrue(policy['reject_other_requesters'])
        self.assertTrue(set(policy['requester_subroles']) <= set(op['x-allowed-roles']))
        self.assertNotIn('ADMIN_SUPER', policy['requester_subroles'])

    def test_payout_change_requires_approved_reauth_window(self):
        op = self.op('/clients/{id}/payout', 'put')
        self.assertEqual(op.get('x-reauthentication-max-age-seconds'), 300)
        self.assertEqual(op['responses']['401'],
                         {'$ref': '#/components/responses/Error401_reauth_required'})

    def test_t1_pending_requirements_block_submit_and_publication(self):
        for path in ('/raffles/{raffle_ref}/submit', '/raffles/{raffle_ref}/moderation/decisions'):
            rule = self.op(path)['x-t1-publication-gate']
            self.assertTrue(rule['includes_t8_base_t1'])
            self.assertTrue(rule['requires_approved_minimum'])
            self.assertTrue(rule['requires_approved_prize_terms'])
            self.assertEqual(rule['if_pending'], 'REJECT')
            self.assertNotIn('minimum_value', rule)

    # A10 Reautenticación ----------------------------------------------------

    def test_reauthentication_window_is_five_minutes(self):
        reauth_ref = {'$ref': '#/components/responses/Error401_reauth_required'}
        sensitive = [op for _, _, op in self.contract.operations(self.doc)
                     if op['responses'].get('401') == reauth_ref]
        # Siete auxiliares previas, decideKyb y cambio de cuenta bancaria ya sensible.
        self.assertEqual(len(sensitive), 9)
        for op in sensitive:
            self.assertEqual(op.get('x-reauthentication-max-age-seconds'), 300, op['operationId'])
        op = self.op('/auth/reauthenticate')
        self.assertEqual(op['x-reauthentication-max-age-seconds'], 300)
        self.assertNotIn('sin ratificar', op['description'])
        example = self.response_example('/auth/reauthenticate', 'post', '200')
        delta = (datetime.fromisoformat(example['valid_until'])
                 - datetime.fromisoformat(example['reauthenticated_at']))
        self.assertEqual(delta.total_seconds(), 300)

    # C1–C4 Configuración ----------------------------------------------------

    def draft(self, **patch):
        base = dict(self.request_example('/raffles'))
        base.update(patch)
        return {k: v for k, v in base.items() if v is not None}

    def test_t1_expiry_policy_is_required_but_minimum_stays_pending(self):
        example = self.request_example('/raffles')
        self.assertEqual(example['raffle_type'], 'T1')
        self.assertTrue(self.valid('RaffleDraft', example))
        policy = example['expiry_policy']
        self.assertFalse(self.valid('RaffleDraft', self.draft(expiry_policy=None)))
        self.assertFalse(self.valid('RaffleDraft', self.draft(raffle_type='T3')))
        self.assertTrue(self.valid('RaffleDraft', self.draft(raffle_type='T3', expiry_policy=None)))
        self.assertFalse(self.valid('RaffleDraft', self.draft(raffle_type='T8', base_type='T1', expiry_policy=None)))
        self.assertTrue(self.valid('RaffleDraft', self.draft(raffle_type='T8', base_type='T1')))
        schema = self.schemas['T1ExpiryPolicy']
        self.assertEqual(schema['properties']['on_expiry']['enum'], ['DRAW_IF_MINIMUM_REACHED_ELSE_REFUND'])
        for patch in ({'max_duration_days': 0}, {'on_expiry': 'CANCEL_WITH_REFUND'},
                      {'minimum_sold_bp': 5000}, {'min_tickets': 10}):
            self.assertFalse(self.valid(schema, dict(policy, **patch)), patch)
        self.assertEqual(schema['x-requirement-status'], 'incomplete-pending-threshold')
        for item in ('mínimo', 'premio', 'comprador'):
            self.assertIn(item, ' '.join(schema['x-pending']))
        self.assertFalse([p for p in schema['properties'] if 'min' in p], 'No inventar el mínimo')

    def test_t7_edition_duration_without_overlap_uses_canon_frequencies(self):
        recurrence = self.schemas['EditionRecurrence']
        self.assertEqual(set(recurrence['properties']['frequency']['enum']),
                         canon_check('raffle_recurrences', 'frequency'))
        self.assertIn('edition_duration_minutes', recurrence['required'])
        self.assertIn('x-server-rule', recurrence)
        good = {'frequency': 'WEEKLY', 'interval_count': 1, 'edition_duration_minutes': 1440}
        self.assertTrue(self.valid(recurrence, good))
        for patch in ({'edition_duration_minutes': 0}, {'frequency': 'HOURLY'}, {'interval_count': 0},
                      {'end_at': '2026-10-01T00:00:00Z'}):
            self.assertFalse(self.valid(recurrence, dict(good, **patch)), patch)
        t7 = self.draft(raffle_type='T7', expiry_policy=None)
        self.assertFalse(self.valid('RaffleDraft', t7))
        self.assertTrue(self.valid('RaffleDraft', dict(t7, recurrence=good)))
        self.assertFalse(self.valid('RaffleDraft', self.draft(recurrence=good)), 'recurrence solo en T7')

    def test_organizer_sets_ticket_price_and_only_paid_regime(self):
        draft = self.schemas['RaffleDraft']
        self.assertIn('ticket_price', draft['required'])
        self.assertEqual(draft['properties']['economic_regime']['enum'], ['PAID'])
        for patch in ({'economic_regime': 'FREE_ENTRY'}, {'economic_regime': 'PROMOTIONAL'},
                      {'target_net_amount': MONEY}, {'gross_required': MONEY}, {'libox_fee_amount': MONEY}):
            self.assertFalse(self.valid('RaffleDraft', self.draft(**patch)), patch)
        self.assertTrue(self.valid('RaffleDraft', self.draft(economic_regime='PAID')))
        management = self.schemas['GetRaffleManagementResponse']
        for field in ('economic_regime', 'expiry_policy', 'recurrence'):
            self.assertIn(field, management['required'])
        example = self.response_example('/raffles/{raffle_ref}/management', 'get', '200')
        self.assertTrue(self.valid(management, example))
        self.assertFalse(self.valid(management, dict(example, economic_regime='FREE_ENTRY')))

    def test_declared_costs_use_approved_cost_kinds_only(self):
        cost = self.schemas['DeclaredCost']
        self.assertEqual(cost['properties']['cost_kind']['enum'], ['SHIPPING', 'NOTARY', 'REGISTRY'])
        self.assertEqual(set(cost['properties']['borne_by']['enum']), canon_check('transfer_costs', 'borne_by'))
        valuation = self.request_example('/raffles/{raffle_ref}/prize-valuation')
        self.assertTrue(self.valid('PrizeValuation', valuation))
        good = valuation['declared_costs'][0]
        for patch in ({'cost_kind': 'INSURANCE'}, {'estimated_amount': 2500}, {'borne_by': 'LIBOX'},
                      {'charge_kind': 'MONTHLY'}, {'macrozone': 'LIMA'}):
            self.assertFalse(self.valid(cost, dict(good, **patch)), patch)
        # macrozone ya existía como texto libre en shipping_estimates públicos: sin enum inventado.
        found = []

        def walk(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    if key in ('charge_kind', 'macrozone') and isinstance(item, dict) and 'type' in item:
                        found.append((key, item))
                    walk(item)
            elif isinstance(value, list):
                for item in value:
                    walk(item)
        walk(self.schemas)
        self.assertFalse([key for key, _ in found if key == 'charge_kind'])
        self.assertTrue(found)
        self.assertFalse([item for _, item in found if 'enum' in item])
        pending = ' '.join(self.schemas['PrizeValuation']['x-pending'])
        self.assertIn('charge_kind', pending)
        self.assertIn('macrozone', pending)

    def test_cowork_proposal_is_not_contracted(self):
        text = (SPECS / 'libox_openapi_L3_V8_DRAFT.yaml').read_text()
        for marker in ('VIABILITY', 'fianza', 'bond', 'guarantee_deposit', '12500', '48 h', '1,25'):
            self.assertNotIn(marker, text, marker)


if __name__ == '__main__':
    unittest.main()
