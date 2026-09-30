---
title: C1 — registro local CD-07 y cambios propuestos
status: borrador
tags: [r0, c1, l3-v8]
updated: 2026-09-30
description: Trazabilidad H-01 a H-19 sin asignar números del doc20 ni editar el canon.
---

# Registro local de cambios candidatos (CD-07)

Origen: [hallazgos técnicos](../2026-09-25-revision-sistema-hallazgos-l3.md).
Dueño disponible: Diego. Fecha: 2026-09-30. Estado general: propuesta documentada,
no emitida. C1-H identifica filas locales, no un CHANGE/DEC de Outline.
Documento afectado: L3 V7 y sus artefactos; candidato al backlog de cambio: sí.

| ID local | Cambio para el borrador | Evidencia necesaria para cerrar |
|---|---|---|
| C1-H01 | No dar por válido L-04 con purchase_liability ya consumida; evaluar momento de T-04/05/06 | Dictamen contable y casos de saldo suficiente antes/después de entrega/reembolso |
| C1-H02 | Especificar T-03, devolución al medio original y movimiento de cash_clearing | Matriz de asientos y prueba PSP aprobadas por dueño contable |
| C1-H03 | Separar cobro de reconocimiento de comisión/impuesto; decisión no tomada | Confirmación contable/tributaria [LEGAL→ABOGADO] |
| C1-H04 | Cuadre sobre asiento completo y moneda consistente; catálogo de cuentas referencial | Implementación humana que rechaza asiento desbalanceado/cuenta inexistente/moneda distinta |
| C1-H05 | Crear particiones iniciales y siguientes; mantener índices/restricciones | SQL completo aplicado a DB vacía, inserciones y rollover mensual en 12 tablas |
| C1-H06 | GRANT explícito por rol/tabla; login técnico separado de roles de grupo | Pruebas como libox_app/append/read/migrate, no solo como propietario |
| C1-H07 | Restituir mínimo 2 ADMIN_SUPER de PRD INV-38 | Rechazo de revocar/suspender al penúltimo, incluyendo concurrencia y bootstrap |
| C1-H08 | Completar transiciones, semillas, incompatibilidades y primer administrador | Migración completa con checks de cobertura; código crítico humano |
| C1-H09 | Cubrir reactivación por UPDATE de asignación revocada | Mismos controles que INSERT y test de privilegio/segunda firma |
| C1-H10 | Añadir resultados esperados de los 5 vectores, sin derivarlos del código bajo prueba | Valores producidos y verificados independientemente por implementador humano |
| C1-H11 | Diferenciar ronda y aleatoriedad; fijar algoritmo/formato del verificador | Especificación inequívoca y prueba pública independiente |
| C1-H12 | Persistir seed cifrada; elegir baliza y espera/alarma/reanudación | Modelo de claves y restore; baliza tardía/caída y compromiso preservado |
| C1-H13 | Reconciliar 61 operaciones candidatas con YAML de 16 operaciones; adoptar JSON Schema 3.1 | OpenAPI completo validado, métodos ambiguos resueltos, ejemplos/tipos/contratos |
| C1-H14 | Sustituir hash directo de DNI por HMAC versionado | Vectores de normalización/rotación y ausencia de DNI/claves en logs |
| C1-H15 | Definir RPO/RTO, PITR, copia de objetos y restauración | Ensayo integral cronometrado y reconciliado; no basta activar backup |
| C1-H16 | Pago tardío no produce tickets fuera del pool; excepción y devolución | Política ratificada, F7 y T-03 consistente |
| C1-H17 | TLS, CSP, WAF y límites por identidad/recurso | Pruebas de abuso y fallback, sin falsear garantía patrimonial |
| C1-H18 | Backend TypeScript/Next.js ratificado; retirar .NET8/Next14 en V8 | Proveedores elegidos, major PG decidido y CI TypeScript en D1 |
| C1-H19 | Alinear nombre/título/pie/versión y referencia PRD V9 | Validación de identidad + BASELINE/Registro en acto C2 |

## Borrador de migraciones y propiedad

Separar rol dueño/migrador de credenciales app; revocar permisos amplios implícitos,
definir defaults para tablas y particiones nuevas. Las pruebas negativas deben
intentar UPDATE/DELETE de datos de solo agregación con el rol real de aplicación.
No suponer que RLS o NOLOGIN implementan por sí solos el permiso requerido.

Inventario existente: 135 CREATE TABLE; 12 particionadas según auditoría original.
C2 requiere comprobar ese conteo contra el SQL final y sus dependencias. Crear
particiones no basta si el esquema/índices/FK fallan. En C1 probar insert, mes siguiente, permisos y límites UTC. La retención y
recuperación integral se ensayan antes de R1 conforme operación; no presentarlas
como pruebas ya ejecutadas ni como una puerta adicional del contrato C1.

La matriz de semillas incluye mercado PE, transiciones FSM, cuentas por moneda,
reglas T1–T8, incompatibilidades y bootstrap seguro. Cuentas/transacciones/triggers
patrimoniales y ejecución de incompatibilidades pertenecen a las zonas sin IA;
este registro especifica aceptación y **no entrega implementación generada**.

## Estado de cierre

Las notas de proveedores/operación/seguridad constituyen propuesta escrita para
estos hallazgos. Ninguno se marca resuelto solo por existir prosa. H-01–H-04 requieren
confirmación contable y código humano; H-10–H-12 requieren especificación cerrada e
implementación independiente. El resto exige artefactos o pruebas descritos arriba.

La siguiente versión debe ser autónoma: consolidar secciones no modificadas y
reemplazos aprobados, sin remitir a V7 como norma. Archivar V7 intacta y emitir V8,
Registro actualizado y BASELINE en un único acto de C2; este paquete no lo ejecuta.

La entrega actual se detalla en [cierre SQL](cierre-sql.md),
[cierre contractual](cierre-contratos.md) y [estado C1](estado-c1.md).
H-01–H-03 pueden permanecer registrados por D-05 del programa; no se exige
su confirmación contable para redactar C1 o emitir C2. Su apertura sí impide
afirmar preparación para operar con dinero real.
