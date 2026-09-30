#!/usr/bin/env python3
"""C1 · verificación del overlay NO crítico sobre libox_schema_L3_V7.sql.

Levanta PostgreSQL efímero (ver pgdocker.py), aplica el SQL V7 intacto y el
overlay borrador de docs/superpowers/specs/c1-l3-v8/database/overlay, ejecuta
pruebas de particiones, ACL, idempotencia, frontera UTC y fuera de rango, y
guarda evidencia JSON sin credenciales.

No es la migración V8, no prueba Supabase gestionado y no implementa lógica
patrimonial, RBAC, sorteo ni concurrencia de negocio. Las sondas H-07/H-09
solo observan el comportamiento del código V7 existente dentro de una
transacción que se revierte.

Uso: python3 scripts/database/c1_sql_check.py --escenario todos
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pgdocker  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
V7_SQL = ROOT / "docs/linea-base/ARTEFACTOS/libox_schema_L3_V7.sql"
V7_SHA256 = "9ff3d07f3efef5ee2cf4997d34e361a6b78c64463b346c855a840f4baf937a43"
L3_DOC = ROOT / "docs/linea-base/LIBOX_ESPECIFICACION_TECNICA_L3_V7.md"
DB_DIR = ROOT / "docs/superpowers/specs/c1-l3-v8/database"
OVERLAY_DIR = DB_DIR / "overlay"
MANIFEST = DB_DIR / "acl-manifest.json"
EVIDENCE_DIR = DB_DIR / "evidencia"
DB = "libox_c1"
INSTALLER = "libox_installer"
LIMA_OFFSET_HOURS = -5  # America/Lima: UTC-5 sin horario de verano desde 1994.
HUMAN_PARTITIONED = ["journal_lines"]  # particiones aportadas por el dueño del ledger
HORIZON_MONTHS = 2  # mes actual + 2: el mes M existe 30 días antes de empezar (L3 V7 §1.3)
ALLOWED_GRANTEES = ["libox_app", "libox_append", "libox_read"]

SCENARIOS = {
    "superusuario": {
        "installer": "postgres", "api_defaults": False,
        "descripcion": "Instalador superusuario de la imagen oficial."},
    "dueno-createrole": {
        "installer": INSTALLER, "api_defaults": False,
        "descripcion": "Instalador dueño de la base, sin SUPERUSER, con CREATEROLE."},
    "privilegios-api-simulados": {
        "installer": INSTALLER, "api_defaults": True,
        "descripcion": ("Como dueno-createrole, más roles anon/authenticated/service_role con privilegios por "
                        "defecto que los exponen. Simulación local del patrón Supabase; no es "
                        "Supabase gestionado.")},
}

ADVERTENCIAS = [
    "Overlay borrador sobre V7 intacto; no es el SQL V8 ni una migración completa.",
    "No acredita comportamiento de Supabase gestionado, pooler ni Data API reales.",
    "H-05 queda parcial (11/12 padres): journal_lines no recibe particiones del overlay; las aporta su dueño humano.",
    "H-06 queda parcial: solo hay privilegios para clases no patrimoniales; la matriz completa está pendiente.",
    "Precondición antes de aplicar en Supabase: validar Data API/exposición del esquema, RLS gestionado y privilegios por defecto de otros roles (supabase_admin).",
    "Las zonas críticas (ledger, RBAC, sorteo, concurrencia, incompatibilidades, comisión) no se implementan aquí.",
]

SEED_EMPTY_TABLES = ["fsm_transitions", "ledger_accounts", "subrole_incompatibilities",
                     "market_config_versions", "fee_schedules", "platform_capabilities",
                     "evidence_strength_rules", "survey_instruments", "holidays_calendar",
                     "subrole_assignments"]


class Abort(RuntimeError):
    """Un paso previo falló; las comprobaciones siguientes no tienen sentido."""


# ---------------------------------------------------------------- utilidades puras

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def overlay_files() -> List[Path]:
    return sorted(OVERLAY_DIR.glob("*.sql"))


def v7_tables(sql_text: str) -> List[str]:
    return re.findall(r"^CREATE TABLE (\w+)", sql_text, re.M)


def v7_partitioned_parents(sql_text: str) -> Dict[str, str]:
    pattern = r"CREATE TABLE (\w+) \((?:(?!\nCREATE ).)*?\) PARTITION BY RANGE \((\w+)\)"
    return dict(re.findall(pattern, sql_text, re.S))


def l3_market_literals(text: str) -> Dict[str, str]:
    """Valores literales de mercado en L3 V7 §10.1."""
    start = text.index("## 10.1 Documento")
    block = text[start:start + 2000]
    patterns = {
        "code": r"\"market_code\": \"([A-Z]{2})\"",
        "currency": r"\"currency\": \{ \"code\": \"([A-Z]{3})\"",
        "timezone": r"\"timezone\": \"([^\"]+)\"",
        "locale": r"\"locale\": \"([^\"]+)\"",
    }
    out = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, block)
        if not match:
            raise ValueError("L3 §10.1 sin literal para " + key)
        out[key] = match.group(1)
    return out


def add_months(year: int, month: int, k: int) -> Tuple[int, int]:
    index = year * 12 + (month - 1) + k
    return index // 12, index % 12 + 1


def month_suffix(year: int, month: int) -> str:
    return "%04d%02d" % (year, month)


def expected_bound(year: int, month: int) -> str:
    y2, m2 = add_months(year, month, 1)
    return ("FOR VALUES FROM ('%04d-%02d-01 00:00:00+00') TO ('%04d-%02d-01 00:00:00+00')"
            % (year, month, y2, m2))


def utc_month_of(literal: str, session_offset_hours: int = LIMA_OFFSET_HOURS) -> str:
    """Mes UTC (AAAAMM) de un literal ISO; sin desfase se interpreta en la zona de sesión."""
    value = dt.datetime.fromisoformat(literal)
    if value.tzinfo is None:
        value = value.replace(tzinfo=dt.timezone(dt.timedelta(hours=session_offset_hours)))
    value = value.astimezone(dt.timezone.utc)
    return month_suffix(value.year, value.month)


def sql_text(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


# ---------------------------------------------------------------- consultas de catálogo

SUMMARY_SQL = (
    "SELECT json_build_object("
    "'tablas', (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace"
    " WHERE n.nspname = 'public' AND c.relkind IN ('r', 'p') AND NOT c.relispartition),"
    "'padres_particionados', (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace"
    " WHERE n.nspname = 'public' AND c.relkind = 'p' AND NOT c.relispartition),"
    "'particiones', (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace"
    " WHERE n.nspname = 'public' AND c.relispartition),"
    "'funciones_public', (SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace"
    " WHERE n.nspname = 'public'),"
    "'disparadores', (SELECT count(*) FROM pg_trigger t JOIN pg_class c ON c.oid = t.tgrelid"
    " JOIN pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname = 'public' AND NOT t.tgisinternal),"
    "'concesiones_a_no_duenos', (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace,"
    " LATERAL aclexplode(coalesce(c.relacl, acldefault('r', c.relowner))) a"
    " WHERE n.nspname = 'public' AND c.relkind IN ('r', 'p') AND a.grantee <> c.relowner),"
    "'filas', json_build_object("
    "'raffle_type_rules', (SELECT count(*) FROM public.raffle_type_rules),"
    "'subrole_grant_matrix', (SELECT count(*) FROM public.subrole_grant_matrix),"
    "'markets', (SELECT count(*) FROM public.markets),"
    "'fsm_transitions', (SELECT count(*) FROM public.fsm_transitions),"
    "'ledger_accounts', (SELECT count(*) FROM public.ledger_accounts),"
    "'subrole_incompatibilities', (SELECT count(*) FROM public.subrole_incompatibilities)))")

FINGERPRINT_SQL = (
    "SELECT md5(string_agg(x, E'\\n' ORDER BY x)) FROM ("
    " SELECT 'col:' || c.relname || '.' || a.attname || ':' || format_type(a.atttypid, a.atttypmod)"
    "  || ':' || a.attnotnull || ':' || coalesce(pg_get_expr(d.adbin, d.adrelid), '') AS x"
    "  FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace"
    "  JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum > 0 AND NOT a.attisdropped"
    "  LEFT JOIN pg_attrdef d ON d.adrelid = c.oid AND d.adnum = a.attnum"
    "  WHERE n.nspname = 'public' AND c.relkind IN ('r', 'p') AND NOT c.relispartition"
    " UNION ALL SELECT 'con:' || c.relname || '.' || co.conname || ':' || pg_get_constraintdef(co.oid)"
    "  FROM pg_constraint co JOIN pg_class c ON c.oid = co.conrelid JOIN pg_namespace n ON n.oid = c.relnamespace"
    "  WHERE n.nspname = 'public' AND NOT c.relispartition"
    " UNION ALL SELECT 'idx:' || pg_get_indexdef(i.indexrelid)"
    "  FROM pg_index i JOIN pg_class c ON c.oid = i.indrelid JOIN pg_namespace n ON n.oid = c.relnamespace"
    "  WHERE n.nspname = 'public' AND NOT c.relispartition"
    " UNION ALL SELECT 'trg:' || c.relname || '.' || t.tgname || ':' || pg_get_triggerdef(t.oid)"
    "  || ':' || t.tgenabled::text"
    "  FROM pg_trigger t JOIN pg_class c ON c.oid = t.tgrelid JOIN pg_namespace n ON n.oid = c.relnamespace"
    "  WHERE n.nspname = 'public' AND NOT t.tgisinternal AND NOT c.relispartition"
    " UNION ALL SELECT 'rel:' || c.relname || ':' || c.relkind::text || ':' || pg_get_userbyid(c.relowner)"
    "  || ':' || c.relrowsecurity || ':' || c.relforcerowsecurity"
    "  FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace"
    "  WHERE n.nspname = 'public' AND c.relkind IN ('r', 'p', 'v', 'm') AND NOT c.relispartition"
    " UNION ALL SELECT 'pol:' || c.relname || '.' || pol.polname || ':' || pol.polcmd::text || ':'"
    "  || coalesce(pg_get_expr(pol.polqual, pol.polrelid), '') || ':'"
    "  || coalesce(pg_get_expr(pol.polwithcheck, pol.polrelid), '')"
    "  FROM pg_policy pol JOIN pg_class c ON c.oid = pol.polrelid JOIN pg_namespace n ON n.oid = c.relnamespace"
    "  WHERE n.nspname = 'public'"
    " UNION ALL SELECT 'rule:' || c.relname || '.' || r.rulename || ':' || pg_get_ruledef(r.oid)"
    "  FROM pg_rewrite r JOIN pg_class c ON c.oid = r.ev_class JOIN pg_namespace n ON n.oid = c.relnamespace"
    "  WHERE n.nspname = 'public'"
    " UNION ALL SELECT 'fn:' || p.proname || ':' || p.prokind::text || ':' || pg_get_userbyid(p.proowner)"
    "  || ':' || md5(p.prosrc) || ':'"
    "  || coalesce(array_to_string(p.proconfig, ','), '') || ':' || p.prosecdef"
    "  FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace WHERE n.nspname = 'public'"
    " UNION ALL SELECT 'dom:' || t.typname || ':' || format_type(t.typbasetype, t.typtypmod)"
    "  FROM pg_type t JOIN pg_namespace n ON n.oid = t.typnamespace"
    "  WHERE n.nspname = 'public' AND t.typtype = 'd') s")

CHILDREN_SQL = (
    "SELECT coalesce(json_object_agg(parent, children), '{}'::json) FROM ("
    " SELECT p.relname AS parent,"
    "  json_object_agg(c.relname, pg_get_expr(c.relpartbound, c.oid) ORDER BY c.relname) AS children"
    " FROM pg_inherits i JOIN pg_class c ON c.oid = i.inhrelid JOIN pg_class p ON p.oid = i.inhparent"
    " JOIN pg_namespace n ON n.oid = p.relnamespace WHERE n.nspname = 'public' GROUP BY p.relname) s")

INVENTORY_SQL = (
    "SELECT json_object_agg(parent_table, json_build_object('clave', partition_key,"
    " 'aprovisionamiento', provisioning)) FROM libox_ops.partitioned_parents")

NON_OWNER_GRANTEES_SQL = (
    "SELECT coalesce(json_agg(json_build_array(kind, schema_name, obj, grantee) ORDER BY 1, 2, 3, 4), '[]') FROM ("
    " SELECT DISTINCT CASE WHEN c.relispartition THEN 'particion' ELSE 'relacion' END AS kind,"
    "  n.nspname::text AS schema_name, c.relname::text AS obj,"
    "  CASE WHEN a.grantee = 0 THEN 'PUBLIC' ELSE pg_get_userbyid(a.grantee)::text END AS grantee"
    " FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace,"
    "  LATERAL aclexplode(coalesce(c.relacl, acldefault('r', c.relowner))) a"
    " WHERE n.nspname IN ('public', 'libox_ops') AND c.relkind IN ('r', 'p', 'S', 'v', 'm')"
    "  AND a.grantee <> c.relowner"
    " UNION SELECT DISTINCT 'funcion', n.nspname::text, p.proname::text,"
    "  CASE WHEN a.grantee = 0 THEN 'PUBLIC' ELSE pg_get_userbyid(a.grantee)::text END"
    " FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace,"
    "  LATERAL aclexplode(coalesce(p.proacl, acldefault('f', p.proowner))) a"
    " WHERE n.nspname IN ('public', 'libox_ops') AND a.grantee <> p.proowner"
    " UNION SELECT DISTINCT 'esquema', n.nspname::text, n.nspname::text,"
    "  CASE WHEN a.grantee = 0 THEN 'PUBLIC' ELSE pg_get_userbyid(a.grantee)::text END"
    " FROM pg_namespace n, LATERAL aclexplode(coalesce(n.nspacl, acldefault('n', n.nspowner))) a"
    " WHERE n.nspname IN ('public', 'libox_ops') AND a.grantee <> n.nspowner) s")

PARENTS_CATALOG_SQL = (
    "SELECT coalesce(json_object_agg(c.relname, a.attname), '{}'::json)"
    " FROM pg_partitioned_table pt JOIN pg_class c ON c.oid = pt.partrelid"
    " JOIN pg_namespace n ON n.oid = c.relnamespace"
    " JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = pt.partattrs[0]"
    " WHERE n.nspname = 'public' AND NOT c.relispartition AND pt.partstrat = 'r'")

SNAPSHOT_SQL = (
    "SELECT json_build_object('relaciones', (SELECT count(*) FROM pg_class c"
    " JOIN pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname IN ('public', 'libox_ops')),"
    " 'particiones', (SELECT json_object_agg(c.relname, json_build_object('limites',"
    " pg_get_expr(c.relpartbound, c.oid), 'acl', c.relacl::text) ORDER BY c.relname)"
    " FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace"
    " WHERE n.nspname = 'public' AND c.relispartition))")

PUBLIC_ACL_SQL = (
    "SELECT json_build_object("
    "'relaciones', (SELECT coalesce(json_agg(DISTINCT c.relname), '[]') FROM pg_class c"
    " JOIN pg_namespace n ON n.oid = c.relnamespace,"
    " LATERAL aclexplode(coalesce(c.relacl, acldefault('r', c.relowner))) a"
    " WHERE n.nspname IN ('public', 'libox_ops') AND c.relkind IN ('r', 'p', 'S', 'v', 'm')"
    " AND a.grantee = 0),"
    "'esquemas', (SELECT coalesce(json_agg(DISTINCT n.nspname), '[]') FROM pg_namespace n,"
    " LATERAL aclexplode(coalesce(n.nspacl, acldefault('n', n.nspowner))) a"
    " WHERE n.nspname IN ('public', 'libox_ops') AND a.grantee = 0),"
    "'funciones', (SELECT coalesce(json_agg(DISTINCT p.proname), '[]') FROM pg_proc p"
    " JOIN pg_namespace n ON n.oid = p.pronamespace,"
    " LATERAL aclexplode(coalesce(p.proacl, acldefault('f', p.proowner))) a"
    " WHERE n.nspname IN ('public', 'libox_ops') AND a.grantee = 0))")

DEFAULT_ACL_SQL = (
    "SELECT coalesce(json_agg(json_build_object('propietario', pg_get_userbyid(d.defaclrole),"
    " 'esquema', coalesce(n.nspname, '(global)'), 'tipo', d.defaclobjtype,"
    " 'beneficiario', CASE WHEN a.grantee = 0 THEN 'PUBLIC' ELSE pg_get_userbyid(a.grantee) END,"
    " 'privilegio', a.privilege_type) ORDER BY 1), '[]')"
    " FROM pg_default_acl d LEFT JOIN pg_namespace n ON n.oid = d.defaclnamespace,"
    " LATERAL aclexplode(d.defaclacl) a WHERE a.grantee <> d.defaclrole")


# ---------------------------------------------------------------- ejecución de un escenario

class ScenarioRun:
    def __init__(self, pg: pgdocker.PgContainer, name: str, manifest: dict, v7_text: str):
        self.pg = pg
        self.name = name
        self.cfg = SCENARIOS[name]
        self.installer = self.cfg["installer"]
        self.manifest = manifest
        self.v7_text = v7_text
        self.checks: List[dict] = []
        self.open_findings: List[dict] = []
        self.characterization: dict = {}
        self.installer_attrs: dict = {}
        self.reference: Tuple[int, int] = (0, 0)
        self.version_num = 0
        self.api_roles: List[str] = []

    # -- infraestructura de comprobación
    def check(self, cid: str, descripcion: str, referencias: Sequence[str], esperado, observado, ok: bool) -> bool:
        self.checks.append({"id": cid, "descripcion": descripcion, "referencias": list(referencias),
                            "esperado": esperado, "observado": observado,
                            "resultado": "pasa" if ok else "falla"})
        return ok

    def admin(self, sql: str) -> pgdocker.PsqlResult:
        return self.pg.psql(sql, user="postgres", db=DB)

    def installer_sql(self, sql: str) -> pgdocker.PsqlResult:
        return self.pg.psql(sql, user=self.installer, db=DB)

    def q(self, query: str, prelude: str = "", user: str = "postgres"):
        return self.pg.json(query, user=user, db=DB, prelude=prelude)

    def expect(self, cid: str, descripcion: str, referencias: Sequence[str], sql: str,
               error: Optional[Tuple[str, str]] = None, user: str = "postgres") -> pgdocker.PsqlResult:
        """error=None exige éxito; error=(sqlstate, fragmento) exige ese fallo."""
        res = self.pg.psql(sql, user=user, db=DB)
        observado = {"rc": res.rc, "error": res.error_line() if res.rc else None}
        if error is None:
            self.check(cid, descripcion, referencias, {"rc": 0}, observado, res.rc == 0)
        else:
            self.check(cid, descripcion, referencias,
                       {"sqlstate": error[0], "mensaje_contiene": error[1]}, observado,
                       res.failed_with(error[0], error[1]))
        return res

    def as_role(self, role: str, body: str) -> str:
        return "BEGIN;\nSET LOCAL ROLE " + role + ";\n" + body + "\nROLLBACK;\n"

    # -- pasos
    def setup(self) -> None:
        if self.installer == "postgres":
            sql = "CREATE DATABASE " + DB + ";"
        else:
            sql = ("CREATE ROLE " + INSTALLER + " LOGIN CREATEROLE NOSUPERUSER;\n"
                   "CREATE DATABASE " + DB + " OWNER " + INSTALLER + ";")
        res = self.pg.psql(sql, user="postgres", db="postgres")
        if res.rc != 0:
            raise Abort("preparación fallida: " + res.error_line())
        if self.cfg["api_defaults"]:
            grant = "ALTER DEFAULT PRIVILEGES FOR ROLE " + INSTALLER + " IN SCHEMA public GRANT ALL ON "
            api = "anon, authenticated, service_role"
            sql = ("CREATE ROLE anon NOLOGIN;\nCREATE ROLE authenticated NOLOGIN;\n"
                   "CREATE ROLE service_role NOLOGIN BYPASSRLS;\n"
                   "GRANT USAGE ON SCHEMA public TO " + api + ";\n"
                   + grant + "TABLES TO " + api + ";\n"
                   + grant + "SEQUENCES TO " + api + ";\n"
                   + grant + "FUNCTIONS TO " + api + ";\n")
            res = self.admin(sql)
            if res.rc != 0:
                raise Abort("simulación de privilegios de API fallida: " + res.error_line())
        self.installer_attrs = self.q(
            "SELECT row_to_json(r) FROM (SELECT rolname, rolsuper, rolcreaterole, rolcreatedb, rolbypassrls"
            " FROM pg_roles WHERE rolname = " + sql_text(self.installer) + ") r")
        self.version_num = int(self.q("SELECT to_json(current_setting('server_version_num')::int)"))

    def apply_v7(self) -> None:
        digest = hashlib.sha256(self.v7_text.encode("utf-8")).hexdigest()
        if not self.check("V7-INTACTO", "El SQL V7 aplicado coincide con el hash fijado",
                          ["docs/linea-base/ARTEFACTOS/libox_schema_L3_V7.sql"], V7_SHA256, digest,
                          digest == V7_SHA256):
            raise Abort("V7 no coincide con el hash fijado")
        res = self.installer_sql(self.v7_text)
        if not self.check("V7-APLICA", "V7 intacto se aplica sin errores con el instalador del escenario",
                          ["L3 V7 §0.2.1"], {"rc": 0},
                          {"rc": res.rc, "error": res.error_line() if res.rc else None}, res.rc == 0):
            raise Abort("V7 no se aplicó")

    def characterize_v7(self) -> None:
        self.characterization["v7_sin_overlay"] = self.q(SUMMARY_SQL)
        self.expect("V7-H05-SIN-PARTICION",
                    "Sin overlay, insertar en audit_events falla por falta de partición (H-05 reproducido)",
                    ["H-05", "L3 V7 §1.3"],
                    "BEGIN;\nINSERT INTO public.audit_events (id, action, entity_type, trace_id)"
                    " VALUES (gen_random_uuid(), 'c1_probe', 'c1', gen_random_uuid());\nROLLBACK;",
                    ("23514", "no partition of relation"))
        can = self.q("SELECT to_json(has_table_privilege('libox_app', 'public.markets', 'SELECT'))")
        self.check("V7-H06-SIN-GRANTS", "Sin overlay, libox_app no puede leer ni un catálogo (H-06 reproducido)",
                   ["H-06", "L3 V7 §1.4"], False, can, can is False)
        if self.cfg["api_defaults"]:
            exposed = self.q("SELECT to_json(has_table_privilege('anon', 'public.journal_lines', 'SELECT'))")
            self.check("V7-API-EXPUESTA",
                       "Sin overlay y con privilegios por defecto de API, anon puede leer journal_lines (riesgo reproducido)",
                       ["cierre-sql-pendientes.md"], True, exposed, exposed is True)
            service = self.q("SELECT to_json(has_table_privilege('service_role', 'public.journal_lines', 'UPDATE'))")
            self.check("V7-API-SERVICE-ROLE-EXPUESTA",
                       "Sin overlay, service_role con privilegios por defecto puede modificar journal_lines (riesgo reproducido)",
                       ["cierre-sql-pendientes.md"], True, service, service is True)

    def fingerprint(self) -> str:
        return self.q("SELECT to_json((" + FINGERPRINT_SQL + "))")

    def apply_overlay(self) -> None:
        ref = self.q("SELECT json_build_array(extract(year FROM date_trunc('month', now() AT TIME ZONE 'UTC'))::int,"
                     " extract(month FROM date_trunc('month', now() AT TIME ZONE 'UTC'))::int)")
        self.reference = (ref[0], ref[1])
        for path in overlay_files():
            res = self.installer_sql(path.read_text(encoding="utf-8"))
            if not self.check("OV-APLICA-" + path.stem, "El archivo del overlay se aplica sin errores",
                              [rel(path)], {"rc": 0},
                              {"rc": res.rc, "error": res.error_line() if res.rc else None}, res.rc == 0):
                raise Abort("overlay no aplicado: " + path.name)

    def check_invariance(self, before: str) -> None:
        after = self.fingerprint()
        self.check("OV-NO-MODIFICA-V7",
                   "El overlay no cambia columnas, restricciones, índices, disparadores, funciones ni dominios de V7",
                   ["Instrucción C1: overlay sobre V7 intacto"], before, after, before == after)

    def managed_parents(self) -> List[str]:
        return [p for p in v7_partitioned_parents(self.v7_text) if p not in HUMAN_PARTITIONED]

    def check_partitions(self) -> None:
        expected_parents = v7_partitioned_parents(self.v7_text)
        inventory = self.q(INVENTORY_SQL)
        catalog = self.q(PARENTS_CATALOG_SQL)
        keys = {k: v["clave"] for k, v in inventory.items()}
        provisioning = {k: v["aprovisionamiento"] for k, v in inventory.items()}
        wanted = {k: ("humano" if k in HUMAN_PARTITIONED else "overlay") for k in expected_parents}
        self.check("PT-INVENTARIO",
                   "Inventario del overlay = padres de V7 = catálogo (tabla y clave); solo journal_lines es de aporte humano",
                   ["H-05", "L3 V7 §1.3", "ZC ledger"], {"claves": expected_parents, "aprovisionamiento": wanted},
                   {"inventario": keys, "catalogo": catalog, "aprovisionamiento": provisioning},
                   keys == expected_parents == catalog and provisioning == wanted)
        children = self.q(CHILDREN_SQL, prelude="SET TimeZone = 'UTC';")
        year, month = self.reference
        diffs = {}
        for parent in expected_parents:
            if parent in HUMAN_PARTITIONED:
                want = None
            else:
                want = {parent + "_pdefault": "DEFAULT"}
                for k in range(HORIZON_MONTHS + 1):
                    y, m = add_months(year, month, k)
                    want[parent + "_p" + month_suffix(y, m)] = expected_bound(y, m)
            if children.get(parent) != want:
                diffs[parent] = {"esperado": want, "observado": children.get(parent)}
        self.check("PT-COBERTURA-UTC",
                   "Los 11 padres gestionados tienen mes actual y dos siguientes con límites exactos en UTC, más"
                   " DEFAULT; journal_lines no tiene hijos",
                   ["H-05 (parcial 11/12)", "L3 V7 §1.3", "C-11"], "sin diferencias", diffs or "sin diferencias",
                   not diffs)

    def check_human_parent_untouched(self) -> None:
        children = self.q(CHILDREN_SQL)
        res = self.admin("BEGIN;\nINSERT INTO public.journal_lines (id, entry_id, account_code, currency, debit)"
                         " VALUES (gen_random_uuid(), gen_random_uuid(), 'c1_probe', 'PEN', 1);\nROLLBACK;")
        observed = {"hijos": children.get("journal_lines"), "rc": res.rc,
                    "error": res.error_line() if res.rc else None}
        self.check("PT-JOURNAL-LINES-HUMANO",
                   "Tras todas las ejecuciones del overlay, journal_lines sigue sin particiones ni DEFAULT: su"
                   " escritura falla como en V7 hasta el aporte humano",
                   ["Revisor C1 (crítico)", "ZC ledger", "H-05 (parcial 11/12)"],
                   {"hijos": None, "sqlstate": "23514", "mensaje_contiene": "no partition of relation"}, observed,
                   children.get("journal_lines") is None and res.failed_with("23514", "no partition of relation"))

    def check_idempotency(self) -> None:
        before = self.q(SNAPSHOT_SQL, prelude="SET TimeZone = 'UTC';")
        path = OVERLAY_DIR / "040_arranque_particiones.sql"
        res = self.installer_sql(path.read_text(encoding="utf-8"))
        actions = sorted({line.split("|")[-1] for line in res.out.splitlines() if "|" in line})
        after = self.q(SNAPSHOT_SQL, prelude="SET TimeZone = 'UTC';")
        ok = res.rc == 0 and actions == ["exists", "exists_default"] and before == after
        self.check("PT-IDEMPOTENCIA",
                   "Reejecutar el arranque no crea relaciones ni cambia límites o ACL",
                   ["Instrucción C1: idempotente"],
                   {"acciones": ["exists", "exists_default"], "catalogo_igual": True},
                   {"rc": res.rc, "acciones": actions, "catalogo_igual": before == after}, ok)

    def check_reference_timezone(self) -> None:
        # 2031-06-30 22:00 en Lima = 2031-07-01 03:00 UTC: el mes debe ser julio (UTC).
        literal = "2031-06-30 22:00:00"
        res = self.installer_sql("SET TimeZone = 'America/Lima';\n"
                                 "SELECT count(*) FROM libox_ops.ensure_monthly_partitions(" + sql_text(literal) + ", 0);")
        month = utc_month_of(literal)
        y, m = int(month[:4]), int(month[4:])
        seen = self.q("SELECT json_build_object('esperada', (SELECT pg_get_expr(relpartbound, oid) FROM pg_class"
                      " WHERE relname = " + sql_text("audit_events_p" + month) + "), 'mes_local',"
                      " EXISTS (SELECT 1 FROM pg_class WHERE relname = " + sql_text("audit_events_p203106") + "))",
                      prelude="SET TimeZone = 'UTC';")
        ok = res.rc == 0 and seen["esperada"] == expected_bound(y, m) and seen["mes_local"] is False
        self.check("PT-REFERENCIA-UTC",
                   "Con sesión en America/Lima, la referencia se convierte a UTC: 30-jun 22:00 local crea julio, no junio",
                   ["Instrucción C1: UTC explícito"],
                   {"particion": "audit_events_p" + month, "limites": expected_bound(y, m), "existe_p203106": False},
                   {"rc": res.rc, "limites": seen.get("esperada"), "existe_p203106": seen.get("mes_local")}, ok)

    def check_boundary_utc(self) -> None:
        res = self.installer_sql("SELECT count(*) FROM libox_ops.ensure_monthly_partitions('2030-01-15T12:00:00+00:00', 1);")
        if not self.check("PT-FRONTERA-PREPARA", "Se crean enero y febrero de 2030 con referencia explícita",
                          ["Instrucción C1"], {"rc": 0}, {"rc": res.rc, "error": res.error_line() if res.rc else None},
                          res.rc == 0):
            return
        created = {month_suffix(*add_months(self.reference[0], self.reference[1], k))
                   for k in range(HORIZON_MONTHS + 1)} | {"203001", "203002"}
        cases = [
            ("analytics_events", "server_ts", "2030-01-31T23:59:59.999999+00:00"),
            ("analytics_events", "server_ts", "2030-02-01T00:00:00+00:00"),
            ("analytics_events", "server_ts", "2030-01-31T19:00:00-05:00"),
            ("analytics_events", "server_ts", "2030-01-31T18:59:59.999999-05:00"),
            ("analytics_events", "server_ts", "2030-01-31 20:00:00"),
            ("audit_events", "created_at", "2030-02-28T23:59:59.999999+00:00"),
            ("audit_events", "created_at", "2030-03-01T00:00:00+00:00"),
        ]
        ids = []
        app_rows, append_rows, expected = [], [], {}
        for table, _column, literal in cases:
            row_id = str(uuid.uuid4())
            ids.append(row_id)
            month = utc_month_of(literal)
            expected[row_id] = {"tabla": table, "literal": literal,
                                "particion": table + ("_p" + month if month in created else "_pdefault")}
            if table == "analytics_events":
                app_rows.append("(" + sql_text(row_id) + ", 'c1_probe', gen_random_uuid(), gen_random_uuid(),"
                                " 'c1', 'PE', " + sql_text(literal) + ")")
            else:
                append_rows.append("(" + sql_text(row_id) + ", 'c1_probe', 'c1', gen_random_uuid(), "
                                   + sql_text(literal) + ")")
        prelude = ("BEGIN;\nSET LOCAL TimeZone = 'America/Lima';\nSET LOCAL ROLE libox_app;\n"
                   "INSERT INTO public.analytics_events (id, event_name, trace_id, session_id, app_version,"
                   " market_code, server_ts) VALUES " + ", ".join(app_rows) + ";\n"
                   "SET LOCAL ROLE libox_append;\n"
                   "INSERT INTO public.audit_events (id, action, entity_type, trace_id, created_at) VALUES "
                   + ", ".join(append_rows) + ";\nRESET ROLE;\n")
        id_list = ", ".join(sql_text(i) + "::uuid" for i in ids)
        try:
            located = self.q("SELECT json_object_agg(id::text, (SELECT relname FROM pg_class WHERE oid = s.tableoid))"
                             " FROM (SELECT id, tableoid FROM public.analytics_events WHERE id IN (" + id_list + ")"
                             " UNION ALL SELECT id, tableoid FROM public.audit_events WHERE id IN (" + id_list + ")) s",
                             prelude=prelude)
            error = None
        except RuntimeError as exc:
            located, error = {}, str(exc)
        wrong = {k: {"esperado": v, "observado": located.get(k)} for k, v in expected.items()
                 if located.get(k) != v["particion"]}
        self.check("PT-FRONTERA-UTC",
                   "Filas en la frontera de mes caen en la partición del mes UTC, con sesión en America/Lima;"
                   " fuera de los meses creados caen en DEFAULT",
                   ["Instrucción C1: frontera UTC", "L3 V7 §1.3"], "sin diferencias",
                   {"error": error, "diferencias": wrong} if (wrong or error) else "sin diferencias",
                   not wrong and error is None)

    def check_out_of_range(self) -> None:
        row_id = str(uuid.uuid4())
        literal = "2099-06-01T00:00:00+00:00"
        insert = ("SET ROLE libox_app;\nINSERT INTO public.analytics_events (id, event_name, trace_id, session_id,"
                  " app_version, market_code, server_ts) VALUES (" + sql_text(row_id) + ", 'c1_probe',"
                  " gen_random_uuid(), gen_random_uuid(), 'c1', 'PE', " + sql_text(literal) + ");")
        res = self.admin(insert)
        where = self.q("SELECT to_json((SELECT relname FROM pg_class WHERE oid = (SELECT tableoid FROM"
                       " public.analytics_events WHERE id = " + sql_text(row_id) + "::uuid)))")
        self.check("PT-FUERA-DE-RANGO-ESCRIBE",
                   "Una fila sin partición mensual se conserva en la DEFAULT en vez de fallar (L3 V7 §1.3)",
                   ["L3 V7 §1.3", "H-05"], "analytics_events_pdefault",
                   {"rc": res.rc, "particion": where}, res.rc == 0 and where == "analytics_events_pdefault")
        status = self.q("SELECT json_object_agg(parent_table, json_build_object('actual', has_current,"
                        " 'default_filas', default_rows)) FROM libox_ops.partition_status('2099-06-10T00:00:00+00:00')")
        others = {k: v for k, v in status.items() if k not in ["analytics_events"] + HUMAN_PARTITIONED
                  and v["default_filas"] != 0}
        others.update({k: status.get(k) for k in HUMAN_PARTITIONED
                       if status.get(k) != {"actual": False, "default_filas": None}})
        self.check("PT-ALARMA-DEFAULT",
                   "partition_status informa la fila en DEFAULT y la falta del mes (insumo de la alarma alta)",
                   ["L3 V7 §1.3"], {"analytics_events": {"actual": False, "default_filas": 1}, "otros_con_filas": {}},
                   {"analytics_events": status.get("analytics_events"), "otros_con_filas": others},
                   status.get("analytics_events") == {"actual": False, "default_filas": 1} and not others)
        self.expect("PT-DEFAULT-CON-FILAS-FALLA",
                    "Crear el mes cuando la DEFAULT tiene filas de ese rango falla con mensaje claro",
                    ["Instrucción C1: fallo claro, sin mover datos"],
                    "SELECT * FROM libox_ops.ensure_monthly_partitions('2099-06-10T00:00:00+00:00', 0);",
                    ("P0001", "LIBOX_PARTITION_DEFAULT_HAS_ROWS"), user=self.installer)
        after = self.q("SELECT json_build_object('en_default', (SELECT count(*) FROM public.analytics_events_pdefault"
                       " WHERE id = " + sql_text(row_id) + "::uuid), 'particiones_209906',"
                       " (SELECT count(*) FROM pg_class WHERE right(relname, 8) = '_p209906'))")
        self.check("PT-SIN-MOVER-NI-BORRAR",
                   "Tras el fallo la fila sigue en DEFAULT y no quedó ninguna partición 2099-06 (sin efectos parciales)",
                   ["Instrucción C1"], {"en_default": 1, "particiones_209906": 0}, after,
                   after == {"en_default": 1, "particiones_209906": 0})

    def check_negative_paths(self) -> None:
        self.expect("PT-LIMITES-DISTINTOS",
                    "Una relación con el nombre esperado y otros límites provoca fallo explícito",
                    ["Instrucción C1: fallo claro"],
                    "BEGIN;\nCREATE TABLE public.notification_attempts_p204001 PARTITION OF public.notification_attempts"
                    " FOR VALUES FROM ('2040-01-01 00:00:00+00') TO ('2040-01-15 00:00:00+00');\n"
                    "SELECT * FROM libox_ops.ensure_monthly_partitions('2040-01-10T00:00:00+00:00', 0);\nROLLBACK;",
                    ("P0001", "LIBOX_PARTITION_BOUNDS_MISMATCH"), user=self.installer)
        self.expect("PT-INVENTARIO-DERIVA",
                    "Un padre particionado no inventariado detiene la creación",
                    ["Instrucción C1: fallo claro"],
                    "BEGIN;\nCREATE TABLE public.c1_probe_unlisted (id int, ts timestamptz) PARTITION BY RANGE (ts);\n"
                    "SELECT * FROM libox_ops.ensure_monthly_partitions();\nROLLBACK;",
                    ("P0001", "LIBOX_PARTITION_INVENTORY_MISMATCH"), user=self.installer)
        self.expect("PT-ARGUMENTOS", "Horizonte fuera de 0..12 se rechaza",
                    ["Instrucción C1"],
                    "SELECT * FROM libox_ops.ensure_monthly_partitions(now(), 13);",
                    ("P0001", "LIBOX_PARTITION_ARG"), user=self.installer)

    def check_seeds(self) -> None:
        literals = l3_market_literals(L3_DOC.read_text(encoding="utf-8"))
        row = self.q("SELECT row_to_json(m) FROM (SELECT code, currency, timezone, locale, name, status"
                     " FROM public.markets WHERE code = 'PE') m")
        observed = {k: (row or {}).get(k) for k in literals}
        self.check("SD-PE-LITERAL", "markets PE coincide con los literales de L3 V7 §10.1 leídos del documento",
                   ["L3 V7 §10.1"], literals, {"literales": observed, "name_no_literal": (row or {}).get("name"),
                                               "status_default_v7": (row or {}).get("status")},
                   observed == literals)
        path = OVERLAY_DIR / "030_semilla_mercado_pe.sql"
        seed = path.read_text(encoding="utf-8")
        res = self.installer_sql(seed)
        count = self.q("SELECT to_json(count(*)) FROM public.markets")
        self.check("SD-PE-IDEMPOTENTE", "Reaplicar la semilla no duplica ni falla",
                   [rel(path)], {"rc": 0, "filas": 1}, {"rc": res.rc, "filas": count}, res.rc == 0 and count == 1)
        self.expect("SD-PE-DERIVA", "Si PE existe con otros valores, la semilla falla y no sobrescribe",
                    [rel(path)],
                    "BEGIN;\nUPDATE public.markets SET timezone = 'UTC' WHERE code = 'PE';\n" + seed + "\nROLLBACK;",
                    ("P0001", "LIBOX_SEED_DRIFT"), user=self.installer)
        counts = self.q("SELECT json_build_object(" + ", ".join(
            sql_text(t) + ", (SELECT count(*) FROM public." + t + ")"
            for t in SEED_EMPTY_TABLES + ["raffle_type_rules", "subrole_grant_matrix"]) + ")")
        invented = {t: counts[t] for t in SEED_EMPTY_TABLES if counts[t] != 0}
        unchanged = counts["raffle_type_rules"] == 8 and counts["subrole_grant_matrix"] == 14
        self.check("SD-NO-INVENTADAS",
                   "El overlay no siembra FSM, ledger, incompatibilidades, configuración financiera ni admins;"
                   " conserva las semillas de V7",
                   ["Instrucción C1: no inventar"],
                   {"tablas_vacias": SEED_EMPTY_TABLES, "raffle_type_rules": 8, "subrole_grant_matrix": 14},
                   {"con_filas": invented, "raffle_type_rules": counts["raffle_type_rules"],
                    "subrole_grant_matrix": counts["subrole_grant_matrix"]}, not invented and unchanged)

    def check_acl_behaviour(self) -> None:
        y, m = self.reference
        current = month_suffix(y, m)
        analytics = ("INSERT INTO public.analytics_events (id, event_name, trace_id, session_id, app_version,"
                     " market_code) VALUES (gen_random_uuid(), 'c1_probe', gen_random_uuid(), gen_random_uuid(),"
                     " 'c1', 'PE');")
        audit = ("INSERT INTO public.audit_events (id, action, entity_type, trace_id) VALUES"
                 " (gen_random_uuid(), 'c1_probe', 'c1', gen_random_uuid());")
        denied = ("42501", "permission denied")
        refs = ["H-06 (parcial)", "L3 V7 §1.4", "acl-manifest.json"]
        self.expect("ACL-APP-INSERTA-TELEMETRIA", "libox_app inserta telemetría por la tabla padre", refs,
                    self.as_role("libox_app", analytics))
        self.expect("ACL-APP-PARTICION-DIRECTA", "libox_app no escribe directamente en una partición", refs,
                    self.as_role("libox_app", analytics.replace("public.analytics_events ",
                                                                "public.analytics_events_p" + current + " ")), denied)
        for verb, body in (("UPDATE", "UPDATE public.analytics_events SET event_name = 'x';"),
                           ("DELETE", "DELETE FROM public.analytics_events;"),
                           ("TRUNCATE", "TRUNCATE public.analytics_events;")):
            self.expect("ACL-APP-NO-" + verb + "-TELEMETRIA", "libox_app no puede " + verb + " en telemetría",
                        refs, self.as_role("libox_app", body), denied)
        self.expect("ACL-APPEND-INSERTA-AUDITORIA", "libox_append inserta en audit_events", refs + ["C-08"],
                    self.as_role("libox_append", audit))
        for verb, body in (("UPDATE", "UPDATE public.audit_events SET reason = 'x';"),
                           ("DELETE", "DELETE FROM public.audit_events;"),
                           ("TRUNCATE", "TRUNCATE public.audit_events;")):
            self.expect("ACL-APPEND-NO-" + verb, "libox_append no puede " + verb + " en audit_events",
                        refs + ["C-08"], self.as_role("libox_append", body), denied)
        self.expect("ACL-APPEND-PARTICION-DIRECTA", "libox_append no escribe directamente en una partición",
                    refs, self.as_role("libox_append", audit.replace("public.audit_events ",
                                                                     "public.audit_events_p" + current + " ")), denied)
        reserved = [
            ("JOURNAL-LINES", "INSERT INTO public.journal_lines (id, entry_id, account_code, currency, debit)"
                              " VALUES (gen_random_uuid(), gen_random_uuid(), 'x', 'PEN', 1);"),
            ("JOURNAL-ENTRIES", "SELECT count(*) FROM public.journal_entries;"),
            ("RAFFLES-STATUS", "UPDATE public.raffles SET status = 'ACTIVE';"),
            ("ORDERS", "SELECT count(*) FROM public.orders;"),
            ("TICKETS", "INSERT INTO public.tickets (id) VALUES (gen_random_uuid());"),
            ("SUBROLES", "SELECT count(*) FROM public.subrole_assignments;"),
            ("SETTLEMENTS", "SELECT count(*) FROM public.settlements;"),
        ]
        for label, body in reserved:
            self.expect("ACL-APP-RESERVADO-" + label, "libox_app sin privilegio sobre tabla reservada a humano",
                        refs + ["zonas-sin-ia"], self.as_role("libox_app", body), denied)
        self.expect("ACL-READ-LEE-CATALOGO", "libox_read lee un catálogo", refs,
                    self.as_role("libox_read", "SELECT count(*) FROM public.markets;"))
        self.expect("ACL-READ-NO-ESCRIBE", "libox_read no escribe", refs,
                    self.as_role("libox_read", "INSERT INTO public.markets (code, name, currency, timezone, locale)"
                                               " VALUES ('XX', 'x', 'XXX', 'UTC', 'x');"), denied)
        self.expect("ACL-READ-NO-AUDITORIA", "libox_read no lee auditoría", refs,
                    self.as_role("libox_read", "SELECT count(*) FROM public.audit_events;"), denied)
        self.expect("ACL-MIGRATE-SIN-DATOS", "libox_migrate no tiene uso del esquema de dominio", refs,
                    self.as_role("libox_migrate", "SELECT count(*) FROM public.markets;"), denied)
        self.expect("ACL-OPS-SIN-EXECUTE", "libox_app no ejecuta funciones de libox_ops", refs,
                    self.as_role("libox_app", "SELECT * FROM libox_ops.partition_status();"), denied)
        res = self.admin("CREATE ROLE c1_probe_public LOGIN;\n"
                         "CREATE ROLE c1_probe_app LOGIN IN ROLE libox_app;")
        if res.rc != 0:
            self.check("ACL-LOGIN-PREPARA", "Roles de login de prueba", refs, {"rc": 0},
                       {"rc": res.rc, "error": res.error_line()}, False)
            return
        self.expect("ACL-PUBLIC-SIN-ESQUEMA", "Un login sin membresías (solo PUBLIC) no accede al esquema de dominio",
                    refs, "SELECT 1 FROM public.markets LIMIT 1;", denied, user="c1_probe_public")
        self.expect("ACL-PUBLIC-SIN-OPS", "Un login sin membresías no ejecuta libox_ops",
                    refs, "SELECT * FROM libox_ops.partition_status();", denied, user="c1_probe_public")
        self.expect("ACL-LOGIN-MIEMBRO-INSERTA", "Un login técnico miembro de libox_app hereda su inserción",
                    refs, "BEGIN;\n" + analytics + "\nROLLBACK;", user="c1_probe_app")
        self.expect("ACL-LOGIN-MIEMBRO-NO-BORRA", "Un login técnico miembro de libox_app no borra",
                    refs, "DELETE FROM public.analytics_events;", denied, user="c1_probe_app")
        self.expect("ACL-DISPARADOR-V7-SIN-EXECUTE",
                    "Revocar EXECUTE a PUBLIC no impide que un disparador V7 se ejecute (lo demuestra su propio error)",
                    refs + ["V7 assert_grant_ceiling (solo observado)"],
                    "BEGIN;\nCREATE ROLE c1_probe_trigger;\n"
                    "GRANT USAGE ON SCHEMA public TO c1_probe_trigger;\n"
                    "GRANT INSERT ON public.subrole_assignments TO c1_probe_trigger;\n"
                    "DO $p$ BEGIN IF has_function_privilege('c1_probe_trigger', 'public.assert_grant_ceiling()',"
                    " 'EXECUTE') THEN RAISE EXCEPTION 'c1 probe: el rol tiene EXECUTE'; END IF; END $p$;\n"
                    "SET LOCAL ROLE c1_probe_trigger;\n"
                    "INSERT INTO public.subrole_assignments (id, user_id, subrole, granted_by, reason) VALUES"
                    " (gen_random_uuid(), '00000000-0000-4000-8000-0000000000c1', 'SUPPORT_L1',"
                    " '00000000-0000-4000-8000-0000000000c1', 'c1 probe');\nROLLBACK;",
                    ("P0001", "ERR_RBAC_SELF_GRANT"))
        if self.cfg["api_defaults"]:
            self.expect("ACL-API-ANON-SIN-ACCESO", "anon no accede tras el overlay", refs + ["cierre-sql-pendientes.md"],
                        self.as_role("anon", "SELECT count(*) FROM public.journal_lines;"), denied)
            self.expect("ACL-API-SERVICE-ROLE-SIN-ACCESO", "service_role no modifica journal_lines tras el overlay",
                        refs + ["cierre-sql-pendientes.md"],
                        self.as_role("service_role", "UPDATE public.journal_lines SET debit = debit;"), denied)

    def check_horizon_30d(self) -> None:
        cases = [("2027-01-30T00:00:00+00:00", 1, False, "2027-03-01T00:00:00+00:00"),
                 ("2027-01-30T00:00:00+00:00", 2, True, "2027-04-01T00:00:00+00:00"),
                 ("2027-02-01T00:00:00+00:00", None, True, "2027-05-01T00:00:00+00:00")]
        observed, ok = [], True
        for ref, horizon, want_ok, want_until in cases:
            call = ("libox_ops.ensure_monthly_partitions(" + sql_text(ref)
                    + ("" if horizon is None else ", " + str(horizon)) + ")")
            status = self.q("SELECT json_object_agg(parent_table, json_build_object('hasta', covered_until,"
                            " 'ok', coverage_ok)) FROM libox_ops.partition_status(" + sql_text(ref) + ")",
                            prelude="BEGIN;\nSET TimeZone = 'UTC';\nSELECT count(*) FROM " + call + ";",
                            user=self.installer)
            managed = {k: v for k, v in status.items() if k not in HUMAN_PARTITIONED}
            wrong = {k: v for k, v in managed.items() if v != {"hasta": want_until, "ok": want_ok}}
            human = {k: status.get(k) for k in HUMAN_PARTITIONED}
            good = len(managed) == 11 and not wrong and all(v == {"hasta": None, "ok": False} for v in human.values())
            ok = ok and good
            observed.append({"referencia": ref, "horizonte": horizon if horizon is not None else "por defecto",
                             "esperado": {"hasta": want_until, "ok": want_ok}, "gestionados_distintos": wrong,
                             "humano": human, "gestionados": len(managed)})
        self.check("PT-HORIZONTE-30D",
                   "Cobertura de 30 días (L3 V7 §1.3): el 30-ene-2027 con horizonte 1 falla (marzo solo con 28 días);"
                   " con horizonte 2 y por defecto desde el 1-feb-2027 existe el tercer mes",
                   ["Revisor C1 I2", "L3 V7 §1.3"], "sin diferencias", observed, ok)

    def check_lock_timeout(self) -> None:
        holder = self.pg.psql_background("BEGIN;\nLOCK TABLE public.audit_events IN ACCESS EXCLUSIVE MODE;\n"
                                         "SELECT pg_sleep(40);\nCOMMIT;\n", user="postgres", db=DB)
        held, elapsed, res = False, None, None
        try:
            for _ in range(60):
                held = self.q("SELECT to_json(EXISTS (SELECT 1 FROM pg_locks l JOIN pg_class c ON c.oid = l.relation"
                              " WHERE c.relname = 'audit_events' AND l.mode = 'AccessExclusiveLock'"
                              " AND l.granted AND l.pid <> pg_backend_pid()))")
                if held:
                    break
                time.sleep(0.25)
            start = time.monotonic()
            res = self.pg.psql("SELECT * FROM libox_ops.ensure_monthly_partitions('2032-05-10T00:00:00+00:00', 0);",
                               user=self.installer, db=DB)
            elapsed = round(time.monotonic() - start, 1)
        finally:
            self.admin("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '" + DB + "'"
                       " AND pid <> pg_backend_pid() AND query LIKE '%pg_sleep(40)%';")
            try:
                holder.wait(timeout=30)
            except subprocess.TimeoutExpired:
                holder.kill()
                holder.wait(timeout=30)
            finally:
                for stream in (holder.stdout, holder.stderr):
                    if stream is not None:
                        stream.close()
        leftover = self.q("SELECT to_json(count(*)) FROM pg_class WHERE right(relname, 8) = '_p203205'")
        ok = (held is True and res is not None and res.failed_with("55P03", "lock timeout")
              and elapsed is not None and elapsed < 20 and leftover == 0)
        self.check("PT-LOCK-TIMEOUT",
                   "Con audit_events bloqueado por otra sesión, ensure falla por lock_timeout (5 s) sin crear"
                   " particiones, en vez de esperar indefinidamente",
                   ["Revisor C1 M2"], {"sqlstate": "55P03", "segundos_max": 20, "particiones_203205": 0},
                   {"bloqueo_tomado": held, "error": res.error_line() if res is not None and res.rc else None,
                    "segundos": elapsed, "particiones_203205": leftover}, ok)

    def check_partition_acl_generic(self) -> None:
        roles = "service_role, c1_custom_reader"
        grant = "ALTER DEFAULT PRIVILEGES FOR ROLE " + self.installer + " IN SCHEMA public "
        setup = self.admin("DO $r$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'service_role')"
                           " THEN CREATE ROLE service_role NOLOGIN; END IF; END $r$;\n"
                           "CREATE ROLE c1_custom_reader NOLOGIN;\n" + grant + "GRANT ALL ON TABLES TO " + roles + ";")
        sanity = self.q("SELECT json_build_object('service_role', has_table_privilege('service_role',"
                        " 'public.c1_probe_sanity', 'UPDATE'), 'c1_custom_reader',"
                        " has_table_privilege('c1_custom_reader', 'public.c1_probe_sanity', 'SELECT'))",
                        prelude="BEGIN;\nCREATE TABLE public.c1_probe_sanity (id integer);", user=self.installer)
        created = self.installer_sql("SELECT count(*) FROM libox_ops.ensure_monthly_partitions("
                                     "'2033-03-10T00:00:00+00:00', 0);")
        rows = self.q(NON_OWNER_GRANTEES_SQL)
        on_partitions = [r for r in rows if r[0] == "particion"]
        new_parts = self.q("SELECT to_json(count(*)) FROM pg_class WHERE relispartition"
                           " AND right(relname, 8) = '_p203303'")
        restore = self.admin(grant + "REVOKE ALL ON TABLES FROM " + roles + ";")
        ok = (setup.rc == 0 and sanity == {"service_role": True, "c1_custom_reader": True} and created.rc == 0
              and new_parts == 11 and not on_partitions and restore.rc == 0)
        self.check("PT-ACL-PARTICIONES",
                   "Con privilegios por defecto para service_role y un rol propio, ninguna partición gestionada (nuevas"
                   " ni previas) tiene beneficiarios distintos del dueño",
                   ["Revisor C1 I3"], {"control_por_defecto_activo": True, "nuevas": 11, "con_beneficiarios": []},
                   {"control_por_defecto_activo": sanity, "nuevas": new_parts, "con_beneficiarios": on_partitions[:40],
                    "rc": [setup.rc, created.rc, restore.rc],
                    "error": created.error_line() if created.rc else None}, ok)

    def check_new_object_probe(self) -> None:
        prelude = ("BEGIN;\n"
                   "CREATE FUNCTION public.c1_probe_fn() RETURNS integer LANGUAGE sql AS $f$SELECT 1$f$;\n"
                   "CREATE FUNCTION libox_ops.c1_probe_fn() RETURNS integer LANGUAGE sql AS $f$SELECT 1$f$;\n"
                   "CREATE TABLE public.c1_probe_tbl (id integer);\n"
                   "CREATE TABLE libox_ops.c1_probe_tbl (id integer);\n")
        rows = self.q("SELECT coalesce(json_agg(r), '[]') FROM json_array_elements((" + NON_OWNER_GRANTEES_SQL
                      + ")) r WHERE r->>2 LIKE 'c1_probe_%'", prelude=prelude, user=self.installer)
        self.check("ACL-SONDA-OBJETOS-NUEVOS",
                   "Funciones y tablas creadas después por el instalador (transacción revertida) no reciben EXECUTE"
                   " ni privilegios para PUBLIC ni otros roles, aunque pg_default_acl esté vacío",
                   ["Revisor C1 I4"], [], rows, rows == [])

    def check_acl_grantees(self) -> None:
        rows = self.q(NON_OWNER_GRANTEES_SQL)
        bad = [r for r in rows
               if not (r[0] in ("relacion", "esquema") and r[1] == "public" and r[3] in ALLOWED_GRANTEES)]
        self.check("ACL-BENEFICIARIOS",
                   "Todo beneficiario distinto del dueño es un rol de grupo permitido sobre una tabla padre o el"
                   " esquema public; ninguno en particiones, funciones ni libox_ops (cualquier rol, no solo el manifiesto)",
                   ["Revisor C1 I3/I4"], [], {"indebidos": bad[:40], "total": len(bad),
                                              "beneficiarios_revisados": len(rows)}, not bad)

    def check_acl_matrix(self) -> None:
        privileges = ["SELECT", "INSERT", "UPDATE", "DELETE", "TRUNCATE", "REFERENCES", "TRIGGER"]
        if self.version_num >= 170000:
            privileges.append("MAINTAIN")
        roles = list(self.manifest["roles_grupo"])
        self.api_roles = [r for r in self.manifest["roles_api_denegados"]
                          if self.q("SELECT to_json(EXISTS (SELECT 1 FROM pg_roles WHERE rolname = " + sql_text(r) + "))")]
        roles += self.api_roles
        rows = self.q(
            "SELECT json_agg(json_build_array(n.nspname, c.relname, c.relispartition, r.rolname,"
            " (SELECT coalesce(json_agg(p ORDER BY p), '[]') FROM unnest(ARRAY[" + ", ".join(sql_text(p) for p in privileges)
            + "]) p WHERE has_table_privilege(r.oid, c.oid, p))))"
            " FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace CROSS JOIN pg_roles r"
            " WHERE n.nspname IN ('public', 'libox_ops') AND c.relkind IN ('r', 'p')"
            " AND r.rolname IN (" + ", ".join(sql_text(r) for r in roles) + ")")
        classes = self.manifest["clases"]
        tables = self.manifest["tablas"]
        mismatches, unknown = [], set()
        checked = 0
        for schema, table, is_partition, role, granted in rows:
            if schema == "public" and not is_partition:
                if table not in tables:
                    unknown.add(table)
                    wanted: List[str] = []
                else:
                    wanted = sorted(classes[tables[table]]["privilegios"].get(role, []))
            else:
                wanted = []
            checked += 1
            if sorted(granted) != wanted:
                mismatches.append({"esquema": schema, "tabla": table, "particion": is_partition, "rol": role,
                                   "esperado": wanted, "observado": granted})
        self.check("ACL-MATRIZ",
                   "Privilegios efectivos de roles de grupo y API = manifiesto; ninguno directo sobre particiones ni libox_ops",
                   ["H-06 (parcial)", "acl-manifest.json"],
                   {"diferencias": [], "tablas_sin_clasificar": []},
                   {"pares_revisados": checked, "diferencias": mismatches[:40],
                    "total_diferencias": len(mismatches), "tablas_sin_clasificar": sorted(unknown)},
                   not mismatches and not unknown and checked > 0)
        public = self.q(PUBLIC_ACL_SQL)
        self.check("ACL-PUBLIC", "PUBLIC sin privilegios en relaciones, esquemas y funciones de public y libox_ops",
                   ["Instrucción C1: denegar PUBLIC"], {"relaciones": [], "esquemas": [], "funciones": []}, public,
                   public == {"relaciones": [], "esquemas": [], "funciones": []})
        defaults = self.q(DEFAULT_ACL_SQL)
        bad = [d for d in defaults if d["beneficiario"] in ["PUBLIC"] + self.manifest["roles_api_denegados"]]
        self.check("ACL-POR-DEFECTO",
                   "Privilegios por defecto sin concesiones a PUBLIC ni a roles de API",
                   ["Instrucción C1"], [], {"indebidos": bad, "todos": defaults}, not bad)
        fn_roles = roles
        fn = self.q("SELECT coalesce(json_agg(json_build_array(p.proname, r.rolname)), '[]')"
                    " FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace CROSS JOIN pg_roles r"
                    " WHERE n.nspname IN ('libox_ops', 'public') AND r.rolname IN ("
                    + ", ".join(sql_text(r) for r in fn_roles) + ") AND has_function_privilege(r.oid, p.oid, 'EXECUTE')")
        self.check("ACL-FUNCIONES", "Roles de grupo y API sin EXECUTE sobre funciones de public y libox_ops",
                   ["Instrucción C1"], [], fn, fn == [])

    def probe_open_findings(self) -> None:
        u = "00000000-0000-4000-8000-0000000000"
        users = ("INSERT INTO public.users (id, market_code, email, phone, birth_date) VALUES"
                 " ('" + u + "01', 'PE', 'c1-probe-1@example.invalid', '+51900000001', '1990-01-01'),"
                 " ('" + u + "02', 'PE', 'c1-probe-2@example.invalid', '+51900000002', '1990-01-01'),"
                 " ('" + u + "03', 'PE', 'c1-probe-3@example.invalid', '+51900000003', '1990-01-01');\n")
        disable = "ALTER TABLE public.subrole_assignments DISABLE TRIGGER trg_grant_ceiling;\n"
        enable = "ALTER TABLE public.subrole_assignments ENABLE TRIGGER trg_grant_ceiling;\n"
        # H-07: con dos ADMIN_SUPER activos, revocar uno debería rechazarse (PRD V9 INV-38).
        prelude = ("BEGIN;\n" + disable + users +
                   "INSERT INTO public.subrole_assignments (id, user_id, subrole, granted_by, reason) VALUES"
                   " ('" + u + "11', '" + u + "01', 'ADMIN_SUPER', '" + u + "99', 'c1 probe'),"
                   " ('" + u + "12', '" + u + "02', 'ADMIN_SUPER', '" + u + "99', 'c1 probe');\n"
                   + enable +
                   "UPDATE public.subrole_assignments SET revoked_at = now(), revoked_by = '" + u + "02',"
                   " revoke_reason = 'c1 probe' WHERE id = '" + u + "11';\n")
        self.open_findings.append(self._probe(
            "H-07", "PRD V9 l.450 (INV-38): impide revocar al penúltimo ADMIN_SUPER",
            prelude, "SELECT to_json(count(*)) FROM public.subrole_assignments WHERE subrole = 'ADMIN_SUPER'"
                     " AND revoked_at IS NULL",
            lambda v: "abierto: se admitió revocar al penúltimo; quedan " + str(v) + " activos" if v == 1 else None,
            "ERR_RBAC_LAST_SUPER_ADMIN"))
        # H-09: reactivar por UPDATE una asignación revocada que exige segunda firma.
        prelude = ("BEGIN;\n" + disable + users +
                   "INSERT INTO public.subrole_assignments (id, user_id, subrole, granted_by, reason) VALUES"
                   " ('" + u + "11', '" + u + "01', 'ADMIN_SUPER', '" + u + "99', 'c1 probe');\n"
                   "INSERT INTO public.subrole_assignments (id, user_id, subrole, granted_by, second_signer_id, reason,"
                   " revoked_at, revoked_by, revoke_reason) VALUES ('" + u + "13', '" + u + "03',"
                   " 'ADMIN_FINANCE', '" + u + "01', '" + u + "02', 'c1 probe', now(), '" + u + "01',"
                   " 'c1 probe');\n" + enable +
                   "UPDATE public.subrole_assignments SET revoked_at = NULL, revoked_by = NULL, revoke_reason = NULL,"
                   " second_signer_id = NULL, granted_by = '" + u + "01' WHERE id = '" + u + "13';\n")
        self.open_findings.append(self._probe(
            "H-09", "L3 V7 §3.16: techo y segunda firma al otorgar ADMIN_FINANCE",
            prelude, "SELECT to_json(count(*)) FROM public.subrole_assignments WHERE id = '" + u + "13'"
                     " AND revoked_at IS NULL AND second_signer_id IS NULL",
            lambda v: "abierto: reactivado por UPDATE sin segunda firma" if v == 1 else None,
            "ERR_RBAC_SECOND_SIGNATURE_REQUIRED"))

    def _probe(self, fid: str, canon: str, prelude: str, query: str, judge, closing_error: str) -> dict:
        entry = {"id": fid, "canon": canon, "transaccion_revertida": True,
                 "nota": "Sonda de caracterización sobre código V7 existente; no es implementación ni prueba superada."}
        try:
            value = self.q(query, prelude=prelude)
            verdict = judge(value)
            entry.update({"observado": value, "estado": verdict or "no reproducido: revisar"})
        except RuntimeError as exc:
            text = str(exc)
            state = "no reproducido: el esquema rechazó" if closing_error in text else "error de sonda"
            entry.update({"observado": text, "estado": state})
        return entry

    def catalog(self) -> dict:
        return {
            "resumen": self.q(SUMMARY_SQL),
            "hijos_por_padre": self.q(CHILDREN_SQL, prelude="SET TimeZone = 'UTC';"),
            "roles": self.q("SELECT json_agg(row_to_json(r) ORDER BY r.rolname) FROM (SELECT rolname, rolsuper,"
                            " rolcreaterole, rolcanlogin, rolbypassrls FROM pg_roles WHERE rolname LIKE 'libox%'"
                            " OR rolname IN ('anon', 'authenticated', 'service_role', 'c1_custom_reader')) r"),
            "privilegios_por_defecto": self.q(DEFAULT_ACL_SQL),
        }


def run_scenario(name: str, image: str, allow_pull: bool, manifest: dict, v7_text: str) -> dict:
    generated = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    sources = [V7_SQL, L3_DOC, MANIFEST] + overlay_files() + [Path(__file__), Path(pgdocker.__file__)]
    evidence = {
        "tipo": "evidencia-c1-sql-overlay",
        "esquema_evidencia": 2,
        "generado_utc": generated,
        "escenario": name,
        "descripcion_escenario": SCENARIOS[name]["descripcion"],
        "alcance": "C1: despliegue no crítico (particiones, ACL base, semilla PE). No R1.",
        "advertencias": ADVERTENCIAS,
        "fuentes": [{"ruta": rel(p), "sha256": sha256_file(p)} for p in sources],
        "entorno": {"docker_servidor": pgdocker.docker_server_version(), "imagen": image,
                    "imagen_fijada_por_defecto": image == pgdocker.DEFAULT_IMAGE},
    }
    run: Optional[ScenarioRun] = None
    aborted = None
    with pgdocker.PgContainer(image, name, allow_pull) as pg:
        evidence["entorno"]["imagen_hechos"] = pgdocker.image_facts(pg.image_id())
        evidence["entorno"]["aislamiento"] = pg.inspect_isolation()
        evidence["entorno"]["contenedor"] = pg.name
        run = ScenarioRun(pg, name, manifest, v7_text)
        try:
            run.setup()
            evidence["entorno"]["postgres"] = run.q("SELECT to_json(version())", user="postgres")
            evidence["entorno"]["instalador"] = run.installer_attrs
            run.apply_v7()
            run.characterize_v7()
            before = run.fingerprint()
            run.apply_overlay()
            run.check_invariance(before)
            run.check_partitions()
            run.check_idempotency()
            run.check_reference_timezone()
            run.check_boundary_utc()
            run.check_out_of_range()
            run.check_negative_paths()
            run.check_horizon_30d()
            run.check_lock_timeout()
            run.check_seeds()
            run.check_acl_behaviour()
            run.check_partition_acl_generic()
            run.check_new_object_probe()
            run.check_acl_matrix()
            run.check_acl_grantees()
            run.check_human_parent_untouched()
            run.probe_open_findings()
            evidence["catalogo"] = run.catalog()
        except (Abort, RuntimeError) as exc:
            aborted = str(exc)
    checks = run.checks if run else []
    failed = [c["id"] for c in checks if c["resultado"] != "pasa"]
    evidence["caracterizacion"] = run.characterization if run else {}
    evidence["comprobaciones"] = checks
    evidence["hallazgos_abiertos_observados"] = run.open_findings if run else []
    evidence["resumen"] = {"comprobaciones": len(checks), "pasan": len(checks) - len(failed), "fallan": failed,
                           "interrumpido": aborted,
                           "resultado": "pasa" if checks and not failed and aborted is None else "falla"}
    return evidence


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--escenario", default="todos", choices=["todos"] + list(SCENARIOS))
    parser.add_argument("--imagen", default=pgdocker.DEFAULT_IMAGE,
                        help="Imagen explícita; por defecto la fijada por digest.")
    parser.add_argument("--permitir-descarga", action="store_true",
                        help="Permite descargar la imagen si falta (por defecto --pull never).")
    parser.add_argument("--evidencia-dir", type=Path, default=EVIDENCE_DIR)
    args = parser.parse_args(argv)
    names = list(SCENARIOS) if args.escenario == "todos" else [args.escenario]
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    v7_text = V7_SQL.read_text(encoding="utf-8")
    try:
        pgdocker.docker_server_version()
    except pgdocker.DockerUnavailable as exc:
        print("Docker no disponible: " + str(exc), file=sys.stderr)
        return 2
    args.evidencia_dir.mkdir(parents=True, exist_ok=True)
    status = 0
    for name in names:
        try:
            evidence = run_scenario(name, args.imagen, args.permitir_descarga, manifest, v7_text)
        except pgdocker.DockerUnavailable as exc:
            print(name + ": infraestructura no disponible: " + str(exc), file=sys.stderr)
            return 2
        target = args.evidencia_dir / (name + ".json")
        target.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=False) + "\n", encoding="utf-8")
        summary = evidence["resumen"]
        print("%s: %s (%d comprobaciones, fallan: %s) -> %s" % (
            name, summary["resultado"], summary["comprobaciones"], summary["fallan"] or "ninguna",
            target))
        for finding in evidence["hallazgos_abiertos_observados"]:
            print("  %s: %s" % (finding["id"], finding["estado"]))
        if summary["resultado"] != "pasa":
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main())
