---
title: Harness activo de auditoría de IA y system design
author: Equipo Libox
status: vigente
tags: [equipo, auditoria, system-design]
updated: 2026-09-25
description: Lanzamiento del audit con Fable 5.1, Opus 5.5 y revisión independiente de Codex.
---

# Lanzamiento

En una sesión nueva de Claude Code abierta en la raíz de Libox, ejecuta:

```text
/libox-system-design-audit
```

Esto inicia la revisión del OS de IA y de su cobertura de system design.
Para una revisión posterior del producto: `/libox-system-design-audit producto`.
El comando carga la [skill compartida](../../.claude/skills/libox-system-design-audit/SKILL.md).
No significa que una auditoría ya se haya ejecutado o aprobado.

## Roles y configuración

| Rol | Modelo solicitado | Enfoque adicional |
|---|---|---|
| libox-audit-fable | claude-fable-5-1 | Dominio, estados, contratos y simplicidad de implementación |
| libox-audit-opus | claude-opus-5-5 | Fallos, concurrencia, seguridad y facilidad de operación |
| Codex independiente | El disponible en su sesión, registrado en el informe | Evidencia reproducible, contradicciones y límites de controles |

Ambos agentes Claude leen el mismo contrato completo. Su allowlist es
`Read, Grep, Glob`: no tienen shell, edición ni delegación.
El coordinador conserva herramientas de escritura y ejecución: esta restricción
no es un sandbox global. Los hooks existentes tampoco cubren toda escritura por shell.
La primera pasada independiente es una regla de procedimiento, no aislamiento de archivos.

La configuración de auditoría es una excepción a la delegación genérica Fable→Opus:
se conservan los dos modelos indicados. Claude Code debe ser **2.1.280 o posterior**.
Los identificadores y requisito se verificaron el 2026-09-25 en la
[documentación oficial](https://code.claude.com/docs/en/model-config).
No sustituir un modelo por un alias ni otro modelo ante falta de acceso.
La instalación compatible no garantiza que la cuenta o gateway permita ambos modelos.

## Preparación por el coordinador

1. Lee `CLAUDE.md`, `.claude/rules/`, el Registro Maestro vigente y este
   [contrato](../superpowers/specs/ai-audit-harness/audit-contract.md).
2. Ejecuta `claude --version`, `git rev-parse HEAD`, `git branch --show-current`
   y `git status --porcelain=v1 --untracked-files=all`. Si hay cambios previos,
   informa el bloqueo de snapshot; no hagas commit, stash ni descarte automático.
3. Comprueba solo la presencia de `CLAUDE_CODE_SUBAGENT_MODEL` y de overrides de
   modelos en la configuración efectiva; no imprimas valores secretos ni el entorno.
   Resuelve cualquier override que impida los modelos pedidos antes de delegar.
4. Crea una carpeta nueva `docs/audits/<fecha-hora-UTC>-harness/` (o `-producto`)
   sin reutilizar una existente. Escribe `manifest.md` con frontmatter y todos los
   campos del contrato. Los modelos efectivos empiezan como `no verificado`.
5. Registra los documentos normativos con versión, fecha y ruta. Una fecha más
   reciente no deroga por sí misma un documento del Registro. Expón ASS-001 y ASS-002.
6. Ejecuta las verificaciones locales de abajo; guarda comandos, salida saneada y
   códigos de salida en `checks.md`. Un fallo es evidencia, no motivo para ocultarlo.
7. Lanza los dos agentes con el mismo brief autocontenido y evidencia. La metadata de
   ejecución, si está disponible, acredita el modelo efectivo; la autodeclaración del
   modelo no lo acredita. Sin metadata, conserva `no verificado` y limita el dictamen.

```sh
python3 verify_corpus.py --dir docs/linea-base
python3 -m unittest discover -s scripts/hooks/tests -v
```

No ejecutes pruebas adversariales contra el checkout real. Los escenarios H-01–H-08
se ensayan en una copia desechable con datos sintéticos; marca como pendientes los
que no se ejecuten. No leas `.env`, credenciales o configuración personal completa.

## Informes y cierre

Usa la [plantilla](../superpowers/specs/ai-audit-harness/report-template.md) para
`fable-report.md`, `opus-report.md`, `codex-report.md` y `synthesis.md`.
El coordinador escribe solo dentro de la carpeta del run. En un reintento utiliza
`fable-report-attempt-2.md`, por ejemplo; conserva la primera respuesta y el motivo.
No fabriques archivos de informe para revisores no ejecutados.

Genera `codex-prompt.md` con una petición equivalente a:

```text
Usa la skill .claude/skills/libox-system-design-audit/SKILL.md como revisor Codex.
Revisa de forma independiente el SHA y alcance del manifest.md de ESTE_RUN.
No leas fable-report.md, opus-report.md ni synthesis.md antes de entregar tu informe.
Guarda tu informe en ESTE_RUN/codex-report.md sin modificar el objeto auditado.
```

Sustituye ESTE_RUN por la ruta real. Diego lanza ese prompt en Codex.
Al terminar cada revisión y antes de sintetizar, comprueba que HEAD sigue siendo el
SHA inicial y que `git status` solo contiene archivos nuevos de esa carpeta de run.
Cualquier otro cambio invalida la comparación afectada: conserva resultados como
parciales y reinicia sobre un nuevo snapshot cuando esté disponible.

Si un agente falla, registra el fallo y su intento; no sustituyas el modelo.
Entrega una síntesis parcial con los informes obtenidos y los revisores ausentes.
Sin Codex, el coordinador entrega la síntesis provisional con esa ausencia explícita.
Con las tres revisiones, concilia por evidencia y mantiene desacuerdos sin resolver.
El cierre requiere explicar cobertura, pruebas pendientes, modelos efectivos y límites.
Un audit no ratifica el stack ni autoriza cambios en el corpus, despliegues o pagos.
Los informes se versionan después del cierre mediante el flujo normal de PR.
