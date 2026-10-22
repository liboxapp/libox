---
title: Evaluación contable de la adquisición sustitutiva para Adrián
status: borrador
tags: [rev6, act-r6-08, h22-01, contabilidad, evaluacion, adrian]
updated: 2026-10-18
description: Encargo de análisis para Adrián y su agente IA sobre T-05, financiación de T-19, compensaciones y reversión.
---

# Evaluación contable de la adquisición sustitutiva para Adrián

**Solicitante:** Diego. **Destinatarios:** Adrián, CEO, y su agente IA. **Fecha:** 18 de octubre de 2026. **Seguimiento:** ACT-R6-08 / H22-01.

Adrián debe evaluar cómo financiar la compra y entrega de premios cuando incumple el organizador. Se solicita a su agente un análisis independiente del modelo propuesto, sus alternativas y sus límites, para que Adrián pueda concluir qué aceptar, corregir o rechazar. La compensación descrita aquí está pendiente de evaluación y aprobación; H22-01 sigue abierto.

**Base de análisis:** paquete de trabajo rev6 y decisiones posteriores registradas. La aceptación formal conjunta y la emisión del corpus reconciliado siguen pendientes.

## Decisiones económicas ya aprobadas por Diego

1. Cubrir primero el coste real de adquirir y entregar los premios.
2. Conservar la comisión publicada hasta donde alcance el saldo, renunciando a la parte necesaria.
3. Mantener el sobrante como obligación con el organizador.
4. Registrar comisión e impuesto sólo después de acreditar las entregas vigentes de **todos los ganadores del sorteo**, sin devengo parcial en el MVP. El pago al organizador conserva las demás compuertas.

Los costes y el tope se consideran **agregados por sorteo**, incluyendo todas sus adquisiciones y entregas. El destino de la compra sustitutiva es el proveedor del bien. La ruta nace de una adjudicación competente de incumplimiento de entrega; no de una decisión administrativa discrecional. Si se propone cambiar alguna decisión económica anterior, se debe señalar el cambio y solicitar una nueva decisión expresa.

El PRD exige autorización de `ADMIN_LEGAL_COMPLIANCE` y segunda firma de `ADMIN_FINANCE`, personas distintas con subroles vigentes. Son controles del producto; no designan a socios como ejecutores ni sustituyen el tratamiento de ajustes T-14.

## Problema de T-05 y T-19

El contrato de trabajo rev6 exige T-05 al confirmar el pago. Ese asiento mueve el neto de la orden desde `purchase_liability`, obligación frente a los participantes, hacia `client_payable`, obligación con el organizador. El dinero permanece retenido, pero la obligación ya está distribuida entre cuentas.

T-19, que registra la compra sustitutiva, debita `purchase_liability` y acredita `cash_clearing`. Esa primera cuenta puede conservar sólo la parte asociada a la comisión aún no devengada. Por tanto, **tener dinero retenido no demuestra que el asiento actual tenga saldo suficiente en la cuenta que debita**. Esta tensión es H22-01 y está reconocida en PRD §10.3 y L3 §6.2.

Revertir sólo la orden del ganador no garantiza financiación: el premio se cubre con la recaudación del sorteo, no necesariamente con lo pagado por ese ganador. Deben mantenerse las referencias de las órdenes, el sorteo y cada adquisición para reconstruir el origen de la obligación.

## Alternativas que debe comparar el agente

| Alternativa | Tratamiento que se evaluará | Pregunta crítica |
|---|---|---|
| A. Mantener T-05 y añadir compensación específica | Reducir parte del pasivo del organizador y llevarla a `purchase_liability` antes de T-19. Es la propuesta técnica inicial presentada a Diego. | ¿La compensación expresa correctamente la obligación extinguida, su fundamento contractual y su relación con cada adquisición? |
| B. Revertir T-05 del ámbito afectado y devengar de nuevo el saldo final | Reponer la obligación previa y calcular después el importe que corresponde al organizador. | ¿Cómo se conserva RN-45, la historia por orden y el tratamiento de varias adquisiciones sin revertir ventas válidas? |
| C. Rediseñar las contrapartidas de T-19 | Financiar el coste contra los pasivos que realmente lo soportan, modificando el catálogo y la secuencia si corresponde. | ¿Produce una representación más clara sin mezclar fondos, duplicar costes ni eludir INV-36? |

Las tres opciones requieren evaluar referencias, controles y una futura emisión cuando corresponda. No se debe escoger A por ser la recomendación inicial; se pide buscar contraejemplos y recomendar otra opción si representa mejor los derechos y obligaciones.

## Desarrollo de la alternativa A para evaluación

1. Conservar el T-05 original y los importes de la orden pagada.
2. Tras la autorización competente y antes del asiento de compra, registrar una operación específica que **debite `client_payable` y acredite `purchase_liability`**. Su importe propuesto es el menor entre el coste que se va a registrar y el saldo retenido del organizador atribuible a ese sorteo, sin reutilizar importes ya compensados.
3. Registrar T-19 por el coste real de compra y entrega: **débito a `purchase_liability` y crédito a `cash_clearing`**, vinculado a la adquisición y al desembolso. El coste que exceda el pasivo disponible del organizador consume la parte de comisión todavía no devengada, dentro del tope agregado autorizado.
4. Acoplar compensación y T-19 de modo que no persista una mitad del registro. El pago externo debe tener conciliación y recuperación de fallos; una transacción local no vuelve atómico al proveedor externo.
5. Al acreditar todas las entregas, determinar la comisión conservada y la renuncia. Mantener los importes publicados de las órdenes; representar la renuncia y la reducción del saldo final de forma explícita. Validar T-04/T-06 y sus referencias sin reconocer dos veces la comisión.
6. Revertir con asientos nuevos, vinculados y por importes justificados. Un dinero pagado no vuelve al ledger por cambiar un estado: hay que distinguir recuperación efectiva, recuperación parcial y pérdida.

La compensación es una operación candidata de dominio: **su código canónico todavía no está definido**. No se propone reutilizar T-14 como atajo general ni editar asientos existentes. Debe evaluarse si requiere alta en el catálogo, motivo, autorizaciones y nuevas restricciones.

## Ejemplo aislado de saldos

Supuestos ilustrativos: S/1.000 cobrados y retenidos, comisión máxima publicada de S/200 y neto inicial del organizador de S/800. Se omiten costes del PSP, contracargos y reservas en este ejemplo. La comisión indicada es el importe total antes de separar el impuesto aplicable; no fija una tasa comercial ni tributaria.

| Momento para un coste de S/700 | Efectivo retenido | `purchase_liability` | `client_payable` |
|---|---:|---:|---:|
| Después del pago y T-05 | S/1.000 | S/200 | S/800 |
| Compensación de S/700 | S/1.000 | S/900 | S/100 |
| Pago al proveedor mediante T-19 | S/300 | S/200 | S/100 |

Sólo después de acreditar todas las entregas se registra la comisión conservada: S/200 en este caso. Los S/100 permanecen como obligación con el organizador hasta que proceda su liquidación.

| Coste agregado de compra y entrega | Comisión conservada propuesta | Renuncia de comisión | Sobrante del organizador |
|---|---:|---:|---:|
| S/700 | S/200 | S/0 | S/100 |
| S/950 | S/50 | S/150 | S/0 |
| S/1.000 | S/0 | S/200 | S/0 |

En el segundo caso, A trasladaría S/800 desde `client_payable`, T-19 consumiría S/950 de `purchase_liability` y quedarían S/50 antes del devengo de la comisión. Esta aritmética describe el caso aislado; el agente debe demostrar cómo se conserva al incorporar todos los demás asientos.

## Casos que debe resolver el análisis

| Caso | Comprobación requerida |
|---|---|
| Entrega normal por el organizador | Mantener T-05 al pago y T-04/T-06 tras todas las entregas, sin compensación ni T-19. |
| Adquisición por S/700, S/950 y S/1.000 | Mostrar cuentas antes y después y reproducir el reparto anterior sin saldos negativos ni ingresos anticipados. |
| Dos adquisiciones de S/700 y S/250 | Aplicar el límite y la renuncia al total de S/950. No reservar dos veces la comisión completa ni financiar dos veces el mismo coste. |
| Autorizaciones concurrentes y repetición de eventos | Considerar pagado y comprometido; impedir sobrecompromiso, doble compensación y doble desembolso. |
| Costes del PSP | T-02 ya registra gasto del PSP. Con cobro bruto S/1.000 y coste S/30 quedan S/970 en el proveedor: explicar cómo se financia una adquisición de S/1.000 sin fingir efectivo ni deducir dos veces el coste. No cargarlo silenciosamente al organizador. |
| Impuestos y comisión reducida | Explicar la base, el reconocimiento y el redondeo de la comisión efectiva, manteniendo el impuesto incluido cuando corresponda. Base, contribuyente y encuadre fiscal están sujetos a L-05. |
| Contracargos, devoluciones y reservas | Definir qué fondos están disponibles o comprometidos. No tratar una reserva o fondos de otro sorteo como dinero libre. |
| Cancelación antes de comprar | Reponer las obligaciones necesarias y permitir devolución íntegra sin duplicar compensaciones ni reembolsos. |
| Cancelación después de pagar S/700 | Si el proveedor devuelve S/700, mostrar la recuperación y las reversiones. Si devuelve S/650 o nada, identificar el faltante de S/50 o S/700 para devolver íntegramente; no crear efectivo mediante una reversión ficticia. |
| Fallo del pago externo | Resolver pago confirmado con registro local incompleto, respuesta incierta y reintento. No dar por fallido un desembolso cuya situación aún no se conoce. |

## Cuestiones para la conclusión de Adrián

- Definir qué significa el saldo disponible y conciliar recaudación bruta, `psp_clearing`, `cash_clearing`, costes, devoluciones, reservas y compromisos. Los S/1.000 del ejemplo no resuelven esa definición.
- Determinar el tratamiento de costes no recuperables y quién aporta liquidez si la devolución íntegra supera los fondos restantes. Esta evaluación no aprueba un presupuesto ni un subsidio ilimitado.
- Confirmar cómo el neto original de la orden y la comisión congelada conviven con la compensación por incumplimiento. Distinguir los importes históricos de la venta de la obligación final de liquidación; revisar RN-01-bis, RN-45 y TX-01.
- [LEGAL→ABOGADO] Verificar el fundamento contractual para compensar obligaciones del organizador y disponer de la recaudación. La titularidad/custodia de fondos y las condiciones del PSP siguen abiertas en ACT-R6-04/03; una solución del ledger no las autoriza por sí sola.
- Separar el ledger operativo del producto del encuadre contable y fiscal formal. NIIF 15 exige analizar el contrato y las obligaciones de desempeño; no valida automáticamente estos asientos ni el modelo regulatorio de LIBOX.

## Encargo y formato de respuesta del agente IA

Analiza las fuentes y las alternativas con criterio independiente. Distingue hechos del corpus, decisiones posteriores registradas, supuestos del ejemplo y propuestas. Ante un conflicto, cita la sección y explica qué decisión o emisión lo resolvería. Si una fuente no está disponible, identifica la conclusión afectada y solicita ese contenido; no atribuyas una validación inexistente.

Entrega: **1)** veredicto sobre A —viable, viable con cambios o no viable— y razones; **2)** comparación con B/C; **3)** secuencia completa de débitos, créditos, importes y referencias para los casos; **4)** contraejemplos, controles y decisiones aún necesarias; **5)** reparto de preguntas entre Adrián, Diego y validación contable/legal/PSP; **6)** texto breve de la decisión recomendada para que Adrián pueda aprobar, modificar o rechazar explícitamente. Una recomendación del agente no cuenta como aprobación de Adrián.

El encargo es de análisis y documentación. No ejecutar SQL, pruebas del producto, pagos ni cambios de canon. La implementación de asientos continúa bajo propiedad humana de Diego. La revisión actual no adelanta la fase de desarrollo ni reactiva la revisión humana obligatoria suspendida.

## Fuentes y condiciones de cierre

- [Decisiones de Diego](https://liboxapp.getoutline.com/doc/diego-pendientes-y-decisiones-tecnicas-rev6-dET6AASY9e): ACT-R6-08 y ACT-R6-09; prioridad económica y momento de comisión aprobados el 18/10/2026. La compensación sigue propuesta.
- [PRD V22](https://liboxapp.getoutline.com/doc/libox-prd-blueprint-mvp-v22-wp9CiWihnf): §10.3, RN-45; §16.7, RN-114-bis y RN-255…258. [L3 V21](https://liboxapp.getoutline.com/doc/libox-especificacion-tecnica-l3-v21-yC2vKLLNbN): §6.1, §6.2, §6.2.1 y §6.5.
- [Registro V24](https://liboxapp.getoutline.com/doc/libox-registro-maestro-de-linea-base-v24-TBDcjlR1hE): H22-01/02/06/07. [Tablero](https://liboxapp.getoutline.com/doc/21-tablero-de-acciones-tasks-iCoCY5qOjR): estados, dependencias y decisiones conjuntas.
- [IFRS Foundation sobre NIIF 15](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-15-revenue-from-contracts-with-customers/): marco general de reconocimiento; no determina por sí solo el tratamiento particular de LIBOX.

El cierre de la **definición** requiere conclusión explícita, asientos y escenarios conciliados, supuestos pendientes identificados y cambios documentales especificados. El cierre **técnico de H22-01** requiere además la emisión que corresponda, implementación humana y evidencia de verificación en desarrollo. Este documento entrega la consulta; no acredita ninguno de esos cierres.
