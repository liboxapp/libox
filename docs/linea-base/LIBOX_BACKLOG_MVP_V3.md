# Índice de contenidos

# 0\. Control documental

**Documento:** LIBOX\_BACKLOG\_MVP\_V3 **Versión:** V3 **Reemplaza:** LIBOX Backlog MVP V2 (deprecado en su totalidad) **Deriva de:** PRD MVP V8 (L2) · Especificación Técnica L3 V7 (L3) · Design System L4 V1 (L4) · Matriz de Casos de Uso V1 **Gobernado por:** LBPF V3 (L0) **Entregable operativo asociado:** `LIBOX_BACKLOG_MVP_V3.xlsx`

## 0.1 Changelog

| Versión | Qué cambió                                                    | Por qué                                                                                                                                     |
| ------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| V3      | **24 historias nuevas, +191 SP**                              | Decisiones acumuladas en la sesión de auditoría, con sus cuatro resoluciones de conflicto                                                   |
| V3      | **R5 dividido en R5 y R6**                                    | Con las historias nuevas, R5 alcanzaba 261 SP: ocho sprints. **Eso no es una entrega, es una fase**, y menos aún si contiene el lanzamiento |
| V3      | Zonas sin generación asistida ampliadas a **261 SP**          | Las restricciones de rango, régimen y campaña con cupo son código de dinero y de concurrencia                                               |
| V3      | **Congelamiento de alcance declarado**                        | §5.1                                                                                                                                        |
| V2      | **Replanificación completa sobre el alcance real**            | El v1 declaraba 191 SP en 7 sprints. El alcance de la línea base vigente es de 936 SP                                                       |
| V2      | Historias trazadas a reglas `RN` e invariantes `INV`          | El v1 citaba anexos que estaban vacíos                                                                                                      |
| V2      | **Zonas sin generación asistida declaradas**                  | El equipo dispone de asistentes de IA; hay código donde su uso está prohibido                                                               |
| V2      | Factor de optimización por asistencia aplicado por bloque     | Aplicar un factor uniforme habría sobrestimado la ganancia en los caminos de dinero                                                         |
| V2      | Dos gates binarios de fase                                    | El v1 tenía un único ensayo con dinero real                                                                                                 |
| V2      | Alcance completo de construcción con **encendido progresivo** | Decisión del fundador: opción 2                                                                                                             |

## 0.2 Por qué el v1 no era corregible

No fue una desviación de estimación. El v1 planificaba contra un PRD cuyo esquema tenía 6 de 45 tablas con columnas, cuyos 26 contratos carecían de tipos y cuyos 14 de 16 anexos estaban vacíos. Historias como *migrar las 45 tablas conforme al §7.1* apuntaban a un capítulo que no existía.

Hoy el esquema **se ejecuta con cero errores** contra PostgreSQL 16 y sus restricciones están probadas contra casos que deben fallar. Las historias de este backlog apuntan a especificación real.

# 1\. Parámetros de planificación

| Parámetro               | Valor                                  |
| ----------------------- | -------------------------------------- |
| Equipo                  | 4 personas, perfil generalista         |
| Velocidad estimada      | **32 SP por sprint** de dos semanas    |
| Alcance total           | **936 SP** · 136 historias · 39 épicas |
| Duración                | **30 sprints ≈ 60 semanas ≈ 14 meses** |
| Alcance de construcción | **Completo** (opción 2)                |
| Encendido               | **Progresivo por configuración**       |

## 1.1 Cómo se llegó a 739 SP

| Etapa                                   | SP      | Nota                                                                               |
| --------------------------------------- | ------- | ---------------------------------------------------------------------------------- |
| Backlog V2                              | 745     | Alcance previo a la sesión de auditoría                                            |
| Decisiones acumuladas                   | \+191   | Control de funciones, regímenes sin recaudación, promocional, descubrimiento, Club |
| **Total del backlog V3**                | **936** | 136 historias                                                                      |
| Estimación por bloques de la línea base | 906     | Suma de los módulos del PRD y L3                                                   |
| Optimización por asistencia de IA       | −211    | Factor por bloque, §1.2                                                            |
| Revisión humana de zonas críticas       | \+50    | No se compensa: se presupuesta                                                     |
| **Total del backlog**                   | **745** | 136 historias                                                                      |

**El delta respecto de la estimación en bloque es normal.** Al descomponer aparece trabajo que el bloque agregaba: estados de error, casos de borde, datos semilla, pruebas de contrato.

## 1.2 Factor de asistencia por bloque

| Bloque                    | Factor   | Fundamento                                                   |
| ------------------------- | -------- | ------------------------------------------------------------ |
| Esquema y migraciones     | 0,45     | DDL validado y ejecutado; la generación es transcripción     |
| Contratos y capa de API   | 0,50     | Tipos generables desde `openapi.yaml`                        |
| Frontend y superficies    | 0,60     | Sistema de diseño con tokens y componentes especificados     |
| Growth y comercial        | 0,60     | Baja criticidad, patrones conocidos                          |
| Analítica y alarmas       | 0,65     | Esquema de eventos definido                                  |
| Lógica de dominio         | 0,75     | Requiere juicio; la especificación acelera pero no sustituye |
| Resolución y registrables | 0,80     | Flujo largo con muchas reglas de estado                      |
| Riesgo, PLAFT, protección | 0,85     | Consecuencia legal; verificación intensiva                   |
| **Caminos de dinero**     | **0,95** | El cuello es la revisión, no la escritura                    |
| **Motor de sorteo**       | **1,00** | **Sin ganancia. Se escribe a mano**                          |

**El límite estructural:** la asistencia acelera escribir código, no revisarlo. En código que mueve dinero el cuello es la revisión y no se comprime. Generar el triple con la misma capacidad de revisión degrada calidad en lugar de aumentar velocidad.

## 1.3 Zonas sin generación asistida

Se escriben a mano y se revisan por una segunda persona. **Propiedad fija, no rotatoria.**

| Zona                                                                   | Motivo                                                    |
| ---------------------------------------------------------------------- | --------------------------------------------------------- |
| Motor de sorteo, serialización canónica y verificación                 | Un error silencioso invalida la tesis del producto        |
| Asientos contables y transacciones canónicas                           | Un desbalance no detectado se propaga a todo el histórico |
| Concurrencia: reserva de inventario, bloqueo de saldo, ejecución única | Los errores solo aparecen bajo carga                      |
| Comprobaciones de incompatibilidad de subrol en ejecución              | Son la defensa contra fraude interno                      |
| Cálculo de la comisión y del impuesto incluido                         | Afecta el neto de cada organizador                        |

**261 SP —el 28 % del backlog— están marcados como zona sin generación asistida.** Las restricciones de rango de recaudación, régimen económico y campaña con cupo atómico son código de dinero y de concurrencia.

**Regla de propiedad:** en estas cinco zonas, una persona es dueña y otra revisa, ambas fijas durante toda la construcción. En el resto, rotación libre.

## 1.4 Reglas del backlog

| \#    | Regla                                                                                                          |
| ----- | -------------------------------------------------------------------------------------------------------------- |
| BR-01 | Toda historia declara al menos una `RN` o un `INV` verificable por prueba automatizada                         |
| BR-02 | Una historia sin criterio de aceptación comprobable no entra al sprint                                         |
| BR-03 | Los contratos y tipos se **generan** desde `openapi.yaml` y desde el esquema, no se escriben como historia     |
| BR-04 | Toda historia que toque dinero exige revisión de segunda persona antes de fusionar                             |
| BR-05 | LINT-003, LINT-004 y LINT-005 bloquean la fusión desde el primer sprint                                        |
| BR-06 | Ninguna historia se cierra sin sus pruebas de propiedad cuando afecta a un invariante                          |
| BR-07 | Todo tipo de sorteo y categoría de premio se construye **habilitado en el modelo y apagado por configuración** |
| BR-08 | El esquema se ejecuta con cero errores en cada integración; es criterio de fusión                              |

## 1.5 Definición de terminado

Código revisado por segunda persona · pruebas unitarias y de integración en verde · prueba de contrato conforme a `openapi.yaml` · prueba de propiedad cuando afecta a un invariante · verificación estática conductual sin bloqueo · trazabilidad `RN`/`INV` documentada · sin deuda de seguridad conocida.

# 2\. Entregas y calendario

| Entrega                          | Sprints | SP  | Contenido                                                                                                      | Gate                                                   |
| -------------------------------- | ------- | --- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| **R0 Fundación**                 | 1–3     | 102 | Plataforma, esquema, identidad, control de acceso, observabilidad, configuración                               | Esquema ejecutado y las 11 incompatibilidades probadas |
| **R1 Núcleo transaccional**      | 4–11    | 243 | Sorteo, tipos, premio, catálogo, compra, pagos, tickets, motor de sorteo, contabilidad                         | **Ensayo en entorno controlado**                       |
| **R2 Confianza y resolución**    | 12–15   | 131 | Salas, atestación, controversias, liquidación, no entrega y re-sorteo                                          | Ciclo completo atestado y liquidado                    |
| **R3 Cumplimiento y protección** | 16–18   | 102 | Prevención financiera, protección del usuario, riesgo, alarmas, indicadores                                    | Auditoría interna de cumplimiento                      |
| **R4 Catálogo ampliado**         | 19–21   | 97  | Categorías P-B, P-D, P-C1, P-C2 y tipos restantes                                                              | Dictámenes legales incorporados                        |
| **R5 Plataforma y regímenes**    | 22–25   | 136 | Control de funciones, ventanas, paneles, cuentas internas, entrada gratuita, promocional, rango de recaudación | Pruebas negativas de las restricciones nuevas          |
| **R6 Crecimiento y lanzamiento** | 26–30   | 125 | Descubrimiento, atribución, LIBOX Club, multi-mercado, rendimiento, endurecimiento                             | **Ensayo con dinero real**                             |

**Por qué R5 se dividió.** Con las 24 historias nuevas, la entrega original alcanzaba 261 SP —ocho sprints—. **Una entrega de ocho sprints no es una entrega: es una fase**, y tenerla como la última, con el lanzamiento dentro, concentraba todo el riesgo en el tramo final. Ahora ninguna entrega supera los ocho sprints y el lanzamiento queda aislado en R6.

## 2.1 Los dos gates binarios

**Gate R1 — Ensayo en entorno controlado.** Ciclo completo en entorno aislado con proveedor de pagos en modo de pruebas: alta de organizador, aprobación, verificación de premio, publicación, compra, congelamiento, sorteo, verificación pública por un tercero, asientos contables cuadrados.

**Advertencia registrada.** El entorno controlado valida la lógica, **no la realidad**. Los entornos de prueba de proveedores difieren en tiempos de notificación y en modos de fallo, y sobre todo **el contracargo no puede simularse**. Una transferencia de liquidación a cuenta bancaria real, tampoco.

**Gate R5 — Ensayo con dinero real.** Innegociable. **Antes de que un solo usuario del público pague, tiene que haber ocurrido un ciclo completo con dinero real**, incluida la liquidación efectiva a una cuenta bancaria. Ningún resultado parcial lo satisface.

## 2.2 Encendido progresivo

El alcance de construcción es completo. El **encendido** se secuencia, y es gratis porque todo vive tras bandera en `client_capabilities` y `market_config`.

| Momento                      | Encendido                                                |
| ---------------------------- | -------------------------------------------------------- |
| Lanzamiento                  | T1 y T3 · categorías P-A y P-E · mercado PE              |
| \+1 mes                      | P-B y P-D · tipo T2                                      |
| \+2 meses                    | P-C1, con dictámenes L-02 a L-04 y L-08 a L-11 resueltos |
| \+3 meses                    | Tipos T4 a T8                                            |
| Tras 3 sorteos P-C1 exitosos | P-C2                                                     |

## 2.3 Restricción operativa

**Las 11 incompatibilidades duras de control de acceso exigen personas naturales distintas.** Con 4 personas eso es el mínimo exacto, sin redundancia: si falta quien tiene `ADMIN_FINANCE` no se ejecuta ninguna liquidación; si falta quien da la segunda firma no se aprueba ningún premio de banda alta.

**El riesgo real no es el calendario: es el mes 12.** Las cuatro personas que construyeron pasan a operar salas de resolución, valorar premios, resolver alarmas con plazo de 24 horas y adjudicar controversias en 10 días. Operar el alcance completo no cabe en cuatro personas.

Por eso el encendido progresivo no es una recomendación de producto: es una **condición de viabilidad operativa**.

# 3\. Épicas

## R0 · Fundación — 102 SP

| ID  | Épica                                       | SP | Contenido                                                                                       | Traza                            |
| --- | ------------------------------------------- | -- | ----------------------------------------------------------------------------------------------- | -------------------------------- |
| E01 | Plataforma y entornos                       | 21 | Repositorio, integración continua, entornos, secretos, contenedores, datos semilla anonimizados | RN-223                           |
| E02 | Esquema y migraciones                       | 18 | Las 26 migraciones, 114 tablas, particiones, roles, disparador de cuadre                        | RN-219 a RN-222 · INV-10         |
| E03 | Identidad y autenticación                   | 21 | Registro, unicidad, verificación de contacto, testigos, prueba de vida, vigencia documental     | INV-08 · RN-115 a RN-125         |
| E04 | Control de acceso y separación de funciones | 21 | 21 subroles, 11 incompatibilidades, multifactor, segunda firma                                  | INC-01 a INC-11 · RN-05, RN-06   |
| E05 | Observabilidad y auditoría                  | 13 | Traza extremo a extremo, auditoría encadenada, cola de emergencia, bandeja de salida            | RN-203 a RN-207                  |
| E06 | Configuración por mercado                   | 8  | `market_config` versionado, vigencia, adaptadores                                               | INV-15, INV-29 · RN-174 a RN-177 |

## R1 · Núcleo transaccional — 238 SP

| ID  | Épica                                      | SP | Contenido                                                                                            | Traza                                      |
| --- | ------------------------------------------ | -- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| E07 | Dominio de sorteo y máquina de estados     | 21 | FSM única de 22 estados, punto de entrada único, registro de transiciones                            | RN-09 a RN-11                              |
| E08 | Tipos T1–T8 y capacidades                  | 13 | Semilla de los ocho tipos, capacidades por cliente y por mercado                                     | RN-12 a RN-14-ter · INV-17                 |
| E09 | Premio, categorías y gate de valoración    | 34 | Seis categorías, dos regímenes, bandas, regla de desviación, código del día, verificaciones externas | RN-20 a RN-24 · INV-28                     |
| E10 | Catálogo, detalle y simulador              | 34 | Superficies públicas, tarjeta con seis ranuras, simulador de recaudación                             | RN-39 · OB-01 a OB-08                      |
| E11 | Compra, idempotencia e inventario          | 34 | Orden, clave por intento, reserva atómica, concentración, recuperación de estado                     | RN-52 a RN-56 · INV-13                     |
| E12 | Pagos y conciliación                       | 34 | Adaptador, firma, deduplicación, monotonía, conciliación, contracargos                               | RN-57 a RN-65                              |
| E13 | Tickets y pool                             | 13 | Emisión, numeración correlativa, anulación sin reciclaje                                             | INV-09, INV-11                             |
| E14 | **Motor de sorteo y verificación pública** | 34 | Compromiso, baliza, ejecución, sin reemplazo, prueba, página pública                                 | INV-18, INV-18-bis, INV-19 · RN-66 a RN-71 |
| E15 | Contabilidad de partida doble              | 21 | Plan de cuentas, 14 transacciones, impuesto incluido, invariantes diarios                            | INV-10, INV-34 a INV-36 · RN-43 a RN-48    |

## R2 · Confianza y resolución — 131 SP

| ID  | Épica                         | SP | Contenido                                                                               | Traza                             |
| --- | ----------------------------- | -- | --------------------------------------------------------------------------------------- | --------------------------------- |
| E16 | Sala de resolución            | 34 | Creación, participación, secuencia, cadena de hashes, minimización, exportación forense | RN-72 a RN-83 · INV-20            |
| E17 | Atestación y evidencia        | 21 | Jerarquía probatoria, atestación, envío, plazos con casuística                          | RN-84 a RN-89 · INV-07, INV-21    |
| E18 | Controversias y adjudicación  | 21 | Reclamo estructurado, inversión de carga, controles de canal, adjudicación              | RN-90 a RN-100 · INV-22           |
| E19 | Liquidación y gates           | 34 | Seis gates, estados, retención, reserva, pago en lote y con segunda firma               | RN-101 a RN-105 · INV-23          |
| E20 | No entrega, re-sorteo y saldo | 21 | Rutas, plazos por tramo, re-sorteo encadenado, saldo de reembolso, contacto             | RN-106 a RN-114 · INV-24 a INV-26 |

## R3 · Cumplimiento y protección — 102 SP

| ID  | Épica                              | SP | Contenido                                                                    | Traza                    |
| --- | ---------------------------------- | -- | ---------------------------------------------------------------------------- | ------------------------ |
| E21 | Prevención financiera              | 26 | Acumuladores, tramos, diligencia previa, expedientes, registro, reserva      | RN-139 a RN-145 · INV-27 |
| E22 | Protección del usuario             | 21 | Autoexclusión, límites con asimetría, panel de gasto, aviso de independencia | RN-128 a RN-138          |
| E23 | Riesgo y antifraude                | 21 | Motor de reglas, concentración, autocompra, correlación, congelamiento       | RN-146 a RN-152 · INV-13 |
| E24 | Panel único de alarmas             | 13 | Nueve familias, dueño nominal, plazos, escalamiento, resolución con motivo   | RN-167 a RN-173          |
| E25 | Analítica, indicadores y encuestas | 21 | Eventos de decisión, seis indicadores, Wilson, encuesta adaptativa           | RN-159 a RN-166          |

## R4 · Catálogo ampliado — 97 SP

| ID  | Épica                               | SP | Contenido                                                                            | Traza                 |
| --- | ----------------------------------- | -- | ------------------------------------------------------------------------------------ | --------------------- |
| E26 | Categorías P-B y P-D                | 21 | Bien usado con peritaje, servicio con puesta a disposición irrevocable               | RN-15 a RN-19         |
| E27 | **Bienes registrables P-C1 y P-C2** | 55 | Siete etapas, instrumento notarial, bloqueo registral, reconsulta, transferencia     | RN-25 a RN-38         |
| E28 | Tipos T2, T4, T5, T6, T7 y T8       | 21 | Umbral, hitos, ventana corta, multi-ganador sin reemplazo, recurrencia, modo en vivo | RN-11-bis a RN-14-ter |

## R5 · Plataforma y regímenes — 136 SP

| ID  | Épica                                    | SP | Contenido                                                                                                                      | Traza                                     |
| --- | ---------------------------------------- | -- | ------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------- |
| E33 | Control de funciones y ventanas          | 29 | Capacidades en tres capas, escalada de apagado, regla de vuelo, ventanas operativas, registro de conmutación                   | INV-45 · RN-06-sexies a duodecies         |
| E34 | Panel de funciones y cuentas internas    | 34 | Panel por subrol, alta con verificación y multifactor, subroles con vigencia, auditoría de consulta                            | RN-06-terdecies a quindecies · RN-203-bis |
| E35 | Regímenes sin recaudación                | 39 | Régimen económico, entrada gratuita con cupo atómico, garantía sustitutiva, prohibición de registrables, verificación diferida | INV-06-b · INV-42 · INV-44                |
| E36 | Régimen promocional                      | 21 | Sin liquidación, cadena de conformidad, plan por adelantado con cupo propio                                                    | INV-43 · RN-14-decies a duodecies         |
| E37 | Rango de recaudación y parte relacionada | 13 | Cuatro zonas con alerta acumulable, trato idéntico con marca de auditoría                                                      | INV-39 a INV-41                           |

## R6 · Crecimiento y lanzamiento — 125 SP

| ID  | Épica                        | SP | Contenido                                                                                      | Traza                                            |
| --- | ---------------------------- | -- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| E29 | Growth y comercial           | 27 | Atribución, referidos por registro, promociones como crédito, destaque etiquetado, captación   | RN-185 a RN-193                                  |
| E30 | Multi-mercado y suspensión   | 13 | Segundo mercado en configuración, cuatro niveles de kill switch                                | RN-182 a RN-184 · INV-30 a INV-33                |
| E31 | Rendimiento y endurecimiento | 21 | Presupuesto en red móvil, matriz de compatibilidad, carga, seguridad                           | RN-209 a RN-218                                  |
| E32 | Ensayo real y lanzamiento    | 8  | Ciclo con dinero real, runbooks, guardia, comunicación                                         | RN-208                                           |
| E38 | Descubrimiento y atribución  | 24 | Directorio y perfil público de organizador, código de organizador, marca compartida            | PU-11 · PU-12 · RN-194-ter a sexies              |
| E39 | LIBOX Club                   | 31 | Suscripción con prorrateo, aliados y beneficios, ingreso diferido, criterio doble de encendido | INV-46 · RN-194-septies a undecies · T-15 a T-18 |

# 4\. Camino crítico y riesgos

## 4.1 Camino crítico

| Hilo                               | Duración                          | Bloquea                                                                             |
| ---------------------------------- | --------------------------------- | ----------------------------------------------------------------------------------- |
| **Dictámenes legales L-01 a L-12** | 2–4 meses, externo                | L-01 bloquea el lanzamiento. L-02 a L-04 y L-08 a L-11 bloquean el encendido de P-C |
| **Diseño de las 60 superficies**   | 4–6 semanas, en paralelo desde R0 | E10, E16, E19                                                                       |
| **Contratación de proveedores**    | 4–8 semanas                       | E12 identidad y pagos                                                               |
| **Plantilla notarial única**       | Con el estudio legal              | E27                                                                                 |

**Con 30 sprints, los dictámenes dejan de ser camino crítico.** En el plan de 14 semanas lo eran; aquí P-C se construye con los dictámenes en mano en lugar de contra ellos. Es la ventaja no obvia de la opción 2.

## 4.2 Riesgos

| \#    | Riesgo                                                             | Mitigación                                                                      |
| ----- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| RG-01 | **Once meses sin usuario real.** Mucho tiempo sin señal de mercado | Encendido progresivo desde el mes 11; captación de organizadores ancla desde R3 |
| RG-02 | **El equipo pasa de construir a operar sin relevo**                | Encendido acotado y contratación de operación antes del mes 12                  |
| RG-03 | Dictamen legal adverso sobre la figura jurídica                    | L-01 se encarga en la semana 1. Es la pregunta que decide si la empresa existe  |
| RG-04 | Exceso de confianza en la asistencia de IA en zonas críticas       | §1.3 con propiedad fija y revisión obligatoria                                  |
| RG-05 | La comisión del 20 % no se valida hasta el mes 11                  | Validar con organizadores reales desde R3, sin producto terminado               |
| RG-06 | Rotación en un equipo de 4                                         | Documentación viva; propiedad fija solo en las 5 zonas críticas                 |
| RG-07 | Deriva de alcance por asistencia de IA barata                      | BR-02: sin criterio comprobable no entra al sprint                              |

## 4.4 Congelamiento de alcance

**El alcance creció un 26 % entre V2 y V3**, de 745 a 936 SP, y cada ampliación estuvo justificada. Ninguna fue capricho.

**Ese es precisamente el problema.** Un proceso de revisión que encuentra huecos legítimos en cada pasada no se detiene solo, porque siempre habrá una pregunta más que descubra algo cierto. **La calidad de los hallazgos es lo que hace difícil parar.**

> **La línea base queda congelada con este backlog.**

Todo hallazgo posterior entra en **backlog de cambio** y se emite en una versión futura, con el sistema ya en construcción. Es el mecanismo que VIES ya tenía en su gobernanza de marca, elevado a corpus.

**Único criterio para romper el congelamiento:** un hallazgo que impida construir, o que exponga a un riesgo legal o patrimonial. Todo lo demás espera.

## 4.3 Lo que no está en estos 936 SP

Diseño de las 60 superficies · dictámenes legales y notariales · contratación e integración comercial de proveedores · L1 Product Strategy y la estrategia de captación · operación una vez lanzado.

*LIBOX Backlog MVP V3. Deriva de PRD MVP V9, Especificación Técnica L3 V7 y Design System L4 V2. El detalle de historias con criterios de aceptación está en* `LIBOX_BACKLOG_MVP_V3.xlsx`*.*
