"""Los estados expuestos de un recurso coinciden con su vocabulario canónico."""
from pathlib import Path
import re
import unittest
import test_openapi_draft

ROOT = Path(__file__).resolve().parents[3]


class CanonicalStates(unittest.TestCase):
    def test_status_vocabulary_matches_existing_schema(self):
        doc = test_openapi_draft.DraftContract().document()
        sql = (ROOT / 'docs/linea-base/ARTEFACTOS/libox_schema_L3_V7.sql').read_text()
        groups = [
            ('clients', 'status', ['Client', 'GetClientResponse', 'CreateClientResponse']),
            ('payout_instructions', 'status', ['PayoutStatus', 'GetPayoutResponse', 'UpdatePayoutResponse']),
            ('prize_valuations', 'outcome', ['PrizeValuationStatus', 'SubmitPrizeValuationResponse']),
            ('pc_workflow_stages', 'status', ['PcStageStatus', 'SubmitPcStageResponse']),
        ]
        for table, field, schemas in groups:
            block = sql.split('CREATE TABLE ' + table + ' (', 1)[1].split('\n);', 1)[0]
            match = re.search(r'CHECK \(' + field + r' IN \((.*?)\)\)', block, re.S)
            self.assertIsNotNone(match, table)
            expected = set(re.findall(r"'([^']+)'", match.group(1)))
            for name in schemas:
                with self.subTest(schema=name):
                    self.assertEqual(set(doc['components']['schemas'][name]['properties']['status']['enum']), expected)
