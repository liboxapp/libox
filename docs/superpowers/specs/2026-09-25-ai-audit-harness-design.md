---
title: Diseño del harness de auditoría compartida — Libox
status: aprobado
tags: [libox, harness, auditoria, system-design]
updated: 2026-09-25
description: Diseño aprobado del protocolo para revisar el OS de IA y la arquitectura con Fable 5.1, Opus 5.5 y Codex, sobre evidencia comparable.
---

# Harness de auditoría compartida

## Intención y alcance

Diego confirmó el 25 de septiembre de 2026 dos modelos en Claude, **Fable 5.1 y
Opus 5.5**, cada uno con un subagente, trabajando sobre el mismo repositorio.
Codex complementa la revisión de forma independiente. Los resultados deben quedar
documentados y versionados. La prioridad del producto es facilitar implementación
y operación de sus flujos; ninguna tecnología recibe preferencia automática.

Diego solicitó activar este diseño el 2026-09-25. La configuración operativa y
el lanzamiento están en el [manual vigente](../../equipo/ai-audit-harness.md).
La activación no ratifica ASS-002 ni modifica el corpus o el código congelados.
La primera auditoría evalúa el **harness**, incluida su capacidad de revisar system
design. Auditar y decidir la arquitectura de producto será una ejecución posterior.

## Situación observada

El checkout examinado estaba en `chore/sistema-operativo-ia`, commit `31c0b68`,
con 15 commits por delante de `origin/main` (`b54f27d`). Allí existen auditores de
corpus y PR, hooks y un manual del OS. Esos cambios no deben tratarse como integrados.
La documentación de este diseño parte de `origin/main` en un worktree separado.

El `AGENTS.md` observado solo contiene el bloque de Next.js. Falta un punto de
entrada de Codex a las reglas de Libox. Los hooks de Claude no acreditan
restricciones equivalentes en otro ejecutor. Estas son observaciones iniciales,
no resultados de una auditoría completa.

## Organización elegida

| Participante | Responsabilidad | Salida independiente |
|---|---|---|
| Claude coordinador | Preparar manifiesto, lanzar las dos revisiones y consolidar | Síntesis y registro de desacuerdos |
| Subagente Fable 5.1 | Coherencia del harness, arquitectura, límites de dominio y contratos | `fable-report.md` |
| Subagente Opus 5.5 | Controles efectivos, operación, recuperación y complejidad | `opus-report.md` |
| Codex | Verificar afirmaciones, reproducir controles y cuestionar complejidad | `codex-report.md` |
| Diego | Resolver alcance, riesgos aceptados y decisiones de producto | Decisiones explícitas en la síntesis |

Interpretación propuesta: el trabajo de revisión corre en un subagente de cada
modelo indicado; la coordinación no cuenta como otro dictamen. Registrar el modelo
real de cada subagente. Los nombres suministrados son etiquetas humanas: antes de
lanzar, verificar identificadores y disponibilidad en Claude. No sustituir modelos
en silencio. Codex registra su modelo real; no se fija uno ficticio en este diseño.

Los tres revisores cubren los escenarios comunes del
[contrato de auditoría](ai-audit-harness/audit-contract.md), además de su especialidad.
No leen informes ajenos antes de cerrar su primera pasada. La separación de archivos
evita exposición accidental; no constituye aislamiento técnico entre sesiones.

Se elige coordinación mediante archivos: es inspeccionable y suficiente para tres
revisores. Un puente automático entre herramientas añade permisos y fallos de
coordinación; queda diferido. Un único informe escrito por todos perdería independencia.

## Entrada reproducible y convivencia

Cada ejecución recibe el mismo manifiesto, hash de commit, corpus vigente y
preguntas. Para revisar los cambios actuales del OS, fijar el SHA completo de la
rama que los contiene; no revisar solamente `main` ni cambiar de base a mitad.
Si hay cambios sin commit, producir primero una instantánea identificable con hash
del diff y contenido de archivos nuevos. Sin instantánea reproducible no comienza.

Mismo repositorio no significa mismo directorio mutable: los revisores leen el
commit fijado; cualquier ensayo con escritura usa un worktree o directorio temporal
propio. Nadie cambia la rama, limpia archivos ni modifica el árbol de otra sesión.
Un solo coordinador incorpora las salidas. No ejecutar push, merge ni despliegue
desde subagentes de revisión. Los ensayos no usan dinero ni datos de producción.

## Estructura propuesta

- `AGENTS.md`: entrada breve para Codex, preservando el bloque administrado por Next.js.
- `CLAUDE.md`: entrada breve para Claude; ambas apuntan a una política compartida.
- `docs/equipo/`: protocolo, precedencia, responsabilidades y comandos verificables.
- Skill `libox-system-design-audit`: una fuente compartida con adaptadores de descubrimiento por herramienta.
- Configuración de agentes y permisos: nativa de cada ejecutor, sin copiar sintaxis entre ellos.
- `docs/audits/<run-id>/`: manifiesto, tres informes, evidencia saneada y síntesis.

Estas rutas describen la futura implementación; no se afirma que ya existan.
Reutilizar el OS y las skills `libox-*` existentes antes de añadir equivalentes.
El corpus mantiene su autoridad según el [Registro Maestro](../../linea-base/LIBOX_REGISTRO_MAESTRO_LINEA_BASE_V6.md).

## Cierre de una revisión

1. Congelar manifiesto y verificar modelos, acceso y comandos disponibles.
2. Ejecutar las tres primeras pasadas independientes con límites declarados.
3. Guardar informes usando la [plantilla](ai-audit-harness/report-template.md).
4. Cruzar hallazgos por evidencia, conservando autoría y desacuerdos.
5. Reproducir los hallazgos críticos; asignar responsable y prueba de cierre.
6. Diego resuelve las decisiones pendientes. Cambios normativos siguen el control del corpus.

Dos votos no convierten una hipótesis en hecho. Los estados de un hallazgo son
`confirmado`, `descartado con evidencia`, `pendiente de prueba` o
`riesgo aceptado por Diego`. Un informe sin acceso suficiente puede cerrar como
`revisión parcial`; nunca como aprobado integralmente.

## Criterios de aceptación del harness

- Ambos ejecutores encuentran las mismas reglas y versiones vigentes.
- Cada modelo efectivo, commit, comando y salida quedan identificados.
- Los informes distinguen implementado, especificado, propuesto y no verificado.
- Los controles se prueban en ambos ejecutores; una instrucción escrita no se reporta como bloqueo técnico.
- Los casos del contrato tienen evidencia o una limitación explícita.
- El intento de modificar un área protegida se prueba en una copia desechable.
- La consolidación preserva desacuerdos y no ratifica stack ni custodia implícitamente.
- El protocolo puede ejecutarse con archivos, sin acceso a cuentas de producción.

## Paso siguiente

Revisar este diseño antes de configurar el harness. El plan de implementación debe
resolver cómo integrar los 15 commits existentes sin duplicarlos, verificar los
identificadores de modelos y definir los controles efectivos por ejecutor. Después
se ensaya el harness con casos conocidos, antes de usar sus dictámenes sobre Libox.
