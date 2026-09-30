-- C1 · overlay BORRADOR: ACL base. No es la matriz V8 ni cierra H-06.
-- Denegación por defecto: PUBLIC y los roles de API (anon, authenticated,
-- service_role, si existen) sin acceso. Solo se conceden los privilegios de acl-manifest.json
-- para clases no patrimoniales. Tablas reservadas a humano y pendientes de
-- matriz quedan sin privilegios para los roles de grupo.
-- No modifica funciones ni disparadores de V7; solo su ACL de ejecución.

REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE USAGE ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM PUBLIC;
REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA libox_ops FROM PUBLIC;
REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA libox_ops FROM PUBLIC;

-- Global para el rol que ejecuta: funciones futuras sin EXECUTE a PUBLIC.
ALTER DEFAULT PRIVILEGES REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;

-- Roles de la API de datos (patrón Supabase). Solo actúa si existen y solo
-- sobre concesiones cuyo otorgante es el rol que ejecuta. Los privilegios por
-- defecto definidos por otros roles (p. ej. supabase_admin) no se revocan
-- aquí: validarlos es precondición antes de aplicar en Supabase
-- (cierre-sql-pendientes.md).
DO $acl$
DECLARE
  v_role text;
BEGIN
  FOR v_role IN SELECT rolname FROM pg_roles
                 WHERE rolname IN ('anon', 'authenticated', 'service_role') ORDER BY rolname
  LOOP
    EXECUTE format('REVOKE ALL ON SCHEMA public FROM %I', v_role);
    EXECUTE format('REVOKE ALL ON ALL TABLES IN SCHEMA public FROM %I', v_role);
    EXECUTE format('REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM %I', v_role);
    EXECUTE format('REVOKE ALL ON ALL FUNCTIONS IN SCHEMA public FROM %I', v_role);
    EXECUTE format('ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON TABLES FROM %I', v_role);
    EXECUTE format('ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON SEQUENCES FROM %I', v_role);
    EXECUTE format('ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON FUNCTIONS FROM %I', v_role);
  END LOOP;
END
$acl$;

GRANT USAGE ON SCHEMA public TO libox_app, libox_append, libox_read;

-- catalogo_lectura
GRANT SELECT ON TABLE public.evidence_strength_rules TO libox_app, libox_read;
GRANT SELECT ON TABLE public.holidays_calendar TO libox_app, libox_read;
GRANT SELECT ON TABLE public.market_legal_requirements TO libox_app, libox_read;
GRANT SELECT ON TABLE public.market_prize_categories TO libox_app, libox_read;
GRANT SELECT ON TABLE public.markets TO libox_app, libox_read;
GRANT SELECT ON TABLE public.notification_templates TO libox_app, libox_read;
GRANT SELECT ON TABLE public.operating_windows TO libox_app, libox_read;
GRANT SELECT ON TABLE public.platform_capabilities TO libox_app, libox_read;
GRANT SELECT ON TABLE public.raffle_type_rules TO libox_app, libox_read;
GRANT SELECT ON TABLE public.sla_definitions TO libox_app, libox_read;
GRANT SELECT ON TABLE public.survey_instruments TO libox_app, libox_read;

-- telemetria_insercion
GRANT INSERT ON TABLE public.analytics_events TO libox_app;
GRANT SELECT ON TABLE public.analytics_events TO libox_read;
GRANT INSERT ON TABLE public.notification_attempts TO libox_app;
GRANT SELECT ON TABLE public.notification_attempts TO libox_read;

-- agregacion_no_patrimonial (journal_lines excluida: reservada a humano)
GRANT INSERT ON TABLE public.audit_access_events TO libox_append;
GRANT INSERT ON TABLE public.audit_events TO libox_append;
GRANT INSERT ON TABLE public.room_messages TO libox_append;
GRANT INSERT ON TABLE public.state_transitions TO libox_append;
