-- Se declaran como DOMAIN para uniformidad y validación centralizada.
CREATE DOMAIN money_amount AS BIGINT CHECK (VALUE >= 0);
CREATE DOMAIN money_signed AS BIGINT;                    -- admite negativo: asientos
CREATE DOMAIN currency_code AS CHAR(3) CHECK (VALUE ~ '^[A-Z]{3}$');
CREATE DOMAIN market_code  AS CHAR(2) CHECK (VALUE ~ '^[A-Z]{2}$');
CREATE DOMAIN sha256_hex   AS CHAR(64) CHECK (VALUE ~ '^[0-9a-f]{64}$');
CREATE DOMAIN email_addr   AS VARCHAR(254);
CREATE DOMAIN phone_e164   AS VARCHAR(16) CHECK (VALUE ~ '^\+[1-9][0-9]{7,14}$');
CREATE DOMAIN pct_basis    AS INTEGER CHECK (VALUE BETWEEN 0 AND 10000); -- puntos básicos


-- Los roles se crean en la migracion 001, antes que cualquier objeto: las
-- sentencias REVOKE de §3 fallan si el rol no existe.
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'libox_app') THEN
    CREATE ROLE libox_app     NOLOGIN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'libox_append') THEN
    CREATE ROLE libox_append  NOLOGIN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'libox_read') THEN
    CREATE ROLE libox_read    NOLOGIN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'libox_migrate') THEN
    CREATE ROLE libox_migrate NOLOGIN;
  END IF;
END $$;


CREATE TABLE markets (
  code            market_code PRIMARY KEY,           -- 'PE'
  name            VARCHAR(80)  NOT NULL,
  currency        currency_code NOT NULL,
  timezone        VARCHAR(64)  NOT NULL,             -- 'America/Lima'
  locale          VARCHAR(10)  NOT NULL,             -- 'es-PE'
  status          VARCHAR(40)  NOT NULL DEFAULT 'ACTIVE'
                  CHECK (status IN ('ACTIVE','SUSPENDED_L1','SUSPENDED_L2',
                                    'SUSPENDED_L3','SUSPENDED_L4')),
  suspended_at    TIMESTAMPTZ,
  suspended_by    UUID,
  suspension_reason TEXT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- INV-15: un sorteo se rige por la version vigente el dia de su publicacion.
CREATE TABLE market_config_versions (
  id              UUID PRIMARY KEY,
  market_code     market_code NOT NULL REFERENCES markets(code),
  version         INTEGER     NOT NULL,
  effective_from  TIMESTAMPTZ NOT NULL,
  effective_to    TIMESTAMPTZ,                        -- NULL = vigente
  config          JSONB       NOT NULL,               -- estructura en §10
  config_hash     sha256_hex  NOT NULL,
  approved_by     UUID        NOT NULL,
  approval_reason TEXT        NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ux_mcv_market_version UNIQUE (market_code, version),
  CONSTRAINT ck_mcv_range CHECK (effective_to IS NULL OR effective_to > effective_from)
);
CREATE INDEX ix_mcv_lookup ON market_config_versions (market_code, effective_from DESC);

-- Solo una version vigente por mercado.
CREATE UNIQUE INDEX ux_mcv_current
  ON market_config_versions (market_code) WHERE effective_to IS NULL;

CREATE TABLE market_legal_requirements (
  id              UUID PRIMARY KEY,
  market_code     market_code NOT NULL REFERENCES markets(code),
  requirement_key VARCHAR(60) NOT NULL,
  gate_scope      VARCHAR(20) NOT NULL
                  CHECK (gate_scope IN ('per_raffle','per_operator','none')),
  document_type   VARCHAR(60),
  authority       VARCHAR(120),
  blocks          VARCHAR(40) NOT NULL
                  CHECK (blocks IN ('PUBLICATION','ONBOARDING','MARKET_LAUNCH')),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ux_mlr UNIQUE (market_code, requirement_key)
);

-- INV-45: control en tres capas. La MAS RESTRICTIVA gana.
-- plataforma -> mercado -> cliente. Apagar arriba no se revierte abajo.
CREATE TABLE platform_capabilities (
  capability      VARCHAR(40) PRIMARY KEY,   -- 'T1'..'T8','P_A'..'P_F','FREE_ENTRY',
                                             -- 'PROMOTIONAL','LIBOX_CLUB','REFERRALS'
  enabled         BOOLEAN     NOT NULL DEFAULT true,
  disabled_by     UUID,
  second_signer_id UUID,                     -- obligatorio al apagar globalmente
  disable_reason  TEXT,
  disable_scope   VARCHAR(20) CHECK (disable_scope IN ('COMMERCIAL','REGULATORY','RISK','DEFECT')),
  disabled_at     TIMESTAMPTZ,
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ck_pc_disable CHECK (
    enabled OR (disabled_by IS NOT NULL AND second_signer_id IS NOT NULL
                AND disable_reason IS NOT NULL AND disable_scope IS NOT NULL)),
  CONSTRAINT ck_pc_signer CHECK (second_signer_id IS NULL OR second_signer_id <> disabled_by)
);

-- RN-06-nonies: ventanas operativas por funcion y mercado. La ventana DIFIERE, no cancela.
CREATE TABLE operating_windows (
  market_code     market_code NOT NULL REFERENCES markets(code),
  function_code   VARCHAR(40) NOT NULL
                  CHECK (function_code IN ('DRAW_EXECUTION','PUBLICATION','SETTLEMENT',
                                           'VALUATION','SUPPORT')),
  enabled         BOOLEAN NOT NULL DEFAULT false,   -- sin ventana = 24 h
  window_from     TIME,
  window_to       TIME,
  days_of_week    SMALLINT[],
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (market_code, function_code),
  CONSTRAINT ck_ow_range CHECK (NOT enabled OR (window_from IS NOT NULL AND window_to IS NOT NULL))
);

-- RN-06-sexies: toda conmutacion deja rastro consultable.
CREATE TABLE feature_toggle_log (
  id              UUID PRIMARY KEY,
  scope           VARCHAR(20) NOT NULL CHECK (scope IN ('PLATFORM','MARKET','CLIENT')),
  scope_id        VARCHAR(60),
  capability      VARCHAR(40) NOT NULL,
  enabled         BOOLEAN NOT NULL,
  reason          TEXT NOT NULL CHECK (length(reason) >= 20),
  disable_scope   VARCHAR(20),
  actor_id        UUID NOT NULL,
  second_signer_id UUID,
  affected_count  INTEGER,                    -- clientes u oportunidades notificadas
  notified_at     TIMESTAMPTZ,
  trace_id        UUID NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ix_ftl_capability ON feature_toggle_log (capability, created_at DESC);

CREATE TABLE market_prize_categories (
  market_code     market_code NOT NULL REFERENCES markets(code),
  category        VARCHAR(6)  NOT NULL
                  CHECK (category IN ('P_A','P_B','P_C1','P_C2','P_D','P_E','P_F')),
  enabled         BOOLEAN     NOT NULL DEFAULT false,
  delivery_sla_days INTEGER   NOT NULL,
  business_days   BOOLEAN     NOT NULL DEFAULT false,
  PRIMARY KEY (market_code, category)
);

CREATE TABLE holidays_calendar (
  market_code     market_code NOT NULL REFERENCES markets(code),
  holiday_date    DATE        NOT NULL,
  name            VARCHAR(120) NOT NULL,
  PRIMARY KEY (market_code, holiday_date)
);


CREATE TABLE users (
  id                 UUID PRIMARY KEY,
  market_code        market_code NOT NULL REFERENCES markets(code),
  email              email_addr  NOT NULL,
  email_verified_at  TIMESTAMPTZ,
  phone              phone_e164  NOT NULL,
  phone_verified_at  TIMESTAMPTZ,
  birth_date         DATE        NOT NULL,
  document_type      VARCHAR(20),
  document_number_hash sha256_hex,          -- INV-08: unicidad sin almacenar en claro
  document_number_enc BYTEA,                -- cifrado con clave gestionada
  full_name_enc      BYTEA,
  display_name       VARCHAR(60),           -- 'Karla F.' — minimizado, R-10
  verification_level VARCHAR(4) NOT NULL DEFAULT 'L0'
                     CHECK (verification_level IN ('L0','L1','L2')),
  status             VARCHAR(40) NOT NULL DEFAULT 'ACTIVE'
                     CHECK (status IN ('ACTIVE','RESTRICTED','FROZEN','BLOCKED_MINOR','CLOSED')),
  status_reason      TEXT,
  risk_score         INTEGER    NOT NULL DEFAULT 0 CHECK (risk_score BETWEEN 0 AND 100),
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id           UUID
);

-- INV-08 — unicidad de documento, correo y telefono sobre usuarios no cerrados.
CREATE UNIQUE INDEX ux_users_email ON users (lower(email)) WHERE status <> 'CLOSED';
CREATE UNIQUE INDEX ux_users_phone ON users (phone)        WHERE status <> 'CLOSED';
CREATE UNIQUE INDEX ux_users_document ON users (document_number_hash)
  WHERE document_number_hash IS NOT NULL;

-- RN-119: el documento de un menor detectado queda bloqueado de forma permanente.
CREATE TABLE blocked_documents (
  document_number_hash sha256_hex PRIMARY KEY,
  reason               VARCHAR(40) NOT NULL
                       CHECK (reason IN ('MINOR','FRAUD','REGULATORY','SELF_EXCLUSION_PERM')),
  blocked_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
  blocked_by           UUID,
  notes                TEXT
);

CREATE TABLE credentials (
  id              UUID PRIMARY KEY,
  user_id         UUID NOT NULL REFERENCES users(id),
  password_hash   VARCHAR(255) NOT NULL,
  algorithm       VARCHAR(20)  NOT NULL DEFAULT 'argon2id',
  mfa_enabled     BOOLEAN      NOT NULL DEFAULT false,
  mfa_secret_enc  BYTEA,
  last_rotated_at TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ux_credentials_user UNIQUE (user_id)
);

CREATE TABLE refresh_tokens (
  id              UUID PRIMARY KEY,
  user_id         UUID NOT NULL REFERENCES users(id),
  token_hash      sha256_hex NOT NULL,
  device_id       UUID,
  issued_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  expires_at      TIMESTAMPTZ NOT NULL,
  revoked_at      TIMESTAMPTZ,
  revoked_reason  VARCHAR(60),
  CONSTRAINT ux_refresh_hash UNIQUE (token_hash)
);
CREATE INDEX ix_refresh_user_active ON refresh_tokens (user_id) WHERE revoked_at IS NULL;

CREATE TABLE devices (
  id              UUID PRIMARY KEY,
  fingerprint     sha256_hex NOT NULL,
  first_seen_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  last_seen_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  user_agent      TEXT,
  platform        VARCHAR(40),
  CONSTRAINT ux_devices_fingerprint UNIQUE (fingerprint)
);

CREATE TABLE user_devices (
  user_id         UUID NOT NULL REFERENCES users(id),
  device_id       UUID NOT NULL REFERENCES devices(id),
  first_seen_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  last_seen_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, device_id)
);
-- Correlacion de fraude: cuantos usuarios distintos comparten un dispositivo.
CREATE INDEX ix_user_devices_device ON user_devices (device_id);


CREATE TABLE identity_verifications (
  id                 UUID PRIMARY KEY,
  user_id            UUID NOT NULL REFERENCES users(id),
  provider           VARCHAR(40) NOT NULL,        -- adaptador por mercado
  method             VARCHAR(40) NOT NULL
                     CHECK (method IN ('DOCUMENT','LIVENESS','DOCUMENT_LIVENESS')),
  result             VARCHAR(20) NOT NULL
                     CHECK (result IN ('PASS','FAIL','MANUAL_REVIEW','EXPIRED')),
  provider_reference VARCHAR(120),
  score              NUMERIC(5,2),
  document_expiry    DATE,                        -- RN-124: monitoreo de vigencia
  raw_response_hash  sha256_hex,
  reviewed_by        UUID,
  review_reason      TEXT,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id           UUID NOT NULL
);
CREATE INDEX ix_idv_user ON identity_verifications (user_id, created_at DESC);
CREATE INDEX ix_idv_expiry ON identity_verifications (document_expiry)
  WHERE result = 'PASS' AND document_expiry IS NOT NULL;

CREATE TABLE age_verifications (
  id              UUID PRIMARY KEY,
  user_id         UUID NOT NULL REFERENCES users(id),
  gate            VARCHAR(4) NOT NULL CHECK (gate IN ('G_A','G_B')),
  declared_birth_date DATE,
  verified_birth_date DATE,
  is_adult        BOOLEAN NOT NULL,
  source          VARCHAR(40) NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id        UUID NOT NULL
);

-- Almacenamiento de documentos con politica de retencion (RN-124, Ley 29733).
CREATE TABLE identity_documents (
  id              UUID PRIMARY KEY,
  user_id         UUID NOT NULL REFERENCES users(id),
  document_kind   VARCHAR(40) NOT NULL,
  object_key      VARCHAR(255) NOT NULL,          -- almacenamiento cifrado
  content_hash    sha256_hex NOT NULL,
  mime_type       VARCHAR(80) NOT NULL,
  size_bytes      INTEGER NOT NULL,
  av_scan_status  VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                  CHECK (av_scan_status IN ('PENDING','CLEAN','INFECTED','ERROR')),
  expires_at      DATE,
  retention_until DATE NOT NULL,
  purged_at       TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ix_iddocs_retention ON identity_documents (retention_until)
  WHERE purged_at IS NULL;


CREATE TABLE clients (
  id                 UUID PRIMARY KEY,
  market_code        market_code NOT NULL REFERENCES markets(code),
  legal_name         VARCHAR(200) NOT NULL,
  trade_name         VARCHAR(120),
  -- RN-03-bis: el identificador tributario es exigible SOLO a persona juridica.
  -- En V4 era NOT NULL y bloqueaba el alta del organizador persona natural.
  tax_id             VARCHAR(20),
  economic_activity  VARCHAR(120),                 -- concordancia de giro, §19.3
  entity_type        VARCHAR(20) NOT NULL
                     CHECK (entity_type IN ('NATURAL','LEGAL')),
  -- Persona natural: se identifica por documento verificado con prueba de vida.
  owner_user_id      UUID REFERENCES users(id),
  owner_document_hash sha256_hex,
  status             VARCHAR(40) NOT NULL DEFAULT 'PENDING_KYB'
                     CHECK (status IN ('PENDING_KYB','ACTIVE','SUSPENDED','FROZEN','CLOSED')),
  -- INV-39: parte relacionada opera COMO CLIENTE, con trato identico.
  -- La marca existe para auditoria y contabilidad, nunca para privilegios.
  related_party      BOOLEAN NOT NULL DEFAULT false,
  reputation_level   VARCHAR(2) NOT NULL DEFAULT 'N0'
                     CHECK (reputation_level IN ('N0','N1','N2','N3')),
  reputation_score   NUMERIC(5,2) NOT NULL DEFAULT 0,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id           UUID,
  -- Persona juridica: identificador tributario y giro obligatorios.
  CONSTRAINT ck_clients_legal CHECK (
    entity_type <> 'LEGAL'
    OR (tax_id IS NOT NULL AND economic_activity IS NOT NULL)),
  -- Persona natural: titular identificado, sin identificador tributario exigible.
  CONSTRAINT ck_clients_natural CHECK (
    entity_type <> 'NATURAL'
    OR (owner_user_id IS NOT NULL AND owner_document_hash IS NOT NULL))
);
-- Unicidad de identificador tributario solo cuando existe.
CREATE UNIQUE INDEX ux_clients_tax ON clients (market_code, tax_id)
  WHERE tax_id IS NOT NULL;
-- RN-03-quater: un mismo documento no sostiene dos organizadores.
CREATE UNIQUE INDEX ux_clients_owner_doc ON clients (owner_document_hash)
  WHERE owner_document_hash IS NOT NULL AND status <> 'CLOSED';

CREATE TABLE client_members (
  id              UUID PRIMARY KEY,
  client_id       UUID NOT NULL REFERENCES clients(id),
  user_id         UUID NOT NULL REFERENCES users(id),
  subrole         VARCHAR(30) NOT NULL
                  CHECK (subrole IN ('CLIENT_OWNER','CLIENT_MANAGER',
                                     'CLIENT_OPERATOR','CLIENT_VIEWER')),
  status          VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
                  CHECK (status IN ('ACTIVE','SUSPENDED','REMOVED')),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ux_client_member UNIQUE (client_id, user_id)
);
-- Todo organizador tiene exactamente un titular activo.
CREATE UNIQUE INDEX ux_client_single_owner ON client_members (client_id)
  WHERE subrole = 'CLIENT_OWNER' AND status = 'ACTIVE';

-- RN-03-ter: el organizador persona natural es titular unico y no delega.
-- Se impone por disparador porque depende de una columna de otra tabla.
CREATE OR REPLACE FUNCTION assert_natural_single_member() RETURNS TRIGGER AS $$
DECLARE et VARCHAR(20); n INTEGER;
BEGIN
  SELECT entity_type INTO et FROM clients WHERE id = NEW.client_id;
  IF et = 'NATURAL' THEN
    IF NEW.subrole <> 'CLIENT_OWNER' THEN
      RAISE EXCEPTION 'ERR_CLIENT_NATURAL_NO_DELEGATION: el organizador persona natural no admite subusuarios';
    END IF;
    SELECT count(*) INTO n FROM client_members
      WHERE client_id = NEW.client_id AND status = 'ACTIVE' AND user_id <> NEW.user_id;
    IF n > 0 THEN
      RAISE EXCEPTION 'ERR_CLIENT_NATURAL_NO_DELEGATION: titular unico';
    END IF;
  END IF;
  RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_natural_single_member
  BEFORE INSERT OR UPDATE ON client_members
  FOR EACH ROW EXECUTE FUNCTION assert_natural_single_member();

CREATE TABLE client_kyb (
  id                    UUID PRIMARY KEY,
  client_id             UUID NOT NULL REFERENCES clients(id),
  legal_rep_user_id     UUID REFERENCES users(id),
  beneficial_owner_enc  BYTEA,                     -- beneficiario final, §19.3
  status                VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                        CHECK (status IN ('PENDING','APPROVED','REJECTED','EXPIRED')),
  approved_by           UUID,
  approved_at           TIMESTAMPTZ,
  expires_at            DATE,
  rejection_reason      TEXT,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id              UUID NOT NULL
);

CREATE TABLE client_kyb_documents (
  id              UUID PRIMARY KEY,
  client_kyb_id   UUID NOT NULL REFERENCES client_kyb(id),
  document_kind   VARCHAR(60) NOT NULL,
  object_key      VARCHAR(255) NOT NULL,
  content_hash    sha256_hex NOT NULL,
  verified        BOOLEAN NOT NULL DEFAULT false,
  verified_by     UUID,
  verified_at     TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- RN-49: titularidad de la cuenta debe coincidir con el titular del KYB.
CREATE TABLE payout_instructions (
  id                 UUID PRIMARY KEY,
  client_id          UUID NOT NULL REFERENCES clients(id),
  account_holder_enc BYTEA NOT NULL,
  account_number_enc BYTEA NOT NULL,
  account_last4      CHAR(4) NOT NULL,
  bank_code          VARCHAR(20) NOT NULL,
  currency           currency_code NOT NULL,
  holder_matches_kyb BOOLEAN NOT NULL DEFAULT false,
  status             VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                     CHECK (status IN ('PENDING','VERIFIED','REJECTED','REPLACED')),
  verified_at        TIMESTAMPTZ,
  -- RN-04: congelamiento de 48 h tras cambio de datos bancarios.
  freeze_until       TIMESTAMPTZ,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id           UUID NOT NULL
);
CREATE UNIQUE INDEX ux_payout_active ON payout_instructions (client_id)
  WHERE status = 'VERIFIED';

CREATE TABLE client_capabilities (
  client_id       UUID NOT NULL REFERENCES clients(id),
  capability      VARCHAR(30) NOT NULL,            -- 'T1'..'T8', 'P_C1', 'P_C2', 'LIVE'
  enabled         BOOLEAN NOT NULL DEFAULT false,
  enabled_by      UUID,
  enabled_at      TIMESTAMPTZ,
  reason          TEXT,
  PRIMARY KEY (client_id, capability)
);


-- Escala de progresion de comision (PRD MVP V8 §1.3.1).
-- Los umbrales son datos por mercado, nunca constantes de codigo.
CREATE TABLE fee_schedules (
  market_code     market_code NOT NULL REFERENCES markets(code),
  level           VARCHAR(2)  NOT NULL CHECK (level IN ('E0','E1','E2','E3','E4')),
  fee_bp          pct_basis   NOT NULL,
  threshold_from  money_amount NOT NULL,        -- volumen liquidado acumulado 12m
  currency        currency_code NOT NULL,
  active          BOOLEAN     NOT NULL DEFAULT false,
  PRIMARY KEY (market_code, level),
  -- E0 es la tasa base y techo: ningun nivel puede superarla.
  CONSTRAINT ck_fee_ceiling CHECK (fee_bp <= 2000)
);

CREATE TABLE client_fee_levels (
  id                    UUID PRIMARY KEY,
  client_id             UUID NOT NULL REFERENCES clients(id),
  level                 VARCHAR(2) NOT NULL CHECK (level IN ('E0','E1','E2','E3','E4')),
  fee_bp                pct_basis NOT NULL,
  settled_volume_12m    money_amount NOT NULL,
  currency              currency_code NOT NULL,
  change_reason         VARCHAR(40) NOT NULL
                        CHECK (change_reason IN ('VOLUME_UPGRADE','SERIOUS_BREACH',
                                                 'MANUAL_ADJUSTMENT','INITIAL')),
  -- RN-01-quinquies: el descenso exige motivo y actor.
  reason_text           TEXT,
  changed_by            UUID,
  effective_from        TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id              UUID NOT NULL,
  CONSTRAINT ck_cfl_downgrade CHECK (
    change_reason NOT IN ('SERIOUS_BREACH','MANUAL_ADJUSTMENT')
    OR (reason_text IS NOT NULL AND changed_by IS NOT NULL))
);
CREATE INDEX ix_cfl_client ON client_fee_levels (client_id, effective_from DESC);

-- Excepciones TIPIFICADAS de tasa (PRD MVP V8 §1.3.1, RN-01-nonies).
-- No existe tarifa negociada: toda excepcion pertenece a una categoria con
-- criterio objetivo publicado, vigencia limitada y segunda firma.
CREATE TABLE fee_exceptions (
  id                  UUID PRIMARY KEY,
  client_id           UUID NOT NULL REFERENCES clients(id),
  market_code         market_code NOT NULL REFERENCES markets(code),
  category            VARCHAR(30) NOT NULL
                      CHECK (category IN ('ANCHOR_LAUNCH','VERIFIED_NONPROFIT',
                                          'INSTITUTIONAL_ALLIANCE')),
  fee_bp              pct_basis NOT NULL,
  criteria_evidence   TEXT NOT NULL,               -- criterio objetivo acreditado
  approved_by         UUID NOT NULL,
  second_signer_id    UUID NOT NULL,
  approval_reason     TEXT NOT NULL,
  valid_from          TIMESTAMPTZ NOT NULL DEFAULT now(),
  valid_to            TIMESTAMPTZ NOT NULL,        -- vigencia SIEMPRE limitada
  max_raffles         INTEGER,
  raffles_used        INTEGER NOT NULL DEFAULT 0,
  revoked_at          TIMESTAMPTZ,
  revoke_reason       TEXT,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id            UUID NOT NULL,
  -- INV-37: ninguna excepcion supera el techo del mercado.
  CONSTRAINT ck_fee_exception_ceiling CHECK (fee_bp <= 2000),
  -- INC-09: la segunda firma corresponde a otra persona natural.
  CONSTRAINT ck_fee_exception_signer CHECK (second_signer_id <> approved_by),
  CONSTRAINT ck_fee_exception_window CHECK (valid_to > valid_from),
  CONSTRAINT ck_fee_exception_reason CHECK (length(approval_reason) >= 100)
);
CREATE INDEX ix_fee_exc_active ON fee_exceptions (client_id, valid_to)
  WHERE revoked_at IS NULL;

CREATE TABLE client_reputation (
  client_id             UUID PRIMARY KEY REFERENCES clients(id),
  raffles_completed     INTEGER NOT NULL DEFAULT 0,
  raffles_failed        INTEGER NOT NULL DEFAULT 0,
  disputes_lost         INTEGER NOT NULL DEFAULT 0,
  disputes_total        INTEGER NOT NULL DEFAULT 0,
  on_time_deliveries    INTEGER NOT NULL DEFAULT 0,
  evidence_first_pass   INTEGER NOT NULL DEFAULT 0,
  winner_satisfaction   NUMERIC(4,2),
  penalties             NUMERIC(6,2) NOT NULL DEFAULT 0,
  score                 NUMERIC(5,2) NOT NULL DEFAULT 0,
  level                 VARCHAR(2) NOT NULL DEFAULT 'N0'
                        CHECK (level IN ('N0','N1','N2','N3')),
  first_raffle_at       TIMESTAMPTZ,
  computed_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE client_reputation_history (
  id              UUID PRIMARY KEY,
  client_id       UUID NOT NULL REFERENCES clients(id),
  score           NUMERIC(5,2) NOT NULL,
  level           VARCHAR(2) NOT NULL,
  delta_reason    VARCHAR(60) NOT NULL,
  related_entity  UUID,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- RN-157: reputacion del usuario por reclamos de mala fe.
CREATE TABLE user_reputation (
  user_id             UUID PRIMARY KEY REFERENCES users(id),
  claims_total        INTEGER NOT NULL DEFAULT 0,
  claims_bad_faith    INTEGER NOT NULL DEFAULT 0,
  deliveries_confirmed INTEGER NOT NULL DEFAULT 0,
  score               NUMERIC(5,2) NOT NULL DEFAULT 100,
  computed_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);


CREATE TABLE raffle_type_rules (
  raffle_type       VARCHAR(2) PRIMARY KEY
                    CHECK (raffle_type IN ('T1','T2','T3','T4','T5','T6','T7','T8')),
  name              VARCHAR(60) NOT NULL,
  trigger_kind      VARCHAR(30) NOT NULL
                    CHECK (trigger_kind IN ('SOLD_OUT','THRESHOLD','TIME',
                                            'MILESTONE','FLASH','RECURRING')),
  requires_end_at   BOOLEAN NOT NULL,
  requires_threshold BOOLEAN NOT NULL,
  multi_winner      BOOLEAN NOT NULL DEFAULT false,
  presentation_mode BOOLEAN NOT NULL DEFAULT false,   -- T8: modo, no motor (INV-17)
  capabilities      JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE raffles (
  id                    UUID PRIMARY KEY,
  raffle_code           VARCHAR(20) NOT NULL,         -- LBX-YYYYMM-XXXXX
  market_code           market_code NOT NULL REFERENCES markets(code),
  client_id             UUID NOT NULL REFERENCES clients(id),
  raffle_type           VARCHAR(2) NOT NULL REFERENCES raffle_type_rules(raffle_type),
  base_type             VARCHAR(2),                   -- tipo base cuando T8
  title                 VARCHAR(140) NOT NULL,
  slug                  VARCHAR(160) NOT NULL,

  -- Pricing (§1.3 PRD). Importes en unidad minima.
  currency              currency_code NOT NULL,
  target_net_amount     money_amount NOT NULL,
  gross_required        money_amount NOT NULL,
  libox_fee_bp          pct_basis    NOT NULL DEFAULT 2000,
  libox_fee_amount      money_amount NOT NULL,
  client_net_amount     money_amount NOT NULL,
  ticket_price          money_amount NOT NULL,
  total_tickets         INTEGER      NOT NULL CHECK (total_tickets > 0),
  min_threshold         INTEGER      CHECK (min_threshold IS NULL OR min_threshold > 0),

  -- Contadores. tickets_reserved incluye emitidos (RN-54).
  tickets_reserved      INTEGER NOT NULL DEFAULT 0,
  tickets_issued        INTEGER NOT NULL DEFAULT 0,
  tickets_voided        INTEGER NOT NULL DEFAULT 0,
  next_ticket_number    INTEGER NOT NULL DEFAULT 1,   -- INV-11: nunca decrece

  -- Ciclo
  status                VARCHAR(40) NOT NULL DEFAULT 'DRAFT',
  starts_at             TIMESTAMPTZ,
  end_at                TIMESTAMPTZ,
  published_at          TIMESTAMPTZ,

  -- INV-15: configuracion congelada al publicar.
  config_version_id     UUID REFERENCES market_config_versions(id),

  -- Regimen economico de la oportunidad.
  economic_regime       VARCHAR(20) NOT NULL DEFAULT 'PAID'
                        CHECK (economic_regime IN ('PAID','FREE_ENTRY','PROMOTIONAL')),
  prize_origin          VARCHAR(20)
                        CHECK (prize_origin IN ('ORGANIZER','LIBOX_RELATED','JOINT_CAMPAIGN')),
  -- INV-40/41: multiplo sobre el valor APROBADO, no el declarado.
  collection_multiple_bp INTEGER,
  multiple_override_by  UUID,
  multiple_override_signer UUID,
  multiple_override_reason TEXT,
  -- INV-06-b: sin recaudacion, la garantia sustituye al escrow.
  substitute_guarantee_id UUID,

  -- T7: vinculo a la serie. Cada edicion es independiente en pool y prueba.
  recurrence_id         UUID,
  edition_number        INTEGER CHECK (edition_number IS NULL OR edition_number >= 1),

  -- INV-24: ruta declarada por el organizador, inmutable tras publicar.
  unclaimed_route       VARCHAR(20) NOT NULL
                        CHECK (unclaimed_route IN ('REDRAW','CANCEL')),
  claim_sla_days        INTEGER NOT NULL,             -- por tramo de valor, §16.2
  delivery_sla_days     INTEGER NOT NULL,             -- por categoria, ampliable
  shipping_paid_by      VARCHAR(10) NOT NULL DEFAULT 'WINNER'
                        CHECK (shipping_paid_by IN ('WINNER','CLIENT')),
  max_concentration_bp  pct_basis NOT NULL DEFAULT 3000,   -- INV-13

  winners_count         INTEGER NOT NULL DEFAULT 1 CHECK (winners_count >= 1),
  created_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id              UUID NOT NULL,

  CONSTRAINT ux_raffles_code UNIQUE (raffle_code),
  CONSTRAINT ux_raffles_slug UNIQUE (market_code, slug),
  CONSTRAINT ck_raffles_status CHECK (status IN (
    'DRAFT','PENDING_VALUATION','PENDING_LEGAL','PENDING_APPROVAL','REJECTED',
    'SCHEDULED','ACTIVE','PAUSED','SOLD_OUT','ENDED_TIME','THRESHOLD_REACHED',
    'THRESHOLD_FAILED','MILESTONE_REACHED','READY_TO_DRAW','POOL_FROZEN','DRAW_EXECUTED',
    'IN_RESOLUTION','DELIVERY_ATTESTED','SETTLED','CLOSED','CANCELLED',
    'SUSPENDED_MARKET')),
  -- Invariante de pricing congelado en la entidad.
  CONSTRAINT ck_raffles_pricing CHECK (client_net_amount + libox_fee_amount = gross_required),
  CONSTRAINT ck_raffles_reserved CHECK (tickets_reserved <= total_tickets),
  CONSTRAINT ck_raffles_threshold CHECK (min_threshold IS NULL OR min_threshold <= total_tickets),
  -- T8 es modo de presentacion, no motor: exige tipo base y solo el es quien lo lleva.
  -- OJO: la comprobacion NOT NULL es imprescindible. Sin ella, con raffle_type='T8'
  -- y base_type NULL la expresion evalua a NULL, y un CHECK que evalua a NULL
  -- SE CONSIDERA SATISFECHO. La logica de tres valores deja pasar la fila.
  CONSTRAINT ck_raffles_base_type CHECK (
    (raffle_type =  'T8' AND base_type IS NOT NULL
                         AND base_type IN ('T1','T2','T3','T4','T5','T6','T7'))
 OR (raffle_type <> 'T8' AND base_type IS NULL)),
  -- T2 exige umbral; T3 y T5 exigen cierre por tiempo.
  CONSTRAINT ck_raffles_t2 CHECK (
    COALESCE(base_type, raffle_type) <> 'T2' OR min_threshold IS NOT NULL),
  CONSTRAINT ck_raffles_end_at CHECK (
    COALESCE(base_type, raffle_type) NOT IN ('T2','T3','T5') OR end_at IS NOT NULL),
  CONSTRAINT ck_raffles_winners CHECK (
    COALESCE(base_type, raffle_type) = 'T6' OR winners_count = 1),

  -- Sin recaudacion no hay precio ni pricing: los importes son cero.
  CONSTRAINT ck_raffles_regime_pricing CHECK (
    economic_regime = 'PAID'
    OR (ticket_price = 0 AND gross_required = 0 AND libox_fee_amount = 0
        AND client_net_amount = 0)),

  -- Origen de premio obligatorio fuera del regimen pagado, prohibido dentro.
  CONSTRAINT ck_raffles_prize_origin CHECK (
    (economic_regime = 'PAID'  AND prize_origin IS NULL)
 OR (economic_regime <> 'PAID' AND prize_origin IS NOT NULL)),

  -- INV-06-b: sin recaudacion, garantia sustitutiva obligatoria para publicar.
  CONSTRAINT ck_raffles_guarantee CHECK (
    economic_regime = 'PAID'
    OR published_at IS NULL
    OR substitute_guarantee_id IS NOT NULL),

  -- INV-40/41: rango de recaudacion. Suelo 1,25x; techo 4,0x con doble firma.
  CONSTRAINT ck_raffles_multiple_floor CHECK (
    economic_regime <> 'PAID' OR collection_multiple_bp IS NULL
    OR collection_multiple_bp >= 12500),
  CONSTRAINT ck_raffles_multiple_ceiling CHECK (
    economic_regime <> 'PAID' OR collection_multiple_bp IS NULL
    OR collection_multiple_bp <= 40000
    OR (multiple_override_by IS NOT NULL AND multiple_override_signer IS NOT NULL
        AND multiple_override_reason IS NOT NULL)),
  CONSTRAINT ck_raffles_multiple_signer CHECK (
    multiple_override_signer IS NULL OR multiple_override_signer <> multiple_override_by)
);

CREATE INDEX ix_raffles_discovery ON raffles (market_code, status, end_at)
  WHERE status IN ('ACTIVE','SCHEDULED');
CREATE INDEX ix_raffles_client ON raffles (client_id, status, created_at DESC);
CREATE INDEX ix_raffles_close_job ON raffles (end_at)
  WHERE status = 'ACTIVE' AND end_at IS NOT NULL;

-- INV-14: bases inmutables desde la publicacion.
CREATE TABLE raffle_terms (
  id              UUID PRIMARY KEY,
  raffle_id       UUID NOT NULL REFERENCES raffles(id),
  version         INTEGER NOT NULL DEFAULT 1,
  content         TEXT NOT NULL,
  content_hash    sha256_hex NOT NULL,
  pdf_object_key  VARCHAR(255),
  frozen_at       TIMESTAMPTZ,                        -- no nulo tras publicar
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ux_raffle_terms UNIQUE (raffle_id, version)
);

-- T4 PROGRESSIVE: hitos declarados en bases e inmutables tras publicar.
CREATE TABLE raffle_milestones (
  id              UUID PRIMARY KEY,
  raffle_id       UUID NOT NULL REFERENCES raffles(id),
  position        INTEGER NOT NULL CHECK (position >= 1),
  tickets_target  INTEGER NOT NULL CHECK (tickets_target > 0),
  description     VARCHAR(200) NOT NULL,
  unlocks_kind    VARCHAR(30) NOT NULL
                  CHECK (unlocks_kind IN ('ADDITIONAL_PRIZE','PRIZE_UPGRADE','DRAW_TRIGGER')),
  unlocked_prize_id UUID,   -- FK añadida en migracion 008, tras crear prizes
  reached_at      TIMESTAMPTZ,
  frozen_at       TIMESTAMPTZ,                       -- inmutable tras publicar
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ux_milestone_pos UNIQUE (raffle_id, position),
  CONSTRAINT ux_milestone_target UNIQUE (raffle_id, tickets_target),
  -- Solo un hito puede disparar el sorteo, y es el que cierra la progresion.
  CONSTRAINT ck_milestone_unlock CHECK (
    unlocks_kind <> 'ADDITIONAL_PRIZE' OR unlocked_prize_id IS NOT NULL)
);
CREATE INDEX ix_milestones_pending ON raffle_milestones (raffle_id, tickets_target)
  WHERE reached_at IS NULL;

-- T7 RECURRING: cada edicion es un raffle independiente con su propio pool y
-- su propia prueba. Esta tabla define la serie, no comparte estado entre ediciones.
CREATE TABLE raffle_recurrences (
  id                  UUID PRIMARY KEY,
  client_id           UUID NOT NULL REFERENCES clients(id),
  market_code         market_code NOT NULL REFERENCES markets(code),
  template_raffle_id  UUID REFERENCES raffles(id),
  frequency           VARCHAR(20) NOT NULL
                      CHECK (frequency IN ('DAILY','WEEKLY','BIWEEKLY','MONTHLY')),
  interval_count      INTEGER NOT NULL DEFAULT 1 CHECK (interval_count >= 1),
  next_edition_at     TIMESTAMPTZ,
  editions_created    INTEGER NOT NULL DEFAULT 0,
  max_editions        INTEGER,
  status              VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
                      CHECK (status IN ('ACTIVE','PAUSED','ENDED')),
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ix_recurrence_due ON raffle_recurrences (next_edition_at)
  WHERE status = 'ACTIVE';

CREATE TABLE raffle_media (
  id              UUID PRIMARY KEY,
  raffle_id       UUID NOT NULL REFERENCES raffles(id),
  object_key      VARCHAR(255) NOT NULL,
  content_hash    sha256_hex NOT NULL,
  media_kind      VARCHAR(20) NOT NULL CHECK (media_kind IN ('IMAGE','VIDEO')),
  position        INTEGER NOT NULL DEFAULT 0,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- RN-09: registro de toda transicion.
CREATE TABLE state_transitions (
  id              UUID NOT NULL,
  entity_type     VARCHAR(40) NOT NULL,
  entity_id       UUID NOT NULL,
  from_state      VARCHAR(40),
  to_state        VARCHAR(40) NOT NULL,
  actor_id        UUID,
  actor_subrole   VARCHAR(40),
  reason          TEXT,
  trace_id        UUID NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);
CREATE INDEX ix_transitions_entity ON state_transitions (entity_type, entity_id, created_at DESC);
CREATE INDEX ix_transitions_trace ON state_transitions (trace_id);


CREATE TABLE prizes (
  id                  UUID PRIMARY KEY,
  raffle_id           UUID NOT NULL REFERENCES raffles(id),
  category            VARCHAR(6) NOT NULL
                      CHECK (category IN ('P_A','P_B','P_C1','P_C2','P_D','P_E','P_F')),
  regime              VARCHAR(15) NOT NULL
                      CHECK (regime IN ('EXISTENTE','PRODUCIBLE')),
  title               VARCHAR(160) NOT NULL,
  description         TEXT,
  declared_value      money_amount NOT NULL,
  approved_value      money_amount,                   -- RN-107: valor rector
  currency            currency_code NOT NULL,
  unique_identifier   VARCHAR(120),                   -- IMEI, VIN, partida
  identifier_kind     VARCHAR(30),
  position            INTEGER NOT NULL DEFAULT 1,     -- T6 multi-ganador
  -- RN-19: costos y cargas declarados
  transfer_costs      JSONB NOT NULL DEFAULT '[]'::jsonb,
  recurring_charges   JSONB NOT NULL DEFAULT '[]'::jsonb,
  shipping_estimates  JSONB NOT NULL DEFAULT '[]'::jsonb,  -- por macrozona
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ux_prizes_raffle_pos UNIQUE (raffle_id, position)
);

-- RN-24: codigo del dia, vigencia 72 h.
-- Referencia diferida: raffle_milestones se crea en la migracion 007 y prizes
-- en la 008. La clave foranea se añade aqui para evitar dependencia circular.
ALTER TABLE raffle_milestones
  ADD CONSTRAINT fk_milestone_prize
  FOREIGN KEY (unlocked_prize_id) REFERENCES prizes(id) ON DELETE RESTRICT;

-- INV-44: categorias registrables prohibidas sin recaudacion, salvo custodia
-- efectiva. Todo el proceso de siete etapas se apoya en la retencion: sin
-- fondos retenidos la clausula de custodia del instrumento notarial queda vacia.
CREATE OR REPLACE FUNCTION assert_registrable_regime() RETURNS TRIGGER AS $$
DECLARE reg VARCHAR(20); guar UUID;
BEGIN
  IF NEW.category IN ('P_C1','P_C2') THEN
    SELECT economic_regime, substitute_guarantee_id INTO reg, guar
      FROM raffles WHERE id = NEW.raffle_id;
    IF reg <> 'PAID' AND guar IS NULL THEN
      RAISE EXCEPTION 'ERR_REGISTRABLE_NO_ESCROW: categorias registrables exigen recaudacion retenida o custodia efectiva';
    END IF;
  END IF;
  RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_registrable_regime
  BEFORE INSERT OR UPDATE ON prizes
  FOR EACH ROW EXECUTE FUNCTION assert_registrable_regime();

CREATE TABLE daily_codes (
  id              UUID PRIMARY KEY,
  raffle_id       UUID NOT NULL REFERENCES raffles(id),
  code            VARCHAR(12) NOT NULL,
  issued_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  expires_at      TIMESTAMPTZ NOT NULL,
  CONSTRAINT ux_daily_code UNIQUE (raffle_id, code)
);

CREATE TABLE prize_valuations (
  id                  UUID PRIMARY KEY,
  prize_id            UUID NOT NULL REFERENCES prizes(id),
  band                VARCHAR(2) NOT NULL CHECK (band IN ('V1','V2','V3','V4')),
  declared_value      money_amount NOT NULL,
  median_reference    money_amount,
  deviation_bp        INTEGER,                        -- (decl − mediana)/mediana en bp
  appraisal_value     money_amount,
  outcome             VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                      CHECK (outcome IN ('PENDING','APPROVED','OBSERVED',
                                         'REJECTED','AUTO_REJECTED')),
  approved_value      money_amount,
  reviewer_id         UUID,
  second_signer_id    UUID,                           -- INC-09
  review_reason       TEXT,
  external_checks     JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  decided_at          TIMESTAMPTZ,
  trace_id            UUID NOT NULL,
  -- INC-09: la segunda firma no puede ser la misma persona.
  CONSTRAINT ck_pv_second_signer CHECK (second_signer_id IS NULL
                                        OR second_signer_id <> reviewer_id)
);

CREATE TABLE prize_valuation_documents (
  id              UUID PRIMARY KEY,
  valuation_id    UUID NOT NULL REFERENCES prize_valuations(id),
  document_kind   VARCHAR(60) NOT NULL,
  object_key      VARCHAR(255) NOT NULL,
  content_hash    sha256_hex NOT NULL,
  mime_type       VARCHAR(80) NOT NULL,
  av_scan_status  VARCHAR(20) NOT NULL DEFAULT 'PENDING',
  daily_code_seen VARCHAR(12),                        -- RN-24
  verification_status VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                      CHECK (verification_status IN ('PENDING','VERIFIED',
                                                     'OBSERVED','REJECTED')),
  verified_by     UUID,
  verified_at     TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE prize_market_references (
  id              UUID PRIMARY KEY,
  valuation_id    UUID NOT NULL REFERENCES prize_valuations(id),
  source_name     VARCHAR(120) NOT NULL,
  source_url      TEXT NOT NULL,
  price           money_amount NOT NULL,
  currency        currency_code NOT NULL,
  captured_at     DATE NOT NULL,
  screenshot_key  VARCHAR(255),
  is_fresh        BOOLEAN NOT NULL DEFAULT true,   -- recalculado por job nocturno
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ix_pmr_valuation ON prize_market_references (valuation_id) WHERE is_fresh;

-- La antiguedad maxima de 30 dias (§7.3 del PRD) NO se impone por CHECK:
-- PostgreSQL exige expresiones inmutables y CURRENT_DATE es estable, de modo
-- que el DDL no se ejecuta. Ademas una regla dependiente del tiempo no puede
-- vivir en una restriccion que solo se evalua al escribir.
-- Se valida en el servicio al aprobar la valoracion y se recalcula en el job
-- refresh-market-reference-freshness (§12.6).

-- RN-22: toda excepcion a la regla de desviacion, con reporte periodico.
CREATE TABLE valuation_exceptions (
  id              UUID PRIMARY KEY,
  valuation_id    UUID NOT NULL REFERENCES prize_valuations(id),
  deviation_bp    INTEGER NOT NULL,
  justification   TEXT NOT NULL CHECK (length(justification) >= 50),
  approver_id     UUID NOT NULL,
  second_signer_id UUID NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ck_ve_signers CHECK (second_signer_id <> approver_id)
);


CREATE TABLE registrable_assets (
  id                  UUID PRIMARY KEY,
  prize_id            UUID NOT NULL REFERENCES prizes(id),
  asset_kind          VARCHAR(20) NOT NULL CHECK (asset_kind IN ('VEHICLE','REAL_ESTATE')),
  registry_id         VARCHAR(60) NOT NULL,          -- placa o partida registral
  registry_office     VARCHAR(120),
  owner_matches_client BOOLEAN NOT NULL DEFAULT false,
  marital_regime      VARCHAR(30),                   -- RN: bien social
  spouse_required     BOOLEAN NOT NULL DEFAULT false,
  spouse_consent_at   TIMESTAMPTZ,
  occupancy_status    VARCHAR(30),                   -- inmuebles
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- RN-17 y RN-30: la consulta la hace LIBOX; nunca vale el documento de la parte.
CREATE TABLE registry_queries (
  id              UUID NOT NULL,
  asset_id        UUID NOT NULL,
  query_kind      VARCHAR(40) NOT NULL
                  CHECK (query_kind IN ('OWNERSHIP','LIENS','PERIODIC_RECHECK',
                                        'FINAL_INSCRIPTION')),
  performed_by    VARCHAR(20) NOT NULL DEFAULT 'SYSTEM',
  provider        VARCHAR(60) NOT NULL,
  has_liens       BOOLEAN,
  owner_name_hash sha256_hex,
  raw_response_key VARCHAR(255),
  response_hash   sha256_hex NOT NULL,
  result          VARCHAR(20) NOT NULL
                  CHECK (result IN ('CLEAN','LIENS_FOUND','NOT_FOUND','ERROR')),
  trace_id        UUID NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);
CREATE INDEX ix_rq_asset ON registry_queries (asset_id, created_at DESC);

-- RN-27: bloqueo registral vigente durante toda la venta.
CREATE TABLE registry_blocks (
  id              UUID PRIMARY KEY,
  asset_id        UUID NOT NULL REFERENCES registrable_assets(id),
  block_reference VARCHAR(80) NOT NULL,
  granted_at      DATE NOT NULL,
  expires_at      DATE NOT NULL,
  renewed_from    UUID REFERENCES registry_blocks(id),
  document_key    VARCHAR(255) NOT NULL,
  document_hash   sha256_hex NOT NULL,
  status          VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
                  CHECK (status IN ('ACTIVE','EXPIRED','RELEASED')),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ck_rb_range CHECK (expires_at > granted_at)
);
CREATE INDEX ix_rb_expiry ON registry_blocks (expires_at) WHERE status = 'ACTIVE';

-- RN-26: plantilla unica versionada.
CREATE TABLE notarial_instruments (
  id                  UUID PRIMARY KEY,
  raffle_id           UUID NOT NULL REFERENCES raffles(id),
  template_version    VARCHAR(20) NOT NULL,
  notary_name         VARCHAR(160),
  notary_reference    VARCHAR(80),
  signed_at           DATE,
  object_key          VARCHAR(255) NOT NULL,
  content_hash        sha256_hex NOT NULL,
  custody_clause_ok   BOOLEAN NOT NULL DEFAULT false,   -- clausula 4, §8.2
  verified_by         UUID,
  verified_at         TIMESTAMPTZ,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE pc_workflow_stages (
  id                  UUID PRIMARY KEY,
  raffle_id           UUID NOT NULL REFERENCES raffles(id),
  stage               VARCHAR(3) NOT NULL
                      CHECK (stage IN ('E1','E2','E3','E4','E5','E6','E7')),
  status              VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                      CHECK (status IN ('PENDING','IN_REVIEW','APPROVED',
                                        'OBSERVED','REJECTED')),
  approver_id         UUID,
  second_signer_id    UUID,
  approval_reason     TEXT,
  sla_due_at          TIMESTAMPTZ,
  approved_at         TIMESTAMPTZ,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id            UUID NOT NULL,
  CONSTRAINT ux_pc_stage UNIQUE (raffle_id, stage),
  -- RN-32: motivo de al menos 100 caracteres al aprobar.
  CONSTRAINT ck_pc_reason CHECK (status <> 'APPROVED' OR length(approval_reason) >= 100),
  CONSTRAINT ck_pc_signer CHECK (second_signer_id IS NULL
                                 OR second_signer_id <> approver_id)
);

-- RN-29: lista cerrada. No existe campo "otros".
CREATE TABLE pc_stage_documents (
  id              UUID PRIMARY KEY,
  stage_id        UUID NOT NULL REFERENCES pc_workflow_stages(id),
  checklist_key   VARCHAR(60) NOT NULL,             -- clave tipificada
  required        BOOLEAN NOT NULL DEFAULT true,
  object_key      VARCHAR(255),
  content_hash    sha256_hex,
  status          VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                  CHECK (status IN ('PENDING','UPLOADED','VERIFIED','OBSERVED','REJECTED')),
  verified_by     UUID,
  verified_at     TIMESTAMPTZ,
  verification_source VARCHAR(60),                  -- RN-34
  notes           TEXT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ux_pc_doc UNIQUE (stage_id, checklist_key)
);

CREATE TABLE transfer_acts (
  id                  UUID PRIMARY KEY,
  raffle_id           UUID NOT NULL REFERENCES raffles(id),
  winner_user_id      UUID NOT NULL REFERENCES users(id),
  act_kind            VARCHAR(40) NOT NULL,
  notary_reference    VARCHAR(80),
  signed_at           DATE,
  filed_at            DATE,
  inscribed_at        DATE,
  inscription_verified_at TIMESTAMPTZ,               -- por consulta directa
  verification_query_id UUID,
  status              VARCHAR(30) NOT NULL DEFAULT 'PENDING'
                      CHECK (status IN ('PENDING','SIGNED','FILED','OBSERVED',
                                        'INSCRIBED','VERIFIED','FAILED')),
  observation_notes   TEXT,
  observation_due_at  TIMESTAMPTZ,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- RN-28: el organizador acepta el pago como acto propio.
CREATE TABLE client_transfer_acceptances (
  id              UUID PRIMARY KEY,
  raffle_id       UUID NOT NULL REFERENCES raffles(id),
  accepted_by     UUID NOT NULL REFERENCES users(id),
  statement       TEXT NOT NULL,
  ip_address      INET,
  device_id       UUID,
  accepted_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id        UUID NOT NULL,
  CONSTRAINT ux_cta_raffle UNIQUE (raffle_id)
);

CREATE TABLE winner_legal_readiness (
  id                  UUID PRIMARY KEY,
  raffle_id           UUID NOT NULL REFERENCES raffles(id),
  winner_user_id      UUID NOT NULL REFERENCES users(id),
  marital_status      VARCHAR(30),
  spouse_required     BOOLEAN NOT NULL DEFAULT false,
  spouse_verified_at  TIMESTAMPTZ,
  documents_complete  BOOLEAN NOT NULL DEFAULT false,
  charges_acknowledged BOOLEAN NOT NULL DEFAULT false,  -- E6: aceptacion informada
  accepted_at         TIMESTAMPTZ,
  declined_at         TIMESTAMPTZ,                      -- derecho de rechazo
  decline_reason      TEXT,
  status              VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                      CHECK (status IN ('PENDING','READY','DECLINED','INELIGIBLE')),
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE transfer_costs (
  id              UUID PRIMARY KEY,
  raffle_id       UUID NOT NULL REFERENCES raffles(id),
  cost_kind       VARCHAR(40) NOT NULL,
  estimated_amount money_amount NOT NULL,
  actual_amount   money_amount,
  currency        currency_code NOT NULL,
  borne_by        VARCHAR(10) NOT NULL CHECK (borne_by IN ('CLIENT','WINNER')),
  receipt_key     VARCHAR(255),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);


-- RN-52: clave provista por el cliente, unica por intento. Corrige el hash de cuerpo de V1.
CREATE TABLE idempotency_keys (
  id                UUID PRIMARY KEY,
  actor_id          UUID NOT NULL,
  endpoint          VARCHAR(120) NOT NULL,
  idempotency_key   VARCHAR(120) NOT NULL,
  request_hash      sha256_hex NOT NULL,
  status            VARCHAR(20) NOT NULL DEFAULT 'IN_FLIGHT'
                    CHECK (status IN ('IN_FLIGHT','COMPLETED','FAILED')),
  response_status   INTEGER,
  stored_response   JSONB,
  expires_at        TIMESTAMPTZ NOT NULL,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id          UUID NOT NULL,
  CONSTRAINT ux_idem UNIQUE (actor_id, endpoint, idempotency_key)
);
CREATE INDEX ix_idem_expiry ON idempotency_keys (expires_at);

-- RN-06-ter: una orden, un sorteo. El desglose de comision se congela por orden
-- y es unico por definicion; no existe carrito multi-sorteo en el MVP.
CREATE TABLE orders (
  id                  UUID PRIMARY KEY,
  market_code         market_code NOT NULL REFERENCES markets(code),
  raffle_id           UUID NOT NULL REFERENCES raffles(id),
  buyer_user_id       UUID NOT NULL REFERENCES users(id),
  quantity            INTEGER NOT NULL CHECK (quantity > 0),
  currency            currency_code NOT NULL,
  unit_price          money_amount NOT NULL,
  gross_amount        money_amount NOT NULL,
  libox_fee_amount    money_amount NOT NULL,
  client_net_amount   money_amount NOT NULL,
  refund_credit_used  money_amount NOT NULL DEFAULT 0,
  cash_amount         money_amount NOT NULL,           -- lo que pasa por el PSP
  status              VARCHAR(30) NOT NULL DEFAULT 'PENDING_PAYMENT'
                      CHECK (status IN ('PENDING_PAYMENT','PAID','EXPIRED',
                                        'CANCELLED','REFUNDED','CHARGEBACK')),
  reserved_until      TIMESTAMPTZ,                     -- RN-55
  paid_at             TIMESTAMPTZ,
  device_id           UUID,
  ip_address          INET,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id            UUID NOT NULL,
  CONSTRAINT ck_orders_split CHECK (client_net_amount + libox_fee_amount = gross_amount),
  CONSTRAINT ck_orders_cash  CHECK (cash_amount + refund_credit_used = gross_amount)
);
CREATE INDEX ix_orders_buyer ON orders (buyer_user_id, created_at DESC);
CREATE INDEX ix_orders_raffle ON orders (raffle_id, status);
CREATE INDEX ix_orders_expiry ON orders (reserved_until)
  WHERE status = 'PENDING_PAYMENT';

CREATE TABLE payments (
  id                  UUID PRIMARY KEY,
  order_id            UUID NOT NULL REFERENCES orders(id),
  provider            VARCHAR(40) NOT NULL,
  provider_reference  VARCHAR(120),
  preference_id       VARCHAR(120),
  method              VARCHAR(40),
  amount              money_amount NOT NULL,
  currency            currency_code NOT NULL,
  psp_fee_amount      money_amount NOT NULL DEFAULT 0,   -- RN-40
  status              VARCHAR(30) NOT NULL DEFAULT 'PENDING'
                      CHECK (status IN ('PENDING','APPROVED','REJECTED','CANCELLED',
                                        'REFUNDED','CHARGEBACK','IN_MEDIATION')),
  status_rank         SMALLINT NOT NULL DEFAULT 0,       -- RN-59: monotonia
  payer_document_hash sha256_hex,                        -- RN-121: titular distinto
  payer_instrument_hash sha256_hex,                      -- RN-123: medio compartido
  approved_at         TIMESTAMPTZ,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id            UUID NOT NULL,
  CONSTRAINT ux_payments_provider_ref UNIQUE (provider, provider_reference)
);
CREATE INDEX ix_payments_instrument ON payments (payer_instrument_hash)
  WHERE payer_instrument_hash IS NOT NULL;

-- RN-58: persistencia de la carga original antes de procesar.
CREATE TABLE psp_events (
  id                  UUID NOT NULL,
  provider            VARCHAR(40) NOT NULL,
  provider_event_id   VARCHAR(120) NOT NULL,
  topic               VARCHAR(60) NOT NULL,
  signature_valid     BOOLEAN NOT NULL,
  signature_ts        TIMESTAMPTZ,
  raw_payload         JSONB NOT NULL,
  payload_hash        sha256_hex NOT NULL,
  processing_status   VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                      CHECK (processing_status IN ('PENDING','PROCESSED',
                                                   'DUPLICATE','FAILED','IGNORED')),
  processing_error    TEXT,
  attempts            INTEGER NOT NULL DEFAULT 0,
  trace_id            UUID NOT NULL,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);
-- psp_events es log bruto particionado. NO deduplica: un indice unico sobre una
-- tabla particionada debe incluir la clave de particion, de modo que el mismo
-- provider_event_id con distinta marca temporal se insertaria dos veces.
CREATE INDEX ix_psp_events_lookup
  ON psp_events (provider, provider_event_id, created_at DESC);

-- P0: la deduplicacion vive en tabla NO particionada. Es la garantia real.
CREATE TABLE processed_psp_events (
  provider            VARCHAR(40) NOT NULL,
  provider_event_id   VARCHAR(120) NOT NULL,
  first_seen_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  psp_event_id        UUID NOT NULL,
  psp_event_created_at TIMESTAMPTZ NOT NULL,
  outcome             VARCHAR(20) NOT NULL DEFAULT 'PROCESSED'
                      CHECK (outcome IN ('PROCESSED','FAILED','IGNORED')),
  trace_id            UUID NOT NULL,
  PRIMARY KEY (provider, provider_event_id)
);

CREATE TABLE reconciliation_batches (
  id              UUID PRIMARY KEY,
  market_code     market_code NOT NULL,
  provider        VARCHAR(40) NOT NULL,
  business_date   DATE NOT NULL,
  report_key      VARCHAR(255),
  total_records   INTEGER NOT NULL DEFAULT 0,
  matched         INTEGER NOT NULL DEFAULT 0,
  exceptions      INTEGER NOT NULL DEFAULT 0,
  status          VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                  CHECK (status IN ('PENDING','RUNNING','COMPLETED','FAILED')),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ux_recon UNIQUE (provider, market_code, business_date)
);

CREATE TABLE reconciliation_exceptions (
  id              UUID PRIMARY KEY,
  batch_id        UUID NOT NULL REFERENCES reconciliation_batches(id),
  exception_kind  VARCHAR(40) NOT NULL,
  provider_reference VARCHAR(120),
  payment_id      UUID REFERENCES payments(id),
  expected_amount money_signed,
  actual_amount   money_signed,
  status          VARCHAR(20) NOT NULL DEFAULT 'OPEN'
                  CHECK (status IN ('OPEN','INVESTIGATING','RESOLVED','WRITTEN_OFF')),
  sla_due_at      TIMESTAMPTZ NOT NULL,
  resolution      TEXT,
  resolved_by     UUID,
  resolved_at     TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);


-- RN-06-quater: el pool es DERIVADO. Es el conjunto de tickets ISSUED en el
-- instante del congelamiento; no existe tabla de pool. Su fotografia inmutable
-- vive en draw_proofs.pool_snapshot_key.
CREATE TABLE tickets (
  id              UUID PRIMARY KEY,
  raffle_id       UUID NOT NULL REFERENCES raffles(id),
  order_id        UUID NOT NULL REFERENCES orders(id),
  owner_user_id   UUID NOT NULL REFERENCES users(id),
  ticket_number   INTEGER NOT NULL CHECK (ticket_number >= 1),
  status          VARCHAR(20) NOT NULL DEFAULT 'ISSUED'
                  CHECK (status IN ('ISSUED','VOIDED','REFUNDED')),
  issued_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  voided_at       TIMESTAMPTZ,
  void_reason     VARCHAR(60),
  trace_id        UUID NOT NULL,
  -- INV-11: el numero no se reasigna jamas dentro del mismo sorteo.
  CONSTRAINT ux_tickets_number UNIQUE (raffle_id, ticket_number)
);
CREATE INDEX ix_tickets_owner ON tickets (owner_user_id, issued_at DESC);
CREATE INDEX ix_tickets_pool ON tickets (raffle_id, ticket_number)
  WHERE status = 'ISSUED';
CREATE INDEX ix_tickets_order ON tickets (order_id);


-- RN-14-sexies: un solo codigo publico con cupo. El decremento es ATOMICO:
-- nunca se emiten mas participaciones que el cupo.
CREATE TABLE free_entry_campaigns (
  id                  UUID PRIMARY KEY,
  raffle_id           UUID NOT NULL REFERENCES raffles(id),
  code                VARCHAR(24) NOT NULL,
  quota_total         INTEGER NOT NULL CHECK (quota_total > 0),
  quota_used          INTEGER NOT NULL DEFAULT 0,
  status              VARCHAR(20) NOT NULL DEFAULT 'OPEN'
                      CHECK (status IN ('OPEN','EXHAUSTED','CLOSED')),
  -- RN-14-octies: ampliar diluye a quien ya entro. Solo antes de ejecutar,
  -- con autorizacion y notificacion a los inscritos.
  extended_from       INTEGER,
  extended_by         UUID,
  extension_reason    TEXT,
  participants_notified_at TIMESTAMPTZ,
  opens_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
  closes_at           TIMESTAMPTZ,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id            UUID NOT NULL,
  CONSTRAINT ux_fec_code UNIQUE (code),
  CONSTRAINT ck_fec_quota CHECK (quota_used <= quota_total),
  CONSTRAINT ck_fec_extension CHECK (
    extended_from IS NULL
    OR (extended_by IS NOT NULL AND extension_reason IS NOT NULL))
);

CREATE TABLE free_entry_grants (
  id                  UUID PRIMARY KEY,
  campaign_id         UUID NOT NULL REFERENCES free_entry_campaigns(id),
  raffle_id           UUID NOT NULL REFERENCES raffles(id),
  user_id             UUID NOT NULL REFERENCES users(id),
  ticket_id           UUID REFERENCES tickets(id),
  granted_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id            UUID NOT NULL,
  -- RN-14-quater: una participacion por persona. INV-42 en el esquema.
  CONSTRAINT ux_feg_user UNIQUE (raffle_id, user_id)
);

-- INV-06-b: garantia sustitutiva del escrow en oportunidades sin recaudacion.
CREATE TABLE substitute_guarantees (
  id                  UUID PRIMARY KEY,
  raffle_id           UUID NOT NULL REFERENCES raffles(id),
  guarantee_kind      VARCHAR(30) NOT NULL
                      CHECK (guarantee_kind IN ('CUSTODY','BANK_GUARANTEE','PREPAID_PLAN',
                                                'LIBOX_OWNED_PRIZE')),
  covered_amount      money_amount NOT NULL,
  currency            currency_code NOT NULL,
  document_key        VARCHAR(255),
  document_hash       sha256_hex,
  verified_by         UUID NOT NULL,
  verified_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  released_at         TIMESTAMPTZ,
  trace_id            UUID NOT NULL
);

-- Regimen promocional: plan de precio fijo, cobrado por adelantado (RN-14-undecies).
CREATE TABLE promotional_plans (
  id                  UUID PRIMARY KEY,
  client_id           UUID NOT NULL REFERENCES clients(id),
  market_code         market_code NOT NULL REFERENCES markets(code),
  raffles_per_month   INTEGER NOT NULL CHECK (raffles_per_month > 0),
  prize_value_band    VARCHAR(2) NOT NULL CHECK (prize_value_band IN ('V1','V2','V3','V4')),
  price               money_amount NOT NULL,
  currency            currency_code NOT NULL,
  prepaid_until       DATE NOT NULL,              -- cobrado por adelantado
  status              VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
                      CHECK (status IN ('ACTIVE','SUSPENDED','ENDED')),
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- RN-14-duodecies: cupo propio dentro del limite de oportunidades activas.
CREATE TABLE promotional_plan_usage (
  plan_id             UUID NOT NULL REFERENCES promotional_plans(id),
  period_month        DATE NOT NULL,
  raffles_used        INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (plan_id, period_month)
);

-- Publicado en POOL_FROZEN, antes de conocerse el resultado.
CREATE TABLE draw_commitments (
  id                  UUID PRIMARY KEY,
  raffle_id           UUID NOT NULL REFERENCES raffles(id),
  sequence            INTEGER NOT NULL DEFAULT 1,      -- 2 = re-sorteo
  pool_hash           sha256_hex NOT NULL,
  pool_size           INTEGER NOT NULL CHECK (pool_size > 0),
  commitment          sha256_hex NOT NULL,             -- H(server_seed)
  beacon_source       VARCHAR(40) NOT NULL,
  beacon_ref          VARCHAR(120) NOT NULL,           -- ronda FUTURA anunciada
  -- P0: propiedad INTRINSECA de la ronda, derivable de la propia fuente y no
  -- escrita por LIBOX. Es lo que permite a un tercero comprobar que la ronda
  -- no existia al comprometer. Sin esto se verifica aritmetica, no honestidad.
  beacon_round_kind   VARCHAR(20) NOT NULL
                      CHECK (beacon_round_kind IN ('ROUND_NUMBER','BLOCK_HEIGHT','ROUND_TIME')),
  beacon_round_value  VARCHAR(80) NOT NULL,
  beacon_round_time   TIMESTAMPTZ NOT NULL,            -- instante previsto de la ronda
  algorithm_version   VARCHAR(20) NOT NULL,
  winners_count       INTEGER NOT NULL DEFAULT 1,
  published_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  earliest_execution_at TIMESTAMPTZ NOT NULL,          -- INV-18
  trace_id            UUID NOT NULL,
  CONSTRAINT ux_commit UNIQUE (raffle_id, sequence),
  CONSTRAINT ck_commit_window CHECK (earliest_execution_at > published_at),
  -- INV-18: la ronda comprometida debe ser POSTERIOR a la publicacion del
  -- compromiso. Se impone en el esquema, no solo en el servicio.
  CONSTRAINT ck_commit_beacon_future CHECK (beacon_round_time > published_at),
  CONSTRAINT ck_commit_exec_after_round CHECK (earliest_execution_at >= beacon_round_time)
);

CREATE TABLE draw_executions (
  id                  UUID PRIMARY KEY,
  raffle_id           UUID NOT NULL REFERENCES raffles(id),
  commitment_id       UUID NOT NULL REFERENCES draw_commitments(id),
  sequence            INTEGER NOT NULL DEFAULT 1,
  server_seed         VARCHAR(128) NOT NULL,           -- revelado en ejecucion
  beacon_value        VARCHAR(256) NOT NULL,
  beacon_round_value  VARCHAR(80)  NOT NULL,           -- debe coincidir con el compromiso
  beacon_round_time   TIMESTAMPTZ  NOT NULL,           -- instante real de la ronda
  beacon_retrieved_at TIMESTAMPTZ NOT NULL,            -- auxiliar, NO probatorio
  seed_material       sha256_hex NOT NULL,
  executed_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id            UUID NOT NULL,
  -- INV-19: unicidad de ejecucion. Es la garantia real, no el bloqueo distribuido.
  CONSTRAINT ux_draw_exec UNIQUE (raffle_id, sequence),
  CONSTRAINT ux_draw_exec_commit UNIQUE (commitment_id)
);

CREATE TABLE draw_winners (
  id                  UUID PRIMARY KEY,
  execution_id        UUID NOT NULL REFERENCES draw_executions(id),
  position            INTEGER NOT NULL CHECK (position >= 1),
  winner_index        INTEGER NOT NULL,
  ticket_id           UUID NOT NULL REFERENCES tickets(id),
  ticket_number       INTEGER NOT NULL,
  winner_user_id      UUID NOT NULL REFERENCES users(id),
  prize_id            UUID NOT NULL REFERENCES prizes(id),
  CONSTRAINT ux_dw_position UNIQUE (execution_id, position),
  CONSTRAINT ux_dw_ticket   UNIQUE (execution_id, ticket_id)
);

CREATE TABLE draw_proofs (
  id                  UUID PRIMARY KEY,
  execution_id        UUID NOT NULL REFERENCES draw_executions(id),
  proof_document      JSONB NOT NULL,                 -- estructura en §5.5
  proof_hash          sha256_hex NOT NULL,
  pool_snapshot_key   VARCHAR(255) NOT NULL,          -- lista completa de tickets
  pool_snapshot_hash  sha256_hex NOT NULL,
  public_url_slug     VARCHAR(80) NOT NULL,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ux_proof_exec UNIQUE (execution_id),
  CONSTRAINT ux_proof_slug UNIQUE (public_url_slug)
);

-- RN-108: re-sorteo encadenado, maximo uno.
CREATE TABLE redraws (
  id                    UUID PRIMARY KEY,
  raffle_id             UUID NOT NULL REFERENCES raffles(id),
  original_execution_id UUID NOT NULL REFERENCES draw_executions(id),
  new_execution_id      UUID REFERENCES draw_executions(id),
  cause                 VARCHAR(30) NOT NULL
                        CHECK (cause IN ('WINNER_NO_CLAIM','SHIPPING_ABANDONED',
                                         'WINNER_DECLINED','WINNER_INELIGIBLE')),
  excluded_ticket_ids   UUID[] NOT NULL,
  authorized_by         UUID NOT NULL,                -- solo ADMIN
  authorization_reason  TEXT NOT NULL,
  new_claim_sla_days    INTEGER NOT NULL,             -- plazos reevaluados
  created_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id              UUID NOT NULL,
  -- Maximo un re-sorteo por sorteo.
  CONSTRAINT ux_redraw_raffle UNIQUE (raffle_id)
);


CREATE TABLE resolution_rooms (
  id                  UUID PRIMARY KEY,
  raffle_id           UUID NOT NULL REFERENCES raffles(id),
  raffle_code         VARCHAR(20) NOT NULL,             -- titulo de la sala
  winner_user_id      UUID NOT NULL REFERENCES users(id),
  client_id           UUID NOT NULL REFERENCES clients(id),
  prize_id            UUID NOT NULL REFERENCES prizes(id),
  prize_category      VARCHAR(6) NOT NULL,
  status              VARCHAR(30) NOT NULL DEFAULT 'ROOM_OPENED'
                      CHECK (status IN ('ROOM_OPENED','AWAITING_CLAIM','CLAIMED',
                                        'SHIPPING_QUOTED','SHIPPING_PAID','PICKUP_AGREED',
                                        'AWAITING_DELIVERY','EVIDENCE_SUBMITTED',
                                        'NEEDS_MORE_EVIDENCE','ATTESTED','DISPUTED',
                                        'SHIPPING_ABANDONED','NO_CLAIM_EXPIRED',
                                        'NO_DELIVERY','RESOLVED_DELIVERED',
                                        'RESOLVED_REDRAW','RESOLVED_CANCELLED')),
  client_joined_at    TIMESTAMPTZ,                      -- RN-73: solo tras reclamo
  claim_due_at        TIMESTAMPTZ NOT NULL,
  delivery_due_at     TIMESTAMPTZ,
  clock_paused_at     TIMESTAMPTZ,
  paused_days_used    INTEGER NOT NULL DEFAULT 0,
  extension_days_used INTEGER NOT NULL DEFAULT 0,
  head_message_hash   sha256_hex,                       -- cadena de mensajes
  frozen_at           TIMESTAMPTZ,
  root_hash           sha256_hex,                       -- RN-81: al cerrar
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id            UUID NOT NULL,
  CONSTRAINT ux_room_raffle UNIQUE (raffle_id, winner_user_id, prize_id)
);
CREATE INDEX ix_rooms_queue ON resolution_rooms (status, claim_due_at);
CREATE INDEX ix_rooms_due ON resolution_rooms (delivery_due_at)
  WHERE status IN ('AWAITING_DELIVERY','NEEDS_MORE_EVIDENCE');

CREATE TABLE room_participants (
  room_id         UUID NOT NULL REFERENCES resolution_rooms(id),
  user_id         UUID NOT NULL REFERENCES users(id),
  party           VARCHAR(20) NOT NULL
                  CHECK (party IN ('WINNER','CLIENT','SUPPORT','ADMIN')),
  can_write       BOOLEAN NOT NULL DEFAULT true,
  can_attest      BOOLEAN NOT NULL DEFAULT false,
  joined_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  left_at         TIMESTAMPTZ,
  PRIMARY KEY (room_id, user_id)
);

-- RN-74: asignacion equilibrada con prioridad por valor y plazo.
CREATE TABLE room_assignments (
  id              UUID PRIMARY KEY,
  room_id         UUID NOT NULL REFERENCES resolution_rooms(id),
  assignee_id     UUID NOT NULL REFERENCES users(id),
  assigned_by     UUID,
  assignment_kind VARCHAR(20) NOT NULL DEFAULT 'AUTO'
                  CHECK (assignment_kind IN ('AUTO','MANUAL','ESCALATION')),
  reason          TEXT,
  assigned_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  released_at     TIMESTAMPTZ
);
CREATE UNIQUE INDEX ux_room_active_assignee ON room_assignments (room_id)
  WHERE released_at IS NULL;

-- RN-75, RN-76: solo agregacion, encadenada por hash.
CREATE TABLE room_messages (
  id                UUID NOT NULL,
  room_id           UUID NOT NULL,
  sequence          INTEGER NOT NULL,
  author_id         UUID NOT NULL,
  author_party      VARCHAR(20) NOT NULL,
  body              TEXT NOT NULL,
  payload_hash      sha256_hex NOT NULL,
  prev_message_hash sha256_hex,                        -- NULL solo en sequence = 1
  visibility        VARCHAR(20) NOT NULL DEFAULT 'PARTIES'
                    CHECK (visibility IN ('PARTIES','INTERNAL','SYSTEM')),
  redaction_of      UUID,                              -- correccion, no edicion
  flagged_kind      VARCHAR(30),                       -- RN-93, RN-94
  server_ts         TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id          UUID NOT NULL,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);
-- Indice de consulta. NO garantiza unicidad de secuencia por el mismo motivo
-- que en psp_events: la clave de particion forma parte del indice.
CREATE INDEX ix_room_msg_seq ON room_messages (room_id, sequence, created_at);

-- P0: la secuencia se asigna desde tabla NO particionada, con bloqueo de fila.
-- Es lo que impide dos mensajes con el mismo room_id + sequence y, por tanto,
-- lo que sostiene la cadena de hashes como prueba.
CREATE TABLE room_message_sequences (
  room_id           UUID PRIMARY KEY REFERENCES resolution_rooms(id),
  last_sequence     INTEGER NOT NULL DEFAULT 0,
  last_message_hash sha256_hex,
  updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

REVOKE UPDATE, DELETE ON room_messages FROM libox_app;

CREATE TABLE room_evidence (
  id                UUID PRIMARY KEY,
  room_id           UUID NOT NULL REFERENCES resolution_rooms(id),
  message_id        UUID,
  uploaded_by       UUID NOT NULL REFERENCES users(id),
  uploader_party    VARCHAR(20) NOT NULL,
  evidence_kind     VARCHAR(60) NOT NULL,
  strength          VARCHAR(10) NOT NULL
                    CHECK (strength IN ('STRONG','MEDIUM','WEAK')),   -- §14.2 PRD
  object_key        VARCHAR(255) NOT NULL,
  content_hash      sha256_hex NOT NULL,
  mime_type         VARCHAR(80) NOT NULL,
  size_bytes        INTEGER NOT NULL,
  av_scan_status    VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                    CHECK (av_scan_status IN ('PENDING','CLEAN','INFECTED','ERROR')),
  daily_code_seen   VARCHAR(12),
  tracking_reference VARCHAR(120),
  verified_externally BOOLEAN NOT NULL DEFAULT false,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ix_evidence_room ON room_evidence (room_id, strength);

-- Clasificacion automatica de fuerza probatoria.
CREATE TABLE evidence_strength_rules (
  evidence_kind     VARCHAR(60) PRIMARY KEY,
  strength          VARCHAR(10) NOT NULL
                    CHECK (strength IN ('STRONG','MEDIUM','WEAK')),
  requires_external_verification BOOLEAN NOT NULL DEFAULT false,
  applies_categories VARCHAR(6)[] NOT NULL
);

CREATE TABLE shipping_quotes (
  id                UUID PRIMARY KEY,
  room_id           UUID NOT NULL REFERENCES resolution_rooms(id),
  carrier_name      VARCHAR(120) NOT NULL,
  service_level     VARCHAR(60),
  amount            money_amount NOT NULL,
  currency          currency_code NOT NULL,
  macrozone         VARCHAR(40) NOT NULL,
  selected          BOOLEAN NOT NULL DEFAULT false,
  paid_at           TIMESTAMPTZ,
  payment_reference VARCHAR(120),
  quote_due_at      TIMESTAMPTZ NOT NULL,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- INV-07: la atestacion es un hecho, no un movimiento de dinero.
CREATE TABLE delivery_attestations (
  id                UUID PRIMARY KEY,
  room_id           UUID NOT NULL REFERENCES resolution_rooms(id),
  raffle_id         UUID NOT NULL REFERENCES raffles(id),
  attested_by       UUID NOT NULL REFERENCES users(id),
  attester_subrole  VARCHAR(40) NOT NULL,
  second_signer_id  UUID,                              -- RN-85: obligatorio en P-C
  evidence_ids      UUID[] NOT NULL,
  strongest_evidence VARCHAR(10) NOT NULL,
  winner_confirmed  BOOLEAN NOT NULL DEFAULT false,
  statement         TEXT NOT NULL,
  attested_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  reverted_at       TIMESTAMPTZ,
  reverted_by       UUID,
  revert_reason     TEXT,
  trace_id          UUID NOT NULL,
  CONSTRAINT ck_att_signer CHECK (second_signer_id IS NULL
                                  OR second_signer_id <> attested_by)
);
CREATE UNIQUE INDEX ux_attestation_active ON delivery_attestations (room_id)
  WHERE reverted_at IS NULL;

-- RN-87: definiciones de plazo por categoria y tramo, y sus extensiones.
CREATE TABLE sla_definitions (
  market_code       market_code NOT NULL,
  sla_kind          VARCHAR(30) NOT NULL
                    CHECK (sla_kind IN ('CLAIM','DELIVERY','SHIPPING_CHOICE',
                                        'DISPUTE','PC_STAGE','SETTLEMENT_HOLD')),
  scope_key         VARCHAR(30) NOT NULL,              -- categoria o tramo
  days              INTEGER NOT NULL,
  business_days     BOOLEAN NOT NULL DEFAULT false,
  PRIMARY KEY (market_code, sla_kind, scope_key)
);

CREATE TABLE sla_extensions (
  id                UUID PRIMARY KEY,
  room_id           UUID REFERENCES resolution_rooms(id),
  stage_id          UUID REFERENCES pc_workflow_stages(id),
  granted_by        UUID NOT NULL,
  granter_subrole   VARCHAR(40) NOT NULL,
  days_granted      INTEGER NOT NULL CHECK (days_granted > 0),
  reason            TEXT NOT NULL,
  second_signer_id  UUID,
  participants_notified_at TIMESTAMPTZ,                -- RN-88
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);


CREATE TABLE disputes (
  id                UUID PRIMARY KEY,
  room_id           UUID NOT NULL REFERENCES resolution_rooms(id),
  raffle_id         UUID NOT NULL REFERENCES raffles(id),
  opened_by         UUID NOT NULL REFERENCES users(id),
  opener_party      VARCHAR(20) NOT NULL,
  -- RN-92: motivo de lista cerrada, nunca texto libre solo.
  reason_code       VARCHAR(40) NOT NULL
                    CHECK (reason_code IN ('NOT_RECEIVED','DAMAGED','NOT_AS_DESCRIBED',
                                           'INCOMPLETE','WRONG_ITEM','SERVICE_NOT_PROVIDED',
                                           'TRANSFER_NOT_COMPLETED','OTHER_TYPED')),
  narrative         TEXT,
  status            VARCHAR(30) NOT NULL DEFAULT 'OPEN'
                    CHECK (status IN ('OPEN','EVIDENCE_GATHERING','ESCALATED',
                                      'ADJUDICATING','RESOLVED','WITHDRAWN')),
  burden_on         VARCHAR(20),                       -- RN-90: carga invertida
  sla_due_at        TIMESTAMPTZ NOT NULL,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id          UUID NOT NULL
);

CREATE TABLE dispute_evidence (
  id              UUID PRIMARY KEY,
  dispute_id      UUID NOT NULL REFERENCES disputes(id),
  evidence_id     UUID NOT NULL REFERENCES room_evidence(id),
  submitted_by    UUID NOT NULL,
  party           VARCHAR(20) NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ux_dispute_evidence UNIQUE (dispute_id, evidence_id)
);

CREATE TABLE dispute_adjudications (
  id                  UUID PRIMARY KEY,
  dispute_id          UUID NOT NULL REFERENCES disputes(id),
  adjudicated_by      UUID NOT NULL REFERENCES users(id),
  outcome             VARCHAR(30) NOT NULL
                      CHECK (outcome IN ('FAVOR_WINNER','FAVOR_CLIENT',
                                         'PARTIAL','INCONCLUSIVE')),
  bad_faith_party     VARCHAR(20),                     -- RN-99
  reasoning           TEXT NOT NULL CHECK (length(reasoning) >= 100),
  evidence_considered UUID[] NOT NULL,
  decided_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  parties_notified_at TIMESTAMPTZ,
  trace_id            UUID NOT NULL,
  CONSTRAINT ux_adjudication UNIQUE (dispute_id)
);


CREATE TABLE settlements (
  id                  UUID PRIMARY KEY,
  raffle_id           UUID NOT NULL REFERENCES raffles(id),
  client_id           UUID NOT NULL REFERENCES clients(id),
  currency            currency_code NOT NULL,
  gross_collected     money_amount NOT NULL,
  libox_fee_amount    money_amount NOT NULL,
  adjustments         money_signed NOT NULL DEFAULT 0,
  chargeback_reserve  money_amount NOT NULL DEFAULT 0,
  net_payable         money_amount NOT NULL,
  status              VARCHAR(20) NOT NULL DEFAULT 'ACCRUED'
                      CHECK (status IN ('ACCRUED','ELIGIBLE','APPROVED','PAID',
                                        'HELD','REVERSED')),
  -- Los seis gates, evaluados de forma determinista (INV-23).
  gate_g1_draw        BOOLEAN NOT NULL DEFAULT false,
  gate_g2_delivery    BOOLEAN NOT NULL DEFAULT false,
  gate_g3_disputes    BOOLEAN NOT NULL DEFAULT false,
  gate_g4_chargeback  BOOLEAN NOT NULL DEFAULT false,
  gate_g5_payout      BOOLEAN NOT NULL DEFAULT false,
  gate_g6_ledger      BOOLEAN NOT NULL DEFAULT false,
  gates_evaluated_at  TIMESTAMPTZ,
  hold_until          TIMESTAMPTZ,
  hold_reason         TEXT,
  approved_by         UUID,
  second_signer_id    UUID,                            -- RN-50 en P-C
  paid_at             TIMESTAMPTZ,
  payment_reference   VARCHAR(120),
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id            UUID NOT NULL,
  CONSTRAINT ux_settlement_raffle UNIQUE (raffle_id),
  CONSTRAINT ck_settlement_net CHECK (
    net_payable = gross_collected - libox_fee_amount + adjustments - chargeback_reserve),
  -- INV-23: no se alcanza ELIGIBLE sin los seis gates.
  CONSTRAINT ck_settlement_gates CHECK (
    status NOT IN ('ELIGIBLE','APPROVED','PAID')
    OR (gate_g1_draw AND gate_g2_delivery AND gate_g3_disputes
        AND gate_g4_chargeback AND gate_g5_payout AND gate_g6_ledger))
);
CREATE INDEX ix_settlements_eligible ON settlements (status, hold_until);

CREATE TABLE settlement_holds (
  id              UUID PRIMARY KEY,
  settlement_id   UUID NOT NULL REFERENCES settlements(id),
  hold_kind       VARCHAR(30) NOT NULL
                  CHECK (hold_kind IN ('CHARGEBACK_WINDOW','RESERVE','DISPUTE',
                                       'COMPLIANCE','PAYOUT_CHANGE','RECONCILIATION')),
  amount          money_amount NOT NULL DEFAULT 0,
  hold_until      TIMESTAMPTZ,
  released_at     TIMESTAMPTZ,
  reason          TEXT NOT NULL,
  created_by      UUID,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);


CREATE TABLE ledger_accounts (
  code            VARCHAR(40) NOT NULL,
  currency        currency_code NOT NULL,
  nature          VARCHAR(10) NOT NULL
                  CHECK (nature IN ('ASSET','LIABILITY','INCOME','EXPENSE','EQUITY')),
  scoped_by       VARCHAR(20)
                  CHECK (scoped_by IN ('CLIENT','USER','RAFFLE')),
  name            VARCHAR(120) NOT NULL,
  PRIMARY KEY (code, currency)
);

CREATE TABLE journal_entries (
  id              UUID PRIMARY KEY,
  transaction_code VARCHAR(10) NOT NULL,              -- 'T-01'..'T-14'
  market_code     market_code NOT NULL,
  currency        currency_code NOT NULL,
  reference_type  VARCHAR(40) NOT NULL,
  reference_id    UUID NOT NULL,
  description     VARCHAR(255) NOT NULL,
  posted_by       UUID,
  reason          TEXT,                                -- obligatorio en T-14
  trace_id        UUID NOT NULL,
  posted_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ck_je_adjust_reason CHECK (transaction_code <> 'T-14' OR reason IS NOT NULL)
);
CREATE INDEX ix_je_reference ON journal_entries (reference_type, reference_id);
CREATE INDEX ix_je_trace ON journal_entries (trace_id);

CREATE TABLE journal_lines (
  id              UUID NOT NULL,
  entry_id        UUID NOT NULL REFERENCES journal_entries(id) ON DELETE RESTRICT,
  account_code    VARCHAR(40) NOT NULL,
  currency        currency_code NOT NULL,
  scope_id        UUID,                                -- cliente, usuario o sorteo
  debit           money_amount NOT NULL DEFAULT 0,
  credit          money_amount NOT NULL DEFAULT 0,
  posted_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (id, posted_at),
  CONSTRAINT ck_jl_one_side CHECK ((debit = 0) <> (credit = 0))
) PARTITION BY RANGE (posted_at);
CREATE INDEX ix_jl_entry ON journal_lines (entry_id);
CREATE INDEX ix_jl_account ON journal_lines (account_code, currency, posted_at);

REVOKE UPDATE, DELETE ON journal_lines FROM libox_app;


CREATE OR REPLACE FUNCTION assert_entry_balanced() RETURNS TRIGGER AS $$
DECLARE d BIGINT; c BIGINT;
BEGIN
  SELECT COALESCE(SUM(debit),0), COALESCE(SUM(credit),0) INTO d, c
    FROM journal_lines WHERE entry_id = NEW.id;
  IF d <> c THEN
    RAISE EXCEPTION 'ERR_LEDGER_UNBALANCED: entry % debit=% credit=%', NEW.id, d, c;
  END IF;
  IF d = 0 THEN
    RAISE EXCEPTION 'ERR_LEDGER_EMPTY: entry % sin lineas', NEW.id;
  END IF;
  RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE CONSTRAINT TRIGGER trg_entry_balanced
  AFTER INSERT ON journal_entries
  DEFERRABLE INITIALLY DEFERRED
  FOR EACH ROW EXECUTE FUNCTION assert_entry_balanced();


CREATE TABLE refund_credits (
  user_id         UUID NOT NULL REFERENCES users(id),
  currency        currency_code NOT NULL,
  balance         money_amount NOT NULL DEFAULT 0,     -- cache materializada
  lifetime_granted money_amount NOT NULL DEFAULT 0,
  lifetime_used   money_amount NOT NULL DEFAULT 0,
  lifetime_withdrawn money_amount NOT NULL DEFAULT 0,
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, currency)
);

CREATE TABLE refund_credit_entries (
  id              UUID PRIMARY KEY,
  user_id         UUID NOT NULL REFERENCES users(id),
  currency        currency_code NOT NULL,
  amount          money_signed NOT NULL,
  entry_kind      VARCHAR(30) NOT NULL
                  CHECK (entry_kind IN ('RAFFLE_CANCELLED','ORDER_REFUND',
                                        'PROMOTION_GRANT','PURCHASE_USE',
                                        'WITHDRAWAL','ADJUSTMENT')),
  reference_type  VARCHAR(40),
  reference_id    UUID,
  balance_after   money_amount NOT NULL,
  journal_entry_id UUID,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id        UUID NOT NULL
);
CREATE INDEX ix_rce_user ON refund_credit_entries (user_id, currency, created_at DESC);

-- RN-65: retiro por solicitud manual con verificacion.
CREATE TABLE refund_credit_withdrawals (
  id                  UUID PRIMARY KEY,
  user_id             UUID NOT NULL REFERENCES users(id),
  currency            currency_code NOT NULL,
  amount              money_amount NOT NULL,
  bank_details_enc    BYTEA NOT NULL,
  kyc_verified        BOOLEAN NOT NULL DEFAULT false,
  status              VARCHAR(20) NOT NULL DEFAULT 'REQUESTED'
                      CHECK (status IN ('REQUESTED','KYC_PENDING','APPROVED',
                                        'PAID','REJECTED')),
  approved_by         UUID,
  paid_at             TIMESTAMPTZ,
  payment_reference   VARCHAR(120),
  rejection_reason    TEXT,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id            UUID NOT NULL
);


CREATE TABLE spend_accumulators (
  id              UUID PRIMARY KEY,
  subject_type    VARCHAR(10) NOT NULL CHECK (subject_type IN ('USER','CLIENT')),
  subject_id      UUID NOT NULL,
  currency        currency_code NOT NULL,
  window_kind     VARCHAR(10) NOT NULL
                  CHECK (window_kind IN ('DAY','MONTH','YEAR','LIFETIME')),
  window_start    DATE NOT NULL,
  amount          money_amount NOT NULL DEFAULT 0,
  operations      INTEGER NOT NULL DEFAULT 0,
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ux_accum UNIQUE (subject_type, subject_id, currency, window_kind, window_start)
);
CREATE INDEX ix_accum_threshold ON spend_accumulators (subject_type, window_kind, amount DESC);

CREATE TABLE aml_thresholds (
  market_code     market_code NOT NULL,
  tier            SMALLINT NOT NULL,
  amount_from     money_amount NOT NULL,
  amount_to       money_amount,                        -- NULL = sin techo
  requirement     VARCHAR(40) NOT NULL
                  CHECK (requirement IN ('L1_VERIFICATION','L2_VERIFICATION',
                                         'SOURCE_DECLARATION','SOURCE_DOCUMENTATION',
                                         'PRIOR_APPROVAL')),
  alarm_severity  VARCHAR(15),
  PRIMARY KEY (market_code, tier)
);

CREATE TABLE aml_cases (
  id                  UUID PRIMARY KEY,
  subject_type        VARCHAR(10) NOT NULL,
  subject_id          UUID NOT NULL,
  trigger_kind        VARCHAR(40) NOT NULL,
  tier_reached        SMALLINT,
  status              VARCHAR(30) NOT NULL DEFAULT 'OPEN'
                      CHECK (status IN ('OPEN','AWAITING_DOCUMENTS','UNDER_REVIEW',
                                        'APPROVED','REJECTED','ESCALATED','CLOSED_NO_ACTION')),
  -- RN-144: la no-decision tambien se documenta.
  decision            VARCHAR(30),
  decision_reason     TEXT,
  decided_by          UUID,
  decided_at          TIMESTAMPTZ,
  sla_due_at          TIMESTAMPTZ NOT NULL,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id            UUID NOT NULL,
  CONSTRAINT ck_aml_decision CHECK (
    status NOT IN ('APPROVED','REJECTED','CLOSED_NO_ACTION')
    OR (decision_reason IS NOT NULL AND decided_by IS NOT NULL))
);

CREATE TABLE aml_case_documents (
  id              UUID PRIMARY KEY,
  case_id         UUID NOT NULL REFERENCES aml_cases(id),
  document_kind   VARCHAR(60) NOT NULL,
  object_key      VARCHAR(255) NOT NULL,
  content_hash    sha256_hex NOT NULL,
  retention_until DATE NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- RN-145: registro de operaciones apto para reporte.
CREATE TABLE operation_register (
  id              UUID NOT NULL,
  market_code     market_code NOT NULL,
  subject_type    VARCHAR(10) NOT NULL,
  subject_id      UUID NOT NULL,
  operation_kind  VARCHAR(40) NOT NULL,
  amount          money_amount NOT NULL,
  currency        currency_code NOT NULL,
  reference_type  VARCHAR(40) NOT NULL,
  reference_id    UUID NOT NULL,
  occurred_at     TIMESTAMPTZ NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

CREATE TABLE risk_rules (
  id              UUID PRIMARY KEY,
  code            VARCHAR(40) NOT NULL UNIQUE,
  family          VARCHAR(30) NOT NULL
                  CHECK (family IN ('VELOCITY','CORRELATION','CONCENTRATION',
                                    'FINANCIAL','DOCUMENTARY','ROOM_BEHAVIOR')),
  expression      JSONB NOT NULL,                      -- regla como dato, no codigo
  severity        VARCHAR(15) NOT NULL
                  CHECK (severity IN ('INFO','MEDIUM','HIGH')),
  action          VARCHAR(30) NOT NULL
                  CHECK (action IN ('ALARM','ALARM_AND_BLOCK','ALARM_AND_FREEZE')),
  enabled         BOOLEAN NOT NULL DEFAULT true,
  market_code     market_code,
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE risk_events (
  id              UUID NOT NULL,
  rule_code       VARCHAR(40),
  subject_type    VARCHAR(10) NOT NULL,
  subject_id      UUID NOT NULL,
  event_kind      VARCHAR(60) NOT NULL,
  severity        VARCHAR(15) NOT NULL,
  score_delta     INTEGER NOT NULL DEFAULT 0,
  context         JSONB NOT NULL DEFAULT '{}'::jsonb,
  device_id       UUID,
  ip_address      INET,
  trace_id        UUID NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);
CREATE INDEX ix_risk_subject ON risk_events (subject_type, subject_id, created_at DESC);


CREATE TABLE self_exclusions (
  id              UUID PRIMARY KEY,
  user_id         UUID NOT NULL REFERENCES users(id),
  duration_kind   VARCHAR(15) NOT NULL
                  CHECK (duration_kind IN ('D7','D30','D90','PERMANENT')),
  starts_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  -- RN-128: irreversible durante el plazo. NULL en permanente.
  ends_at         TIMESTAMPTZ,
  status          VARCHAR(15) NOT NULL DEFAULT 'ACTIVE'
                  CHECK (status IN ('ACTIVE','EXPIRED')),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id        UUID NOT NULL
);
CREATE UNIQUE INDEX ux_self_excl_active ON self_exclusions (user_id)
  WHERE status = 'ACTIVE';

REVOKE DELETE ON self_exclusions FROM libox_app;

CREATE TABLE spending_limits (
  id              UUID PRIMARY KEY,
  user_id         UUID NOT NULL REFERENCES users(id),
  currency        currency_code NOT NULL,
  window_kind     VARCHAR(10) NOT NULL
                  CHECK (window_kind IN ('DAY','WEEK','MONTH')),
  amount          money_amount NOT NULL,
  effective_from  TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ux_limit UNIQUE (user_id, currency, window_kind)
);

-- RN-133: asimetria. Bajar aplica ya; subir espera 24 h.
CREATE TABLE spending_limit_changes (
  id                UUID PRIMARY KEY,
  user_id           UUID NOT NULL REFERENCES users(id),
  currency          currency_code NOT NULL,
  window_kind       VARCHAR(10) NOT NULL,
  old_amount        money_amount,
  new_amount        money_amount NOT NULL,
  direction         VARCHAR(10) NOT NULL
                    CHECK (direction IN ('DECREASE','INCREASE')),
  requested_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  effective_at      TIMESTAMPTZ NOT NULL,
  applied_at        TIMESTAMPTZ,
  cancelled_at      TIMESTAMPTZ,
  trace_id          UUID NOT NULL,
  -- La asimetria se impone en el esquema, no solo en la aplicacion.
  CONSTRAINT ck_slc_asymmetry CHECK (
    (direction = 'DECREASE' AND effective_at <= requested_at)
    OR (direction = 'INCREASE' AND effective_at >= requested_at + INTERVAL '24 hours'))
);

CREATE TABLE responsible_play_events (
  id              UUID PRIMARY KEY,
  user_id         UUID NOT NULL REFERENCES users(id),
  event_kind      VARCHAR(40) NOT NULL
                  CHECK (event_kind IN ('SPEND_PANEL_VIEWED','THRESHOLD_NOTICE',
                                        'LIMIT_SET','LIMIT_BLOCKED_PURCHASE',
                                        'SELF_EXCLUSION_STARTED','SELF_EXCLUSION_ENDED',
                                        'INDEPENDENCE_NOTICE_SHOWN')),
  context         JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);


CREATE TABLE analytics_events (
  id                UUID NOT NULL,
  event_name        VARCHAR(60) NOT NULL,
  trace_id          UUID NOT NULL,
  session_id        UUID NOT NULL,
  actor_id          UUID,
  behavioral_zone   VARCHAR(15) CHECK (behavioral_zone IN ('ATTRACTION','DECISION')),
  decision_class    VARCHAR(4)  CHECK (decision_class IN ('B0','B1','B2','B3','B4')),
  lbpf_patterns     VARCHAR(10)[],
  surface           VARCHAR(20),
  entity_type       VARCHAR(40),
  entity_id         UUID,
  properties        JSONB NOT NULL DEFAULT '{}'::jsonb,
  app_version       VARCHAR(20) NOT NULL,
  market_code       market_code NOT NULL,
  server_ts         TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (id, server_ts)
) PARTITION BY RANGE (server_ts);
CREATE INDEX ix_ae_name ON analytics_events (event_name, server_ts);
CREATE INDEX ix_ae_session ON analytics_events (session_id, server_ts);

CREATE TABLE survey_instruments (
  id              UUID PRIMARY KEY,
  code            VARCHAR(30) NOT NULL UNIQUE,
  question        TEXT NOT NULL,
  answer_kind     VARCHAR(20) NOT NULL
                  CHECK (answer_kind IN ('NUMERIC','SINGLE_CHOICE','SCALE_1_5','BOOLEAN')),
  options         JSONB,
  feeds_kpi       VARCHAR(4)[] NOT NULL,
  trigger_moment  VARCHAR(30) NOT NULL
                  CHECK (trigger_moment IN ('POST_PURCHASE','T_PLUS_24H','POST_DELIVERY')),
  enabled         BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE survey_responses (
  id              UUID PRIMARY KEY,
  instrument_id   UUID NOT NULL REFERENCES survey_instruments(id),
  user_id         UUID NOT NULL REFERENCES users(id),
  raffle_id       UUID,
  answer_numeric  NUMERIC(12,2),
  answer_text     VARCHAR(120),
  is_correct      BOOLEAN,                             -- P3: con tolerancia del 10 %
  market_code     market_code NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ix_sr_instrument ON survey_responses (instrument_id, created_at DESC);

CREATE TABLE kpi_snapshots (
  id              UUID PRIMARY KEY,
  kpi_code        VARCHAR(4) NOT NULL,
  market_code     market_code NOT NULL,
  window_start    DATE NOT NULL,
  window_end      DATE NOT NULL,
  sample_size     INTEGER NOT NULL,
  successes       INTEGER NOT NULL,
  proportion      NUMERIC(6,4) NOT NULL,
  wilson_lower    NUMERIC(6,4) NOT NULL,
  wilson_upper    NUMERIC(6,4) NOT NULL,
  threshold       NUMERIC(6,4) NOT NULL,
  status          VARCHAR(20) NOT NULL
                  CHECK (status IN ('OK','INSUFFICIENT_DATA','AT_RISK','BREACH')),
  consecutive_breaches INTEGER NOT NULL DEFAULT 0,
  computed_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ux_kpi_snapshot UNIQUE (kpi_code, market_code, window_end)
);

-- RN-167: un solo panel.
CREATE TABLE alarms (
  id                UUID PRIMARY KEY,
  alarm_type        VARCHAR(40) NOT NULL,
  family            VARCHAR(20) NOT NULL
                    CHECK (family IN ('BEHAVIORAL','RISK','SLA','CONCENTRATION',
                                      'COMPLIANCE','RECONCILIATION','LEDGER',
                                      'REGISTRY','OPERATIONAL')),
  severity          VARCHAR(15) NOT NULL
                    CHECK (severity IN ('INFO','MEDIUM','HIGH')),
  entity_type       VARCHAR(40) NOT NULL,
  entity_id         UUID NOT NULL,
  market_code       market_code NOT NULL,
  title             VARCHAR(160) NOT NULL,
  context           JSONB NOT NULL DEFAULT '{}'::jsonb,
  trace_id          UUID,
  -- RN-169: dueño nominal, nunca colectivo.
  owner_id          UUID NOT NULL,
  sla_due_at        TIMESTAMPTZ NOT NULL,
  status            VARCHAR(20) NOT NULL DEFAULT 'OPEN'
                    CHECK (status IN ('OPEN','ACKNOWLEDGED','ESCALATED','RESOLVED')),
  escalated_at      TIMESTAMPTZ,
  escalated_to      UUID,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ix_alarms_queue ON alarms (status, severity, sla_due_at);
CREATE INDEX ix_alarms_owner ON alarms (owner_id, status);

CREATE TABLE alarm_resolutions (
  id              UUID PRIMARY KEY,
  alarm_id        UUID NOT NULL REFERENCES alarms(id),
  resolved_by     UUID NOT NULL,
  outcome         VARCHAR(30) NOT NULL
                  CHECK (outcome IN ('ACTION_TAKEN','NO_ACTION_NEEDED',
                                     'FALSE_POSITIVE','ESCALATED')),
  -- RN-172: la conclusion de que no hay problema tambien se documenta.
  reason          TEXT NOT NULL CHECK (length(reason) >= 20),
  actions         JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ux_alarm_resolution UNIQUE (alarm_id)
);

CREATE TABLE notification_templates (
  id              UUID PRIMARY KEY,
  code            VARCHAR(60) NOT NULL,
  market_code     market_code NOT NULL,
  channel         VARCHAR(20) NOT NULL
                  CHECK (channel IN ('EMAIL','SMS','WHATSAPP','PUSH','IN_APP')),
  version         INTEGER NOT NULL,
  subject         VARCHAR(200),
  body            TEXT NOT NULL,
  is_critical     BOOLEAN NOT NULL DEFAULT false,      -- exento de tope de frecuencia
  is_commercial   BOOLEAN NOT NULL DEFAULT false,      -- suprimido por autoexclusion
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ux_ntpl UNIQUE (code, market_code, channel, version)
);

CREATE TABLE notification_attempts (
  id                UUID NOT NULL,
  template_code     VARCHAR(60) NOT NULL,
  channel           VARCHAR(20) NOT NULL,
  user_id           UUID NOT NULL,
  reference_type    VARCHAR(40),
  reference_id      UUID,
  destination_masked VARCHAR(60) NOT NULL,             -- nunca en claro
  attempt_number    INTEGER NOT NULL DEFAULT 1,
  provider          VARCHAR(40),
  provider_status   VARCHAR(30)
                    CHECK (provider_status IN ('QUEUED','SENT','DELIVERED',
                                               'BOUNCED','FAILED','READ')),
  provider_reference VARCHAR(120),
  server_ts         TIMESTAMPTZ NOT NULL DEFAULT now(),
  trace_id          UUID NOT NULL,
  PRIMARY KEY (id, server_ts)
) PARTITION BY RANGE (server_ts);
CREATE INDEX ix_na_user_ref ON notification_attempts (user_id, reference_id, server_ts);

CREATE TABLE notification_preferences (
  user_id         UUID NOT NULL REFERENCES users(id),
  channel         VARCHAR(20) NOT NULL,
  commercial_optin BOOLEAN NOT NULL DEFAULT false,
  quiet_from      TIME,
  quiet_to        TIME,
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, channel)
);

CREATE TABLE audit_events (
  id              UUID NOT NULL,
  actor_id        UUID,
  actor_subrole   VARCHAR(40),
  action          VARCHAR(80) NOT NULL,
  entity_type     VARCHAR(40) NOT NULL,
  entity_id       UUID,
  before_state    JSONB,
  after_state     JSONB,
  reason          TEXT,
  ip_address      INET,
  device_id       UUID,
  -- Encadenamiento por hash. Obligatorio en acciones criticas (§3.14.1).
  critical        BOOLEAN NOT NULL DEFAULT false,
  payload_hash    sha256_hex,
  prev_audit_hash sha256_hex,
  trace_id        UUID NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (id, created_at),
  CONSTRAINT ck_audit_hash CHECK (NOT critical OR payload_hash IS NOT NULL)
) PARTITION BY RANGE (created_at);
CREATE INDEX ix_audit_entity ON audit_events (entity_type, entity_id, created_at DESC);
CREATE INDEX ix_audit_trace ON audit_events (trace_id);
CREATE INDEX ix_audit_actor ON audit_events (actor_id, created_at DESC);

REVOKE UPDATE, DELETE ON audit_events FROM libox_app;

-- RN-204: un fallo de auditoria nunca revierte un cobro exitoso.
-- RN-203-bis: quien miro que es tan relevante como quien cambio que.
-- Cubre consultas de rol interno a datos de terceros, no la navegacion de
-- participantes ni organizadores, que va a analitica con otra retencion.
CREATE TABLE audit_access_events (
  id              UUID NOT NULL,
  actor_id        UUID NOT NULL,
  actor_subrole   VARCHAR(40) NOT NULL,
  resource_type   VARCHAR(40) NOT NULL
                  CHECK (resource_type IN ('RESOLUTION_ROOM','AML_CASE','IDENTITY_DOCUMENT',
                                           'ROOM_EVIDENCE','PAYOUT_INSTRUCTION','USER_PROFILE',
                                           'FORENSIC_EXPORT')),
  resource_id     UUID NOT NULL,
  subject_user_id UUID,
  reason          TEXT,
  ip_address      INET,
  trace_id        UUID NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);
CREATE INDEX ix_aae_actor ON audit_access_events (actor_id, created_at DESC);
CREATE INDEX ix_aae_resource ON audit_access_events (resource_type, resource_id, created_at DESC);

REVOKE UPDATE, DELETE ON audit_access_events FROM libox_app;

CREATE TABLE audit_emergency_queue (
  id              UUID PRIMARY KEY,
  -- Columnas buscables: soporte y SRE necesitan filtrar en incidente sin
  -- recorrer JSONB.
  trace_id        UUID NOT NULL,
  entity_type     VARCHAR(40) NOT NULL,
  entity_id       UUID,
  action          VARCHAR(80) NOT NULL,
  severity        VARCHAR(15) NOT NULL DEFAULT 'HIGH'
                  CHECK (severity IN ('MEDIUM','HIGH')),
  payload         JSONB NOT NULL,
  failure_reason  TEXT NOT NULL,
  attempts        INTEGER NOT NULL DEFAULT 0,
  last_error_at   TIMESTAMPTZ,
  next_attempt_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  resolved_at     TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ix_aeq_pending ON audit_emergency_queue (next_attempt_at)
  WHERE resolved_at IS NULL;
CREATE INDEX ix_aeq_trace ON audit_emergency_queue (trace_id);

CREATE TABLE event_outbox (
  id              UUID NOT NULL,
  event_name      VARCHAR(80) NOT NULL,
  schema_version  INTEGER NOT NULL DEFAULT 1,
  aggregate_type  VARCHAR(40) NOT NULL,
  aggregate_id    UUID NOT NULL,
  payload         JSONB NOT NULL,
  trace_id        UUID NOT NULL,
  status          VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                  CHECK (status IN ('PENDING','DISPATCHED','FAILED','DEAD')),
  attempts        INTEGER NOT NULL DEFAULT 0,
  dispatched_at   TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);
CREATE INDEX ix_outbox_pending ON event_outbox (created_at) WHERE status = 'PENDING';


CREATE TABLE attribution_touches (
  id              UUID PRIMARY KEY,
  session_id      UUID NOT NULL,
  user_id         UUID,
  source          VARCHAR(60),
  medium          VARCHAR(60),
  campaign        VARCHAR(120),
  landing_surface VARCHAR(20),
  touch_kind      VARCHAR(20) NOT NULL
                  CHECK (touch_kind IN ('FIRST','LAST','REGISTRATION','PURCHASE')),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- RN-190: recompensa por registro verificado, nunca por gasto del referido.
CREATE TABLE referrals (
  id                  UUID PRIMARY KEY,
  referrer_user_id    UUID NOT NULL REFERENCES users(id),
  referred_user_id    UUID REFERENCES users(id),
  code                VARCHAR(20) NOT NULL UNIQUE,
  status              VARCHAR(20) NOT NULL DEFAULT 'ISSUED'
                      CHECK (status IN ('ISSUED','REGISTERED','VERIFIED','REWARDED','VOID')),
  reward_amount       money_amount,
  reward_currency     currency_code,
  rewarded_at         TIMESTAMPTZ,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ux_referred UNIQUE (referred_user_id)
);

CREATE TABLE promotions (
  id                UUID PRIMARY KEY,
  code              VARCHAR(30) NOT NULL UNIQUE,
  market_code       market_code NOT NULL,
  grant_amount      money_amount NOT NULL,
  currency          currency_code NOT NULL,
  max_grants        INTEGER,
  grants_used       INTEGER NOT NULL DEFAULT 0,
  valid_from        TIMESTAMPTZ NOT NULL,
  valid_to          TIMESTAMPTZ NOT NULL,
  segment_rule      JSONB,
  enabled           BOOLEAN NOT NULL DEFAULT true,
  created_by        UUID NOT NULL,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE promotion_grants (
  id              UUID PRIMARY KEY,
  promotion_id    UUID NOT NULL REFERENCES promotions(id),
  user_id         UUID NOT NULL REFERENCES users(id),
  amount          money_amount NOT NULL,
  currency        currency_code NOT NULL,
  credit_entry_id UUID,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ux_promo_grant UNIQUE (promotion_id, user_id)
);

CREATE TABLE featured_placements (
  id              UUID PRIMARY KEY,
  raffle_id       UUID NOT NULL REFERENCES raffles(id),
  placement_kind  VARCHAR(20) NOT NULL
                  CHECK (placement_kind IN ('PAID','ORGANIC_VOLUME','ORGANIC_NEW',
                                            'ORGANIC_CLOSING','ORGANIC_VELOCITY')),
  -- RN-187 y RN-188: etiqueta y razon siempre visibles.
  label           VARCHAR(60) NOT NULL,
  reason_text     VARCHAR(120) NOT NULL,
  position        INTEGER NOT NULL,
  starts_at       TIMESTAMPTZ NOT NULL,
  ends_at         TIMESTAMPTZ NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE waitlists (
  id              UUID PRIMARY KEY,
  user_id         UUID NOT NULL REFERENCES users(id),
  subject_kind    VARCHAR(20) NOT NULL
                  CHECK (subject_kind IN ('CLIENT','CATEGORY','RAFFLE')),
  subject_id      VARCHAR(60) NOT NULL,
  notified_at     TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ux_waitlist UNIQUE (user_id, subject_kind, subject_id)
);

-- RN-194-ter: codigo permanente de organizador. NO otorga participacion.
CREATE TABLE organizer_referral_codes (
  client_id       UUID PRIMARY KEY REFERENCES clients(id),
  code            VARCHAR(20) NOT NULL UNIQUE,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Instrumenta H-07: origen del usuario y compra cruzada.
CREATE TABLE user_attributions (
  user_id             UUID PRIMARY KEY REFERENCES users(id),
  origin_client_id    UUID REFERENCES clients(id),
  origin_code         VARCHAR(20),
  origin_kind         VARCHAR(20) NOT NULL
                      CHECK (origin_kind IN ('ORGANIZER_CODE','FREE_CAMPAIGN','ORGANIC','CAMPAIGN')),
  registered_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ix_ua_origin ON user_attributions (origin_client_id);

-- LIBOX Club. INV-46: jamas otorga participaciones ni probabilidad.
CREATE TABLE subscription_plans (
  id                  UUID PRIMARY KEY,
  market_code         market_code NOT NULL REFERENCES markets(code),
  code                VARCHAR(30) NOT NULL,
  price               money_amount NOT NULL,
  currency            currency_code NOT NULL,
  period_months       INTEGER NOT NULL DEFAULT 1,
  -- INV-46 impuesto en el esquema: ninguna columna otorga participaciones.
  grants_entries      BOOLEAN NOT NULL DEFAULT false
                      CHECK (grants_entries = false),
  enabled             BOOLEAN NOT NULL DEFAULT false,
  CONSTRAINT ux_sp_code UNIQUE (market_code, code)
);

CREATE TABLE subscriptions (
  id                  UUID PRIMARY KEY,
  user_id             UUID NOT NULL REFERENCES users(id),
  plan_id             UUID NOT NULL REFERENCES subscription_plans(id),
  status              VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
                      CHECK (status IN ('ACTIVE','PAST_DUE','CANCELLED','ENDED')),
  started_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  current_period_end  TIMESTAMPTZ NOT NULL,
  cancelled_at        TIMESTAMPTZ,
  trace_id            UUID NOT NULL
);
CREATE UNIQUE INDEX ux_sub_active ON subscriptions (user_id)
  WHERE status IN ('ACTIVE','PAST_DUE');

CREATE TABLE partners (
  id              UUID PRIMARY KEY,
  market_code     market_code NOT NULL REFERENCES markets(code),
  name            VARCHAR(160) NOT NULL,
  status          VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
                  CHECK (status IN ('ACTIVE','SUSPENDED','ENDED')),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE benefits (
  id              UUID PRIMARY KEY,
  partner_id      UUID NOT NULL REFERENCES partners(id),
  title           VARCHAR(160) NOT NULL,
  benefit_kind    VARCHAR(30) NOT NULL
                  CHECK (benefit_kind IN ('DISCOUNT','EARLY_ACCESS','ALERT','EXPERIENCE')),
  -- RN-194-octies: jamas descuento sobre el precio del ticket.
  applies_to_tickets BOOLEAN NOT NULL DEFAULT false
                     CHECK (applies_to_tickets = false),
  max_per_user_period INTEGER,
  valid_from      TIMESTAMPTZ NOT NULL,
  valid_to        TIMESTAMPTZ NOT NULL,
  enabled         BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE benefit_redemptions (
  id              UUID PRIMARY KEY,
  benefit_id      UUID NOT NULL REFERENCES benefits(id),
  user_id         UUID NOT NULL REFERENCES users(id),
  redeemed_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  reference       VARCHAR(80)
);

CREATE TABLE leads (
  id              UUID PRIMARY KEY,
  market_code     market_code NOT NULL,
  contact_name    VARCHAR(120),
  contact_email   email_addr,
  contact_phone   phone_e164,
  company         VARCHAR(160),
  simulated_prize_value money_amount,
  source          VARCHAR(60),
  status          VARCHAR(20) NOT NULL DEFAULT 'NEW'
                  CHECK (status IN ('NEW','CONTACTED','QUALIFIED','ONBOARDED','LOST')),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);


CREATE TABLE subrole_assignments (
  id              UUID PRIMARY KEY,
  user_id         UUID NOT NULL REFERENCES users(id),
  subrole         VARCHAR(40) NOT NULL,
  granted_by      UUID NOT NULL,
  second_signer_id UUID,                        -- RN-05-quater
  reason          TEXT NOT NULL,
  granted_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  revoked_at      TIMESTAMPTZ,
  revoked_by      UUID,
  revoke_reason   TEXT,
  CONSTRAINT ux_subrole UNIQUE (user_id, subrole)
);
CREATE INDEX ix_subrole_active ON subrole_assignments (user_id) WHERE revoked_at IS NULL;

-- Techo de privilegio (PRD MVP V8 §2.6.1). Quien puede crear usuarios puede
-- crear privilegios: sin esta matriz, delegar el alta produce escalada.
CREATE TABLE subrole_grant_matrix (
  granter_subrole   VARCHAR(40) NOT NULL,
  grantable_subrole VARCHAR(40) NOT NULL,
  requires_second_signature BOOLEAN NOT NULL DEFAULT false,
  PRIMARY KEY (granter_subrole, grantable_subrole)
);

-- RN-05-quinquies: suspender es inmediato y distribuido; restaurar es concentrado.
CREATE TABLE internal_account_suspensions (
  id                UUID PRIMARY KEY,
  user_id           UUID NOT NULL REFERENCES users(id),
  suspended_by      UUID NOT NULL REFERENCES users(id),
  suspender_subrole VARCHAR(40) NOT NULL,
  reason            TEXT NOT NULL CHECK (length(reason) >= 20),
  suspended_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  restored_by       UUID REFERENCES users(id),   -- solo ADMIN_SUPER
  restored_at       TIMESTAMPTZ,
  restore_reason    TEXT,
  trace_id          UUID NOT NULL,
  CONSTRAINT ck_susp_self CHECK (suspended_by <> user_id),
  CONSTRAINT ck_susp_restore CHECK (restored_at IS NULL
    OR (restored_by IS NOT NULL AND restore_reason IS NOT NULL))
);
CREATE UNIQUE INDEX ux_susp_active ON internal_account_suspensions (user_id)
  WHERE restored_at IS NULL;

CREATE TABLE subrole_incompatibilities (
  code            VARCHAR(10) PRIMARY KEY,             -- 'INC-01'..'INC-11'
  subrole_a       VARCHAR(40) NOT NULL,
  subrole_b       VARCHAR(40) NOT NULL,
  rationale       TEXT NOT NULL,
  enforcement     VARCHAR(20) NOT NULL
                  CHECK (enforcement IN ('ASSIGNMENT','RUNTIME','BOTH'))
);


-- RN-05-bis y RN-05-ter: nadie otorga por encima de su techo ni a si mismo.
CREATE OR REPLACE FUNCTION assert_grant_ceiling() RETURNS TRIGGER AS $$
DECLARE allowed BOOLEAN; needs_second BOOLEAN; granter_role VARCHAR(40);
BEGIN
  IF NEW.granted_by = NEW.user_id THEN
    RAISE EXCEPTION 'ERR_RBAC_SELF_GRANT: nadie se otorga un subrol a si mismo';
  END IF;
  SELECT EXISTS (
    SELECT 1 FROM subrole_assignments sa
      JOIN subrole_grant_matrix m ON m.granter_subrole = sa.subrole
     WHERE sa.user_id = NEW.granted_by
       AND sa.revoked_at IS NULL
       AND m.grantable_subrole = NEW.subrole
  ) INTO allowed;
  IF NOT allowed THEN
    RAISE EXCEPTION 'ERR_RBAC_GRANT_CEILING: % no puede otorgar %',
                    NEW.granted_by, NEW.subrole;
  END IF;
  SELECT bool_or(m.requires_second_signature) INTO needs_second
    FROM subrole_assignments sa
    JOIN subrole_grant_matrix m ON m.granter_subrole = sa.subrole
   WHERE sa.user_id = NEW.granted_by AND sa.revoked_at IS NULL
     AND m.grantable_subrole = NEW.subrole;
  IF needs_second AND NEW.second_signer_id IS NULL THEN
    RAISE EXCEPTION 'ERR_RBAC_SECOND_SIGNATURE_REQUIRED: % toca dinero', NEW.subrole;
  END IF;
  RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_grant_ceiling
  BEFORE INSERT ON subrole_assignments
  FOR EACH ROW EXECUTE FUNCTION assert_grant_ceiling();

-- INV-38: minimo dos ADMIN_SUPER activos. Protege del bloqueo total.
CREATE OR REPLACE FUNCTION assert_min_super_admins() RETURNS TRIGGER AS $$
DECLARE n INTEGER;
BEGIN
  IF OLD.subrole = 'ADMIN_SUPER' AND OLD.revoked_at IS NULL
     AND NEW.revoked_at IS NOT NULL THEN
    SELECT count(*) INTO n FROM subrole_assignments
     WHERE subrole = 'ADMIN_SUPER' AND revoked_at IS NULL AND id <> OLD.id;
    IF n < 1 THEN
      RAISE EXCEPTION 'ERR_RBAC_LAST_SUPER_ADMIN: deben quedar al menos dos titulares activos';
    END IF;
  END IF;
  RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_min_super_admins
  BEFORE UPDATE ON subrole_assignments
  FOR EACH ROW EXECUTE FUNCTION assert_min_super_admins();


INSERT INTO subrole_grant_matrix (granter_subrole, grantable_subrole, requires_second_signature)
SELECT 'ADMIN_SUPER', r, r IN ('ADMIN_FINANCE','ADMIN_COMPLIANCE','ADMIN_LEGAL_COMPLIANCE')
  FROM unnest(ARRAY['USER_VERIFIED','SUPPORT_L1','SUPPORT_L2','SUPPORT_VALUATOR',
                    'SUPPORT_SUPERVISOR','SUPPORT_BEHAVIORAL_ANALYST','ADMIN_MODERATION',
                    'ADMIN_RISK','ADMIN_FINANCE','ADMIN_LEGAL_COMPLIANCE','ADMIN_COMPLIANCE',
                    'ADMIN_BEHAVIORAL','ADMIN_SUPER']) AS r;
-- Unica delegacion: el rol de mayor rotacion y menor privilegio.
INSERT INTO subrole_grant_matrix VALUES ('SUPPORT_SUPERVISOR','SUPPORT_L1',false);


CREATE TABLE fsm_transitions (
  entity_type       VARCHAR(40) NOT NULL,
  from_state        VARCHAR(40) NOT NULL,
  to_state          VARCHAR(40) NOT NULL,
  trigger_code      VARCHAR(60) NOT NULL,
  actor_kind        VARCHAR(20) NOT NULL
                    CHECK (actor_kind IN ('SYSTEM','CLIENT','SUPPORT','ADMIN')),
  required_subroles VARCHAR(40)[],
  requires_reason   BOOLEAN NOT NULL DEFAULT false,
  requires_second_signature BOOLEAN NOT NULL DEFAULT false,
  guard_expression  JSONB,
  PRIMARY KEY (entity_type, from_state, to_state, trigger_code)
);


INSERT INTO raffle_type_rules
  (raffle_type, name, trigger_kind, requires_end_at, requires_threshold,
   multi_winner, presentation_mode, capabilities) VALUES
('T1','Sold-out',            'SOLD_OUT',  false, false, false, false,
   '{"expiry_policy_required":true}'),
('T2','Umbral mínimo',       'THRESHOLD', true,  true,  false, false,
   '{"auto_cancel_on_miss":true,"early_close_on_threshold":false}'),
('T3','Por tiempo',          'TIME',      true,  false, false, false,
   '{"cancel_if_empty":true}'),
('T4','Progresivo por hitos','MILESTONE', false, false, false, false,
   '{"milestones_required":true,"milestones_immutable_after_publish":true}'),
('T5','Flash',               'FLASH',     true,  false, false, false,
   '{"max_duration_from_market_config":true,"oversell_metric":true,
     "reinforced_reservation":true}'),
('T6','Multi-ganador',       'SOLD_OUT',  false, false, true,  false,
   '{"without_replacement":true,"prizes_by_position":true}'),
('T7','Recurrente',          'RECURRING', true,  false, false, false,
   '{"independent_edition":true,"own_pool_and_proof":true}'),
('T8','Live',                'SOLD_OUT',  false, false, false, true,
   '{"inherits_from_base_type":true,"visual_only":true}');
