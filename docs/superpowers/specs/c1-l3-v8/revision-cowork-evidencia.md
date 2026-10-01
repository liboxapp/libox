---
title: C1 — evidencia de la comparación Codex y Opus
status: vigente
tags: [r0, c1, evidencia, cowork]
updated: 2026-10-01
description: Procedencia, resultados comprobados y límites de la revisión independiente que alimenta la reconciliación documental de C1.
---

# Evidencia de la revisión Cowork

Revisión documental independiente pedida por Diego; después autorizó actualizar
el trabajo. No es una ejecución del harness Fable/Opus/Codex, una emisión canónica
ni una ratificación de cada decisión económica de la fuente.

## Entradas y recuperación

- Origen nuevo en el workspace: `Cowork station/LIBOX_LINEA_BASE_VIGENTE/`.
- Canon comparado: `docs/linea-base/`, commit
  `ab18a2cd9f8c391253108bafc1931ffd93315348`.
- Tercer origen: C1 con los cambios locales ya existentes en las cuatro fichas
  de decisiones. Se conservaron al integrar esta actualización.
- Run: `comparacion-linea-base-20260930-212305`, carpeta del workspace
  `Output/comparacion-linea-base-20260930-212305/`. Sus informes y copias de entrada
  se conservan fuera del canon. Rutas aquí son procedencia, no links de checkout.
- [Manifest de recepción](revision-cowork-manifest.json): hashes de 93 entradas,
  informes finales y resultados de comprobación. Las rutas de origen son relativas
  al workspace o repo indicados en él; no contiene una copia nueva de SQL protegido.

## Trabajo independiente y contraste

Codex comparó 93 entradas, incluidos los 15 Word; verificó texto Word/Markdown,
API, tokens, fórmulas/sumas Excel y los dos verificadores documentales. No encontró
decisiones materiales exclusivas del Word; su maquetación no fue certificada.

Claude Desktop/Cowork tenía **Opus 5.5 Medium** seleccionado; no hay metadata API
del identificador efectivo. La CLI no tenía sesión. El chat de revisión es
[Fuentes-libox auditoría independiente](https://claude.ai/cowork/cse_01LmeDBT46WK2cvNZhoHNr9Y).
Opus recibió 78 entradas, sin los Word, y ejecutó PostgreSQL 16.13 efímero,
sondas, recálculo LibreOffice y mutaciones. Las dos primeras pasadas se cerraron
antes de leer la otra; después se resolvieron diferencias y se conservaron adendas.

## Resultados y límites

| Evidencia | Resultado comprobado | Qué no acredita |
|---|---|---|
| Verificador de corpus antiguo y nuevo | Exit 0, 15 documentos, cero errores/warnings | Identidad de fianza, fórmula económica, coherencia Excel o emisión formal |
| SQL de Opus | PG16.13: 135 tablas, 54 transiciones, 30 cuentas (15 × 2 monedas), 8 tipos | PG17 completo, overlay C1, Supabase o backend real |
| Suite recibida | 39 OK: 17 rechazos, 17 aceptaciones y 5 checks de semilla; sin warnings/errores en las salidas | Que cualquier excepción sea el rechazo correcto o que el runner falle ante una regresión |
| Sondas adversariales | Se aceptan UUID de fianza inventado/ajeno/insuficiente y mínimo de tickets alterado | Que el gate esté corregido por cargar la semilla |
| Contadores/campaña | Se aceptan anulados > emitidos y campaña gratuita asociada a PAID | Que un servicio real incremente indebidamente la recaudación; no fue ejecutado |
| Excel | Filas suman 145/991; resumen recalculado conserva 136/936/30 | Capacidad real de una persona o calendario de 31 sprints |
| Anexos Opus | Codex comprobó 32 hashes y 6 entradas, sin discrepancias | Reejecución SQL independiente de Codex |
| Integridad al cierre del análisis | 93 fuentes intactas y copias coincidentes | Inmutabilidad posterior de las fichas C1 que esta actualización modifica |

Los anexos separan originales, estado persistido y reejecuciones. P10/P11 se
recuperaron del log original y se reejecutaron. P5 opera sobre `POOL_FROZEN`, no
ACTIVE; P6b acepta un retorno `DRAW_EXECUTED` desde una fila POOL_FROZEN, no prueba
la transición de un sorteo ya ejecutado a suspensión.

## Correcciones incorporadas

- T4 sí tiene trigger para sus hitos; falta revalidar al cambiar el mínimo padre.
- `tickets_reserved` incluye emitidos: el defecto excluye reservas pendientes,
  no cuenta dos veces los pagos.
- T-20/T-21 con las mismas cuentas no son necesariamente incorrectos; falta
  declarar destino, beneficiario y ciclo de caja.
- V9 solo corresponde si se confirma emisión formal de V8; no renombrar por intuición.
- Retenciones de canal/modelo de margen eran supuestos, no tarifas verificadas.
- Los V1 legales/históricos no añaden dictámenes ni aprobaciones.

Estas conclusiones alimentan los 14 [deltas C1-V](reconciliacion-linea-base.md),
que cubren los 27 grupos del informe. No se consultó ni escribió Outline, no se
probó dinero real/PSP y no se cerró ASS-001. La aprobación de backend TypeScript
ya existente sigue vigente; la revisión no la revoca.
