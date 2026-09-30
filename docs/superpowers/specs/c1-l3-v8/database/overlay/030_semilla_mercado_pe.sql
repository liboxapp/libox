-- C1 · overlay BORRADOR: semilla no patrimonial.
-- markets PE. Valores literales de L3 V7 §10.1 (market_code, currency.code,
-- timezone, locale). name es la traducción visible del código PE (no es dato
-- contable ni normativo; no requiere confirmación). status toma el DEFAULT de V7.
-- No siembra market_config_versions, comisiones, impuestos, FSM, ledger,
-- incompatibilidades ni administradores.

INSERT INTO public.markets (code, name, currency, timezone, locale)
VALUES ('PE', 'Perú', 'PEN', 'America/Lima', 'es-PE')
ON CONFLICT (code) DO NOTHING;

DO $seed$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM public.markets
                  WHERE code = 'PE' AND currency = 'PEN'
                    AND timezone = 'America/Lima' AND locale = 'es-PE') THEN
    RAISE EXCEPTION 'LIBOX_SEED_DRIFT: markets PE existe con valores distintos de L3 V7 §10.1; no se sobrescribe';
  END IF;
END
$seed$;
