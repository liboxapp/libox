"""C1 · pruebas contra PostgreSQL 17 efímero en Docker.

Se omiten salvo LIBOX_DB_DOCKER=1. Usan la imagen fijada por digest (o
LIBOX_PG_IMAGE, explícita), sin red ni puertos. Además de exigir que los tres
escenarios pasen, introducen mutaciones y exigen que las comprobaciones fallen:
un control que nunca falla no demuestra nada.
"""
import copy
import json
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import c1_sql_check as check  # noqa: E402
import pgdocker  # noqa: E402

ENABLED = os.environ.get("LIBOX_DB_DOCKER") == "1"
ACCEPTED_FINDING_STATES = ("abierto", "no reproducido: el esquema rechazó")


def last(run, cid):
    matches = [c for c in run.checks if c["id"] == cid]
    if not matches:
        raise AssertionError("sin comprobación " + cid)
    return matches[-1]


@unittest.skipUnless(ENABLED, "Requiere LIBOX_DB_DOCKER=1 y Docker local con la imagen fijada")
class Pg17Ephemeral(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(check.MANIFEST.read_text(encoding="utf-8"))
        cls.v7 = check.V7_SQL.read_text(encoding="utf-8")
        cls.image = os.environ.get("LIBOX_PG_IMAGE", pgdocker.DEFAULT_IMAGE)

    def test_scenarios_pass(self):
        for name in check.SCENARIOS:
            with self.subTest(escenario=name):
                evidence = check.run_scenario(name, self.image, False, self.manifest, self.v7)
                summary = evidence["resumen"]
                self.assertIsNone(summary["interrumpido"])
                self.assertEqual(summary["fallan"], [])
                self.assertEqual(summary["resultado"], "pasa")
                self.assertEqual(evidence["entorno"]["aislamiento"]["red"], "none")
                self.assertEqual(evidence["entorno"]["aislamiento"]["puertos"], {})
                for finding in evidence["hallazgos_abiertos_observados"]:
                    self.assertTrue(finding["estado"].startswith(ACCEPTED_FINDING_STATES), finding)

    def test_checks_detect_mutations(self):
        with pgdocker.PgContainer(self.image, "mutaciones") as pg:
            run = check.ScenarioRun(pg, "superusuario", self.manifest, self.v7)
            run.setup()
            run.apply_v7()
            run.apply_overlay()

            run.check_acl_matrix()
            self.assertEqual(last(run, "ACL-MATRIZ")["resultado"], "pasa", "control limpio")

            altered = copy.deepcopy(self.manifest)
            altered["tablas"]["markets"] = "reservado_humano"
            run.manifest = altered
            run.check_acl_matrix()
            self.assertEqual(last(run, "ACL-MATRIZ")["resultado"], "falla", "manifiesto más estricto")
            run.manifest = self.manifest

            mutations = [
                ("GRANT UPDATE ON public.journal_lines TO libox_app;",
                 "REVOKE UPDATE ON public.journal_lines FROM libox_app;", "ACL-MATRIZ"),
                ("GRANT SELECT ON public.analytics_events_p" + check.month_suffix(*run.reference) + " TO libox_read;",
                 "REVOKE SELECT ON public.analytics_events_p" + check.month_suffix(*run.reference) + " FROM libox_read;",
                 "ACL-MATRIZ"),
                ("GRANT SELECT ON public.markets TO PUBLIC;", "REVOKE SELECT ON public.markets FROM PUBLIC;",
                 "ACL-PUBLIC"),
                ("GRANT EXECUTE ON FUNCTION libox_ops.partition_status(timestamptz) TO libox_app;",
                 "REVOKE EXECUTE ON FUNCTION libox_ops.partition_status(timestamptz) FROM libox_app;",
                 "ACL-FUNCIONES"),
            ]
            for grant, revoke, cid in mutations:
                with self.subTest(mutacion=grant):
                    self.assertEqual(run.admin(grant).rc, 0)
                    run.check_acl_matrix()
                    self.assertEqual(last(run, cid)["resultado"], "falla")
                    self.assertEqual(run.admin(revoke).rc, 0)
            run.check_acl_matrix()
            for cid in ("ACL-MATRIZ", "ACL-PUBLIC", "ACL-FUNCIONES", "ACL-POR-DEFECTO"):
                self.assertEqual(last(run, cid)["resultado"], "pasa", "tras revertir " + cid)

            current = check.month_suffix(*run.reference)
            run.check_acl_grantees()
            self.assertEqual(last(run, "ACL-BENEFICIARIOS")["resultado"], "pasa", "control limpio beneficiarios")
            self.assertEqual(run.admin("CREATE ROLE c1_mut_custom NOLOGIN;\nGRANT SELECT ON public.audit_events_p"
                                       + current + " TO c1_mut_custom;").rc, 0)
            run.check_acl_grantees()
            self.assertEqual(last(run, "ACL-BENEFICIARIOS")["resultado"], "falla", "rol ajeno al manifiesto en partición")
            self.assertEqual(run.admin("REVOKE SELECT ON public.audit_events_p" + current + " FROM c1_mut_custom;").rc, 0)
            run.check_acl_grantees()
            self.assertEqual(last(run, "ACL-BENEFICIARIOS")["resultado"], "pasa", "tras revertir rol ajeno")

            run.check_new_object_probe()
            self.assertEqual(last(run, "ACL-SONDA-OBJETOS-NUEVOS")["resultado"], "pasa", "control limpio sonda")
            empty_defaults = run.q(check.DEFAULT_ACL_SQL)
            self.assertEqual(run.installer_sql("ALTER DEFAULT PRIVILEGES GRANT EXECUTE ON FUNCTIONS TO PUBLIC;").rc, 0)
            self.assertEqual(run.q(check.DEFAULT_ACL_SQL), empty_defaults,
                             "La mutación deja pg_default_acl sin filas visibles: solo la sonda la detecta")
            run.check_new_object_probe()
            self.assertEqual(last(run, "ACL-SONDA-OBJETOS-NUEVOS")["resultado"], "falla", "EXECUTE a PUBLIC por defecto")
            self.assertEqual(run.installer_sql("ALTER DEFAULT PRIVILEGES REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;").rc, 0)
            run.check_new_object_probe()
            self.assertEqual(last(run, "ACL-SONDA-OBJETOS-NUEVOS")["resultado"], "pasa", "tras revertir EXECUTE")

            self.assertEqual(run.admin("UPDATE libox_ops.partitioned_parents SET provisioning = \x27overlay\x27"
                                       " WHERE parent_table = \x27journal_lines\x27;").rc, 0)
            run.check_partitions()
            self.assertEqual(last(run, "PT-INVENTARIO")["resultado"], "falla", "journal_lines marcada como overlay")
            self.assertEqual(run.admin("UPDATE libox_ops.partitioned_parents SET provisioning = \x27humano\x27"
                                       " WHERE parent_table = \x27journal_lines\x27;").rc, 0)
            run.check_human_parent_untouched()
            self.assertEqual(last(run, "PT-JOURNAL-LINES-HUMANO")["resultado"], "pasa")

            real = run.reference
            run.reference = check.add_months(real[0], real[1], -1)
            run.check_partitions()
            self.assertEqual(last(run, "PT-COBERTURA-UTC")["resultado"], "falla", "mes de referencia equivocado")
            run.reference = real
            run.check_partitions()
            self.assertEqual(last(run, "PT-COBERTURA-UTC")["resultado"], "pasa")

            schema_mutations = [
                "ALTER TABLE public.markets ALTER COLUMN name TYPE varchar(81);",
                "ALTER TABLE public.markets ENABLE ROW LEVEL SECURITY;",
                "CREATE POLICY c1_mut_policy ON public.markets USING (true);",
                "CREATE RULE c1_mut_rule AS ON DELETE TO public.leads DO INSTEAD NOTHING;",
                "CREATE PROCEDURE public.c1_mut_proc() LANGUAGE sql AS $p$SELECT 1$p$;",
                "ALTER TABLE public.leads OWNER TO libox_app;",
            ]
            for mutation in schema_mutations:
                with self.subTest(huella=mutation):
                    before = run.fingerprint()
                    self.assertEqual(run.admin(mutation).rc, 0)
                    run.check_invariance(before)
                    self.assertEqual(last(run, "OV-NO-MODIFICA-V7")["resultado"], "falla", mutation)


if __name__ == "__main__":
    unittest.main()
