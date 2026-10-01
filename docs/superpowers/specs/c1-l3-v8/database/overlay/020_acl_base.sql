-- C1 · overlay BORRADOR: ACL base. No es la matriz V8 ni cierra H-06.
-- Denegación por defecto: PUBLIC y los roles de API (anon, authenticated,
-- service_role, si existen) sin acceso. Solo se conceden los privilegios de acl-manifest.json
-- para clases no patrimoniales, incluida la matriz B1 aprobada por Diego el
-- 2026-09-30. Ninguna clase concede DELETE, TRUNCATE, REFERENCES, TRIGGER ni
-- MAINTAIN. Las tablas reservadas a humano (incluidas las seis que B1
-- reclasifica) quedan sin privilegios para los roles de grupo.
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
GRANT SELECT ON TABLE public.aml_thresholds TO libox_app, libox_read;
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

-- operativa (B1): libox_app S, I, U; libox_read S
GRANT SELECT, INSERT, UPDATE ON TABLE public.alarms TO libox_app;
GRANT SELECT ON TABLE public.alarms TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.audit_emergency_queue TO libox_app;
GRANT SELECT ON TABLE public.audit_emergency_queue TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.benefits TO libox_app;
GRANT SELECT ON TABLE public.benefits TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.client_capabilities TO libox_app;
GRANT SELECT ON TABLE public.client_capabilities TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.client_kyb_documents TO libox_app;
GRANT SELECT ON TABLE public.client_kyb_documents TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.client_members TO libox_app;
GRANT SELECT ON TABLE public.client_members TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.client_reputation TO libox_app;
GRANT SELECT ON TABLE public.client_reputation TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.clients TO libox_app;
GRANT SELECT ON TABLE public.clients TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.devices TO libox_app;
GRANT SELECT ON TABLE public.devices TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.disputes TO libox_app;
GRANT SELECT ON TABLE public.disputes TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.featured_placements TO libox_app;
GRANT SELECT ON TABLE public.featured_placements TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.notarial_instruments TO libox_app;
GRANT SELECT ON TABLE public.notarial_instruments TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.notification_preferences TO libox_app;
GRANT SELECT ON TABLE public.notification_preferences TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.partners TO libox_app;
GRANT SELECT ON TABLE public.partners TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.pc_stage_documents TO libox_app;
GRANT SELECT ON TABLE public.pc_stage_documents TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.pc_workflow_stages TO libox_app;
GRANT SELECT ON TABLE public.pc_workflow_stages TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.prize_valuation_documents TO libox_app;
GRANT SELECT ON TABLE public.prize_valuation_documents TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.raffle_media TO libox_app;
GRANT SELECT ON TABLE public.raffle_media TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.raffle_recurrences TO libox_app;
GRANT SELECT ON TABLE public.raffle_recurrences TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.registrable_assets TO libox_app;
GRANT SELECT ON TABLE public.registrable_assets TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.registry_blocks TO libox_app;
GRANT SELECT ON TABLE public.registry_blocks TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.resolution_rooms TO libox_app;
GRANT SELECT ON TABLE public.resolution_rooms TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.risk_rules TO libox_app;
GRANT SELECT ON TABLE public.risk_rules TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.room_assignments TO libox_app;
GRANT SELECT ON TABLE public.room_assignments TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.room_participants TO libox_app;
GRANT SELECT ON TABLE public.room_participants TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.sla_extensions TO libox_app;
GRANT SELECT ON TABLE public.sla_extensions TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.transfer_acts TO libox_app;
GRANT SELECT ON TABLE public.transfer_acts TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.user_devices TO libox_app;
GRANT SELECT ON TABLE public.user_devices TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.user_reputation TO libox_app;
GRANT SELECT ON TABLE public.user_reputation TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.waitlists TO libox_app;
GRANT SELECT ON TABLE public.waitlists TO libox_read;
GRANT SELECT, INSERT, UPDATE ON TABLE public.winner_legal_readiness TO libox_app;
GRANT SELECT ON TABLE public.winner_legal_readiness TO libox_read;

-- registro_inmutable (B1): libox_app S, I; libox_read S
GRANT SELECT, INSERT ON TABLE public.alarm_resolutions TO libox_app;
GRANT SELECT ON TABLE public.alarm_resolutions TO libox_read;
GRANT SELECT, INSERT ON TABLE public.attribution_touches TO libox_app;
GRANT SELECT ON TABLE public.attribution_touches TO libox_read;
GRANT SELECT, INSERT ON TABLE public.benefit_redemptions TO libox_app;
GRANT SELECT ON TABLE public.benefit_redemptions TO libox_read;
GRANT SELECT, INSERT ON TABLE public.client_reputation_history TO libox_app;
GRANT SELECT ON TABLE public.client_reputation_history TO libox_read;
GRANT SELECT, INSERT ON TABLE public.client_transfer_acceptances TO libox_app;
GRANT SELECT ON TABLE public.client_transfer_acceptances TO libox_read;
GRANT SELECT, INSERT ON TABLE public.daily_codes TO libox_app;
GRANT SELECT ON TABLE public.daily_codes TO libox_read;
GRANT SELECT, INSERT ON TABLE public.dispute_evidence TO libox_app;
GRANT SELECT ON TABLE public.dispute_evidence TO libox_read;
GRANT SELECT, INSERT ON TABLE public.feature_toggle_log TO libox_app;
GRANT SELECT ON TABLE public.feature_toggle_log TO libox_read;
GRANT SELECT, INSERT ON TABLE public.kpi_snapshots TO libox_app;
GRANT SELECT ON TABLE public.kpi_snapshots TO libox_read;
GRANT SELECT, INSERT ON TABLE public.organizer_referral_codes TO libox_app;
GRANT SELECT ON TABLE public.organizer_referral_codes TO libox_read;
GRANT SELECT, INSERT ON TABLE public.prize_market_references TO libox_app;
GRANT SELECT ON TABLE public.prize_market_references TO libox_read;
GRANT SELECT, INSERT ON TABLE public.raffle_terms TO libox_app;
GRANT SELECT ON TABLE public.raffle_terms TO libox_read;
GRANT SELECT, INSERT ON TABLE public.registry_queries TO libox_app;
GRANT SELECT ON TABLE public.registry_queries TO libox_read;
GRANT SELECT, INSERT ON TABLE public.responsible_play_events TO libox_app;
GRANT SELECT ON TABLE public.responsible_play_events TO libox_read;
GRANT SELECT, INSERT ON TABLE public.risk_events TO libox_app;
GRANT SELECT ON TABLE public.risk_events TO libox_read;
GRANT SELECT, INSERT ON TABLE public.room_evidence TO libox_app;
GRANT SELECT ON TABLE public.room_evidence TO libox_read;
GRANT SELECT, INSERT ON TABLE public.survey_responses TO libox_app;
GRANT SELECT ON TABLE public.survey_responses TO libox_read;
GRANT SELECT, INSERT ON TABLE public.user_attributions TO libox_app;
GRANT SELECT ON TABLE public.user_attributions TO libox_read;

-- sensible (B1): solo libox_app S, I, U; sin libox_read (vistas seudonimizadas pendientes)
GRANT SELECT, INSERT, UPDATE ON TABLE public.aml_cases TO libox_app;
GRANT SELECT, INSERT, UPDATE ON TABLE public.blocked_documents TO libox_app;
GRANT SELECT, INSERT, UPDATE ON TABLE public.client_kyb TO libox_app;
GRANT SELECT, INSERT, UPDATE ON TABLE public.credentials TO libox_app;
GRANT SELECT, INSERT, UPDATE ON TABLE public.identity_documents TO libox_app;
GRANT SELECT, INSERT, UPDATE ON TABLE public.leads TO libox_app;
GRANT SELECT, INSERT, UPDATE ON TABLE public.refresh_tokens TO libox_app;
GRANT SELECT, INSERT, UPDATE ON TABLE public.users TO libox_app;

-- sensible_inmutable (B1): solo libox_app S, I
GRANT SELECT, INSERT ON TABLE public.age_verifications TO libox_app;
GRANT SELECT, INSERT ON TABLE public.aml_case_documents TO libox_app;
GRANT SELECT, INSERT ON TABLE public.identity_verifications TO libox_app;
