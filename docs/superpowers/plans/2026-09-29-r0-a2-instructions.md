---
title: A2 — instrucciones y responsabilidad para R0
status: borrador
tags: [r0, harness, gobernanza]
updated: 2026-09-29
description: Alineación del harness a TypeScript y límites de responsabilidad mientras Diego trabaja solo.
---

# A2 — instrucciones y responsabilidad

> **Actualización posterior — 2026-09-29:** Diego suspendió toda revisión humana
> obligatoria hasta reactivación explícita suya, incluidas las zonas críticas y
> el criterio de R0. Las referencias anteriores a segunda persona en este registro
> describen el estado previo y no bloquean durante la suspensión. Incorporar
> colaboradores no la reactiva. Ver la [regla operativa](../../../.claude/rules/revision-humana.md).


Implementa A2 del [programa de R0](../specs/2026-09-25-habilitar-r0-design.md).
Alcance: documentación e instrucciones, sin cambios al corpus, código de producto,
hooks ni ruleset. A3 se ejecutará como entrega posterior.

## Entregables

- `CLAUDE.md`, `AGENTS.md` y `src/CLAUDE.md` reconocen TypeScript ratificado y
  distinguen la decisión del levantamiento del freeze, pendiente de C2/D1.
- `CONTRIBUTING.md` extrae reglas neutrales de L3 V7 §4.2 y §12. Drizzle,
  Supabase e Inngest quedan a confirmar en C1; las referencias históricas no
  cierran proveedores ni autorizan dependencias.
- `.claude/rules/zonas-sin-ia.md` declara las cinco zonas de Backlog V3 §1.3;
  `AGENTS.md` replica su alcance y exige implementación y segunda revisión humanas.
- `AGENTS.md` explica que los hooks de Claude no se ejecutan automáticamente en
  Codex. CI protege la integración, no las escrituras locales.
- CODEOWNERS apunta a rutas existentes de canon, planes, auditorías y OS; Diego
  es el responsable disponible, con cobertura por defecto para archivos nuevos.

## Límites pendientes

Diego confirmó que trabaja solo. Arom B. y Martin G. se incorporarán después.
No se asignan usuarios desconocidos ni se exige una aprobación que Diego no puede
darse a sí mismo. GitHub conserva cero aprobaciones y revisión de dueños opcional.

La asignación de dueño fijo y segundo revisor por zona y la activación del ruleset
siguen pendientes. Esta entrega no satisface el quinto criterio de habilitación
de R0 ni modifica las restricciones del backlog. No se cierran entregas críticas
sin la segunda persona.

La regla `src-congelado.md` todavía contiene el estado histórico de ASS-002.
Su cambio está bloqueado por A1 y se resolverá mediante la transición revisada de
D1. Las instrucciones de entrada explican la discrepancia; el bloqueo sigue activo.
Los mensajes de hooks corresponden a A3, no se corrigen mediante cambios de código
ocultos en este PR documental. Los informes de auditoría histórica se conservan.

## Verificación

- Comparación manual con L3 V7 §4.2/§12 y Backlog V3 §1.3.
- Markdownlint, diff-check, verificación del corpus y políticas A1.
- Revisión independiente de consistencia, restricciones y alcance.
- Checks remotos y validación de sintaxis de CODEOWNERS en GitHub.
- Sin pruebas unitarias nuevas: esta entrega no cambia comportamiento ejecutable.
