---
name: libox-system-design-audit
description: Auditar el harness de IA o el system design de Libox con evidencia comparable, revisores independientes y control de vigencia documental.
---

# Auditoría compartida de Libox

Lee `CLAUDE.md`, las reglas aplicables y `docs/equipo/ai-audit-harness.md`.
Las rutas de este procedimiento se resuelven desde la raíz del repositorio.
Lee el contrato y la plantilla enlazados por el manual antes de revisar.

## Coordinador Claude

La invocación sin argumentos audita el **harness**; `producto` revisa el diseño.
Usa `python3 scripts/audit/run.py start <run-id> --scope harness` (o `producto`)
para crear el snapshot y un checkout detached por revisor. Para retomar, usa
`resume <run-id> --scope <alcance-original>`; nunca recrees ni cambies su SHA.
Prepara el manifiesto y las verificaciones según el manual. No empieces con un
snapshot sucio ni sustituyas modelos que no estén disponibles.
Lanza exactamente una primera revisión con cada agente del proyecto:
`libox-audit-fable` y `libox-audit-opus`. Conserva el modelo de cada definición.
Entrega el mismo SHA, manifiesto, alcance, contrato y evidencia saneada a ambos,
y asigna a cada uno su checkout exclusivo de `run.json`. No les des acceso
procedimental al directorio de informes ni a los checkouts ajenos; esta regla
y `disallowedTools: mcp__*` no son un sandbox del filesystem.
No les entregues el informe del otro. No delegues estas revisiones en agentes genéricos.
Guarda sus respuestas con la plantilla mediante el subcomando `report` (stdin),
que sanea y crea exclusivamente un archivo nuevo; conserva los intentos anteriores
al reintentar. No uses la shell para sobreescribir informes ni variables de escape E5.
Prepara `codex-prompt.md` con el SHA, ruta del run y solicitud de revisión independiente.
Claude no interpreta el papel de Codex ni declara ejecutado ese informe.
Si un agente falla, registra el error y entrega solo los resultados obtenidos;
no sustituyas el modelo ni fabriques un informe. Si Codex aún no participó,
entrega una síntesis provisional y marca la revisión Codex pendiente. No bloquees la entrega de lo ya obtenido.
Verifica nuevamente el snapshot antes de sintetizar. No corrijas lo auditado durante
la ejecución; entrega hallazgos y correcciones propuestas para un cambio posterior.

## Revisor Claude o Codex

Si recibes un brief de revisión, actúa como revisor, no como coordinador.
No lances otros agentes. Lee el manifiesto y las fuentes del snapshot indicado.
No leas otros informes de la ejecución hasta entregar tu primera pasada.
Aplica todos los escenarios comunes, además del enfoque asignado.
Clasifica evidencia como ejecutada, documental o pendiente; cita archivo y línea.
No infieras vigencia por el número de PRD: comprueba Registro Maestro, estado y fechas.
Devuelve el informe al coordinador. Codex puede guardar solo su informe en la carpeta
asignada si el usuario lo solicita; no sobrescribas intentos previos.
No leas secretos ni vuelques variables de entorno. No modifiques código o corpus.

## Concurrencia y validación

Sigue [runs reproducibles](../../../docs/equipo/audit-runs.md). El gestor serializa
operaciones en el directorio Git común. En un mismo host, otro run sin versionar
bloquea el inicio; usa un host limpio distinto si necesitas una ejecución paralela.
Al reanudar solo se admiten archivos nuevos del run actual. Ejecuta `validate`
al terminar cada revisión y antes de sintetizar. Divergencia implica conservar los
resultados como parciales, sin modificar ni borrar el snapshot original.
