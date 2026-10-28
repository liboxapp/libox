---
title: Plan — emisión conjunta rev7 (PRD V23, L3 V22, Matriz V11, API V18, Registro V25)
status: borrador
tags: [plan, emision, rev7, l3, prd, openapi]
updated: 2026-10-28
description: Pasos verificables para llevar al paquete rev7 todo lo decidido hasta el 28/10, sin tocar esquema ni batería, con C-1 como reserva.
---

# Emisión conjunta rev7 — plan de ejecución

> **Para agentes:** ejecutar tarea por tarea con `superpowers:subagent-driven-development`
> o `superpowers:executing-plans`. Los pasos usan casillas `- [ ]`.

**Objetivo:** un paquete `LIBOX_LINEA_BASE_INTEGRADA_rev7` en Cowork station que recoja
toda decisión tomada hasta el 28/10 y resuelva las contradicciones C-3 a C-10 y C-13,
listo para que Adrián añada T-22/DC-01 y para el acta (ACT-R6-01).

**Arquitectura:** copia íntegra de rev6; cada documento cambiado sube una versión con
identidad en cuatro lugares y changelog («decisión que invalida»). El verificador del
paquete es el juez: se actualiza su `BASELINE` en cada tarea y debe terminar sin fallos.

**Herramientas:** Markdown, `verify_corpus.py` del paquete (V16) con `openpyxl` en entorno
aislado, `pandoc` para DOCX, PostgreSQL 16 y 17 en Docker.

**Especificación:** [decisiones del 27/10](../specs/c1-l3-v8/decisiones-2026-10-27.md),
[decisiones del 28/10](../specs/c1-l3-v8/decisiones-2026-10-28.md), documentos de
`docs/desarrollo/` (R6-08 a R6-16) y el informe «Documentación completa — criterio de
salida» en Outline, cuya tabla «Decidido pero no recogido» fija las secciones por decisión.

## Restricciones globales

- **Solo documentos.** `libox_schema_L3_V20.sql`, `tests_v20.sql` y `refutaciones_v20.sql` no cambian; la batería debe seguir en 400/400 y 22 HUECO / 14 NO REPRODUCIDO.
- **Ningún bloque SQL de L3 V21 cambia** en L3 V22: las zonas sin IA siguen siendo implementación humana.
- **rev6 queda intacto:** misma huella antes y después.
- **C-1 es reserva:** RN-268 (1,25× derivado) se conserva; el suelo de publicación de 1,45× se declara pendiente, sin cifra vigente.
- **T-22/DC-01 los escribe Adrián:** se dejan secciones marcadas `[PENDIENTE DC-01 · Adrián]`.
- Claims legales con `[LEGAL→ABOGADO]`; nada se presenta como implementado.

## Puntos de revisión

1. **Contradicción entre documentos:** una decisión recogida en PRD y no en L3, o al revés. Cada tarea comprueba ambos con `grep`.
2. **Bloque SQL alterado** al editar prosa de L3: lo detecta la comprobación de la tarea 2.
3. **Verificador en silencio:** ejecutarlo siempre con el entorno que tiene `openpyxl`.
4. **Referencias obsoletas** a PRD V22, L3 V21, Matriz V10, OpenAPI V17 o Registro V24 en LEEME, Guía, Backlog o Estructura.
5. **C-1 escrito como decidido:** buscar «1,45» y comprobar que solo aparece como reserva.

---

### Tarea 1: Paquete rev7 y verificador

**Archivos:** crear `Cowork station/LIBOX_LINEA_BASE_INTEGRADA_rev7/` como copia de rev6.

- [ ] Guardar la huella de rev6 (`find … | md5`) en `CONTROL_Registro_y_verificacion/huella_rev6.txt` del nuevo paquete.
- [ ] Copiar rev6 a rev7 y correr el verificador sobre rev7. Esperado: `RESULTADO: sin fallos, 0 avisos`.
- [ ] Hacer que `derived_figures` falle si no puede leer el XLSX, en vez de `except Exception: pass`. Comprobación: sin `openpyxl` el verificador falla; con él, pasa con 188 historias y 1.255 SP.

### Tarea 2: L3 V22 — pila, operación e integración (C-3, C-4, C-5, C-12)

**Archivos:** `L3_Tecnico/LIBOX_ESPECIFICACION_TECNICA_L3_V22.md` desde V21.
**Insumos:** borrador C1 del repo (`docs/superpowers/specs/c1-l3-v8/`), `operacion.md`, `seguridad.md`, `mercado-pago.md`, `proveedores.md`, `truora-evaluacion.md`.

- [ ] §0.3: PostgreSQL 17, Render (API y worker), Vercel Pro (frontend), Next.js 16 con Turbopack, Supabase Pro y Auth, Trigger.dev solo para lo no crítico, sin Redis si no queda función que lo use, y techo de infraestructura de US$250/mes como restricción.
- [ ] Fusionar en §12–14 lo único de C1: sesiones/HMAC, KMS, Mercado Pago (`x-signature`), Truora, F1–F7 y la frontera por criticidad del worker.
- [ ] Comprobación de bloques: script en el scratchpad que extrae los bloques ```sql de V21 y verifica que cada uno aparece idéntico una vez en V22.
- [ ] `grep` sin coincidencias en §0.3: «PostgreSQL 16», «Next.js 14». Verificador sin fallos.

### Tarea 3: L3 V22 — reglas de dominio y configuración

- [ ] §4.3: estados Renuncia validada e Inelegibilidad confirmada; autoriza `ADMIN_LEGAL_COMPLIANCE`; bloqueo por controversia abierta (C-6, C-7); `CLAIMED → AWAITING_DELIVERY` para servicios y registrables (R6-14).
- [ ] §6.2–6.3: comisión e impuesto tras acreditar a todos los ganadores (C-9); T-14 con `ADMIN_FINANCE` y segunda firma `ADMIN_SUPER` (C-10); orden de reparto de R6-08; T-22 marcado `[PENDIENTE DC-01 · Adrián]`.
- [ ] §10.1: catálogo de plazos de R6-11 en lugar de 120/90 fijos (C-8); quitar `settlement_hold_days` (C-14); umbral de reputación del 20 %.
- [ ] §3.14 y trabajo diario: worker y privacidad de R6-15; auditabilidad del 04/10.
- [ ] Definiciones de H22-10 como requisitos en prosa (sin SQL).
- [ ] Repetir la comprobación de bloques SQL de la tarea 2. Verificador sin fallos.

### Tarea 4: PRD V23

**Archivos:** `L2_Contrato/LIBOX_PRD_BLUEPRINT_MVP_V23.md` desde V22.

- [ ] Mismas decisiones que la tarea 3 en sus reglas: RN-45, RN-46, RN-103/104, §16.4, §16.7.2 (RN-256), RN-85, RN-96, RN-48/82, RN-147 por persona verificada, INV-25 por expediente con causa.
- [ ] §5.8.4 y §21: apelación 10 + 10 días hábiles (`ADMIN_LEGAL_COMPLIANCE`), umbral del 20 %, revisión de `ADMIN_RISK` en 5 días hábiles.
- [ ] §1.3.2: reserva C-1 con ambas posiciones enlazadas.
- [ ] Comprobación cruzada: para cada regla tocada, `grep` del mismo identificador en L3 V22 con el mismo valor.

### Tarea 5: Matriz V11

- [ ] UC-061 con `ADMIN_LEGAL_COMPLIANCE`; casos de delivery de R6-14; roles de T-14; apelación reputacional.
- [ ] `grep` sin `ADMIN_SUPER` como autorizador del re-sorteo. Verificador sin fallos.

### Tarea 6: OpenAPI V18

**Archivos:** `L3_Artefactos_ejecutables/libox_openapi_L3_V18.yaml` desde el OpenAPI 2.0.0-draft.3 de C1.

- [ ] Añadir las rutas que solo están en V17 y las nuevas: re-sorteo y revocación de accesos de entrega. T-22, ruta de Adrián.
- [ ] Validar el YAML (OpenAPI 3.1) y correr las pruebas de contrato del repo adaptadas a la nueva ruta (`scripts/contracts/tests`).

### Tarea 7: Registro V25 y cierre del paquete

- [ ] §1: nuevas versiones; §1.1: anexo de concurrencia y manifiesto (R6-16); nota de linaje (V8–V21 emitidas en la línea de Cowork).
- [ ] §5: H21-05, H22-04 (parte de Diego) y H22-10 decididos; C-13 corregido; reservas: C-1, ASS-001, T-22/DC-01.
- [ ] Actualizar LEEME, Estructura y referencias en Guía y Backlog. `BASELINE` del verificador al día.
- [ ] Verificador sin fallos; batería y refutaciones en PostgreSQL 16 y 17 iguales a rev6; huella de rev6 sin cambios.
- [ ] DOCX regenerados con `pandoc` y el estilo de referencia de rev6; revisión del render.
- [ ] Revisión independiente con `auditor-corpus` sobre rev7, sin darle esta lista.

### Tarea 8: Entrega a Adrián

- [ ] Publicar en Outline el resumen de cambios de rev7 y las secciones `[PENDIENTE DC-01 · Adrián]`, condicionadas a su SQL corregido (revisión H22-01).
