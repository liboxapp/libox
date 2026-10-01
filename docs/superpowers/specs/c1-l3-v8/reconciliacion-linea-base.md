---
title: C1 — reconciliación de la documentación recibida en Cowork
status: borrador
tags: [r0, c1, reconciliacion, linea-base]
updated: 2026-10-01
description: Incorporación al trabajo de C1 de las 27 diferencias revisadas por Codex y Claude Opus, conservando decisiones aprobadas y pendientes humanos.
---

# Reconciliación de la documentación de Cowork

Diego autorizó actualizar el trabajo tras la comparación independiente de Codex
y Claude Opus 5.5. Esta entrega incorpora sus conclusiones al candidato y al
[plan C1](../../plans/2026-09-30-r0-c1.md). Los requisitos económicos nuevos quedan
como propuesta trazada: recibir un archivo llamado «vigente» no acredita su
emisión ni ratifica todos sus parámetros. Véase [procedencia](revision-cowork-evidencia.md).

## Decisiones que se conservan

- Backend Next.js/TypeScript ratificado por los socios; Scalar. Drizzle sigue sin elección.
- Supabase Pro + Trigger.dev + Vercel Pro, techo inicial de US$250/mes;
  PostgreSQL 17 condicionado a la migración completa y compatibilidad del proveedor.
- Mercado Pago elegido; Truora en evaluación. No se contrató un servicio en esta entrega.
- [Decisiones C1](decisiones-c1.md): T1 parcial viable, T7 con duración propia
  sin solape, precio elegido por organizador, condiciones fijadas antes de publicar,
  MVP solo `PAID`, firmas, roles, cifrado, particiones y drand quicknet.
- ASS-001, confirmación contable y aportes humanos mantienen su estado.
  La revisión humana del desarrollo sigue suspendida; las segundas firmas del
  producto siguen exigidas. No se modifica el freeze.

La fuente nueva conserva .NET 8 y no incorpora todos estos acuerdos. Sus archivos
SQL/API V8 no sustituyen automáticamente al candidato C1 ni a sus 92 operaciones.

## Identidad y alcance de la siguiente emisión

La carpeta `c1-l3-v8` y `L3_V8_DRAFT` conservan su identidad de trabajo. Antes de
C2 se comprobará si la V8 recibida fue formalmente emitida. Si lo fue, se
preparará V9; si no, se resolverá una única V8 consolidada. No decidir la versión
solo por fecha o nombre de archivo.

L0/L2, L3, casos de uso, L4, API, SQL, semilla y backlog deben describir el mismo
flujo. C2 registrará las versiones afectadas, artefactos, resolver e historial en
un único acto, preservando los originales. CD-11 de la fuente reutiliza un
identificador anterior: su regla nueva necesita identidad inequívoca y correlación.

## Registro local de integración

`C1-Vxx` identifica trabajo local; no asigna CHANGE/DEC de Outline. «Grupos» remite
al catálogo 01–27 del informe conservado. `D-1…D-6` son decisiones de la fuente
Cowork; no son las `D-01…D-09` aprobadas del programa R0.

| ID | Prioridad | Grupos | Cambio incorporado al trabajo | Cierre pendiente / dueño |
|---|---|---|---|---|
| C1-V01 | P1 | 01, 02, 16, 26 | Plazo final en T1–T8 y cierre lógico; conservar parcial viable de T1 y duración T7 | Máximo de mercado, excepción T5/24 h, reloj y pago tardío; Diego |
| C1-V02 | P0 | 03, 04, 05, 21, 23 | Respaldo para entregar todos los premios; mínimo derivado y configuración inmutable | Caja disponible, fórmula/redondeo y correspondencia tickets/importe/mercado; Diego, contabilidad y abogado |
| C1-V03 | P0 | 07, 08, 15 | Fianza `VIABILITY_GAP`, custodia, devolución y ejecución como ciclo completo | Validación de fondos, T-19/20/21, cancelación y sobrantes; Diego, contabilidad y abogado |
| C1-V04 | P0 | 09, 14, 22 | Viabilidad comprobada antes de freeze/compromiso; FSM recuperable | Operación atómica, estados, precedencia, firmas y motor de guardas; Diego, código humano |
| C1-V05 | P1 | 10, 25 | Potencial de venta incluye reservas aún pagables; contadores coherentes | Corregir la fórmula y decidir recuperación tras falso positivo; Diego, código humano |
| C1-V06 | P1 | 06, 24 | Cierre por tipo: umbral T2, hito T4, todos los premios y elegibles T6 | Desenlaces por tipo y bases antes de publicar; Diego |
| C1-V07 | P0 | 12, 20 | Bases, checkout, lecturas, avisos y API con el mismo desenlace | Resolver cancelación frente a cobertura y ampliar contrato/L4; Diego y abogado |
| C1-V08 | P1 | 13, 23 | Coste de cobro/reembolso por canal; devolución íntegra al participante | Datos reales, caja, comisión y alcance de canales; Diego, contabilidad y abogado |
| C1-V09 | P2 | 11, 22 | Reputación por causa, con precedencia entre vacío, umbral y viabilidad | Imputabilidad, umbrales, apelación y reparación; Diego |
| C1-V10 | P1 | 14, 15, 20 | Semilla única/idempotente y cuentas completas; no declarar H-08 resuelto | Cuenta `adjustment`, intérprete FSM y pruebas de integridad; Diego, código humano |
| C1-V11 | P1 | 20 | Separar verificación documental, prueba SQL y comportamiento real | Checks fatales, SQLSTATE esperado y contraejemplos; dueño de cada prueba |
| C1-V12 | P1 | 19, 27 | Incorporar US-137–145 y sus dependencias sin adoptar el resumen Excel | Normalizar releases, sumar historias/épicas y desglosar esfuerzo humano; Diego |
| C1-V13 | P1 | 17, 18, 27 | Resolver maestro, artefactos, pies, CD-11 y procedencia | Confirmar emisión/aprobación y reconstruir trazabilidad; Diego, C2 |
| C1-V14 | P1 | 18, 20, 27 | Conservar stack, datos, baliza y contrato C1; distinguir cambios editoriales | Integración de acuerdos C1 aún pendientes y migración PG17 completa; Diego |

Todos los grupos tienen destino. Ningún hallazgo se cierra por registrar esta tabla.
La [aceptación técnica](reconciliacion-aceptacion.md) concreta V01–V11; las
[decisiones y planificación](reconciliacion-decisiones-planificacion.md) concretan
V06, V08, V09, V12–V14.

## Orden de trabajo

1. Resolver autoridad/versionado y condiciones del comprador, incluidos T1 y fianza.
2. Fijar el contrato económico, plazos, configuración, causas y cierre por tipo.
3. Integrar esa especificación en el candidato, API y L4; conservar lo aprobado en C1.
4. Recibir implementación humana de controles críticos y componer una migración única.
5. Validar migración/semilla/contrato, contraejemplos y coherencia del backlog.
6. Emitir en C2; habilitar código en D1 y probar servicios reales en D1/R1.

La documentación del nuevo flujo y sus controles no puede afirmar cobertura
efectiva mientras falle su gate. D-05 sigue permitiendo registrar H-01–H-03 sin
confirmación contable al emitir; no se añade una aprobación contable general
como puerta de C1. Antes de operar con dinero real deben cerrarse esos asuntos,
ASS-001 y el ciclo de caja. [LEGAL→ABOGADO]

## Entrega de esta actualización

- Registro completo de diferencias y decisiones conservadas.
- Casos de aceptación y pendientes por dueño/fase.
- Nueve historias nuevas incorporadas al plan con dependencias.
- Estado C1, diseño R0, candidato L3 y cierres SQL/API enlazados y actualizados.

Las fórmulas, plazos y fianza de la fuente se estudian como requisitos candidatos;
no se copió su SQL, no se modificó el canon ni se dio por probado un backend.
