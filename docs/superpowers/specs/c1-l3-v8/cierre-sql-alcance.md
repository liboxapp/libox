---
title: C1 — alcance del cierre SQL frente a R1
status: borrador
tags: [r0, c1, l3-v8, sql, alcance]
updated: 2026-09-30
description: Qué exige C1 al SQL, qué queda para C2, D1 y R1, y discrepancias de alcance con sus referencias.
---

# Alcance del cierre SQL: C1 frente a R1

Anexo de [cierre SQL](cierre-sql.md). Separa lo que el programa pide en C1 de las
pruebas de negocio de R1, para no convertir estas en requisitos de C1.

## Lo que el programa pide a C1

[Programa R0](../2026-09-25-habilitar-r0-design.md), Stream C, C1:

| Línea | Exigencia | Situación tras este overlay |
|---|---|---|
| l.82 | SQL desplegable: particiones, GRANTs, semillas, disparadores prometidos e INV-38 | Particiones: 11/12 padres verificados; `journal_lines` es aporte humano (ledger). GRANTs: parcial (H-06 no cerrado). Semillas: solo PE. Disparadores prometidos e INV-38: **humano, abierto** |
| l.84 | Vectores de prueba **con resultado esperado** y `verify_draw` sin ambigüedad | **Pendiente humano.** Es entregable de C1 aunque su ejecución corresponda a la integración (L3 V7 §14.5, R1/E14). No se fabrican valores |
| l.88 (C2) | Emisión con `verify_corpus` en cero, Registro y BASELINE | Fuera de este paquete |
| l.95 (D1) | CI con migraciones sobre PostgreSQL efímero y esquema V8 | El runner es candidato, pero no está conectado a CI y opera sobre V7 más el overlay, no sobre V8 |

L3 V7 §0.2.1 (regla de emisión) pide que el esquema se ejecute con cero errores y
que sus restricciones se prueben contra casos que deben fallar. Eso aplica a la
**emisión de V8 (C2)** sobre el SQL V8 completo, no a este borrador.

## Lo que no es C1

- **F1–F7:** programa l.48, definición de terminado de R1 y del motor de sorteo
  (E14), contra PostgreSQL real y el sandbox del PSP.
- **Concurrencia de L3 V7 §14.4** (`conc_*`): R1. Además es zona sin generación
  asistida.
- **Restauración RPO/RTO:** [operación](operacion.md) l.87, "antes de R1".
- **Ensayo con dinero real:** L3 V7 §14.7, gate de fase.

## Discrepancias de alcance, a la vista

1. **Vectores de sorteo.** En mi informe técnico anterior los asigné a R1. El
   programa (l.84) y [cambios](cambios.md) C1-H10 (l.27) los piden en C1 como
   especificación con resultados esperados, calculados por una implementación
   humana independiente. Queda corregido: son **C1 pendiente humano**; su
   ejecución en cada integración es R1/E14.
2. **"Retención y recuperación"** en [cambios](cambios.md) l.47–48, dentro de la
   evidencia de particiones. La recuperación es un ensayo de R1 (operación l.87).
   La retención de 4 de los 12 padres (`psp_events`, `operation_register`,
   `risk_events`, `audit_access_events`) no está definida en L3 V7 §1.3; la de
   `operation_register` está pendiente de [LEGAL→ABOGADO]. Aquí no se ejecuta
   retención ni recuperación.
3. **C1-H06** (l.23) pide pruebas como `libox_app`, `libox_append`, `libox_read` y
   `libox_migrate`. Se hicieron sobre las 17 tablas concedidas y las
   denegaciones, junto con la comprobación de que ningún otro rol (incluidos
   `service_role` y un rol propio) tiene privilegios. No cierran H-06 sin la
   matriz completa ni los logins reales.
4. **C1-H05** (l.22) pide rotación mensual en 12 tablas. Aquí se cubren 11:
   las particiones de `journal_lines` son SQL del ledger (zona sin generación
   asistida) y quedan como aporte humano.
5. **C1-H07 e INV-38.** La corrección y su prueba concurrente dependen del
   disparador humano. La sonda documenta que sigue abierto.

## Proveedores

Mercado Pago como PSP y Truora como prioridad de evaluación de identidad no
afectan a este overlay: `payments.provider` e `identity_verifications.provider`
son `VARCHAR` sin catálogo en V7. L3 V7 §0.3 ya nombraba a Mercado Pago como
primario en PE. Supabase Pro, PostgreSQL 17 condicionado y Trigger.dev no se
ejercitan aquí; ver [pendientes](cierre-sql-pendientes.md).
