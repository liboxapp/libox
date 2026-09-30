-- C1 · overlay BORRADOR: arranque de particiones.
-- Mes actual y dos siguientes en UTC, más DEFAULT, para los 11 padres con
-- provisioning = overlay. journal_lines no se toca (aporte humano).
-- Horizonte 2: el mes M existe al menos 30 días antes de empezar (L3 V7 §1.3).
-- Idempotente.
SELECT parent_table, partition_name, action
  FROM libox_ops.ensure_monthly_partitions(now(), 2)
 ORDER BY parent_table, partition_name;
