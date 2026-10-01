"""C1 · pruebas estáticas del overlay SQL (sin Docker, solo stdlib).

Comprueban que el overlay no toca zonas críticas, que sus concesiones son
exactamente las del manifiesto, que el inventario coincide con V7 y que la
semilla coincide con los literales de L3 V7 §10.1.
"""
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import c1_sql_check as check  # noqa: E402
import pgdocker  # noqa: E402

OVERLAY = {p.name: p.read_text(encoding="utf-8") for p in check.overlay_files()}
MANIFEST = json.loads(check.MANIFEST.read_text(encoding="utf-8"))
V7_TEXT = check.V7_SQL.read_text(encoding="utf-8")
GRANT_RE = re.compile(r"^GRANT ([A-Z, ]+) ON TABLE public\.(\w+) TO ([\w, ]+);$", re.M)
DECISION_DOC = check.ROOT / "docs/superpowers/specs/c1-l3-v8/decisiones-c1-datos.md"
LETTERS = {"S": "SELECT", "I": "INSERT", "U": "UPDATE"}


def strip_comments(sql):
    return "\n".join(line.split("--", 1)[0] for line in sql.splitlines())


class OverlayStatic(unittest.TestCase):
    def test_v7_is_intact_and_pinned(self):
        digest = hashlib.sha256(check.V7_SQL.read_bytes()).hexdigest()
        self.assertEqual(digest, check.V7_SHA256, "El SQL V7 cambió: el overlay se validó contra otro hash")
        self.assertEqual(MANIFEST["fuente_esquema_sha256"], check.V7_SHA256)

    def test_overlay_files_expected(self):
        self.assertEqual(sorted(OVERLAY), ["010_libox_ops_particiones.sql", "020_acl_base.sql",
                                           "030_semilla_mercado_pe.sql", "040_arranque_particiones.sql"])

    def test_manifest_classifies_every_v7_table_once(self):
        tables = check.v7_tables(V7_TEXT)
        self.assertEqual(len(tables), 135)
        self.assertEqual(sorted(MANIFEST["tablas"]), sorted(tables))
        self.assertTrue(set(MANIFEST["tablas"].values()) <= set(MANIFEST["clases"]))

    def test_critical_classes_have_no_privileges(self):
        self.assertEqual(MANIFEST["clases"]["reservado_humano"]["privilegios"], {})
        self.assertNotIn("pendiente_matriz", MANIFEST["clases"], "B1 clasificó las 67 tablas")
        self.assertEqual(sum(1 for c in MANIFEST["tablas"].values() if c == "reservado_humano"), 57)
        for table in check.B1_RESERVED:
            self.assertEqual(MANIFEST["tablas"][table], "reservado_humano", table)
        self.assertEqual(sorted(MANIFEST["reclasificadas_b1_reservado_humano"]), check.B1_RESERVED)
        for table in ("journal_lines", "journal_entries", "ledger_accounts", "orders", "payments", "tickets",
                      "raffles", "settlements", "draw_executions", "subrole_assignments",
                      "subrole_incompatibilities", "fsm_transitions", "fee_schedules", "market_config_versions",
                      "refund_credits", "free_entry_campaigns", "event_outbox", "idempotency_keys"):
            self.assertEqual(MANIFEST["tablas"][table], "reservado_humano", table)

    def test_b1_matches_decision_doc(self):
        doc = DECISION_DOC.read_text(encoding="utf-8")
        b1 = doc[doc.index("## B1."):doc.index("## B1-bis.")]
        self.assertIn("**Decisión:** clases aprobadas y las seis candidatas pasan a `reservado_humano`", b1)
        decided = {}
        for cls, app, read, tables in re.findall(r"^\| `(\w+)`(?: \(existente\))? \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$",
                                                 b1, re.M):
            privs = {}
            for role, cell in (("libox_app", app), ("libox_read", read)):
                letters = [x.strip() for x in cell.split(",") if x.strip() in LETTERS]
                if letters:
                    privs[role] = sorted(LETTERS[x] for x in letters)
            self.assertEqual({r: sorted(p) for r, p in MANIFEST["clases"][cls]["privilegios"].items()}, privs, cls)
            for table in re.findall(r"`(\w+)`", tables):
                decided[table] = cls
        candidates = b1[b1.index("**Candidatas a reclasificar"):b1.index("**Recomendación:**")]
        for row in re.findall(r"^\| (`[^|]+) \|", candidates, re.M):
            for table in re.findall(r"`(\w+)`", row):
                decided[table] = "reservado_humano"
        self.assertEqual(len(decided), 67)
        self.assertEqual({t: MANIFEST["tablas"][t] for t in decided}, decided)

    def test_b1_classes_never_grant_destructive_privileges(self):
        for cls, spec in MANIFEST["clases"].items():
            for role, privs in spec["privilegios"].items():
                self.assertTrue(set(privs) <= {"SELECT", "INSERT", "UPDATE"}, cls + "/" + role)
                self.assertIn(role, MANIFEST["roles_grupo"])
        for cls in ("sensible", "sensible_inmutable"):
            self.assertEqual(sorted(MANIFEST["clases"][cls]["privilegios"]), ["libox_app"], cls)
        for cls in ("registro_inmutable", "sensible_inmutable"):
            self.assertNotIn("UPDATE", MANIFEST["clases"][cls]["privilegios"]["libox_app"], cls)

    def test_b2_login_spec(self):
        logins = MANIFEST["logins_componente_b2"]["miembros"]
        self.assertEqual(logins, {"libox_api": ["libox_app"], "libox_worker": ["libox_app", "libox_append"],
                                  "libox_reporting": ["libox_read"], "libox_deployer": ["libox_migrate"]})
        for name, sql in OVERLAY.items():
            self.assertNotRegex(strip_comments(sql), r"(?i)\bPASSWORD\b|\bLOGIN\b|libox_(api|worker|reporting|deployer)",
                                name)
        source = Path(check.__file__).read_text(encoding="utf-8")
        method = source[source.index("def check_component_logins"):source.index("def check_ownership_pending")]
        self.assertIn("prelude = \"BEGIN;\\n\"", method)
        self.assertNotRegex(method, r"(?i)PASSWORD|COMMIT")

    def test_b4_default_procedure_scope(self):
        spec = MANIFEST["procedimiento_default_b4"]
        allowed, human = spec["padres_permitidos"], spec["padres_humano"]
        parents = check.v7_partitioned_parents(V7_TEXT)
        self.assertEqual(sorted(allowed + human), sorted(parents))
        self.assertFalse(set(allowed) & set(human))
        for table in allowed:
            self.assertNotEqual(MANIFEST["tablas"][table], "reservado_humano", table)
        for table in human:
            self.assertEqual(MANIFEST["tablas"][table], "reservado_humano", table)
        self.assertIn("journal_lines", human)

    def test_b6_retention_is_metadata_only(self):
        sql = OVERLAY["010_libox_ops_particiones.sql"]
        block = sql[sql.index("INSERT INTO libox_ops.partitioned_parents"):sql.index("ON CONFLICT (parent_table)")]
        retention = dict(re.findall(r"\(\x27(\w+)\x27,\s*\x27\w+\x27,\s*\x27\w+\x27,\s*\x27([^\x27]*)\x27\)", block))
        self.assertEqual(len(retention), 12)
        for table in ("audit_access_events", "risk_events"):
            self.assertIn("B6", retention[table])
            self.assertIn("indefinida", retention[table])
        for table in ("psp_events", "operation_register"):
            self.assertIn("[LEGAL→ABOGADO]", retention[table])
            self.assertIn("sin borrado", retention[table])
        self.assertFalse([t for t, r in retention.items() if r.startswith("Pendiente")])
        for name, body in OVERLAY.items():
            self.assertNotRegex(strip_comments(body), r"(?i)DETACH\s+PARTITION|pg_cron|cron\.schedule", name)

    def test_no_kms_columns_in_overlay(self):
        for name, body in OVERLAY.items():
            self.assertNotRegex(strip_comments(body), r"(?i)_enc\b|ADD\s+COLUMN|pgcrypto|pgsodium|vault\.", name)

    def test_grants_equal_manifest(self):
        sql = strip_comments(OVERLAY["020_acl_base.sql"])
        granted = set()
        for privs, table, roles in GRANT_RE.findall(sql):
            for role in (r.strip() for r in roles.split(",")):
                granted.update((table, role, p.strip()) for p in privs.split(","))
        expected = set()
        for table, cls in MANIFEST["tablas"].items():
            for role, privs in MANIFEST["clases"][cls]["privilegios"].items():
                expected.update((table, role, p) for p in privs)
        self.assertEqual(granted, expected)
        other = [line for line in sql.splitlines() if line.startswith("GRANT ") and not GRANT_RE.match(line)]
        self.assertEqual(other, ["GRANT USAGE ON SCHEMA public TO libox_app, libox_append, libox_read;"])

    def test_no_grants_in_other_files(self):
        for name, sql in OVERLAY.items():
            if name != "020_acl_base.sql":
                self.assertNotRegex(strip_comments(sql), r"(?im)^\s*GRANT ", name)

    def test_forbidden_constructs(self):
        forbidden = [r"CREATE\s+(CONSTRAINT\s+)?TRIGGER", r"\bTO\s+PUBLIC\b", r"GRANT\s+ALL", r"\bDROP\s",
                     r"\bDELETE\s+FROM\b", r"\bTRUNCATE\b", r"^\s*UPDATE\s", r"\bALTER\s+TABLE\b",
                     r"SECURITY\s+DEFINER", r"DISABLE\s+TRIGGER", r"session_replication_role",
                     r"ALTER\s+ROLE", r"CREATE\s+ROLE", r"\bOWNER\s+TO\b", r"\bPROCEDURE\b",
                     r"\bPOLICY\b", r"CREATE\s+(OR\s+REPLACE\s+)?RULE", r"ROW\s+LEVEL\s+SECURITY",
                     r"\bBYPASSRLS\b", r"ALTER\s+FUNCTION", r"public\.journal_lines"]
        for name, sql in OVERLAY.items():
            body = strip_comments(sql)
            for pattern in forbidden:
                self.assertNotRegex(body, re.compile(pattern, re.I | re.M), name + ": " + pattern)

    def test_functions_only_in_libox_ops(self):
        for name, sql in OVERLAY.items():
            for target in re.findall(r"CREATE\s+(?:OR\s+REPLACE\s+)?FUNCTION\s+([\w.]+)", sql, re.I):
                self.assertTrue(target.startswith("libox_ops."), name + ": " + target)

    def test_inserts_only_ops_inventory_and_market(self):
        targets = set()
        for sql in OVERLAY.values():
            targets.update(re.findall(r"INSERT\s+INTO\s+([\w.]+)", strip_comments(sql), re.I))
        self.assertEqual(targets, {"libox_ops.partitioned_parents", "public.markets"})

    def test_inventory_matches_v7_parents(self):
        sql = OVERLAY["010_libox_ops_particiones.sql"]
        block = sql[sql.index("INSERT INTO libox_ops.partitioned_parents"):sql.index("ON CONFLICT (parent_table)")]
        rows = re.findall(r"\(\x27(\w+)\x27,\s*\x27(\w+)\x27,\s*\x27(overlay|humano)\x27,", block)
        self.assertEqual({parent: key for parent, key, _ in rows}, check.v7_partitioned_parents(V7_TEXT))
        self.assertEqual(len(rows), 12)
        humans = sorted(parent for parent, _, prov in rows if prov == "humano")
        self.assertEqual(humans, ["journal_lines"])
        self.assertEqual(humans, check.HUMAN_PARTITIONED)
        self.assertEqual(humans, MANIFEST["particiones_reservadas_humano"])
        self.assertEqual(MANIFEST["tablas"]["journal_lines"], "reservado_humano")

    def test_ensure_only_provisions_overlay_parents(self):
        sql = OVERLAY["010_libox_ops_particiones.sql"]
        ensure = sql[sql.index("FUNCTION libox_ops.ensure_monthly_partitions("):sql.index("FUNCTION libox_ops.partition_status(")]
        self.assertIn("WHERE pp.provisioning = \x27overlay\x27", ensure)
        self.assertEqual(ensure.count("FROM libox_ops.partitioned_parents pp"), 1)
        for name, body in OVERLAY.items():
            self.assertNotRegex(strip_comments(body), r"journal_lines_p", name)

    def test_partition_acl_is_generic(self):
        sql = OVERLAY["010_libox_ops_particiones.sql"]
        block = sql[sql.index("restrict_partition_acl(p_partition text)"):sql.index("ensure_monthly_partitions(\n")]
        self.assertIn("aclexplode(coalesce(c.relacl, acldefault(\x27r\x27, c.relowner)))", block)
        self.assertIn("a.grantee <> c.relowner", block)
        self.assertIn("FROM PUBLIC", block)
        self.assertIn("LIBOX_PARTITION_ACL_RESIDUAL", block)
        self.assertNotIn("rolname IN", block, "La revocación no debe depender de una lista fija de roles")
        acl = OVERLAY["020_acl_base.sql"]
        roles = re.search(r"WHERE rolname IN \(([^)]*)\)", acl).group(1)
        self.assertEqual(sorted(r.strip().strip("\x27") for r in roles.split(",")), sorted(MANIFEST["roles_api_denegados"]))
        self.assertIn("service_role", MANIFEST["roles_api_denegados"])

    def test_horizon_and_lock_timeout(self):
        sql = OVERLAY["010_libox_ops_particiones.sql"]
        self.assertIn("p_months_ahead integer     DEFAULT 2)", sql)
        self.assertIn("ensure_monthly_partitions(now(), 2)", OVERLAY["040_arranque_particiones.sql"])
        self.assertEqual(check.HORIZON_MONTHS, 2)
        ensure = sql[sql.index("FUNCTION libox_ops.ensure_monthly_partitions("):sql.index("FUNCTION libox_ops.partition_status(")]
        self.assertIn("SET lock_timeout = \x275s\x27", ensure)
        self.assertNotRegex(strip_comments(sql), r"pg_advisory|FOR UPDATE|LOCK TABLE")
        status = sql[sql.index("FUNCTION libox_ops.partition_status("):]
        self.assertIn("covered_until > p_reference + interval \x2730 days\x27", status)

    def test_utc_is_explicit(self):
        sql = OVERLAY["010_libox_ops_particiones.sql"]
        self.assertEqual(sql.count("SET \"TimeZone\" = \x27UTC\x27"), 2)
        self.assertIn("date_trunc(\x27month\x27, p_reference AT TIME ZONE \x27UTC\x27)", sql)

    def test_seed_literals_match_l3(self):
        literals = check.l3_market_literals(check.L3_DOC.read_text(encoding="utf-8"))
        values = re.search(r"VALUES \(([^)]*)\)", OVERLAY["030_semilla_mercado_pe.sql"]).group(1)
        code, _name, currency, timezone, locale = [v.strip().strip("\x27") for v in values.split(",")]
        self.assertEqual({"code": code, "currency": currency, "timezone": timezone, "locale": locale}, literals)

    def test_docker_command_is_isolated(self):
        argv = pgdocker.build_run_command("libox-c1-sql-x", pgdocker.DEFAULT_IMAGE)
        self.assertIn("none", argv[argv.index("--network") + 1])
        self.assertEqual(argv[argv.index("--pull") + 1], "never")
        self.assertFalse({"-p", "--publish", "-P", "--publish-all", "--privileged"} & set(argv))
        self.assertIn("--read-only", argv)
        self.assertEqual(argv[argv.index("--cap-drop") + 1], "ALL")
        self.assertTrue(pgdocker.DEFAULT_IMAGE.startswith("postgres@sha256:"))
        self.assertEqual(argv[-1], pgdocker.DEFAULT_IMAGE)
        self.assertNotRegex(" ".join(argv), r"PASSWORD")
        pulled = pgdocker.build_run_command("x", "img", allow_pull=True)
        self.assertEqual(pulled[pulled.index("--pull") + 1], "missing")

    def test_utc_helpers(self):
        self.assertEqual(check.utc_month_of("2030-01-31T23:59:59.999999+00:00"), "203001")
        self.assertEqual(check.utc_month_of("2030-01-31T19:00:00-05:00"), "203002")
        self.assertEqual(check.utc_month_of("2030-01-31 20:00:00"), "203002")
        self.assertEqual(check.add_months(2026, 12, 1), (2027, 1))
        self.assertEqual(check.expected_bound(2026, 12),
                         "FOR VALUES FROM (\x272026-12-01 00:00:00+00\x27) TO (\x272027-01-01 00:00:00+00\x27)")


if __name__ == "__main__":
    unittest.main()
