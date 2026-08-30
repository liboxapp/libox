# Índice de contenidos

# LIBOX Behavioral Product Framework — LBPF V3

### Nivel L0 · Filosofía de Producto y Gobernanza Conductual

**Documento:** LIBOX\_BEHAVIORAL\_PRODUCT\_FRAMEWORK\_LBPF\_V3 **Versión:** V3 **Nivel:** L0 — Rector **Fecha de emisión:** 2026-08-07 **Reemplaza:** LBPF V2 (deprecado en su totalidad) **Consumido por:** Product Strategy L1 · PRD MVP y Enterprise L2 · Especificación Técnica L3 · Design System L4 · VIES **Estado:** vigente

# Changelog

## Cambios de la versión V3

Esta versión se emite tras una auditoría global de coherencia que detectó cuatro conflictos entre decisiones nuevas y invariantes vigentes. Tres de las resoluciones son materia del rector.

| Versión | Sección         | Qué cambió                                                                                                                                                                        | Por qué                                                                                                                                                                                                                     | Decisión que invalida            |
| ------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| V3      | §13.1           | **Regla de parte relacionada.** Una entidad vinculada a LIBOX puede organizar oportunidades **como cliente**, con las tarifas publicadas, los mismos gates y sin trato preferente | LIBOX necesita organizar sorteos promocionales propios. Hacerlo directamente vulneraría INV-02 e INV-04. La estructura de entidad separada preserva la neutralidad **literalmente**, en lugar de abrir una excepción a ella | Ninguna; evita derogar §13       |
| V3      | §13.2           | **La suscripción no otorga participaciones ni mejora probabilidad.** Cruzar esa línea exige BDR de clase B4 con revisión legal previa                                             | Sin esta regla, un plan de beneficios deriva en venta de participaciones y la posición estructural de §13 deja de ser cierta                                                                                                | Amplía                           |
| V3      | **P13 nuevo**   | **Igualdad de probabilidad entre vía gratuita y vía pagada.** Quien participa sin pagar tiene exactamente las mismas probabilidades que quien paga                                | Doble fundamento: es la condición que sostiene el mecanismo de entrada gratuita, **y** premiar el gasto con más probabilidad es el bucle de fidelización que R-08 prohíbe                                                   | Amplía el catálogo de principios |
| V3      | **BR-09 nuevo** | **Derecho a la proporción razonable.** La recaudación de una oportunidad guarda relación acotada con el valor del premio                                                          | Sin suelo, el reembolso no está financiado. Sin techo, el participante recibe una fracción del valor esperado sin saberlo                                                                                                   | Amplía el catálogo de derechos   |
| V3      | §0.1 R-10       | **Precisión de alcance.** R-10 protege a los **participantes**. El historial del **organizador** es público y deliberadamente visible                                             | Sin la precisión, el perfil público del organizador se leería como incumplimiento de R-10                                                                                                                                   | Precisa R-10                     |
| V3      | §12.2           | Los beneficios de suscripción **nunca son descuento sobre el precio del ticket**                                                                                                  | Un ticket a distinto precio rompe la uniformidad de precio y ensucia la integridad del pool                                                                                                                                 | Amplía                           |
| V3      | §6.2.1          | La **recaudación del organizador no es información pública**                                                                                                                      | Es su información comercial, como el margen de cualquier comercio. Lo esencial para decidir —precio, probabilidad, pool y valor verificado— sí es público                                                                   | Amplía                           |

## Cambios de la versión V2

| Versión | Fecha      | Sección    | Qué cambió                                                                                          | Por qué                                                                                               | Decisión que invalida                                                   |
| ------- | ---------- | ---------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| V2      | 2026-08-06 | §0.1       | Se añaden **R-09** (adaptabilidad regulatoria) y **R-10** (confidencialidad de participación)       | El modelo pasa a multi-mercado y se define el alcance exacto de la transparencia                      | Ninguna; amplía                                                         |
| V2      | 2026-08-06 | §0.3       | Se añade **excepción de reserva en materia PLAFT**                                                  | Prohibición de tipping-off: única materia donde no puede haber transparencia hacia el usuario         | Deroga la lectura de transparencia absoluta de R-05 en ese ámbito       |
| V2      | 2026-08-06 | LBPF-001.2 | Se añade **BR-08 Integridad del Proceso**                                                           | La ruta de resolución y los plazos deben conocerse antes de comprometerse                             | Ninguna; amplía                                                         |
| V2      | 2026-08-06 | LBPF-005   | Nueva **§5.4 Custodia y garantía patrimonial**                                                      | El escrow deja de ser mecanismo operativo y pasa a ser garantía conductual declarada                  | Ninguna; amplía                                                         |
| V2      | 2026-08-06 | LBPF-005   | Nueva **§5.5 Verificación de valor y unicidad de identidad**                                        | La evidencia del premio y la unicidad del participante son condición de confianza, no detalle técnico | Ninguna; amplía                                                         |
| V2      | 2026-08-06 | LBPF-006.2 | Se precisa qué es público en la tarjeta: **pool y vendidos sí; identidad y concentración no**       | La concentración no altera la probabilidad de nadie; la identidad es dato personal                    | Deroga la lectura de v1.0 que podía exigir divulgación de participación |
| V2      | 2026-08-06 | LBPF-007   | De 12 KPI declarados a **6 activos con método de cálculo**; el resto diferido o convertido en regla | En v1.0 ningún KPI era calculable: no existía instrumentación                                         | Deroga los umbrales operativos de P2, P4, P9, P10, P11, P12 en el MVP   |
| V2      | 2026-08-06 | LBPF-009.1 | **LINT-003, LINT-004 y LINT-005 bloquean el merge.** El resto advierte                              | Un guardarraíl que no se hace cumplir no es un guardarraíl                                            | Deroga la configuración no bloqueante                                   |
| V2      | 2026-08-06 | LBPF-010.4 | Degradación en MVP redefinida sobre alcance real                                                    | v1.0 declaraba degradaciones sin decir qué sustituía al control                                       | Reemplaza §10.4 v1.0                                                    |
| V2      | 2026-08-06 | LBPF-010.7 | Nuevo **Panel Único de Alarmas** con dueño nominal y SLA                                            | La supervisión pasó de pública a interna; requiere mecanismo real                                     | Ninguna; amplía                                                         |
| V2      | 2026-08-06 | —          | Nueva norma **LBPF-011 Adaptabilidad Regulatoria Multi-Mercado**                                    | El producto nace multi-mercado                                                                        | Ninguna; amplía                                                         |
| V2      | 2026-08-06 | —          | Nueva norma **LBPF-012 Ética Comercial y de Crecimiento**                                           | Marketing y comercial son externos al producto, pero el sistema debe imponerles límites               | Ninguna; amplía                                                         |
| V2      | 2026-08-06 | §11        | Se declara **neutralidad económica de LIBOX frente al azar**                                        | Posición estructural que define la naturaleza del negocio                                             | Ninguna; amplía                                                         |

# 0\. Control documental, alcance y prevalencia

El LBPF es el nivel **L0** de la arquitectura documental de LIBOX. Define principios, derechos, límites y reglas de decisión que prevalecen sobre los documentos de construcción cuando exista tensión entre conversión, experiencia, riesgo y autonomía del usuario. El LBPF no reemplaza al PRD: lo condiciona. El PRD especifica qué construir y cómo debe comportarse el sistema; el LBPF determina por qué una experiencia es admisible y cuáles son los límites conductuales que no pueden vulnerarse.

## 0.1 Reglas rectoras R-01 a R-10

| Regla    | Nombre                                | Mandato                                                                                                                                                                                                                                                                         |
| -------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **R-01** | Supremacía L0                         | Toda decisión de producto, UX, UI, copy, recomendación, pricing, notificación o experimentación debe ser compatible con este framework.                                                                                                                                         |
| **R-02** | Consumo, no duplicación               | Los PRD MVP y Enterprise consumen el LBPF mediante referencias normativas; no copian extensamente su contenido.                                                                                                                                                                 |
| **R-03** | Prevalencia del usuario               | Ante conflicto entre conversión marginal y comprensión, reversibilidad o evidencia, prevalece el derecho conductual del usuario.                                                                                                                                                |
| **R-04** | Neutralidad probabilística            | Ninguna interfaz puede sugerir que una acción del usuario modifica la probabilidad objetiva cuando no existe tal causalidad.                                                                                                                                                    |
| **R-05** | Evidencia antes de persuasión         | La persuasión comercial solo es válida cuando no precede ni desplaza información esencial sobre costo, probabilidad, reglas y riesgo.                                                                                                                                           |
| **R-06** | Trazabilidad                          | Toda excepción, experimento o mutación B2-B4 debe registrar BDR, `trace_id` y evento auditable.                                                                                                                                                                                 |
| **R-07** | Compatibilidad MVP-Enterprise         | Los controles pueden degradarse operativamente en MVP, pero no pueden desaparecer semánticamente ni impedir su endurecimiento futuro.                                                                                                                                           |
| **R-08** | Prohibición de vulnerabilidad         | Prohibido segmentar o personalizar para explotar vulnerabilidad financiera, cognitiva, emocional, etaria o situacional.                                                                                                                                                         |
| **R-09** | **Adaptabilidad regulatoria**         | Ninguna regla de jurisdicción vive en el código. Toda norma que una autoridad pueda modificar es configuración versionada por mercado. Adaptarse a un cambio regulatorio es una operación de configuración, no un despliegue de software.                                       |
| **R-10** | **Confidencialidad de participación** | La identidad de quienes participan y la distribución de tenencia de tickets no son información pública. Sí lo son, obligatoriamente, el tamaño del pool y los tickets vendidos. **Protege al participante, no al organizador**: el historial del organizador es público (§0.4). |

### Fundamento de R-10

La concentración de tickets **no altera la probabilidad objetiva de ningún participante**. Quien compra 1 ticket de 1.000 tiene 0,1 % de probabilidad, tenga otro usuario 5 tickets o 300: el denominador es idéntico. Por tanto, no divulgarla no vulnera BR-01 ni P3.

Lo que sí es información esencial —y por tanto obligatoria— es **el denominador**: tickets vendidos y total del pool. Ocultarlo haría incalculable la probabilidad y sería una infracción directa de BR-01, BR-05, P3 y P4.

La confidencialidad de la identidad responde a protección de datos personales y a un riesgo operativo concreto: un participante identificado como gran tenedor se convierte en blanco de ingeniería social y de contacto fuera de plataforma.

### Alcance de R-10 — a quién protege

R-10 protege a **quien participa**, no a quien organiza. La distinción es deliberada y las razones son opuestas:

| Sujeto                          | Tratamiento                                                      | Fundamento                                                                                        |
| ------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Participante**                | Identidad y tenencia **no públicas**                             | Es dato personal, y un gran tenedor identificado se vuelve blanco de contacto fuera de plataforma |
| **Organizador**                 | Historial de oportunidades, entregas y controversias **público** | Quien pide dinero al público responde ante él. **Su historial es la garantía que ofrece**         |
| **Recaudación del organizador** | **No pública**                                                   | Información comercial propia, como el margen de cualquier comercio. No es condición de la compra  |

**Fundamento de la asimetría.** El participante no le pide nada a nadie: entrega dinero y necesita protección. El organizador pide dinero al público, y **la exposición de su historial es precisamente lo que permite confiar en un desconocido**. Sin ella, un marketplace de organizadores no verificables sería indistinguible de una rifa informal.

**Contrapartida obligatoria.** Al retirar la vigilancia pública, la detección de anomalías pasa íntegramente a control interno. R-10 solo es admisible si existe y opera el **Panel Único de Alarmas** de §10.7, con dueño nominal y SLA. Si ese panel no funciona, R-10 deja de estar justificada.

## 0.2 Pirámide documental L0-L4

| Nivel  | Documento                               | Responsabilidad                                                                                                           |
| ------ | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **L0** | LBPF — Product Philosophy               | Axiomas, derechos, arquitectura de decisión, principios, límites y gobernanza conductual                                  |
| **L1** | Product Strategy                        | Objetivos, segmentos, propuesta de valor, modelo de negocio y prioridades                                                 |
| **L2** | PRD MVP / Enterprise                    | Contrato de construcción: qué existe, qué reglas de negocio lo gobiernan, qué debe cumplir                                |
| **L3** | Architecture, Security, Engineering, QA | Mecanismos de implementación: esquema de datos, contratos de API, máquinas de estado, algoritmos, observabilidad, pruebas |
| **L4** | Design System, UI Kit, Motion, Copy     | Materialización de la experiencia y sus componentes                                                                       |

**Precisión introducida en v2.0.** El límite L2/L3 estaba ambiguo en v1.0 y produjo que el PRD absorbiera contenido de L3 y se degradara a plantilla. La línea es: **L2 declara la existencia y las reglas; L3 especifica la forma.** El PRD declara que existe la tabla `settlements` y cuáles son sus gates de negocio; el `schema.sql` de L3 define sus columnas. Un PRD no contiene DDL: lo referencia.

## 0.3 Excepción única de reserva — materia PLAFT

Existe **una sola** materia en la que LIBOX no puede ser transparente con el usuario sobre lo que ocurre: la prevención de lavado de activos y financiamiento del terrorismo.

Cuando una operación es objeto de análisis por sospecha, **el usuario no es informado de esa circunstancia**. La comunicación es funcional y neutra —*“para continuar necesitamos acreditar el origen de los fondos”*— y nunca revela la existencia de un análisis, una alerta o un reporte.

Esta excepción es deliberada, acotada y de obligado cumplimiento. Es la única derogación admitida de la transparencia que gobierna el resto del framework, y existe porque advertir a quien está siendo analizado frustra el propósito del control y, en jurisdicciones donde LIBOX califique como sujeto obligado, constituye infracción.

**Alcance estricto:** la reserva cubre el análisis y el reporte, **no** el requerimiento de documentación, que sí se comunica con claridad, ni los derechos del usuario sobre sus fondos, que se mantienen intactos.

# Resumen ejecutivo

LIBOX opera en un dominio donde la experiencia comercial y la decisión bajo incertidumbre están íntimamente conectadas. Una interfaz puede facilitar comprensión y confianza o, por el contrario, amplificar sesgos, inducir urgencia artificial y convertir una oportunidad verificable en una experiencia de impulso. El LBPF establece un marco normativo para preservar conversión sostenible sin degradar autonomía.

La versión 2.0 incorpora cinco evoluciones estructurales respecto de v1.0:

**Se cierra la brecha entre norma y medición.** v1.0 declaraba doce KPI con umbrales numéricos y ninguno era calculable, porque no existía instrumentación. v2.0 define seis KPI activos con método explícito, distingue lo que se mide por telemetría de lo que requiere encuesta y de lo que se verifica en integración continua, y establece el criterio estadístico para declarar una ruptura.

**Se cierra la brecha entre norma y cumplimiento.** v1.0 definía reglas de linter con severidad ERROR que en la práctica no bloqueaban nada. v2.0 establece qué reglas bloquean el merge y cuáles advierten, con el criterio explícito: bloquea lo que ya es norma decidida; advierte lo que aún se está calibrando.

**Se precisa el alcance de la transparencia.** v1.0 podía leerse como exigencia de divulgación total. v2.0 distingue lo que es esencial para decidir —costo, probabilidad, pool, reglas, evidencia— de lo que es dato personal de terceros, y declara la única excepción legítima de reserva.

**Se incorpora la garantía patrimonial como principio conductual.** La retención íntegra de la recaudación hasta la entrega verificada deja de ser un mecanismo operativo del PRD y pasa a ser una promesa declarada: ningún participante pierde su aporte en ningún escenario de fallo.

**Se incorpora la dimensión multi-mercado.** El producto nace preparado para operar bajo marcos regulatorios distintos, con la exigencia de que adaptarse sea configuración y no reescritura.

# LBPF-001 — Purpose & Behavioral Rights

## 1.1 Propósito estratégico y ético

LIBOX existe para transformar oportunidades de alto valor en experiencias accesibles, verificables y comprensibles. El objetivo del producto no es maximizar clics aislados, sino crear un ciclo de confianza en el que el usuario pueda descubrir, evaluar, decidir, pagar, verificar resultados, reclamar y disputar sin ambigüedad ni coerción.

El propósito comercial se expresa como **conversión informada**: una participación es válida cuando el usuario comprende la oportunidad, conoce el costo y la probabilidad, dispone de evidencia relevante y conserva control razonable sobre la decisión. La conversión obtenida mediante confusión, urgencia falsa, estimulación de casi-acierto u ocultamiento de costos no se reconoce como creación de valor.

## 1.2 Los ocho Derechos Conductuales

| Derecho                              | Norma                                                                                                                                                                                                                                                    | KPI mínimo                                                                                    |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **BR-01** Comprensión                | Derecho a entender costo, probabilidad, reglas, estado y consecuencia antes del compromiso                                                                                                                                                               | Decision Comprehension Rate ≥ 85 % en flujos financieros críticos                             |
| **BR-02** Reversibilidad             | Poder corregir información, abandonar o volver atrás antes del commit irreversible                                                                                                                                                                       | 100 % de corrección pre-commit; retorno ≤ 1 interacción en checkout                           |
| **BR-03** Control                    | Controlar preferencias, notificaciones, consentimiento, recomendaciones y **límites de gasto propios**                                                                                                                                                   | Opt-out en ≤ 2 pasos, sin degradación punitiva del servicio                                   |
| **BR-04** Dignidad                   | La interfaz no ridiculiza, presiona, infantiliza ni culpa por rechazar una oferta                                                                                                                                                                        | 0 confirmshaming y 0 copy coercitivo en producción                                            |
| **BR-05** Evidencia                  | Toda afirmación esencial debe ser sustentable por datos, reglas o prueba verificable                                                                                                                                                                     | Evidence Accessibility ≥ 95 % en oportunidades activas                                        |
| **BR-06** Descanso                   | El sistema respeta períodos sin estímulo y limita frecuencia de contacto                                                                                                                                                                                 | Quiet hours, frequency caps y opt-out persistente                                             |
| **BR-07** Equidad                    | No se explota vulnerabilidad ni se discrimina mediante personalización opaca                                                                                                                                                                             | 0 targeting por vulnerabilidad; auditoría de fairness por segmento                            |
| **BR-08** **Integridad del Proceso** | Derecho a conocer, **antes de comprometerse**, cómo se resolverá la oportunidad en todos sus desenlaces: plazos de reclamo y entrega, ruta ante premio no reclamado, costos de envío o transferencia, y qué ocurre con su dinero si el sorteo se cancela | 100 % de sorteos con ruta de resolución, plazos y costos publicados antes de la primera venta |
| **BR-09** **Proporción Razonable**   | Derecho a que la recaudación total de una oportunidad guarde una relación acotada con el valor verificado del premio. Ninguna oportunidad se publica fuera del rango declarado por el mercado                                                            | 100 % de oportunidades dentro del rango; 0 excepciones sin doble firma registrada             |

**Fundamento de BR-08.** Un participante que compra sin saber qué ocurre si el ganador no aparece, cuánto costará recibir el premio, o cuánto puede tardar la resolución, está tomando una decisión incompleta aunque conozca costo y probabilidad. Los desenlaces son parte de la oportunidad, no letra pequeña.

**Fundamento de BR-09.** La relación entre lo recaudado y el valor del premio es técnicamente calculable por cualquiera —precio por total de tickets, dividido entre el valor verificado— y en la práctica **nadie hace esa cuenta al comprar**. Este framework existe porque reconoce esa distancia entre lo disponible y lo efectivamente usado: es la misma razón por la que DP-03 exige emparejar costo y probabilidad en lugar de confiar en que el participante los relacione por su cuenta.

**BR-09 se protege por rango, no por divulgación.** La recaudación es información comercial del organizador y no es condición de la compra; lo que sí es condición es que exista un límite y que se cumpla.

**El suelo protege el reembolso.** Si lo recaudado no cubre lo que habría que devolver, la garantía patrimonial de §5.4 deja de ser cierta. **El techo protege al participante**, que por encima de cierto múltiplo recibe una fracción del valor esperado sin haberlo advertido.

**Los umbrales concretos son parámetro de mercado y se calibran con datos.** El principio no lo es.

> **CRITERIO DE RECHAZO.** Una experiencia que alcance objetivos de conversión pero vulnere cualquiera de los ocho derechos debe rechazarse, corregirse o degradarse hasta recuperar cumplimiento.

## 1.3 Obligaciones de equipos

**Product** documenta la intención conductual de cada cambio B2-B4. **Design** demuestra comprensión, jerarquía informativa y ausencia de coerción, **y diseña tolerante a longitud de texto variable** (LBPF-011.3). **Engineering** conserva telemetría y trazabilidad suficientes para auditar la experiencia. **Risk & Compliance** define límites de personalización y señales de vulnerabilidad no explotables. **QA** valida criterios Given/When/Then conductuales además de funcionales. **Marketing y Comercial** respetan las mismas reglas de probabilidad, costo, urgencia y evidencia que la interfaz transaccional. Su estrategia es externa al producto; sus límites, no (LBPF-012).

# LBPF-002 — Prospect Economy & Opportunity Value

*Sin cambios normativos respecto de v1.0.* Se mantienen la definición de Prospect Economy, la función de valor y ponderación, la ecuación Opportunity Value, el Cognitive Step Count y las reglas de ejecución asíncrona y uso interno.

**Precisión operativa añadida en v2.0:** el Cognitive Step Count se mide sobre la experiencia real en el dispositivo de menor capacidad soportado, no sobre el diseño de escritorio. Un flujo de 3 pasos en escritorio que se convierte en 7 en móvil incumple igual.

# LBPF-003 — Decision Architecture & Progressive Disclosure

*Sin cambios normativos.* Se mantienen los tipos de fricción, la clasificación de decisiones, la divulgación progresiva y los defaults conservadores.

**Precisión añadida en v2.0 sobre §3.4 Defaults conservadores.** El principio de default conservador se extiende explícitamente a los límites de gasto autoimpuestos, con una **asimetría obligatoria**: reducir un límite aplica de inmediato; aumentarlo requiere un período de espera de 24 horas.

Sin esa asimetría, la herramienta se desactiva precisamente en el momento en que sería útil, y su existencia se vuelve decorativa. La asimetría no es una restricción al usuario: es lo que hace que su decisión previa, tomada en frío, tenga peso sobre su decisión posterior, tomada en caliente.

# LBPF-004 — Behavioral Economics Standard

*Sin cambios normativos.* Se mantienen los sesgos catalogados, sus contramedidas y los controles de precio cero.

**Extensión en v2.0 — asignación de identificadores.** El identificador de ticket es asignado por el sistema de forma automática y correlativa al confirmarse el pago. **No existe selección manual.**

Fundamento: elegir un número no modifica la probabilidad objetiva, y permitir la elección activa una ilusión de control que el usuario no puede desactivar por sí mismo. Suprimir el mecanismo es preferible a permitirlo y luego advertir contra él, porque la advertencia rara vez compensa el sesgo que la interfaz acaba de inducir. Esta decisión hace innecesario el principio P10 en el alcance actual y refuerza R-04 estructuralmente en lugar de hacerlo por copy.

Corolario: **el sorteo se realiza siempre sobre los tickets vendidos válidos, nunca sobre el rango completo de numeración.** Un desenlace sin ganador por haber sorteado sobre números no vendidos sería una promesa incumplida hacia todos los participantes.

# LBPF-005 — Trust Architecture & Proof Systems

Se mantienen la pirámide de evidencia de ocho capas, las reglas de prueba social auténtica y el Proof of Value. Se añaden dos secciones.

## 5.4 Custodia y garantía patrimonial

LIBOX retiene la totalidad de la recaudación de un sorteo desde la venta hasta la verificación de la entrega. Dado que el dimensionamiento del sorteo parte del valor del premio, **la suma retenida excede estructuralmente ese valor**.

De ahí se deriva una promesa que el framework declara como norma, no como práctica operativa:

> **Ningún participante pierde su aporte en ningún escenario de fallo.** Si el sorteo se cancela por cualquier causa —premio inexistente, incumplimiento del organizador, gravamen sobrevenido, imposibilidad de transferencia—, el reembolso íntegro está financiado por la recaudación retenida.

Esta promesa debe estar redactada en lenguaje llano en las bases de todo sorteo y es de cumplimiento incondicional. **Ninguna suspensión operativa, decisión de riesgo, análisis de cumplimiento o cierre de mercado puede impedir que una persona reclame su premio, reciba su reembolso o disponga de su saldo.** Suspender la operación jamás puede convertirse en retener dinero de terceros.

**Límite explícito de la garantía.** La custodia protege contra el incumplimiento; **no protege contra la sobrevaloración del premio**. Un premio cuyo valor fue inflado puede entregarse íntegramente y el escrow no detectará nada. Contra la sobrevaloración solo protege el control de §5.5. Son dos riesgos distintos con dos controles distintos, y ninguno sustituye al otro.

## 5.5 Verificación de valor e identidad única

**Verificación de valor.** Ninguna oportunidad se publica sin que el valor declarado del premio haya sido verificado documentalmente y contrastado contra referencias de mercado. Esta verificación es **obligatoria en todos los casos, sin excepción por reputación, antigüedad ni volumen del organizador**.

Fundamento conductual: el valor del premio es la variable sobre la que el usuario evalúa si la oportunidad merece su dinero. Un valor no verificado convierte toda la información de la tarjeta —costo, probabilidad, evidencia— en una comparación contra una cifra inventada. **La verificación de valor es la condición de posibilidad del resto del framework.**

**Neutralidad del verificador.** Ningún rol con capacidad de aprobar el valor de un premio puede tener métricas de desempeño ligadas al volumen de oportunidades aprobadas. Toda excepción a los umbrales exige segunda firma de persona distinta, con motivo registrado.

Fundamento: LIBOX percibe una comisión proporcional a la recaudación, y la recaudación se dimensiona sobre el valor del premio. Existe por tanto un **incentivo estructural a aprobar valores altos**. El framework lo neutraliza por diseño organizativo, no por confianza en la buena voluntad.

**Identidad única.** Una persona, una cuenta. La unicidad se garantiza sobre documento de identidad, correo y teléfono, y se ata a la persona mediante verificación con prueba de vida. La unicidad no es un control antifraude accesorio: es la condición para que los límites de concentración, los topes de gasto, la autoexclusión y la protección de menores signifiquen algo. Sin unicidad, **todos los controles del framework son evadibles creando otra cuenta**.

# LBPF-006 — Opportunity Architecture & Motion Calm Standard

## 6.1 Teoría de Fronteras de Interacción

Se mantiene íntegra. Dos zonas:

**Zona de Atracción** — descubrimiento, catálogo, rankings, comunicación editorial. Admite riqueza visual, imágenes aspiracionales, profundidad y microinteracciones.

**Zona de Decisión** — detalle de oportunidad, checkout, resultado, evidencia, reclamo, disputa. Exige calma, neutralidad y ausencia de estímulo persuasivo.

**Regla de determinación (precisada en v2.0):** el límite lo define la **intención de la superficie, no su ubicación**. Cualquier superficie que contenga un llamado a la acción de compra o que muestre un resultado es Zona de Decisión, aunque esté en la página de inicio. Un hero con botón de compra es zona de decisión.

**Regla de Prevalencia Visual.** Si un componente del Design System contradice Motion Calm en una Zona de Decisión, prevalece LBPF-006 y el componente debe corregirse, deshabilitarse o limitarse a la Zona de Atracción.

## 6.2 Verified Opportunity Card — anatomía

Seis zonas obligatorias:

| Zona               | Contenido                                                                                                                                                                         |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A · Encabezado** | Premio, categoría, organizador y sello de verificación. Sin claim absoluto                                                                                                        |
| **B · Valor**      | Precio total del ticket **y valor verificado del premio con fuente y fecha**                                                                                                      |
| **C · Decisión**   | **Probabilidad objetiva y tamaño del pool.** Formato triple: “1 de 1.000 · 0,10 % · 1 por cada 1.000 tickets”                                                                     |
| **D · Reglas**     | Cierre, tipo de sorteo, elegibilidad, **plazo de reclamo, plazo de entrega, ruta ante no reclamo, costo estimado de envío o transferencia** (BR-08). Accesible en ≤ 1 interacción |
| **E · Evidencia**  | Política de prueba e historial auténtico. No decorativa                                                                                                                           |
| **F · Acción**     | CTA descriptivo y no coercitivo. “Revisar y participar”, nunca “¡Gana ya\!”                                                                                                       |

### 6.2.1 Alcance de la divulgación — precisión de v2.0

| Dato                                             | Divulgación                                                   | Fundamento                                                                     |
| ------------------------------------------------ | ------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Tickets vendidos y total del pool                | **Obligatoria**                                               | Es el denominador de la probabilidad. Ocultarlo infringe BR-01, BR-05, P3 y P4 |
| Probabilidad objetiva                            | **Obligatoria**                                               | P3, DP-03                                                                      |
| Valor verificado del premio con fuente y fecha   | **Obligatoria**                                               | §5.5                                                                           |
| Plazos, ruta de resolución y costos de recepción | **Obligatoria**                                               | BR-08                                                                          |
| Identidad de los participantes                   | **Prohibida**                                                 | R-10                                                                           |
| Distribución de tenencia de tickets              | **Prohibida**                                                 | R-10                                                                           |
| **Recaudación del organizador**                  | **Prohibida**                                                 | Información comercial propia. No es condición de la compra (§0.1 R-10)         |
| **Historial del organizador**                    | **Obligatoria**                                               | Es la garantía que ofrece quien pide dinero al público                         |
| Identidad del ganador                            | **Solo con consentimiento** explícito, específico y revocable | R-10, DP-13                                                                    |

### 6.2.2 Límite de concentración

Ningún participante puede adquirir más del **30 %** de los tickets de un sorteo. El límite se declara en los Términos y Condiciones y se hace cumplir en el sistema.

Fundamento doble. **Conductual:** una oportunidad donde una sola persona posee la mayoría del pool deja de ser una oportunidad abierta, aunque la probabilidad de cada quien siga siendo aritméticamente correcta. **De integridad:** adquirir la totalidad o casi totalidad del pool cuesta más que el premio, de modo que quien lo intenta persigue algo distinto del premio, y ese algo distinto es precisamente lo que el marco de prevención debe detectar.

El umbral concreto es parámetro por mercado; el principio no lo es.

## 6.3 Veto anti-impulso

Prohibido en Zona de Decisión, sin excepción: explosiones de partículas, brillos en bucle continuo, confeti, luces de premio mayor, **regalos tridimensionales flotantes**, sonidos de premio, animación de casi-acierto, contadores de demanda simulados, pulsos de CTA de alta frecuencia, y cualquier movimiento cuya función principal sea acelerar emocionalmente la compra.

## 6.4 Motion Calm

| Perfil               | Hover  | Estado | Pantalla | Bucle                                                          |
| -------------------- | ------ | ------ | -------- | -------------------------------------------------------------- |
| Atracción            | 160 ms | 220 ms | 240 ms   | Permitido si es pausable y no representa evidencia inexistente |
| **Calma** (decisión) | 120 ms | 160 ms | 180 ms   | **Prohibido**                                                  |

**Revelación del resultado:** máximo 800 ms totales, secuencia neutral, sin casi-acierto, sin confeti, sin repetición. La prueba verificable debe ser accesible en el mismo cuadro.

**Límites duros en Zona de Decisión:** ninguna animación supera 240 ms; ninguna animación es infinita. Ambos se verifican en integración continua y **bloquean el merge** (LINT-003, LINT-004).

Toda animación no funcional se detiene ante `prefers-reduced-motion`.

# LBPF-007 — Principios Conductuales y Medición

## 7.1 Los doce principios

Los doce principios de v1.0 se mantienen como norma. Lo que cambia en v2.0 es su régimen de medición, porque en v1.0 **ninguno era calculable**: se declararon umbrales sin instrumentación que los alimentara.

| Principio                               | Régimen v2.0                                                                                                               |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **P1** Confianza antes que conversión   | **KPI activo** — telemetría                                                                                                |
| **P2** Oportunidad antes que excitación | Métrica calibrable — advierte, no bloquea                                                                                  |
| **P3** Probabilidad objetiva            | **KPI activo** — encuesta                                                                                                  |
| **P4** Encuadre simétrico               | Métrica calibrable — advierte, no bloquea                                                                                  |
| **P5** Evidencia a la mano              | **KPI activo** — telemetría                                                                                                |
| **P6** Fricción protectora              | **KPI activo** — telemetría (error) y encuesta (arrepentimiento)                                                           |
| **P7** Defaults conservadores           | **KPI activo** — verificación estática, umbral cero, **bloquea merge**                                                     |
| **P8** Calma en momentos críticos       | **KPI activo** — verificación estática, umbral cero, **bloquea merge**                                                     |
| **P9** Reversibilidad antes del commit  | **Invariante de diseño**, no métrica. Umbral 100 % → ítem de checklist obligatorio                                         |
| **P10** Control neutral                 | **Neutralizado estructuralmente** por asignación automática (LBPF-004). Se reactiva solo si se implementa selección manual |
| **P11** Persuasión silenciosa           | Diferido — se activa cuando el volumen de comunicación lo justifique                                                       |
| **P12** Personalización explicable      | **Convertido en regla binaria** (LINT-006). El porcentaje se difiere                                                       |
| **P13** Igualdad de vía                 | **KPI activo** — verificación estática, umbral cero, **bloquea merge**                                                     |

### P13 · Igualdad de vía

> **Cuando una oportunidad admite participación gratuita y participación pagada, ambas tienen exactamente la misma probabilidad de resultar ganadoras.**

Prohibido sin excepción: que comprar otorgue participaciones adicionales en un sorteo con entrada gratuita · que el gasto acumulado mejore las opciones en cualquier sorteo · que la vía gratuita se presente con menor prominencia que la pagada · que la vía gratuita tenga cupo, plazo o requisitos más restrictivos dentro de la misma oportunidad.

**Doble fundamento, y los dos son decisivos.**

El primero es **estructural**: la igualdad de probabilidad es la condición que sostiene la existencia misma de una vía gratuita. En cuanto pagar mejora las opciones, el pago vuelve a comprar azar y el mecanismo deja de ser lo que dice ser.

El segundo es **conductual y propio de este framework**: premiar el gasto con más probabilidad de ganar es exactamente el bucle que R-08 prohíbe. Convierte gastar en sentirse recompensado, y es la mecánica que separa un producto de participación de un producto de dependencia.

**Umbral cero.** Se verifica de forma estática y bloquea la integración, como P7 y P8. No es una métrica a observar: es una condición a cumplir.

**Criterio de la reducción.** Un principio no medido no es un principio relajado: sigue siendo norma y sigue siendo auditable. Lo que se difiere es su seguimiento cuantitativo continuo. Medir doce indicadores con volumen insuficiente produce ruido que erosiona la credibilidad del sistema de gobernanza, y un sistema de gobernanza al que el equipo aprende a ignorar es peor que no tenerlo.

## 7.2 Las tres capas de medición

**Capa 1 — Verificación estática en integración continua.** P7 y P8. Se calculan sobre el código, no sobre usuarios. Son normas de umbral cero ya decididas en este framework, no hipótesis a validar. **Bloquean el merge**, no el lanzamiento: el defecto se detiene antes de existir en ningún entorno.

**Capa 2 — Telemetría de producto.** P1, P5, P6 (error). Requieren el esquema de eventos de decisión.

**Capa 3 — Encuesta muestral.** P3, P6 (arrepentimiento). Miden lo que la persona **cree o siente**, no lo que hace. Ningún evento de interacción mide una creencia. Sin instrumento de encuesta, estos indicadores no existen.

## 7.3 Método de medición

**Instrumento de encuesta.** De cinco a siete preguntas breves, de las que se muestran una o dos por sesión, **nunca durante el checkout** — situarla ahí la convertiría en fricción en Zona de Decisión, que es lo contrario de su propósito.

**Muestreo adaptativo.** La tasa se ajusta al volumen con objetivo de aproximadamente 150 respuestas mensuales por instrumento: al inicio se consulta a la totalidad de las compras y la tasa decrece conforme crece el volumen. Una tasa fija baja produce muestras inservibles en las etapas tempranas.

**Criterio estadístico de ruptura.** Un KPI se declara en ruptura solo cuando concurren tres condiciones:

1.  **n ≥ 100** respuestas o eventos válidos en la ventana. Por debajo, el indicador se reporta como “sin datos suficientes”, nunca como incumplido.
2.  **Intervalo de confianza de Wilson al 95 %** con el límite superior por debajo del umbral. No se usa la proporción cruda: una proporción puntual puede caer bajo el umbral por azar.
3.  **Dos ventanas consecutivas** de 30 días en incumplimiento.

Este criterio existe para que el sistema no genere falsos positivos. Una alerta emitida sobre ruido enseña al equipo que las alertas no importan, y a partir de ese momento el sistema está muerto aunque siga funcionando.

## 7.4 Consecuencia de la ruptura

Una ruptura confirmada **no bloquea automáticamente**. Genera alerta clasificada en el Panel Único (§10.7), dirigida al rol responsable, quien decide con criterio y registra la decisión.

Toda alerta tiene **dueño nominal** —una persona, nunca un colectivo—, plazo de atención de 24 horas para severidad alta y 48 para media, y escalamiento automático si vence sin atención. La decisión de no actuar es una decisión válida y **debe registrarse con motivo**, igual que la de actuar.

# LBPF-008 — Decision Patterns Catalog

Se mantienen íntegros los patrones de decisión de v1.0 y su anatomía mínima. Dos precisiones.

**DP-03 Cost-Probability Pairing.** El emparejamiento exige que costo y probabilidad se rendericen en la misma unidad visual y con peso tipográfico comparable. La probabilidad nunca en tamaño de nota al pie, nunca en pestaña distinta, nunca por debajo del pliegue cuando el costo está por encima.

**DP-13 Authentic Social Proof.** La prueba social se alimenta exclusivamente de resultados reales registrados, con ventana temporal visible. Prohibido contenido sintético, de ejemplo o de relleno. La identidad se muestra minimizada —nombre e inicial— y solo con consentimiento explícito capturado en el flujo de reclamo, revocable en cualquier momento.

**Patrón nuevo — DP-16 Symmetric Dispute.** Toda controversia entre partes se resuelve sobre evidencia clasificada por fuerza probatoria, nunca sobre la afirmación de una sola parte, y **en ninguna de las dos direcciones**. Cuando una parte aporta evidencia fuerte, la carga de la prueba se traslada a la otra, que debe rebatir con evidencia y no con aserción. Quien adjudica no puede ser quien atestó el caso.

Fundamento: un procedimiento que resuelve por afirmación crea un incentivo a afirmar en falso, y ese incentivo recae siempre sobre la parte con menos que perder. La simetría probatoria y la existencia de consecuencias reputacionales **para ambas partes** es lo que desactiva ese incentivo.

# LBPF-009 — Anti-patterns & LBPF Linter Rules

El catálogo de doce antipatrones se conserva íntegro en §9.2 de este documento. Ninguna versión anterior es fuente de contenido normativo (CD-06).

**Precisión de v2.0 sobre AP-01 y AP-08.** El antipatrón no es la urgencia ni la prueba social: es su **falsedad**. La escasez auténtica —“quedan 23 de 1.000 tickets”— es información esencial y su comunicación es legítima y deseable. El contador atado a un cierre real es legítimo. El ganador real de hace dos horas es legítimo. Lo prohibido es fabricar cualquiera de las tres.

Esta precisión importa porque la escasez en LIBOX es **estructuralmente verificable**: un pool finito con venta pública. LIBOX no necesita fabricar urgencia porque dispone de urgencia real, que además es más eficaz comercialmente por no desmoronarse ante el escrutinio.

## 9.1 Reglas de linter y régimen de cumplimiento

| Regla        | Verifica                                                                      | Severidad | Régimen v2.0      |
| ------------ | ----------------------------------------------------------------------------- | --------- | ----------------- |
| LINT-001     | Urgencia atada a plazo real                                                   | ERROR     | Advierte          |
| LINT-002     | Presencia de costo, probabilidad y evidencia en tarjetas de oportunidad       | ERROR     | Advierte          |
| **LINT-003** | Ninguna animación \> 240 ms en Zona de Decisión                               | ERROR     | **Bloquea merge** |
| **LINT-004** | Ninguna animación infinita en Zona de Decisión                                | ERROR     | **Bloquea merge** |
| **LINT-005** | Ningún default premarcado en opciones monetarias o de marketing               | ERROR     | **Bloquea merge** |
| **LINT-011** | Ninguna participación adicional ni ventaja de probabilidad derivada del gasto | ERROR     | **Bloquea merge** |
| LINT-006     | Recomendación con metadata de razón                                           | WARNING   | Advierte          |
| LINT-007     | Copy sin claim absoluto ni coerción                                           | WARNING   | Advierte          |
| LINT-008     | Opt-out alcanzable en ≤ 2 pasos                                               | WARNING   | Advierte          |
| LINT-009     | Propagación de `trace_id` en eventos de decisión                              | ERROR     | Advierte          |
| LINT-010     | Etiquetas y jerarquía accesibles                                              | WARNING   | Advierte          |

**Criterio de bloqueo.** Bloquea el merge lo que ya es **norma decidida de umbral cero** en este framework: no hay animación infinita admisible en un checkout, ni default premarcado admisible en una opción monetaria. No son hipótesis que los datos de producción vayan a matizar; son decisiones tomadas.

Advierte lo que requiere **calibración** o **criterio contextual**: los umbrales de proporción visual, la suficiencia de una metadata de razón, la naturaleza de un claim.

**Bloquear el merge no retrasa un lanzamiento.** Detiene la integración del código antes de que exista en ningún entorno; quien lo escribió lo ve en segundos y lo corrige en minutos. Lanzar un patrón oscuro para “medir su impacto” significa que personas reales lo reciben mientras se mide, lo cual es incompatible con R-01 y R-03.

## 9.2 Metadatos mínimos de componente

Todo componente de oportunidad o decisión declara: `behavioral_zone`, `decision_class`, `lbpf_patterns`, `probability_source`, `evidence_source`, `motion_profile`, `tracking_events`.

# LBPF-010 — Experience Governance & BDR Protocol

Se mantienen la clasificación B0-B4, la plantilla de Behavioral Decision Record y la integración con control de versiones y auditoría.

## 10.4 Degradación controlada en MVP

R-07 permite degradar operativamente sin que el control desaparezca semánticamente. v2.0 declara qué se degrada y **qué lo sustituye**, porque una degradación sin sustituto no es degradación: es ausencia.

| Control                                           | Estado en MVP               | Sustituto operativo                                                      |
| ------------------------------------------------- | --------------------------- | ------------------------------------------------------------------------ |
| Doce KPI con seguimiento continuo                 | Seis activos                | Los seis restantes permanecen como norma auditable en revisión de diseño |
| Análisis automatizado de patrones de gasto        | Diferido                    | Acumuladores multi-ventana con alertas por umbral                        |
| Autoexclusión federada entre operadores           | Diferida                    | Autoexclusión de plataforma, irreversible durante el plazo               |
| Enfriamiento, reality check y detección de patrón | Declarados y deshabilitados | Panel de gasto visible y límites autoimpuestos                           |
| Verificación automatizada de premios registrables | No aplica                   | **Proceso mecánico por etapas con validación documental notarial**       |
| Personalización explicable medida                 | Regla binaria               | LINT-006                                                                 |

**Regla de degradación:** todo control degradado se declara en el modelo de datos y en la configuración, **deshabilitado por parámetro y nunca ausente del diseño**. Habilitarlo debe ser una operación de configuración, jamás un rediseño.

## 10.5 Métricas guardrail

Los seis KPI activos de §7.1, con el método de §7.3.

## 10.6 Release gates

Una entrega no se libera si: incumple un límite duro de Motion Calm en Zona de Decisión; introduce un default no conservador en opción monetaria; publica una oportunidad sin costo, probabilidad y pool visibles; publica una oportunidad sin valor de premio verificado; o carece de la ruta de resolución, plazos y costos exigidos por BR-08.

## 10.7 Panel Único de Alarmas

**Norma nueva en v2.0, y condición de validez de R-10.**

Existe **un solo** panel de alarmas, no uno por dominio. Concentra alertas conductuales, de riesgo y fraude, de vencimiento de plazos, de concentración de tickets, de cumplimiento financiero y de excepciones de conciliación.

**Esquema común obligatorio:** tipo, severidad, entidad afectada, `trace_id`, **dueño nominal**, plazo de atención, estado, y resolución con motivo. Acceso restringido a roles internos, con visibilidad acotada por subrol.

**Reglas:** toda alerta tiene una persona responsable, nunca un colectivo · plazo de 24 horas para severidad alta y 48 para media · escalamiento automático al vencer · **la conclusión de que no hay problema se documenta con motivo, igual que la de actuar**.

Fundamento de la última regla: una auditoría no pregunta qué se reportó, pregunta qué se revisó y por qué se decidió no reportar. La trazabilidad de la no-decisión es lo que hace defendible el proceso.

**Fundamento de la existencia del panel.** Al establecer R-10 se renunció a la vigilancia distribuida que proporcionaba la divulgación pública. Esa capacidad de detección debe existir en algún lugar, y ese lugar es este panel. **Si el panel no opera con dueños y plazos reales, R-10 pierde su justificación** y la confidencialidad de participación debería revisarse.

# LBPF-011 — Adaptabilidad Regulatoria Multi-Mercado

*Norma nueva en v2.0.*

## 11.1 Principio

LIBOX opera bajo marcos regulatorios que difieren por jurisdicción y cambian en el tiempo. El producto se diseña para que **adaptarse a un cambio normativo sea una operación de configuración**, verificable y aprobada, y no una modificación de software.

Si adaptarse a un requisito regulatorio exige tocar código, el diseño falló.

## 11.2 Alcance de la configuración por mercado

Es configuración versionada por mercado, y por tanto nunca código: requisitos de identidad y verificación · umbrales financieros y de acreditación · régimen tributario y de comprobantes · documento habilitante del sorteo, autoridad competente y ámbito de la exigencia · plazos de reclamo, entrega y retención · categorías de premio admisibles · moneda, unidad mínima y regla de redondeo · política de contenido, calendario de feriados y zona horaria · controles de juego responsable exigibles · umbral de concentración · parámetros de muestreo conductual.

## 11.3 Reglas

**Versionado con vigencia.** Toda configuración se versiona con fechas. **Una oportunidad se rige por la versión vigente el día de su publicación, no por la actual.** Sin esto es imposible demostrar cumplimiento retroactivo ante una autoridad.

**El mercado pertenece a la oportunidad, no a la persona.** Cada sorteo opera en un mercado y una moneda. No hay conversión de divisa ni participación transfronteriza.

**Interfaz única, contenido variable.** La experiencia es la misma en todos los mercados. Lo que cambia —moneda y su formato, denominación del documento de identidad, etiquetas fiscales, plazos, categorías disponibles, textos legales— proviene del servidor. La interfaz no decide nada por jurisdicción: lo presenta.

**Tolerancia de composición.** El diseño debe soportar variación sustancial en la longitud de los textos. Una etiqueta de tres caracteres en un mercado puede tener veinte en otro. Un componente compuesto sobre la longitud de un idioma o de una jurisdicción específica se rompe al abrir el siguiente, y corregirlo después supone revisar la totalidad de las pantallas.

**Suspensión gradual.** Debe existir capacidad de suspender la operación de un mercado por niveles —ventas, publicación, registro, total— sin afectar las oportunidades ya vendidas, que deben poder resolverse y liquidarse. **Ningún nivel de suspensión puede impedir reclamar un premio, recibir un reembolso o disponer del saldo propio** (§5.4).

**Diseño por el estándar más exigente.** Cuando exista duda sobre si una obligación regulatoria aplica, se diseña como si aplicara. Relajar un control después es trivial; incorporarlo con operación en curso y usuarios activos, no.

# LBPF-012 — Ética Comercial y de Crecimiento

*Norma nueva en v2.0.*

## 12.1 Separación de ámbitos

La estrategia de marketing, adquisición y ventas es **externa al diseño del producto**. El producto no la define. Pero el producto **sí define sus límites**, porque toda comunicación comercial es una superficie conductual y está sujeta a R-01.

El sistema provee a las áreas comerciales los datos e instrumentos que necesitan; el framework establece qué no pueden hacer con ellos.

## 12.2 Límites

**Uniformidad de precio.** El precio del ticket de una oportunidad es único e inmutable para todos los participantes. Toda promoción se instrumenta como crédito aplicable, **nunca como precio diferenciado**. Esto alcanza también a los beneficios de suscripción: **un beneficio jamás es descuento sobre el ticket** (§13.2). Dos personas no pueden pagar cantidades distintas por la misma probabilidad: rompería la equivalencia entre aporte y participación y afectaría la integridad de la oportunidad.

**Identificación de la promoción.** Toda posición destacada por contraprestación se identifica visiblemente como tal y se presenta separada del ordenamiento orgánico. La publicidad no identificada es publicidad encubierta.

**Explicabilidad del ordenamiento.** Todo ordenamiento o recomendación expone su criterio en una interacción: por cierre próximo, por volumen de oportunidades completadas por el organizador, por velocidad de venta. El criterio nunca es opaco (DP-12, LINT-006).

**Equidad de descubrimiento.** Todo criterio de destaque basado en el historial del organizador debe reservar cuota para organizadores nuevos verificados. Un ordenamiento que se retroalimenta convierte al primero en único, cierra el mercado y contradice el propósito de §1.1.

**Recompensa por referido.** Toda recompensa por recomendación se paga por **registro verificado**, nunca en función del gasto de la persona referida. Retribuir el gasto de un tercero en un producto de participación onerosa configura un incentivo de captación en cadena, incompatible con R-08.

**Simetría de reglas.** La comunicación comercial —correo, notificación, red social, publicidad— está sujeta a las mismas reglas de probabilidad, costo, urgencia y evidencia que la interfaz transaccional. Lo prohibido dentro del producto lo está también fuera de él.

**Respeto automático del consentimiento.** El sistema hace cumplir por sí mismo la exclusión voluntaria, la baja de comunicaciones y los períodos de descanso. Marketing no puede vulnerarlos aunque quiera: no es una política, es una restricción del sistema.

# 13\. Neutralidad económica frente al azar

*Declaración estructural nueva en v2.0.*

> **LIBOX no lucra con el azar. Percibe una comisión por el uso de su sistema de sorteos.**

Esta afirmación es una posición estructural, y el diseño del producto debe sostenerla en todo momento:

  - La comisión es un porcentaje fijo de la recaudación, **idéntica sea cual sea el resultado**.
  - LIBOX **no participa** del premio ni retiene parte de él.
  - LIBOX **no ofrece** instrumento, producto ni mecanismo cuyo valor dependa de quién resulta ganador.
  - LIBOX **no adquiere** participaciones en las oportunidades que aloja.
  - Los ingresos de LIBOX son **indiferentes** a la identidad del ganador.

**Ninguna evolución futura del producto puede vulnerar esta neutralidad.** Toda propuesta que la comprometa exige BDR de clase B4 y revisión legal previa. La neutralidad económica es la que sostiene la naturaleza del negocio como infraestructura de confianza y no como operador de juego.

## 13.1 Regla de parte relacionada

LIBOX necesita organizar oportunidades propias: sorteos promocionales para activar su base, campañas conjuntas con organizadores, y premios de adquisición. Hacerlo **directamente** vulneraría la neutralidad, porque LIBOX pasaría a participar del premio y a organizar lo que aloja.

**La resolución no es abrir una excepción a la neutralidad: es no necesitarla.**

> **Una entidad vinculada a LIBOX puede organizar oportunidades en la plataforma únicamente en condición de cliente**, sujeta a las mismas reglas, los mismos gates y las tarifas publicadas.

| \#    | Condición                                                                                                                                    |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| PR-01 | Paga las **tarifas publicadas**. Sin tarifa especial, sin exención, sin condiciones que no estén disponibles para cualquier otro organizador |
| PR-02 | Pasa **todos los gates**: verificación de valor del premio, gate legal, atestación de entrega, resolución y controversias                    |
| PR-03 | Se identifica como **parte relacionada** en el registro contable y en la auditoría. No se oculta                                             |
| PR-04 | **El sistema la trata igual que a cualquier organizador.** Ninguna ruta de código, configuración ni permiso puede darle trato distinto       |
| PR-05 | No accede a datos de otros organizadores ni a información de la plataforma no disponible para el resto                                       |

**PR-04 es la condición que hace creíble la estructura.** Una separación societaria que dentro del sistema se traduce en privilegios no es separación: es la misma entidad con dos nombres.

**Límite de la estructura, dicho con honestidad.** La separación preserva la neutralidad en la forma y en gran medida en el fondo, pero **una autoridad evalúa sustancia**. Si el control es común, la separación ayuda y no blinda. Es materia de decisión societaria y legal, y este framework solo fija lo que corresponde al producto: **trato idéntico, sin excepción**.

## 13.2 Límite de la suscripción

LIBOX puede ofrecer suscripciones de beneficios como fuente de ingreso recurrente. Con un límite que no admite matiz:

> **Ninguna suscripción otorga participaciones, entradas, ventajas de probabilidad ni acceso preferente a oportunidades.**

Los beneficios admisibles son ajenos al azar: acceso anticipado al catálogo, avisos y alertas, filtros, ventajas con comercios aliados, atención preferente. **Nunca descuento sobre el precio del ticket**, que rompería la uniformidad de precio dentro de una oportunidad.

**Fundamento.** Una suscripción que incluye participaciones convierte parte del ingreso de LIBOX en cobro por ofrecer azar, y §13 deja de ser cierto en el momento exacto en que más importa que lo sea. Cruzar esta línea es decisión de clase **B4 con revisión legal previa**, nunca un añadido de plan comercial.

# 14\. Aplicación transversal

El LBPF aplica a producto, diseño, ingeniería, contenido, soporte, riesgo, cumplimiento, marketing y comercial. Ninguna función está exenta.

Todo cambio de clase B2 a B4 requiere BDR con: intención conductual, principios y patrones aplicados, antipatrones descartados, evidencia esperada, y plan de reversión.

# 15\. Roadmap de adopción

| Fase | Contenido                                                        |
| ---- | ---------------------------------------------------------------- |
| 1    | Adopción de vocabulario, zonas y clasificación de decisiones     |
| 2    | Verified Opportunity Card y divulgación conforme a §6.2.1        |
| 3    | Instrumentación de eventos de decisión e instrumento de encuesta |
| 4    | Linter en integración continua con el régimen de §9.1            |
| 5    | Panel Único de Alarmas con dueños y plazos operando              |
| 6    | Auditoría conductual periódica y protocolo BDR en régimen        |

# Anexo A — Trazabilidad con el corpus

| Norma LBPF                  | Sección de PRD que la implementa                                             |
| --------------------------- | ---------------------------------------------------------------------------- |
| R-09, LBPF-011              | Configuración por mercado y suspensión gradual                               |
| R-10, §6.2.1                | Divulgación en detalle de oportunidad                                        |
| §5.4                        | Retención de recaudación y motor de liquidación                              |
| §5.5                        | Gate de verificación de valor · verificación de identidad con prueba de vida |
| §6.2.2                      | Límite de concentración                                                      |
| BR-08                       | Publicación de plazos, ruta de resolución y costos antes de la venta         |
| DP-16                       | Protocolo de resolución de controversias                                     |
| §7.3                        | Eventos de decisión, instrumento de encuesta y agregación de indicadores     |
| §9.1                        | Integración continua y régimen de bloqueo                                    |
| §10.7                       | Panel Único de Alarmas                                                       |
| LBPF-004                    | Asignación automática de identificador de ticket                             |
| §0.3                        | Reserva en materia de prevención financiera                                  |
| §13                         | Modelo de comisión                                                           |
| §13.1 Parte relacionada     | Régimen de organizador vinculado                                             |
| §13.2 Límite de suscripción | LIBOX Club                                                                   |
| BR-09 Proporción razonable  | Rango de recaudación y gate de valoración                                    |
| P13 Igualdad de vía         | Sorteo con entrada gratuita                                                  |

# Anexo B — Plantilla BDR

Identificador · fecha · autor · clase B0-B4 · intención conductual · principios aplicados · patrones aplicados · antipatrones descartados · zona afectada · métricas esperadas · plan de reversión · aprobación.

# Anexo C — Checklist de auditoría conductual

1.  ¿Costo, probabilidad y tamaño de pool visibles antes del llamado a la acción?
2.  ¿Valor del premio verificado con fuente y fecha?
3.  ¿Plazos, ruta de resolución y costos de recepción publicados antes de la venta?
4.  ¿Evidencia accesible en una interacción?
5.  ¿CTA descriptivo y no coercitivo?
6.  ¿Ausencia de animación infinita o superior a 240 ms en Zona de Decisión?
7.  ¿Ausencia de defaults premarcados en opciones monetarias?
8.  ¿Prueba social exclusivamente auténtica y con consentimiento?
9.  ¿Ordenamiento con criterio expuesto?
10. ¿Corrección posible antes del compromiso irreversible?
11. ¿Baja alcanzable en dos pasos o menos?
12. ¿Identidad y concentración no divulgadas?
13. ¿Etiquetas y textos provenientes del servidor, sin fijación por jurisdicción?
14. ¿Composición tolerante a variación de longitud de texto?

*LBPF V3 — Nivel L0. Los PRD MVP V9 y Enterprise V3 consumen este documento por referencia normativa conforme a R-02.*
