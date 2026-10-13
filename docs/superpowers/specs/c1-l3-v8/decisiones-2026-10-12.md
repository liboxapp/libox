---
title: C1 — decisiones de Diego del 12 de octubre
status: aprobado
tags: [r0, c1, decisiones, go, render, postgresql]
updated: 2026-10-12
description: Render sustituye a Vercel como alojamiento del backend Go y PostgreSQL 17 pasa de condicionado a elegido; qué se conserva, qué falta validar y evidencia PG17 con sus límites.
---

# Decisiones del 12 de octubre de 2026

Origen: respuesta de Diego del 2026-10-12 sobre el alojamiento del backend y la
versión de PostgreSQL: «Render y postgre17». Este registro aprueba esas dos
elecciones; no declara completado C1, emitido el canon, contratado un servicio
ni habilitado un entorno. Sustituye la fila 1 de las
[decisiones del 04/10](decisiones-2026-10-04.md) y conserva el resto de ese
registro sin cambios.

## Registro por punto

| Punto | Respuesta de Diego | Alcance registrado | Trabajo que continúa |
|---|---|---|---|
| Alojamiento del backend Go | «Render y postgre17» | Render aloja el backend Go: API y worker. Sustituye a Vercel, elegido el 04/10 (fila 1). Vercel Pro conserva el frontend Next.js | Validaciones de abajo antes de habilitarlo |
| Versión de PostgreSQL | «Render y postgre17» | PostgreSQL 17 pasa de condicionado a elegido. La validación de la migración deja de condicionar la elección, pero sigue siendo requisito de C1 y R1 | Migración V8 completa en 17 (C1) y prueba en Supabase (R1) |

La respuesta no elige plan, tamaño de instancia, región ni modalidad de servicio
de Render, ni crea cuentas. Si la validación de PostgreSQL 17 fallara, la
respuesta corresponde a Diego; este registro no la anticipa.

## Qué se conserva

- **Vercel Pro para el frontend** Next.js y TypeScript.
- **Trigger.dev**, conservado y en evaluación durante los primeros meses
  (punto 2 del 04/10). Su frontera con el worker Go sigue por definir.
- **Supabase Pro** como PostgreSQL gestionado y Supabase Auth (punto 4 del 04/10).
- **Techo de infraestructura de US$250/mes** (punto 12 del 04/10), que debe
  recalcularse. Los escenarios de [proveedores](proveedores.md) y de la
  [adaptación a Go](../2026-10-02-r0-backend-go-design.md) no incluyen un plan
  concreto de Render; no son un coste ejecutado.
- Los demás puntos del 04/10, la [decisión de stack](../2026-10-02-stack-go-frontend-ts.md)
  y las [decisiones C1](decisiones-c1.md) del 30/09.

## Qué falta validar antes de habilitar

Ninguna de estas comprobaciones se ha hecho:

- **Región.** El candidato L3 (§0.3) exige que el backend esté en la región
  de Supabase. Confirmar qué región de Render lo cumple y medir la latencia
  real hacia la base.
- **Conexiones y pooling.** Pool acotado de API y worker hacia Supabase.
  Comprobar si Render alcanza la conexión directa de Supabase o requiere el
  pooler en modo sesión. Si el ejecutor de trabajos usa LISTEN/NOTIFY, no le
  sirve el modo transacción. Presupuesto de conexiones (API, worker, servicios de Supabase,
  migraciones y despliegues) frente al límite del cómputo elegido.
- **Worker como proceso separado.** API y worker como servicios distintos de
  una misma imagen, con los mismos módulos de dominio ([ficha D-10](../2026-10-02-r0-backend-go-design.md)).
  Verificar reinicio, reanudación desde PostgreSQL y convivencia durante un
  despliegue. La ejecución única y la idempotencia siguen siendo zona crítica de
  implementación humana; el alojamiento no las garantiza.
- **Despliegue y secretos.** Orden entre migraciones (`libox_deployer`, B2) y
  publicación de la versión, reversión y entornos separados. B2 ([datos](decisiones-c1-datos.md))
  ubicaba los secretos de los logins en los gestores de Vercel y Trigger.dev:
  la ubicación de `libox_api` y `libox_worker` en Render y su rotación de 90 días
  quedan por confirmar. La adaptación a Go aceptaba Render con una credencial
  AWS exclusiva y rotada para KMS; falta definirla.
- **Coste.** Recalcular con Render (API y worker), Trigger.dev, Supabase, KMS,
  copias y observabilidad, con el objetivo de US$215 antes de impuestos y sus
  alertas. Medir antes de ampliar.
- **Auditoría y logs.** Los logs de la plataforma no sustituyen la auditoría de
  negocio aprobada el 04/10.

## Evidencia PostgreSQL 17 y su límite

Verificado por el coordinador el 2026-10-12, en contenedores Docker desechables:

- El esquema `libox_schema_L3_V17.sql` (151 tablas) cargó con cero errores en
  PostgreSQL 17.11 y 16.15.
- Su batería `tests_v17.sql` pasó 258 OK y 0 fallos en ambas versiones.

Ambos archivos provienen del paquete de Cowork
`LIBOX_LINEA_BASE_VIGENTE rev3/L3_Artefactos_ejecutables/`, fuera del repo.
Ese paquete los registra como vigentes en su propio Registro Maestro V20; el
repo sigue gobernado por el Registro Maestro V6, que no los incluye, y recibirlos
no les da vigencia. Los registros de la ejecución no están versionados.

Esta evidencia **no acredita la migración completa del overlay** de
[`database/`](database/README.md) ni la secuencia V8 del Anexo A del candidato.
Tampoco prueba Supabase gestionado, su pooler, `pg_cron` ni su build de
PostgreSQL 17. La batería es la del propio paquete: su verde no demuestra que
cubra los defectos abiertos de C1 (H-04, H-07–H-12) ni los aportes humanos.

## Efecto en otros documentos

- La fila 1 del [registro del 04/10](decisiones-2026-10-04.md) queda
  sustituida; sus citas y el resto de su contenido no cambian.
- DP-09 del [candidato L3](LIBOX_ESPECIFICACION_TECNICA_L3_V8_DRAFT.md) pasa a
  PostgreSQL 17 elegido; la validación de §0.2.1 se mantiene.
- Falta trasladar estas decisiones al doc 20 de Outline (DP-19) y al canon en
  C2. El freeze de `src/`, las zonas sin generación asistida y la suspensión de
  la revisión humana no cambian.
