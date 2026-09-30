---
title: Prompt para el revisor Codex — auditoría del harness 20260925-203710
author: Claude coordinador (claude-opus-5-5)
status: vigente
tags: [auditoria, harness, codex]
updated: 2026-09-25
description: Petición de revisión independiente para que Diego la lance en Codex sobre el SHA y el manifiesto de este run.
---

# Prompt para Codex

Diego lanza este texto en Codex. El coordinador Claude no ejecuta ni simula la revisión de Codex.

```text
Usa la skill .claude/skills/libox-system-design-audit/SKILL.md como revisor Codex.
Revisa de forma independiente el SHA y alcance del manifest.md de docs/audits/20260925-203710-harness/.
SHA: 471a28d050a3f03c3b605649f7463822a8e157ad (rama codex/activate-ai-audit).
Usa también checks.md de ese run como evidencia ejecutada por el coordinador y reprodúcela si puedes.
No leas fable-report.md, opus-report.md ni synthesis.md antes de entregar tu informe.
Guarda tu informe en docs/audits/20260925-203710-harness/codex-report.md sin modificar el objeto auditado.
Registra en el informe el modelo real de tu sesión.
```

## Nota de contexto

Al preparar este run se observó una ejecución concurrente de Codex en `docs/audits/20260925-203250-harness-codex/`, con su propio `codex-report.md`, creada a las 20:32:50 UTC y previa a este manifiesto. La síntesis la considerará solo si su SHA y alcance son comparables. En tal caso, este prompt es opcional.
