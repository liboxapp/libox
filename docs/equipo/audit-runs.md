---
title: Runs de auditoría reproducibles
status: vigente
tags: [equipo, auditoria, harness, pruebas]
updated: 2026-09-29
description: Snapshots por revisor, reanudación, informes inmutables y evidencia sintética de A4.
---

# Preparar y reanudar

Requiere Python 3.9+, Git y POSIX (`fcntl`, probado en macOS; CI en Linux).
Desde un checkout limpio, crear un identificador único y elegir el alcance:

```sh
python3 scripts/audit/run.py start 20260929-ejemplo-harness --scope harness
python3 scripts/audit/run.py resume 20260929-ejemplo-harness --scope harness
python3 scripts/audit/run.py validate 20260929-ejemplo-harness --scope harness
```

Son ejemplos de uso, no evidencia de una auditoría realizada. El gestor fija HEAD
completo y crea tres worktrees detached diferentes, uno para Fable, Opus y Codex.
`run.json` guarda las rutas absolutas, host, rama, alcance y fecha UTC. Cada revisor
recibe solo su checkout, el mismo brief y checks saneados. La carpeta del run se
queda en el host del coordinador y no se copia a los snapshots recién creados.
No se lanzan revisores automáticamente ni se acreditan modelos efectivos.

Los checkouts y una copia de control de `run.json` viven bajo
`<git-common-dir>/libox-audit-runs/<run-id>/`, también cuando el host es un worktree.
El JSON del run debe coincidir byte a byte con esa copia. No es una firma ni protege
contra un operador con escritura en Git; permite detectar divergencias accidentales.
Completar `brief.md` nuevo con las entradas del [contrato](../superpowers/specs/ai-audit-harness/audit-contract.md).
El manifiesto generado deja presupuesto, plazo, responsables y modelos efectivos
sin verificar; no inventa evidencia ni sustituye la lectura del Registro vigente.

`resume` exige que el run ya exista, mismo host, SHA y alcance. Solo permite cambios
no versionados dentro de ese run. Cambios staged, en archivos ya versionados o en
otro run invalidan la comparación. Comprueba además SHA, detached y limpieza de los
tres revisores, incluidos archivos ignorados. Repetir `validate` después de cada
revisión y antes de sintetizar. No hacer commit de informes hasta finalizar el run.

Las operaciones del gestor se serializan con un lock en Git común. Dos inicios con
el mismo ID nunca reutilizan archivos. Un host con un run nuevo bloquea otro inicio;
para paralelismo usar hosts limpios distintos e IDs distintos. El lock no impide
escrituras externas: la validación detecta divergencia en los puntos de control,
no cada mutación transitoria. Un inicio interrumpido conserva todo; si está parcial,
registrar el fallo y usar otro ID desde un host limpio, sin borrado automático.
No hay limpieza automática de worktrees: conservar evidencia antes de retirarlos.

## Informes y saneamiento

El subcomando `report` lee texto suministrado por stdin, sanea y crea un archivo
nuevo con exclusión (`open('x')`). No abre secretos ni lee el entorno:

```sh
python3 scripts/audit/run.py report 20260929-ejemplo-harness --scope harness \
  --filename fable-report.md < /ruta/al/informe-sintetico.md
```

Los nombres admitidos son `fable-report.md`, `opus-report.md`, `codex-report.md` y
`synthesis.md`, y reintentos `*-attempt-2.md` en adelante. Si el nombre existe,
falla sin modificar el original. Usar la plantilla del manual y registrar el
motivo del reintento. E5 protege informes `.md` existentes bajo `docs/audits/<run>/`,
excepto `manifest.md`, `checks.md` y `codex-prompt.md`; no tiene escape por entorno.
Es una barrera de herramientas de edición; una shell o proceso externo aún puede
escribir. El escritor exclusivo evita la sobreescritura en el flujo admitido.

El [saneador](../../scripts/audit/sanitize.py) cubre asignaciones habituales de claves,
JSON sencillo, Bearer/Basic, credenciales en URL, tokens conocidos y claves privadas
PEM. Preserva referencias de evidencia y códigos de salida. No detecta todos los
secretos, formatos codificados, fragmentados ni credenciales sin etiqueta. Nunca
alimentarlo con `.env` real ni con dumps de entorno: prevención antes que redacción.
El gestor rechaza nombres sensibles versionados antes de crear snapshots, sin
abrirlos. Esto no acredita que el resto del repositorio esté libre de secretos.

## Evidencia A4 y límites

```sh
python3 -m unittest discover -s scripts/audit/tests -v
python3 -m unittest discover -s scripts/hooks/tests -v
```

La suite de auditoría solo usa repos Git temporales y credenciales sintéticas.
En desarrollo se observó RED inicial: 9 fallos por gestor, saneador y predicado E5
ausentes; GREEN: 9 pruebas. La ampliación detectó un rechazo incorrecto del intento
10; se corrigió la expresión y se volvió a ejecutar la suite ampliada. El registro
de CI es la evidencia repetible; este texto no sustituye su resultado por commit.
La revisión posterior reprodujo en RED y corrigió tres bordes: comillas escapadas
en credenciales, rutas Unicode citadas por Git y symlinks circulares en E5.

| Escenario | Evidencia y límite |
|---|---|
| H-01 | Fixture JSON con Registro vigente V2 y PRD derogado V99; prueba materializa y fija ambas versiones en snapshots. Juicio de vigencia de un revisor real: pendiente. |
| H-02 | Fixture JSON de conflicto local TypeScript/.NET y ASS-002 sintético histórico; snapshots comprobados. Juicio de un revisor real: pendiente. No describe la ratificación vigente. |
| H-03 | CLI devuelve código distinto de cero al rechazar un run. Registro de un fallo de verificador por revisores reales: pendiente. |
| H-04 | Pruebas de guards en suite de hooks; no prueban sandbox ni bloqueo universal de shell/MCP. |
| H-05 | Git temporal: divergencia de HEAD, archivo host, checkout revisor y archivo ignorado son rechazados al reanudar. |
| H-06 | Independencia y síntesis sin fuentes son reglas documentales; comportamiento con revisores reales pendiente. |
| H-07 | Escritura exclusiva conserva original y permite intentos 2 y 10; no se simula una interrupción del proveedor. |
| H-08 | Fixture sintética cubre formatos declarados y exige ausencia de valores, evidencia conservada e idempotencia. No certifica detección universal. |

Las fixtures H-01/H-02 están en `scripts/audit/tests/fixtures/`. No se ejecutaron
revisores reales para estos ensayos. La revisión humana obligatoria permanece
suspendida según la [regla vigente](../../.claude/rules/revision-humana.md).
