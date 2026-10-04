---
title: LIBOX Especificación Técnica L3 V8 — borrador DRAFT-8 (no emitido)
status: borrador
tags: [r0, c1, l3-v8, linea-base, borrador]
updated: 2026-10-04
description: Candidato L3 no emitido sobre V7, con alcance de reconciliación Cowork en §0.8 y aportes pendientes para C1, C2 y D1/R1.
---

# LIBOX_ESPECIFICACION_TECNICA_L3_V8_DRAFT

> **Estado: candidato de C1, no emitido.** La L3 V7 sigue vigente hasta que se
> complete el acto de emisión de C2. El candidato **aún no cierra C1**: faltan
> aportes humanos para defectos concretos del código de zonas sin IA (H-04,
> H-07–H-12), la parte no crítica del SQL que se está preparando y la versión
> final del contrato. Lo que falta para C1, para C2 y para D1/R1 se detalla por
> separado en §0.5, §0.6 y el Anexo C. El código heredado sin hallazgo se
> conserva tal cual y no hay que reescribirlo para emitir.
>
> **Actualización Cowork:** §0.8 incorpora los requisitos candidatos de plazo,
> viabilidad y fianza y delimita qué falta integrar. Las secciones heredadas de
> esquema, FSM y ledger aún no implementan ese flujo; no usar este borrador como
> contrato financiero final. La identidad V8/V9 de emisión se resolverá en C2.
>
> **Decisiones C1 integradas (2026-10-01).** Las decisiones A1–A11, B1–B6, C1–C4
> y D1 que Diego aprobó el 2026-09-30 ([paquete](decisiones-c1.md)) se integran
> en la prosa y las tablas normativas de las secciones afectadas. Donde el código
> heredado preservado contradice una de ellas, la sección lo marca como **legado
> preservado, no listo para emisión en C2**: la regla vigente es la de la prosa y
> el código lo corrige el SQL V8 o el aporte humano. Las propuestas de Cowork no
> ratificadas (fianza, ventana de 48 h) no se convierten en norma.
>
> **Ratificaciones del 04/10:** [registro](decisiones-2026-10-04.md) con Vercel
> para Go, Trigger.dev, Auth administrada, mínimo 1,45 y auditoría general.
> La prosa/contratos y el SQL completo aún deben integrar ese alcance. El CHECK
> protegido heredado conserva 1,25: su adaptación al mínimo nuevo es aporte humano,
> no se modifica en esta actualización. Diego eligió el 04/10 la **garantía del
> sorteo** (antes "fianza") desde la primera entrega y subió el suelo del rango a
> 1,45×; parámetros y adaptación del SQL protegido siguen pendientes. La
> terminología de fianza en la recepción Cowork se conserva como origen.

## 0\. Propósito, alcance y control documental

**Documento:** LIBOX\_ESPECIFICACION\_TECNICA\_L3\_V8\_DRAFT **Versión:** identidad de trabajo V8, borrador DRAFT-8, no emitido **Nivel:** L3 — Architecture, Security, Engineering & QA **Reemplazaría a:** LIBOX Especificación Técnica L3 V7 del canon del repo **Gobernantes de origen:** LBPF V3 (nivel L0) y PRD MVP V9 (nivel L2); la recepción LBPF V4/PRD V10 se reconcilia en §0.8 **Artefactos asociados:** `libox_openapi_L3_V8_DRAFT.yaml` (`2.0.0-draft.3`) · migración C1 completa pendiente **Estado:** borrador candidato

**Identidad en C2.** Confirmar primero si la V8 recibida fue formalmente emitida: si lo fue, la consolidación será V9; si no, se resolverá una única V8. Nombre de archivo, título, pie y versión deben coincidir con esa identidad y Registro/BASELINE. Se retira el frontmatter del wiki y desaparecen las marcas de borrador. El registro ZC permanece como mapa de zonas sin IA. En DP solo quedan decisiones que no condicionan C2, con la fase que sí bloquean. Hasta resolver la emisión, los cuatro lugares conservan `L3_V8_DRAFT` como identidad de trabajo.

**Origen del texto.** Las secciones sin cambio reproducen el contenido de la [L3 V7](../../../linea-base/LIBOX_ESPECIFICACION_TECNICA_L3_V7.md) para que este documento se lea sin ella. La cita solo indica la procedencia. Ninguna regla de este borrador remite a V7 para completarse.

**Fidelidad de la transcripción.** El coordinador ejecutó `scripts/contracts/tests/test_preserved_l3.py` y sus dos pruebas pasan. La primera comprueba que 32 bloques protegidos de V7 (transacciones, motor, funciones y disparadores, entre otros) aparecen completos en este candidato. Solo difieren en líneas vacías y espacios finales. La segunda comprueba que no queda ningún marcador de transcripción sin terminar. Esa evidencia no equivale a una comparación byte a byte del documento completo. Los cambios de forma deliberados son tres: encabezados un nivel más bajos, líneas vacías sin espacios dentro de los bloques y un punto final en algunas líneas en negrita, todo por el lint del wiki. Cualquier edición posterior del candidato exige volver a ejecutar esas pruebas.

**Evidencia complementaria:** el [overlay SQL](cierre-sql.md) pasó tres escenarios locales
en PostgreSQL 17.11 (100/100/104 comprobaciones), sin alterar el código protegido de V7.
No es el SQL V8 completo ni una prueba de Supabase gestionado. El contrato pasa a
`2.0.0-draft.3` con la integración de las decisiones A y C; conserva las 61
operaciones inventariadas más las auxiliares. El contrato tiene 93 operaciones (61 inventariadas y 32 auxiliares), 50 pruebas
contractuales y 13 intercambios del cliente TypeScript verificados localmente. Véase [estado C1](estado-c1.md) para pendientes y alcance.

### 0.0 Changelog

Conforme a la política de control documental de LIBOX, no existen subversiones: todo cambio incrementa la versión completa de V(X) a V(X+1). La marca DRAFT-8 identifica el borrador y desaparece al emitir.

#### Cambios de la versión V8 (borrador)

| Versión | Sección | Qué cambió | Por qué | Decisión que invalida |
| ------- | ------- | ---------- | ------- | --------------------- |
| V8 | §0, pie | Identidad de borrador; PRD MVP V9 en encabezado, §0.1 y pie; se elimina el índice vacío | H-19: el encabezado citaba PRD V8 y el pie PRD V4 | Corrige encabezado y pie de V7 |
| V8 | §0.2, §0.2.1 | OpenAPI `2.0.0-draft.3`; migración C1 completa pendiente. V7 en PG17.11 confirmó H-05, H-06 y semillas vacías; SQL V8 de Cowork es otra entrada | Regla de emisión de §0.2.1 | Deroga la validación de V7 en PG16 como evidencia de la consolidación |
| V8 | §0.3, §0.4 | Backend Go en monolito modular (D-10) y frontend Next.js + TypeScript; Supabase Pro, Vercel Pro para el frontend y Upstash; workflows y hosting del backend en reevaluación; Scalar; Mercado Pago como PSP; Truora en evaluación para KYC y KYB; techo de US$250/mes | H-18; ASS-002 ratificada el 2026-09-29; proveedores y PSP elegidos el 2026-09-30; backend Go decidido el 2026-10-02 (D-10) | Deroga .NET 8 LTS, Next.js 14 y Redis como pieza de la pila |
| V8 | §0.5–§0.7, Anexo C | Mapa de zonas sin IA (ZC), decisiones por fase (DP), mapa H-01–H-19 y criterios de cierre de C1, C2 y D1/R1 | Trazabilidad CD-07; implementación humana de Backlog MVP V3 §1.3; decisión D-05 del programa R0 | Amplía |
| V8 | §1.1 | C-13: HMAC versionado para identificadores de documento | H-14: SHA-256 directo de un DNI se revierte por fuerza bruta | Deroga el SHA-256 directo de V7 §2.2 |
| V8 | §1.3 | Doce tablas particionadas y particiones iniciales obligatorias | H-05: sin particiones creadas, todo `INSERT` falla | Corrige la lista de ocho tablas y la regla de alarma |
| V8 | §1.4 | `GRANT` explícitos por rol y tabla; login técnico separado; roles del proveedor sin acceso a dominio | H-06: cinco `REVOKE` sin ningún `GRANT` no protegen nada | Amplía |
| V8 | §2.2 | `auth_identities` y `app_sessions` sustituyen a `credentials` y `refresh_tokens`; versión de clave del HMAC | Autenticación en Supabase Auth; H-14 | Deroga la contraseña argon2id almacenada por LIBOX |
| V8 | §3.16.1, §14.3 | INV-38 exige dos `ADMIN_SUPER` activos; los casos de prueba se corrigen; el código heredado queda en ZC-11 | H-07 y H-09 | Deroga el caso "revocar al penúltimo: admitido" |
| V8 | §5 | Requisitos de baliza, semilla cifrada y vectores; el código heredado queda en ZC-13 | H-10, H-11 y H-12 | Amplía; no corrige código |
| V8 | §6 | Marcado ZC-14; H-01–H-03 quedan registrados como pendientes según D-05; H-04 requiere aporte humano | La política contable necesita confirmación [LEGAL→ABOGADO] | Ninguna: no decide el ledger |
| V8 | §7.3–§7.6 | Contrato de sesión sobre Supabase Auth; DNI, evidencias, transporte y límites de frecuencia | Nota de seguridad C1; H-14; H-17 | Deroga la tabla de autenticación de V7 |
| V8 | §8 | Respuesta de error sin `details`; cinco códigos genéricos del contrato | Contrato C1 | Deroga `details` en la respuesta pública |
| V8 | §11 | Base `/api/v2`; `Money` con importe en cadena; OpenAPI 3.1 con las 61 operaciones del inventario y las auxiliares de cierre-contratos; webhook de Mercado Pago | H-13; `Money` ratificado el 2026-09-30 | Deroga el importe como entero JSON para el contrato V8 |
| V8 | §12.6–§12.10 | Ejecutor de los 30 trabajos, despacho del outbox cada 10 s, reintentos, consola, pago tardío y baliza tardía | H-12, H-16; D-08 del programa R0 | Amplía |
| V8 | §13.5–§13.7 | RPO/RTO, copias, restauración, observabilidad y gasto | H-15 | Amplía |
| V8 | §14.8–§14.9 | Pruebas F1–F7; roles, particiones, HMAC, restauración y abuso | D-08 del programa R0 | Amplía |
| V8 | Anexos A–C | Propiedad humana de migraciones, materias legales nuevas y criterios de cierre de C1, C2 y D1/R1 | — | Amplía |
| V8 | §11.7, §12.5 | Webhook de Mercado Pago: firma sobre el manifiesto, no sobre el cuerpo; el cuerpo no es autoritativo; consulta autenticada | Mercado Pago elegido el 2026-09-30 | Amplía; el procedimiento heredado se conserva |
| C1 | §0, §0.6, §0.8 | Reconciliación Cowork: 27 grupos, requisitos candidatos de plazo/viabilidad/fianza, contrato comprador y dependencias; identidad de emisión pendiente | Revisión independiente Codex/Opus y autorización de actualizar el trabajo | No revoca acuerdos C1 ni ratifica valores nuevos |
| C1 | §4.1, §7.1–§7.3, §11.5 | Firmas por `action_code`, cofirma V2, actor de observación, aprobadores por etapa P-C, decisión KYB, rechazos manuales en la tabla FSM, motivos de moderación, INC-07/INC-11 en ejecución, reautenticación de 5 min y atestación con `SignatureRequest` | Decisiones A1–A11 de Diego, 2026-09-30 | Deroga la fila única "Etapas P-C", el actor "Verificador", `second_signer_id` en el cuerpo de la atestación e INC-11 en asignación |
| C1 | §1.1, §1.3, §1.4, §7.3, §7.4 | Clases de privilegios y seis tablas `reservado_humano`; logins por componente; `pg_cron`; DEFAULT en los doce padres y procedimiento manual; retención B6; cifrado AWS KMS con compatibilidad Supabase obligatoria | Decisiones B1–B6 y B1-bis | Amplía; el código de `journal_lines` y de las seis tablas sigue siendo humano |
| C1 | §2.1, §2.4, §3.1, §3.3, §5, §10 | Plazo de T1 con mínimo pendiente, duración propia de T7 sin solape, `ticket_price` fijado por el organizador, MVP solo `PAID`, `cost_kind` inicial, retirada de `LIVE`, categorías P-C y drand quicknet | Decisiones C1–C4 y D1 | Deroga `LIVE` como capacidad y `FREE_ENTRY`/`PROMOTIONAL` en el MVP |

#### Cambios de la versión V7

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

La fila "Instrumenta H-07" del changelog de V7 usa una numeración de hipótesis del producto, no la de hallazgos técnicos H-01–H-19 de §0.7.

#### Cambios de la versión V6

| Versión | Sección | Qué cambió                                                                                            | Por qué                                                                                               | Decisión que invalida |
| ------- | ------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | --------------------- |
| V6      | §3.16   | `subrole_grant_matrix` con techo de privilegio, y disparador que impide otorgar por encima del propio | La creación de usuarios era exclusiva de un rol. Sin techo, delegar produciría escalada de privilegio | Amplía                |
| V6      | §3.16   | `internal_account_suspensions`: suspensión inmediata y distribuida, restauración concentrada          | Revocar acceso debe ser rápido; concederlo no                                                         | Amplía                |
| V6      | §3.16   | Disparador `assert_min_super_admins`: **mínimo dos titulares activos**                                | INV-38. La pérdida del único titular produce bloqueo total sin recuperación                           | Amplía                |
| V6      | §2.4    | Migración 026 crea el **administrador semilla** con credencial de un solo uso                         | No existía ruta de arranque de la administración                                                      | Amplía                |
| V6      | §10.1   | **Proveedores concretos y límites de capacidad** en la configuración de mercado                       | Los adaptadores no nombraban proveedor y no había ningún tope declarado                               | Amplía                |
| V6      | §14.3   | Casos de prueba de escalada de privilegio y de mínimo de administradores                              | Un control que no se prueba contra el caso que debe impedir no es un control                          | Amplía                |

#### Cambios de la versión V5

| Versión | Sección | Qué cambió                                                                                     | Por qué                                                                                                                                                                         | Decisión que invalida          |
| ------- | ------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| V5      | §2.4    | `clients.tax_id` **pasa a admitir nulo**, con restricción que lo exige solo a persona jurídica | La columna era obligatoria y **bloqueaba el alta del organizador persona natural**, un segmento declarado en L1. Es un defecto que solo aparece al intentar dar de alta el caso | Deroga la obligatoriedad de V4 |
| V5      | §2.4    | Restricciones de régimen: identificación por documento, titular único y unicidad extendida     | Los dos regímenes tienen acreditación distinta y el esquema no los distinguía                                                                                                   | Amplía                         |
| V5      | §2.4    | `fee_exceptions`, con categorías tipificadas y segunda firma                                   | Sustituye a la ambigüedad de *por acuerdo* de V4. Una excepción sin criterio objetivo es tarifa negociada con otro nombre                                                       | Amplía                         |
| V5      | §2.4    | `ck_fee_exception_ceiling`: ninguna excepción supera el techo del mercado                      | INV-37 se impone en el esquema, no en el procedimiento                                                                                                                          | Amplía                         |
| V5      | §14.3   | Casos de prueba de régimen de organizador y de techo de excepción                              | Un defecto que solo aparece al intentar el caso exige prueba que lo intente                                                                                                     | Amplía                         |

#### Cambios de la versión V4

| Versión | Sección | Qué cambió                                           | Por qué                                                                                                       | Decisión que invalida |
| ------- | ------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | --------------------- |
| V4      | §3.1    | **Tablas** `fee_schedules` **y** `client_fee_levels` | La escala de progresión de comisión de PRD MVP V8 §1.3.1 necesita nivel por organizador e historial auditable | Amplía                |
| V4      | §10.1   | `fee_schedule` en la configuración por mercado       | Los umbrales son parámetro de negocio, no constante de código                                                 | Amplía                |
| V4      | §12.6   | Trabajo `recompute-client-fee-level`                 | El nivel se recalcula sobre volumen liquidado móvil de 12 meses                                               | Amplía                |
| V4      | §14.2   | Prueba de propiedad `prop_fee_frozen_at_publish`     | Un cambio de nivel no puede alterar sorteos ya publicados                                                     | Amplía                |

**Sin cambio en** `raffles`**.** `libox_fee_bp` ya era un valor por sorteo con 2000 por defecto: la tasa variable estaba soportada desde V2.

#### Cambios de la versión V3

| Versión | Sección           | Qué cambió                                                                              | Por qué                                                                                                                                                                                                                             | Decisión que invalida |
| ------- | ----------------- | --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| V3      | Pie del documento | **Referencia final corregida a PRD MVP V8**                                             | El encabezado declaraba correctamente su gobierno y el pie contradecía al propio control documental apuntando a una versión anterior                                                                                                | Corrige el pie de V2  |
| V3      | §0.2              | `libox_openapi_L3_V7.yaml` **emitido como artefacto físico** `libox_openapi_L3_V7.yaml` | El PRD lo declara bloqueante de toda la construcción del cliente, y la regla BR-03 del backlog exige que los contratos y tipos se **generen**. Sin archivo no hay generación de tipos, ni pruebas de contrato, ni servidor simulado | Amplía                |
| V3      | §0.2.2            | **Verificación de correspondencia entre agregados del PRD y tablas reales**             | Cuatro entidades divergían entre L2 y L3                                                                                                                                                                                            | Amplía                |
| V3      | §3.4              | Comentario de `orders`: **una orden, un sorteo**                                        | Regla RN-06-ter del PRD MVP V9, ahora explícita en el esquema                                                                                                                                                                       | Amplía                |
| V3      | §3.5              | Comentario de `tickets`: **el pool es derivado, no persistido**                         | Regla RN-06-quater                                                                                                                                                                                                                  | Amplía                |
| V3      | Todo              | Nomenclatura de versiones normalizada sin dígito menor                                  | La política documental no admite subversiones                                                                                                                                                                                       | Amplía                |

#### Cambios de la versión V2

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

### 0.1 Qué es este documento

Este documento es el **nivel L3** de la arquitectura documental de LIBOX. Contiene los mecanismos de implementación que el PRD MVP V9 declara y referencia pero no especifica: esquema de base de datos, contratos de interfaz, máquinas de estado implementables, algoritmos, plan de cuentas, catálogos de errores y eventos, matriz de control de acceso y estructura de configuración por mercado.

| Nivel  | Documento                   | Responde                                |
| ------ | --------------------------- | --------------------------------------- |
| L0     | LBPF V3                     | Por qué una experiencia es admisible    |
| L1     | Product Strategy            | Qué se persigue y para quién            |
| L2     | PRD MVP V9                  | Qué existe y bajo qué reglas de negocio |
| **L3** | **Este documento**          | **Cómo se implementa**                  |
| L4     | Design System, UI Kit, Copy | Cómo se ve y cómo se dice               |

**Regla de precedencia.** Si este documento contradice al PRD MVP V9 en una regla de negocio, prevalece el PRD. Si el PRD contradice al LBPF V3 en materia conductual, prevalece el LBPF (R-01). Este documento nunca inventa reglas de negocio: las implementa. En particular, conserva INV-38 del PRD (mínimo dos `ADMIN_SUPER` activos), las segundas firmas y las incompatibilidades de subrol. La suspensión de la revisión humana del repositorio no debilita ninguno de estos controles del producto.

### 0.2 Artefactos contenidos

| §   | Artefacto                                                    | Artefacto físico asociado |
| --- | ------------------------------------------------------------ | ------------------------- |
| 1–3 | Convenciones y esquema de base de datos                      | Migración C1 completa: **pendiente**. Componer V7, overlay no crítico, cambios aprobados y aportes humanos de §0.5/§0.8; el SQL V8 recibido no la sustituye |
| 4   | Máquina de estados del sorteo                                | —                         |
| 5   | Motor de sorteo, serialización canónica y vectores de prueba | —                         |
| 6   | Plan de cuentas y transacciones canónicas                    | —                         |
| 7   | Matriz de control de acceso                                  | —                         |
| 8   | Catálogo de errores                                          | Enumeración `Error.code` del OpenAPI |
| 9   | Catálogo de eventos                                          | —                         |
| 10  | Estructura de configuración por mercado                      | —                         |
| 11  | Contratos de interfaz                                        | [`libox_openapi_L3_V8_DRAFT.yaml`](libox_openapi_L3_V8_DRAFT.yaml): `2.0.0-draft.3`. Contiene las 61 operaciones del inventario y operaciones auxiliares documentadas en [cierre de contratos](cierre-contratos.md); el conteo final lo fija el coordinador. Se emite como `libox_openapi_L3_V8.yaml` |
| 12  | Concurrencia, idempotencia y trabajos programados            | —                         |
| 13  | Observabilidad, operación y recuperación                     | —                         |
| 14  | Estrategia de pruebas                                        | —                         |

El artefacto OpenAPI declara `x-target-document: L3 V8 (no emitido)` y `x-implements: PRD MVP V9`. Al emitir se sustituyen esos metadatos por la identidad definitiva.

### 0.2.1 Validación del esquema

**Evidencia disponible (informada por el coordinador).** PostgreSQL 17.11 ejecutó intacto V7 (`libox_schema_L3_V7.sql`): 135 tablas y cero errores. Confirma H-05 (12 padres sin particiones), H-06 (sin `GRANT`) y H-08 (semillas vacías). El overlay no crítico posterior pasó 100/100/104 comprobaciones (§0, [cierre SQL](cierre-sql.md)); sigue sin ser la migración completa de C1. No se probó Supabase gestionado. El SQL V8 de Cowork se ejecutó por Opus en PG16.13 y aceptó contraejemplos de cobertura/mínimo: esa evidencia no valida la consolidación en PG17 (§0.8).

**Regla de emisión.** Ninguna versión se emite sin que su esquema se ejecute con cero errores **y sin que sus restricciones se prueben contra casos que deben fallar**. Un esquema que compila no es un esquema que protege. Para V8, la comprobación del esquema candidato en C1 es esta:

1. Migración completa, en orden (Anexo A), sobre PostgreSQL 17 vacío. Si falla, la alternativa se decide en DP-09.
2. Inserción en las doce tablas particionadas y paso al mes siguiente (§1.3).
3. Pruebas negativas con las credenciales reales de cada rol, no con el propietario (§1.4, §14.9).
4. Pruebas negativas de los defectos con aporte humano: INV-38 y reactivación (H-07, H-09), incompatibilidades en asignación y transición única (H-08), y cuadre del asiento (H-04).
5. Semillas presentes: mercado PE, transiciones, `raffle_type_rules`, incompatibilidades, matriz de otorgamiento y arranque de administración. Las cuentas por moneda las siembra su dueño humano.

Las pruebas de dominio contra el backend, contra el proveedor real y los ensayos de restauración pertenecen a D1/R1 y no condicionan C1 (Anexo C).

**Defecto de lógica de tres valores.** Un `CHECK` que evalúa a nulo se considera satisfecho. Toda restricción condicional debe incluir comprobaciones explícitas de `NOT NULL`, como hace `ck_raffles_base_type`.

### 0.2.2 Correspondencia entre agregados y tablas

El criterio de cierre del PRD exige que toda tabla declarada tenga columnas reales. Toda entidad declarada en PRD MVP V9 §3.1 existe como tabla en este documento, o está marcada expresamente como derivada.

| Entidad del PRD      | Estado en V8                            | Motivo                                                                                                                                              |
| -------------------- | --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `processed_webhooks` | **Renombrada** a `processed_psp_events` | El nombre debía coincidir con la tabla de deduplicación real                                                                                        |
| `sessions`           | **Sustituida** por `app_sessions`       | V8 separa la sesión del proveedor de identidad de la sesión aplicativa, que es la que LIBOX comprueba en cada acceso interno (§7.3)                 |
| `order_items`        | **Derogada**                            | Una orden corresponde a un solo sorteo (RN-06-ter). Su desglose de comisión es único por definición                                                 |
| `ticket_pools`       | **Derogada**                            | El pool es el conjunto de tickets emitidos en el instante del congelamiento. Su fotografía inmutable vive en la instantánea del documento de prueba |

**Regla de emisión ampliada.** Ninguna versión se emite sin que la correspondencia entre los agregados del PRD y las tablas de este documento sea completa.

### 0.3 Pila tecnológica

ASS-002 fue ratificada por los socios el 2026-09-29 con backend TypeScript. **Diego decidió el 2026-10-02 implementar el backend en Go (D-10)**, como monolito modular; el frontend sigue en Next.js y TypeScript. Diego confirmó los proveedores el 2026-09-30. Las herramientas de Go, el hosting del backend y el ejecutor de trabajos son propuestas pendientes de confirmar ([adaptación a Go](../2026-10-02-r0-backend-go-design.md)). La elección fija la arquitectura, pero no contrata servicios, no acredita capacidad y no garantiza una factura fija.

| Capa | Decisión | Nota |
| ---- | -------- | ---- |
| Lenguaje y runtime | Backend: Go (versión fijada en D1). Frontend: TypeScript estricto sobre Node.js | Node se fija en D1 contra la versión de Next.js instalada y soportada |
| Aplicación | Monolito modular en Go: una imagen con modo API HTTP y modo worker, y módulos de dominio (órdenes, pagos, boletos, sorteo y liquidaciones) que invocan los endpoints y los trabajos. Next.js 16 con App Router solo para la interfaz, que consume la API REST | Las reglas no se duplican en endpoints, trabajos ni cliente. Propuesta: `net/http` + oapi-codegen, pgx + sqlc, sin ORM. Versiones en D1 |
| Base de datos | PostgreSQL gestionado en Supabase Pro; cómputo Small y PITR de 7 días para R1 | Autoridad sobre dinero e inventario. Major 17: el esquema V7 corre en 17.11 local; falta el esquema V8 y probar en Supabase (DP-09) |
| Conexiones | Migraciones por conexión directa con el rol migrador. El backend Go es un proceso persistente con pool acotado; si el ejecutor usa LISTEN/NOTIFY, necesita conexión directa o pooler en modo sesión | Presupuesto de conexiones (API, worker, servicios de Supabase, migraciones y despliegues) frente al límite de Small, por fijar en D1 |
| Workflows | **En reevaluación por D-10.** Propuesta: River (cola sobre PostgreSQL) en el worker Go, con encolado en la misma transacción que el dato de negocio. Alternativa: Trigger.dev con tareas TypeScript. `create-next-partitions` corre en `pg_cron` dentro de la base (B3) | Encolar una vez no garantiza un efecto patrimonial único: la idempotencia y la ejecución única siguen siendo zona crítica |
| Ticker del outbox | Propuesta: el worker Go despacha cada 10 s. Alternativa: Supabase Cron cada 10 s contra un endpoint privado | El cron de Vercel no alcanza 10 s: su intervalo mínimo es un minuto |
| Hosting | Frontend: Vercel Pro. Backend Go: pendiente; propuesta Fly.io con federación OIDC hacia AWS para KMS, o Render con credencial exclusiva y rotada | Vercel no aloja un proceso Go persistente. La región del backend coincide con la de Supabase |
| Identidad | Supabase Auth con TOTP. Roles, permisos por recurso, incompatibilidades y sesión aplicativa los gestiona LIBOX | §7.3 |
| Objetos | Supabase Storage privado, más una copia independiente | Destino de la copia en DP-10 |
| Límites de frecuencia | Upstash (pago por uso) | **Nunca autoritativo sobre dinero ni inventario** (§12.1) |
| Correo transaccional | Pendiente (DP-11) | Presupuestado como Resend Pro |
| Proveedor de pagos | Mercado Pago, elegido por Diego el 2026-09-30, detrás de un adaptador por mercado | Checkout Pro es la modalidad propuesta, sin confirmar. Acceso a sandbox sin confirmar. No se han creado cuentas ni usado credenciales ([nota](mercado-pago.md)) |
| Verificación KYC y KYB | Truora priorizado para evaluación | No contratado. La referencia de Checks estándar lista `company` como N/A para Perú: KYB peruano sin confirmar. Sumsub y Veriff siguen como alternativas ([evaluación](truora-evaluacion.md)). Costo fuera del techo de infraestructura |
| Documentación de API | Scalar sobre el mismo artefacto OpenAPI | Decisión D-07 del programa R0 |
| Importes en código | `int64` en Go, `bigint` en el frontend TypeScript, `BIGINT` en PostgreSQL y cadena decimal en JSON | Nunca `number` ni punto flotante (C-06, §11.1) |
| Desarrollo local | PostgreSQL efímero para migraciones y pruebas | La herramienta se fija en D1 |

Neon queda como alternativa si falla la validación del proveedor elegido. Ninguna herramienta de código queda ratificada por esta elección; Drizzle deja de aplicar al backend. `src/` y el futuro directorio del backend siguen congelados hasta D1.

### 0.4 Presupuesto de infraestructura

Techo indicado por Diego: US$250 al mes. Objetivo operativo: US$215 antes de impuestos, con alertas proyectadas a US$175, US$200 y US$215. El escenario R1 ilustrativo suma US$208,39 (Supabase Small con PITR US$130, Vercel US$20, Trigger US$23,39 con 1 s de media por trabajo, correo US$20, límites US$5 y reserva de copias US$10). Con 5 s de media, Trigger sube a US$77,18 y el total **supera el techo**. El despacho añade 259.200 llamadas HTTP al mes, cuyo consumo no se ha medido. **Con D-10:** sin Trigger.dev (−23,39) y con hosting Go (+25 a +50) y KMS (+2 a +5), el escenario R1 queda en unos US$212–240: bajo el techo, pero desde unos US$215 por encima del objetivo. Se elige hosting cerca del extremo inferior y no se recorta PITR ni la copia independiente ([adaptación a Go](../2026-10-02-r0-backend-go-design.md)). No se activa un corte ciego de consumo que deje pagos aceptados sin conciliar. Si el gasto proyectado supera el techo, se frenan las ventas nuevas de forma operativa y se conserva la recuperación. Pagos, KYC, SMS y asesoría legal se presupuestan aparte.

### 0.5 Mapa de zonas sin IA (ZC)

Backlog MVP V3 §1.3 reserva a implementación humana, con propiedad fija, cinco zonas: motor de sorteo, serialización canónica y verificación; asientos contables y transacciones canónicas; concurrencia (reserva de inventario, bloqueo de saldo y ejecución única); comprobaciones de incompatibilidad de subrol en ejecución; cálculo de comisión e impuesto incluido. También cuentan como código de dinero y concurrencia las restricciones de rango de recaudación, de régimen económico y de campaña con cupo atómico. La clasificación depende del comportamiento.

Este candidato **no genera ni corrige** código de esas zonas. Los bloques heredados llevan una marca `[ZC-nn]` y se conservan como estaban en V7 (§0, fidelidad). La marca no obliga a reescribir el bloque: indica que cualquier cambio o implementación futura es humana. Solo los defectos registrados que se listan abajo exigen un aporte humano para cerrar C1. Diego (`@DianCotrina`) es el dueño actual. La suspensión de la revisión humana obligatoria no cambia la prohibición de generar este código.

Estados:

- **Preservado.** Código heredado sin hallazgo registrado. Se emite tal cual; sus pruebas de dominio corresponden a D1/R1.
- **Aporte C1.** Defecto registrado que exige código, DDL o valores escritos por humanos antes de cerrar C1.
- **Pendiente D-05.** Hallazgo contable que la decisión D-05 del [programa R0](../2026-09-25-habilitar-r0-design.md) deja registrado y pendiente de confirmación contable. No condiciona C1 ni C2; debe resolverse antes de mover dinero real en R1.

| ID | Ubicación | Zona | Estado | Qué falta y cuándo |
| -- | --------- | ---- | ------ | ------------------ |
| ZC-01 | §2.5 `fee_schedules`, `fee_exceptions` | Comisión; segunda firma | Preservado | Pruebas de techo y firma en D1 |
| ZC-02 | §3.1 `raffles` | Comisión, inventario, régimen económico, rango de recaudación | Preservado | Casos de §14.3 en D1 |
| ZC-03 | §3.2 `assert_registrable_regime`, `prize_valuations` | Régimen económico; segunda firma | Preservado | Caso `ERR_REGISTRABLE_NO_ESCROW` en D1 |
| ZC-04 | §3.4 idempotencia, órdenes, pagos, deduplicación | Dinero y ejecución única | Preservado. H-16 es política (§12.9), no código | F1, F2 y F7 en R1 |
| ZC-05 | §3.5 tickets y asignación de número | Inventario y concurrencia | Preservado | F5 y `prop_no_number_reuse` en R1 |
| ZC-06 | §3.6 campañas, planes promocionales, garantías | Cupo atómico y régimen económico | Preservado | Cupo bajo concurrencia en D1/R1 |
| ZC-07 | §3.6 compromisos, ejecuciones, ganadores, pruebas, re-sorteos | Motor y ejecución única | **Aporte C1** por H-12 | DDL humano para persistir la semilla cifrada (§5.8); F6 en D1/R1 |
| ZC-08 | §3.9 `settlements` | Dinero | Preservado; depende de D-05 | Casos de liquidación antes de dinero real en R1 |
| ZC-09 | §3.10 contabilidad | Asientos contables | **Aporte C1** por H-04 | Rechazo de asiento desbalanceado, cuenta inexistente y moneda distinta |
| ZC-10 | §3.11 saldo de reembolso | Bloqueo de saldo | Preservado | `conc_refund_credit`, L-02 y L-03 en D1/R1 |
| ZC-11 | §3.16.1 disparadores de otorgamiento | Privilegio y concurrencia de titulares | **Aporte C1** por H-07, H-08 y H-09 | INV-38 con dos titulares, reactivación con los controles del `INSERT`, disparador de incompatibilidades en asignación y arranque (DP-16) |
| ZC-12 | §4.2 punto único de transición | Concurrencia; incompatibilidades en ejecución | **Aporte C1** por H-08 | Procedimiento humano y prueba de que no hay otra ruta de `UPDATE` |
| ZC-13 | §5.2–§5.7 motor, serialización, verificación | Motor de sorteo | **Aporte C1** por H-10, H-11 y H-12 | Especificación cerrada (DP-04), verificador sin ambigüedad y salidas de los vectores calculadas por dos implementaciones humanas independientes |
| ZC-14 | §6 plan de cuentas y transacciones | Asientos, comisión e impuesto | **Pendiente D-05** por H-01, H-02 y H-03 | Confirmación contable y T-03 [LEGAL→ABOGADO], antes de dinero real en R1 |
| ZC-15 | §12.2–§12.5 reserva, emisión, idempotencia, webhooks | Concurrencia y ejecución única | Preservado. La emisión hereda H-01 (D-05) | F1–F5 y F7 contra PostgreSQL y el sandbox de Mercado Pago en R1 |
| ZC-16 | §3.7, §3.8 y §7.2 INC-06–INC-09 e INC-11 | Incompatibilidades en ejecución (INC-07 e INC-11 solo en ejecución, A11) y política de segunda firma por `action_code` (A1) | Preservado; sin código en V7: es lógica de servicio | Implementación humana y casos INC de §14.3 en D1 |
| ZC-17 | §1.4 clase `reservado_humano`: `spending_limits`, `spending_limit_changes`, `self_exclusions`, `operation_register`, `transfer_costs`, `raffle_milestones` | Bloqueo de saldo, inventario, importes y AML (B1) | **Reclasificadas** por B1; sin `GRANT` en la capa no crítica | DDL, ACL y pruebas humanas antes de que la aplicación escriba en ellas |
| ZC-18 | §1.3 partición DEFAULT de `journal_lines` | Asientos contables | Regla decidida (B5); código pendiente | Partición DEFAULT, ACL de `libox_append` (solo `INSERT`) y alarma, por implementación humana |

Ningún valor esperado de sorteo, vector criptográfico ni resultado contable se fabrica para hacer pasar una prueba.

### 0.6 Decisiones por fase (DP)

La columna "Bloquea" indica la primera fase que no puede cerrarse sin esa decisión. Una decisión que bloquea R1 no condiciona C1 ni C2.

| ID | Decisión que falta | Bloquea | Dueño |
| -- | ------------------ | ------- | ----- |
| DP-01 | ASS-001: quién custodia el dinero y con qué figura [LEGAL→ABOGADO] | R1 y R2 (dinero real) | Socios y abogado |
| DP-02 | Momento en que se reconocen comisión, neto e impuesto (T-04, T-05, T-06). Propuesta registrada: "liquidación elegible", sin confirmar [LEGAL→ABOGADO] | R1, por D-05 | Dueño contable, sin designar; Diego |
| DP-03 | Asiento T-03: devolución al medio de pago original y movimiento de `cash_clearing` y `psp_clearing` | R1, por D-05 | Dueño contable; implementación de Diego |
| DP-04 | drand quicknet ratificada; faltan suite/codificación de ronda y valor, formato del verificador y valores esperados | C1 (H-10/H-11) | Dueño del motor (Diego) |
| DP-05 | Baliza tardía: qué pasa tras el incidente de los 30 minutos, reanudar o cancelar | C1 (programa R0: timeout de baliza) | Dueño del motor |
| DP-06 | AWS KMS con cifrado de sobre está elegido para datos personales (B1-bis, §7.4). Falta decidir el servicio de la semilla cifrada, la rotación de la clave maestra y de la clave HMAC, el recifrado y la restauración | C1 para la semilla (H-12); R1 para la rotación | Diego |
| DP-08 | Mercado Pago: confirmar la modalidad (Checkout Pro propuesta), el acceso a sandbox y la aceptación comercial del caso de uso | R1 | Diego |
| DP-09 | Major de PostgreSQL: 17 si el esquema V8 completo pasa en 17 y en Supabase; si no, la versión soportada por el proveedor o Neon | C1 para el esquema local; R1 para Supabase | Diego |
| DP-10 | Copia independiente de objetos (R2 o S3), versionado, Object Lock y retención por clase de documento [LEGAL→ABOGADO] | R1, antes de documentos reales | Diego y abogado |
| DP-11 | Proveedor de correo transaccional | R1 | Diego |
| DP-12 | B6 integrada en §1.3: `risk_events` y `audit_access_events` indefinidas. Falta el plazo de `psp_events` y `operation_register`; nada se borra hasta aprobarlo [LEGAL→ABOGADO] | R1 | Diego y abogado |
| DP-13 | Re-sorteo: política y causales del comando `redraw` | Habilitar `redraw` en D1/R1 | Dueño del motor |
| DP-16 | Arranque del primer y segundo `ADMIN_SUPER` conforme al PRD, sin cuentas ficticias en producción | C1 (parte del aporte de ZC-11) | Diego |
| DP-19 | Correlación con el doc 20: números CHANGE y DEC de este candidato y alta del DEC de ASS-002 | C2 | Diego |
| DP-20 | KYC y KYB: resultado de la evaluación de Truora. KYB peruano con Checks estándar figura como N/A y debe confirmarse por escrito; si no encaja, Sumsub o Veriff | R1 (el contrato C1 es neutral respecto del proveedor) | Diego |
| DP-21 | I-01–I-09 del [cierre de contratos](cierre-contratos.md) decididos por A1–A11 y C1–C4 e integrados en §4.1, §7 y §11 de este candidato; I-10/I-11 resueltos. Quedan los datos de DP-24 a DP-27 | C1 para contrato; documentos antes de habilitar P-C | Diego; P-C/gate legal [LEGAL→ABOGADO] |
| DP-22 | Resolver deltas Cowork: T1/fianza, mínimo/caja, ventanas, estados, contrato comprador y parámetros, según §0.8 | C1 para especificación/artefactos coherentes; dinero real en R1 | Diego; contabilidad y abogado según materia |
| DP-23 | Confirmar emisión V8 recibida, identidad siguiente y correlación de CD-11/Registro/artefactos | C2 | Diego |
| DP-24 | T1 (C1): umbral del mínimo vendido (porcentaje o boletos) y quién lo fija, premio que se entrega al alcanzarlo y aviso al comprador. La regla de estabilidad ya está aprobada (§3.1) | Publicar T1; C1 para el contrato | Diego [LEGAL→ABOGADO] |
| DP-25 | Valores de `charge_kind` y `macrozone` (C4) | C1 para los enums del SQL V8 y el contrato | Diego |
| DP-26 | Cifrado (B1-bis): alcance de Supabase Auth, inventario de datos personales (documentos, logs, exportaciones), excepción de email/teléfono en `auth.users` (pendiente, no autorizada), vistas seudonimizadas y caché de claves de datos | C1 para el SQL V8 de columnas cifradas; R1 para la operación | Diego |
| DP-27 | Lista cerrada de documentos por etapa P-C (A8): clave, descripción y obligatoriedad, validada por el abogado. Fecha objetivo por acordar; se revisa en cada revisión de avance de C1 | Habilitar P-C | Diego y [LEGAL→ABOGADO] |

Los números DP-07, DP-14, DP-15, DP-17 y DP-18 ya no figuran como decisiones abiertas: pasaron a propuestas técnicas del candidato (abajo). DP-08 dejó de ser la elección del PSP porque Mercado Pago ya está elegido.

**Propuestas técnicas del candidato.** Las siguientes forman parte del texto normativo del candidato. Diego las ratifica **en un solo acto** en C2, no una por una. Si alguna se rechaza, se corrige el candidato antes de emitir.

- P-01, sesión: `auth_identities`, `app_sessions` y el contrato de §7.3, con puente entre la reutilización de testigos del proveedor y el evento de riesgo.
- P-02, pago tardío: sin ticket, excepción y conciliación (§12.9). La devolución contable queda sujeta a DP-03.
- P-03, espera de baliza: alarma a los 5 minutos e incidente a los 30 (§12.10), sin otra ronda ni sorteo manual.
- P-04, recuperación: RPO ≤ 5 min y RTO ≤ 4 h como objetivos de R1, sujetos a ensayo (§13.5).
- P-05, HMAC versionado para documentos (C-13, §7.4).
- P-06, límites de frecuencia, CSP y almacenamiento de evidencias (§7.5, §7.6).
- P-07, operaciones auxiliares del contrato marcadas `x-authorization-status: proposed` (§11).
- P-08, códigos de error que lanzan los disparadores y aún no figuran en §8.2. Los fija el dueño del contrato y se sincronizan con `Error.code` al consolidar.
- P-09, partición por defecto: B4–B5 la aprueban en los doce padres y §1.3 la integra como norma. La DEFAULT de `journal_lines` es código humano (ZC-18).

### 0.7 Mapa de hallazgos H-01–H-19

Origen: [hallazgos técnicos de L3](../2026-09-25-revision-sistema-hallazgos-l3.md) y [registro local CD-07](cambios.md). Estado dentro de este borrador:

| Hallazgo | Dónde se trata | Estado en el candidato | C1 exige | Después (D1/R1) |
| -------- | -------------- | ---------------------- | -------- | ---------------- |
| H-01 | §6.3, §6.4, §12.3 | Registrado, pendiente por D-05. ZC-14, DP-02 | Nada más que dejarlo registrado | Dictamen contable antes de dinero real |
| H-02 | §6.2 | Registrado, pendiente por D-05. ZC-14, DP-03 | Nada más que dejarlo registrado | T-03 y prueba en el sandbox del PSP |
| H-03 | §6.3 | Registrado, pendiente por D-05 [LEGAL→ABOGADO] | Nada más que dejarlo registrado | Confirmación contable y tributaria |
| H-04 | §3.10 | Aporte C1. ZC-09 | Código humano que rechace asiento desbalanceado, cuenta inexistente y moneda distinta | Propiedad del ledger en D1 |
| H-05 | §1.3, Anexo A | Norma incorporada; overlay no crítico probado en 11/12 padres; ledger pendiente | SQL aplicado a base vacía, inserción y paso de mes en las doce tablas | Rotación y retención en R1 |
| H-06 | §1.4 | Norma incorporada con las clases de B1 y logins de B2; ACL no crítica probada; seis tablas reclasificadas y ledger pendientes de aporte humano (ZC-17, ZC-18) | `GRANT` por clase y pruebas negativas con cada credencial | Roles reales del proveedor en R1 |
| H-07 | §3.16.1, §14.3 | Norma y casos corregidos. Aporte C1 (ZC-11) | Código humano de INV-38 con dos titulares, suspensiones y concurrencia | — |
| H-08 | §4.2, §3.16.1, Anexo A | Aporte C1 (ZC-11, ZC-12); semillas no críticas en la capa SQL | Procedimiento de transición, disparador de incompatibilidades y semillas con comprobación de cobertura | — |
| H-09 | §3.16.1 | Norma incorporada. Aporte C1 (ZC-11) | Reactivación con los mismos controles que `INSERT` | — |
| H-10 | §5.7 | Aporte C1 (ZC-13) | Salidas de cada vector calculadas por dos implementaciones humanas independientes | Ejecución en cada integración |
| H-11 | §5.6, §5.8 | Aporte C1 (ZC-13), DP-04 | Especificación cerrada y verificador sin ambigüedad | Prueba pública independiente |
| H-12 | §5.3, §5.8, §12.10 | Requisitos y P-03 incorporados. Aporte C1 (ZC-07), DP-05, DP-06 | DDL humano de semilla cifrada y resolución tras la espera | Restauración de clave y datos; F6 |
| H-13 | §11 y OpenAPI | 61 operaciones del inventario más auxiliares documentadas; `Money` en cadena; `/api/v2` | Versión `2.0.0-draft.3` con pruebas estructurales. Alcanzar el conteo no lo cierra | Comportamiento contra backend y proveedor reales |
| H-14 | §1.1 C-13, §2.2, §7.4 | Norma y DDL propuesto (P-05), sin ejecutar | Ejecución del DDL no crítico | Vectores de normalización y rotación; ausencia de DNI en registros |
| H-15 | §13.5 | Objetivos propuestos (P-04) | Nada más que la norma | Ensayo integral cronometrado y conciliado |
| H-16 | §12.9 | Política propuesta (P-02) | Nada más que la norma | F7 en el sandbox; asiento de devolución sujeto a DP-03 |
| H-17 | §7.6 | Norma incorporada (P-06) | Nada más que la norma | Pruebas de abuso con umbrales medidos |
| H-18 | §0.3 | Incorporado. DP-09 | Esquema V8 en PostgreSQL 17 | Supabase y CI Go y TypeScript en D1 |
| H-19 | §0, pie, §0.8 | Identidad de borrador conservada; recepción pendiente de reconciliar (C1-V13) | Registrar procedencia y alcance | Confirmar emisión, identidad, BASELINE y Registro en C2 |

La propuesta de cada hallazgo está en las notas de [operación](operacion.md), [seguridad](seguridad.md), [contratos](contratos.md), [notas contractuales](notas-contractuales.md), [cierre de contratos](cierre-contratos.md), [Mercado Pago](mercado-pago.md) y [evaluación de Truora](truora-evaluacion.md). Este documento incorpora lo normativo de esas notas y no depende de ellas para completarse. La evidencia de proveedores sigue en las notas.

### 0.8 Requisitos candidatos tras la recepción Cowork

Recepción LBPF V4, PRD MVP V10 y L3/SQL V8, comparada con el canon y los acuerdos
C1. El [registro C1-V](reconciliacion-linea-base.md) cubre las 27 diferencias.
Este apartado incorpora su alcance; no afirma que el esquema, ledger o API
heredados ya cumplan las reglas. Sigue pendiente la consolidación por sección.

1. **Plazos.** T1–T8 tienen cierre final lógico, con máximo aprobado por mercado
   y validación por tipo. Se conserva duración propia/no solape T7. Resolver
   mínimo global 24 h frente a Flash T5 y efectos de pagos/reservas tardíos.
2. **Respaldo.** El mínimo debe permitir entregar todos los premios y ser coherente
   con importe, tickets, precio y versión aprobada fijada antes de publicar.
   Contar pagos válidos, excluir impagados/gratuitos/anulados y demostrar caja
   disponible. BR-09/KPI deben admitir respaldo por fianza sin llamarlo ingreso.
3. **Garantía del sorteo** (antes "fianza"). Aprobada el 04/10 desde la primera
   entrega (B); `VIABILITY_FAILED` y `VIABILITY_GAP` dejan de ser solo propuesta.
   Antes de operarla, declarar plazo, fondos acreditados, actor,
   custodia, T-19/20/21, devolución, incumplimiento, cancelación y sobrantes.
   Un UUID no nulo no demuestra garantía suficiente y vigente.
4. **FSM e inventario.** Comprobación y freeze/compromiso deben ser coherentes
   ante concurrencia. Declarar rutas tras perder viabilidad, suspensión, pausa,
   plazo y falso positivo; precedencia de vacío/umbral T2/mínimo. El potencial
   incluye reservas aún pagables; `tickets_reserved` ya incluye emitidos.
5. **Tipos.** Mantener umbral T2 y declarar desenlace T4 sin hito al vencer.
   T6 suma todos los premios y necesita suficientes elegibles para sus ganadores
   sin reemplazo. MVP sigue `PAID`; no habilitar otros regímenes por la semilla.
6. **Comprador y canal.** Bases, checkout, avisos y API declaran el mismo mínimo,
   fecha, cobertura y desenlace antes del pago. Costes/plazos de canal se declaran
   antes de habilitarlo; refund íntegro según contrato. No habilitar IAP por su
   mención en la fuente ni inferir tarifas/impuestos a partir del análisis.
7. **Evidencia.** Semilla única/idempotente, cuentas completas y rechazo con error
   esperado; fallos fatales y sondas adversariales. 39 checks PG16 o un verificador
   lexical verde no prueban cobertura, FSM, Excel ni migración completa PG17.

El múltiplo PE 1,25 y la ventana de 48 h son propuestas de la fuente, no valores
ratificados aquí. Reputación, relojes, JSON de configuración, alcance de garantía
y ciclo de caja requieren dueño/decisión. [LEGAL→ABOGADO] para custodia y bases;
ASS-001 permanece abierto. Se conserva D-05 para H-01–H-03.

[Aceptación](reconciliacion-aceptacion.md) fija contraejemplos y resultado exigido;
[decisiones/planificación](reconciliacion-decisiones-planificacion.md) registra
US-137–145 y dependencias. Dinero, contabilidad, concurrencia, incompatibilidades
y motor siguen siendo código humano de Diego. Esta ampliación no levanta el
freeze, no modifica el canon y no presenta servicios reales como probados.

## 1\. Convenciones de esquema

Los comentarios `-- V8` dentro del SQL señalan las líneas que cambian respecto de la versión anterior. Todo el DDL de este borrador está **sin ejecutar** (§0.2.1).

### 1.1 Reglas generales

| \#   | Regla                                                                                                                         |
| ---- | ----------------------------------------------------------------------------------------------------------------------------- |
| C-01 | Nombres de tabla en plural, minúscula, separación por guion bajo                                                              |
| C-02 | Clave primaria `id UUID` con generación en aplicación, nunca secuencial expuesta                                              |
| C-03 | Toda tabla mutable lleva `created_at TIMESTAMPTZ NOT NULL DEFAULT now()` y `updated_at TIMESTAMPTZ NOT NULL DEFAULT now()`    |
| C-04 | Toda tabla cuya mutación proviene de una operación trazable lleva `trace_id UUID NOT NULL`                                    |
| C-05 | Los estados son `VARCHAR(40)` con `CHECK` explícito, nunca tipos enumerados nativos: un `ALTER TYPE` bloquea en producción    |
| C-06 | Todo importe es `BIGINT` en unidad mínima de la moneda, acompañado de `currency CHAR(3)`. **Nunca punto flotante**. En Go se maneja como `int64`, en el frontend TypeScript como `bigint` y en JSON como cadena decimal (§11.1) |
| C-07 | Toda tabla con datos de un mercado lleva `market_code CHAR(2)`                                                                |
| C-08 | Las tablas de solo agregación llevan `CHECK` de inmutabilidad por disparador y revocación de `UPDATE`/`DELETE` a nivel de rol, con `GRANT` explícitos (§1.4) |
| C-09 | Toda clave foránea declara `ON DELETE RESTRICT`. No hay borrado en cascada en dominio financiero                              |
| C-10 | Los índices se nombran `ix_<tabla>_<columnas>`; los únicos, `ux_<tabla>_<columnas>`                                           |
| C-11 | Las tablas de crecimiento sin techo se particionan por rango mensual sobre su marca temporal de inserción (§1.3)              |
| C-12 | No existe borrado físico en dominio financiero ni de auditoría. La baja es lógica y explícita                                 |
| C-13 | **V8.** Todo identificador de documento de baja entropía (documento de usuario, de titular y de pagador) se guarda como HMAC-SHA-256 en hexadecimal, con secreto fuera de la base y versión de clave en columna propia. La entrada canónica incluye mercado, tipo de documento y número normalizado. Nunca SHA-256 directo (§7.4) |
| C-14 | **V8 (B1-bis).** La base no guarda datos personales en claro. Se cifran en el backend con cifrado de sobre sobre AWS KMS (AES-256-GCM): se guarda el texto cifrado en una columna `*_enc` junto con la clave de datos cifrada. La clave maestra no sale de KMS. Donde haga falta buscar o detectar duplicados se añade una huella HMAC con clave propia (C-13). Las columnas `*_enc` nuevas pertenecen al SQL V8, no al DDL heredado de este documento (§7.4) |

### 1.2 Tipos de dominio

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

**`sha256_hex` y HMAC.** El dominio valida el formato de 64 caracteres hexadecimales, sea cual sea la función. La salida de HMAC-SHA-256 cabe en él. Que un valor sea HMAC y no un hash directo lo garantiza el código que lo calcula (C-13), no el dominio.

### 1.3 Particionamiento

| Tabla                   | Clave de partición | Retención                                    |
| ----------------------- | ------------------ | -------------------------------------------- |
| `audit_events`          | `created_at`       | Indefinida; archivado en frío desde 24 meses |
| `audit_access_events`   | `created_at`       | Indefinida; archivado en frío desde 24 meses (B6) |
| `journal_lines`         | `posted_at`        | Indefinida                                   |
| `event_outbox`          | `created_at`       | 90 días tras despacho confirmado             |
| `analytics_events`      | `server_ts`        | 24 meses; agregados indefinidos              |
| `room_messages`         | `created_at`       | Indefinida                                   |
| `notification_attempts` | `server_ts`        | 24 meses                                     |
| `state_transitions`     | `created_at`       | Indefinida                                   |
| `registry_queries`      | `created_at`       | Indefinida                                   |
| `psp_events`            | `created_at`       | Pendiente (DP-12): la del soporte contable del pago [LEGAL→ABOGADO]; sin borrado hasta aprobarla |
| `operation_register`    | `created_at`       | Pendiente (DP-12) [LEGAL→ABOGADO]; sin borrado hasta aprobarla |
| `risk_events`           | `created_at`       | Indefinida; archivado en frío desde 24 meses (B6) |

Todas usan rango mensual. **V8 corrige la lista:** eran doce tablas particionadas y solo figuraban ocho. **Retención (B6).** La retención es una regla de operación y metadato de la tabla; este documento no define un borrado automático. Mientras un plazo esté pendiente, nada se borra.

**Particiones iniciales (H-05).** Una tabla particionada sin particiones rechaza todo `INSERT`. La migración 025 crea, para cada una de las doce tablas, la partición del mes en curso y las de los dos meses siguientes, con los índices y restricciones que declara la tabla madre. Sin ellas no hay auditoría, outbox ni ledger que puedan escribirse. El SQL de particiones de `journal_lines` forma parte de la contabilidad (ZC-09) y lo escribe su dueño.

**Regla de operación (B3).** El planificador único es `pg_cron` dentro de Supabase, con el rol dueño del esquema: una ejecución diaria de `ensure_monthly_partitions` con horizonte de dos meses mantiene creada, con al menos 30 días de antelación, la partición del mes siguiente de cada tabla. Una tarea de Trigger.dev solo lee `partition_status` y emite la alarma de severidad alta (§13.3) si la cobertura no está completa o si hay filas en una `DEFAULT`; no recibe la credencial del dueño. Condición: verificar que Supabase Pro permite `pg_cron` con ese rol. Si falta la partición del mes en curso, la escritura cae en la `DEFAULT` y activa la alarma; no se mueve ni borra automáticamente.

**Partición por defecto (P-09, B4, B5).** Los doce padres tienen una partición `DEFAULT`, `journal_lines` incluida, con la misma alarma. Así la falta de partición es una alarma y no un error de escritura, y no se bloquean cobros por un fallo del planificador. Crear un mes cuyo rango ya tiene filas en la `DEFAULT` falla con `LIBOX_PARTITION_DEFAULT_HAS_ROWS` sin mover datos. Para ese caso existe un procedimiento escrito, **nunca automático**, que ejecuta el dueño tras la alarma en una sola transacción: crea la tabla del mes suelta, mueve las filas desde la `DEFAULT`, la adjunta y registra la operación en `audit_events`. En `journal_lines`, `libox_append` solo tiene `INSERT` y nadie tiene `UPDATE` ni `DELETE`. **Estado:** la capa no crítica cubre once padres; la `DEFAULT` y la ACL de `journal_lines` están decididas pero su código es implementación humana pendiente (ZC-18), y mover filas del ledger nunca lo hace un procedimiento generado.

**Aceptación C1.** SQL aplicado a una base vacía, permisos y cobertura mensual UTC con al menos 30 días de antelación. El overlay prueba once padres; completar los doce requiere el aporte humano del ledger. Retención y restauración integral se ensayan antes de R1.

### 1.4 Roles de base de datos

| Rol             | Permisos                                                                                                         |
| --------------- | ---------------------------------------------------------------------------------------------------------------- |
| `libox_app`     | `SELECT`, `INSERT`, `UPDATE` según tabla. **Sin** `DELETE` **en dominio financiero ni de auditoría**             |
| `libox_append`  | Solo `INSERT` sobre tablas de agregación (`audit_events`, `audit_access_events`, `journal_lines`, `room_messages`, `state_transitions`) |
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

**Permisos explícitos (H-06).** Los cuatro roles son de grupo y no inician sesión. Que existan y que haya `REVOKE` no concede ni protege nada por sí solo. V8 exige lo siguiente:

1. **Logins técnicos separados (B2).** `libox_migrate` (`NOLOGIN`) es el dueño del esquema de dominio. Hay un login por componente, miembro solo de los roles de grupo que necesita: `libox_api` → `libox_app`; `libox_worker` → `libox_app` y `libox_append`; `libox_reporting` → `libox_read`; `libox_deployer` → `libox_migrate`, usado solo en el CI de migraciones. Los secretos viven en el gestor de Vercel y de Trigger.dev y rotan cada 90 días. La credencial de la aplicación nunca es la del propietario del esquema ni la del migrador. Pendiente de comprobar en Supabase: que `postgres` puede crear esos logins y ceder la propiedad.
2. **Sin privilegios implícitos.** Se revocan de `PUBLIC` los privilegios sobre el esquema de dominio. Se fijan `ALTER DEFAULT PRIVILEGES` para que las tablas y particiones que cree `libox_migrate` nazcan sin permisos amplios.
3. **`GRANT` por tabla (B1).** Cada tabla recibe exactamente el `GRANT` de su clase, según la tabla de clases de abajo. Nadie recibe `DELETE`. Solo agregación: `INSERT` y el `SELECT` necesario, nunca `UPDATE` ni `DELETE`. `libox_read` no lee las clases sensibles. La columna `raffles.status` solo cambia a través del procedimiento de §4.2.
4. **Roles del proveedor.** Los roles `anon` y `authenticated` de Supabase no tienen privilegios sobre el esquema de dominio, y sus tablas no se exponen por la API de datos del proveedor. El cliente nunca usa la clave `service_role`. RLS no sustituye a los `GRANT` ni a los controles de §7.
5. **Sin supuesto de superusuario.** Ninguna migración depende de privilegios de superusuario que el proveedor no conceda.

**Clases de privilegios (B1).** Decididas por Diego el 2026-09-30 para las 67 tablas que estaban pendientes de matriz. La lista de tablas por clase vive en el manifiesto de ACL del SQL (`database/acl-manifest.json`), que es el artefacto que prueba las concesiones exactas.

| Clase | `libox_app` | `libox_read` | Alcance |
| ----- | ----------- | ------------ | ------- |
| `operativa` | `SELECT`, `INSERT`, `UPDATE` | `SELECT` | Tablas de operación no patrimonial (31 tablas) |
| `registro_inmutable` | `SELECT`, `INSERT` | `SELECT` | Registros de solo agregación no patrimoniales (18 tablas) |
| `sensible` | `SELECT`, `INSERT`, `UPDATE` | — | Datos personales e identidad (8 tablas) |
| `sensible_inmutable` | `SELECT`, `INSERT` | — | Verificaciones de identidad y edad y documentos AML (3 tablas) |
| `catalogo_lectura` | `SELECT` | `SELECT` | `aml_thresholds`; cambia solo por migración con su versión |
| `reservado_humano` | — | — | Tablas de zonas sin IA; sus `GRANT` los escribe el dueño humano |

La reportería sobre datos personales irá por vistas seudonimizadas, que se definen aparte (DP-26). **Reclasificadas a `reservado_humano`** por B1, porque su comportamiento puede caer en una zona crítica: `spending_limits`, `spending_limit_changes` y `self_exclusions` (se comprueban dentro de la compra), `operation_register` (registro AML con importes), `transfer_costs` (importes que pueden afectar la liquidación) y `raffle_milestones` (desbloqueo por boletos vendidos). La capa no crítica no les concede nada; su ACL, DDL y pruebas son implementación humana (ZC-17).

**Aceptación.** Con la credencial real de cada login se intentan `UPDATE` y `DELETE` sobre tablas de solo agregación y de dominio financiero, lectura de las clases sensibles con `libox_read`, lectura con `anon` y `authenticated`, y DDL fuera del migrador. Todo debe fallar. Probar solo como propietario no vale como evidencia.

**Estado.** La capa no crítica del SQL aplica la ACL por clase: deniega por defecto y no concede nada a `reservado_humano`. No cierra H-06 hasta que el dueño humano escriba los permisos de las tablas reservadas, como `journal_lines` y las seis reclasificadas. El overlay deniega también `service_role`; la configuración gestionada real queda por verificar.

## 2\. Esquema — Identidad, organizador y mercado

### 2.1 Mercado y configuración

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

**V8 — capacidades de plataforma (A1, A5, C4).** El apagado global de una capacidad (`CAPABILITY_PLATFORM_DISABLE`) lo solicita un `ADMIN_SUPER` y lo firma **otro** `ADMIN_SUPER` (§7.2); `ck_pc_signer` solo impide que sea la misma persona, y el subrol del firmante lo comprueba el servicio. `LIVE` no es una capacidad: `T8` es la única capacidad para sorteos en vivo. En el MVP solo existe el régimen `PAID`: las capacidades `FREE_ENTRY` y `PROMOTIONAL` del comentario anterior permanecen deshabilitadas en las tres capas hasta diseñar su garantía sustitutiva (INV-06-b, INV-44).

### 2.2 Identidad

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
                                                -- V8: HMAC-SHA-256 (C-13), nunca SHA-256 directo
      document_hash_key_version SMALLINT,       -- V8: version de clave del HMAC
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
      trace_id           UUID,
      -- V8: hash y version de clave van juntos.
      CONSTRAINT ck_users_doc_key CHECK (
        (document_number_hash IS NULL) = (document_hash_key_version IS NULL))
    );

    -- INV-08 — unicidad de documento, correo y telefono sobre usuarios no cerrados.
    CREATE UNIQUE INDEX ux_users_email ON users (lower(email)) WHERE status <> 'CLOSED';
    CREATE UNIQUE INDEX ux_users_phone ON users (phone)        WHERE status <> 'CLOSED';
    CREATE UNIQUE INDEX ux_users_document ON users (document_number_hash)
      WHERE document_number_hash IS NOT NULL;

    -- RN-119: el documento de un menor detectado queda bloqueado de forma permanente.
    CREATE TABLE blocked_documents (
      document_number_hash sha256_hex PRIMARY KEY,   -- V8: HMAC-SHA-256 (C-13)
      key_version          SMALLINT NOT NULL,        -- V8: version de clave del HMAC
      reason               VARCHAR(40) NOT NULL
                           CHECK (reason IN ('MINOR','FRAUD','REGULATORY','SELF_EXCLUSION_PERM')),
      blocked_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
      blocked_by           UUID,
      notes                TEXT
    );

    -- V8: sustituye a credentials. La contrasena y el factor TOTP los gestiona el
    -- proveedor de identidad (§7.3). LIBOX no guarda una segunda copia de ninguno.
    CREATE TABLE auth_identities (
      user_id          UUID PRIMARY KEY REFERENCES users(id),
      provider         VARCHAR(40) NOT NULL,          -- 'supabase_auth'
      provider_subject UUID NOT NULL,                  -- identificador del usuario en el proveedor
      created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
      updated_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
      CONSTRAINT ux_auth_identity UNIQUE (provider, provider_subject)
    );

    -- V8: sustituye a refresh_tokens. Sesion aplicativa autoritativa para el
    -- acceso interno (§7.3). La renovacion de testigos no cuenta como actividad.
    CREATE TABLE app_sessions (
      id                     UUID PRIMARY KEY,
      user_id                UUID NOT NULL REFERENCES users(id),
      provider_session_id    UUID,
      device_id              UUID,
      assurance_level        VARCHAR(4) NOT NULL
                             CHECK (assurance_level IN ('aal1','aal2')),
      started_at             TIMESTAMPTZ NOT NULL DEFAULT now(),
      last_human_activity_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      absolute_expires_at    TIMESTAMPTZ NOT NULL,     -- maximo 30 dias desde started_at
      reauthenticated_at     TIMESTAMPTZ,              -- MFA reciente para acciones sensibles
      revoked_at             TIMESTAMPTZ,
      revoked_reason         VARCHAR(60),
      CONSTRAINT ck_app_session_window CHECK (
        absolute_expires_at > started_at
        AND absolute_expires_at <= started_at + INTERVAL '30 days')
    );
    CREATE INDEX ix_app_sessions_user_active ON app_sessions (user_id) WHERE revoked_at IS NULL;

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

**Unicidad con rotación de clave (C-13).** Mientras coexisten dos versiones de clave, un mismo documento produce dos valores HMAC distintos. El índice único solo protege dentro de una versión. Al registrar o verificar, el servicio calcula el HMAC con cada versión activa y busca todos los valores, tanto en `users` como en `blocked_documents` y en `clients`. La migración de valores a la clave nueva sigue un plan explícito de coexistencia; no se reemplazan valores sin él.

**`app_sessions` y `auth_identities` son una propuesta del candidato (P-01).** `app_sessions.device_id` queda sin clave foránea hasta que se decida si toda sesión debe asociarse a un dispositivo registrado.

**Datos personales cifrados (B1-bis, C-14).** Además de lo que V7 ya cifra (documento, nombre), V8 exige cifrar email, teléfono y fecha de nacimiento de `users`, con huella HMAC para el email del login y para detectar duplicados. Las columnas `email`, `phone` y `birth_date` en claro del bloque anterior, y los índices únicos que las usan, son **legado preservado, no listo para emisión en C2**: el SQL V8 los sustituye por columnas `*_enc` y huellas. La compatibilidad con Supabase es obligatoria. Exigirla no autoriza guardar email o teléfono en claro en `auth.users` (esa excepción sigue pendiente, DP-26) ni ratifica reemplazar Supabase Auth por una autenticación propia.

### 2.3 Verificación de identidad y edad

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

Los objetos de `identity_documents`, `client_kyb_documents`, `prize_valuation_documents`, `pc_stage_documents`, `room_evidence` y `aml_case_documents` siguen las reglas de almacenamiento de §7.5. La retención concreta de cada clase está sujeta a dictamen [LEGAL→ABOGADO].

### 2.4 Organizador

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
      owner_document_hash sha256_hex,                   -- V8: HMAC-SHA-256 (C-13)
      owner_document_key_version SMALLINT,              -- V8: version de clave del HMAC
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
        OR (owner_user_id IS NOT NULL AND owner_document_hash IS NOT NULL
            AND owner_document_key_version IS NOT NULL))   -- V8: version de clave
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

**V8 — KYB y capacidades del cliente (A5, A7).** La decisión de KYB (`client_kyb.status` a `APPROVED` o `REJECTED`, con `approved_by`) corresponde a `ADMIN_COMPLIANCE`; `ADMIN_RISK` la lee y gestiona las capacidades del cliente (§7.1). El proveedor de KYB sigue en evaluación (DP-20). En las capacidades del cliente se retira `LIVE`: `T8` es la única capacidad para sorteos en vivo. `P_C1` y `P_C2` no son tipos de sorteo: se habilitan en un campo propio de categorías (`enabled_categories` en el contrato), separado de los tipos `T1`–`T8`. El comentario `'P_C1', 'P_C2', 'LIVE'` de `client_capabilities` es **legado preservado, no listo para emisión en C2**; el SQL V8 fija la representación de las categorías. Los datos del representante legal y de contactos se cifran (C-14).

### 2.5 Reputación

> **[ZC-01 · zona sin IA · preservado]** El bloque siguiente conserva el código de V7 en zona crítica (comisión; segunda firma): `ck_fee_ceiling`, `ck_fee_exception_ceiling`, `ck_fee_exception_signer` y `ck_cfl_downgrade`. No tiene hallazgo registrado y se emite tal cual. Cualquier cambio posterior lo escribe a mano su dueño. Pruebas en D1.

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

## 3\. Esquema — Núcleo de negocio

### 3.1 Sorteo

> **[ZC-02 · zona sin IA · preservado]** El bloque siguiente conserva la tabla `raffles` de V7. Incluye restricciones de zona crítica: reparto de comisión (`ck_raffles_pricing`), contador de inventario (`ck_raffles_reserved`), régimen económico (`ck_raffles_regime_pricing`, `ck_raffles_prize_origin`, `ck_raffles_guarantee`) y rango de recaudación (`ck_raffles_multiple_floor`, `ck_raffles_multiple_ceiling`, `ck_raffles_multiple_signer`). No tiene hallazgo registrado y se emite tal cual. Cualquier cambio lo escribe a mano su dueño.

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

**Reglas V8 de configuración por tipo (C1–C4).** Decididas por Diego el 2026-09-30. Fijan la regla de producto; el código de inventario, rango de recaudación, régimen y reembolso que las aplique sigue siendo humano (ZC-02).

- **T1, plazo máximo (C1).** Todo T1 declara una política de expiración con duración máxima (`max_duration_days`) y su desenlace. Al vencer, si se alcanzó el mínimo vendido, se sortea con lo vendido; si no, se cancela con reembolso. El mínimo vendido, el premio que se entregará y las condiciones comunicadas al comprador quedan fijados antes de publicar y **no cambian después de la primera compra**. Siguen pendientes (DP-24) el umbral del mínimo (porcentaje o número de boletos), quién lo fija y dentro de qué límites, si el premio se entrega completo al alcanzarlo y cómo se informa antes de pagar. Como el mínimo debe estar fijado al publicar, un T1 no se publica mientras falte ese dato. La ampliación de Cowork que permite continuar bajo mínimo mediante fianza **no está aprobada**: bajo mínimo corresponde cancelar y reembolsar (§0.8). [LEGAL→ABOGADO]
- **T7, duración de cada edición (C2).** Cada edición declara su duración, independiente del intervalo de la recurrencia, y la duración no supera el intervalo: dos ediciones de la misma serie no se solapan.
- **Precio (C3).** El organizador fija `ticket_price`; se le muestra el neto estimado. El cálculo de comisión e impuesto que produce ese neto es zona sin IA (§6.2.1).
- **Régimen (C4).** En el MVP solo existe `PAID`. `FREE_ENTRY` y `PROMOTIONAL` quedan fuera hasta diseñar la garantía sustitutiva (INV-06-b, INV-44) y sus capacidades permanecen apagadas (§2.1).

**Legado preservado, no listo para emisión en C2.** El bloque anterior no tiene campo para la política de expiración de T1 (su obligación figura en `raffle_type_rules`, §4.1.1), ni para la duración propia de cada edición T7 en `raffle_recurrences`, y `ck_raffles_end_at` no cubre el plazo de T1. El `CHECK` de `economic_regime` conserva los tres regímenes; en el MVP se limitan a `PAID` por capacidades, y cualquier restricción adicional en `raffles` la escribe su dueño humano. Estos campos y restricciones se resuelven en el SQL V8 o en el aporte humano, no en este bloque.

### 3.2 Premio y valoración

> **[ZC-03 · zona sin IA · preservado]** El bloque siguiente conserva de V7 el disparador `assert_registrable_regime` (régimen económico) y la restricción `ck_pv_second_signer` (segunda firma). No tienen hallazgo registrado y se emiten tal cual. Cualquier cambio lo escribe a mano su dueño.

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

**V8 — actores de la valoración (A1, A2, A3, A6).** La cofirma de la banda V2 (`VALUATION_V2_COSIGN`) la da `ADMIN_MODERATION`, que cofirma sin obtener escritura sobre la valoración (§7.1). La banda V4 la firma `ADMIN_LEGAL_COMPLIANCE`. Una excepción de desviación (`VALUATION_EXCEPTION`) la solicita `SUPPORT_VALUATOR` o `ADMIN_LEGAL_COMPLIANCE` y la firma el otro de los dos o un `ADMIN_SUPER`. Observar una valoración (`VALUATION_OBSERVED`) y rechazarla manualmente (`VALUATION_REJECTED`) corresponde a quienes aprueban la banda: `SUPPORT_VALUATOR` y `ADMIN_LEGAL_COMPLIANCE`; ambos exigen motivo (§4.1). Los `CHECK` de firmantes de este bloque solo impiden que la misma persona firme dos veces; la política por acción la aplica el servicio (§7.2).

### 3.3 Bienes registrables (P-C)

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

**V8 — P-C en el MVP (A4, A8, B1, C4).** P-C entra en el MVP. Cada etapa tiene su aprobador según el PRD MVP V9 (matriz por etapa en §7.1): E1 `ADMIN_RISK`; E2, E3, E4 y E7 `ADMIN_LEGAL_COMPLIANCE`; E5 sin aprobador (automática); E6 en dos pasos, verificación de `SUPPORT_L2` y habilitación de `ADMIN_LEGAL_COMPLIANCE`. E3 y E7 llevan segunda firma (`PC_STAGE_E3`, `PC_STAGE_E7`, firmadas por `ADMIN_SUPER`). [LEGAL→ABOGADO] en E2, E4 y E7.

- **Lista de documentos (A8).** `checklist_key` es de lista cerrada por etapa (RN-29) y no tiene semilla todavía. Diego coordina con el abogado la entrega de la lista: clave, descripción y obligatoriedad por etapa, validada por el abogado. La fecha objetivo sigue pendiente; su estado se revisa en cada revisión de avance de C1 y antes del cierre del alcance P-C del MVP (DP-27). **Hasta recibirla, P-C sigue bloqueado** y no se inventan claves. El seguimiento no crea avisos automáticos ni mensajes externos.
- **Costos (C4).** `cost_kind` tiene como valores iniciales `SHIPPING`, `NOTARY` y `REGISTRY`, ampliables en V8. Los valores de `charge_kind` y `macrozone` están pendientes de Diego (DP-25). El bloque anterior no restringe `cost_kind`; el `CHECK` correspondiente es del SQL V8.
- **`transfer_costs` (B1).** Pasa a `reservado_humano`: guarda importes y quién los asume y puede afectar la liquidación. Sus permisos y restricciones los escribe el dueño humano (ZC-17).

### 3.4 Orden, idempotencia y pago

> **[ZC-04 · zona sin IA · preservado]** El bloque siguiente conserva el código de V7. Es zona crítica: la idempotencia y la deduplicación de eventos del PSP son ejecución única, y `orders` contiene el reparto del dinero (`ck_orders_split`, `ck_orders_cash`). No tiene defecto de código registrado. H-16 se resuelve como política (§12.9). La aplicación de C-13 a `payments.payer_document_hash` es propuesta del candidato (P-05) y la ajusta a mano su dueño cuando se implemente. Pruebas F1, F2 y F7 en R1.

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

### 3.5 Tickets

> **[ZC-05 · zona sin IA · preservado]** La tabla `tickets` y la sentencia de asignación de número conservan el código de V7. Son zona crítica de concurrencia e inventario, sin defecto de código registrado. Según la política de §12.9, un pago aprobado tras vencer la reserva o congelarse el pool no emite tickets. F5 se prueba en R1.

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

### 3.6 Sorteo ejecutado

El bloque de V7 se divide en dos partes para que cada una lleve su marca. El orden y el contenido no cambian.

> **[ZC-06 · zona sin IA · preservado]** Campañas de entrada gratuita con cupo atómico, garantías sustitutivas y cupo de planes promocionales, tal como estaban en V7. Son zona crítica (cupo atómico y régimen económico) y no tienen hallazgo registrado.

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

> **[ZC-07 · zona sin IA · aporte C1]** Compromisos, ejecuciones, ganadores, pruebas y re-sorteos conservan el código de V7. Son zona crítica: motor de sorteo y ejecución única. Aporte humano necesario para C1 (H-12): no existe dónde persistir la semilla cifrada entre el compromiso y la ejecución (requisito en §5.8). El resto del bloque se conserva. La espera ante una baliza tardía es norma operativa (§12.10). La política de re-sorteo condiciona solo habilitar el comando (DP-13).

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

### 3.7 Sala de Resolución

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

**[ZC-16 · zona sin IA · preservado]** `ck_att_signer` solo impide que la misma persona firme dos veces. Las incompatibilidades en ejecución (INC-06, INC-07, INC-09 e INC-11) y la política de segunda firma por `action_code` no se imponen con un `CHECK` estático: son lógica de servicio. Su dueño la implementa a mano en D1 (§7.2). **Atestación P-C (A9).** La segunda firma de la atestación se obtiene con una `SignatureRequest` de `ATTEST_PC` (§11.5); el cliente no envía `second_signer_id`. Si el SQL conserva la columna, la rellena el servidor con el firmante de la solicitud aprobada.

### 3.8 Controversias

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

**INC-08 implementado como restricción de aplicación y prueba.** Antes de persistir una adjudicación se verifica que `adjudicated_by` no figure en `delivery_attestations.attested_by` ni en `prize_valuations.reviewer_id` para ese sorteo. Es caso de prueba obligatorio (§14.3). Esta comprobación en ejecución pertenece a ZC-16 y la escribe a mano su dueño.

### 3.9 Liquidación

> **[ZC-08 · zona sin IA · preservado]** `settlements` y sus retenciones conservan el código de V7. Son dinero: `ck_settlement_net` y `ck_settlement_gates`. No tienen defecto de código registrado. Su uso con dinero real depende de la política contable pendiente por D-05 (H-01–H-03, DP-02) y de la custodia (DP-01), ambas antes de R1.

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

### 3.10 Contabilidad

> **[ZC-09 · zona sin IA · aporte C1]** Cuentas, asientos, líneas y disparador de cuadre conservan el código de V7. Es zona crítica: asientos contables. Aporte humano necesario para C1 por H-04. El cuadre solo se valida al insertar la cabecera del asiento, `account_code` no tiene clave foránea hacia `ledger_accounts` y la coherencia de moneda que se anuncia no está implementada. La aceptación exigida está en §14.9.

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

Un asiento que no cuadra aborta la transacción completa. La operación falla; no se persiste un desbalance. **Límite conocido (H-04):** esta garantía solo cubre las líneas presentes al confirmar la inserción de la cabecera. Líneas añadidas después a un asiento ya confirmado no se vuelven a comprobar. Tampoco se comprueba que la cuenta exista ni que la moneda de las líneas coincida con la del asiento.

### 3.11 Saldo de reembolso

> **[ZC-10 · zona sin IA · preservado]** Saldos, movimientos y retiros conservan el código de V7. Es zona crítica (bloqueo de saldo) sin hallazgo registrado. El retiro con dinero real depende de la custodia (DP-01).

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

### 3.12 Cumplimiento y riesgo

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

### 3.13 Protección del usuario

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

### 3.14 Analítica, alarmas, notificaciones y auditoría

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

Los `REVOKE` de este bloque solo protegen si existen los `GRANT` explícitos de §1.4 y si la aplicación se conecta con un login miembro de `libox_app`. El despacho de `event_outbox` sigue el contrato de §12.7. El `payload` publicado lleva identificadores y versión del evento, nunca documentos, semillas ni credenciales.

### 3.15 Growth

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

### 3.16 Control de acceso interno

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

### 3.16.1 Reglas de otorgamiento impuestas por el motor

**Norma V8.** Estas reglas son obligatorias con independencia del código que las implemente:

1. **INV-38.** Existen al menos dos `ADMIN_SUPER` activos en todo momento. Se rechaza cualquier revocación o suspensión que deje menos de dos, también cuando dos operaciones concurrentes actúan sobre titulares distintos. Si el número baja a uno por cualquier vía, salta una alarma de severidad alta.
2. **Techo y firma en toda activación (H-09).** Reactivar una asignación revocada, es decir, hacer un `UPDATE` que vuelve `revoked_at` a nulo o cambia el subrol, pasa los mismos controles que un `INSERT`: nadie se otorga a sí mismo, techo de privilegio y segunda firma cuando corresponda.
3. **Incompatibilidades en asignación (H-08).** INC-01 a INC-05 se rechazan al asignar, tanto por `INSERT` como por reactivación. INC-11 **no** se comprueba en asignación: depende de la acción concreta y se comprueba en ejecución (A11, §7.2).
4. **Arranque.** El primer y el segundo titular se crean conforme al PRD (DP-16), sin cuentas ficticias en producción. Las pruebas pueden usar identidades sintéticas.

> **[ZC-11 · zona sin IA · aporte C1]** Los disparadores siguientes conservan el código de V7 y **no cumplen la norma anterior**, así que C1 necesita un aporte humano. `assert_min_super_admins` rechaza solo si no queda ningún otro titular (`n < 1`), así que permite quedarse con uno solo (H-07). Además no cubre las suspensiones ni la concurrencia. `trg_grant_ceiling` se dispara solo en `INSERT`, así que una reactivación por `UPDATE` se salta el techo y la segunda firma (H-09). Falta el disparador de incompatibilidades en asignación (H-08). Los casos corregidos de §14.3 fallarán contra este código, y es lo esperado. Lo reemplaza el código escrito a mano por su dueño.

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

**INC-01 a INC-05 se imponen en asignación** mediante disparador que consulta `subrole_incompatibilities` antes de insertar en `subrole_assignments` o de reactivar una asignación. **INC-06 a INC-09 e INC-11 se imponen en ejecución**, porque dependen del sorteo o de la acción concreta: se verifican en el servicio y son casos de prueba obligatorios. INC-07 se comprueba solo en ejecución. **INC-10 es organizativo y auditado**, sin comprobación en la base. Así lo decidió Diego el 2026-09-30 (A11): prevalece §7.2. El campo `enforcement` de cada fila de `subrole_incompatibilities` se siembra con ese momento. Ambos mecanismos son zona crítica (ZC-11, ZC-16) y los escribe a mano su dueño.

**Segunda firma de un otorgamiento.** Cuando la matriz exige segunda firma (`SUBROLE_GRANT`), firma otro `ADMIN_SUPER` distinto de quien otorga (A1, §7.2). El disparador anterior solo exige que exista `second_signer_id`; comprobar persona y subrol del firmante forma parte del aporte humano de ZC-11.

## 4\. Máquina de estados del sorteo

### 4.1 Tabla de transiciones

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
| `PENDING_VALUATION`                                                | `DRAFT`             | `VALUATION_OBSERVED`    | SUPPORT\_VALUATOR o ADMIN\_LEGAL\_COMPLIANCE | Motivo obligatorio (A3)                                   |
| `PENDING_VALUATION`                                                | `REJECTED`          | `VALUATION_REJECTED`    | SUPPORT\_VALUATOR o ADMIN\_LEGAL\_COMPLIANCE | Motivo obligatorio (A6)                                   |
| `PENDING_LEGAL`                                                    | `PENDING_APPROVAL`  | `LEGAL_GATE_PASSED`     | ADMIN\_LEGAL\_COMPLIANCE                     | `gate_scope` satisfecho; en P-C, etapas E1–E4 aprobadas   |
| `PENDING_LEGAL`                                                    | `DRAFT`             | `LEGAL_GATE_OBSERVED`   | ADMIN\_LEGAL\_COMPLIANCE                     | Motivo obligatorio; subsanable (A6) [LEGAL→ABOGADO]       |
| `PENDING_LEGAL`                                                    | `REJECTED`          | `LEGAL_GATE_REJECTED`   | ADMIN\_LEGAL\_COMPLIANCE                     | Motivo obligatorio; terminal (A6) [LEGAL→ABOGADO]         |
| `PENDING_APPROVAL`                                                 | `SCHEDULED`         | `APPROVE_SCHEDULED`     | ADMIN\_MODERATION                            | `starts_at` futuro                                        |
| `PENDING_APPROVAL`                                                 | `ACTIVE`            | `APPROVE_IMMEDIATE`     | ADMIN\_MODERATION                            | Capacidad y categoría habilitadas en el mercado           |
| `PENDING_APPROVAL`                                                 | `REJECTED`          | `REJECT`                | ADMIN\_MODERATION                            | Motivo estructurado de la lista A11.1                     |
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
| `IN_RESOLUTION`                                                    | `DELIVERY_ATTESTED` | `ATTEST`                | SUPPORT\_L2 o ADMIN\_LEGAL\_COMPLIANCE       | En P-C solicita ADMIN_LEGAL_COMPLIANCE (A1); `ATTEST_PC` firmada (A9)       |
| `IN_RESOLUTION`                                                    | `CANCELLED`         | `RESOLVE_CANCEL`        | ADMIN                                        | Ruta declarada = CANCEL, o incumplimiento del organizador |
| `DELIVERY_ATTESTED`                                                | `SETTLED`           | `PAY_SETTLEMENT`        | ADMIN\_FINANCE                               | Seis gates verdaderos                                     |
| `SETTLED`                                                          | `CLOSED`            | `CLOSE`                 | SYSTEM                                       | Ventana de retención vencida sin incidencias              |
| Cualquiera previo a `DRAW_EXECUTED`                                | `SUSPENDED_MARKET`  | `MARKET_KILL_SWITCH`    | ADMIN\_SUPER                                 | Nivel de suspensión aplicable                             |
| `SUSPENDED_MARKET`                                                 | Estado anterior     | `MARKET_RESUME`         | ADMIN\_SUPER                                 | Segunda firma de otro ADMIN\_SUPER (A1)                   |

**Estados terminales sin salida:** `CLOSED`, `CANCELLED`, `REJECTED`.

**Decisiones V8 en esta tabla (A3, A6, A11).** La observación de una valoración la hacen quienes aprueban la banda, sin subrol nuevo. Los tres rechazos u observaciones manuales (`VALUATION_REJECTED`, `LEGAL_GATE_OBSERVED`, `LEGAL_GATE_REJECTED`) exigen motivo y replican el patrón de `VALUATION_OBSERVED`. Se añaden como filas de esta tabla; no se escribe aquí SQL para ellas: su carga en `fsm_transitions` y el punto único de transición (§4.2, H-08) siguen siendo aporte humano. No se crean estados nuevos: los destinos `DRAFT` y `REJECTED` ya existen.

**Motivo estructurado de `REJECT` (A11.1).** Lista cerrada aprobada por Diego el 2026-09-30: `CONTENT_POLICY`, `PRIZE_INELIGIBLE`, `TERMS_INCOMPLETE`, `MEDIA_INVALID`, `LEGAL_REQUIREMENT` y `OTHER`. `OTHER` exige texto.

**Semilla de `fsm_transitions` (H-08).** La migración 026 carga todas las filas de esta tabla y de §4.3 como datos. Una comprobación de cobertura en la migración verifica que cada fila de ambas tablas existe en `fsm_transitions`. La mera prosa no cuenta como semilla.

### 4.1.1 Semilla de `raffle_type_rules`

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

**Nota sobre T8.** Su `trigger_kind` en la semilla es un valor de relleno: el disparo real proviene siempre de `base_type`. La restricción `ck_raffles_base_type` garantiza que exista, y el invariante INV-17 que no altere la matemática. T8 es la única capacidad de sorteo en vivo; no existe una capacidad `LIVE` separada (A5).

**T1 y T7 en V8 (C1, C2).** `expiry_policy_required` de T1 se satisface con la política de §3.1: duración máxima y desenlace al vencer (sortear si se alcanzó el mínimo vendido; si no, cancelar con reembolso). Las filas de la tabla de §4.1 que llevan ese vencimiento a sorteo o a cancelación no se añaden todavía: dependen del umbral pendiente (DP-24) y no se crean estados nuevos para anticiparlas. En T7, `independent_edition` se complementa con la duración propia de cada edición, que no supera el intervalo de la serie (sin solape).

### 4.2 Aplicación de la transición

> **[ZC-12 · zona sin IA · aporte C1]** Esta sección especifica el comportamiento; no contiene código. El procedimiento que lo implementa no existe (H-08) y es aporte humano necesario para C1. Toma un bloqueo de fila y comprueba incompatibilidades en ejecución: es zona crítica y lo escribe a mano su dueño.

Toda transición pasa por un único punto de entrada, que en una sola transacción:

1. Toma bloqueo de fila sobre `raffles` con `SELECT ... FOR UPDATE`
2. Verifica que la tupla `(from_state, to_state, trigger)` existe en `fsm_transitions`
3. Verifica subrol del actor contra `required_subroles` y las incompatibilidades de ejecución
4. Evalúa la guarda
5. Exige motivo y segunda firma si la transición lo requiere
6. Actualiza `raffles.status`
7. Inserta en `state_transitions`
8. Inserta en `audit_events`
9. Inserta en `event_outbox`

**No existe otra ruta para cambiar** `raffles.status`**.** El permiso de `UPDATE` sobre esa columna se restringe al procedimiento almacenado que implementa este flujo. Los módulos de dominio TypeScript lo invocan; los endpoints y los trabajos no escriben el estado directamente.

### 4.3 Máquina de la Sala de Resolución

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

## 5\. Motor de sorteo

> **[ZC-13 · zona sin IA · aporte C1]** Las secciones §5.2 a §5.7 conservan el motor, la serialización canónica, la verificación y los vectores de V7. C1 necesita aportes humanos para los defectos siguientes; lo demás se conserva. Defectos abiertos: H-10 (vectores sin resultado esperado), H-11 (`verify_draw` compara el valor de la ronda con su identificador; dos implementaciones honestas pueden divergir) y H-12 (semilla cifrada sin almacenamiento definido; baliza con fuente heredada sin fijar ni espera acotada; la fuente queda ratificada en V8 como drand quicknet, D1). Los requisitos V8 están en §5.8. Ni la especificación cerrada, ni el código, ni los valores esperados se generan en este borrador. Los aportan su dueño y una implementación humana independiente.

### 5.1 Propiedades exigibles

| \#   | Propiedad                                                       | Cómo se consigue                                                   |
| ---- | --------------------------------------------------------------- | ------------------------------------------------------------------ |
| D-01 | El operador no puede elegir el resultado                        | Semilla secreta comprometida antes de conocerse el pool ganador    |
| D-02 | El operador no puede repetir hasta obtener el resultado deseado | Baliza pública de ronda **futura**, anunciada en el compromiso     |
| D-03 | Nadie puede precomputar el resultado antes de la ejecución      | La baliza no existe aún al publicarse el compromiso                |
| D-04 | Un tercero puede verificar sin confiar en LIBOX                 | Compromiso, baliza y pool son públicos y sellados temporalmente    |
| D-05 | Dos implementaciones honestas obtienen el mismo resultado       | Serialización canónica especificada al byte con vectores de prueba |
| D-06 | El sorteo no se re-ejecuta                                      | Restricción de unicidad en base de datos, no bloqueo distribuido   |

**Lo que se corrige respecto del algoritmo heredado.** La versión previa obtenía entropía pública *en el momento de ejecutar*, sin compromiso previo. Quien opera podía obtenerla, calcular el resultado y repetir la operación si no le convenía. Su verificación recomputaba a partir del valor almacenado por el propio operador: comprobaba **consistencia aritmética, no honestidad**. D-02, D-03 y D-04 no se cumplían.

**Estado V8.** D-05 no se cumple mientras sigan abiertos H-10 y H-11: sin resultados esperados y con un verificador ambiguo, dos implementaciones honestas pueden obtener resultados distintos. Ratificar drand quicknet como fuente (D1, §5.8) no cierra ninguno de los dos.

### 5.2 Serialización canónica del pool

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

El pseudocódigo es de referencia y está en Python, como en la versión anterior. No indica el lenguaje de la implementación, que en V8 es Go (D-10) y escribe su dueño.

### 5.3 Compromiso

Se ejecuta al pasar a `POOL_FROZEN`, antes de conocerse ningún resultado.

    server_seed  = 32 bytes de un generador criptográficamente seguro
                   representados en hexadecimal minúscula (64 caracteres)
    commitment   = SHA256_hex( utf8( server_seed ) )
    beacon_ref   = identificador de una ronda FUTURA de la fuente pública
    earliest_execution_at = momento previsto de disponibilidad de esa ronda

**Se publica de inmediato y se sella temporalmente:** `pool_hash`, `pool_size`, `commitment`, `beacon_source`, `beacon_ref`, `algorithm_version`, `winners_count`, `earliest_execution_at`.

**El** `server_seed` **se almacena cifrado y no se expone por ninguna interfaz hasta la ejecución.** En V8 este requisito se precisa en §5.8. El esquema de ZC-07 todavía no lo soporta.

**Elección de la ronda de baliza.** `beacon_ref` debe corresponder a una ronda que **aún no se ha producido** en el momento de publicar el compromiso, con un margen mínimo definido en `market_config` (INV-18). Si la ronda ya existe al publicar, el compromiso es inválido y el congelamiento falla con `ERR_DRAW_BEACON_NOT_FUTURE`.

**Propiedad intrínseca de la ronda.** Junto al identificador se publican `beacon_round_kind`, `beacon_round_value` y `beacon_round_time`. Esta terna es lo que hace la verificación **independiente de LIBOX**.

La versión anterior comprobaba que `beacon.retrieved_at` fuera posterior a `commitment.published_at`. Esa comprobación es insuficiente: `retrieved_at` **es una marca temporal que escribe LIBOX**, de modo que un tercero no puede distinguir “esta ronda no existía al comprometer” de “declaramos haberla obtenido después”. Se verificaba consistencia aritmética, no honestidad, que es exactamente el defecto que este diseño existe para eliminar.

Con la terna, el verificador consulta **la propia fuente de baliza** —no a LIBOX— y comprueba que la ronda comprometida es posterior al compromiso por una propiedad de la fuente: número de ronda, altura de bloque o instante de la ronda. `retrieved_at` se conserva como dato operativo y **carece de valor probatorio**.

### 5.4 Ejecución

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

### 5.5 Documento de prueba

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

### 5.6 Verificación pública

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

**Defecto heredado (H-11).** La función anterior mezcla tres conceptos distintos: el identificador de la ronda (`ref`), su propiedad intrínseca (`round_value`) y los bytes de aleatoriedad (`value`). Al comparar `round_value` con `ref` y el valor devuelto con `value`, una implementación honesta que separe los tres puede fallar la verificación. Tampoco valida la autenticidad de la baliza. La corrección requiere antes la especificación cerrada de DP-04.

### 5.7 Vectores de prueba

Obligatorios en la batería de pruebas. Cualquier implementación debe reproducirlos exactamente.

**Defecto heredado (H-10).** Los vectores siguientes dan entradas pero no resultados esperados (`pool_hash`, `commitment`, `seed_material`, ganadores), así que "reproducirlos exactamente" no se puede comprobar. V8 exige completar cada vector con sus salidas. Esas salidas las calcula una implementación humana independiente, con código distinto del que se prueba, y las verifica una segunda implementación. No se derivan del código bajo prueba ni las genera este borrador.

#### Vector 1 — pool pequeño, un ganador

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

#### Vector 2 — pool con huecos por anulación

    pool              = [1,2,5,7,8]          -- 3, 4 y 6 anulados: no participan
    canonical_string  = "<raffle_id>|5|1,2,5,7,8"

Comprueba que los números anulados quedan fuera y que el orden es por número, no por identificador.

#### Vector 3 — multi-ganador sin reemplazo

    pool = [10,20,30,40,50], k = 3

Comprueba que no hay repetición y que el pool remanente se reduce en cada extracción.

#### Vector 4 — re-sorteo encadenado

    pool_1 = [1..100], ganador = 42
    pool_2 = pool_1 sin 42       -- 99 elementos
    commitment_2 != commitment_1
    beacon_ref_2  posterior a beacon_ref_1

Comprueba la exclusión del ganador original y el compromiso nuevo.

#### Vector 5 — casos de rechazo

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

`ERR_DRAW_BEACON_VALUE_MISMATCH` y `ERR_DRAW_PROOF_INCOMPLETE` no figuran en §8.2 (P-08).

### 5.8 Requisitos V8 del motor, pendientes de implementación humana

Estos requisitos proceden de la nota de seguridad de C1. Especifican la aceptación sin dar el código.

1. **Tres datos separados.** La especificación distingue el identificador de red o ronda, el instante programado y los bytes de aleatoriedad. El verificador consulta la ronda comprometida y valida la autenticidad de la baliza con la suite de firmas de la fuente. No acepta el `retrieved_at` que da LIBOX. **La fuente está ratificada (D1):** drand quicknet, red principal no encadenada con período de 3 s, cadena `52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971`. Identidad de cadena y clave pública de confianza se fijan en la configuración versionada; no basta el nombre `quicknet` ni HTTPS, y `latest` no es una selección de ronda válida. Un relay alternativo solo puede servir la misma cadena y la misma ronda. Siguen pendientes en DP-04, como aporte humano, la biblioteca compatible con el esquema de firma, la serialización y codificación de cada campo, la interfaz de `verify_draw` y los resultados esperados de los cinco vectores; ninguno se produce en este borrador ([propuesta de baliza](baliza-propuesta.md)).
2. **Semilla cifrada (H-12).** Antes de publicar el compromiso se persisten el texto cifrado de `server_seed` con cifrado autenticado, el identificador y la versión de la clave y la referencia al sorteo. La clave se gestiona aparte (DP-06). Solo el ejecutor autorizado puede descifrar, y el texto en claro no llega a registros ni a copias sin cifrar. La restauración de clave y datos se ensaya (§13.5).
3. **Baliza tardía.** Si la ronda no está disponible en `earliest_execution_at`, se aplica §12.10. El vencimiento no autoriza otra ronda, otra semilla ni un sorteo manual.
4. **Vectores completos.** Cada vector de §5.7 lleva sus salidas, obtenidas y verificadas por dos implementaciones humanas independientes (§14.5).
5. **Prueba pública independiente.** Una persona distinta de la que escribe el motor escribe el verificador, sin compartir código con la ejecución.

## 6\. Plan de cuentas y transacciones

> **[ZC-14 · zona sin IA · pendiente D-05]** Esta sección especifica asientos contables, comisión e impuesto incluido. Se conserva como estaba en V7, y este candidato no decide la política contable. Según la decisión D-05 del programa R0, estos hallazgos quedan registrados y pendientes de confirmación contable. No condicionan C1 ni C2, pero deben resolverse antes de mover dinero real en R1. Defectos abiertos: H-01, porque con T-01, T-04 y T-05 en el mismo instante el saldo de `purchase_liability` de una orden pagada queda en cero y L-04 falla con cualquier orden pagada; H-02, porque T-03 no existe y ninguna transacción debita `cash_clearing` al devolver al medio de pago original; H-03, porque la comisión y el impuesto se reconocen al cobrar, antes del sorteo y de la entrega [LEGAL→ABOGADO]. La propuesta registrada es diferir T-04, T-05 y T-06 hasta "liquidación elegible". **No está aceptada** y requiere confirmación contable (DP-02). La custodia (ASS-001, DP-01) sigue abierta. Una elección técnica no resuelve ninguno de estos puntos.

### 6.1 Cuentas

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

### 6.2 Transacciones canónicas

Todos los importes en unidad mínima. Cada bloque es un asiento con cuadre obligatorio.

**T-01 · Confirmación de pago** — al recibirse aprobación del proveedor.

| Cuenta                    | Débito               | Crédito        | Ámbito  |
| ------------------------- | -------------------- | -------------- | ------- |
| `psp_clearing`            | `cash_amount`        |                | —       |
| `refund_credit_liability` | `refund_credit_used` |                | usuario |
| `purchase_liability`      |                      | `gross_amount` | sorteo  |

**T-02 · Comisión del proveedor de pagos.**

| Cuenta            | Débito    | Crédito   |
| ----------------- | --------- | --------- |
| `psp_fee_expense` | `psp_fee` |           |
| `psp_clearing`    |           | `psp_fee` |

**T-03 · No definida (H-02, DP-03).** Pendiente: devolución al medio de pago original y movimiento de `cash_clearing` y `psp_clearing`. La definirán el dueño contable y el código humano. Sin ella no se cierran F4 ni F7.

**T-04 · Devengo de comisión de plataforma.**

| Cuenta               | Débito             | Crédito            | Ámbito |
| -------------------- | ------------------ | ------------------ | ------ |
| `purchase_liability` | `libox_fee_amount` |                    | sorteo |
| `platform_revenue`   |                    | `libox_fee_amount` | —      |

**T-05 · Devengo de obligación con el organizador.**

| Cuenta               | Débito              | Crédito             | Ámbito  |
| -------------------- | ------------------- | ------------------- | ------- |
| `purchase_liability` | `client_net_amount` |                     | sorteo  |
| `client_payable`     |                     | `client_net_amount` | cliente |

**T-06 · Devengo de impuesto sobre la comisión.**

| Cuenta             | Débito       | Crédito      |
| ------------------ | ------------ | ------------ |
| `platform_revenue` | `tax_amount` |              |
| `tax_payable`      |              | `tax_amount` |

**T-07 · Retención por contracargo** — al alcanzar `ELIGIBLE`.

| Cuenta               | Débito           | Crédito          | Ámbito  |
| -------------------- | ---------------- | ---------------- | ------- |
| `client_payable`     | `reserve_amount` |                  | cliente |
| `chargeback_reserve` |                  | `reserve_amount` | cliente |

**T-08 · Liquidación al organizador.**

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

**T-12 · Retiro de saldo.**

| Cuenta                    | Débito   | Crédito  | Ámbito  |
| ------------------------- | -------- | -------- | ------- |
| `refund_credit_liability` | `amount` |          | usuario |
| `cash_clearing`           |          | `amount` | —       |

**T-13 · Contracargo recibido.**

| Cuenta                              | Débito   | Crédito  | Ámbito |
| ----------------------------------- | -------- | -------- | ------ |
| `purchase_liability` o `adjustment` | `amount` |          | sorteo |
| `psp_clearing`                      |          | `amount` | —      |

Si el sorteo ya se ejecutó, el débito va a `adjustment`: **los tickets no se invalidan retroactivamente** (RN-62), porque hacerlo rompería la integridad del pool y de la prueba.

**T-14 · Ajuste administrativo** — motivo obligatorio y segunda firma (RN-46).

**T-15 · Cobro de suscripción o plan promocional.**

| Cuenta                          | Débito   | Crédito  | Ámbito            |
| ------------------------------- | -------- | -------- | ----------------- |
| `psp_clearing`                  | `amount` |          | —                 |
| `subscription_deferred_revenue` |          | `amount` | usuario o cliente |

**T-16 · Devengo diario de suscripción o plan.**

| Cuenta                                              | Débito          | Crédito         | Ámbito            |
| --------------------------------------------------- | --------------- | --------------- | ----------------- |
| `subscription_deferred_revenue`                     | `daily_accrual` |                 | usuario o cliente |
| `subscription_revenue` o `promotional_plan_revenue` |                 | `daily_accrual` | —                 |

**T-17 · Baja con prorrateo.**

| Cuenta                                      | Débito               | Crédito              | Ámbito  |
| ------------------------------------------- | -------------------- | -------------------- | ------- |
| `subscription_deferred_revenue`             | `unearned_remainder` |                      | usuario |
| `refund_credit_liability` o `cash_clearing` |                      | `unearned_remainder` | usuario |

**T-18 · Premio de oportunidad sin recaudación.**

| Cuenta                | Débito       | Crédito      |
| --------------------- | ------------ | ------------ |
| `promotional_expense` | `prize_cost` |              |
| `cash_clearing`       |              | `prize_cost` |

**Nota sobre T-18.** No existe `purchase_liability` porque **nadie pagó**. El premio es gasto de la parte que lo aporta, y cuando lo aporta una parte relacionada se registra con su marca para consolidación (INV-39).

**Nota sobre T-16.** El devengo diario es lo que impide reconocer como ingreso un cobro que aún no se ha prestado. **Sin él, una baja a mitad de periodo dejaría el ledger sin saber qué devolver.**

### 6.2.1 Impuesto incluido en la comisión

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

**Supuesto sujeto a dictamen (L-05):** que el impuesto aplique sobre la comisión, cuál es su base y quién es el contribuyente permanece pendiente de asesoría. Lo que esta versión fija es la **mecánica**: si aplica, se extrae de la comisión y jamás del neto del organizador. [LEGAL→ABOGADO]

**Ejemplo heredado, no verificado en V8.** Las cifras del ejemplo vienen de V7. Este borrador no las recalcula ni las acredita como vector de prueba de comisión o impuesto. Los vectores de esta zona los produce su dueño.

### 6.3 Secuencia por ciclo de vida

| Momento                             | Asientos                                   |
| ----------------------------------- | ------------------------------------------ |
| Pago aprobado                       | T-01, T-02, T-04, T-05, T-06               |
| Liquidación elegible                | T-07                                       |
| Pago al organizador                 | T-08                                       |
| Vencimiento de la ventana extendida | T-09, y T-08 por el saldo retenido         |
| Cancelación                         | Reversión de T-04, T-05, T-06 y luego T-10 |
| Contracargo                         | T-13                                       |

**Secuencia heredada, en disputa (H-01, H-03, DP-02).** Con esta secuencia, L-04 no se cumple desde el primer pago aprobado. La tabla no se corrige aquí porque moverla supone decidir la política contable.

### 6.4 Invariantes contables verificados a diario

| \#   | Invariante                                  | Consulta                                                                                           |
| ---- | ------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| L-01 | Todo asiento cuadra                         | `SUM(debit) = SUM(credit)` agrupado por `entry_id`                                                 |
| L-02 | Saldo de reembolso agregado igual al pasivo | `SUM(refund_credits.balance)` frente al saldo de `refund_credit_liability`                         |
| L-03 | Caché de saldo consistente                  | `refund_credits.balance = SUM(refund_credit_entries.amount)` por usuario y moneda                  |
| L-04 | **INV-16 — suficiencia de reembolso**       | Para todo sorteo activo, saldo de `purchase_liability` del sorteo ≥ suma de importes reembolsables |
| L-05 | Sin ticket sin pago                         | Ningún ticket `ISSUED` con orden distinta de `PAID`                                                |
| L-06 | Cuadre de liquidación                       | `net_payable = gross_collected − libox_fee + adjustments − reserve`                                |
| L-07 | Cuadre de conciliación                      | Suma de `psp_clearing` frente al reporte del proveedor, con excepciones abiertas identificadas     |

Toda divergencia genera alarma de familia `LEDGER` y severidad alta. **L-04 es la que respalda la promesa de §1.5 del PRD** y no admite tolerancia. **No se da por válida mientras siga abierto H-01.**

## 7\. Matriz de control de acceso y seguridad

### 7.1 Permisos por subrol

`R` lectura · `W` escritura · `A` acción privilegiada · `—` sin acceso

| Recurso                    | USER\_VER | CLI\_OWN | CLI\_MGR | CLI\_OPR | CLI\_VIEW | SUP\_L1 | SUP\_L2 | SUP\_VAL | SUP\_SUP | SUP\_BEH | ADM\_MOD | ADM\_RISK | ADM\_FIN | ADM\_LEG | ADM\_CMP | ADM\_BEH | ADM\_SUP |
| -------------------------- | --------- | -------- | -------- | -------- | --------- | ------- | ------- | -------- | -------- | -------- | -------- | --------- | -------- | -------- | -------- | -------- | -------- |
| Catálogo público           | R         | R        | R        | R        | R         | R       | R       | R        | R        | R        | R        | R         | R        | R        | R        | R        | R        |
| Compra de tickets          | W         | —        | —        | —        | —         | —       | —       | —        | —        | —        | —        | —         | —        | —        | —        | —        | —        |
| Sorteo propio              | —         | W        | W        | R        | R         | R       | R       | R        | R        | —        | A        | R         | R        | R        | R        | —        | R        |
| Aprobar sorteo             | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | **A**    | —         | —        | —        | —        | —        | —        |
| Valoración de premio       | —         | W        | W        | —        | R         | R       | R       | **A**    | R        | —        | R        | R         | —        | **A**    | —        | —        | R        |
| Cofirma de valoración V2   | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | **A**    | —         | —        | —        | —        | —        | —        |
| Etapas P-C: expediente     | —         | W        | W        | W        | R         | R       | R       | R        | R        | —        | R        | R         | —        | R        | R        | —        | R        |
| P-C E1 elegibilidad        | —         | —        | —        | —        | —         | R       | R       | R        | R        | —        | R        | **A**     | —        | R        | R        | —        | R        |
| P-C E2–E4 y E7             | —         | —        | —        | —        | —         | R       | R       | R        | R        | —        | R        | R         | —        | **A**    | R        | —        | R        |
| P-C E6 verificación        | —         | —        | —        | —        | —         | R       | **A**   | R        | R        | —        | R        | R         | —        | R        | R        | —        | R        |
| P-C E6 habilitación        | —         | —        | —        | —        | —         | R       | R       | R        | R        | —        | R        | R         | —        | **A**    | R        | —        | R        |
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
| Decisión KYB               | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | —        | R         | —        | —        | **A**    | —        | —        |
| Aprobación sobre umbral    | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | —        | —         | —        | —        | **A**    | —        | A        |
| Panel de alarmas           | —         | —        | —        | —        | —         | R       | R       | R        | R        | R        | R        | R         | R        | R        | R        | R        | A        |
| Indicadores conductuales   | —         | —        | —        | —        | —         | —       | —       | —        | —        | R        | R        | —         | —        | —        | —        | **A**    | R        |
| Configuración de mercado   | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | —        | —         | —        | **A**    | R        | —        | A        |
| Suspensión de mercado      | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | —        | —         | —        | R        | R        | —        | **A**    |
| Usuarios internos          | —         | —        | —        | —        | —         | —       | —       | —        | —        | —        | —        | —         | —        | —        | —        | —        | **A**    |
| Segunda firma†             | —         | —        | —        | —        | —         | —       | —       | A        | —        | —        | A        | —         | —        | A        | —        | —        | **A**    |

`W*` = escritura restringida a las salas en que la persona es parte o asignada.

`†` = solo en los `action_code` en que la política de §7.2 lo hace firmante; nunca sobre su propia solicitud.

**Decisiones V8 en esta matriz (A1, A2, A4, A7).** La cofirma de la banda V2 da a `ADMIN_MODERATION` la acción de cofirmar, no escritura sobre la valoración. La fila única "Etapas P-C" de V7 se parte por etapa según el PRD MVP V9: E1 la aprueba `ADMIN_RISK`; E2, E3, E4 y E7, `ADMIN_LEGAL_COMPLIANCE`; E5 es automática y no tiene aprobador; E6 tiene dos pasos, verificación de `SUPPORT_L2` y habilitación de `ADMIN_LEGAL_COMPLIANCE`. [LEGAL→ABOGADO] en E2, E4 y E7. KYB lo decide `ADMIN_COMPLIANCE` y lo lee `ADMIN_RISK`, que habilita capacidades: así se separa quien verifica al cliente de quien le habilita capacidades. La fila "Segunda firma" deja de ser exclusiva de `ADMIN_SUPER`: el firmante de cada acción lo fija la política de §7.2.

La lista de roles no basta. Cada operación comprueba también pertenencia al recurso, estado y separación de funciones. En el contrato de §11 se describe con `x-authorization`.

### 7.2 Incompatibilidades y momento de comprobación

| Código | Regla                                                    | Momento                |
| ------ | -------------------------------------------------------- | ---------------------- |
| INC-01 | `ADMIN_MODERATION` y `ADMIN_FINANCE`                     | Asignación             |
| INC-02 | `ADMIN_LEGAL_COMPLIANCE` y `ADMIN_FINANCE`               | Asignación             |
| INC-03 | `ADMIN_COMPLIANCE` y `ADMIN_FINANCE`                     | Asignación             |
| INC-04 | `ADMIN_COMPLIANCE` y `ADMIN_MODERATION`                  | Asignación             |
| INC-05 | `ADMIN_BEHAVIORAL` y `ADMIN_FINANCE`                     | Asignación             |
| INC-06 | `SUPPORT_VALUATOR` no atesta el sorteo que valoró        | **Ejecución**          |
| INC-07 | `ADMIN_FINANCE` no atesta entregas                       | **Ejecución**          |
| INC-08 | Quien adjudica no atestó ese caso                        | **Ejecución**          |
| INC-09 | Segunda firma de otra persona y, salvo en acciones propias de `ADMIN_SUPER`, de otro subrol | **Ejecución** |
| INC-10 | Sin métrica de volumen para roles de aprobación de valor | Organizativo, auditado |
| INC-11 | `ADMIN_SUPER` no firma en segundo lugar su propia acción | **Ejecución**          |

Las de asignación se imponen por disparador sobre `subrole_assignments`, también al reactivar una asignación. Las de ejecución se verifican en el servicio y son casos de prueba obligatorios (§14.3). Ambas son zona crítica (ZC-11, ZC-16). La suspensión de la revisión humana del repositorio no suprime ninguna incompatibilidad ni segunda firma del producto.

**Momento de INC-07, INC-10 e INC-11 (A11).** Esta tabla prevalece sobre cualquier otro texto del documento. INC-07 se comprueba solo en ejecución: `ADMIN_FINANCE` no tiene `A` para atestar y no hay par de subroles que bloquear al asignar. INC-10 es organizativo y auditado, sin comprobación en la base. INC-11 depende de la acción concreta y se comprueba en ejecución.

**Política de segunda firma por `action_code` (A1).** Decidida por Diego el 2026-09-30. Se carga como dato, no como condicionales en código. Reglas: la segunda firma es siempre de **otra persona** (INC-11: nadie firma su propia acción); es de **otro subrol**, salvo cuando la acción es propia de `ADMIN_SUPER`, en cuyo caso firma **otro** `ADMIN_SUPER` (coherente con INV-38). Sin una fila en esta tabla, una solicitud no es firmable (falla cerrado).

| `action_code` | Solicita normalmente | Firmantes elegibles |
| ------------- | -------------------- | ------------------- |
| `VALUATION_V2_COSIGN` | `SUPPORT_VALUATOR` | `ADMIN_MODERATION` (A2) |
| `VALUATION_V4` | `SUPPORT_VALUATOR` | `ADMIN_LEGAL_COMPLIANCE` |
| `VALUATION_EXCEPTION` | `SUPPORT_VALUATOR` o `ADMIN_LEGAL_COMPLIANCE` | El otro de los dos; `ADMIN_SUPER` |
| `PC_STAGE_E3` | `ADMIN_LEGAL_COMPLIANCE` | `ADMIN_SUPER` |
| `PC_STAGE_E7` | `ADMIN_LEGAL_COMPLIANCE` | `ADMIN_SUPER` |
| `ATTEST_PC` | `ADMIN_LEGAL_COMPLIANCE` | `ADMIN_SUPER` |
| `CAPABILITY_PLATFORM_DISABLE` | `ADMIN_SUPER` | Otro `ADMIN_SUPER` |
| `MARKET_RESUME` | `ADMIN_SUPER` | Otro `ADMIN_SUPER` |
| `MULTIPLE_OVERRIDE` | `ADMIN_COMPLIANCE` | `ADMIN_SUPER` |
| `SUBROLE_GRANT` | `ADMIN_SUPER` | Otro `ADMIN_SUPER` |
| `MFA_RESET_INTERNAL` | `ADMIN_SUPER` | Otro `ADMIN_SUPER` |

`MULTIPLE_OVERRIDE` toca el rango de recaudación: aquí solo se fija el firmante, no la regla del múltiplo, que es zona sin IA. Todas las segundas firmas, incluida la atestación P-C (A9), usan el mismo mecanismo `SignatureRequest`, con INC-09 e INC-11 comprobados en un único punto. La comprobación es lógica de servicio en zona sin IA (ZC-16).

### 7.3 Autenticación y sesión

**Proveedor.** Supabase Auth gestiona la identidad de acceso, la contraseña y el factor TOTP. LIBOX gestiona roles, permisos por recurso, incompatibilidades y la sesión aplicativa. No se afirma equivalencia literal entre el comportamiento del proveedor y el contrato anterior: las diferencias se registran abajo.

| Aspecto | Decisión V8 | Diferencia con el contrato anterior |
| ------- | ----------- | ----------------------------------- |
| Credencial de acceso | JWT del proveedor con vida de 15 minutos. El backend valida emisor, audiencia, firma, expiración y sesión aplicativa. No confía en claims de rol obsoletos | Un JWT puede sobrevivir al fin de la sesión: por eso cada acceso interno consulta la sesión aplicativa |
| Renovación | Testigo de renovación del proveedor. Sesión máxima de 30 días, comprobada por LIBOX en `app_sessions.absolute_expires_at` además de por el proveedor | El testigo del proveedor no expira por sí solo; el límite lo impone la sesión |
| Reutilización de testigo | El proveedor admite una ventana de reutilización de 10 s y mantiene activo el testigo padre. Las excepciones se documentan y el evento de riesgo de LIBOX se alimenta por un puente verificable (P-01) | Ya no se garantiza que "toda reutilización revoca la familia" |
| Multifactor | Obligatorio para todo subrol interno (RN-05). Toda ruta interna exige nivel `aal2`; tener el factor enrolado no basta | — |
| Inactividad interna | La sesión aplicativa expira a los 30 minutos sin actividad humana. Solo cuentan las solicitudes autenticadas de interacción; no cuentan la renovación de testigos, el sondeo ni un latido que alargue la sesión indefinidamente | El temporizador del proveedor mide renovaciones, no interacción |
| Acciones sensibles | Reautenticación o MFA reciente (`app_sessions.reauthenticated_at`), válida **5 minutos** (A10). Pasado ese plazo, la acción exige reautenticar | La ventana la fijó Diego el 2026-09-30; antes era un supuesto |
| Revocación y cambio de rol | Efectivos en el siguiente acceso interno | — |
| Contraseña | La gestiona el proveedor con bcrypt. LIBOX no guarda segunda copia | Sustituye al argon2id almacenado por LIBOX |
| Portabilidad | **Nunca exclusivamente por cookie** (RN-213). La aplicación nativa futura usa Bearer con el mismo mecanismo | — |

Los testigos no aparecen nunca en registros ni en URLs. El cliente no recibe acceso directo a tablas de dominio ni la clave `service_role`. INV-38 se mantiene: mínimo dos `ADMIN_SUPER` activos (§3.16.1).

**Datos personales y Supabase (B1-bis).** La compatibilidad con Supabase es obligatoria (Diego, 2026-09-30). El cifrado de C-14 se aplica en el backend con AWS KMS y no sustituye a los `GRANT` de §1.4: protege ante el robo de la base, y los permisos limitan qué componente lee qué. Antes de implementarlo hay que definir el alcance de Supabase Auth y el inventario de datos personales, incluidos documentos, registros y exportaciones (DP-26). La excepción para guardar email o teléfono en `auth.users` sigue **pendiente y no autorizada**, y esta exigencia no ratifica sustituir Supabase Auth por una autenticación propia. También quedan pendientes la rotación de la clave maestra y de la clave HMAC con su recifrado (DP-06), las vistas seudonimizadas de `libox_read` y la caché de claves de datos en el backend con su tiempo de vida.

### 7.4 Protección de identificadores de documento

1. **HMAC-SHA-256 (C-13).** Los identificadores de documento se guardan como HMAC con secreto fuera de la base. La entrada canónica incluye versión de clave, mercado, tipo de documento y número normalizado.
2. **Normalización exacta por tipo.** Se fija para cada tipo de documento. No se añaden ceros, prefijos ni formatos regionales que la fuente oficial no defina.
3. **Rotación.** Hay un periodo de coexistencia controlado y búsqueda con todas las versiones activas (§2.2). No se reemplazan valores sin un plan de migración. La gestión del secreto y su rotación están en DP-06.
4. **Cifrado de sobre (B1-bis, C-14).** Los datos personales, incluido el número de documento, se cifran con una clave de datos que entrega AWS KMS (AES-256-GCM). Se guardan el texto cifrado y la clave de datos cifrada; la clave maestra no sale de KMS. CloudTrail registra llamadas a KMS; cada acceso mediante claves de datos ya obtenidas requiere auditoría aplicativa, según el [alcance KMS/Auth](compatibilidad-supabase-kms.md). La huella HMAC de búsqueda usa una clave propia, distinta de la de cifrado.
5. **Telemetría.** Ningún DNI, carga de KYC, clave ni testigo llega a registros, trazas ni analítica.
6. **Aceptación.** Vectores de normalización y de rotación escritos por el dueño, y búsqueda en registros que demuestre la ausencia de DNI y claves.

### 7.5 Evidencias y almacenamiento de objetos

1. Buckets privados y autorización por objeto. Las URL firmadas de descarga duran 5 minutos, según la propuesta inicial, y no valen como permiso permanente.
2. Antes de marcar una evidencia como recibida se verifican tamaño, tipo y hash, y pasa por cuarentena para validación y antimalware (`av_scan_status`).
3. Ninguna evidencia confirmada sin copia durable verificable. Si la copia independiente es asíncrona, el estado es `PENDING` y el RPO de objetos se fija antes de usarla (§13.5).
4. Las URL y las evidencias no pasan por cachés públicas. El PITR de la base no cubre objetos.
5. La retención por clase de documento, y la necesidad de Object Lock, dependen de dictamen [LEGAL→ABOGADO] (DP-10). No se activa retención indefinida e irreversible sobre datos personales sin decisión de conservación.
6. En R0 no se almacenan evidencias reales.

### 7.6 Transporte, cabeceras y límites de frecuencia

1. **TLS** entre cliente, API y base de datos.
2. **Cookies web**, cuando se usen: `Secure`, `HttpOnly`, `SameSite` adecuado y defensa CSRF. La portabilidad nativa conserva Bearer.
3. **CSP** definida según los orígenes reales de pago e identidad. Empieza en modo de medición y es obligatoria antes de producción. No se usan comodines para cerrar la comprobación.
4. **Respuestas privadas** con `Cache-Control: no-store`.
5. **Límites de frecuencia (H-17).** Inicio de sesión y recuperación, por cuenta seudónima más IP. Mutaciones, por usuario y recurso. Lectura pública, por IP, con protección perimetral. Los umbrales se fijan tras pruebas y responden 429 con `Retry-After`. Si el limitador no está disponible, eso no decide inventario ni saldo. Un webhook con firma válida se persiste y deduplica: no se descarta un pago solo por su IP.
6. **Aceptación.** Pruebas de abuso y de caída del limitador, sin presentar el limitador como garantía patrimonial.

## 8\. Catálogo de errores

### 8.1 Estructura de respuesta

    {
      "error": {
        "code": "ERR_ORDER_MIN_AMOUNT",
        "message": "El monto mínimo de compra no se alcanza.",
        "trace_id": "…"
      }
    }

**V8.** La respuesta pública lleva `code`, `message` y `trace_id`, y nada más. Se retira `details`: podía filtrar datos y llevaba importes como número JSON. Si una versión futura reintroduce detalles, los importes usarán el esquema `Money` de §11.1.

**RN-201.** Ningún mensaje revela existencia de cuentas, datos de terceros ni información que facilite enumeración. **RN-200.** El mensaje al usuario es llano y no culpabilizante. La causa técnica va al registro, nunca a la respuesta.

### 8.2 Catálogo

| Código                                         | HTTP | Mensaje al usuario                                                    |
| ---------------------------------------------- | ---- | --------------------------------------------------------------------- |
| `ERR_AUTH_INVALID_CREDENTIALS`                 | 401  | Los datos de acceso no son correctos.                                 |
| `ERR_AUTH_MFA_REQUIRED`                        | 401  | Se requiere verificación adicional.                                   |
| `ERR_AUTH_REAUTH_REQUIRED`                     | 401  | Vuelve a verificar tu identidad para continuar.                       |
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
| `ERR_REQUEST_INVALID`                          | 400  | No fue posible completar la solicitud.                                |
| `ERR_RESOURCE_NOT_FOUND`                       | 404  | No fue posible completar la solicitud.                                |
| `ERR_RESOURCE_VERSION_CONFLICT`                | 409  | No fue posible completar la solicitud.                                |
| `ERR_SERVICE_UNAVAILABLE`                      | 503  | No fue posible completar la solicitud.                                |
| `ERR_INTERNAL`                                 | 500  | No fue posible completar la solicitud.                                |

**V8.** Las cinco últimas filas son los códigos genéricos del contrato de §11. `ERR_RESOURCE_VERSION_CONFLICT` responde a un `expected_version` desactualizado. Las demás filas coinciden con el catálogo anterior, salvo el ejemplo de §8.1, que ahora usa el mensaje del catálogo. El contrato puede añadir códigos auxiliares documentados en [cierre de contratos](cierre-contratos.md). Esta tabla se sincroniza con `Error.code` del artefacto al consolidar. Los códigos que lanzan los disparadores siguen pendientes (P-08).

**Nota sobre los tres códigos de cumplimiento.** Sus mensajes son deliberadamente funcionales y neutros. **Ninguno indica análisis, sospecha ni reporte** (RN-142). Es la aplicación literal de la excepción de reserva del LBPF §0.3.

## 9\. Catálogo de eventos

### 9.1 Envoltura común

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

Los importes dentro de `payload` siguen el esquema `Money` de §11.1. Ningún evento lleva documentos, semillas ni credenciales.

### 9.2 Eventos de dominio

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

### 9.3 Eventos de decisión

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

### 9.4 Cálculo de indicadores

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

## 10\. Estructura de `market_config`

### 10.1 Documento

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

`market_config` es un documento interno en JSONB, así que sus importes son enteros en unidad mínima. Cuando un importe de configuración se expone por la API, se convierte al esquema `Money` (§11.1). La fuente de baliza está ratificada (D1): drand quicknet, con identidad de cadena y clave pública fijadas en `draw` (§5.8). Los valores `"…"` de `draw.beacon_source` y `PENDING_SELECTION` de `providers.beacon` en el ejemplo anterior son legado de V7 y se sustituyen al versionar la configuración; la codificación sigue en DP-04. Los parámetros de baliza tardía de §12.10 se añadirán a `draw` cuando se cierre DP-05. `providers.identity.vendor` sigue en `PENDING_CONTRACT`; Truora está en evaluación y no contratado (DP-20).

**Decisiones V8 sobre la configuración (A5, A8, C1, C2, C4).** El ejemplo anterior es de V7 y no contiene todavía los campos que exigen las decisiones de C1; se completan al versionar la configuración, sin inventar valores:

- `raffle_types` contiene solo tipos `T1`–`T8`; `T8` es la única capacidad en vivo y no hay entrada `LIVE`. Las categorías `P_C1` y `P_C2` se habilitan por `prize_categories`, no por tipos. Que una categoría P-C figure como `true` no habilita P-C mientras falte la lista de documentos por etapa (A8, DP-27).
- `raffle_type_params.T1` debe declarar la duración máxima y el desenlace al vencer (C1). El umbral del mínimo vendido no tiene valor aprobado (DP-24).
- `raffle_type_params.T7` debe permitir la duración propia de cada edición, que no supera el intervalo de la serie (C2). El contrato usa `edition_duration_minutes`; la comparación mensual usa instantes de calendario, no un mes fijo de 30 días.
- El MVP solo admite régimen `PAID` (C4).
- Los catálogos de `charge_kind` y `macrozone` están pendientes de Diego (DP-25).

### 10.2 Resolución de configuración

    -- Al publicar: se congela la version vigente en raffles.config_version_id.
    SELECT id FROM market_config_versions
     WHERE market_code = :m AND effective_to IS NULL;

    -- Al operar un sorteo: se usa SIEMPRE su version congelada, nunca la actual.
    SELECT config FROM market_config_versions WHERE id = :raffle_config_version_id;

**INV-15.** Ningún servicio consulta la configuración vigente para operar un sorteo ya publicado. Es caso de prueba obligatorio: cambiar la configuración y comprobar que los sorteos previos conservan sus reglas.

### 10.3 Adaptadores

| Interfaz                | Responsabilidad                                      | Adaptador PE          |
| ----------------------- | ---------------------------------------------------- | --------------------- |
| `IIdentityVerifier`     | Validar documento y prueba de vida                   | `identity.pe.default` |
| `IPaymentProvider`      | Preferencia, cobro, webhook, reembolso, conciliación | `psp.pe.mercadopago`  |
| `IPayoutProvider`       | **V8.** Pago al organizador y retiro de saldo        | Sin adaptador: depende de ASS-001 (DP-01) |
| `IInvoiceIssuer`        | Emisión de comprobante                               | `invoice.pe.default`  |
| `IRegistryProvider`     | Consulta registral de bienes                         | `registry.pe.default` |
| `ITaxDocumentValidator` | Validación de comprobante de compra del premio       | `taxdoc.pe.default`   |
| `IEntropyBeacon`        | Obtención de baliza pública por ronda                | Común a mercados      |

**La elección es dato; la integración es código.** Añadir un mercado con proveedores existentes es configuración. Añadirlo con proveedores nuevos requiere implementar adaptadores, nunca modificar el dominio.

**V8.** Los puertos de cobro y de pago al organizador son distintos. Elegir un proveedor de infraestructura no resuelve ASS-001. Los nombres de interfaz son nombres de puerto; la convención de nombres TypeScript se fija en D1. Mercado Pago es el PSP elegido; el contrato de su notificación está en §11.7 y en la [nota del PSP](mercado-pago.md). La evidencia de sandbox es de D1/R1 (DP-08). `IIdentityVerifier` queda neutral respecto del proveedor mientras se evalúa Truora (DP-20).

## 11\. Contratos de interfaz

El artefacto normativo de esta sección es [`libox_openapi_L3_V8_DRAFT.yaml`](libox_openapi_L3_V8_DRAFT.yaml) (OpenAPI 3.1; `2.0.0-draft.3`). Contiene las 61 operaciones del inventario de §11.7 y operaciones auxiliares que el inventario omitía, documentadas en [cierre de contratos](cierre-contratos.md) y sus notas. Este candidato no fija un conteo final: lo fija el coordinador al cerrar la integración del artefacto. Los ejemplos de esta sección son ilustrativos. Si un ejemplo contradice al artefacto, prevalece el esquema del artefacto. Ningún conteo cierra H-13 por sí solo.

### 11.1 Convenciones

| Aspecto       | Regla                                                    |
| ------------- | -------------------------------------------------------- |
| Base          | `/api/v2`. **V8:** el cambio de `Money` es incompatible con el contrato anterior, que usaba `/api/v1`. No se sustituye `/api/v1` en silencio |
| Formato       | OpenAPI 3.1. La nulabilidad se expresa con una unión explícita con `null`, nunca con `nullable` |
| Autenticación | `Authorization: Bearer <token>`. Las operaciones públicas declaran `security: []` y nunca heredan `bearerAuth` por accidente |
| Idempotencia  | `Idempotency-Key` obligatoria en toda mutación de dinero |
| Trazabilidad  | `X-Trace-Id` aceptada; si falta, se genera y se devuelve |
| Paginación    | Por cursor: `cursor`, `limit` de 1 a 100; `next_cursor` opaco o `null` |
| Importes      | **V8.** Objeto `Money`: `{"amount": "2500", "currency": "PEN"}` representa S/ 25,00. `amount` es una cadena decimal en unidad mínima, de 0 a 9223372036854775807, sin signo, sin ceros a la izquierda, sin fracciones ni exponentes. Nunca número JSON. Ratificado por Diego el 2026-09-30 |
| Concurrencia optimista | Los recursos consultables devuelven `version`; los comandos envían `expected_version` y reciben 409 `ERR_RESOURCE_VERSION_CONFLICT` si no coincide. El cliente no inventa versiones |
| Caché         | Las respuestas privadas llevan `Cache-Control: no-store` |
| Fechas        | ISO 8601 con desplazamiento del mercado                  |
| Versionado    | Ningún cambio incompatible sin nueva versión mayor       |

**Reglas de contenido.** Cada operación lleva `operationId` único, rol y ámbito, parámetros, cuerpo, respuesta de éxito y catálogo de errores aplicables, sin esquemas genéricos vacíos. El cliente no decide gates, precio calculado de la orden, fecha efectiva de límites ni estado de pago: el servidor rechaza esos campos. El contrato no expone la clave `service_role`, identificadores KYC sensibles ni datos de otros participantes. Las operaciones con autorización inferida llevan `x-authorization-status: proposed`. Se ratifican en bloque con el resto de propuestas en C2 (P-07). Los conflictos con el canon I-01 a I-11 están decididos (A1–A11, C1–C4) y su regla está en §4.1, §7 y este apartado; los datos que siguen pendientes figuran en DP-24 a DP-27. Scalar publica la documentación desde el mismo artefacto que genera los tipos y las pruebas de contrato.

**Validar no es calcular.** El esquema `Money` valida forma y rango. No calcula comisión, impuesto ni reparto, que son zona crítica.

### 11.2 Compra

    POST /api/v2/orders
    Headers: Authorization, Idempotency-Key, X-Trace-Id
    { "raffle_id": "uuid", "quantity": 5, "use_refund_credit": true,
      "device_id": "uuid" }

Respuesta `201`, con importes ilustrativos:

    { "order_id": "uuid", "raffle_id": "uuid", "quantity": 5,
      "status": "PENDING_PAYMENT",
      "unit_price":            { "amount": "500",  "currency": "PEN" },
      "gross_amount":          { "amount": "2500", "currency": "PEN" },
      "refund_credit_applied": { "amount": "500",  "currency": "PEN" },
      "cash_amount":           { "amount": "2000", "currency": "PEN" },
      "reserved_until": "2026-08-10T14:30:00-05:00",
      "resulting_probability": "…esquema Probability…",
      "payment": { "provider": "mercadopago", "preference_id": "…",
                   "checkout_url": "https://…" } }

`payment` puede ser `null`. La cabecera `X-Trace-Id` acompaña a toda respuesta.

Errores: `ERR_ORDER_MIN_AMOUNT` · `ERR_ORDER_INSUFFICIENT_INVENTORY` · `ERR_LIMIT_CONCENTRATION` · `ERR_LIMIT_SELF_IMPOSED` · `ERR_LIMIT_SELF_EXCLUDED` · `ERR_ORDER_SELF_PURCHASE` · `ERR_IDENTITY_VERIFICATION_REQUIRED` · `ERR_COMPLIANCE_*` · `ERR_RAFFLE_NOT_ACTIVE`.

**Orden de validación.** Autoexclusión → verificación de identidad → tramo de cumplimiento → autocompra → concentración → límite propio → importe mínimo → inventario. Se valida antes lo que es una prohibición absoluta y después lo que depende de disponibilidad, para que el mensaje al usuario sea el más informativo posible.

    GET /api/v2/orders/{id}

Devuelve estado real. Es el punto de recuperación tras pérdida de conexión (RN-218): la aplicación consulta y muestra estado inequívoco, nunca ambigüedad.

### 11.3 Tickets y participación

    GET /api/v2/me/tickets?cursor=&limit=
    GET /api/v2/me/tickets/{raffle_id}
    { "raffle_code": "LBX-202608-A7K3M",
      "ticket_numbers": [143,144,145],
      "pool": { "sold": 750, "total": 1000 },
      "probability": { "fraction": "3 / 750", "percent": 0.4,
                       "per_thousand_text": "4 de cada 1.000 tickets vendidos" },
      "independence_notice": "Los resultados anteriores no aumentan ni reducen la probabilidad de este sorteo. Cada sorteo es independiente." }

**No devuelve** identidad de otros participantes ni distribución de tenencia (R-10).

### 11.4 Verificación pública

    GET /api/v2/public/draws/{slug}          -- sin autenticacion
    GET /api/v2/public/draws/{slug}/pool     -- snapshot completo del pool

Devuelve el documento de prueba de §5.5. Indexable, cacheable, sin datos personales. Los ejemplos del artefacto son deliberadamente sintéticos y no constituyen pruebas criptográficas (ZC-13).

### 11.5 Resolución

    POST /api/v2/rooms/{id}/messages
    POST /api/v2/rooms/{id}/evidence
    POST /api/v2/rooms/{id}/claim
    POST /api/v2/rooms/{id}/shipping-quotes
    POST /api/v2/rooms/{id}/shipping-selection
    POST /api/v2/rooms/{id}/attest            -- SUPPORT_L2 / ADMIN_LEGAL_COMPLIANCE
    POST /api/v2/rooms/{id}/sla-extension
    GET  /api/v2/rooms/{id}/forensic-export   -- ADMIN

`POST /rooms/{id}/attest`:

    { "evidence_ids": ["uuid"], "winner_confirmed": true,
      "statement": "…", "signature_request_id": "uuid" }

**Ámbito P-C (A1/A9).** Solo `ADMIN_LEGAL_COMPLIANCE` solicita la atestación de
P-C1/P-C2: coincide con el solicitante de `ATTEST_PC`. Los otros roles de la
operación general se rechazan para P-C; no se crea una solicitud sin firmante
admisible ni se interpreta la lista general como excepción a la política.

Respuesta `201` con la atestación y **el estado de los seis gates de liquidación tras la evaluación**, para que el operador vea de inmediato si algo más bloquea el pago. La atestación excluye a finanzas (INC-07, en ejecución). **V8 (A9):** el cuerpo ya no lleva `second_signer_id`. En P-C, la segunda firma se pide con una `SignatureRequest` de `ATTEST_PC` y la atestación referencia esa solicitud ya firmada por un `ADMIN_SUPER` distinto del solicitante (§7.2); el servidor rechaza un firmante enviado por el cliente. Es un cambio incompatible del cuerpo frente a V7 y se registra como migración del contrato. Las evidencias y la exportación forense exigen autorización por recurso y quedan en `audit_access_events`.

### 11.6 Liquidación

    GET  /api/v2/clients/{id}/settlements
    GET  /api/v2/settlements/{id}
    POST /api/v2/settlements/{id}/execute     -- ADMIN_FINANCE
    POST /api/v2/settlements/batch-execute    -- ADMIN_FINANCE, lote
    { "settlement_id": "uuid", "status": "HELD",
      "gross_collected":    { "amount": "563000", "currency": "PEN" },
      "libox_fee_amount":   { "amount": "112600", "currency": "PEN" },
      "tax_amount":         { "amount": "…",      "currency": "PEN" },
      "chargeback_reserve": { "amount": "22520",  "currency": "PEN" },
      "net_payable":        { "amount": "427880", "currency": "PEN" },
      "gates": { "g1_draw": true, "g2_delivery": true, "g3_disputes": true,
                 "g4_chargeback": false, "g5_payout": true, "g6_ledger": true },
      "hold_until": "2026-08-25T00:00:00-05:00",
      "hold_reason": "Ventana de retención por contracargo",
      "version": 3 }

**El motivo y la fecha estimada se exponen siempre al organizador** (RN-102): un estado retenido sin explicación se interpreta como retención indebida. Los importes proceden del ejemplo anterior y no acreditan fórmulas, asientos ni PSP. `tax_amount` queda sin valor porque su cálculo es zona crítica (ZC-14). La ejecución de la liquidación es exclusiva de finanzas, lleva `Idempotency-Key` y `expected_version`, y depende de DP-01 y DP-02.

### 11.7 Inventario de operaciones de L3

Base `/api/v2`. El artefacto agrupa las 61 operaciones en 57 rutas: comparte los métodos de un mismo recurso y normaliza `/raffles/{slug}` y `/raffles/{id}` como `/raffles/{raffle_ref}`, que recibe slug en lectura y UUID en mutación. Cuando el inventario anterior no daba método, se ha concretado según la acción: consultas GET, comandos POST y reemplazos PUT. Esos métodos se marcan como "concretado".

| Familia | Método | Ruta | Método en el inventario anterior |
| ------- | ------ | ---- | -------------------------------- |
| Compra | POST | `/orders` | explícito |
| Compra | GET | `/orders/{id}` | explícito |
| Tickets | GET | `/me/tickets` | explícito |
| Tickets | GET | `/me/tickets/{raffle_id}` | explícito |
| Verificación pública | GET | `/public/draws/{slug}` | explícito |
| Verificación pública | GET | `/public/draws/{slug}/pool` | explícito |
| Resolución | POST | `/rooms/{id}/messages` | explícito |
| Resolución | POST | `/rooms/{id}/evidence` | explícito |
| Resolución | POST | `/rooms/{id}/claim` | explícito |
| Resolución | POST | `/rooms/{id}/shipping-quotes` | explícito |
| Resolución | POST | `/rooms/{id}/shipping-selection` | explícito |
| Resolución | POST | `/rooms/{id}/attest` | explícito |
| Resolución | POST | `/rooms/{id}/sla-extension` | explícito |
| Resolución | GET | `/rooms/{id}/forensic-export` | explícito |
| Liquidación | GET | `/clients/{id}/settlements` | explícito |
| Liquidación | GET | `/settlements/{id}` | explícito |
| Liquidación | POST | `/settlements/{id}/execute` | explícito |
| Liquidación | POST | `/settlements/batch-execute` | explícito |
| Identidad | POST | `/auth/register` | explícito |
| Identidad | POST | `/auth/verify-contact` | concretado |
| Identidad | POST | `/auth/login` | concretado |
| Identidad | POST | `/auth/refresh` | concretado |
| Identidad | POST | `/identity/verify` | concretado |
| Identidad | POST | `/identity/liveness` | concretado |
| Organizador | POST | `/clients` | explícito |
| Organizador | POST | `/clients/{id}/kyb` | concretado |
| Organizador | POST | `/clients/{id}/members` | concretado |
| Organizador | PUT | `/clients/{id}/payout` | explícito |
| Organizador | PUT | `/clients/{id}/capabilities` | concretado |
| Catálogo | GET | `/raffles` | explícito |
| Catálogo | GET | `/raffles/{slug}` | concretado |
| Catálogo | GET | `/raffles/{slug}/terms` | concretado |
| Sorteo | POST | `/raffles` | explícito |
| Sorteo | PATCH | `/raffles/{id}` | explícito |
| Sorteo | POST | `/raffles/{id}/submit` | explícito |
| Sorteo | POST | `/raffles/{id}/prize-valuation` | concretado |
| Sorteo | POST | `/raffles/{id}/pc-stages/{stage}` | concretado |
| Pagos | POST | `/webhooks/psp/{provider}` | explícito |
| Pagos | GET | `/reconciliation/{date}` | explícito |
| Pagos | POST | `/reconciliation/exceptions/{id}/resolve` | explícito |
| Sorteo ejecutado | POST | `/raffles/{id}/freeze` | explícito |
| Sorteo ejecutado | POST | `/raffles/{id}/execute-draw` | concretado |
| Sorteo ejecutado | POST | `/raffles/{id}/redraw` | concretado |
| Controversias | POST | `/disputes` | explícito |
| Controversias | POST | `/disputes/{id}/evidence` | concretado |
| Controversias | POST | `/disputes/{id}/adjudicate` | concretado |
| Saldo | GET | `/me/refund-credit` | explícito |
| Saldo | POST | `/me/refund-credit/withdrawals` | explícito |
| Protección | GET | `/me/limits` | explícito |
| Protección | PUT | `/me/limits` | explícito |
| Protección | POST | `/me/self-exclusion` | explícito |
| Protección | GET | `/me/spend-panel` | explícito |
| Cumplimiento | GET | `/compliance/cases` | explícito |
| Cumplimiento | POST | `/compliance/cases/{id}/decide` | explícito |
| Alarmas | GET | `/alarms` | explícito |
| Alarmas | POST | `/alarms/{id}/acknowledge` | explícito |
| Alarmas | POST | `/alarms/{id}/resolve` | concretado |
| Mercado | GET | `/markets/{code}/config` | explícito |
| Mercado | POST | `/markets/{code}/config` | explícito |
| Mercado | POST | `/markets/{code}/suspend` | concretado |
| Simulador | POST | `/public/pricing-simulator` — **sin autenticación** | explícito |

**Reglas por familia.** El webhook no usa el JWT del comprador. Para Mercado Pago, el artefacto concreta `POST /api/v2/webhooks/psp/mercadopago` para el tópico `payment`. La firma `x-signature` (componentes `ts` y `v1`) es un HMAC-SHA256 de un manifiesto formado por el `data.id` del query, `x-request-id` y la marca temporal. **No firma el cuerpo completo**, así que el cuerpo recibido no es autoritativo. El resultado del pago se confirma consultando la API autenticada de Mercado Pago en un endpoint fijo, y se contrastan referencia de orden, moneda e importe con los datos del servidor. La política de marca temporal y repetición se fija con reentregas reales del sandbox (DP-08), sin ventanas arbitrarias que descarten pagos legítimos retrasados ([nota del PSP](mercado-pago.md)). Los comandos de sorteo (`freeze`, `execute-draw`, `redraw`) exigen una identidad de servicio distinta del usuario y no reciben ganadores, semilla ni pool elegidos por quien llama. El registro responde de forma genérica para evitar enumeración. Identidad y KYB usan referencias a sesiones del proveedor vinculadas por el servidor, sin DNI ni documentos crudos en las respuestas. MFA, recuperación, subidas y lecturas versionadas que faltaban en el inventario se tratan como operaciones auxiliares ([cierre de contratos](cierre-contratos.md)). KYC y KYB siguen con un contrato neutral respecto del proveedor hasta cerrar DP-20.

**Estado de verificación.** El paquete C1 documenta pruebas estructurales del artefacto (validación 3.1, ejemplos, límites de `Money` e intercambios HTTP contra un servidor simulado) en los documentos de contrato. Ese servidor no valida permisos, firma del PSP, cabeceras de seguridad ni reglas de negocio. Esas pruebas no acreditan backend, migraciones, cálculos ni criptografía, y este candidato no las ha vuelto a ejecutar. El comportamiento contra el backend y los proveedores reales se prueba en D1/R1. Los endpoints de dinero, sorteo y concurrencia especifican contratos; su implementación la hace a mano su dueño ([zonas sin IA](../../../../.claude/rules/zonas-sin-ia.md)).

## 12\. Concurrencia, idempotencia y trabajos

### 12.1 Bloqueo autoritativo

**RN-56.** El bloqueo autoritativo sobre dinero e inventario es de base de datos. Un bloqueo distribuido en memoria es optimización de fast-fail; nunca la garantía, porque una conmutación puede producir dos poseedores del mismo bloqueo.

**V8.** PostgreSQL mantiene la autoridad sobre dinero e inventario. Upstash solo limita frecuencia. El proveedor de workflows reintenta y programa, pero no sustituye ni a la idempotencia ni a las transacciones patrimoniales. Su cupo de concurrencia (25 provisional) no es un mecanismo de exclusión.

> **[ZC-15 · zona sin IA · preservado]** §12.2 a §12.5 conservan el texto de V7. Son zona crítica: reserva de inventario, emisión, idempotencia y procesamiento único de webhooks. La emisión de §12.3 contabiliza T-04, T-05 y T-06 en el mismo instante: es H-01, pendiente por D-05. El pago tardío se rige por la política de §12.9. La implementación la escribe a mano su dueño y se acepta en R1 con F1–F5 y F7 (§14.8).

### 12.2 Reserva de inventario

La carrera real ocurre sobre el pool, no sobre el usuario. Serializar por usuario, como hacía la versión anterior, no la resuelve.

    UPDATE raffles
       SET tickets_reserved = tickets_reserved + :qty
     WHERE id = :raffle_id
       AND status = 'ACTIVE'
       AND tickets_reserved + :qty <= total_tickets
    RETURNING tickets_reserved;
    -- Cero filas afectadas -> ERR_ORDER_INSUFFICIENT_INVENTORY

Actualización condicional atómica, sin lectura previa. La liberación por expiración corre en el trabajo `release-expired-reservations`.

### 12.3 Emisión de tickets

Al confirmarse el pago, en una única transacción: bloqueo de fila del sorteo, asignación del rango de números con la actualización de §3.5, inserción de tickets, asientos T-01, T-02, T-04, T-05 y T-06, y publicación de eventos.

### 12.4 Idempotencia

    1. INSERT en idempotency_keys con status IN_FLIGHT.
       Conflicto de clave única -> ya existe:
         - COMPLETED con mismo request_hash -> devolver stored_response
         - COMPLETED con distinto hash      -> ERR_ORDER_IDEMPOTENCY_CONFLICT
         - IN_FLIGHT                        -> 409 con reintento sugerido
    2. Ejecutar la operación.
    3. Actualizar a COMPLETED con la respuesta.

**La clave la genera el cliente por intento.** No se deriva del contenido: dos compras legítimas idénticas separadas en el tiempo producirían el mismo hash y la segunda devolvería la primera, dejando al usuario sin sus tickets.

### 12.5 Webhooks

    1. Validar firma y ventana anti-repetición.
    2. Persistir en psp_events con la carga original y su hash.
       Conflicto de deduplicación -> marcar DUPLICATE y responder 200.
    3. Procesar con monotonía de estado: si status_rank entrante <= actual, ignorar.
    4. Marcar PROCESSED. Ante fallo, FAILED con reintento exponencial y alarma.

Se responde `200` incluso ante duplicado: un error haría reintentar indefinidamente al proveedor.

**Nota V8 sobre el texto heredado.** El procedimiento anterior se conserva tal como estaba. Con Mercado Pago, "validar firma" significa validar `x-signature` sobre el manifiesto de §11.7, no sobre el cuerpo. La carga original se guarda como evidencia, pero no es autoritativa: el estado del pago sale de la consulta autenticada al PSP. Si falla la persistencia, se responde 503 para que el proveedor reintente. La ejecución única del procesamiento sigue siendo zona sin IA.

### 12.6 Trabajos programados

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
| `create-next-partitions`             | 24 h       | Particiones del mes siguiente. **V8 (B3):** lo ejecuta `pg_cron` en la base con el rol dueño; Trigger.dev solo lee `partition_status` y alarma (§1.3) |
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

**Ejecutores (V8).** Son 30 trabajos: nueve cada minuto, dos cada 15 minutos, cuatro cada hora, catorce diarios y uno cada 10 segundos. En un mes de 30 días suman unas 657.060 activaciones. `create-next-partitions` corre en `pg_cron` con el rol dueño (B3, §1.3), para no sacar esa credencial de la base. Los otros 28 de los 29 primeros, y la tarea que vigila `partition_status`, se programan en Trigger.dev, cuyo cron no baja de un minuto; la frecuencia de esa vigilancia no está fijada. `dispatch-outbox` lo dispara un ticker de Supabase Cron cada 10 s contra un endpoint privado (§12.7). Fuera del DDL de particiones, ningún trabajo se ejecuta como función larga dentro de Supabase Cron, que admite como máximo 8 trabajos concurrentes y 10 minutos por trabajo. Un cron de un minuto no acredita la cadencia de 10 s. La ejecución única de los trabajos que tocan dinero, inventario o sorteo es zona crítica, y su código lo escribe a mano su dueño.

**Con D-10** el ejecutor se reevalúa. La propuesta es River en el worker Go, que también despacharía el outbox cada 10 s sin ticker externo. Hasta confirmarla rige el reparto anterior.

### 12.7 Outbox y despacho

Contrato del despachador. No incluye la implementación de concurrencia:

1. Autentica al emisor con un secreto dedicado y rotable, nunca con una clave publicable. El secreto puede guardarse en el Vault del proveedor.
2. Recupera lotes acotados del outbox que la transacción de dominio persistió.
3. Publica identificadores y versión del evento. Excluye documentos, semillas y credenciales.
4. Marca como despachado solo después de que el destino acepte el evento de forma durable. Si cae entre publicar y confirmar, puede repetir la entrega; el consumidor produce un único efecto.
5. Tras un fallo, recupera desde la base, no desde memoria ni solo desde `pg_net`. `pg_net` no es una cola durable de negocio.

La cadencia no garantiza entrega durante una caída. Objetivo: despacho en menos de 60 s en operación normal y alarma alta a partir de 5 minutos (§13.3).

### 12.8 Reintentos y consola interna

Los reintentos tienen plazo de negocio, backoff acotado y alarma. Que expire un intento no cancela los efectos en el PSP ni autoriza generar otra clave de cobro. Los casos agotados pasan a la consola interna con `trace_id`, estado real, última respuesta y acción permitida. La consola diagnostica y reintenta cada incidente de F1–F7 con autorización y auditoría, sin saltarse los gates. Sorteos y pagos no se reintentan con SQL manual. La consola es una épica de R1.

### 12.9 Pago tardío (H-16, F7)

**Política del candidato (P-02) [LEGAL→ABOGADO].** Un pago aprobado después de vencer la reserva, o después de congelarse el pool, no emite tickets ni amplía el pool. El sistema registra una excepción, notifica y concilia. La devolución íntegra al medio de pago original se hace con una operación idempotente cuando existan T-03 (DP-03) y la confirmación de devolución de Mercado Pago en sandbox (DP-08). No se convierte automáticamente en saldo interno ni se contabiliza comisión como si hubiera habido participación. La custodia (DP-01) sigue abierta. La política forma parte del candidato; el asiento de devolución y la custodia deben estar resueltos antes de mover dinero real en R1.

### 12.10 Baliza tardía (H-12, F6)

**Norma del candidato (P-03).** Si la ronda comprometida no está disponible en `earliest_execution_at`, salta una alarma a los 5 minutos. A los 30 minutos se escala a incidente. Vencer ese plazo **no** autoriza otra ronda, otra semilla ni un sorteo manual. El compromiso y los fondos siguen bloqueados. Antes de cerrar C1 falta decidir qué pasa tras el incidente, reanudar o cancelar (DP-05), y la fuente de baliza (DP-04).

## 13\. Observabilidad, operación y recuperación

### 13.1 Trazabilidad

`trace_id` se genera en el borde y se propaga por toda la cadena: registro, base de datos, eventos, notificaciones y respuestas. La consulta por `trace_id` reconstruye la línea de tiempo completa.

### 13.2 Objetivos de nivel de servicio

| Métrica                                                 | Objetivo       |
| ------------------------------------------------------- | -------------- |
| Disponibilidad de superficies públicas                  | 99,5 % mensual |
| Latencia p95 de API propia                              | \< 500 ms      |
| Latencia p95 de creación de orden, excluyendo proveedor | \< 800 ms      |
| Retraso de despacho del outbox                          | \< 60 s        |
| Tiempo de procesamiento de webhook                      | \< 5 s         |

**Se mide la API propia separada del proveedor.** Mezclarlas hace incumplir el objetivo por causas ajenas y vuelve inútil la métrica. Son objetivos del sistema. Los planes contratados no compran un SLA para toda la aplicación.

### 13.3 Alertas técnicas

| Alerta                                                         | Severidad |
| -------------------------------------------------------------- | --------- |
| Divergencia de invariante contable (L-01 a L-07)               | Alta      |
| Outbox con retraso superior a 5 minutos                        | Alta      |
| Cola de auditoría de emergencia no vacía por más de 15 minutos | Alta      |
| Tasa de webhooks fallidos superior al 1 %                      | Alta      |
| Falta de partición para el mes siguiente                       | Alta      |
| **V8.** Filas en una partición `DEFAULT` (B4; procedimiento manual de §1.3) | Alta |
| `ERR_DRAW_COMMITMENT_MISMATCH` en cualquier ocurrencia         | Alta      |
| **V8.** Baliza no disponible 5 minutos después de `earliest_execution_at` | Alta |
| **V8.** Número de `ADMIN_SUPER` activos igual a uno            | Alta      |
| **V8.** Gasto mensual proyectado por encima de US$175, US$200 o US$215 | Media     |
| Excepciones de conciliación fuera de plazo                     | Media     |
| Latencia p95 por encima del objetivo durante 15 minutos        | Media     |
| Bloqueo registral próximo a vencer con sorteo activo           | Media     |

### 13.4 Runbooks

| Incidente                     | Procedimiento resumido                                                                                                                             |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Proveedor de pagos caído      | Suspender ventas del mercado en nivel L1; conservar sorteos activos; comunicar; reanudar y liberar reservas expiradas                              |
| Webhooks no llegan            | Conciliar por consulta activa contra el proveedor; reprocesar desde `psp_events`; verificar firma y clave                                          |
| Divergencia de ledger         | Congelar liquidaciones del ámbito afectado; identificar el asiento por `trace_id`; corregir con T-14 y segunda firma; nunca editar `journal_lines` |
| Sorteo con pool incorrecto    | No re-ejecutar. Congelar liquidación, abrir caso, publicar comunicación; la corrección exige decisión de dirección y queda registrada              |
| Saldo de reembolso divergente | Recomputar desde `refund_credit_entries`; la caché nunca es la verdad                                                                              |
| Gravamen sobrevenido en P-C   | Suspender el sorteo de inmediato, notificar, evaluar cancelación con reembolso íntegro                                                             |
| **V8.** Baliza tardía         | Aplicar §12.10: alarma, incidente a los 30 minutos, compromiso y fondos intactos; nunca otra ronda ni sorteo manual                                |
| **V8.** Despacho detenido     | Revisar el ticker y el secreto del emisor; reanudar desde el outbox persistido; confirmar que el consumidor no duplica efectos                     |
| **V8.** Pérdida de base de datos | Restaurar por PITR en un entorno aislado, verificar integridad, conciliar contra el PSP y el outbox, restaurar objetos y claves, y solo después reabrir |

### 13.5 Recuperación ante desastres (H-15)

**Objetivos del candidato para R1 (P-04).** Son objetivos del sistema y no un SLA comprado ni un cumplimiento demostrado.

| Activo | Objetivo propuesto | Evidencia exigida antes de operar |
| ------ | ------------------ | --------------------------------- |
| PostgreSQL | RPO ≤ 5 min; RTO ≤ 4 h; PITR de 7 días más copia independiente | Restauración aislada, integridad y conciliación contra el PSP y el outbox |
| Evidencias recibidas | Ninguna evidencia confirmada sin copia durable verificable | Restaurar original, hash y metadatos, y verificar permisos |
| Secretos y semilla cifrada | Recuperación de claves autorizada y separada de las copias de datos | Ensayo sin imprimir secretos, con control de acceso y registro |
| Workflows | Reanudar desde el estado persistido sin duplicar efectos | F3 y F6, más reentrega de eventos |

No se afirma RPO cero entre proveedores. El PITR de la base no cubre objetos (§7.5). El RTO incluye objetos, credenciales y conciliación, y se mide en ensayo. No se deduce del PITR. Se hace un ensayo de restauración antes de R1 y luego periódicamente.

### 13.6 Observabilidad

Se miden la antigüedad máxima del outbox y sus percentiles, el backlog, los reintentos, los webhooks fallidos, las conexiones a la base, las particiones futuras, el gasto y los vencimientos. Ninguna métrica ni traza lleva DNI, cargas de KYC, testigos ni secretos (§7.4).

### 13.7 Gasto

Se aplica el techo de §0.4. Se definen límites por proveedor antes de contratar, sin corte ciego de consumo. Si el gasto proyectado supera el techo, se frenan las ventas nuevas de forma operativa y se conservan la conciliación y la recuperación.

## 14\. Estrategia de pruebas

Ninguna prueba de esta sección está ejecutada contra el sistema V8, porque el backend no existe. Son criterios de aceptación. Las de las zonas críticas se ejecutan contra el código escrito a mano por su dueño.

### 14.1 Pirámide

| Nivel             | Alcance                                       | Cobertura mínima                 | Ejecución        |
| ----------------- | --------------------------------------------- | -------------------------------- | ---------------- |
| Unitaria          | Reglas de negocio, cálculo, transiciones      | 80 % en dominio financiero       | Cada integración |
| Integración       | Flujos entre agregados con base de datos real | Todos los casos de uso de dinero | Cada integración |
| Contrato          | Conformidad con el artefacto OpenAPI de V8    | 100 % de endpoints               | Cada integración |
| Propiedad         | Invariantes                                   | Ver §14.2                        | Cada integración |
| Extremo a extremo | Recorridos por rol                            | Los 12 recorridos críticos       | Diaria           |
| Carga             | Presupuesto de rendimiento                    | —                                | Semanal          |
| Ensayo real       | Ciclo completo con dinero real                | Gate de fase                     | Una vez por fase |

El CI de código entra en D1: backend Go (build, `go vet`, linter, pruebas, migraciones sobre PostgreSQL efímero con el esquema V8 y conformidad con OpenAPI) y frontend TypeScript (build, lint, typecheck, pruebas y cliente generado).

### 14.2 Pruebas de propiedad

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
| **V8.** `prop_min_super_admins`  | Ninguna secuencia de revocaciones y suspensiones deja menos de dos `ADMIN_SUPER` activos (INV-38)                           |

`prop_refund_solvency` fallará con la secuencia contable heredada mientras siga abierto H-01. Es el comportamiento esperado de la prueba, no un defecto de la prueba.

### 14.3 Casos obligatorios de control de acceso

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
| **V8.** Revocar a un `ADMIN_SUPER` con tres o más activos                   | **Admitido**                             |
| **V8.** Revocar al penúltimo `ADMIN_SUPER` (quedaría uno)                   | `ERR_RBAC_LAST_SUPER_ADMIN`              |
| **V8.** Suspender la cuenta interna del penúltimo `ADMIN_SUPER`             | `ERR_RBAC_LAST_SUPER_ADMIN`              |
| **V8.** Dos revocaciones concurrentes de titulares distintos, con tres activos | Una admitida; la otra `ERR_RBAC_LAST_SUPER_ADMIN` |
| **V8.** Reactivar por `UPDATE` un subrol por encima del techo de quien lo otorga | `ERR_RBAC_GRANT_CEILING`            |
| **V8.** Reactivar `ADMIN_FINANCE` sin segunda firma                         | `ERR_RBAC_SECOND_SIGNATURE_REQUIRED`     |
| **V8.** Reactivar una asignación que viola INC-01                           | `ERR_RBAC_INCOMPATIBLE_SUBROLE`          |
| **V8.** Acceso interno con sesión de nivel `aal1`                           | `ERR_AUTH_MFA_REQUIRED`                  |
| **V8.** Acceso interno tras 30 minutos sin actividad humana, habiendo renovado testigos | `ERR_AUTH_TOKEN_EXPIRED`     |
| **V8.** Acción sensible con reautenticación de hace más de 5 minutos (A10)  | `ERR_AUTH_REAUTH_REQUIRED`               |
| **V8.** `ADMIN_SUPER` firma `MARKET_RESUME` solicitado por otro `ADMIN_SUPER` (A1) | **Admitido**                      |
| **V8.** `ADMIN_SUPER` firma su propia `SUBROLE_GRANT` (INC-11, en ejecución) | `ERR_RBAC_SELF_SIGNATURE`               |
| **V8.** Firmante fuera de la política del `action_code`, p. ej. `ADMIN_FINANCE` en `VALUATION_V2_COSIGN` (A1) | `ERR_RBAC_FORBIDDEN` |
| **V8.** `action_code` sin fila en la política de firma                      | Rechazo: la solicitud no es firmable     |
| **V8.** Atestación P-C con `second_signer_id` en el cuerpo, sin `SignatureRequest` `ATTEST_PC` firmada (A9) | Rechazo de validación del contrato |
| **V8.** `VALUATION_REJECTED`, `LEGAL_GATE_OBSERVED` o `LEGAL_GATE_REJECTED` sin motivo (A6) | Rechazo de la transición        |
| **V8.** `REJECT` en moderación con motivo fuera de la lista A11.1, u `OTHER` sin texto | Rechazo de validación         |
| **V8.** Decidir KYB con un subrol distinto de `ADMIN_COMPLIANCE` (A7)        | `ERR_RBAC_FORBIDDEN`                     |
| **V8.** Habilitar la capacidad `LIVE` o `P_C1` como tipo de sorteo (A5)      | Rechazo de validación                    |
| Suspender la propia cuenta interna                                          | `ck_susp_self`                           |
| Restaurar una suspensión sin motivo                                         | `ck_susp_restore`                        |

**V8.** Los casos "revocar al penúltimo: admitido" y "revocar al último: rechazado" de la versión anterior contradecían INV-38 del PRD y quedan derogados. Los casos nuevos fallarán contra el código heredado de ZC-11, como se espera.

**V8 (decisiones C1).** Los casos de firma, reautenticación, rechazos manuales, motivos de moderación, KYB y capacidades derivan de A1–A11. Donde el resultado esperado no tiene aún código de error en §8.2, lo fija el dueño del contrato (P-08); no se inventa uno nuevo para estos casos. Su comprobación es lógica de servicio en zona sin IA (ZC-16) y se ejecuta contra el backend en D1.

### 14.4 Concurrencia

| Prueba                      | Escenario                                                                                                                        |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `conc_last_tickets`         | 50 solicitudes simultáneas por los últimos 3 tickets: exactamente 3 emitidos                                                     |
| `conc_duplicate_webhooks`   | Mismo evento 10 veces en paralelo: un solo procesamiento                                                                         |
| `conc_double_click`         | Misma clave de idempotencia en paralelo: una orden                                                                               |
| `conc_refund_credit`        | Uso simultáneo del mismo saldo: sin saldo negativo                                                                               |
| `conc_double_draw`          | Dos ejecuciones simultáneas del mismo sorteo: una persiste, la otra recibe `ERR_DRAW_ALREADY_EXECUTED`                           |
| `conc_webhook_cross_month`  | El mismo evento de proveedor recibido en dos meses distintos: **un solo procesamiento**. Verifica la corrección de deduplicación |
| `conc_room_seq_cross_month` | Sala que cruza de mes: la secuencia no se repite y la cadena de hashes permanece continua                                        |

### 14.5 Verificación del sorteo

Los cinco vectores de §5.7 se ejecutan en cada integración. **La implementación de verificación debe ser independiente de la de ejecución**, escrita por persona distinta: una verificación que comparte código con la ejecución no verifica nada. **V8:** los vectores solo sirven cuando llevan salidas calculadas por una implementación humana independiente y verificadas por otra (H-10). Hasta entonces esta prueba no puede aprobarse.

### 14.6 Verificación estática conductual

| Regla                    | Verifica                                        | Efecto            |
| ------------------------ | ----------------------------------------------- | ----------------- |
| LINT-003                 | Animación superior a 240 ms en zona de decisión | **Bloquea merge** |
| LINT-004                 | Animación infinita en zona de decisión          | **Bloquea merge** |
| LINT-005                 | Opción monetaria o de comunicación premarcada   | **Bloquea merge** |
| LINT-001, 002, 006 a 010 | Resto del catálogo conductual                   | Advierte          |

Se ejecutan sobre el árbol de componentes y sus metadatos declarados, no sobre el sistema en ejecución.

### 14.7 Ensayo con dinero real

Gate binario de fase. Ciclo completo con importe simbólico real: alta de organizador, KYB, verificación de premio, gate legal, publicación, verificación de identidad del comprador, compra con pago real, emisión de tickets, congelamiento con compromiso, ejecución con baliza, verificación pública por un tercero, apertura de sala, evidencia, atestación, evaluación de los seis gates, liquidación con pago real, y comprobación de los siete invariantes contables.

**Ningún resultado parcial lo satisface.** Requiere haber resuelto antes DP-01 a DP-03.

### 14.8 Pruebas de fallo inyectado F1–F7

Obligatorias en la definición de terminado del flujo de compra (R1) y del motor de sorteo. Se ejecutan contra PostgreSQL real y el sandbox del PSP, no solo con mocks. Cada incidente se diagnostica y reintenta desde la consola interna, sin SQL manual (§12.8).

| Caso | Fallo inyectado | Resultado exigido | Evidencia |
| ---- | --------------- | ----------------- | --------- |
| F1 | Webhook duplicado, en serie y en concurrencia | Un procesamiento; ambas llamadas responden 200 | Base real, evento del sandbox y conteo de efectos |
| F2 | El PSP acepta el pago y la llamada agota el tiempo | La orden queda pendiente; la consulta o la conciliación la resuelve sin doble cobro | Misma clave, consulta al proveedor y traza del timeout |
| F3 | El proceso muere tras el commit y antes de publicar | El outbox entrega al reanudar, sin pérdida | Reinicio real y trazas de persistencia y consumo |
| F4 | Reembolso pedido dos veces | Un solo efecto patrimonial | Contabilidad validada (requiere T-03) y estado en el PSP |
| F5 | N compras concurrentes por el último boleto | Exactamente una emisión; cero sobreventa | Concurrencia en PostgreSQL, invariantes y respuesta a los perdedores |
| F6 | Sorteo disparado dos veces, reinicio del ejecutor o baliza tardía | Una ejecución; espera acotada con alarma (§12.10) | Implementación humana independiente y fixture de baliza |
| F7 | Pago posterior al vencimiento de la reserva o al congelamiento del pool | Sin ticket tardío; conciliación y devolución según §12.9 | Política P-02, T-03 (DP-03) y caso en el sandbox de Mercado Pago |

Son criterios de prueba, **no pruebas pasadas**.

### 14.9 Pruebas de base de datos, seguridad y recuperación

| Prueba | Resultado exigido |
| ------ | ----------------- |
| Permisos por login (§1.4) | `UPDATE` y `DELETE` sobre tablas de solo agregación y financieras fallan con la credencial real de la aplicación; `anon` y `authenticated` no leen el dominio |
| Particiones (§1.3) | Inserción en las doce tablas; paso de mes; alarma si falta la partición siguiente |
| Ledger (H-04) | Se rechazan el asiento desbalanceado, la cuenta inexistente, la moneda distinta y las líneas añadidas después del cuadre. Código humano (ZC-09) |
| HMAC de documento (§7.4) | Vectores de normalización y rotación; unicidad entre versiones de clave; sin DNI en registros |
| Sesión (§7.3) | La renovación y el sondeo no cuentan como actividad; revocación y cambio de rol efectivos en el siguiente acceso |
| Límites de frecuencia (§7.6) | 429 con `Retry-After`; la caída del limitador no afecta a inventario ni saldo |
| Contrato `Money` (§11.1) | El esquema rechaza números JSON, signos, ceros a la izquierda, fracciones y desbordamiento; el cliente tipado no acepta `number` |
| Restauración (§13.5) | Ensayo cronometrado de base, objetos y claves, con conciliación posterior |

## Anexo A — Orden de migraciones

| \#  | Migración                | Contenido                                                                                                                                                                                                           |
| --- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 001 | Dominios y roles         | Tipos de dominio, roles de grupo. **V8:** logins técnicos, revocación a `PUBLIC`, privilegios por defecto y `GRANT` por tabla (§1.4) |
| 002 | Mercado                  | `markets`, `market_config_versions`, requisitos, categorías, feriados                                                                                                                                               |
| 003 | Identidad                | `users`, **V8:** `auth_identities`, `app_sessions`, dispositivos, documentos bloqueados                                                                                                                            |
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
| 025 | Particiones              | **V8:** particiones del mes en curso y del siguiente para las doce tablas de §1.3, y trabajo de creación                                                                                                           |
| 026 | Datos semilla            | Mercado PE, cuentas contables por moneda, reglas de fuerza probatoria, instrumentos de encuesta, incompatibilidades de subrol, **matriz de otorgamiento**, **V8:** `fsm_transitions` completa con comprobación de cobertura, y arranque de administración conforme a DP-16 |

**Propiedad humana.** Contienen código de zonas sin IA las migraciones siguientes. El código heredado sin hallazgo se conserva; todo cambio o aporte (§0.5) lo escribe a mano su dueño: 005 (ZC-01, excepciones de tasa), 006 (ZC-01), 007 (ZC-02), 008 (ZC-03), 010 (ZC-04), 011 (ZC-05), 012 (ZC-06, ZC-07), 013 (ZC-16), 015 (ZC-09), 016 (ZC-08), 017 (ZC-10), 024 (ZC-11), 025 (particiones de `journal_lines`) y 026 (cuentas contables e incompatibilidades).

**Tablas sin migración nombrada.** El anexo heredado no nombra expresamente varias tablas añadidas entre V4 y V7: `platform_capabilities`, `operating_windows`, `feature_toggle_log`, `fee_schedules`, `client_fee_levels`, `fee_exceptions`, `free_entry_campaigns`, `free_entry_grants`, `substitute_guarantees`, `promotional_plans`, `promotional_plan_usage`, `audit_access_events`, `organizer_referral_codes`, `user_attributions`, `subscription_plans`, `subscriptions`, `partners`, `benefits`, `benefit_redemptions`, `subrole_grant_matrix`, `internal_account_suspensions` y `fsm_transitions`. El SQL V8 debe asignar cada una a una migración y comprobarlo en la ejecución de §0.2.1.

**Motor.** El esquema V7 ya corre en PostgreSQL 17.11 local, según evidencia del coordinador. La secuencia V8 completa se valida en PostgreSQL 17 para cerrar C1, y en Supabase en R1 (DP-09).

## Anexo B — Materias pendientes de dictamen

Los siguientes valores figuran como `PENDING_LEGAL_OPINION` en la configuración y **deben resolverse antes de operar**: aplicabilidad del impuesto sobre la comisión, su base y su contribuyente (§6.2.1) · emisor del comprobante y base imponible · autoridad y tipo de documento del gate legal · calificación como sujeto obligado y sus umbrales · admisibilidad de la custodia de fondos · plazo y renovación del bloqueo registral · tratamiento tributario del premio para el ganador · límite de responsabilidad oponible. [LEGAL→ABOGADO]

**Añadidas en V8** [LEGAL→ABOGADO]: custodia del dinero (ASS-001, DP-01) · momento de reconocimiento de comisión e impuesto (H-03, DP-02) · devolución al medio de pago original y pago tardío (DP-03, P-02) · retención por clase de documento y necesidad de Object Lock (DP-10) · retención de `operation_register` y de los registros de pagos (DP-12).

**Añadidas por las decisiones C1** [LEGAL→ABOGADO]: aprobadores de las etapas P-C E2, E4 y E7 (A4) · observación y rechazo del gate legal (A6) · lista cerrada de documentos por etapa P-C (A8, DP-27) · expiración de T1, mínimo vendido y aviso al comprador, por protección al consumidor y reglas de sorteos promocionales (C1, DP-24) · plazo de `psp_events` como soporte contable del pago y de `operation_register` (B6). La fianza propuesta por Cowork no está aprobada y no forma parte de estas materias como regla vigente (§0.8).

## Anexo C — Criterios de cierre por fase

Cada fase exige solo lo suyo. Una prueba de D1/R1 no condiciona C1, y una decisión que bloquea R1 no condiciona C2. Las restricciones de las zonas sin IA y los hallazgos pendientes siguen vigentes en todas las fases.

**C1 — candidato listo.** Se cierra cuando existen:

1. **SQL candidato desplegable.** Esquema V7, más la capa no crítica (particiones, ACL base, semillas no críticas y DDL de identidad de §2.2), más los aportes humanos de §0.5: H-04, H-07, H-08 (con arranque según DP-16), H-09 y el DDL de semilla cifrada de H-12. La ACL sigue las clases de B1 (§1.4); las seis tablas reclasificadas (ZC-17) y la `DEFAULT` y ACL de `journal_lines` (ZC-18) las escribe el dueño humano. Todo se ejecuta sobre PostgreSQL 17 con cero errores y con las pruebas negativas de §0.2.1.
2. **Contratos.** OpenAPI 3.1 en `2.0.0-draft.3`, con las 61 operaciones del inventario y las auxiliares documentadas, y pruebas estructurales en verde; el conteo final lo fija el coordinador. Los conflictos I-01 a I-11 están decididos (A1–A11, C1–C4) e integrados en este candidato (DP-21). Siguen sin valor el mínimo de T1, la lista de documentos P-C y los catálogos `charge_kind` y `macrozone` (DP-24, DP-25, DP-27); el contrato los deja explícitamente pendientes y no se anuncian como completos.
3. **Vectores de sorteo.** Especificación cerrada (DP-04), verificador sin ambigüedad (H-11) y salidas de los vectores calculadas por dos implementaciones humanas independientes (H-10). Resolución tras la espera de baliza (DP-05).
4. **Transcripción verificada.** `test_preserved_l3.py` en verde tras la última edición del candidato.

C1 **no** exige: confirmación contable ni T-03 (H-01–H-03, pendientes por D-05), ASS-001, contrato de KYC o KYB, sandbox de Mercado Pago, pruebas de backend ni ensayos de restauración. El código heredado sin hallazgo no se reescribe.

**C2 — emisión.** Un solo acto con: identidad en los cuatro lugares; changelog con "decisión que invalida"; autonomía comprobada; ratificación en bloque de las propuestas P-01 a P-09; V7 archivada sin editar; ningún bloque marcado **legado preservado, no listo para emisión en C2** sin resolver por el SQL V8 o el aporte humano; alta de V8 en BASELINE y en el Registro §1; `verify_corpus.py` con cero fallos; y correlación con el doc 20 (DP-19). Los hallazgos contables se emiten con su estado pendiente explícito (§6), no corregidos.

**D1/R1 — pruebas de dominio y operación.** D1 levanta el freeze y añade el CI de código Go y TypeScript. En D1/R1 se ejecutan: §14.3, §14.4 y §14.9 contra el backend; F1–F7 contra PostgreSQL y el sandbox de Mercado Pago; KYC y KYB con el proveedor que resulte de DP-20; el esquema en Supabase (DP-09); y el ensayo de restauración (§13.5). Antes de mover dinero real deben estar resueltos DP-01, DP-02, DP-03, DP-08, DP-10 y DP-12.

*LIBOX Especificación Técnica L3 V8, borrador DRAFT-8, no emitido. Implementa LIBOX PRD BLUEPRINT MVP V9 (nivel L2), gobernado por LBPF V3 (nivel L0). Este documento no crea reglas de negocio: las implementa.*
