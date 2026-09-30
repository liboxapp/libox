---
title: Revisión Codex del harness de Libox
status: borrador
tags: [auditoria, harness, codex]
updated: 2026-09-25
description: Revisión parcial independiente con pruebas de los guards en una copia temporal.
---

# Dictamen: revisión parcial; requiere cambios en los controles

## Identificación y alcance

- Ejecución: 20260925-203250-harness-codex; objetivo: harness y cobertura documental de system design.
- Snapshot: `471a28d050a3f03c3b605649f7463822a8e157ad`; rama `codex/activate-ai-audit`.
- Fecha de ejecución: 2026-09-25T20:32:50.007083+00:00 (UTC); zona del usuario: America/Lima.
- Revisor/ejecutor: Codex. Modelo exacto efectivo: no verificado mediante metadata.
- Entrada: invocación directa de la skill por Diego; no existía `docs/audits/` ni
  manifiesto de Claude. Esta revisión autónoma no acredita una ejecución coordinada.
- Árbol inicial limpio; HEAD se comprobó nuevamente antes de escribir este informe.
- Herramientas usadas: lectura local, Git, Python, shell. Pruebas adversariales solo
  contra hooks copiados a un directorio temporal, eliminado al finalizar.
- Fable y Opus: no ejecutados en esta revisión. Ningún informe de ellos fue consultado.
- Independencia limitada: este mismo asistente implementó el harness en el turno previo;
  primera pasada sin informes ajenos, pero no es una revisión ciega respecto del diseño.
- Outline vivo: no consultado. Presupuesto y plazo aprobados: no especificados.
- Carga, tamaño del equipo, RPO/RTO y proveedores: no verificados en este alcance.
- ASS-001 y ASS-002 siguen abiertos según `CLAUDE.md`; no se ratifica el stack.

## Fuentes vigentes

Registro Maestro V6, §1, líneas 25–27: MVP V9, Enterprise V3 direccional,
L3 V7. Sus líneas 92–96 declaran obsoletas versiones mayores de la línea anterior.
Último commit que afecta al Registro: `5ef1766`, 2026-08-30; esta fecha de Git no
se interpreta como fecha de emisión ni como ratificación de cambios externos.
Contrato y plantilla de auditoría: estado vigente, fecha declarada 2026-09-25.

## CX-01 — Alias por symlink evita E2

- Severidad: riesgo operativo; un control que protege el freeze no cubre el destino real.
- Estado/naturaleza: confirmado en ejecución del hook implementado.
- Evidencia: `scripts/hooks/guard_edit.py:54` usa `normpath`, no resuelve enlaces;
  líneas 84–86 comparan prefijos textuales. Regla: `.claude/rules/src-congelado.md`.
- Escenario: copia temporal con `src/probe.txt` y `alias -> src`; se entrega al hook
  `file_path=<temporal>/alias/probe.txt`. Sin variables de escape.
- Esperado: mismo bloqueo que la ruta directa. Observado: directa exit 2; alias exit 0.
- Propuesta: resolver destino real y raíz antes de clasificar rutas, incluyendo archivos
  nuevos dentro de directorios enlazados. Cambiar solo mensajes no corrige el control.
- Validación: prueba de regresión con symlinks internos y externos y rutas inexistentes.
- Incertidumbre: probado como proceso de hook, no como llamada real de Edit desde Claude.
- Seguimiento: responsable de implementación por asignar; cambio posterior a este audit.

## CX-02 — El freeze no cubre escritura por Bash

- Severidad: riesgo operativo para sesiones con shell; no bloquea la revisión de lectura.
- Estado/naturaleza: confirmado; limitación ya reconocida por el manual, líneas 31–35.
- Evidencia: `scripts/hooks/guard_bash.py:56`–77 solo controla ciertas operaciones Git;
  `.claude/settings.json` enruta Bash a ese guard y edición al guard E2.
- Escenario: hook Bash recibe `printf after > src/probe.txt` en copia desechable.
- Esperado si se exige freeze en todas las herramientas: denegación. Observado: exit 0;
  la ejecución posterior en esa copia modifica el archivo, exit 0, contenido `after`.
- Propuesta: restringir escrituras con aislamiento/permisos de filesystem en sesiones de
  auditoría o declarar y aceptar explícitamente un freeze solo procedimental del coordinador.
  Una regex que busque `src/` no cubre intérpretes, aliases ni todas las escrituras.
- Validación: intentar escrituras por shell e intérprete contra copia protegida.
- Incertidumbre: otros plugins o permisos personales podrían añadir controles; no probados.
- Seguimiento: Diego decide garantía requerida; implementación por asignar.

## CX-03 — No existe un procedimiento de reanudación del run

- Severidad: riesgo operativo; dificulta completar una auditoría tras interrupción.
- Estado/naturaleza: confirmado documentalmente; falta procedimiento, no pérdida ejecutada.
- Evidencia: `docs/equipo/ai-audit-harness.md:48`–56 bloquea árbol sucio y exige carpeta
  nueva; líneas 78–79 prevén reintentos sin explicar cómo retomar un run existente.
- Escenario: un run deja manifiesto e informe Fable sin commit; la sesión se interrumpe.
  Una nueva invocación encuentra esos archivos como cambios previos y queda bloqueada.
- Esperado: reanudar con el mismo 471a28d050a3f03c3b605649f7463822a8e157ad y artefactos preservados. Observado: no hay entrada
  definida para validar y reanudar; depende de instrucciones improvisadas del usuario.
- Propuesta: modo explícito `resume <run-id>` que verifique 471a28d050a3f03c3b605649f7463822a8e157ad y limite cambios permitidos
  al run existente. No permitir indiscriminadamente cualquier árbol sucio.
- Validación: interrumpir después de Fable; reanudar sin sobrescribirlo ni duplicarlo.
- Incertidumbre: no se ensayó una interrupción real de Claude.
- Seguimiento: responsable por asignar; no corregido durante esta revisión.

## Comprobaciones ejecutadas

| Comando/prueba | Resultado | Exit |
|---|---|---|
| `python3 verify_corpus.py --dir docs/linea-base` | 15/15 documentos; 0 fallos, 0 avisos | 0 |
| `python3 -m unittest discover -s scripts/hooks/tests` | 53 pruebas, OK | 0 |
| `claude --version` | 2.1.282 | 0 |
| Hook Edit con ruta directa temporal | Deniega | 2 |
| Hook Edit con symlink temporal | Permite | 0 |
| Hook Bash con escritura temporal | Permite; escritura ejecutada después | 0 |
| Hook Edit con JSON malformado | Permite, comportamiento fail-open declarado | 0 |

Los procesos de hook recibieron JSON por stdin y `CLAUDE_PROJECT_DIR` apuntando a
la copia temporal. Se quitaron las tres variables de escape de su entorno de prueba.
No se ejecutó la escritura de prueba en el repositorio real ni se usaron secretos.
El fail-open está explícito en `guard_edit.py:103`–105; es una decisión existente,
no se presenta como hallazgo nuevo ni como protección ante errores del hook.

## Cobertura del contrato

| Escenario | Evidencia obtenida | Pendiente |
|---|---|---|
| H-01 vigencia | Registro distingue V9 de líneas mayores obsoletas | Ensayo de conducta de ambos Claude |
| H-02 conflicto de stack | Regla ASS-002 explícita; no se cerró | Ensayo con instrucciones contradictorias |
| H-03 comando fallido | Se conservaron exits 2 y 0 diferenciados | Inyección de fallo en verificador dentro de Claude |
| H-04 escrituras | Directa bloqueada; symlink y Bash permiten | Herramientas reales y permisos efectivos de Claude |
| H-05 snapshot | Limpio e igual antes de guardar informe | Inyección de cambio concurrente |
| H-06 mayoría sin evidencia | Contrato exige evidencia, no votación | Ensayo de síntesis adversarial |
| H-07 reintento | Falta ruta de reanudación, CX-03 | Interrupción real y recuperación |
| H-08 secretos | No se accedió a secretos | Ensayo de redacción con credencial sintética |

El contrato cubre estados, transacciones, pagos, webhooks, colas, Redis, rate limiter,
balanceo, seguridad, operación, recuperación y simplicidad. Los diez escenarios de
producto están especificados; ninguno se probó contra una implementación en esta revisión.
La allowlist de ambos agentes contiene Read/Grep/Glob; esto se verificó en archivos,
no en una sesión Claude efectiva. Modelos, acceso de cuenta y metadata quedan pendientes.

## Condiciones de cierre

Resolver o aceptar explícitamente CX-01/CX-02; definir reanudación para CX-03.
Ejecutar Fable y Opus sobre evidencia comparable, completar escenarios pendientes
y conciliar resultados sin tratar consenso como prueba. Este informe no es una síntesis
multimodelo ni certifica que el producto o el OS estén listos para producción.
