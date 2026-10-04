---
title: C1 — decisiones pendientes y planificación tras Cowork
status: borrador
tags: [r0, c1, decisiones, backlog]
updated: 2026-10-04
description: Deltas sobre acuerdos C1, valores sin ratificar y dependencias de las nueve historias nuevas del backlog recibido.
---

# Decisiones y planificación tras Cowork

Anexo del [registro de integración](reconciliacion-linea-base.md). «Actualizar
nuestro trabajo» autoriza esta integración documental. No convierte automáticamente
en aprobados parámetros económicos, política de garantía o dictámenes legales.
Los acuerdos aprobados de [C1](decisiones-c1.md) se conservan literalmente.
Las [decisiones del 04/10](decisiones-2026-10-04.md) fijan el múltiplo 1,45 y
auditabilidad general; conservan proveedores y ratifican Auth administrada.
No convierten «queda» en valores de plazos/reputación ni en dictámenes recibidos.

## Diferencias que requieren decisión

| Tema | Acuerdo / problema verificado | Trabajo de decisión y dueño |
|---|---|---|
| T1 bajo mínimo | C1 ordena cancelar/reembolsar; Cowork permite continuar por garantía | Diego debe ratificar o descartar la ampliación. Mantener cancelación de C1 mientras no se resuelva; reflejar la ruta elegida en bases/checkout [LEGAL→ABOGADO] |
| Premio completo y respaldo | El nuevo piso pretende garantizar entrega, no solo devolución; valoración no garantiza disponibilidad del bien | Definir obligación, costes cubiertos, sustitución/adquisición y figura de custodia; Diego, contabilidad y abogado |
| Parámetros de mínimo | Fuente proponía PE 1,25; Diego fijó 1,45 el 04/10 | Completar fórmula, fuente de valoración, redondeo, caja y owner de configuración; no confundir el múltiplo con comisión; Diego y contabilidad |
| Ventanas de venta | `end_at` general; máximo de mercado sin valor; mínimo 24 h contradice Flash T5 de 15–240 min | Definir ubicación JSON y validación por tipo/mercado; Diego. Sin máximo no publicar; no inventar duración de un mes |
| Cobertura | Fuente propone 48 h y jobs de 1 min/1 h/10 min | Definir reloj, suspensión, reanudación, pagos tardíos y alarmas; Diego. El job no prolonga la venta ni el vencimiento |
| Cierre por tipo | Umbral T2, hito T4 y elegibles T6 no son intercambiables con el mínimo | Declarar tabla de desenlaces por tipo y precedencia; Diego |
| Reputación | Cancelación penalizada, con excepción T2; causas solapadas | Definir imputabilidad, umbral, duración, ascenso, reparación y apelación; Diego |
| Canales | Costes a cargo de LIBOX y refund íntegro; IAP aparece fuera del MVP web/PWA | Mantener Mercado Pago como canal elegido. No habilitar IAP sin revisar alcance/categoría y condiciones; Diego [LEGAL→ABOGADO] |
| Penalización económica | Tasa por reincidencia se menciona como futura | Mantener fuera del MVP; no crear comisión nueva por completar enums |
| Identidad/autoría | Dos candidatos V8 y CD-11 con distinto significado; snapshot sin aprobador completo | Confirmar emisión, aprobador/fecha y procedencia del SQL, sin inferir falta de autorización; Diego, C2 |

Los escenarios de caja/margen del análisis usaron retenciones hipotéticas. No son
tarifas vigentes, una aprobación de impuesto ni un dictamen sobre tiendas.
ASS-001 y cuestiones tributarias conservan sus validaciones. [LEGAL→ABOGADO]

## Nueve historias recibidas — C1-V12

Se incorporan al plan con su ID y estimación de origen. Las entregas abajo son
una **propuesta normalizada** R0–R3, no una nueva emisión del Backlog. R0 corresponde
a Fundación y R1 a Núcleo transaccional; no se conservan aliases R1 Venta/R2 Sorteo.
Los
controles económicos, de FSM y de inventario son implementación humana; las
historias mixtas requieren desglosar esa parte antes de planificar capacidad.

| Historia | SP origen | Trabajo | Entrega candidata | Dependencia previa |
|---|---|---|---|---|
| US-137 | 8 | Semilla FSM de 54 aristas | R0 | Política de cierre, precedencia y guardas; ejecución crítica humana |
| US-138 | 3 | Retorno de suspensión | R0 | Reloj/estados admisibles y misma ruta única de transición |
| US-139 | 3 | Derivar mínimo | R0 | Fórmula y configuración aprobadas; implementación humana |
| US-140 | 5 | Restricciones de viabilidad | R0 | US-139 + garantía/caja + carreras; implementación humana |
| US-141 | 5 | Costes por canal | R1 | Datos reales y política de coste/refund aprobada |
| US-142 | 5 | Checkout y mínimo | R1 | Desenlace T1/garantía y contrato público coherente |
| US-143 | 8 | Trabajos de cierre/inviabilidad/cobertura | R1 | Cierre lógico, fórmula potencial, FSM y F7 |
| US-144 | 5 | Semilla/cuentas/T-19/20/21 | R1 | Política de custodia y ciclo contable; aporte humano |
| US-145 | 13 | Cubrir brecha con garantía | R1 | Gate y ciclo de depósito/devolución/ejecución, no solo depósito |

Total recibido: **55 SP**. R1 debe ensayar el ciclo completo de garantía antes de
habilitarlo con dinero real: no diferir devolución/ejecución a R3 y anunciar que
el depósito ya está operativo. La descomposición de US-145 y cualquier extensión
operativa R2/R3 quedan por estimar; no se suman otros 13 SP ni se habilita una fase
con dependencias ausentes.

## Reconciliación del calendario y esfuerzo

| Medida comprobada en la fuente | Valor | Corrección pendiente |
|---|---|---|
| Historias Excel | 145 / 991 SP | Tabla única para resumen, épicas, releases y trabajo humano |
| Resumen recalculado | 136 / 936 SP / 30 sprints | Rangos terminan en fila 137 y omiten 138–146 |
| Épicas Markdown | 946 SP | Diferencia total 45 SP: 6 heredados y 39 adicionales |
| Calendario declarado nuevo | 31 sprints a 32 SP | División aritmética con capacidad supuesta; no forecast para Diego solo |
| Trabajo completamente «Prohibida» | 287 SP | «300 sin IA» necesita desglose de historias Parcial; no inferir los 13 restantes |

Ampliar fórmulas hasta fila 146 no basta: `R1 Venta`, `R2 Sorteo` y `R3 Resolución`
no coinciden con las claves del calendario. Normalizar primero y luego recalcular
sumas. No modificar Excel V3 congelado ni reemplazarlo por V4 sin emisión.

## Orden y entregables

1. **C1 documental:** decisiones pendientes, aceptación y dependencias registradas
   en esta entrega; terminar contrato consolidado tras las definiciones.
2. **C1 humano:** entregar controles/migración completos y pruebas negativas;
   semilla recibida no cierra H-04/H-08 ni integridad del dinero.
3. **C2:** resolver versión, CD-11/Registro, referencias residuales e historial;
   emitir conjunto coherente, incluyendo backlog corregido cuando corresponda.
4. **D1/R1:** CI/backend/PSP/Supabase y F1–F7 reales; capacidad medida de Diego,
   trabajo humano separado y calendario basado en dependencias.

L1 debe reflejar coste/caja del nuevo flujo; L4 y casos de uso deben reflejar
bases y desenlaces. L1, Enterprise, Guía, L4 y VIES cambian principalmente citas
en el paquete recibido; los tokens mantienen valores. El dossier y los tres V1
históricos no aportan una nueva aprobación legal. No se reabre un rediseño de
marca por esas diferencias editoriales.
