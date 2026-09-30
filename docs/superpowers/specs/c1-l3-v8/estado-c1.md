---
title: C1 — estado de entrega y dependencias
status: borrador
tags: [r0, c1, seguimiento]
updated: 2026-09-30
description: Entregas verificadas, aportes humanos concretos y límites entre C1, C2 y R1.
---

# Estado de C1

**C1 sigue abierto.** Hay un candidato completo de L3 V8, un contrato ampliado y
un overlay SQL no crítico verificable. No se ha emitido canon V8, levantado el
freeze ni implementado producto. La revisión humana obligatoria del desarrollo
continúa suspendida; las pruebas y la revisión automatizada siguen activas.

## Entregado

| Frente | Entrega y evidencia |
|---|---|
| Proveedores | Supabase Pro + Trigger.dev + Vercel Pro; techo de infraestructura US$250. Mercado Pago elegido. Truora priorizado para evaluar KYC/KYB, sin contratación |
| L3 | [Candidato completo](LIBOX_ESPECIFICACION_TECNICA_L3_V8_DRAFT.md), con TypeScript, sesiones, HMAC, recuperación, F1–F7 y registros de pendientes |
| Preservación | 32 bloques de código protegido de V7 conservados, salvo líneas vacías/espacios finales; prueba automática. No demuestra corrección del código heredado |
| API | OpenAPI 3.1 `2.0.0-draft.2`: 61 operaciones inventariadas +31 auxiliares; 29 pruebas, 92 intercambios HTTP de fixtures y 11 del cliente TypeScript |
| Mercado Pago | Payload `payment` y entradas de firma concretados. Sandbox, firma real, conciliación y efectos patrimoniales no probados |
| PostgreSQL | V7 instala en PG17.11 con 135 tablas. Overlay añade particiones UTC/DEFAULT para 11 padres (ledger pendiente), ACL no crítica y PE; tres escenarios pasan 63/63/67 comprobaciones |
| Herramientas DB | 21 pruebas, incluidas mutaciones que detectan permisos indebidos y limpieza tras fallo de arranque. CI ejecuta Docker en Python 3.12 |
| Truora | [Cobertura y brechas](truora-evaluacion.md), consulta preparada sin enviar y plan de aceptación. KYB Perú y precio por confirmar |

Los conteos describen evidencia estructural/local. No prueban seguridad ni reglas
financieras del producto. SQL y artefactos mantienen estado de borrador.

## Aportes necesarios para cerrar C1

Las decisiones de dominio que bloquean la integración están reunidas, con opciones
y recomendación, en el [paquete de decisiones](decisiones-c1.md).

| Pendiente | Entrega concreta | Responsable |
|---|---|---|
| H-04 | Integridad del ledger en DB: cuenta/moneda, cuadre y líneas tardías; pruebas negativas | Diego, implementación humana |
| H-07/H-09 | INV-38 conserva dos administradores; revocación/suspensión concurrente y reactivación no eluden controles | Diego, implementación humana |
| H-08 | Incompatibilidades, punto único de transición, semilla FSM y bootstrap coherente de dos administradores | Diego, implementación humana en los controles críticos |
| H-10/H-11/H-12 | Fuente y codificación de baliza, verificador sin ambigüedad, valores esperados independientes y almacenamiento de semilla cifrada | Diego, dueño humano del motor; [entrega delimitada](baliza-propuesta.md) |
| SQL restante | Matriz completa de roles, semillas pendientes y composición del SQL V8; ejecutar el conjunto, no solo overlay | Diego; ver [pendientes SQL](cierre-sql-pendientes.md) |
| Contratos auxiliares pendientes | Configuración T1–T8, datos de mercado completos, decisiones I-01 a I-09; I-10 e I-11 resueltos | Ver [cierre contractual](cierre-contratos.md); no generar reglas patrimoniales para llenar huecos |

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
- **C2:** emisión de L3 V8 y artefactos, Registro/BASELINE y archivo de V7 en un
  acto coherente. Requiere los aportes de C1 y ratificación documental del candidato.
- **D1/R1:** backend, adaptadores reales, F1–F7, controles de permisos, sandbox,
  Supabase gestionado y ensayo integral de restauración. C1 especifica sus casos;
  no necesita fingir que los servicios reales ya fueron probados.
- La aceptación comercial de Mercado Pago y la evaluación de Truora deben quedar
  resueltas antes de habilitar sus flujos reales, no mediante ejemplos del mock.

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
