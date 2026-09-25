---
title: Plantilla de informe independiente y síntesis — Libox
status: borrador
tags: [harness, auditoria, plantilla]
updated: 2026-09-25
description: Campos obligatorios para comparar informes sin perder evidencia, incertidumbre ni desacuerdos.
---

# Plantilla de informes

Usar con el [diseño](../2026-09-25-ai-audit-harness-design.md) y el
[contrato](audit-contract.md). Este archivo es una plantilla, no un informe ejecutado.
Cada informe creado lleva su propio frontmatter, fecha, responsable y estado.

## Identificación

- Ejecución y objetivo.
- Revisor, modelo solicitado, modelo efectivo y ejecutor.
- SHA completo y referencia al manifiesto.
- Inicio, fin y zona horaria.
- Acceso efectivo, herramientas y limitaciones.
- Confirmación de primera pasada sin consultar otros informes, o desviación declarada.

## Dictamen

Elegir: `sin bloqueos en el alcance revisado`, `requiere cambios` o
`revisión parcial`. Justificar con IDs de hallazgos y cobertura real.
No usar un porcentaje de confianza ni una puntuación sin método declarado.

## Hallazgos

Un bloque por hallazgo:

- **ID:** prefijo del revisor y número estable; no reutilizar al corregir.
- **Título:** problema concreto.
- **Severidad:** bloquea ejecución, riesgo legal/patrimonial u operativo, o menor; justificar impacto.
- **Estado:** confirmado, descartado con evidencia, pendiente de prueba o riesgo aceptado por Diego.
- **Naturaleza:** implementado, especificado, propuesto o no verificado.
- **Evidencia:** archivo y línea/sección al SHA revisado; fuente externa con URL y fecha cuando aplique.
- **Escenario:** entrada, secuencia y resultado observable.
- **Esperado frente a observado:** diferencia y requisito del que deriva.
- **Propuesta:** corrección mínima y alternativa descartada con motivo.
- **Validación:** prueba que puede confirmar o refutar el hallazgo.
- **Incertidumbre:** qué no se pudo verificar y por qué.
- **Seguimiento:** responsable y vínculo al cambio o registro cuando exista.

No crear IDs ASS-/CHANGE-/RISK- oficiales sin pasar por el registro correspondiente.
Los IDs de auditoría son locales a la ejecución y no sustituyen esos registros.

## Verificaciones ejecutadas

| Comando o prueba | Entorno y snapshot | Resultado y código de salida | Evidencia saneada |
|---|---|---|---|

Anotar separadamente lo no ejecutado y su motivo. Conservar salidas suficientes
para reproducir el resultado sin secretos, datos personales ni tokens.

## Cobertura y límites

| Área o escenario | Revisado | Resultado | Falta comprobar |
|---|---|---|---|

Incluir también áreas revisadas sin hallazgos. No confundir ausencia de hallazgos
con verificación de partes que no se leyeron o no pudieron ejecutarse.

## Síntesis del coordinador

Se redacta después de cerrar los informes independientes, en un archivo distinto.

| Tema | Fable | Opus | Codex | Evidencia decisiva | Resolución y responsable |
|---|---|---|---|---|---|

Deduplicar sin borrar procedencia. Cuando un revisor cambie de conclusión, conservar
la primera versión e indicar qué evidencia motivó el cambio en una adenda.
Toda decisión de Diego lleva fecha y alcance; la ausencia de respuesta no es aprobación.

Cerrar con cambios propuestos, pruebas pendientes y condiciones de cierre.
No presentar una mayoría como prueba ni una síntesis como autorización para
descongelar código, cambiar el corpus, desplegar o operar dinero real.
