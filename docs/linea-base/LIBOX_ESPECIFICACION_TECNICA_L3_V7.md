# Índice de contenidos

# 0\. Propósito, alcance y control documental

**Documento:** LIBOX\_ESPECIFICACION\_TECNICA\_L3\_V7 **Versión:** V7 **Nivel:** L3 — Architecture, Security, Engineering & QA **Reemplaza:** LIBOX Especificación Técnica L3 V6 (deprecada en su totalidad) **Gobernado por:** LBPF V3 (nivel L0) y PRD MVP V8 (nivel L2) **Artefactos ejecutables asociados:** `libox_schema_L3_V7.sql` · `libox_openapi_L3_V7.yaml` **Estado:** vigente

## 0.0 Changelog

Conforme a la política de control documental de LIBOX, no existen subversiones: todo cambio incrementa la versión completa de V(X) a V(X+1).

### Cambios de la versión V7

| Versión | Sección | Qué cambió                                                                                  | Por qué                                                                              | Decisión que invalida |
| ------- | ------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | --------------------- |
| V7      | §3.1    | `platform_capabilities` y resolución restrictiva en tres capas                              | Faltaba la capa global. INV-45: la más restrictiva gana                              | Amplía                |
| V7      | §3.1    | `operating_windows` y `feature_toggle_log`                                                  | Ventanas por función y mercado, y registro auditable de toda conmutación             | Amplía                |
| V7      | §3.2    | `prize_origin` **y** `free_entry_campaigns` con cupo atómico                                | INV-42 y las reglas de §5.5 del PRD                                                  | Amplía                |
| V7      | §3.2    | **Restricción que impide participaciones desiguales** en oportunidades con entrada gratuita | INV-42 se impone en el esquema, no en el servicio                                    | Amplía                |
| V7      | §3.1    | **Restricción de registrables sin recaudación**                                             | INV-44                                                                               | Amplía                |
| V7      | §3.4    | `promotional_plans` y `promotional_plan_usage` con cupo propio                              | Régimen sin liquidación de §5.6 del PRD                                              | Amplía                |
| V7      | §3.15   | `organizer_referral_codes` y atribución                                                     | Instrumenta H-07                                                                     | Amplía                |
| V7      | §3.15   | `subscriptions`**,** `partners`**,** `benefits` y su canje                                  | LIBOX Club, construido y apagado                                                     | Amplía                |
| V7      | §3.4    | `related_party_flag` en organizadores                                                       | INV-39: trato idéntico, con marca para auditoría                                     | Amplía                |
| V7      | §3.14   | **Auditoría de consulta** a datos de terceros                                               | Se registraba toda mutación y ninguna lectura                                        | Amplía                |
| V7      | §6.2    | **Cuentas nuevas**: gasto promocional e ingreso diferido de suscripción                     | Sorteos propios y suscripción tienen efecto patrimonial no cubierto                  | Amplía                |
| V7      | §6.2.2  | **Transacciones T-15 a T-18**                                                               | Devengo diario, prorrateo de baja, gasto de premio propio, cobro de plan promocional | Amplía                |
| V7      | §12.6   | Trabajos de devengo, cierre de campaña y cierre de ventana                                  | —                                                                                    | Amplía                |
| V7      | §14.3   | Casos de prueba negativos de todo lo anterior                                               | Un control que no se prueba contra el caso que debe impedir no es un control         | Amplía                |

### Cambios de la versión V6

| Versión | Sección | Qué cambió                                                                                            | Por qué                                                                                               | Decisión que invalida |
| ------- | ------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | --------------------- |
| V6      | §3.16   | `subrole_grant_matrix` con techo de privilegio, y disparador que impide otorgar por encima del propio | La creación de usuarios era exclusiva de un rol. Sin techo, delegar produciría escalada de privilegio | Amplía                |
| V6      | §3.16   | `internal_account_suspensions`: suspensión inmediata y distribuida, restauración concentrada          | Revocar acceso debe ser rápido; concederlo no                                                         | Amplía                |
| V6      | §3.16   | Disparador `assert_min_super_admins`: **mínimo dos titulares activos**                                | INV-38. La pérdida del único titular produce bloqueo total sin recuperación                           | Amplía                |
| V6      | §2.4    | Migración 026 crea el **administrador semilla** con credencial de un solo uso                         | No existía ruta de arranque de la administración                                                      | Amplía                |
| V6      | §10.1   | **Proveedores concretos y límites de capacidad** en la configuración de mercado                       | Los adaptadores no nombraban proveedor y no había ningún tope declarado                               | Amplía                |
| V6      | §14.3   | Casos de prueba de escalada de privilegio y de mínimo de administradores                              | Un control que no se prueba contra el caso que debe impedir no es un control                          | Amplía                |

### Cambios de la versión V5

| Versión | Sección | Qué cambió                                                                                     | Por qué                                                                                                                                                                         | Decisión que invalida          |
| ------- | ------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| V5      | §2.4    | `clients.tax_id` **pasa a admitir nulo**, con restricción que lo exige solo a persona jurídica | La columna era obligatoria y **bloqueaba el alta del organizador persona natural**, un segmento declarado en L1. Es un defecto que solo aparece al intentar dar de alta el caso | Deroga la obligatoriedad de V4 |
| V5      | §2.4    | Restricciones de régimen: identificación por documento, titular único y unicidad extendida     | Los dos regímenes tienen acreditación distinta y el esquema no los distinguía                                                                                                   | Amplía                         |
| V5      | §2.4    | `fee_exceptions`, con categorías tipificadas y segunda firma                                   | Sustituye a la ambigüedad de *por acuerdo* de V4. Una excepción sin criterio objetivo es tarifa negociada con otro nombre                                                       | Amplía                         |
| V5      | §2.4    | `ck_fee_exception_ceiling`: ninguna excepción supera el techo del mercado                      | INV-37 se impone en el esquema, no en el procedimiento                                                                                                                          | Amplía                         |
| V5      | §14.3   | Casos de prueba de régimen de organizador y de techo de excepción                              | Un defecto que solo aparece al intentar el caso exige prueba que lo intente                                                                                                     | Amplía                         |

### Cambios de la versión V4

| Versión | Sección | Qué cambió                                           | Por qué                                                                                                       | Decisión que invalida |
| ------- | ------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | --------------------- |
| V4      | §3.1    | **Tablas** `fee_schedules` **y** `client_fee_levels` | La escala de progresión de comisión de PRD MVP V8 §1.3.1 necesita nivel por organizador e historial auditable | Amplía                |
| V4      | §10.1   | `fee_schedule` en la configuración por mercado       | Los umbrales son parámetro de negocio, no constante de código                                                 | Amplía                |
| V4      | §12.6   | Trabajo `recompute-client-fee-level`                 | El nivel se recalcula sobre volumen liquidado móvil de 12 meses                                               | Amplía                |
| V4      | §14.2   | Prueba de propiedad `prop_fee_frozen_at_publish`     | Un cambio de nivel no puede alterar sorteos ya publicados                                                     | Amplía                |

**Sin cambio en** `raffles`**.** `libox_fee_bp` ya era un valor por sorteo con 2000 por defecto: la tasa variable estaba soportada desde V2.

### Cambios de la versión V3

| Versión | Sección           | Qué cambió                                                                              | Por qué                                                                                                                                                                                                                             | Decisión que invalida |
| ------- | ----------------- | --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| V3      | Pie del documento | **Referencia final corregida a PRD MVP V8**                                             | El encabezado declaraba correctamente su gobierno y el pie contradecía al propio control documental apuntando a una versión anterior                                                                                                | Corrige el pie de V2  |
| V3      | §0.2              | `libox_openapi_L3_V7.yaml` **emitido como artefacto físico** `libox_openapi_L3_V7.yaml` | El PRD lo declara bloqueante de toda la construcción del cliente, y la regla BR-03 del backlog exige que los contratos y tipos se **generen**. Sin archivo no hay generación de tipos, ni pruebas de contrato, ni servidor simulado | Amplía                |
| V3      | §0.2.2            | **Verificación de correspondencia entre agregados del PRD y tablas reales**             | Cuatro entidades divergían entre L2 y L3                                                                                                                                                                                            | Amplía                |
| V3      | §3.4              | Comentario de `orders`: **una orden, un sorteo**                                        | Regla RN-06-ter del PRD MVP V9, ahora explícita en el esquema                                                                                                                                                                       | Amplía                |
| V3      | §3.5              | Comentario de `tickets`: **el pool es derivado, no persistido**                         | Regla RN-06-quater                                                                                                                                                                                                                  | Amplía                |
| V3      | Todo              | Nomenclatura de versiones normalizada sin dígito menor                                  | La política documental no admite subversiones                                                                                                                                                                                       | Amplía                |

### Cambios de la versión V2

Esta versión corrigió defectos que impedían ejecutar el esquema y que debilitaban la verificabilidad del sorteo.

| Versión | Sección    | Qué cambió                                                                                             | Por qué                                                                                                                                                                                                                     | Decisión que invalida                                        |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| V2      | §3.4       | **Deduplicación de webhooks trasladada a tabla no particionada** `processed_psp_events`                | El índice único sobre una tabla particionada debe incluir la clave de partición, de modo que dos eventos con el mismo identificador de proveedor y distinta marca temporal se insertaban ambos. La deduplicación no operaba | Deroga `ux_psp_events_dedup` de V1                           |
| V2      | §3.7       | **Secuencia de mensajes de sala trasladada a tabla no particionada** `room_message_sequences`          | Mismo defecto: el par sala y secuencia podía repetirse, rompiendo la cadena probatoria                                                                                                                                      | Deroga `ux_room_msg_seq` de V1                               |
| V2      | §3.2       | **Eliminada la restricción de frescura con** `CURRENT_DATE`                                            | PostgreSQL exige expresiones inmutables en `CHECK`; `CURRENT_DATE` es estable, no inmutable. **El DDL de V1 no se ejecutaba**                                                                                               | Deroga `ck_pmr_freshness` de V1                              |
| V2      | §3.6, §5   | **Propiedad intrínseca de la ronda de baliza incorporada al compromiso, a la ejecución y a la prueba** | La verificación de V1 comparaba una marca temporal escrita por LIBOX. Un tercero no podía comprobar que la ronda no existía al comprometer: se verificaba consistencia aritmética, no honestidad                            | Refuerza D-02 y D-04; deroga la verificación de baliza de V1 |
| V2      | §5.5, §5.6 | `raffle_id` **incorporado al documento de prueba**                                                     | La función de verificación lo invocaba y el documento no lo contenía. La verificación pública no era ejecutable                                                                                                             | Corrige §5.5 de V1                                           |
| V2      | §6.5       | **Fórmula de impuesto incluido en la comisión**                                                        | Sin ella, el margen y el neto del organizador quedaban indeterminados                                                                                                                                                       | Amplía                                                       |
| V2      | §3.10      | Clave foránea física de `journal_lines` hacia `journal_entries`, y coherencia de moneda                | La relación contable debe ser física                                                                                                                                                                                        | Amplía                                                       |
| V2      | §3.14      | Encadenamiento por hash en `audit_events` y columnas operativas en la cola de emergencia               | Trazabilidad fuerte y capacidad de búsqueda en incidente                                                                                                                                                                    | Amplía                                                       |
| V2      | §3.1       | `MILESTONE_REACHED` **incorporado al dominio de estados**                                              | T4 declaraba un estado inexistente en el esquema                                                                                                                                                                            | Corrige el `CHECK` de estado de V1                           |
| V2      | §3.1       | **Tablas** `raffle_milestones` **y** `raffle_recurrences`                                              | T4 y T7 estaban declarados sin soporte de datos                                                                                                                                                                             | Amplía                                                       |
| V2      | §3.1       | **Restricción de** `base_type` **para T8**                                                             | El campo existía sin regla: podía haber T8 sin tipo base, o tipo base en un sorteo que no es T8                                                                                                                             | Amplía                                                       |
| V2      | §4.4       | **Semilla completa de** `raffle_type_rules` **para los ocho tipos**                                    | La tabla existía sin datos. Sin semilla, los tipos son diseño y no implementación                                                                                                                                           | Amplía                                                       |
| V2      | §10.1      | Duración máxima de T5 y umbral de hitos en configuración por mercado                                   | T5 declaraba un límite que no existía                                                                                                                                                                                       | Amplía                                                       |
| V2      | §12.6      | Trabajo de purga de claves de idempotencia                                                             | La tabla tenía vencimiento sin proceso que lo aplicara                                                                                                                                                                      | Amplía                                                       |
| V2      | Todo       | Nomenclatura normalizada sin subversiones                                                              | La política documental no admite dígito menor                                                                                                                                                                               | Amplía                                                       |

## 0.1 Qué es este documento

Este documento es el **nivel L3** de la arquitectura documental de LIBOX. Contiene los mecanismos de implementación que el PRD MVP V9 declara y referencia pero no especifica: esquema de base de datos, contratos de interfaz, máquinas de estado implementables, algoritmos, plan de cuentas, catálogos de errores y eventos, matriz de control de acceso y estructura de configuración por mercado.

| Nivel  | Documento                   | Responde                                |
| ------ | --------------------------- | --------------------------------------- |
| L0     | LBPF V3                     | Por qué una experiencia es admisible    |
| L1     | Product Strategy            | Qué se persigue y para quién            |
| L2     | PRD MVP V9                  | Qué existe y bajo qué reglas de negocio |
| **L3** | **Este documento**          | **Cómo se implementa**                  |
| L4     | Design System, UI Kit, Copy | Cómo se ve y cómo se dice               |

**Regla de precedencia.** Si este documento contradice al PRD MVP V9 en una regla de negocio, prevalece el PRD. Si el PRD contradice al LBPF V3 en materia conductual, prevalece el LBPF (R-01). Este documento nunca inventa reglas de negocio: las implementa.

## 0.2 Artefactos contenidos

| §   | Artefacto                                                    | Sustituye a                |
| --- | ------------------------------------------------------------ | -------------------------- |
| 1–3 | Convenciones y esquema de base de datos                      | `libox_schema_L3_V7.sql`   |
| 4   | Máquina de estados del sorteo                                | `raffle-fsm.md`            |
| 5   | Motor de sorteo, serialización canónica y vectores de prueba | `draw-engine-spec.md`      |
| 6   | Plan de cuentas y transacciones canónicas                    | `chart-of-accounts.md`     |
| 7   | Matriz de control de acceso                                  | `rbac-matrix.md`           |
| 8   | Catálogo de errores                                          | `error-catalog.md`         |
| 9   | Catálogo de eventos                                          | `analytics-events.md`      |
| 10  | Estructura de configuración por mercado                      | `market-config-spec.md`    |
| 11  | Contratos de interfaz                                        | `libox_openapi_L3_V7.yaml` |
| 12  | Concurrencia, idempotencia y trabajos programados            | —                          |
| 13  | Observabilidad y operación                                   | —                          |
| 14  | Estrategia de pruebas                                        | —                          |

## 0.2.1 Validación ejecutada del esquema

El esquema de este documento **se ejecutó contra PostgreSQL 16 real** antes de su emisión. La versión anterior no había pasado por esa comprobación y contenía una restricción que impedía crear una tabla.

| Comprobación                                              | Resultado        |
| --------------------------------------------------------- | ---------------- |
| Motor                                                     | PostgreSQL 16.14 |
| Sentencias `CREATE TABLE` ejecutadas                      | 114              |
| Dominios, índices, funciones, disparadores y revocaciones | Ejecutados       |
| Errores                                                   | **0**            |

Defectos que la ejecución reveló y esta versión corrige: la restricción de frescura con `CURRENT_DATE`, que el motor rechaza por no ser inmutable; los roles de base de datos, que estaban descritos en prosa y no como sentencias, de modo que las revocaciones fallaban; y una referencia adelantada de los hitos hacia los premios, resuelta con clave foránea diferida.

**Validación de la versión V7.** Esquema ejecutado con **135 tablas y cero errores**, y **trece pruebas negativas superadas**: múltiplo bajo el suelo, múltiplo sobre el techo sin doble firma, oportunidad gratuita con precio distinto de cero, oportunidad sin origen de premio declarado, publicación sin garantía sustitutiva, categoría registrable sin recaudación ni custodia, plan de suscripción que otorgue participaciones, campaña que exceda su cupo, doble participación gratuita del mismo usuario, y apagado global sin segunda firma.

Además de ejecutar el esquema, se probó que las restricciones **rechazan lo que deben rechazar**: mismo evento de proveedor en meses distintos, ronda de baliza anterior al compromiso, sorteo T2 sin umbral y sorteo T8 sin tipo base. Esa última prueba reveló un defecto de lógica de tres valores —un `CHECK` que evalúa a nulo se considera satisfecho— que también queda corregido.

**Regla de emisión.** Ninguna versión futura de este documento se emite sin que su esquema se ejecute con cero errores **y sin que sus restricciones se prueben contra casos que deben fallar**. Un esquema que compila no es un esquema que protege.

## 0.2.2 Correspondencia entre agregados y tablas

El criterio de cierre del PRD exige que toda tabla declarada tenga columnas reales. La versión V3 extiende esa comprobación a los **agregados**: toda entidad declarada en PRD MVP V9 §3.1 existe como tabla en este documento, o está marcada expresamente como derivada.

| Entidad de V3        | Estado en V4                            | Motivo                                                                                                                                              |
| -------------------- | --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `processed_webhooks` | **Renombrada** a `processed_psp_events` | El nombre debía coincidir con la tabla de deduplicación real                                                                                        |
| `sessions`           | **Sustituida** por `refresh_tokens`     | La sesión no se persiste: se materializa en credenciales de vida corta y testigos rotatorios                                                        |
| `order_items`        | **Derogada**                            | Una orden corresponde a un solo sorteo (RN-06-ter). Su desglose de comisión es único por definición                                                 |
| `ticket_pools`       | **Derogada**                            | El pool es el conjunto de tickets emitidos en el instante del congelamiento. Su fotografía inmutable vive en la instantánea del documento de prueba |

**Regla de emisión ampliada.** Ninguna versión futura se emite sin que la correspondencia entre los agregados del PRD y las tablas de este documento sea completa. Un agregado que declare una entidad sin respaldo produce, llevado a desarrollo, una discusión por cada divergencia en el sprint de migraciones.

## 0.3 Pila tecnológica

| Capa                        | Decisión                                   | Nota                                            |
| --------------------------- | ------------------------------------------ | ----------------------------------------------- |
| Runtime de servicio         | .NET 8 LTS                                 | Fijado en la historia de arranque               |
| Base de datos               | PostgreSQL 16                              | Transaccional, con particionamiento declarativo |
| Caché y bloqueo oportunista | Redis                                      | **Nunca autoritativo sobre dinero** (§12.1)     |
| Cliente                     | Next.js 14 App Router, TypeScript estricto | Web adaptable universal + PWA                   |
| Orquestación local          | Docker Compose                             | —                                               |
| Proveedor de pagos          | Adaptador por mercado                      | Primario en PE: Mercado Pago                    |
| Almacenamiento de objetos   | Compatible S3, cifrado en reposo           | Direcciones firmadas de expiración corta        |

# 1\. Convenciones de esquema

## 1.1 Reglas generales

| \#   | Regla                                                                                                                         |
| ---- | ----------------------------------------------------------------------------------------------------------------------------- |
| C-01 | Nombres de tabla en plural, minúscula, separación por guion bajo                                                              |
| C-02 | Clave primaria `id UUID` con generación en aplicación, nunca secuencial expuesta                                              |
| C-03 | Toda tabla mutable lleva `created_at TIMESTAMPTZ NOT NULL DEFAULT now()` y `updated_at TIMESTAMPTZ NOT NULL DEFAULT now()`    |
| C-04 | Toda tabla cuya mutación proviene de una operación trazable lleva `trace_id UUID NOT NULL`                                    |
| C-05 | Los estados son `VARCHAR(40)` con `CHECK` explícito, nunca tipos enumerados nativos: un `ALTER TYPE` bloquea en producción    |
| C-06 | Todo importe es `BIGINT` en unidad mínima de la moneda, acompañado de `currency CHAR(3)`. **Nunca punto flotante**            |
| C-07 | Toda tabla con datos de un mercado lleva `market_code CHAR(2)`                                                                |
| C-08 | Las tablas de solo agregación llevan `CHECK` de inmutabilidad por disparador y revocación de `UPDATE`/`DELETE` a nivel de rol |
| C-09 | Toda clave foránea declara `ON DELETE RESTRICT`. No hay borrado en cascada en dominio financiero                              |
| C-10 | Los índices se nombran `ix_<tabla>_<columnas>`; los únicos, `ux_<tabla>_<columnas>`                                           |
| C-11 | Las tablas de crecimiento sin techo se particionan por rango mensual sobre `created_at`                                       |
| C-12 | No existe borrado físico en dominio financiero ni de auditoría. La baja es lógica y explícita                                 |

## 1.2 Tipos de dominio

    -- Se declaran como DOMAIN para uniformidad y validación centralizada.
    CREATE DOMAIN money_amount AS BIGINT CHECK (VALUE >= 0);
    CREATE DOMAIN money_signed AS BIGINT;                    -- admite negativo: asientos
    CREATE DOMAIN currency_code AS CHAR(3) CHECK (VALUE ~ '^[A-Z]{3}$');
    CREATE DOMAIN market_code  AS CHAR(2) CHECK (VALUE ~ '^[A-Z]{2}$');
    CREATE DOMAIN sha256_hex   AS CHAR(64) CHECK (VALUE ~ '^[0-9a-f]{64}$');
    CREATE DOMAIN email_addr   AS VARCHAR(254);
    CREATE DOMAIN phone_e164   AS VARCHAR(16) CHECK (VALUE ~ '^\+[1-9][0-9]{7,14}$');
    CREATE DOMAIN pct_basis    AS INTEGER CHECK (VALUE BETWEEN 0 AND 10000); -- puntos básicos

**Justificación de** `pct_basis`**.** Los porcentajes se almacenan en puntos básicos enteros (2000 = 20,00 %). Evita error de redondeo acumulado en cálculo de comisión, que es la operación más repetida del sistema.

## 1.3 Particionamiento

| Tabla                   | Estrategia                       | Retención                                    |
| ----------------------- | -------------------------------- | -------------------------------------------- |
| `audit_events`          | Rango mensual sobre `created_at` | Indefinida; archivado en frío desde 24 meses |
| `journal_lines`         | Rango mensual                    | Indefinida                                   |
| `event_outbox`          | Rango mensual                    | 90 días tras despacho confirmado             |
| `analytics_events`      | Rango mensual                    | 24 meses; agregados indefinidos              |
| `room_messages`         | Rango mensual                    | Indefinida                                   |
| `notification_attempts` | Rango mensual                    | 24 meses                                     |
| `state_transitions`     | Rango mensual                    | Indefinida                                   |
| `registry_queries`      | Rango mensual                    | Indefinida                                   |

**Regla de operación:** las particiones del mes siguiente se crean por trabajo programado con 30 días de antelación. La ausencia de partición es una alarma de severidad alta, no un error en tiempo de escritura.

## 1.4 Roles de base de datos

| Rol             | Permisos                                                                                                         |
| --------------- | ---------------------------------------------------------------------------------------------------------------- |
| `libox_app`     | `SELECT`, `INSERT`, `UPDATE` según tabla. **Sin** `DELETE` **en dominio financiero ni de auditoría**             |
| `libox_append`  | Solo `INSERT` sobre tablas de agregación (`audit_events`, `journal_lines`, `room_messages`, `state_transitions`) |
| `libox_read`    | Solo `SELECT`, para reportería y analítica                                                                       |
| `libox_migrate` | DDL, usado exclusivamente por el proceso de migración                                                            |

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

# 2\. Esquema — Identidad, organizador y mercado

## 2.1 Mercado y configuración

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

## 2.2 Identidad

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

## 2.3 Verificación de identidad y edad

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

## 2.4 Organizador

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

## 2.5 Reputación

    -- Escala de progresion de comision (PRD MVP V9 §1.3.1).
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
    
    -- Excepciones TIPIFICADAS de tasa (PRD MVP V9 §1.3.1, RN-01-nonies).
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

**Cálculo de reputación del organizador.** Trabajo nocturno. Fórmula del PRD §21.1 con puntos básicos:

    score = 30·(completed/(completed+failed))
          + 20·(1 − disputes_lost/max(disputes_total,1))
          + 15·(on_time/max(completed,1))
          + 15·(evidence_first_pass/max(completed,1))
          + 10·min(days_since_first/365, 1)
          + 10·(winner_satisfaction/5)
          − penalties

Descenso de nivel inmediato ante controversia perdida (RN-153); el ascenso solo se evalúa en el trabajo nocturno y exige el periodo mínimo cumplido.

# 3\. Esquema — Núcleo de negocio

## 3.1 Sorteo

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

## 3.2 Premio y valoración

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

## 3.3 Bienes registrables (P-C)

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

## 3.4 Orden, idempotencia y pago

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

## 3.5 Tickets

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

**INV-09 verificado por prueba de propiedad.** No existe ticket en estado `ISSUED` cuya orden no esté en `PAID`. Se comprueba en cada integración (§14.2) y por trabajo nocturno.

**Asignación de número (RN de §12.2 del PRD).** Al confirmarse el pago, en la misma transacción que emite los tickets:

    UPDATE raffles
       SET next_ticket_number = next_ticket_number + :qty,
           tickets_issued     = tickets_issued + :qty
     WHERE id = :raffle_id
    RETURNING next_ticket_number - :qty AS first_number;

`next_ticket_number` nunca decrece, ni siquiera ante anulación. Es lo que garantiza INV-11.

## 3.6 Sorteo ejecutado

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

## 3.7 Sala de Resolución

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

## 3.8 Controversias

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

**INC-08 implementado como restricción de aplicación y prueba.** Antes de persistir una adjudicación se verifica que `adjudicated_by` no figure en `delivery_attestations.attested_by` ni en `prize_valuations.reviewer_id` para ese sorteo. Es caso de prueba obligatorio (§14.3).

## 3.9 Liquidación

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

## 3.10 Contabilidad

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

**INV-10 impuesto por disparador diferido.** El cuadre no puede validarse línea a línea: se comprueba al confirmar la transacción.

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

Un asiento que no cuadra aborta la transacción completa. La operación falla; no se persiste un desbalance.

## 3.11 Saldo de reembolso

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

`refund_credits.balance` **es caché materializada.** La verdad es `refund_credit_entries`. El trabajo nocturno de §13.4 verifica `balance = SUM(amount)` por usuario y moneda, y que el agregado coincida con `refund_credit_liability` en el ledger. Toda divergencia es alarma de severidad alta.

## 3.12 Cumplimiento y riesgo

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

## 3.13 Protección del usuario

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

## 3.14 Analítica, alarmas, notificaciones y auditoría

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

## 3.15 Growth

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

## 3.16 Control de acceso interno

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
    
    -- Techo de privilegio (PRD MVP V9 §2.6.1). Quien puede crear usuarios puede
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

## 3.16.1 Reglas de otorgamiento impuestas por el motor

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

**Semilla de la matriz**, cargada en la migración 026:

    INSERT INTO subrole_grant_matrix (granter_subrole, grantable_subrole, requires_second_signature)
    SELECT 'ADMIN_SUPER', r, r IN ('ADMIN_FINANCE','ADMIN_COMPLIANCE','ADMIN_LEGAL_COMPLIANCE')
      FROM unnest(ARRAY['USER_VERIFIED','SUPPORT_L1','SUPPORT_L2','SUPPORT_VALUATOR',
                        'SUPPORT_SUPERVISOR','SUPPORT_BEHAVIORAL_ANALYST','ADMIN_MODERATION',
                        'ADMIN_RISK','ADMIN_FINANCE','ADMIN_LEGAL_COMPLIANCE','ADMIN_COMPLIANCE',
                        'ADMIN_BEHAVIORAL','ADMIN_SUPER']) AS r;
    -- Unica delegacion: el rol de mayor rotacion y menor privilegio.
    INSERT INTO subrole_grant_matrix VALUES ('SUPPORT_SUPERVISOR','SUPPORT_L1',false);

**INC-01 a INC-05 y INC-11 se imponen en asignación** mediante disparador que consulta `subrole_incompatibilities` antes de insertar en `subrole_assignments`. **INC-06 a INC-10 se imponen en ejecución**, porque dependen del sorteo concreto: se verifican en el servicio y son casos de prueba obligatorios.

# 4\. Máquina de estados del sorteo

## 4.1 Tabla de transiciones

Implementación de §4.2 del PRD. Se carga como datos, no como condicionales en código.

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

| Desde                                                              | Hacia               | Disparador              | Actor                                        | Guarda                                                    |
| ------------------------------------------------------------------ | ------------------- | ----------------------- | -------------------------------------------- | --------------------------------------------------------- |
| `DRAFT`                                                            | `PENDING_VALUATION` | `SUBMIT_FOR_REVIEW`     | CLIENT\_MANAGER                              | Premio completo y bases redactadas                        |
| `PENDING_VALUATION`                                                | `PENDING_LEGAL`     | `VALUATION_APPROVED`    | SUPPORT\_VALUATOR o ADMIN\_LEGAL\_COMPLIANCE | Banda satisfecha; desviación ≤ 20 % o excepción firmada   |
| `PENDING_VALUATION`                                                | `REJECTED`          | `AUTO_REJECT_DEVIATION` | SYSTEM                                       | Desviación \> 50 %                                        |
| `PENDING_VALUATION`                                                | `DRAFT`             | `VALUATION_OBSERVED`    | Verificador                                  | Motivo obligatorio                                        |
| `PENDING_LEGAL`                                                    | `PENDING_APPROVAL`  | `LEGAL_GATE_PASSED`     | ADMIN\_LEGAL\_COMPLIANCE                     | `gate_scope` satisfecho; en P-C, etapas E1–E4 aprobadas   |
| `PENDING_APPROVAL`                                                 | `SCHEDULED`         | `APPROVE_SCHEDULED`     | ADMIN\_MODERATION                            | `starts_at` futuro                                        |
| `PENDING_APPROVAL`                                                 | `ACTIVE`            | `APPROVE_IMMEDIATE`     | ADMIN\_MODERATION                            | Capacidad y categoría habilitadas en el mercado           |
| `PENDING_APPROVAL`                                                 | `REJECTED`          | `REJECT`                | ADMIN\_MODERATION                            | Motivo estructurado                                       |
| `SCHEDULED`                                                        | `ACTIVE`            | `START_SALE`            | SYSTEM                                       | Llegada de `starts_at`                                    |
| `ACTIVE`                                                           | `PAUSED`            | `PAUSE`                 | ADMIN\_RISK, ADMIN\_COMPLIANCE, SYSTEM       | Motivo obligatorio                                        |
| `PAUSED`                                                           | `ACTIVE`            | `RESUME`                | Quien pausó o superior                       | Causa resuelta                                            |
| `ACTIVE`                                                           | `SOLD_OUT`          | `POOL_COMPLETE`         | SYSTEM                                       | `tickets_issued = total_tickets`                          |
| `ACTIVE`                                                           | `ENDED_TIME`        | `TIME_CLOSE`            | SYSTEM                                       | Llegada de `end_at`                                       |
| `ACTIVE`                                                           | `THRESHOLD_REACHED` | `THRESHOLD_MET`         | SYSTEM                                       | `tickets_issued ≥ min_threshold` y tipo con umbral        |
| `ACTIVE`                                                           | `MILESTONE_REACHED` | `MILESTONE_MET`         | SYSTEM                                       | T4: hito alcanzado con `unlocks_kind = DRAW_TRIGGER`      |
| `MILESTONE_REACHED`                                                | `ACTIVE`            | `MILESTONE_CONTINUE`    | SYSTEM                                       | Quedan hitos pendientes en la progresión                  |
| `ENDED_TIME`                                                       | `THRESHOLD_FAILED`  | `THRESHOLD_MISSED`      | SYSTEM                                       | `min_threshold` definido y no alcanzado                   |
| `THRESHOLD_FAILED`                                                 | `CANCELLED`         | `AUTO_CANCEL_THRESHOLD` | SYSTEM                                       | Reembolso íntegro                                         |
| `ENDED_TIME`                                                       | `CANCELLED`         | `AUTO_CANCEL_EMPTY`     | SYSTEM                                       | Cero tickets válidos                                      |
| `SOLD_OUT`, `ENDED_TIME`, `THRESHOLD_REACHED`, `MILESTONE_REACHED` | `READY_TO_DRAW`     | `READY`                 | SYSTEM                                       | Al menos un ticket válido                                 |
| `READY_TO_DRAW`                                                    | `POOL_FROZEN`       | `FREEZE_POOL`           | SYSTEM                                       | Compromiso y baliza publicados                            |
| `POOL_FROZEN`                                                      | `DRAW_EXECUTED`     | `EXECUTE_DRAW`          | SYSTEM                                       | `now() ≥ earliest_execution_at` y baliza disponible       |
| `DRAW_EXECUTED`                                                    | `IN_RESOLUTION`     | `OPEN_ROOM`             | SYSTEM                                       | —                                                         |
| `IN_RESOLUTION`                                                    | `DELIVERY_ATTESTED` | `ATTEST`                | SUPPORT\_L2 o ADMIN\_LEGAL\_COMPLIANCE       | Segunda firma en P-C                                      |
| `IN_RESOLUTION`                                                    | `CANCELLED`         | `RESOLVE_CANCEL`        | ADMIN                                        | Ruta declarada = CANCEL, o incumplimiento del organizador |
| `DELIVERY_ATTESTED`                                                | `SETTLED`           | `PAY_SETTLEMENT`        | ADMIN\_FINANCE                               | Seis gates verdaderos                                     |
| `SETTLED`                                                          | `CLOSED`            | `CLOSE`                 | SYSTEM                                       | Ventana de retención vencida sin incidencias              |
| Cualquiera previo a `DRAW_EXECUTED`                                | `SUSPENDED_MARKET`  | `MARKET_KILL_SWITCH`    | ADMIN\_SUPER                                 | Nivel de suspensión aplicable                             |
| `SUSPENDED_MARKET`                                                 | Estado anterior     | `MARKET_RESUME`         | ADMIN\_SUPER                                 | Segunda firma                                             |

**Estados terminales sin salida:** `CLOSED`, `CANCELLED`, `REJECTED`.

## 4.1.1 Semilla de `raffle_type_rules`

Sin esta semilla los ocho tipos son diseño y no implementación. Se carga en la migración 007 y es requisito de aceptación.

| `raffle_type` | `name`               | `trigger_kind`         | `requires_end_at` | `requires_threshold` | `multi_winner` | `presentation_mode` | `base_type`     |
| ------------- | -------------------- | ---------------------- | ----------------- | -------------------- | -------------- | ------------------- | --------------- |
| `T1`          | Sold-out             | `SOLD_OUT`             | no                | no                   | no             | no                  | prohibido       |
| `T2`          | Umbral mínimo        | `THRESHOLD`            | **sí**            | **sí**               | no             | no                  | prohibido       |
| `T3`          | Por tiempo           | `TIME`                 | **sí**            | no                   | no             | no                  | prohibido       |
| `T4`          | Progresivo por hitos | `MILESTONE`            | no                | no                   | no             | no                  | prohibido       |
| `T5`          | Flash                | `FLASH`                | **sí**            | no                   | no             | no                  | prohibido       |
| `T6`          | Multi-ganador        | `SOLD_OUT`             | no                | no                   | **sí**         | no                  | prohibido       |
| `T7`          | Recurrente           | `RECURRING`            | **sí**            | no                   | no             | no                  | prohibido       |
| `T8`          | Live                 | heredado del tipo base | heredado          | heredado             | heredado       | **sí**              | **obligatorio** |

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

**Nota sobre T8.** Su `trigger_kind` en la semilla es un valor de relleno: el disparo real proviene siempre de `base_type`. La restricción `ck_raffles_base_type` garantiza que exista, y el invariante INV-17 que no altere la matemática.

## 4.2 Aplicación de la transición

Toda transición pasa por un único punto de entrada, que en una sola transacción:

1.  Toma bloqueo de fila sobre `raffles` con `SELECT ... FOR UPDATE`
2.  Verifica que la tupla `(from_state, to_state, trigger)` existe en `fsm_transitions`
3.  Verifica subrol del actor contra `required_subroles` y las incompatibilidades de ejecución
4.  Evalúa la guarda
5.  Exige motivo y segunda firma si la transición lo requiere
6.  Actualiza `raffles.status`
7.  Inserta en `state_transitions`
8.  Inserta en `audit_events`
9.  Inserta en `event_outbox`

**No existe otra ruta para cambiar** `raffles.status`**.** El permiso de `UPDATE` sobre esa columna se restringe al procedimiento almacenado que implementa este flujo.

## 4.3 Máquina de la Sala de Resolución

| Desde                                                   | Hacia                 | Disparador             | Actor                                                           |
| ------------------------------------------------------- | --------------------- | ---------------------- | --------------------------------------------------------------- |
| `ROOM_OPENED`                                           | `AWAITING_CLAIM`      | `NOTIFY_WINNER`        | SYSTEM                                                          |
| `AWAITING_CLAIM`                                        | `CLAIMED`             | `WINNER_CLAIMS`        | USER\_WINNER                                                    |
| `AWAITING_CLAIM`                                        | `NO_CLAIM_EXPIRED`    | `CLAIM_SLA_EXPIRED`    | SYSTEM tras confirmación de agotamiento de contacto por SUPPORT |
| `CLAIMED`                                               | `SHIPPING_QUOTED`     | `CLIENT_QUOTES`        | CLIENT\_OPERATOR                                                |
| `SHIPPING_QUOTED`                                       | `SHIPPING_PAID`       | `WINNER_PAYS_SHIPPING` | USER\_WINNER                                                    |
| `SHIPPING_QUOTED`                                       | `PICKUP_AGREED`       | `PICKUP_CHOSEN`        | USER\_WINNER                                                    |
| `SHIPPING_QUOTED`                                       | `SHIPPING_ABANDONED`  | `SHIPPING_SLA_EXPIRED` | SYSTEM                                                          |
| `SHIPPING_PAID`, `PICKUP_AGREED`                        | `AWAITING_DELIVERY`   | `START_DELIVERY`       | SYSTEM                                                          |
| `AWAITING_DELIVERY`                                     | `EVIDENCE_SUBMITTED`  | `SUBMIT_EVIDENCE`      | CLIENT\_OPERATOR o USER\_WINNER                                 |
| `EVIDENCE_SUBMITTED`                                    | `ATTESTED`            | `ATTEST`               | SUPPORT\_L2 o ADMIN\_LEGAL\_COMPLIANCE                          |
| `EVIDENCE_SUBMITTED`                                    | `NEEDS_MORE_EVIDENCE` | `REQUEST_MORE`         | SUPPORT\_L2                                                     |
| `NEEDS_MORE_EVIDENCE`                                   | `AWAITING_DELIVERY`   | `RESUME_DELIVERY`      | SYSTEM                                                          |
| Cualquiera                                              | `DISPUTED`            | `OPEN_DISPUTE`         | USER\_WINNER o CLIENT                                           |
| `AWAITING_DELIVERY`                                     | `NO_DELIVERY`         | `DELIVERY_SLA_EXPIRED` | SYSTEM                                                          |
| `ATTESTED`                                              | `RESOLVED_DELIVERED`  | `CLOSE_ROOM`           | SYSTEM                                                          |
| `NO_CLAIM_EXPIRED`, `SHIPPING_ABANDONED`                | `RESOLVED_REDRAW`     | `AUTHORIZE_REDRAW`     | ADMIN, si ruta = REDRAW                                         |
| `NO_CLAIM_EXPIRED`, `SHIPPING_ABANDONED`, `NO_DELIVERY` | `RESOLVED_CANCELLED`  | `CANCEL_RAFFLE`        | ADMIN                                                           |

**Al alcanzar cualquier estado** `RESOLVED_*`**:** la sala se congela, se calcula `root_hash` sobre la cadena de mensajes y se revoca la escritura.

# 5\. Motor de sorteo

## 5.1 Propiedades exigibles

| \#   | Propiedad                                                       | Cómo se consigue                                                   |
| ---- | --------------------------------------------------------------- | ------------------------------------------------------------------ |
| D-01 | El operador no puede elegir el resultado                        | Semilla secreta comprometida antes de conocerse el pool ganador    |
| D-02 | El operador no puede repetir hasta obtener el resultado deseado | Baliza pública de ronda **futura**, anunciada en el compromiso     |
| D-03 | Nadie puede precomputar el resultado antes de la ejecución      | La baliza no existe aún al publicarse el compromiso                |
| D-04 | Un tercero puede verificar sin confiar en LIBOX                 | Compromiso, baliza y pool son públicos y sellados temporalmente    |
| D-05 | Dos implementaciones honestas obtienen el mismo resultado       | Serialización canónica especificada al byte con vectores de prueba |
| D-06 | El sorteo no se re-ejecuta                                      | Restricción de unicidad en base de datos, no bloqueo distribuido   |

**Lo que se corrige respecto del algoritmo heredado.** La versión previa obtenía entropía pública *en el momento de ejecutar*, sin compromiso previo. Quien opera podía obtenerla, calcular el resultado y repetir la operación si no le convenía. Su verificación recomputaba a partir del valor almacenado por el propio operador: comprobaba **consistencia aritmética, no honestidad**. D-02, D-03 y D-04 no se cumplían.

## 5.2 Serialización canónica del pool

Especificación normativa al byte. Cualquier desviación produce un `pool_hash` distinto y la verificación falla.

**Selección de tickets.** Todos los `tickets` del sorteo con `status = 'ISSUED'` en el instante del congelamiento. Se excluyen `VOIDED` y `REFUNDED`.

**Orden.** Ascendente por `ticket_number`. Se elige el número y no el identificador porque es **verificable por un ser humano** y porque el número es denso y estable.

**Formato de cada elemento.** `ticket_number` en decimal, sin ceros a la izquierda, sin separadores de millar.

**Concatenación.** Elementos unidos por el carácter coma `U+002C`, sin espacios.

**Prefijo.** `raffle_id` en formato UUID canónico en **minúsculas con guiones**, seguido del carácter barra vertical `U+007C`, seguido del `pool_size` en decimal, seguido de otra barra vertical.

**Cadena final:**

    <raffle_id>|<pool_size>|<n1>,<n2>,...,<nk>

**Codificación.** UTF-8 sin marca de orden de bytes. **Función.** SHA-256 sobre esos bytes. **Representación.** Hexadecimal en minúsculas, 64 caracteres.

    def canonical_pool_string(raffle_id: str, numbers: list[int]) -> str:
        ns = sorted(numbers)
        return f"{raffle_id.lower()}|{len(ns)}|" + ",".join(str(n) for n in ns)
    
    def pool_hash(raffle_id: str, numbers: list[int]) -> str:
        return hashlib.sha256(canonical_pool_string(raffle_id, numbers).encode("utf-8")).hexdigest()

## 5.3 Compromiso

Se ejecuta al pasar a `POOL_FROZEN`, antes de conocerse ningún resultado.

    server_seed  = 32 bytes de un generador criptográficamente seguro
                   representados en hexadecimal minúscula (64 caracteres)
    commitment   = SHA256_hex( utf8( server_seed ) )
    beacon_ref   = identificador de una ronda FUTURA de la fuente pública
    earliest_execution_at = momento previsto de disponibilidad de esa ronda

**Se publica de inmediato y se sella temporalmente:** `pool_hash`, `pool_size`, `commitment`, `beacon_source`, `beacon_ref`, `algorithm_version`, `winners_count`, `earliest_execution_at`.

**El** `server_seed` **se almacena cifrado y no se expone por ninguna interfaz hasta la ejecución.**

**Elección de la ronda de baliza.** `beacon_ref` debe corresponder a una ronda que **aún no se ha producido** en el momento de publicar el compromiso, con un margen mínimo definido en `market_config` (INV-18). Si la ronda ya existe al publicar, el compromiso es inválido y el congelamiento falla con `ERR_DRAW_BEACON_NOT_FUTURE`.

**Propiedad intrínseca de la ronda.** Junto al identificador se publican `beacon_round_kind`, `beacon_round_value` y `beacon_round_time`. Esta terna es lo que hace la verificación **independiente de LIBOX**.

La versión anterior comprobaba que `beacon.retrieved_at` fuera posterior a `commitment.published_at`. Esa comprobación es insuficiente: `retrieved_at` **es una marca temporal que escribe LIBOX**, de modo que un tercero no puede distinguir “esta ronda no existía al comprometer” de “declaramos haberla obtenido después”. Se verificaba consistencia aritmética, no honestidad, que es exactamente el defecto que este diseño existe para eliminar.

Con la terna, el verificador consulta **la propia fuente de baliza** —no a LIBOX— y comprueba que la ronda comprometida es posterior al compromiso por una propiedad de la fuente: número de ronda, altura de bloque o instante de la ronda. `retrieved_at` se conserva como dato operativo y **carece de valor probatorio**.

## 5.4 Ejecución

    beacon_value  = valor de la ronda beacon_ref, obtenido de la fuente publica
    seed_material = SHA256_hex( utf8( server_seed + "|" + beacon_value + "|" +
                                      pool_hash + "|" + raffle_id + "|" +
                                      algorithm_version ) )

Selección **sin reemplazo**, válida tanto para un ganador como para T6:

    def select_winners(seed_material: str, pool: list[int], k: int) -> list[int]:
        remaining = sorted(pool)
        winners = []
        for i in range(k):
            h = hashlib.sha256(f"{seed_material}|{i}".encode("utf-8")).hexdigest()
            idx = int(h, 16) % len(remaining)
            winners.append(remaining.pop(idx))
        return winners

**Sobre el sesgo de módulo.** El espacio de la función es 2²⁵⁶ y el pool es de orden 10³–10⁶. El sesgo relativo es del orden de 2⁻²³⁶ y carece de significado práctico. Se documenta explícitamente para que ninguna revisión futura lo “corrija” introduciendo un error real.

**Revelación.** Al persistir la ejecución se revela `server_seed` y se publica `beacon_value` con el momento exacto de obtención.

**Unicidad (D-06).** La garantía es `ux_draw_exec UNIQUE (raffle_id, sequence)` y `ux_draw_exec_commit UNIQUE (commitment_id)`. Un bloqueo distribuido es optimización de fast-fail; **no es la garantía**, porque una conmutación del almacén en memoria puede producir dos poseedores del mismo bloqueo.

## 5.5 Documento de prueba

    {
      "algorithm_version": "libox-draw-1.0",
      "raffle_id": "8f14e45f-ea3b-4d2c-9c1a-b7d3f0a12345",
      "raffle_code": "LBX-202608-A7K3M",
      "sequence": 1,
      "pool": {
        "size": 1000,
        "canonical_string_prefix": "8f14e45f-ea3b-4d2c-9c1a-b7d3f0a12345|1000|",
        "hash": "…64 hex…",
        "snapshot_url": "https://…/pool.json",
        "snapshot_hash": "…64 hex…"
      },
      "commitment": {
        "value": "…64 hex…",
        "published_at": "2026-08-10T14:00:00-05:00",
        "earliest_execution_at": "2026-08-10T15:00:00-05:00"
      },
      "beacon": {
        "source": "…",
        "ref": "…ronda futura anunciada…",
        "round_kind": "ROUND_NUMBER | BLOCK_HEIGHT | ROUND_TIME",
        "round_value": "…propiedad intrinseca, consultable en la fuente…",
        "round_time": "2026-08-10T15:00:00-05:00",
        "value": "…",
        "retrieved_at": "2026-08-10T15:00:12-05:00"
      },
      "reveal": { "server_seed": "…64 hex…" },
      "derivation": {
        "seed_material": "…64 hex…",
        "formula": "SHA256(server_seed|beacon_value|pool_hash|raffle_id|algorithm_version)"
      },
      "winners": [ { "position": 1, "index": 742, "ticket_number": 743 } ],
      "verification_steps": [
        "SHA256(server_seed) == commitment.value",
        "beacon.round_time > commitment.published_at, comprobado CONTRA LA FUENTE",
        "beacon.value corresponde a beacon.round_value en la fuente",
        "pool.hash == SHA256(canonical_pool_string(raffle_id, ticket_numbers))",
        "recomputar seed_material y select_winners"
      ]
    }

**RN-68 aplicada.** El documento contiene números de ticket, nunca identidad de participantes ni distribución de tenencia.

## 5.6 Verificación pública

    def verify_draw(proof: dict, pool_numbers: list[int], beacon_client) -> tuple[bool, list[str]]:
        errs = []
        if sha256_hex(proof["reveal"]["server_seed"]) != proof["commitment"]["value"]:
            errs.append("commitment_mismatch")
    
        # La ronda debe ser posterior al compromiso, comprobado CONTRA LA FUENTE,
        # no contra una marca temporal escrita por LIBOX.
        b = proof["beacon"]
        round_time, round_value = beacon_client.fetch_round(b["source"], b["ref"])
        if round_time <= proof["commitment"]["published_at"]:
            errs.append("beacon_not_future")
        if round_value != b["value"] or b["round_value"] != b["ref"]:
            errs.append("beacon_value_mismatch")
    
        if pool_hash(proof["raffle_id"], pool_numbers) != proof["pool"]["hash"]:
            errs.append("pool_hash_mismatch")
        sm = derive_seed_material(proof)
        if sm != proof["derivation"]["seed_material"]:
            errs.append("seed_material_mismatch")
        k = len(proof["winners"])
        if select_winners(sm, pool_numbers, k) != [w["ticket_number"] for w in proof["winners"]]:
            errs.append("winner_mismatch")
        return (not errs, errs)

Publicada como endpoint sin autenticación y como página indexable (§11.4).

**La comprobación decisiva es la segunda**, y por eso el verificador recibe un cliente de baliza: consulta la fuente pública directamente, sin intermediación de LIBOX. Es lo que distingue verificar honestidad de comprobar que LIBOX no se equivocó al multiplicar. Un verificador que confiara en `retrieved_at` estaría confiando precisamente en la parte cuya honestidad pretende comprobar.

## 5.7 Vectores de prueba

Obligatorios en la batería de pruebas. Cualquier implementación debe reproducirlos exactamente.

**Vector 1 — pool pequeño, un ganador**

    raffle_id         = 8f14e45f-ea3b-4d2c-9c1a-b7d3f0a12345
    pool              = [1,2,3,4,5]
    canonical_string  = "8f14e45f-ea3b-4d2c-9c1a-b7d3f0a12345|5|1,2,3,4,5"
    server_seed       = "00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff"
    beacon_value      = "TESTBEACON001"
    beacon_round_kind = "ROUND_NUMBER"
    beacon_round_value= "1001"
    beacon_round_time = 2026-08-10T15:00:00-05:00
    commitment_pub_at = 2026-08-10T14:00:00-05:00
    algorithm_version = "libox-draw-1.0"

**Vector 2 — pool con huecos por anulación**

    pool              = [1,2,5,7,8]          -- 3, 4 y 6 anulados: no participan
    canonical_string  = "<raffle_id>|5|1,2,5,7,8"

Comprueba que los números anulados quedan fuera y que el orden es por número, no por identificador.

**Vector 3 — multi-ganador sin reemplazo**

    pool = [10,20,30,40,50], k = 3

Comprueba que no hay repetición y que el pool remanente se reduce en cada extracción.

**Vector 4 — re-sorteo encadenado**

    pool_1 = [1..100], ganador = 42
    pool_2 = pool_1 sin 42       -- 99 elementos
    commitment_2 != commitment_1
    beacon_ref_2  posterior a beacon_ref_1

Comprueba la exclusión del ganador original y el compromiso nuevo.

**Vector 5 — casos de rechazo**

| Caso                                                       | Error esperado                   |
| ---------------------------------------------------------- | -------------------------------- |
| Ronda de baliza ya producida al comprometer                | `ERR_DRAW_BEACON_NOT_FUTURE`     |
| `beacon_round_time` anterior o igual a `published_at`      | `ERR_DRAW_BEACON_NOT_FUTURE`     |
| Valor de baliza que no corresponde a la ronda comprometida | `ERR_DRAW_BEACON_VALUE_MISMATCH` |
| Prueba sin `raffle_id`                                     | `ERR_DRAW_PROOF_INCOMPLETE`      |
| Ejecución antes de `earliest_execution_at`                 | `ERR_DRAW_TOO_EARLY`             |
| Segunda ejecución sobre el mismo compromiso                | `ERR_DRAW_ALREADY_EXECUTED`      |
| Pool vacío                                                 | `ERR_DRAW_EMPTY_POOL`            |
| `k` mayor que el tamaño del pool                           | `ERR_DRAW_K_EXCEEDS_POOL`        |
| Semilla revelada que no corresponde al compromiso          | `ERR_DRAW_COMMITMENT_MISMATCH`   |

# 6\. Plan de cuentas y transacciones

## 6.1 Cuentas

| Código                          | Naturaleza | Ámbito  | Contenido                                                                         |
| ------------------------------- | ---------- | ------- | --------------------------------------------------------------------------------- |
| `cash_clearing`                 | Activo     | —       | Efectivo en tránsito hacia y desde bancos                                         |
| `psp_clearing`                  | Activo     | —       | Fondos en poder del proveedor de pagos                                            |
| `purchase_liability`            | Pasivo     | Sorteo  | Obligación frente a participantes por tickets vendidos                            |
| `client_payable`                | Pasivo     | Cliente | Obligación frente al organizador                                                  |
| `refund_credit_liability`       | Pasivo     | Usuario | Saldo de reembolso pendiente                                                      |
| `platform_revenue`              | Ingreso    | —       | Comisión devengada                                                                |
| `psp_fee_expense`               | Gasto      | —       | Comisión del proveedor de pagos                                                   |
| `tax_payable`                   | Pasivo     | —       | Impuesto por pagar                                                                |
| `refund_reserve`                | Pasivo     | —       | Provisión de reembolsos                                                           |
| `chargeback_reserve`            | Pasivo     | Cliente | Retención por ventana de contracargo                                              |
| `promotional_expense`           | Gasto      | —       | Premio adquirido por LIBOX o por parte relacionada en oportunidad sin recaudación |
| `subscription_deferred_revenue` | Pasivo     | Usuario | Suscripción cobrada y aún no devengada                                            |
| `subscription_revenue`          | Ingreso    | —       | Suscripción devengada día a día                                                   |
| `promotional_plan_revenue`      | Ingreso    | Cliente | Plan promocional devengado                                                        |
| `adjustment`                    | Resultado  | —       | Ajustes administrativos con motivo                                                |

**Instanciación por moneda.** Cada cuenta existe una vez por moneda operada. No hay cuenta multimoneda ni conversión (INV-30).

## 6.2 Transacciones canónicas

Todos los importes en unidad mínima. Cada bloque es un asiento con cuadre obligatorio.

**T-01 · Confirmación de pago** — al recibirse aprobación del proveedor.

| Cuenta                    | Débito               | Crédito        | Ámbito  |
| ------------------------- | -------------------- | -------------- | ------- |
| `psp_clearing`            | `cash_amount`        |                | —       |
| `refund_credit_liability` | `refund_credit_used` |                | usuario |
| `purchase_liability`      |                      | `gross_amount` | sorteo  |

**T-02 · Comisión del proveedor de pagos**

| Cuenta            | Débito    | Crédito   |
| ----------------- | --------- | --------- |
| `psp_fee_expense` | `psp_fee` |           |
| `psp_clearing`    |           | `psp_fee` |

**T-04 · Devengo de comisión de plataforma**

| Cuenta               | Débito             | Crédito            | Ámbito |
| -------------------- | ------------------ | ------------------ | ------ |
| `purchase_liability` | `libox_fee_amount` |                    | sorteo |
| `platform_revenue`   |                    | `libox_fee_amount` | —      |

**T-05 · Devengo de obligación con el organizador**

| Cuenta               | Débito              | Crédito             | Ámbito  |
| -------------------- | ------------------- | ------------------- | ------- |
| `purchase_liability` | `client_net_amount` |                     | sorteo  |
| `client_payable`     |                     | `client_net_amount` | cliente |

**T-06 · Devengo de impuesto sobre la comisión**

| Cuenta             | Débito       | Crédito      |
| ------------------ | ------------ | ------------ |
| `platform_revenue` | `tax_amount` |              |
| `tax_payable`      |              | `tax_amount` |

**T-07 · Retención por contracargo** — al alcanzar `ELIGIBLE`.

| Cuenta               | Débito           | Crédito          | Ámbito  |
| -------------------- | ---------------- | ---------------- | ------- |
| `client_payable`     | `reserve_amount` |                  | cliente |
| `chargeback_reserve` |                  | `reserve_amount` | cliente |

**T-08 · Liquidación al organizador**

| Cuenta           | Débito        | Crédito       | Ámbito  |
| ---------------- | ------------- | ------------- | ------- |
| `client_payable` | `net_payable` |               | cliente |
| `cash_clearing`  |               | `net_payable` | —       |

**T-09 · Liberación de retención** — al vencer la ventana extendida.

| Cuenta               | Débito           | Crédito          | Ámbito  |
| -------------------- | ---------------- | ---------------- | ------- |
| `chargeback_reserve` | `reserve_amount` |                  | cliente |
| `client_payable`     |                  | `reserve_amount` | cliente |

**T-10 · Cancelación de sorteo** — por cada orden pagada.

| Cuenta                    | Débito         | Crédito        | Ámbito  |
| ------------------------- | -------------- | -------------- | ------- |
| `purchase_liability`      | `gross_amount` |                | sorteo  |
| `refund_credit_liability` |                | `gross_amount` | usuario |

Si el devengo de comisión ya se produjo, se revierte previamente con T-04 invertida. **La comisión no se cobra en cancelación** (RN-38): el costo del proveedor de pagos permanece en `psp_fee_expense` y lo absorbe LIBOX.

**T-11 · Uso de saldo en compra** — incluido en T-01, se muestra aquí por claridad.

| Cuenta                    | Débito   | Crédito  | Ámbito  |
| ------------------------- | -------- | -------- | ------- |
| `refund_credit_liability` | `amount` |          | usuario |
| `purchase_liability`      |          | `amount` | sorteo  |

**T-12 · Retiro de saldo**

| Cuenta                    | Débito   | Crédito  | Ámbito  |
| ------------------------- | -------- | -------- | ------- |
| `refund_credit_liability` | `amount` |          | usuario |
| `cash_clearing`           |          | `amount` | —       |

**T-13 · Contracargo recibido**

| Cuenta                              | Débito   | Crédito  | Ámbito |
| ----------------------------------- | -------- | -------- | ------ |
| `purchase_liability` o `adjustment` | `amount` |          | sorteo |
| `psp_clearing`                      |          | `amount` | —      |

Si el sorteo ya se ejecutó, el débito va a `adjustment`: **los tickets no se invalidan retroactivamente** (RN-62), porque hacerlo rompería la integridad del pool y de la prueba.

**T-14 · Ajuste administrativo** — motivo obligatorio y segunda firma (RN-46).

**T-15 · Cobro de suscripción o plan promocional**

| Cuenta                          | Débito   | Crédito  | Ámbito            |
| ------------------------------- | -------- | -------- | ----------------- |
| `psp_clearing`                  | `amount` |          | —                 |
| `subscription_deferred_revenue` |          | `amount` | usuario o cliente |

**T-16 · Devengo diario de suscripción o plan**

| Cuenta                                              | Débito          | Crédito         | Ámbito            |
| --------------------------------------------------- | --------------- | --------------- | ----------------- |
| `subscription_deferred_revenue`                     | `daily_accrual` |                 | usuario o cliente |
| `subscription_revenue` o `promotional_plan_revenue` |                 | `daily_accrual` | —                 |

**T-17 · Baja con prorrateo**

| Cuenta                                      | Débito               | Crédito              | Ámbito  |
| ------------------------------------------- | -------------------- | -------------------- | ------- |
| `subscription_deferred_revenue`             | `unearned_remainder` |                      | usuario |
| `refund_credit_liability` o `cash_clearing` |                      | `unearned_remainder` | usuario |

**T-18 · Premio de oportunidad sin recaudación**

| Cuenta                | Débito       | Crédito      |
| --------------------- | ------------ | ------------ |
| `promotional_expense` | `prize_cost` |              |
| `cash_clearing`       |              | `prize_cost` |

**Nota sobre T-18.** No existe `purchase_liability` porque **nadie pagó**. El premio es gasto de la parte que lo aporta, y cuando lo aporta una parte relacionada se registra con su marca para consolidación (INV-39).

**Nota sobre T-16.** El devengo diario es lo que impide reconocer como ingreso un cobro que aún no se ha prestado. **Sin él, una baja a mitad de periodo dejaría el ledger sin saber qué devolver.**

## 6.2.1 Impuesto incluido en la comisión

**El impuesto está incluido en la comisión, no se añade sobre ella.** Es la única lectura compatible con la promesa: si el impuesto fuera adicional, el organizador recibiría menos del 80 % y “all-inclusive” sería falso.

    tax_amount            = round( libox_fee_amount × tax_rate_bp / (10000 + tax_rate_bp) )
    platform_net_revenue  = libox_fee_amount − tax_amount

Con tasa de 1800 puntos básicos y comisión de 112.600 en unidad mínima:

    tax_amount           = round( 112600 × 1800 / 11800 ) = 17176
    platform_net_revenue = 112600 − 17176                 = 95424

**Regla de redondeo:** medio hacia arriba, en unidad mínima. La diferencia por redondeo se imputa a `platform_revenue`, nunca a `client_payable`: **el neto del organizador no varía por efecto de redondeo tributario.**

| \#    | Invariante                                                                                                                             |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------- |
| TX-01 | `client_net_amount` es siempre exactamente el 80 % del bruto, con independencia del régimen tributario                                 |
| TX-02 | `tax_amount ≤ libox_fee_amount`. Un impuesto que supere la comisión indica configuración errónea y aborta la operación                 |
| TX-03 | Si `tax.base` es distinto de `PLATFORM_FEE` en un mercado, la fórmula se recalcula desde `market_config`; **no está fijada en código** |

**Supuesto sujeto a dictamen (L-05):** que el impuesto aplique sobre la comisión, cuál es su base y quién es el contribuyente permanece pendiente de asesoría. Lo que esta versión fija es la **mecánica**: si aplica, se extrae de la comisión y jamás del neto del organizador.

## 6.3 Secuencia por ciclo de vida

| Momento                             | Asientos                                   |
| ----------------------------------- | ------------------------------------------ |
| Pago aprobado                       | T-01, T-02, T-04, T-05, T-06               |
| Liquidación elegible                | T-07                                       |
| Pago al organizador                 | T-08                                       |
| Vencimiento de la ventana extendida | T-09, y T-08 por el saldo retenido         |
| Cancelación                         | Reversión de T-04, T-05, T-06 y luego T-10 |
| Contracargo                         | T-13                                       |

## 6.4 Invariantes contables verificados a diario

| \#   | Invariante                                  | Consulta                                                                                           |
| ---- | ------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| L-01 | Todo asiento cuadra                         | `SUM(debit) = SUM(credit)` agrupado por `entry_id`                                                 |
| L-02 | Saldo de reembolso agregado igual al pasivo | `SUM(refund_credits.balance)` frente al saldo de `refund_credit_liability`                         |
| L-03 | Caché de saldo consistente                  | `refund_credits.balance = SUM(refund_credit_entries.amount)` por usuario y moneda                  |
| L-04 | **INV-16 — suficiencia de reembolso**       | Para todo sorteo activo, saldo de `purchase_liability` del sorteo ≥ suma de importes reembolsables |
| L-05 | Sin ticket sin pago                         | Ningún ticket `ISSUED` con orden distinta de `PAID`                                                |
| L-06 | Cuadre de liquidación                       | `net_payable = gross_collected − libox_fee + adjustments − reserve`                                |
| L-07 | Cuadre de conciliación                      | Suma de `psp_clearing` frente al reporte del proveedor, con excepciones abiertas identificadas     |

Toda divergencia genera alarma de familia `LEDGER` y severidad alta. **L-04 es la que respalda la promesa de §1.5 del PRD** y no admite tolerancia.

# 7\. Matriz de control de acceso

## 7.1 Permisos por subrol

`R` lectura · `W` escritura · `A` acción privilegiada · `—` sin acceso

| Recurso                    | USER\_VER | CLI\_OWN | CLI\_MGR | CLI\_OPR | CLI\_VIEW | SUP\_L1 | SUP\_L2 | SUP\_VAL | SUP\_SUP | SUP\_BEH | ADM\_MOD | ADM\_RISK | ADM\_FIN | ADM\_LEG | ADM\_CMP | ADM\_BEH | ADM\_SUP |
| -------------------------- | --------- | -------- | -------- | -------- | --------- | ------- | ------- | -------- | -------- | -------- | -------- | --------- | -------- | -------- | -------- | -------- | -------- |
| Catálogo público           | R         | R        | R        | R        | R         | R       | R       | R        | R        | R        | R        | R         | R        | R        | R        | R        | R        |
| Compra de tickets          | W         | —        | —        | —        | —         | —       | —       | —        | —        | —        | —        | —         | —        | —        | —        | —        | —        |
| Sorteo propio              | —         | W        | W        | R        | R         | R       | R       | R        | R        | —        | A        | R         | R        | R        | R        | —        | R        |
| Aprobar sorteo             | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | **A**    | —         | —        | —        | —        | —        | —        |
| Valoración de premio       | —         | W        | W        | —        | R         | R       | R       | **A**    | R        | —        | R        | R         | —        | **A**    | —        | —        | R        |
| Etapas P-C                 | —         | W        | W        | W        | R         | R       | R       | R        | R        | —        | R        | R         | —        | **A**    | R        | —        | R        |
| Gate legal                 | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | R        | —         | —        | **A**    | —        | —        | R        |
| Datos de cobro             | —         | **A**    | —        | —        | R         | —       | —       | —        | —        | —        | —        | —         | R        | —        | R        | —        | R        |
| Sala: cola                 | —         | —        | —        | —        | —         | R       | R       | —        | R        | —        | R        | R         | —        | R        | R        | —        | R        |
| Sala: escribir             | R+W\*     | —        | —        | W\*      | —         | W\*     | W       | —        | W        | —        | —        | —         | —        | W        | —        | —        | W        |
| **Atestar entrega**        | —         | —        | —        | —        | —         | —       | **A**   | —        | A        | —        | —        | —         | **—**    | **A**    | —        | —        | A        |
| Adjudicar controversia     | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | —        | —         | —        | **A**    | —        | —        | A        |
| Liquidación: ver           | —         | —        | R        | —        | R         | R       | R       | —        | R        | —        | —        | —         | R        | R        | R        | —        | R        |
| **Ejecutar pago**          | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | **—**    | —         | **A**    | **—**    | —        | —        | —        |
| Ajuste de ledger           | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | —        | —         | **A**    | —        | R        | —        | R        |
| Congelar cuenta            | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | —        | **A**     | —        | —        | A        | —        | A        |
| Capacidades del cliente    | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | —        | **A**     | —        | —        | —        | —        | A        |
| Expediente de cumplimiento | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | —        | R         | —        | R        | **A**    | —        | R        |
| Aprobación sobre umbral    | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | —        | —         | —        | —        | **A**    | —        | A        |
| Panel de alarmas           | —         | —        | —        | —        | —         | R       | R       | R        | R        | R        | R        | R         | R        | R        | R        | R        | A        |
| Indicadores conductuales   | —         | —        | —        | —        | —         | —       | —       | —        | —        | R        | R        | —         | —        | —        | —        | **A**    | R        |
| Configuración de mercado   | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | —        | —         | —        | **A**    | R        | —        | A        |
| Suspensión de mercado      | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | —        | —         | —        | R        | R        | —        | **A**    |
| Usuarios internos          | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | —        | —         | —        | —        | —        | —        | **A**    |
| Segunda firma              | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | —        | —         | —        | —        | —        | —        | **A**    |

`W*` = escritura restringida a las salas en que la persona es parte o asignada.

## 7.2 Incompatibilidades y momento de comprobación

| Código | Regla                                                    | Momento                |
| ------ | -------------------------------------------------------- | ---------------------- |
| INC-01 | `ADMIN_MODERATION` y `ADMIN_FINANCE`                     | Asignación             |
| INC-02 | `ADMIN_LEGAL_COMPLIANCE` y `ADMIN_FINANCE`               | Asignación             |
| INC-03 | `ADMIN_COMPLIANCE` y `ADMIN_FINANCE`                     | Asignación             |
| INC-04 | `ADMIN_COMPLIANCE` y `ADMIN_MODERATION`                  | Asignación             |
| INC-05 | `ADMIN_BEHAVIORAL` y `ADMIN_FINANCE`                     | Asignación             |
| INC-06 | `SUPPORT_VALUATOR` no atesta el sorteo que valoró        | **Ejecución**          |
| INC-07 | `ADMIN_FINANCE` no atesta entregas                       | Asignación y ejecución |
| INC-08 | Quien adjudica no atestó ese caso                        | **Ejecución**          |
| INC-09 | Segunda firma de otra persona y otro subrol              | **Ejecución**          |
| INC-10 | Sin métrica de volumen para roles de aprobación de valor | Organizativo, auditado |
| INC-11 | `ADMIN_SUPER` no firma en segundo lugar su propia acción | **Ejecución**          |

Las de asignación se imponen por disparador sobre `subrole_assignments`. Las de ejecución se verifican en el servicio y son casos de prueba obligatorios (§14.3).

## 7.3 Autenticación

| Aspecto                    | Decisión                                                                                               |
| -------------------------- | ------------------------------------------------------------------------------------------------------ |
| Credencial de acceso       | Testigo firmado de vida corta, 15 minutos                                                              |
| Renovación                 | Testigo de renovación rotatorio, 30 días, con detección de reutilización                               |
| Portabilidad               | **Nunca exclusivamente por cookie** (RN-213): la aplicación nativa futura reutiliza el mismo mecanismo |
| Multifactor                | Obligatorio para todo subrol interno (RN-05)                                                           |
| Sesión interna             | Expiración de 30 minutos de inactividad                                                                |
| Detección de reutilización | La reutilización de un testigo de renovación revoca toda la familia y genera evento de riesgo          |

# 8\. Catálogo de errores

## 8.1 Estructura de respuesta

    {
      "error": {
        "code": "ERR_ORDER_MIN_AMOUNT",
        "message": "El monto mínimo de compra es S/ 10.00.",
        "details": { "min_amount": 1000, "currency": "PEN" },
        "trace_id": "…"
      }
    }

**RN-201.** Ningún mensaje revela existencia de cuentas, datos de terceros ni información que facilite enumeración. **RN-200.** El mensaje al usuario es llano y no culpabilizante. La causa técnica va al registro, nunca a la respuesta.

## 8.2 Catálogo

| Código                                         | HTTP | Mensaje al usuario                                                    |
| ---------------------------------------------- | ---- | --------------------------------------------------------------------- |
| `ERR_AUTH_INVALID_CREDENTIALS`                 | 401  | Los datos de acceso no son correctos.                                 |
| `ERR_AUTH_MFA_REQUIRED`                        | 401  | Se requiere verificación adicional.                                   |
| `ERR_AUTH_TOKEN_EXPIRED`                       | 401  | La sesión expiró. Ingresa nuevamente.                                 |
| `ERR_AUTH_TOKEN_REUSE`                         | 401  | Se detectó un problema de seguridad. Ingresa nuevamente.              |
| `ERR_AUTH_RATE_LIMITED`                        | 429  | Demasiados intentos. Espera unos minutos.                             |
| `ERR_IDENTITY_EMAIL_TAKEN`                     | 409  | No fue posible completar el registro con esos datos.                  |
| `ERR_IDENTITY_PHONE_TAKEN`                     | 409  | No fue posible completar el registro con esos datos.                  |
| `ERR_IDENTITY_DOCUMENT_TAKEN`                  | 409  | Ese documento ya está asociado a una cuenta.                          |
| `ERR_IDENTITY_DOCUMENT_BLOCKED`                | 403  | No es posible registrar una cuenta con ese documento.                 |
| `ERR_IDENTITY_UNDERAGE`                        | 403  | Debes ser mayor de edad para usar LIBOX.                              |
| `ERR_IDENTITY_VERIFICATION_REQUIRED`           | 403  | Verifica tu identidad para realizar tu primera compra.                |
| `ERR_IDENTITY_LIVENESS_FAILED`                 | 422  | No pudimos validar la prueba de vida. Intenta nuevamente.             |
| `ERR_IDENTITY_DOCUMENT_EXPIRED`                | 403  | Tu documento está vencido. Actualízalo para poder comprar.            |
| `ERR_RBAC_FORBIDDEN`                           | 403  | No tienes permisos para esta acción.                                  |
| `ERR_RBAC_INCOMPATIBLE_SUBROLE`                | 409  | Esa combinación de roles no está permitida.                           |
| `ERR_RBAC_SECOND_SIGNATURE_REQUIRED`           | 428  | Esta acción requiere una segunda firma.                               |
| `ERR_RBAC_SELF_SIGNATURE`                      | 409  | La segunda firma debe corresponder a otra persona.                    |
| `ERR_RAFFLE_INVALID_TRANSITION`                | 409  | El sorteo no permite esta acción en su estado actual.                 |
| `ERR_RAFFLE_CAPABILITY_DISABLED`               | 403  | Este tipo de sorteo no está habilitado para tu cuenta.                |
| `ERR_RAFFLE_TERMS_FROZEN`                      | 409  | Las bases no pueden modificarse después de publicar.                  |
| `ERR_RAFFLE_NOT_ACTIVE`                        | 409  | Este sorteo no está disponible para compra.                           |
| `ERR_PRIZE_CATEGORY_DISABLED`                  | 403  | Esta categoría de premio no está habilitada en tu mercado.            |
| `ERR_PRIZE_EVIDENCE_INCOMPLETE`                | 422  | Faltan documentos obligatorios del premio.                            |
| `ERR_PRIZE_DEVIATION_REJECTED`                 | 422  | El valor declarado excede el rango admitido frente al mercado.        |
| `ERR_PRIZE_DAILY_CODE_MISSING`                 | 422  | Las imágenes deben mostrar el código del día vigente.                 |
| `ERR_PRIZE_DAILY_CODE_EXPIRED`                 | 422  | El código del día venció. Solicita uno nuevo.                         |
| `ERR_PRIZE_REFERENCE_STALE`                    | 422  | Las referencias de mercado deben tener menos de 30 días.              |
| `ERR_REGISTRABLE_STAGE_INCOMPLETE`             | 409  | La etapa anterior debe completarse primero.                           |
| `ERR_REGISTRABLE_LIEN_FOUND`                   | 422  | El bien registra cargas o gravámenes.                                 |
| `ERR_REGISTRABLE_BLOCK_MISSING`                | 422  | Se requiere bloqueo registral vigente.                                |
| `ERR_REGISTRABLE_BLOCK_EXPIRING`               | 409  | El bloqueo registral no cubre la duración del sorteo.                 |
| `ERR_REGISTRABLE_NOT_INSCRIBED`                | 409  | La transferencia aún no consta inscrita.                              |
| `ERR_ORDER_IDEMPOTENCY_REQUIRED`               | 400  | Falta la clave de idempotencia.                                       |
| `ERR_ORDER_IDEMPOTENCY_CONFLICT`               | 409  | Esa clave ya se usó con otros datos.                                  |
| `ERR_ORDER_MIN_AMOUNT`                         | 422  | El monto mínimo de compra no se alcanza.                              |
| `ERR_ORDER_INSUFFICIENT_INVENTORY`             | 409  | No quedan tickets suficientes.                                        |
| `ERR_ORDER_RESERVATION_EXPIRED`                | 409  | La reserva expiró. Vuelve a intentarlo.                               |
| `ERR_ORDER_SELF_PURCHASE`                      | 403  | No puedes comprar tickets de tu propio sorteo.                        |
| `ERR_LIMIT_CONCENTRATION`                      | 422  | Superas el máximo de tickets permitido por participante.              |
| `ERR_LIMIT_SELF_IMPOSED`                       | 422  | Esta compra supera el límite que configuraste.                        |
| `ERR_LIMIT_SELF_EXCLUDED`                      | 403  | Tu cuenta tiene una autoexclusión activa.                             |
| `ERR_PAYMENT_PROVIDER_ERROR`                   | 502  | No pudimos procesar el pago. Intenta nuevamente.                      |
| `ERR_PAYMENT_WEBHOOK_SIGNATURE`                | 401  | — (interno)                                                           |
| `ERR_PAYMENT_WEBHOOK_REPLAY`                   | 409  | — (interno)                                                           |
| `ERR_PAYMENT_STATE_REGRESSION`                 | 409  | — (interno)                                                           |
| `ERR_DRAW_BEACON_NOT_FUTURE`                   | 422  | — (interno)                                                           |
| `ERR_DRAW_TOO_EARLY`                           | 409  | — (interno)                                                           |
| `ERR_DRAW_ALREADY_EXECUTED`                    | 409  | Este sorteo ya fue ejecutado.                                         |
| `ERR_DRAW_EMPTY_POOL`                          | 422  | — (interno)                                                           |
| `ERR_DRAW_K_EXCEEDS_POOL`                      | 422  | — (interno)                                                           |
| `ERR_DRAW_COMMITMENT_MISMATCH`                 | 500  | — (interno, alarma alta)                                              |
| `ERR_RESOLUTION_NOT_PARTICIPANT`               | 403  | No tienes acceso a esta sala.                                         |
| `ERR_RESOLUTION_IMMUTABLE`                     | 409  | Los mensajes no pueden editarse ni eliminarse.                        |
| `ERR_RESOLUTION_EXTERNAL_CONTACT`              | 422  | No es posible compartir datos de contacto externos aquí.              |
| `ERR_RESOLUTION_MONETARY_OFFER`                | 409  | Este caso fue derivado a revisión.                                    |
| `ERR_RESOLUTION_CLAIM_EXPIRED`                 | 409  | El plazo de reclamo venció.                                           |
| `ERR_RESOLUTION_ATTEST_FORBIDDEN`              | 403  | No puedes atestar este caso.                                          |
| `ERR_DISPUTE_REASON_REQUIRED`                  | 422  | Selecciona un motivo y adjunta evidencia.                             |
| `ERR_DISPUTE_EVIDENCE_REQUIRED`                | 422  | Se requiere evidencia para abrir el reclamo.                          |
| `ERR_SETTLEMENT_GATES_UNMET`                   | 409  | La liquidación aún no cumple todos los requisitos.                    |
| `ERR_SETTLEMENT_PAYOUT_UNVERIFIED`             | 409  | Los datos de cobro no están verificados.                              |
| `ERR_SETTLEMENT_PAYOUT_FROZEN`                 | 409  | Los cobros están en espera por un cambio reciente de datos bancarios. |
| `ERR_LEDGER_UNBALANCED`                        | 500  | — (interno, alarma alta)                                              |
| `ERR_COMPLIANCE_SOURCE_DECLARATION_REQUIRED`   | 428  | Para continuar necesitamos acreditar el origen de los fondos.         |
| `ERR_COMPLIANCE_SOURCE_DOCUMENTATION_REQUIRED` | 428  | Para continuar necesitamos documentación del origen de los fondos.    |
| `ERR_COMPLIANCE_PRIOR_APPROVAL_REQUIRED`       | 428  | Esta operación requiere una revisión previa.                          |
| `ERR_MARKET_SUSPENDED`                         | 503  | La operación está temporalmente suspendida en tu país.                |
| `ERR_MARKET_CATEGORY_UNAVAILABLE`              | 403  | Esta categoría no está disponible en tu mercado.                      |
| `ERR_LEGAL_GATE`                               | 422  | Falta el documento habilitante del sorteo.                            |

**Nota sobre los tres códigos de cumplimiento.** Sus mensajes son deliberadamente funcionales y neutros. **Ninguno indica análisis, sospecha ni reporte** (RN-142). Es la aplicación literal de la excepción de reserva del LBPF §0.3.

# 9\. Catálogo de eventos

## 9.1 Envoltura común

    {
      "event_id": "uuid",
      "event_name": "raffle.published",
      "schema_version": 1,
      "occurred_at": "2026-08-10T14:00:00-05:00",
      "trace_id": "uuid",
      "actor": { "id": "uuid", "kind": "CLIENT", "subrole": "CLIENT_MANAGER" },
      "aggregate": { "type": "raffle", "id": "uuid" },
      "market_code": "PE",
      "payload": { }
    }

## 9.2 Eventos de dominio

| Familia              | Eventos                                                                                                                                                                                                                         |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `identity.*`         | `registered` · `email_verified` · `phone_verified` · `identity_verified` · `liveness_passed` · `document_expiring` · `document_expired` · `blocked_minor`                                                                       |
| `client.*`           | `created` · `kyb_submitted` · `kyb_approved` · `kyb_rejected` · `payout_changed` · `payout_frozen` · `capability_changed` · `reputation_changed`                                                                                |
| `raffle.*`           | `created` · `submitted` · `valuation_approved` · `valuation_rejected` · `legal_gate_passed` · `approved` · `published` · `paused` · `resumed` · `sold_out` · `time_closed` · `threshold_met` · `threshold_failed` · `cancelled` |
| `prize.*`            | `valuation_requested` · `valuation_decided` · `daily_code_issued` · `pc_stage_approved` · `pc_stage_observed`                                                                                                                   |
| `registry.*`         | `query_performed` · `lien_detected` · `block_registered` · `block_expiring` · `inscription_verified`                                                                                                                            |
| `order.*`            | `created` · `paid` · `expired` · `cancelled` · `refunded` · `chargeback_received`                                                                                                                                               |
| `ticket.*`           | `issued` · `voided`                                                                                                                                                                                                             |
| `draw.*`             | `pool_frozen` · `commitment_published` · `executed` · `proof_generated` · `redraw_authorized` · `redraw_executed`                                                                                                               |
| `resolution.*`       | `room_opened` · `winner_notified` · `claimed` · `shipping_quoted` · `shipping_paid` · `shipping_abandoned` · `evidence_submitted` · `attested` · `attestation_reverted` · `no_claim_expired` · `no_delivery` · `closed`         |
| `dispute.*`          | `opened` · `escalated` · `adjudicated` · `withdrawn`                                                                                                                                                                            |
| `settlement.*`       | `accrued` · `gate_evaluated` · `eligible` · `held` · `approved` · `paid` · `reversed`                                                                                                                                           |
| `refund_credit.*`    | `granted` · `used` · `withdrawal_requested` · `withdrawal_paid`                                                                                                                                                                 |
| `risk.*`             | `event_raised` · `account_frozen` · `account_unfrozen`                                                                                                                                                                          |
| `compliance.*`       | `tier_reached` · `case_opened` · `case_decided`                                                                                                                                                                                 |
| `responsible_play.*` | `limit_set` · `limit_change_requested` · `purchase_blocked` · `self_exclusion_started` · `self_exclusion_ended`                                                                                                                 |
| `market.*`           | `config_changed` · `suspended` · `resumed`                                                                                                                                                                                      |
| `alarm.*`            | `raised` · `acknowledged` · `escalated` · `resolved`                                                                                                                                                                            |

## 9.3 Eventos de decisión

Alimentan los indicadores conductuales. Requieren `behavioral_zone` obligatorio.

| Evento                                      | Zona       | Propiedades                                                                                        | Alimenta   |
| ------------------------------------------- | ---------- | -------------------------------------------------------------------------------------------------- | ---------- |
| `decision.raffle_detail_viewed`             | DECISION   | `probability_visible`, `cost_visible`, `pool_visible`, `evidence_visible`, `time_to_cta_render_ms` | P1         |
| `decision.evidence_drawer_opened`           | DECISION   | `inline` (sin navegación de página)                                                                | P5         |
| `decision.cta_rendered`                     | DECISION   | `elapsed_ms_since_view`                                                                            | P1         |
| `decision.checkout_started`                 | DECISION   | `quantity`, `amount`, `refund_credit_used`                                                         | P6         |
| `decision.checkout_reviewed`                | DECISION   | `changed_before_commit`                                                                            | P9         |
| `decision.order_committed`                  | DECISION   | `order_id`                                                                                         | P6         |
| `decision.refund_requested_fast`            | DECISION   | `minutes_since_purchase`, `reason_code`                                                            | P6 error   |
| `decision.ranking_impression`               | ATTRACTION | `reason_present`, `placement_kind`, `label`                                                        | P12        |
| `decision.spend_panel_viewed`               | DECISION   | `period_amount`, `lifetime_amount`                                                                 | Protección |
| `decision.independence_notice_shown`        | DECISION   | `surface`                                                                                          | P3         |
| `decision.survey_shown` / `survey_answered` | ATTRACTION | `instrument_code`, `is_correct`                                                                    | P3, P6     |

## 9.4 Cálculo de indicadores

    -- Wilson al 95 %. z = 1.959964
    WITH s AS (
      SELECT :successes::numeric AS x, :n::numeric AS n, 1.959964::numeric AS z
    ), c AS (
      SELECT x/n AS p, n, z, z*z AS z2 FROM s
    )
    SELECT
      p,
      (p + z2/(2*n) - z*sqrt((p*(1-p) + z2/(4*n))/n)) / (1 + z2/n) AS wilson_lower,
      (p + z2/(2*n) + z*sqrt((p*(1-p) + z2/(4*n))/n)) / (1 + z2/n) AS wilson_upper
    FROM c;

**Regla de ruptura (RN-163):**

    si n < 100                          -> INSUFFICIENT_DATA
    si wilson_upper < umbral            -> ventana en incumplimiento
    si dos ventanas consecutivas        -> BREACH, se emite alarma familia BEHAVIORAL
    si wilson_lower < umbral <= upper   -> AT_RISK, sin alarma
    en otro caso                        -> OK

Se usa el límite **superior** del intervalo para declarar incumplimiento: se afirma que el indicador está mal solo cuando incluso el escenario más favorable compatible con los datos queda por debajo del umbral.

# 10\. Estructura de `market_config`

## 10.1 Documento

    {
      "market_code": "PE",
      "version": 1,
      "currency": { "code": "PEN", "minor_unit": 2, "rounding_multiple": 1000,
                    "format": "S/ #,##0.00" },
      "timezone": "America/Lima",
      "locale": "es-PE",
      "identity": {
        "document_types": ["DNI","CE"],
        "provider_adapter": "identity.pe.default",
        "liveness_required": true,
        "levels": { "L0": { "requires": ["EMAIL","PHONE"] },
                    "L1": { "requires": ["DOCUMENT"] },
                    "L2": { "requires": ["DOCUMENT","LIVENESS"] } }
      },
      "aml": {
        "prior_verification": true,
        "tiers": [
          { "tier": 1, "from": 0,        "to": 100000,  "requirement": "L1_VERIFICATION" },
          { "tier": 2, "from": 100001,   "to": 500000,  "requirement": "L2_VERIFICATION" },
          { "tier": 3, "from": 500001,   "to": 1500000, "requirement": "SOURCE_DECLARATION",
            "alarm": "MEDIUM" },
          { "tier": 4, "from": 1500001,  "to": 10000000,"requirement": "SOURCE_DOCUMENTATION",
            "alarm": "HIGH" },
          { "tier": 5, "from": 10000001, "to": null,    "requirement": "PRIOR_APPROVAL",
            "alarm": "HIGH", "label_key": "enhanced_accreditation_threshold" }
        ],
        "shared_instrument": { "info_at": 3, "medium_at": 5 }
      },
      "tax": { "name": "IGV", "rate_bp": 1800, "base": "PLATFORM_FEE",
               "invoice_issuer": "PENDING_LEGAL_OPINION",
               "provider_adapter": "invoice.pe.default" },
      "legal_gate": { "scope": "per_raffle", "document_type": "BASES_AUTORIZADAS",
                      "authority": "PENDING_LEGAL_OPINION", "blocks": "PUBLICATION" },
      "deadlines": {
        "claim_by_value": [
          { "up_to": 300000,  "days": 7  },
          { "up_to": 1000000, "days": 15 },
          { "up_to": null,    "days": 30 }
        ],
        "delivery_by_category": { "P_A": 20, "P_B": 20, "P_C1": 45, "P_C2": 90,
                                  "P_D": 30, "P_E": 7 },
        "business_days_categories": ["P_C1","P_C2"],
        "shipping_choice_days": 7,
        "shipping_grace_days": 7,
        "settlement_hold_days": 7,
        "chargeback_reserve_days": 90,
        "dispute_adjudication_days": 10
      },
      "settlement": { "reserve_bp": 500 },
      "fee_schedule": {
        "active": false,
        "base_fee_bp": 2000,
        "levels": [
          { "level": "E0", "fee_bp": 2000, "threshold_from": 0 },
          { "level": "E1", "fee_bp": 1800, "threshold_from": null },
          { "level": "E2", "fee_bp": 1600, "threshold_from": null },
          { "level": "E3", "fee_bp": 1400, "threshold_from": null },
          { "level": "E4", "fee_bp": 1200, "threshold_from": null }
        ],
        "_note": "Umbrales nulos hasta calibrarlos con el costo unitario real (L1 V1 §6.4). La escala se activa a partir del cuarto trimestre de operacion."
      },
      "prize_categories": { "P_A": true, "P_B": true, "P_C1": true, "P_C2": false,
                            "P_D": true, "P_E": true, "P_F": false },
      "raffle_types": { "T1": true, "T2": true, "T3": true, "T4": false,
                        "T5": false, "T6": false, "T7": false, "T8": false },
      "raffle_type_params": {
        "T2": { "early_close_on_threshold": false },
        "T4": { "min_milestones": 2, "max_milestones": 6 },
        "T5": { "max_duration_minutes": 240, "min_duration_minutes": 15,
                "reservation_ttl_minutes": 10 },
        "T6": { "max_winners": 10 },
        "T7": { "max_editions": 52, "min_gap_hours": 24 }
      },
      "purchase": { "min_order_amount": 1000, "ticket_price_min": 100,
                    "ticket_price_max": 5000000, "reservation_ttl_minutes": 30 },
      "concentration": { "max_bp": 3000, "alarm_info_bp": 1500, "alarm_medium_bp": 2500 },
      "valuation_bands": [
        { "band": "V1", "up_to": 100000,  "approver": "SUPPORT_VALUATOR" },
        { "band": "V2", "up_to": 1000000, "approver": "SUPPORT_VALUATOR",
          "cosign": "ADMIN_MODERATION" },
        { "band": "V3", "up_to": 5000000, "approver": "ADMIN_LEGAL_COMPLIANCE" },
        { "band": "V4", "up_to": null,    "approver": "ADMIN_LEGAL_COMPLIANCE",
          "second_signature": true }
      ],
      "valuation_deviation": { "approvable_bp": 2000, "cosign_bp": 5000,
                               "auto_reject_bp": 5001 },
      "draw": { "beacon_source": "…", "beacon_round_kind": "ROUND_NUMBER",
                "min_commit_window_minutes": 60,
                "algorithm_version": "libox-draw-1.0" },
      "responsible_play": { "self_exclusion_options": ["D7","D30","D90","PERMANENT"],
                            "limit_increase_delay_hours": 24,
                            "cooling_off_enabled": false,
                            "reality_check_enabled": false },
      "behavioral": { "survey_target_n_per_month": 150,
                      "survey_sampling_mode": "ADAPTIVE",
                      "kpi_thresholds": { "P1": 0.95, "P3": 0.85, "P5": 0.95,
                                          "P6_error": 0.005, "P6_regret": 0.03 } },
      "psp": { "primary_adapter": "psp.pe.mercadopago", "fallback_adapter": null },
      "providers": {
        "identity":   { "adapter": "identity.pe.default", "vendor": "PENDING_CONTRACT",
                        "source": "registro oficial de identificación del mercado",
                        "liveness": true },
        "tax_document": { "adapter": "taxdoc.pe.default", "vendor": "PENDING_CONTRACT",
                        "source": "autoridad tributaria del mercado" },
        "registry":   { "adapter": "registry.pe.default", "vendor": "PENDING_CONTRACT",
                        "source": "registro público competente" },
        "invoice":    { "adapter": "invoice.pe.default", "vendor": "PENDING_CONTRACT" },
        "beacon":     { "adapter": "beacon.public", "vendor": "PENDING_SELECTION" }
      },
      "capacity_limits": {
        "max_active_raffles_per_market": 500,
        "max_concurrent_organizers_with_active_raffle": null,
        "max_members_per_legal_client": 10,
        "max_members_per_natural_client": 1,
        "min_super_admins": 2,
        "_note": "El limite de organizadores con sorteo activo es de capacidad de operacion, no tecnico. Al alcanzarse, las publicaciones entran en cola con fecha estimada; nunca se rechazan (RN-06-quinquies)."
      },
      "content_policy": { "prohibited_categories": ["WEAPONS","ALCOHOL","TOBACCO",
                          "LIVE_ANIMALS","ADULT","CRYPTO"] }
    }

## 10.2 Resolución de configuración

    -- Al publicar: se congela la version vigente en raffles.config_version_id.
    SELECT id FROM market_config_versions
     WHERE market_code = :m AND effective_to IS NULL;
    
    -- Al operar un sorteo: se usa SIEMPRE su version congelada, nunca la actual.
    SELECT config FROM market_config_versions WHERE id = :raffle_config_version_id;

**INV-15.** Ningún servicio consulta la configuración vigente para operar un sorteo ya publicado. Es caso de prueba obligatorio: cambiar la configuración y comprobar que los sorteos previos conservan sus reglas.

## 10.3 Adaptadores

| Interfaz                | Responsabilidad                                      | Adaptador PE          |
| ----------------------- | ---------------------------------------------------- | --------------------- |
| `IIdentityVerifier`     | Validar documento y prueba de vida                   | `identity.pe.default` |
| `IPaymentProvider`      | Preferencia, cobro, webhook, reembolso, conciliación | `psp.pe.mercadopago`  |
| `IInvoiceIssuer`        | Emisión de comprobante                               | `invoice.pe.default`  |
| `IRegistryProvider`     | Consulta registral de bienes                         | `registry.pe.default` |
| `ITaxDocumentValidator` | Validación de comprobante de compra del premio       | `taxdoc.pe.default`   |
| `IEntropyBeacon`        | Obtención de baliza pública por ronda                | Común a mercados      |

**La elección es dato; la integración es código.** Añadir un mercado con proveedores existentes es configuración. Añadirlo con proveedores nuevos requiere implementar adaptadores, nunca modificar el dominio.

# 11\. Contratos de interfaz

## 11.1 Convenciones

| Aspecto       | Regla                                                    |
| ------------- | -------------------------------------------------------- |
| Base          | `/api/v1`                                                |
| Autenticación | `Authorization: Bearer <token>`                          |
| Idempotencia  | `Idempotency-Key` obligatoria en toda mutación de dinero |
| Trazabilidad  | `X-Trace-Id` aceptada; si falta, se genera y se devuelve |
| Paginación    | Por cursor: `cursor`, `limit` (máximo 100)               |
| Importes      | Entero de unidad mínima, con `currency` adyacente        |
| Fechas        | ISO 8601 con desplazamiento del mercado                  |
| Versionado    | Ningún cambio incompatible sin nueva versión mayor       |

## 11.2 Compra

    POST /api/v1/orders
    Headers: Authorization, Idempotency-Key, X-Trace-Id
    { "raffle_id": "uuid", "quantity": 5, "use_refund_credit": true,
      "device_id": "uuid" }

Respuesta `201`:

    { "order_id": "uuid", "status": "PENDING_PAYMENT",
      "currency": "PEN", "unit_price": 500, "gross_amount": 2500,
      "refund_credit_applied": 500, "cash_amount": 2000,
      "reserved_until": "2026-08-10T14:30:00-05:00",
      "payment": { "provider": "mercadopago", "preference_id": "…",
                   "checkout_url": "https://…" },
      "trace_id": "uuid" }

Errores: `ERR_ORDER_MIN_AMOUNT` · `ERR_ORDER_INSUFFICIENT_INVENTORY` · `ERR_LIMIT_CONCENTRATION` · `ERR_LIMIT_SELF_IMPOSED` · `ERR_LIMIT_SELF_EXCLUDED` · `ERR_ORDER_SELF_PURCHASE` · `ERR_IDENTITY_VERIFICATION_REQUIRED` · `ERR_COMPLIANCE_*` · `ERR_RAFFLE_NOT_ACTIVE`.

**Orden de validación.** Autoexclusión → verificación de identidad → tramo de cumplimiento → autocompra → concentración → límite propio → importe mínimo → inventario. Se valida antes lo que es una prohibición absoluta y después lo que depende de disponibilidad, para que el mensaje al usuario sea el más informativo posible.

    GET /api/v1/orders/{id}

Devuelve estado real. Es el punto de recuperación tras pérdida de conexión (RN-218): la aplicación consulta y muestra estado inequívoco, nunca ambigüedad.

## 11.3 Tickets y participación

    GET /api/v1/me/tickets?cursor=&limit=
    GET /api/v1/me/tickets/{raffle_id}
    { "raffle_code": "LBX-202608-A7K3M",
      "ticket_numbers": [143,144,145],
      "pool": { "sold": 750, "total": 1000 },
      "probability": { "fraction": "3 / 750", "percent": 0.4,
                       "per_thousand_text": "4 de cada 1.000 tickets vendidos" },
      "independence_notice": "Los resultados anteriores no aumentan ni reducen la probabilidad de este sorteo. Cada sorteo es independiente." }

**No devuelve** identidad de otros participantes ni distribución de tenencia (R-10).

## 11.4 Verificación pública

    GET /api/v1/public/draws/{slug}          -- sin autenticacion
    GET /api/v1/public/draws/{slug}/pool     -- snapshot completo del pool

Devuelve el documento de prueba de §5.5. Indexable, cacheable, sin datos personales.

## 11.5 Resolución

    POST /api/v1/rooms/{id}/messages
    POST /api/v1/rooms/{id}/evidence
    POST /api/v1/rooms/{id}/claim
    POST /api/v1/rooms/{id}/shipping-quotes
    POST /api/v1/rooms/{id}/shipping-selection
    POST /api/v1/rooms/{id}/attest            -- SUPPORT_L2 / ADMIN_LEGAL_COMPLIANCE
    POST /api/v1/rooms/{id}/sla-extension
    GET  /api/v1/rooms/{id}/forensic-export   -- ADMIN

`POST /rooms/{id}/attest`:

    { "evidence_ids": ["uuid"], "winner_confirmed": true,
      "statement": "…", "second_signer_id": "uuid" }

Respuesta `201` con la atestación y **el estado de los seis gates de liquidación tras la evaluación**, para que el operador vea de inmediato si algo más bloquea el pago.

## 11.6 Liquidación

    GET  /api/v1/clients/{id}/settlements
    GET  /api/v1/settlements/{id}
    POST /api/v1/settlements/{id}/execute     -- ADMIN_FINANCE
    POST /api/v1/settlements/batch-execute    -- ADMIN_FINANCE, lote
    { "settlement_id": "uuid", "status": "HELD",
      "gross_collected": 563000, "libox_fee_amount": 112600,
      "chargeback_reserve": 22520, "net_payable": 427880,
      "gates": { "g1_draw": true, "g2_delivery": true, "g3_disputes": true,
                 "g4_chargeback": false, "g5_payout": true, "g6_ledger": true },
      "hold_until": "2026-08-25T00:00:00-05:00",
      "hold_reason": "Ventana de retención por contracargo" }

**El motivo y la fecha estimada se exponen siempre al organizador** (RN-102): un estado retenido sin explicación se interpreta como retención indebida.

## 11.7 Endpoints restantes

| Familia          | Endpoints                                                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Identidad        | `POST /auth/register` · `/auth/verify-contact` · `/auth/login` · `/auth/refresh` · `/identity/verify` · `/identity/liveness`                |
| Organizador      | `POST /clients` · `/clients/{id}/kyb` · `/clients/{id}/members` · `PUT /clients/{id}/payout` · `/clients/{id}/capabilities`                 |
| Catálogo         | `GET /raffles` · `/raffles/{slug}` · `/raffles/{slug}/terms`                                                                                |
| Sorteo           | `POST /raffles` · `PATCH /raffles/{id}` · `POST /raffles/{id}/submit` · `/raffles/{id}/prize-valuation` · `/raffles/{id}/pc-stages/{stage}` |
| Pagos            | `POST /webhooks/psp/{provider}` · `GET /reconciliation/{date}` · `POST /reconciliation/exceptions/{id}/resolve`                             |
| Sorteo ejecutado | `POST /raffles/{id}/freeze` · `/raffles/{id}/execute-draw` · `/raffles/{id}/redraw`                                                         |
| Controversias    | `POST /disputes` · `/disputes/{id}/evidence` · `/disputes/{id}/adjudicate`                                                                  |
| Saldo            | `GET /me/refund-credit` · `POST /me/refund-credit/withdrawals`                                                                              |
| Protección       | `GET/PUT /me/limits` · `POST /me/self-exclusion` · `GET /me/spend-panel`                                                                    |
| Cumplimiento     | `GET /compliance/cases` · `POST /compliance/cases/{id}/decide`                                                                              |
| Alarmas          | `GET /alarms` · `POST /alarms/{id}/acknowledge` · `/alarms/{id}/resolve`                                                                    |
| Mercado          | `GET /markets/{code}/config` · `POST /markets/{code}/config` · `/markets/{code}/suspend`                                                    |
| Simulador        | `POST /public/pricing-simulator` — **sin autenticación**                                                                                    |

# 12\. Concurrencia, idempotencia y trabajos

## 12.1 Bloqueo autoritativo

**RN-56.** El bloqueo autoritativo sobre dinero e inventario es de base de datos. Un bloqueo distribuido en memoria es optimización de fast-fail; nunca la garantía, porque una conmutación puede producir dos poseedores del mismo bloqueo.

## 12.2 Reserva de inventario

La carrera real ocurre sobre el pool, no sobre el usuario. Serializar por usuario, como hacía la versión anterior, no la resuelve.

    UPDATE raffles
       SET tickets_reserved = tickets_reserved + :qty
     WHERE id = :raffle_id
       AND status = 'ACTIVE'
       AND tickets_reserved + :qty <= total_tickets
    RETURNING tickets_reserved;
    -- Cero filas afectadas -> ERR_ORDER_INSUFFICIENT_INVENTORY

Actualización condicional atómica, sin lectura previa. La liberación por expiración corre en el trabajo `release-expired-reservations`.

## 12.3 Emisión de tickets

Al confirmarse el pago, en una única transacción: bloqueo de fila del sorteo, asignación del rango de números con la actualización de §3.5, inserción de tickets, asientos T-01, T-02, T-04, T-05 y T-06, y publicación de eventos.

## 12.4 Idempotencia

    1. INSERT en idempotency_keys con status IN_FLIGHT.
       Conflicto de clave única -> ya existe:
         - COMPLETED con mismo request_hash -> devolver stored_response
         - COMPLETED con distinto hash      -> ERR_ORDER_IDEMPOTENCY_CONFLICT
         - IN_FLIGHT                        -> 409 con reintento sugerido
    2. Ejecutar la operación.
    3. Actualizar a COMPLETED con la respuesta.

**La clave la genera el cliente por intento.** No se deriva del contenido: dos compras legítimas idénticas separadas en el tiempo producirían el mismo hash y la segunda devolvería la primera, dejando al usuario sin sus tickets.

## 12.5 Webhooks

    1. Validar firma y ventana anti-repetición.
    2. Persistir en psp_events con la carga original y su hash.
       Conflicto de deduplicación -> marcar DUPLICATE y responder 200.
    3. Procesar con monotonía de estado: si status_rank entrante <= actual, ignorar.
    4. Marcar PROCESSED. Ante fallo, FAILED con reintento exponencial y alarma.

Se responde `200` incluso ante duplicado: un error haría reintentar indefinidamente al proveedor.

## 12.6 Trabajos programados

| Trabajo                              | Frecuencia | Responsabilidad                                                                                                     |
| ------------------------------------ | ---------- | ------------------------------------------------------------------------------------------------------------------- |
| `release-expired-reservations`       | 1 min      | Liberar inventario de órdenes vencidas                                                                              |
| `close-raffles-by-time`              | 1 min      | `ENDED_TIME` al llegar el cierre                                                                                    |
| `evaluate-thresholds`                | 1 min      | Umbral alcanzado o fallido                                                                                          |
| `freeze-pools`                       | 1 min      | Congelar, publicar compromiso y anunciar baliza                                                                     |
| `execute-draws`                      | 1 min      | Ejecutar tras `earliest_execution_at` con baliza disponible                                                         |
| `dispatch-outbox`                    | 10 s       | Despachar eventos pendientes                                                                                        |
| `retry-audit-emergency`              | 1 min      | Reintentar cola de auditoría                                                                                        |
| `check-room-slas`                    | 15 min     | Vencimientos de reclamo, envío y entrega                                                                            |
| `send-winner-reminders`              | 1 h        | Cadencia de contacto por tramo                                                                                      |
| `recheck-registry-blocks`            | 24 h       | Reconsulta registral de P-C y vigencia de bloqueo                                                                   |
| `evaluate-settlement-gates`          | 15 min     | Recalcular los seis gates                                                                                           |
| `release-chargeback-reserves`        | 24 h       | Liberar reservas vencidas                                                                                           |
| `daily-reconciliation`               | 24 h       | Conciliación con el proveedor y cola de excepciones                                                                 |
| `verify-ledger-invariants`           | 24 h       | L-01 a L-07                                                                                                         |
| `compute-client-reputation`          | 24 h       | Recalcular puntuación y nivel de reputación                                                                         |
| `recompute-client-fee-level`         | 24 h       | Recalcular el nivel de comisión sobre volumen liquidado móvil de 12 meses. **Nunca modifica sorteos ya publicados** |
| `compute-kpi-snapshots`              | 24 h       | Ventanas móviles con Wilson                                                                                         |
| `check-document-expiry`              | 24 h       | Aviso de vencimiento a 30 días                                                                                      |
| `expire-self-exclusions`             | 1 h        | Fin de plazo de autoexclusión                                                                                       |
| `apply-pending-limit-increases`      | 1 h        | Aumentos tras 24 horas                                                                                              |
| `create-next-partitions`             | 24 h       | Particiones del mes siguiente                                                                                       |
| `accrue-subscription-revenue`        | 24 h       | Devengo diario de suscripciones y planes promocionales (T-16)                                                       |
| `close-exhausted-campaigns`          | 1 min      | Cerrar campañas gratuitas con cupo agotado                                                                          |
| `open-close-operating-windows`       | 1 min      | Ejecutar lo diferido al abrirse la ventana y detener al cerrarse                                                    |
| `reset-promotional-quota`            | 24 h       | Reiniciar el cupo mensual de los planes promocionales                                                               |
| `purge-expired-idempotency-keys`     | 24 h       | Archivar y eliminar claves vencidas. La tabla tenía vencimiento sin proceso que lo aplicara                         |
| `refresh-market-reference-freshness` | 24 h       | Recalcular `is_fresh` de referencias de mercado. Sustituye a la restricción no inmutable de V1                      |
| `evaluate-milestones`                | 1 min      | T4: marcar hitos alcanzados y disparar el sorteo cuando corresponda                                                 |
| `create-recurring-editions`          | 1 h        | T7: crear la edición siguiente de cada serie activa                                                                 |
| `purge-expired-documents`            | 24 h       | Retención de documentos personales                                                                                  |

**Todos idempotentes y con bloqueo de ejecución única.** Un trabajo que se ejecuta dos veces no debe producir efecto doble.

# 13\. Observabilidad y operación

## 13.1 Trazabilidad

`trace_id` se genera en el borde y se propaga por toda la cadena: registro, base de datos, eventos, notificaciones y respuestas. La consulta por `trace_id` reconstruye la línea de tiempo completa.

## 13.2 Objetivos de nivel de servicio

| Métrica                                                 | Objetivo       |
| ------------------------------------------------------- | -------------- |
| Disponibilidad de superficies públicas                  | 99,5 % mensual |
| Latencia p95 de API propia                              | \< 500 ms      |
| Latencia p95 de creación de orden, excluyendo proveedor | \< 800 ms      |
| Retraso de despacho del outbox                          | \< 60 s        |
| Tiempo de procesamiento de webhook                      | \< 5 s         |

**Se mide la API propia separada del proveedor.** Mezclarlas hace incumplir el objetivo por causas ajenas y vuelve inútil la métrica.

## 13.3 Alertas técnicas

| Alerta                                                         | Severidad |
| -------------------------------------------------------------- | --------- |
| Divergencia de invariante contable (L-01 a L-07)               | Alta      |
| Outbox con retraso superior a 5 minutos                        | Alta      |
| Cola de auditoría de emergencia no vacía por más de 15 minutos | Alta      |
| Tasa de webhooks fallidos superior al 1 %                      | Alta      |
| Falta de partición para el mes siguiente                       | Alta      |
| `ERR_DRAW_COMMITMENT_MISMATCH` en cualquier ocurrencia         | Alta      |
| Excepciones de conciliación fuera de plazo                     | Media     |
| Latencia p95 por encima del objetivo durante 15 minutos        | Media     |
| Bloqueo registral próximo a vencer con sorteo activo           | Media     |

## 13.4 Runbooks

| Incidente                     | Procedimiento resumido                                                                                                                             |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Proveedor de pagos caído      | Suspender ventas del mercado en nivel L1; conservar sorteos activos; comunicar; reanudar y liberar reservas expiradas                              |
| Webhooks no llegan            | Conciliar por consulta activa contra el proveedor; reprocesar desde `psp_events`; verificar firma y clave                                          |
| Divergencia de ledger         | Congelar liquidaciones del ámbito afectado; identificar el asiento por `trace_id`; corregir con T-14 y segunda firma; nunca editar `journal_lines` |
| Sorteo con pool incorrecto    | No re-ejecutar. Congelar liquidación, abrir caso, publicar comunicación; la corrección exige decisión de dirección y queda registrada              |
| Saldo de reembolso divergente | Recomputar desde `refund_credit_entries`; la caché nunca es la verdad                                                                              |
| Gravamen sobrevenido en P-C   | Suspender el sorteo de inmediato, notificar, evaluar cancelación con reembolso íntegro                                                             |

# 14\. Estrategia de pruebas

## 14.1 Pirámide

| Nivel             | Alcance                                       | Cobertura mínima                 | Ejecución        |
| ----------------- | --------------------------------------------- | -------------------------------- | ---------------- |
| Unitaria          | Reglas de negocio, cálculo, transiciones      | 80 % en dominio financiero       | Cada integración |
| Integración       | Flujos entre agregados con base de datos real | Todos los casos de uso de dinero | Cada integración |
| Contrato          | Conformidad con `libox_openapi_L3_V7.yaml`    | 100 % de endpoints               | Cada integración |
| Propiedad         | Invariantes                                   | Ver §14.2                        | Cada integración |
| Extremo a extremo | Recorridos por rol                            | Los 12 recorridos críticos       | Diaria           |
| Carga             | Presupuesto de rendimiento                    | —                                | Semanal          |
| Ensayo real       | Ciclo completo con dinero real                | Gate de fase                     | Una vez por fase |

## 14.2 Pruebas de propiedad

Ejecutan secuencias aleatorias de N operaciones y verifican que los invariantes se mantienen en todo momento.

| Prueba                           | Invariante                                                                                                                  |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `prop_ledger_balanced`           | Para cualquier secuencia, todo asiento cuadra (INV-10)                                                                      |
| `prop_no_ticket_without_payment` | No existe ticket `ISSUED` sin orden `PAID` (INV-09)                                                                         |
| `prop_no_number_reuse`           | Ningún número se asigna dos veces en un sorteo (INV-11)                                                                     |
| `prop_refund_solvency`           | La recaudación retenida cubre el reembolso íntegro (INV-16)                                                                 |
| `prop_credit_cache`              | La caché de saldo coincide con la suma de movimientos                                                                       |
| `prop_concentration`             | Ningún usuario supera el umbral (INV-13)                                                                                    |
| `prop_no_oversell`               | `tickets_issued ≤ total_tickets` bajo concurrencia                                                                          |
| `prop_settlement_gates`          | Ninguna liquidación alcanza `PAID` sin los seis gates (INV-23)                                                              |
| `prop_fee_frozen_at_publish`     | Un cambio de nivel de comisión no altera la tasa de sorteos ya publicados ni el desglose de órdenes ya emitidas (RN-01-bis) |
| `prop_client_net_invariant`      | `client_net_amount` es siempre el 80 % del bruto, sea cual sea el régimen tributario (TX-01)                                |
| `prop_beacon_future`             | Ningún compromiso admite una ronda de baliza anterior o igual a su publicación (INV-18)                                     |

## 14.3 Casos obligatorios de control de acceso

| Caso                                                                        | Resultado esperado                       |
| --------------------------------------------------------------------------- | ---------------------------------------- |
| `SUPPORT_L2` intenta ejecutar liquidación                                   | `ERR_RBAC_FORBIDDEN`                     |
| `SUPPORT_L2` intenta modificar ganador                                      | `ERR_RBAC_FORBIDDEN`                     |
| `SUPPORT_L2` intenta asiento de ledger                                      | `ERR_RBAC_FORBIDDEN`                     |
| `SUPPORT_VALUATOR` atesta el sorteo que valoró                              | `ERR_RBAC_FORBIDDEN` (INC-06)            |
| `ADMIN_FINANCE` atesta una entrega                                          | `ERR_RBAC_FORBIDDEN` (INC-07)            |
| Quien atestó adjudica esa controversia                                      | `ERR_RBAC_FORBIDDEN` (INC-08)            |
| Segunda firma de la misma persona                                           | `ERR_RBAC_SELF_SIGNATURE` (INC-09)       |
| Asignar `ADMIN_MODERATION` a quien tiene `ADMIN_FINANCE`                    | `ERR_RBAC_INCOMPATIBLE_SUBROLE` (INC-01) |
| `CLIENT_MANAGER` cambia datos bancarios                                     | `ERR_RBAC_FORBIDDEN`                     |
| Organizador compra en su propio sorteo                                      | `ERR_ORDER_SELF_PURCHASE`                |
| Alta de organizador persona jurídica sin identificador tributario           | `ck_clients_legal`                       |
| Alta de organizador persona natural sin titular verificado                  | `ck_clients_natural`                     |
| **Alta de organizador persona natural sin identificador tributario**        | **Admitida**                             |
| Dos organizadores persona natural con el mismo documento                    | `ux_clients_owner_doc`                   |
| Subusuario en organizador persona natural                                   | `ERR_CLIENT_NATURAL_NO_DELEGATION`       |
| Excepción de tasa superior al techo del mercado                             | `ck_fee_exception_ceiling`               |
| Excepción de tasa con la misma persona en ambas firmas                      | `ck_fee_exception_signer`                |
| Excepción de tasa sin vigencia limitada                                     | `ck_fee_exception_window`                |
| **Oportunidad pagada con múltiplo bajo 1,25×**                              | `ck_raffles_multiple_floor`              |
| **Múltiplo sobre 4,0× sin doble firma**                                     | `ck_raffles_multiple_ceiling`            |
| Múltiplo sobre techo con la misma persona en ambas firmas                   | `ck_raffles_multiple_signer`             |
| **Oportunidad sin recaudación publicada sin garantía sustitutiva**          | `ck_raffles_guarantee`                   |
| **Categoría registrable en régimen promocional sin custodia**               | `ERR_REGISTRABLE_NO_ESCROW`              |
| Oportunidad gratuita con precio de ticket distinto de cero                  | `ck_raffles_regime_pricing`              |
| Régimen pagado con origen de premio declarado                               | `ck_raffles_prize_origin`                |
| **Dos participaciones gratuitas del mismo usuario en la misma oportunidad** | `ux_feg_user`                            |
| **Campaña que emite más participaciones que su cupo**                       | `ck_fec_quota`                           |
| Ampliación de cupo sin autorización registrada                              | `ck_fec_extension`                       |
| **Plan de suscripción que otorgue participaciones**                         | `subscription_plans.grants_entries`      |
| **Beneficio que aplique descuento sobre el ticket**                         | `benefits.applies_to_tickets`            |
| Apagado global sin segunda firma o sin motivo                               | `ck_pc_disable`                          |
| Apagado global con la misma persona en ambas firmas                         | `ck_pc_signer`                           |
| `SUPPORT_SUPERVISOR` **intenta crear** `SUPPORT_L2`                         | `ERR_RBAC_GRANT_CEILING`                 |
| `SUPPORT_SUPERVISOR` crea `SUPPORT_L1`                                      | **Admitido**                             |
| Cualquier subrol se otorga un privilegio a sí mismo                         | `ERR_RBAC_SELF_GRANT`                    |
| `ADMIN_SUPER` otorga `ADMIN_FINANCE` sin segunda firma                      | `ERR_RBAC_SECOND_SIGNATURE_REQUIRED`     |
| Revocar al penúltimo `ADMIN_SUPER`                                          | **Admitido**                             |
| Revocar al último `ADMIN_SUPER`                                             | `ERR_RBAC_LAST_SUPER_ADMIN`              |
| Suspender la propia cuenta interna                                          | `ck_susp_self`                           |
| Restaurar una suspensión sin motivo                                         | `ck_susp_restore`                        |

## 14.4 Concurrencia

| Prueba                      | Escenario                                                                                                                        |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `conc_last_tickets`         | 50 solicitudes simultáneas por los últimos 3 tickets: exactamente 3 emitidos                                                     |
| `conc_duplicate_webhooks`   | Mismo evento 10 veces en paralelo: un solo procesamiento                                                                         |
| `conc_double_click`         | Misma clave de idempotencia en paralelo: una orden                                                                               |
| `conc_refund_credit`        | Uso simultáneo del mismo saldo: sin saldo negativo                                                                               |
| `conc_double_draw`          | Dos ejecuciones simultáneas del mismo sorteo: una persiste, la otra recibe `ERR_DRAW_ALREADY_EXECUTED`                           |
| `conc_webhook_cross_month`  | El mismo evento de proveedor recibido en dos meses distintos: **un solo procesamiento**. Verifica la corrección de deduplicación |
| `conc_room_seq_cross_month` | Sala que cruza de mes: la secuencia no se repite y la cadena de hashes permanece continua                                        |

## 14.5 Verificación del sorteo

Los cinco vectores de §5.7 se ejecutan en cada integración. **La implementación de verificación debe ser independiente de la de ejecución**, escrita por persona distinta: una verificación que comparte código con la ejecución no verifica nada.

## 14.6 Verificación estática conductual

| Regla                    | Verifica                                        | Efecto            |
| ------------------------ | ----------------------------------------------- | ----------------- |
| LINT-003                 | Animación superior a 240 ms en zona de decisión | **Bloquea merge** |
| LINT-004                 | Animación infinita en zona de decisión          | **Bloquea merge** |
| LINT-005                 | Opción monetaria o de comunicación premarcada   | **Bloquea merge** |
| LINT-001, 002, 006 a 010 | Resto del catálogo conductual                   | Advierte          |

Se ejecutan sobre el árbol de componentes y sus metadatos declarados, no sobre el sistema en ejecución.

## 14.7 Ensayo con dinero real

Gate binario de fase. Ciclo completo con importe simbólico real: alta de organizador, KYB, verificación de premio, gate legal, publicación, verificación de identidad del comprador, compra con pago real, emisión de tickets, congelamiento con compromiso, ejecución con baliza, verificación pública por un tercero, apertura de sala, evidencia, atestación, evaluación de los seis gates, liquidación con pago real, y comprobación de los siete invariantes contables.

**Ningún resultado parcial lo satisface.**

# Anexo A — Orden de migraciones

| \#  | Migración                | Contenido                                                                                                                                                                                                           |
| --- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 001 | Dominios y roles         | Tipos de dominio, roles de base de datos                                                                                                                                                                            |
| 002 | Mercado                  | `markets`, `market_config_versions`, requisitos, categorías, feriados                                                                                                                                               |
| 003 | Identidad                | `users`, credenciales, testigos, dispositivos, documentos bloqueados                                                                                                                                                |
| 004 | Verificación             | Verificaciones de identidad y edad, documentos                                                                                                                                                                      |
| 005 | Organizador              | `clients`, miembros, KYB, cobro, capacidades                                                                                                                                                                        |
| 006 | Reputación               | Reputación de organizador y de usuario                                                                                                                                                                              |
| 007 | Sorteo                   | Tipos con **semilla completa T1–T8 (§4.1.1)**, `raffles`, bases, medios, hitos, recurrencias, transiciones                                                                                                          |
| 008 | Premio                   | `prizes`, valoraciones, documentos, referencias, códigos del día                                                                                                                                                    |
| 009 | Registrables             | Activos, consultas, bloqueos, instrumentos, etapas, actos                                                                                                                                                           |
| 010 | Orden y pago             | Idempotencia, `orders`, `payments`, log de eventos, `processed_psp_events` **no particionada**, conciliación                                                                                                        |
| 011 | Tickets                  | `tickets` y sus índices                                                                                                                                                                                             |
| 012 | Sorteo ejecutado         | Compromisos, ejecuciones, ganadores, pruebas, re-sorteos                                                                                                                                                            |
| 013 | Resolución               | Salas, participantes, `room_message_sequences` **no particionada**, mensajes, evidencia, atestaciones, plazos                                                                                                       |
| 014 | Controversias            | Controversias, evidencia, adjudicaciones                                                                                                                                                                            |
| 015 | Contabilidad             | Cuentas, asientos, líneas, disparador de cuadre                                                                                                                                                                     |
| 016 | Liquidación              | `settlements`, retenciones                                                                                                                                                                                          |
| 017 | Saldo de reembolso       | Saldos, movimientos, retiros                                                                                                                                                                                        |
| 018 | Cumplimiento y riesgo    | Acumuladores, tramos, expedientes, registro, reglas, eventos                                                                                                                                                        |
| 019 | Protección               | Autoexclusión, límites, cambios, eventos                                                                                                                                                                            |
| 020 | Analítica                | Eventos, encuestas, indicadores                                                                                                                                                                                     |
| 021 | Alarmas y notificaciones | Panel, resoluciones, plantillas, intentos, preferencias                                                                                                                                                             |
| 022 | Auditoría                | Eventos, cola de emergencia, outbox                                                                                                                                                                                 |
| 023 | Growth                   | Atribución, referidos, promociones, destacados, listas, contactos                                                                                                                                                   |
| 024 | Control de acceso        | Asignaciones de subrol, incompatibilidades                                                                                                                                                                          |
| 025 | Particiones              | Particiones iniciales y trabajo de creación                                                                                                                                                                         |
| 026 | Datos semilla            | Mercado PE, cuentas contables por moneda, reglas de fuerza probatoria, instrumentos de encuesta, incompatibilidades de subrol, **matriz de otorgamiento** y **administrador semilla con credencial de un solo uso** |

## Anexo B — Materias pendientes de dictamen

Los siguientes valores figuran como `PENDING_LEGAL_OPINION` en la configuración y **deben resolverse antes de operar**: aplicabilidad del impuesto sobre la comisión, su base y su contribuyente (§6.2.1) · emisor del comprobante y base imponible · autoridad y tipo de documento del gate legal · calificación como sujeto obligado y sus umbrales · admisibilidad de la custodia de fondos · plazo y renovación del bloqueo registral · tratamiento tributario del premio para el ganador · límite de responsabilidad oponible.

*LIBOX Especificación Técnica L3 V7. Implementa LIBOX PRD BLUEPRINT MVP V4 (nivel L2), gobernado por LBPF V3 (nivel L0). Este documento no crea reglas de negocio: las implementa.*
