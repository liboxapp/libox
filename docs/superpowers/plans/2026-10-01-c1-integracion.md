---
title: C1 — integrar decisiones aprobadas en contratos y SQL permitido
status: borrador
tags: [r0, c1, plan, integracion]
updated: 2026-10-01
description: Ejecución de los acuerdos C1 sobre la reconciliación recibida, preservando código crítico y propuestas aún sin ratificar.
---

# Integración de decisiones C1

Autorizada por Diego el 2026-10-01. Entradas: decisiones aprobadas A–D,
aclaraciones de Supabase/T1/P-C y reconciliación Cowork local del mismo día.
Complementa el [plan C1](2026-09-30-r0-c1.md); no sustituye el programa R0.

## Alcance de esta entrega

1. Conservar e integrar las aclaraciones y la reconciliación documental recibida.
2. Aplicar A1–A11 y C1–C4 a OpenAPI, ejemplos y pruebas; mantener pendientes los
   valores de T1, documentos P-C, catálogos restantes y decisiones nuevas Cowork.
3. Aplicar B1 a ACL no crítica y reclasificar seis tablas como humanas. B2–B6 se
   integran en norma y validación local dentro del alcance permitido; no generar
   particiones del ledger, traslado de datos críticos ni una migración V8 ficticia.
4. Actualizar L3 en prosa/tablas y contratos; preservar los 32 bloques protegidos.
5. Documentar la frontera Supabase/KMS y preparar seguimiento P-C.
6. Verificar, revisar el diff completo, abrir PR y rebase-merge tras CI obligatorio.

## Distribución de trabajo

| Frente | Archivos propios | Coordinación |
|---|---|---|
| Contratos | YAML, scripts/contracts salvo preservación, cierres contractuales | Sesión Claude Code; informa operaciones y pruebas finales |
| SQL | database, scripts/database, cierres SQL | Sesión Claude Code; regenera evidencia de fuentes finales |
| L3 | Candidato L3 y propuesta de baliza | Sesión Claude Code; no altera bloques protegidos |
| Integración | Fichas, seguimiento, estado/plan, revisión de coherencia y PR | Codex comprueba resultados y conserva pendientes |

Las sesiones y prompts quedan en el scratch local de ejecución, fuera de canon.
No se confunde una revisión automatizada con autoría humana del código protegido.

## Decisiones de ejecución

- La política T1 vigente cancela/reembolsa bajo mínimo. La propuesta de fianza
  Cowork permanece pendiente; no se activan parámetros 1,25 ni 48 h por inferencia.
- B2 se interpreta como membresías explícitas por componente, incluido el worker
  con app y append, según su tabla aprobada. Se corrige «un solo rol» en la prosa.
- Supabase compatible no autoriza una excepción Auth ni autenticación propia.
  La ficha de compatibilidad explicita qué debe ratificarse antes de implementar.
- El checkout original y sus archivos personales se conservan; integración en
  worktree separado, con hashes de entrada para detectar cambios concurrentes.

## Verificación

- Contratos: validación OpenAPI, ejemplos, rechazos relevantes, fixtures HTTP y
  cliente TypeScript. Estas pruebas no acreditan permisos ni backend real.
- SQL: clasificación completa, concesiones exactas, ausencia de permisos críticos,
  pruebas negativas/mutaciones y escenarios PG17; no equivale a Supabase gestionado.
- Preservación de código crítico, corpus vigente, harness y políticas de CI.
- Markdown, enlaces, diff y revisión automatizada; CI obligatorio antes de merge.

El [estado C1](../specs/c1-l3-v8/estado-c1.md) recoge la evidencia final y pendientes.
Esta entrega no emite C2 ni levanta el freeze del producto.
