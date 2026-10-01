---
title: C1 — estado de entrega y dependencias
status: borrador
tags: [r0, c1, seguimiento]
updated: 2026-10-01
description: Entregas C1, reconciliación Cowork y aportes pendientes, distinguiendo integración documental, emisión y operación real.
---

# Estado de C1

**C1 sigue abierto.** Hay un candidato completo de L3 V8, un contrato ampliado y
un overlay SQL no crítico verificable. El candidato incorpora ahora el alcance de
la [reconciliación Cowork](reconciliacion-linea-base.md) y las decisiones aprobadas
A–D. Los deltas Cowork sin ratificar y la migración completa siguen pendientes. No se ha emitido canon, levantado el
freeze ni implementado producto. La revisión humana obligatoria del desarrollo
continúa suspendida; las pruebas y la revisión automatizada siguen activas.

## Entregado

| Frente | Entrega y evidencia |
|---|---|
| Proveedores | Supabase Pro + Trigger.dev + Vercel Pro; techo de infraestructura US$250. Mercado Pago elegido. Truora priorizado para evaluar KYC/KYB, sin contratación |
| L3 | [Candidato completo](LIBOX_ESPECIFICACION_TECNICA_L3_V8_DRAFT.md), con TypeScript, sesiones, HMAC, recuperación, F1–F7 y registros de pendientes |
| Preservación | 32 bloques de código protegido de V7 conservados, salvo líneas vacías/espacios finales; prueba automática. No demuestra corrección del código heredado |
| API | OpenAPI 3.1 `2.0.0-draft.3`: 61 operaciones inventariadas +32 auxiliares; 50 pruebas, 93 intercambios HTTP de fixtures y 13 del cliente TypeScript |
| Mercado Pago | Payload `payment` y entradas de firma concretados. Sandbox, firma real, conciliación y efectos patrimoniales no probados |
| PostgreSQL | V7 instala en PG17.11 con 135 tablas. Overlay añade particiones UTC/DEFAULT para 11 padres (ledger pendiente), ACL B1 para 78 tablas (57 reservadas), logins B2 simulados y PE; tres escenarios pasan 100/100/104 comprobaciones |
| Herramientas DB | 27 pruebas, incluidas mutaciones que detectan permisos indebidos y limpieza tras fallo de arranque. CI ejecuta Docker en Python 3.12 |
| Truora | [Cobertura y brechas](truora-evaluacion.md), consulta preparada sin enviar y plan de aceptación. KYB Perú y precio por confirmar |
| Cowork | 27 diferencias comparadas con Claude Opus, 14 deltas C1-V, aceptación y US-137–145 incorporadas al plan. [Evidencia y límites](revision-cowork-evidencia.md); no es una emisión ni corrección ejecutada del gate |

Los conteos describen evidencia estructural/local. No prueban seguridad ni reglas
financieras del producto. SQL y artefactos mantienen estado de borrador.

## Seguimiento de decisiones integradas

- [Supabase/KMS](compatibilidad-supabase-kms.md): compatibilidad obligatoria; falta
  ratificar el alcance Auth, inventario, rotación y coste. El presupuesto anterior
  no incluye KMS. La [matriz B1](cierre-sql-riesgos-acl.md) aún expone datos de
  tablas operativas a reportería: resolver antes de usar datos reales.
- T1: mínimo, premio y condiciones fijados antes de publicar, sin cambios tras la
  primera compra. Umbral y premio siguen pendientes; bajo mínimo rige cancelación.
- [P-C](plantilla-documentos-pc.md): plantilla preparada, Diego coordina con el
  abogado; lista y fecha pendientes. Revisar en cada avance de C1.
- Segundas firmas: falta incorporar otra persona real antes de operar esas acciones.
  La revisión humana de desarrollo permanece suspendida.

## Aportes necesarios para cerrar C1

Las [decisiones C1](decisiones-c1.md) tomadas por Diego el 30/09 conservan su
aprobación y están integradas en el contrato, la norma L3 y la ACL no crítica.
Las diferencias nuevas que requieren definición
están en [decisiones Cowork](reconciliacion-decisiones-planificacion.md).

| Pendiente | Entrega concreta | Responsable |
|---|---|---|
| H-04 | Integridad del ledger en DB: cuenta/moneda, cuadre y líneas tardías; pruebas negativas | Diego, implementación humana |
| H-07/H-09 | INV-38 conserva dos administradores; revocación/suspensión concurrente y reactivación no eluden controles | Diego, implementación humana |
| H-08 | Incompatibilidades, punto único de transición, semilla FSM y bootstrap coherente de dos administradores | Diego, implementación humana en los controles críticos |
| H-10/H-11/H-12 | drand quicknet ratificada; codificación, verificador, valores independientes y almacenamiento de semilla cifrada pendientes | Diego, dueño humano del motor; [entrega delimitada](baliza-propuesta.md) |
| SQL restante | Matriz completa de roles, semillas pendientes y composición del SQL V8; ejecutar el conjunto, no solo overlay | Diego; ver [pendientes SQL](cierre-sql-pendientes.md) |
| Contratos auxiliares pendientes | Políticas A/C reflejadas; faltan lista P-C, valores T1, configuración completa, catálogos, apagado global, alcance sensible A10 y entrada del simulador. I-10/I-11 resueltos | Ver [cierre contractual](cierre-contratos.md); no generar reglas patrimoniales para llenar huecos |
| C1-V01–V11 | Política T1/fianza, mínimo/caja, relojes y FSM; controles humanos, contrato comprador y pruebas negativas | Diego; contabilidad/abogado según [aceptación](reconciliacion-aceptacion.md). Registrar no cierra el gate |
| C1-V12–V14 | Cuadrar backlog, identidad/Registro e integración de acuerdos C1 | Diego; [planificación](reconciliacion-decisiones-planificacion.md), antes de la emisión correspondiente |

Las sondas locales reproducen dos fallos del SQL heredado: permite revocar al
penúltimo `ADMIN_SUPER` y reactivar `ADMIN_FINANCE` sin segunda firma. Se registran
como **abiertos** aunque el ensayo de observación pase. No confundir ese verde
con una corrección de INV-38 o de privilegios.

La restricción vigente dice: «No generar ni modificar ese código; delimitar la
tarea y remitirla al dueño humano», en
[zonas sin IA](../../../../.claude/rules/zonas-sin-ia.md).
La suspensión de revisión no revoca esa restricción ni las segundas firmas del producto.
No se exige un segundo revisor ni reescribir bloques heredados sin defecto conocido.

## C2 y R1 no son puertas inventadas de C1

- **D-05 permite** conservar H-01–H-03 registrados sin confirmación contable al
  preparar C1 y emitir C2. ASS-001 sigue abierto; no afirmar preparación para
  dinero real mientras custodia y contabilidad no estén resueltas.
- **C2:** emisión del conjunto reconciliado con identidad resuelta, Registro/BASELINE
  y archivo de versiones anteriores intactas. V9 solo si se acredita emisión formal
  de la V8 recibida. Requiere aportes C1 y ratificación documental del candidato.
- **D1/R1:** backend, adaptadores reales, F1–F7, controles de permisos, sandbox,
  Supabase gestionado y ensayo integral de restauración. C1 especifica sus casos;
  no necesita fingir que los servicios reales ya fueron probados.
- La aceptación comercial de Mercado Pago y la evaluación de Truora deben quedar
  resueltas antes de habilitar sus flujos reales, no mediante ejemplos del mock.

La nueva suite verde PG16 no cierra los defectos de cobertura/fórmula observados,
ni acredita la migración completa PG17. Las validaciones locales heredadas de esta
tabla no incluyen aún los deltas Cowork.

## Reproducción

```sh
python3 -m unittest discover -s scripts/contracts/tests -q
python3 scripts/contracts/check_typescript.py
LIBOX_DB_DOCKER=1 python3 -m unittest discover -s scripts/database/tests -q
python3 scripts/database/c1_sql_check.py --escenario todos
python3 verify_corpus.py --dir docs/linea-base
```

Instalar antes las dependencias aisladas indicadas en [contratos](notas-contractuales.md).
Docker requiere la imagen fijada por digest; el runner no descarga sin indicación explícita.
