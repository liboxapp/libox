-- C1 · overlay BORRADOR sobre libox_schema_L3_V7.sql. No es SQL V8 ni canon.
-- Alcance: almacenamiento no crítico. Particiones mensuales con límites en UTC
-- explícito y partición DEFAULT para conservar la escritura sin partición
-- (L3 V7 §1.3) en 11 de los 12 padres. journal_lines queda inventariada pero
-- sus particiones las aporta su dueño humano (ledger, zona sin generación
-- asistida): el overlay no le crea hijos, DEFAULT ni ACL.
-- No mueve ni borra filas. No crea disparadores. No toca lógica patrimonial,
-- RBAC, sorteo, concurrencia de negocio ni incompatibilidades.
-- retention es metadato documental (B6): nada en el overlay borra ni archiva.
-- El planificador (B3) y el procedimiento para filas en DEFAULT (B4) se
-- especifican en database/planificador-default.md; no se implementan aquí.
-- Ejecutar con el rol dueño de las tablas padre (crear particiones lo exige).

CREATE SCHEMA IF NOT EXISTS libox_ops;
REVOKE ALL ON SCHEMA libox_ops FROM PUBLIC;

-- Inventario esperado de padres particionados. La función falla si el catálogo
-- difiere: una tabla particionada nueva exige decisión y alta explícita.
-- provisioning = overlay: el overlay crea sus particiones.
-- provisioning = humano:  solo se inventaría; el overlay no la toca.
CREATE TABLE IF NOT EXISTS libox_ops.partitioned_parents (
  parent_table  text PRIMARY KEY,
  partition_key text NOT NULL,
  provisioning  text NOT NULL CHECK (provisioning IN ('overlay', 'humano')),
  retention     text NOT NULL
);
REVOKE ALL ON TABLE libox_ops.partitioned_parents FROM PUBLIC;

INSERT INTO libox_ops.partitioned_parents (parent_table, partition_key, provisioning, retention) VALUES
  ('analytics_events',      'server_ts',  'overlay', 'L3 V7 §1.3: 24 meses; agregados indefinidos'),
  ('audit_access_events',   'created_at', 'overlay', 'B6 (Diego, 2026-09-30): indefinida; archivo en frío desde 24 meses'),
  ('audit_events',          'created_at', 'overlay', 'L3 V7 §1.3: indefinida; archivado en frío desde 24 meses'),
  ('event_outbox',          'created_at', 'overlay', 'L3 V7 §1.3: 90 días tras despacho confirmado'),
  ('journal_lines',         'posted_at',  'humano',  'L3 V7 §1.3: indefinida. B5: DEFAULT aprobada; particiones, DEFAULT y ACL las aporta el dueño del ledger'),
  ('notification_attempts', 'server_ts',  'overlay', 'L3 V7 §1.3: 24 meses'),
  ('operation_register',    'created_at', 'overlay', 'B6: plazo del registro de operaciones [LEGAL→ABOGADO]; sin borrado hasta plazo aprobado'),
  ('psp_events',            'created_at', 'overlay', 'B6: la del soporte contable del pago [LEGAL→ABOGADO]; sin borrado hasta plazo aprobado'),
  ('registry_queries',      'created_at', 'overlay', 'L3 V7 §1.3: indefinida'),
  ('risk_events',           'created_at', 'overlay', 'B6 (Diego, 2026-09-30): indefinida; archivo en frío desde 24 meses'),
  ('room_messages',         'created_at', 'overlay', 'L3 V7 §1.3: indefinida'),
  ('state_transitions',     'created_at', 'overlay', 'L3 V7 §1.3: indefinida')
ON CONFLICT (parent_table) DO NOTHING;

CREATE OR REPLACE FUNCTION libox_ops.assert_partition_inventory()
RETURNS void
LANGUAGE plpgsql
SET search_path = pg_catalog, pg_temp
AS $fn$
DECLARE
  v_extra   text;
  v_missing text;
  v_keys    text;
BEGIN
  WITH cat AS (
    SELECT c.relname::text AS parent_table, pt.partstrat, pt.partnatts,
           a.attname::text AS key_column
      FROM pg_partitioned_table pt
      JOIN pg_class c ON c.oid = pt.partrelid
      JOIN pg_namespace n ON n.oid = c.relnamespace
      LEFT JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = pt.partattrs[0]
     WHERE n.nspname = 'public' AND NOT c.relispartition
  )
  SELECT
    (SELECT string_agg(cat.parent_table, ', ' ORDER BY cat.parent_table) FROM cat
      WHERE cat.parent_table NOT IN (SELECT pp.parent_table FROM libox_ops.partitioned_parents pp)),
    (SELECT string_agg(pp.parent_table, ', ' ORDER BY pp.parent_table) FROM libox_ops.partitioned_parents pp
      WHERE pp.parent_table NOT IN (SELECT cat.parent_table FROM cat)),
    (SELECT string_agg(pp.parent_table, ', ' ORDER BY pp.parent_table)
       FROM libox_ops.partitioned_parents pp JOIN cat ON cat.parent_table = pp.parent_table
      WHERE cat.partstrat IS DISTINCT FROM 'r' OR cat.partnatts IS DISTINCT FROM 1
         OR cat.key_column IS DISTINCT FROM pp.partition_key)
  INTO v_extra, v_missing, v_keys;

  IF v_extra IS NOT NULL OR v_missing IS NOT NULL OR v_keys IS NOT NULL THEN
    RAISE EXCEPTION 'LIBOX_PARTITION_INVENTORY_MISMATCH: sin inventario [%]; ausentes del catálogo [%]; clave o estrategia distinta [%]',
      coalesce(v_extra, ''), coalesce(v_missing, ''), coalesce(v_keys, '');
  END IF;
END
$fn$;

-- Deja una partición gestionada sin ningún beneficiario distinto del dueño:
-- PUBLIC y todo rol que la ACL contenga (roles de grupo, anon, authenticated,
-- service_role o cualquier rol con privilegios por defecto). El acceso de la
-- app va por la tabla padre. Si algo no se puede revocar (otro otorgante),
-- falla en vez de dejar la partición expuesta.
CREATE OR REPLACE FUNCTION libox_ops.restrict_partition_acl(p_partition text)
RETURNS void
LANGUAGE plpgsql
SET search_path = pg_catalog, pg_temp
AS $fn$
DECLARE
  v_grantee oid;
  v_left    text;
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
                  WHERE n.nspname = 'public' AND c.relname = p_partition AND c.relispartition) THEN
    RAISE EXCEPTION 'LIBOX_PARTITION_ACL: public.% no es una partición', p_partition;
  END IF;
  EXECUTE format('REVOKE ALL ON TABLE public.%I FROM PUBLIC', p_partition);
  FOR v_grantee IN
    SELECT DISTINCT a.grantee
      FROM pg_class c
      JOIN pg_namespace n ON n.oid = c.relnamespace,
           LATERAL aclexplode(coalesce(c.relacl, acldefault('r', c.relowner))) a
     WHERE n.nspname = 'public' AND c.relname = p_partition
       AND a.grantee <> c.relowner AND a.grantee <> 0
  LOOP
    EXECUTE format('REVOKE ALL ON TABLE public.%I FROM %I', p_partition, pg_get_userbyid(v_grantee));
  END LOOP;
  SELECT string_agg(DISTINCT CASE WHEN a.grantee = 0 THEN 'PUBLIC' ELSE pg_get_userbyid(a.grantee)::text END, ', ')
    INTO v_left
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace,
         LATERAL aclexplode(coalesce(c.relacl, acldefault('r', c.relowner))) a
   WHERE n.nspname = 'public' AND c.relname = p_partition AND a.grantee <> c.relowner;
  IF v_left IS NOT NULL THEN
    RAISE EXCEPTION 'LIBOX_PARTITION_ACL_RESIDUAL: public.% conserva privilegios para [%]; solo su otorgante puede revocarlos',
      p_partition, v_left;
  END IF;
END
$fn$;

-- Idempotente: crea el mes de p_reference (UTC) y los p_months_ahead siguientes,
-- más una DEFAULT si falta, SOLO para padres con provisioning = overlay.
-- Horizonte por defecto 2: mes actual más dos, para que el mes M exista 30 días
-- antes de empezar aunque el mes previo tenga 28 días (L3 V7 §1.3).
-- Falla con mensaje claro, sin efectos parciales (una sola transacción), si:
--   * el inventario no coincide con el catálogo;
--   * existe una relación con el nombre esperado y otros límites;
--   * la DEFAULT tiene filas en el rango del mes a crear (no se mueven datos);
--   * no obtiene un bloqueo en 5 s (lock_timeout): no espera indefinidamente
--     detrás de una transacción larga bloqueando inserciones.
-- Debe correr desde un único planificador; dos ejecuciones concurrentes pueden
-- fallar por nombre duplicado sin efecto sobre datos.
CREATE OR REPLACE FUNCTION libox_ops.ensure_monthly_partitions(
  p_reference    timestamptz DEFAULT now(),
  p_months_ahead integer     DEFAULT 2)
RETURNS TABLE (parent_table text, partition_name text,
               range_from timestamptz, range_to timestamptz, action text)
LANGUAGE plpgsql
SET search_path = pg_catalog, pg_temp
SET "TimeZone" = 'UTC'
SET lock_timeout = '5s'
AS $fn$
#variable_conflict use_column
DECLARE
  r          record;
  v_base     timestamp;
  v_month    timestamp;
  v_from     timestamptz;
  v_to       timestamptz;
  v_name     text;
  v_default  text;
  v_expected text;
  v_actual   text;
  v_parent   text;
  v_rows     bigint;
  v_i        integer;
BEGIN
  IF p_reference IS NULL THEN
    RAISE EXCEPTION 'LIBOX_PARTITION_ARG: p_reference es obligatorio';
  END IF;
  IF p_months_ahead IS NULL OR p_months_ahead < 0 OR p_months_ahead > 12 THEN
    RAISE EXCEPTION 'LIBOX_PARTITION_ARG: p_months_ahead debe estar entre 0 y 12 (recibido %)', p_months_ahead;
  END IF;
  PERFORM libox_ops.assert_partition_inventory();
  v_base := date_trunc('month', p_reference AT TIME ZONE 'UTC');

  FOR r IN SELECT pp.parent_table AS parent, pp.partition_key AS key_column
             FROM libox_ops.partitioned_parents pp
            WHERE pp.provisioning = 'overlay'
            ORDER BY pp.parent_table
  LOOP
    v_default := NULL;
    SELECT c.relname INTO v_default
      FROM pg_inherits i
      JOIN pg_class c ON c.oid = i.inhrelid
      JOIN pg_class p ON p.oid = i.inhparent
      JOIN pg_namespace n ON n.oid = p.relnamespace
     WHERE n.nspname = 'public' AND p.relname = r.parent
       AND pg_get_expr(c.relpartbound, c.oid) = 'DEFAULT';

    FOR v_i IN 0..p_months_ahead LOOP
      v_month    := v_base + make_interval(months => v_i);
      v_from     := v_month AT TIME ZONE 'UTC';
      v_to       := (v_month + interval '1 month') AT TIME ZONE 'UTC';
      v_name     := r.parent || '_p' || to_char(v_month, 'YYYYMM');
      v_expected := format('FOR VALUES FROM (%L) TO (%L)', v_from, v_to);

      v_actual := NULL;
      v_parent := NULL;
      SELECT pg_get_expr(c.relpartbound, c.oid), p.relname
        INTO v_actual, v_parent
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        LEFT JOIN pg_inherits i ON i.inhrelid = c.oid
        LEFT JOIN pg_class p ON p.oid = i.inhparent
       WHERE n.nspname = 'public' AND c.relname = v_name;

      IF FOUND THEN
        IF v_parent IS DISTINCT FROM r.parent OR v_actual IS DISTINCT FROM v_expected THEN
          RAISE EXCEPTION 'LIBOX_PARTITION_BOUNDS_MISMATCH: public.% existe pero no es la partición % de public.% (actual: padre %, %)',
            v_name, v_expected, r.parent, coalesce(v_parent, 'ninguno'), coalesce(v_actual, 'sin límites');
        END IF;
        action := 'exists';
      ELSE
        IF v_default IS NOT NULL THEN
          EXECUTE format('SELECT count(*) FROM public.%I WHERE %I >= $1 AND %I < $2',
                         v_default, r.key_column, r.key_column)
             INTO v_rows USING v_from, v_to;
          IF v_rows > 0 THEN
            RAISE EXCEPTION 'LIBOX_PARTITION_DEFAULT_HAS_ROWS: public.% tiene % filas en [%, %); no se crea public.% ni se mueven o borran datos. Requiere procedimiento operativo aprobado.',
              v_default, v_rows, v_from, v_to, v_name;
          END IF;
        END IF;
        EXECUTE format('CREATE TABLE public.%I PARTITION OF public.%I FOR VALUES FROM (%L) TO (%L)',
                       v_name, r.parent, v_from, v_to);
        action := 'created';
      END IF;
      PERFORM libox_ops.restrict_partition_acl(v_name);
      parent_table := r.parent;
      partition_name := v_name;
      range_from := v_from;
      range_to := v_to;
      RETURN NEXT;
    END LOOP;

    IF v_default IS NULL THEN
      v_default := r.parent || '_pdefault';
      EXECUTE format('CREATE TABLE public.%I PARTITION OF public.%I DEFAULT', v_default, r.parent);
      action := 'created_default';
    ELSE
      action := 'exists_default';
    END IF;
    PERFORM libox_ops.restrict_partition_acl(v_default);
    parent_table := r.parent;
    partition_name := v_default;
    range_from := NULL;
    range_to := NULL;
    RETURN NEXT;
  END LOOP;
END
$fn$;

-- Insumo para la alarma de L3 V7 §1.3, para los 12 padres (incluido
-- journal_lines, marcado humano). covered_until es el final de la cadena
-- contigua de meses desde el mes de p_reference (UTC). coverage_ok exige que
-- p_reference + 30 días quede cubierto. No corrige nada.
CREATE OR REPLACE FUNCTION libox_ops.partition_status(p_reference timestamptz DEFAULT now())
RETURNS TABLE (parent_table text, provisioning text, has_current boolean, has_next boolean,
               covered_until timestamptz, coverage_ok boolean,
               default_partition text, default_rows bigint)
LANGUAGE plpgsql
SET search_path = pg_catalog, pg_temp
SET "TimeZone" = 'UTC'
AS $fn$
#variable_conflict use_column
DECLARE
  r       record;
  v_base  timestamp := date_trunc('month', p_reference AT TIME ZONE 'UTC');
  v_month timestamp;
  v_i     integer;
BEGIN
  FOR r IN SELECT pp.parent_table AS parent, pp.provisioning AS prov
             FROM libox_ops.partitioned_parents pp ORDER BY pp.parent_table
  LOOP
    parent_table := r.parent;
    provisioning := r.prov;
    SELECT
      coalesce(bool_or(c.relname = r.parent || '_p' || to_char(v_base, 'YYYYMM')), false),
      coalesce(bool_or(c.relname = r.parent || '_p' || to_char(v_base + interval '1 month', 'YYYYMM')), false),
      max(c.relname) FILTER (WHERE pg_get_expr(c.relpartbound, c.oid) = 'DEFAULT')
      INTO has_current, has_next, default_partition
      FROM pg_inherits i
      JOIN pg_class c ON c.oid = i.inhrelid
      JOIN pg_class p ON p.oid = i.inhparent
      JOIN pg_namespace n ON n.oid = p.relnamespace
     WHERE n.nspname = 'public' AND p.relname = r.parent;
    covered_until := NULL;
    v_month := v_base;
    FOR v_i IN 0..24 LOOP
      EXIT WHEN NOT EXISTS (
        SELECT 1 FROM pg_inherits i
          JOIN pg_class c ON c.oid = i.inhrelid
          JOIN pg_class p ON p.oid = i.inhparent
          JOIN pg_namespace n ON n.oid = p.relnamespace
         WHERE n.nspname = 'public' AND p.relname = r.parent
           AND c.relname = r.parent || '_p' || to_char(v_month, 'YYYYMM'));
      v_month := v_month + interval '1 month';
      covered_until := v_month AT TIME ZONE 'UTC';
    END LOOP;
    coverage_ok := covered_until IS NOT NULL AND covered_until > p_reference + interval '30 days';
    default_rows := NULL;
    IF default_partition IS NOT NULL THEN
      EXECUTE format('SELECT count(*) FROM public.%I', default_partition) INTO default_rows;
    END IF;
    RETURN NEXT;
  END LOOP;
END
$fn$;

REVOKE ALL ON FUNCTION libox_ops.assert_partition_inventory() FROM PUBLIC;
REVOKE ALL ON FUNCTION libox_ops.restrict_partition_acl(text) FROM PUBLIC;
REVOKE ALL ON FUNCTION libox_ops.ensure_monthly_partitions(timestamptz, integer) FROM PUBLIC;
REVOKE ALL ON FUNCTION libox_ops.partition_status(timestamptz) FROM PUBLIC;
