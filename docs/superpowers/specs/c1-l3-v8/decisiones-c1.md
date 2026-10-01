---
title: C1 — paquete de decisiones para el cierre
status: aprobado
tags: [r0, c1, l3-v8, decisiones]
updated: 2026-10-01
description: Resumen de las decisiones de dominio de C1 tomadas por Diego el 2026-09-30, con enlaces a cada ficha y lo que queda abierto.
---

# Paquete de decisiones de C1

Diego resolvió el 2026-09-30 las decisiones de dominio que bloqueaban integrar
contratos, SQL y configuración en el borrador L3 V8 ([estado de C1](estado-c1.md)).
Cada ficha conserva el conflicto, las opciones y la recomendación.

**Alcance.** Son decisiones operativas para el borrador: no cambian el canon
(CD-07) hasta emitir el conjunto reconciliado. No incluyen importes, porcentajes, comisiones ni
impuestos (ver el [bloque E](decisiones-c1-configuracion.md#e-datos-que-no-se-proponen)).
Donde alimentan código de las [zonas sin IA](../../../../.claude/rules/zonas-sin-ia.md),
solo fijan la regla; el código sigue siendo implementación humana de Diego.
Lo marcado [LEGAL→ABOGADO] es provisional hasta su ratificación.

**Tras Cowork.** Esta aprobación conserva su alcance del 30/09. El nuevo flujo
de fianza y sus parámetros se registran aparte en la
[reconciliación](reconciliacion-linea-base.md); no heredan el estado `aprobado`
de esta ficha. La extensión de T1 bajo mínimo requiere resolver el cambio de
cancelación a cobertura antes de integrarlo en las bases.

| Nota | Fichas |
|---|---|
| [Firmas y aprobadores](decisiones-c1-firmas.md) | A1–A4 |
| [Capacidades, transiciones y roles](decisiones-c1-transiciones.md) | A5–A11 |
| [Base de datos y cifrado](decisiones-c1-datos.md) | B1, B1-bis, B2–B6 |
| [Configuración y sorteo](decisiones-c1-configuracion.md) | C1–C4, D1, E |

## Resumen

| Ficha | Decisión |
|---|---|
| A1 | Segunda firma por `action_code`: otra persona siempre; otro subrol salvo en acciones propias de `ADMIN_SUPER`, donde firma otro `ADMIN_SUPER` |
| A2 | `ADMIN_MODERATION` cofirma la banda V2, sin escritura |
| A3 | Observan quienes aprueban la banda; sin subrol nuevo |
| A4 | Aprobadores por etapa P-C según el PRD V9 [LEGAL→ABOGADO] |
| A5 | Se retira `LIVE`; P-C1/P-C2 en un campo de categorías |
| A6 | Rechazo manual de valoración; observar y rechazar el gate legal |
| A7 | `ADMIN_COMPLIANCE` decide KYB |
| A8 | P-C entra en el MVP, con la lista de documentos del abogado |
| A9 | La atestación usa `SignatureRequest` |
| A10 | Reautenticación válida 5 minutos |
| A11 | Motivos de rechazo en moderación aprobados; §7.2 prevalece, INC-07 solo en ejecución |
| B1 | Clases de privilegios aprobadas; seis tablas pasan a `reservado_humano` |
| B1-bis | Datos personales cifrados con AWS KMS (cifrado de sobre) y huella HMAC para buscar |
| B2 | Un login por componente; `libox_migrate` dueño |
| B3 | `pg_cron` crea particiones; Trigger.dev alerta |
| B4–B5 | DEFAULT en los 12 padres, `journal_lines` incluido; procedimiento escrito para moverla |
| B6 | Auditoría de accesos y riesgo: indefinida; PSP y AML al abogado |
| C1 | T1 con plazo máximo; al vencer se sortea si hay un mínimo vendido, si no se reembolsa |
| C2 | T7 con duración propia, sin solape entre ediciones |
| C3 | El organizador fija `ticket_price` |
| C4 | Solo `PAID` en el MVP; `cost_kind` inicial `SHIPPING`, `NOTARY`, `REGISTRY` |
| D1 | drand quicknet ratificado como fuente pública |

## Abierto tras estas decisiones

| Tema | Qué falta | Dueño |
|---|---|---|
| Lista de documentos P-C (A8) | Claves por etapa; seguimiento en cada revisión de C1, fecha por acordar | Diego y [LEGAL→ABOGADO] |
| Mínimo de T1 (C1) | Definir umbral, premio y aviso antes de publicar; sin cambios tras la primera compra | Diego y [LEGAL→ABOGADO] |
| Cifrado (B1-bis) | Compatibilidad con Supabase obligatoria; alcance de Auth, rotación, reportería y caché pendientes | Diego |
| Retención (B6) | Plazos de `psp_events` y `operation_register` | [LEGAL→ABOGADO] |
| Enums de costos (C4) | `charge_kind`, `macrozone` | Diego |
| Datos del bloque E | Comisiones, ledger H-01 a H-03, pago tardío, ASS-001 | Diego y dueño contable |
| Implementación humana | H-04, H-07 a H-12 y SQL de las seis tablas reclasificadas | Diego |

## Integración autorizada

Diego autorizó el 2026-10-01 aplicar estos acuerdos a los contratos, L3 y SQL
permitido, según el [plan de integración](../../plans/2026-10-01-c1-integracion.md).
La evidencia final y lo aún abierto se consolidan en [estado C1](estado-c1.md).

## Siguiente paso

1. Integrar A y C en el borrador OpenAPI y L3 V8, con pruebas.
2. Integrar B1, B2, B4 y B6 en el overlay y el manifiesto, y volver a ejecutar el
   runner. B1-bis y las columnas cifradas nuevas van al SQL V8.
3. Registrar como hallazgos de V8 las correcciones del canon: §1.3, §3.16, §7.1,
   §7.3 y §11.5.
4. Completar con el abogado la [plantilla P-C](plantilla-documentos-pc.md) y acordar fecha de entrega.
5. Reconciliar los acuerdos anteriores con C1-V01–V14 sin perder decisiones
   aprobadas; mantener explícitos los valores y desenlaces aún pendientes.
