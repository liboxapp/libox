# Índice de contenidos

# 0\. Control documental

**Documento:** LIBOX\_PRD\_BLUEPRINT\_ENTERPRISE\_V3 **Versión:** V3 **Nivel:** L2 — Anexo direccional **Reemplaza:** LIBOX PRD Blueprint Enterprise V2 (deprecado en su totalidad) **Gobernado por:** LBPF V2 (nivel L0), por referencia normativa conforme a R-02 **Complementa:** LIBOX PRD Blueprint MVP V4 **Compatible con:** Especificación Técnica L3 V7 **Estado:** vigente, no ejecutable

## 0.1 Qué es y qué no es este documento

Este documento **no describe un producto a construir**. Describe **cuándo y por qué** la arquitectura del MVP dejará de ser suficiente, y qué se hace entonces.

Su naturaleza es direccional por una razón de disciplina: la versión V1 contenía veinte fichas de construcción de microservicios, arquitectura de eventos distribuida y planes de infraestructura elástica, escritos antes de la primera venta. Ese contenido **contradecía la regla más valiosa del propio documento**, que prohíbe extraer servicios antes de alcanzar un umbral de operación real.

V2 resolvió la contradicción eliminando el contenido prematuro y conservando la regla.

| Este documento contiene                                                | Este documento no contiene                    |
| ---------------------------------------------------------------------- | --------------------------------------------- |
| El umbral cuantitativo que habilita la evolución arquitectónica        | Fichas de construcción de servicios           |
| El orden de extracción por dolor observado, no por dependencia teórica | Diseño de infraestructura elástica            |
| El costo estimado de cada paso                                         | Contratos de interfaz entre servicios         |
| El criterio de reversión de cada extracción                            | Esquemas de datos distribuidos                |
| Los gates legales de apertura de mercado                               | Configuración de orquestación de contenedores |
| Lo que se decide hoy para no bloquear mañana                           | Cronograma de migración                       |

## 0.2 Changelog

### Cambios de la versión V3

| Versión | Sección            | Qué cambió                                        | Por qué                                                                                                                             | Decisión que invalida               |
| ------- | ------------------ | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| V3      | Control documental | **Referencias actualizadas a PRD MVP V7 y L3 V3** | El documento complementaba una versión del contrato funcional que ya no es vigente. Cinco referencias apuntaban a la línea anterior | Corrige el control documental de V2 |
| V3      | Todo               | Nomenclatura normalizada sin dígito menor         | La política documental no admite subversiones                                                                                       | Amplía                              |

**Ningún contenido conceptual de V2 cambia en V3.** La regla de bloqueo, las señales de dolor, el orden de extracción, el criterio de reversión y los gates de apertura de mercado se conservan íntegros.

### Cambios de la versión V2

| Versión | Fecha      | Sección    | Qué cambió                                                                    | Por qué                                                                                                                                        | Decisión que invalida                                              |
| ------- | ---------- | ---------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| V2      | 2026-08-06 | §2 V1      | **Eliminados los 20 Service Build Books**                                     | Contradecían la regla de bloqueo del propio documento y describían servicios que nadie ha necesitado                                           | Deroga §2 de V1 completa                                           |
| V2      | 2026-08-06 | §3 V1      | Eliminada la plataforma de eventos distribuida como contenido de construcción | El patrón de bandeja de salida del MVP cubre la necesidad hasta el umbral                                                                      | Deroga §3 de V1                                                    |
| V2      | 2026-08-06 | §4 V1      | **Ledger migrado al PRD MVP V7 y a L3**                                       | El plan de cuentas de partida doble estaba en el documento congelado mientras el MVP lo necesitaba en el sprint de liquidación                 | Deroga §4 de V1; el contenido vive ahora en MVP §10 y L3 §6        |
| V2      | 2026-08-06 | §5 V1      | **Motor de sorteo migrado y corregido**                                       | El algoritmo estaba únicamente aquí, y permitía manipulación por repetición: obtenía entropía en el momento de ejecutar, sin compromiso previo | Deroga §5 de V1; el contenido corregido vive en MVP §12 y L3 V6 §5 |
| V2      | 2026-08-06 | §6 a §9 V1 | Reducidas a criterios de evolución                                            | Describían capacidades sin umbral de activación                                                                                                | Reemplaza §6 a §9 de V1                                            |
| V2      | 2026-08-06 | §10.0 V1   | **Conservada íntegra y elevada a §1**                                         | Es la decisión más valiosa del expediente                                                                                                      | Ninguna                                                            |
| V2      | 2026-08-06 | §3 nueva   | Orden de extracción **por dolor observado**                                   | V1 ordenaba por dependencia técnica, no por necesidad                                                                                          | Amplía                                                             |
| V2      | 2026-08-06 | §4 nueva   | Costo estimado de la evolución                                                | V1 protegía del gasto prematuro sin informar del gasto futuro                                                                                  | Amplía                                                             |
| V2      | 2026-08-06 | §5 nueva   | **Criterio de reversión** de cada extracción                                  | V1 tenía retroceso por paso, sin regla para declarar fallida una extracción                                                                    | Amplía                                                             |
| V2      | 2026-08-06 | §8 nueva   | Multi-inquilino y marca blanca                                                | Mencionado en el LBPF, ausente del documento                                                                                                   | Amplía                                                             |
| V2      | 2026-08-06 | Anexos     | 15 de 18 anexos vacíos: eliminados                                            | Un anexo referenciado sin contenido es peor que su ausencia                                                                                    | Deroga los anexos vacíos de V1                                     |

# 1\. La regla de bloqueo

## 1.1 Enunciado

> **Cero extracción de microservicios, cero mensajería distribuida en producción, cero orquestación de contenedores elástica, hasta alcanzar 10.000 transacciones mensuales pagadas con ledger balanceado.**

Esta regla se conserva **literal** de la versión anterior. Es la decisión de arquitectura más valiosa del expediente y no se modifica.

## 1.2 Definición precisa del umbral

Para que la regla no admita interpretación, sus términos se definen aquí:

| Término                | Definición                                                                                      |
| ---------------------- | ----------------------------------------------------------------------------------------------- |
| **Transacción pagada** | Orden en estado `PAID` con al menos un ticket emitido y asiento contable registrado             |
| **Mensual**            | Mes calendario completo en la zona horaria del mercado                                          |
| **Ledger balanceado**  | Los siete invariantes contables (L3 §6.4) verificados sin excepción durante los 30 días del mes |
| **10.000**             | Agregado de todos los mercados operativos                                                       |

**El umbral se cumple cuando se alcanza en dos meses consecutivos.** Un mes aislado por efecto de una campaña no habilita nada.

## 1.3 Por qué existe

Un monolito modular con base de datos relacional única sostiene un volumen muy superior al del umbral. Lo que un equipo pequeño no sostiene es la complejidad operativa de un sistema distribuido: consistencia eventual entre servicios, transacciones compensatorias, trazabilidad fragmentada, y una superficie de fallo que crece más rápido que el equipo.

Extraer servicios antes del umbral no produce escalabilidad: produce el costo de la escalabilidad sin su beneficio.

## 1.4 Qué sí está permitido antes del umbral

La regla prohíbe la distribución, no la preparación. Se permite y se recomienda:

  - Fronteras de módulo estrictas, con propiedad exclusiva de tablas por agregado y prohibición de escritura cruzada, verificada en compilación (MVP §3.1)
  - Patrón de bandeja de salida y comunicación entre módulos por evento
  - Interfaces con adaptador para todo proveedor externo
  - Particionamiento de tablas de crecimiento sin techo desde la primera migración
  - Trazabilidad extremo a extremo por identificador de traza
  - Réplica de solo lectura para reportería
  - Caché en memoria como optimización, nunca como fuente autoritativa

**Todo eso es trabajo del MVP y ya está especificado.** Es lo que hace que la extracción futura sea un movimiento de código y no una reescritura.

# 2\. Señales de dolor

## 2.1 Principio

**Nada se extrae porque toque. Se extrae cuando duele, y se extrae lo que duele.**

La versión anterior ordenaba la migración por dependencia técnica. Esa secuencia describe qué se puede extraer primero, no qué conviene extraer primero. El orden correcto lo dicta el síntoma observado en producción.

## 2.2 Catálogo de señales

Cada señal tiene su métrica, su umbral y la respuesta proporcionada. **La primera respuesta casi nunca es extraer un servicio.**

| \#  | Señal                                            | Métrica observable                                               | Umbral                  | Respuesta ordenada                                                                                  |
| --- | ------------------------------------------------ | ---------------------------------------------------------------- | ----------------------- | --------------------------------------------------------------------------------------------------- |
| S-1 | El despacho de eventos no sigue el ritmo         | Retraso de la bandeja de salida                                  | \> 5 min sostenido      | 1\. Aumentar concurrencia del despachador · 2. Particionar por agregado · 3. Extraer el despachador |
| S-2 | La escritura del ledger se convierte en cuello   | Contención de bloqueo sobre asientos                             | p95 de espera \> 200 ms | 1\. Revisar índices y lotes · 2. Particionar por mercado · 3. Extraer contabilidad                  |
| S-3 | La lectura del catálogo degrada la escritura     | Carga de consultas de descubrimiento sobre la instancia primaria | \> 60 % del total       | 1\. Réplica de lectura · 2. Caché de catálogo · 3. Servicio de lectura dedicado                     |
| S-4 | Los picos de venta saturan el proceso            | Latencia p95 de creación de orden                                | \> 800 ms en picos      | 1\. Escalado horizontal del monolito · 2. Cola de admisión · 3. Extraer compra                      |
| S-5 | La verificación de identidad bloquea el registro | Latencia de proveedor externo                                    | p95 \> 8 s              | 1\. Asincronía con estado intermedio · 2. Extraer verificación                                      |
| S-6 | La resolución de casos crece con el catálogo     | Salas abiertas simultáneas                                       | \> 2.000                | 1\. Índices y colas por asignado · 2. Extraer resolución                                            |
| S-7 | Un mercado afecta a otro                         | Incidentes correlacionados entre mercados                        | Cualquier ocurrencia    | 1\. Particionar por mercado · 2. **Aislamiento de datos por mercado** · 3. Despliegue por región    |
| S-8 | El equipo se bloquea entre sí                    | Conflictos de despliegue por semana                              | \> 3 sostenido          | Es la señal organizativa, no técnica. Extraer el módulo del equipo con más bloqueos                 |
| S-9 | El cumplimiento exige aislamiento                | Requisito regulatorio de residencia de datos                     | Cualquier ocurrencia    | Aislamiento por mercado. **No es opcional ni graduable**                                            |

**S-8 y S-9 son las únicas señales que pueden justificar extracción antes del umbral de §1.** La primera porque el cuello es humano y ninguna optimización técnica lo resuelve; la segunda porque una obligación regulatoria no admite postergación.

## 2.3 Regla de proporcionalidad

Antes de extraer un servicio deben haberse agotado, y documentado como agotadas, las respuestas de menor costo de la fila correspondiente. Una extracción sin ese registro se rechaza en revisión de arquitectura.

# 3\. Orden de extracción

## 3.1 Secuencia recomendada

Si las señales aparecen simultáneamente, este es el orden que maximiza beneficio y minimiza riesgo. **Es una recomendación condicionada al síntoma, no un plan.**

| Paso | Qué se extrae                              | Por qué en esta posición                                                    | Riesgo       |
| ---- | ------------------------------------------ | --------------------------------------------------------------------------- | ------------ |
| 1    | **Lectura de catálogo**                    | Sin escritura, sin transacción, sin dinero. Reversible en horas             | Bajo         |
| 2    | **Despacho de eventos**                    | Ya está desacoplado por la bandeja de salida; extraerlo es mover un proceso | Bajo         |
| 3    | **Notificaciones**                         | Sin efecto patrimonial; el fallo es tolerable y reintentables               | Bajo         |
| 4    | **Analítica e indicadores**                | Consume eventos, no produce estado de dominio                               | Bajo         |
| 5    | **Verificación de identidad y documentos** | Frontera natural con proveedores externos; ya está tras adaptador           | Medio        |
| 6    | **Resolución y controversias**             | Dominio acotado, pero produce la atestación que alimenta liquidación        | Medio        |
| 7    | **Compra y pago**                          | Alta contención, pero **toca dinero**: exige transacciones compensatorias   | Alto         |
| 8    | **Contabilidad y liquidación**             | El último. Es la fuente de verdad patrimonial                               | **Muy alto** |

## 3.2 Lo que no se extrae

| Nunca se extrae                   | Razón                                                                                                                                                                                                           |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Sorteo y prueba criptográfica** | La ejecución debe ser atómica con el congelamiento del pool. Distribuirla introduce una ventana en la que el pool y el compromiso pueden divergir, y esa ventana es exactamente el vector que el diseño elimina |
| **Emisión de tickets**            | Debe ocurrir en la misma transacción que la confirmación del pago y los asientos, o aparece el estado inconsistente de un cobro sin tickets                                                                     |
| **Motor de control de acceso**    | Distribuir la autorización multiplica los puntos donde puede fallar una incompatibilidad dura                                                                                                                   |

Estos tres permanecen en el núcleo transaccional aunque todo lo demás se extraiga.

# 4\. Costo de la evolución

La regla de §1 protege del gasto prematuro. Esta sección informa del gasto futuro, para que la decisión de cruzar el umbral sea deliberada.

## 4.1 Naturaleza de los costos

| Categoría           | Contenido                                                                                                                  |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **Infraestructura** | Orquestación, mensajería gestionada, malla de servicios, réplicas por servicio, entornos adicionales                       |
| **Observabilidad**  | Trazado distribuido, agregación de registros y métricas por servicio. Crece más que linealmente con el número de servicios |
| **Equipo**          | Ingeniería de plataforma dedicada. Un sistema distribuido sin personas que lo operen es una deuda con intereses            |
| **Coordinación**    | Contratos entre servicios, versionado, compatibilidad hacia atrás, pruebas de contrato                                     |
| **Oportunidad**     | Cada sprint dedicado a extracción es un sprint no dedicado a producto                                                      |

## 4.2 Regla de decisión

Antes de cada paso de extracción se estima el costo anual incremental de las cinco categorías y se contrasta con el costo del problema que resuelve.

**Un paso cuyo costo anual supera el costo del problema no se ejecuta, aunque la señal esté activa.** Se documenta la decisión de no actuar, con su motivo, igual que se documentaría la de actuar.

## 4.3 Costo del camino no tomado

Conviene registrar también lo contrario: qué cuesta **no** extraer cuando la señal persiste. Se mide como degradación de servicio, incidentes atribuibles y tiempo de ingeniería consumido en mitigaciones. Sin esta medición, la disciplina de §1 se convierte en inercia.

# 5\. Reversión

## 5.1 Principio

Toda extracción es una hipótesis. Una hipótesis necesita condición de refutación declarada **antes** de ejecutarla.

## 5.2 Criterio de fallo

Una extracción se declara fallida y se revierte al monolito si, transcurridos 60 días desde su puesta en producción, se cumple cualquiera de:

| \#  | Condición                                                                         |
| --- | --------------------------------------------------------------------------------- |
| R-1 | La señal de dolor que la motivó no mejoró de forma medible                        |
| R-2 | Los incidentes atribuibles al nuevo servicio superan a los que resolvió           |
| R-3 | La latencia extremo a extremo de los recorridos afectados empeoró                 |
| R-4 | Apareció inconsistencia de datos entre el servicio y el núcleo en cualquier grado |
| R-5 | El equipo dedica más tiempo a operar el servicio que el que ahorró                |

## 5.3 Condiciones para que la reversión sea posible

Estas cinco se establecen **antes** de la extracción, no después:

1.  El código extraído conserva su forma de módulo y no adopta un modelo de datos divergente durante el periodo de prueba
2.  La escritura se dirige a un único propietario de datos; no hay doble escritura permanente
3.  Existe una bandera de configuración que redirige el tráfico al camino anterior
4.  El esquema del servicio permanece en la misma base de datos hasta superar el periodo de prueba
5.  Existen pruebas de contrato que cubren ambos caminos

**Sin las cinco, la extracción no se autoriza.** Una extracción irreversible no es una hipótesis: es una apuesta.

## 5.4 Reversión de datos

Si el servicio adquirió base de datos propia y debe revertirse, se detiene la escritura, se reconcilia contra el núcleo, se verifica la integridad referencial y solo entonces se redirige el tráfico. En dominio con efecto patrimonial la reconciliación exige cuadre contable completo, no muestreo.

# 6\. Evolución por dominio

Lo que cambia en cada dominio al superar el umbral. **Todo lo aquí descrito está fuera del alcance del MVP y ninguna de estas capacidades condiciona su construcción**, salvo las decisiones señaladas como preparatorias.

## 6.1 Contabilidad

| Capacidad                    | Detalle                                                                                                                                         |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Cierre contable periódico    | Balance de comprobación, bloqueo de periodo cerrado, ajustes solo con apertura autorizada                                                       |
| Multi-moneda con conversión  | Cuenta de compensación cambiaria, política de tipo de cambio y reconocimiento de diferencia. **Fuera del MVP por decisión expresa** (MVP §24.5) |
| Consolidación multi-mercado  | Reportería agregada con conversión a moneda de presentación                                                                                     |
| Conciliación multi-proveedor | Varios proveedores por mercado con emparejamiento y cola unificada                                                                              |

**Decisión preparatoria ya tomada en el MVP:** cuentas instanciadas por moneda e importes con código de moneda adyacente. Introducir conversión después es añadir cuentas, no rehacer el ledger.

## 6.2 Sorteo

El algoritmo **no cambia**. Cambia su operación.

| Capacidad                                       | Detalle                                                                                            |
| ----------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Múltiples fuentes de baliza                     | Redundancia ante indisponibilidad de la fuente primaria, declarada por adelantado en el compromiso |
| Publicación de pruebas en repositorio inmutable | Archivo verificable de largo plazo, independiente de la infraestructura de LIBOX                   |
| Verificación por tercero                        | Publicación de la implementación de verificación como herramienta de uso público                   |
| Auditoría criptográfica externa                 | Revisión independiente del esquema de compromiso y revelación                                      |

**Ninguna de estas capacidades altera el resultado de un sorteo.** Todas aumentan la capacidad de demostrarlo.

## 6.3 Riesgo y fraude

| Capacidad                         | Detalle                                                                                                  |
| --------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Grafo de relaciones               | Detección de vínculos entre organizadores y compradores más allá de la coincidencia directa de atributos |
| Modelos de comportamiento         | Puntuación aprendida sobre historial propio, con explicabilidad exigible (LBPF DP-12)                    |
| Listas compartidas entre mercados | Sujeto a marco de protección de datos de cada jurisdicción                                               |
| Autoexclusión federada            | Interoperabilidad con esquemas multi-operador donde existan                                              |

**Restricción permanente:** ninguna capacidad de riesgo puede segmentar ni personalizar explotando vulnerabilidad (LBPF R-08). Un modelo que identifica usuarios en dificultad se usa para protegerlos, jamás para dirigirles oferta.

## 6.4 Infraestructura

| Capacidad                                  | Se activa cuando                                                 |
| ------------------------------------------ | ---------------------------------------------------------------- |
| Escalado automático                        | La carga presenta picos que el aprovisionamiento fijo no absorbe |
| Despliegue multi-región                    | S-7 o S-9                                                        |
| Recuperación ante desastre con conmutación | El objetivo de tiempo de recuperación baja de 4 horas            |
| Malla de servicios                         | Existen al menos cinco servicios extraídos. Antes es sobrecarga  |

## 6.5 Calidad

| Capacidad                           | Detalle                                                                                                       |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Pruebas de contrato entre servicios | Obligatorias desde la primera extracción                                                                      |
| Ingeniería de caos                  | Comienza por indisponibilidad de proveedor externo y de réplica de lectura, nunca por el núcleo transaccional |
| Despliegue progresivo               | Por porcentaje de tráfico, con reversión automática por indicador                                             |
| Ensayo con dinero real periódico    | El gate del MVP se convierte en verificación recurrente por mercado                                           |

# 7\. Apertura de mercados

## 7.1 Principio

**Lo que limita la expansión regional no es la arquitectura: es el marco legal de sorteos de cada jurisdicción.** El sistema estará técnicamente preparado mucho antes que los permisos. Esta sección existe para que nadie confunda la existencia de la configuración con la habilitación para operar.

## 7.2 Gates de apertura

Ninguno es graduable ni admite excepción comercial.

| Gate                           | Requisito                                                                                                           | Bloquea       |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------- | ------------- |
| **G-L1 Figura jurídica**       | Dictamen escrito sobre la naturaleza legal del producto y sobre si LIBOX requiere autorización propia como operador | Lanzamiento   |
| **G-L2 Autorización**          | Habilitación obtenida, con su ámbito definido: por sorteo, por operador o inexistente                               | Lanzamiento   |
| **G-L3 Tributario**            | Régimen aplicable, emisor de comprobantes, base imponible y retenciones                                             | Lanzamiento   |
| **G-L4 Prevención financiera** | Calificación como sujeto obligado y obligaciones derivadas                                                          | Lanzamiento   |
| **G-L5 Protección de datos**   | Marco aplicable, residencia de datos, derechos del titular, plazos de retención                                     | Lanzamiento   |
| **G-L6 Consumidor**            | Requisitos de información, canal de reclamaciones, límite de responsabilidad oponible                               | Lanzamiento   |
| **G-L7 Custodia de fondos**    | Admisibilidad del modelo de retención sin configurar actividad regulada adicional                                   | Lanzamiento   |
| **G-L8 Categorías de premio**  | Qué categorías son operables y bajo qué requisitos, en particular los bienes registrables                           | Por categoría |
| **G-O1 Pagos**                 | Proveedor con cobertura local y método de pago dominante del mercado                                                | Lanzamiento   |
| **G-O2 Identidad**             | Proveedor de verificación con prueba de vida contra fuente oficial local                                            | Lanzamiento   |
| **G-O3 Soporte**               | Capacidad de atención en horario e idioma del mercado                                                               | Lanzamiento   |

## 7.3 Secuencia de apertura

1.  Dictamen legal completo (G-L1 a G-L8)
2.  Contratación de proveedores y desarrollo de adaptadores (G-O1, G-O2)
3.  Alta de la configuración de mercado, versionada y aprobada
4.  Ensayo con dinero real en el mercado nuevo
5.  Apertura limitada con categorías y tipos restringidos
6.  Ampliación progresiva conforme a los gates satisfechos

**El paso 4 no se omite.** Un mercado nuevo con proveedores nuevos es un sistema que nunca se ha ejercitado extremo a extremo.

## 7.4 Aislamiento por mercado

| Nivel                                        | Cuándo                                     |
| -------------------------------------------- | ------------------------------------------ |
| Datos compartidos, particionados por mercado | Situación por defecto                      |
| Esquemas separados por mercado               | Requisito regulatorio de separación lógica |
| Bases de datos separadas                     | Requisito de residencia de datos           |
| Despliegue regional completo                 | Residencia estricta o latencia inaceptable |

**El requisito de residencia de datos (S-9) puede obligar a saltar directamente al nivel más alto**, con independencia del umbral de §1. Es la única excepción reconocida a la regla de bloqueo, junto con S-8.

# 8\. Multi-inquilino y marca blanca

## 8.1 Estado

**Fuera de alcance del MVP y de la primera fase Enterprise.** Se documenta porque el LBPF menciona la posibilidad de otras iniciativas sobre la misma base, y porque tres decisiones tomadas hoy determinan si será viable o costoso.

## 8.2 Decisiones preparatorias ya tomadas en el MVP

| Decisión                                                 | Efecto sobre multi-inquilino                                   |
| -------------------------------------------------------- | -------------------------------------------------------------- |
| Configuración por mercado versionada y externa al código | El mismo mecanismo soporta configuración por inquilino         |
| Tokens de diseño en formato portable                     | Permite tematización por marca sin bifurcar componentes        |
| Interfaz de cliente que no fija etiquetas ni formatos    | Permite cambiar denominación, idioma y textos legales por dato |
| Interfaces con adaptador para todo proveedor externo     | Permite proveedores distintos por inquilino                    |

## 8.3 Lo que faltaría

Identificador de inquilino en el modelo de datos con aislamiento verificado; segregación contable por inquilino con consolidación; control de acceso con ámbito de inquilino; y un modelo de responsabilidad legal que defina quién responde ante el consumidor final.

**Esta última es la pregunta difícil y es jurídica, no técnica.** En un esquema de marca blanca, si el operador visible es un tercero y la infraestructura es de LIBOX, la responsabilidad ante el participante debe estar definida antes de escribir código.

# 9\. Matriz MVP → Enterprise

| Capacidad            | MVP V4                                | Enterprise                                  | Preparación en el MVP                                  |
| -------------------- | ------------------------------------- | ------------------------------------------- | ------------------------------------------------------ |
| Arquitectura         | Monolito modular, 23 agregados        | Extracción selectiva por señal              | Fronteras estrictas verificadas en compilación         |
| Comunicación interna | Bandeja de salida y eventos           | Mensajería distribuida                      | Mismo contrato de evento con versión de esquema        |
| Base de datos        | Instancia única particionada          | Segregación por servicio o mercado          | Particionamiento desde la primera migración            |
| Lecturas             | Instancia primaria y caché            | Réplicas y servicio de lectura              | Consultas de lectura ya separadas                      |
| Contabilidad         | Partida doble, moneda por mercado     | Cierre periódico, conversión, consolidación | Cuentas por moneda; importes con código adyacente      |
| Sorteo               | Compromiso y baliza pública           | Redundancia de fuente y archivo inmutable   | Algoritmo y prueba idénticos                           |
| Riesgo               | Reglas configurables                  | Grafo y modelos explicables                 | Reglas como dato, no como código                       |
| Identidad            | Adaptador por mercado                 | Múltiples proveedores con conmutación       | Interfaz común ya definida                             |
| Pagos                | Adaptador primario por mercado        | Múltiples proveedores con enrutamiento      | Interfaz común ya definida                             |
| Cliente              | Web adaptable y aplicación progresiva | Aplicaciones nativas                        | Autenticación portable; interfaz agnóstica del cliente |
| Mercados             | Uno operativo, arquitectura preparada | Varios con aislamiento por nivel            | Configuración versionada y suspensión gradual          |
| Observabilidad       | Traza extremo a extremo               | Trazado distribuido                         | Identificador de traza ya propagado                    |
| Inquilinos           | Uno                                   | Multi-inquilino y marca blanca              | Configuración y tematización externas al código        |

**Toda la columna de preparación es trabajo del MVP y ya está especificada.** Ese es el propósito de este documento: garantizar que la evolución sea un movimiento y no una reescritura.

# 10\. Gobierno de la evolución

## 10.1 Decisión de cruzar el umbral

Se registra como decisión de arquitectura con: umbral alcanzado y evidencia de los dos meses consecutivos, señales de dolor activas con su métrica, respuestas de menor costo agotadas y documentadas, costo anual estimado, criterio de reversión y responsable.

**Sin ese registro no se autoriza ninguna extracción.**

## 10.2 Revisión periódica

Cada trimestre se revisa el estado de las señales de §2 y se decide expresamente. **La decisión de no actuar se documenta con su motivo**, igual que la de actuar. Sin revisión periódica, la disciplina de la regla de bloqueo degenera en inercia, que es un fallo distinto pero igual de costoso.

## 10.3 Vigencia de este documento

Se revisa al alcanzarse el umbral de §1 y ante la apertura de cada mercado nuevo. Toda modificación sigue la política de control documental: incremento de versión, changelog con la columna de decisión invalidada, y archivo de la versión anterior sin edición.

# Anexo A — Materias pendientes de dictamen

Comunes al PRD MVP V9 y ampliadas por mercado. Ninguna capacidad de este documento se ejecuta sin respuesta escrita de asesoría colegiada de la jurisdicción correspondiente.

| \#   | Materia                                                                       | Bloquea                                           |
| ---- | ----------------------------------------------------------------------------- | ------------------------------------------------- |
| E-01 | Figura jurídica y necesidad de autorización propia como operador, por mercado | Apertura de mercado                               |
| E-02 | Admisibilidad de la custodia de fondos en cada jurisdicción                   | Modelo de garantía patrimonial                    |
| E-03 | Calificación como sujeto obligado y obligaciones derivadas, por mercado       | Carga operativa de cumplimiento                   |
| E-04 | Requisitos de residencia de datos                                             | Nivel de aislamiento y arquitectura de despliegue |
| E-05 | Régimen tributario y emisión de comprobantes, por mercado                     | Motor de liquidación                              |
| E-06 | Categorías de premio admisibles, en particular bienes registrables            | Catálogo por mercado                              |
| E-07 | Responsabilidad ante el consumidor final en esquema de marca blanca           | Multi-inquilino                                   |
| E-08 | Transferencia transfronteriza de datos entre mercados                         | Listas compartidas de riesgo                      |

# Anexo B — Registro de decisiones conservadas de V1

Se deja constancia explícita de lo que sobrevive de la versión anterior, para que no se pierda por efecto de la reducción.

| Decisión                                                                         | Estado                                                                                           |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Regla de bloqueo de infraestructura hasta 10.000 transacciones mensuales pagadas | **Conservada literal**, elevada a §1                                                             |
| Plan de cuentas de partida doble                                                 | **Migrada** al PRD MVP V9 §10 y a L3 §6                                                          |
| Motor de sorteo con entropía pública                                             | **Migrada y corregida**: se añade compromiso previo y baliza de ronda futura. MVP §12 y L3 V7 §5 |
| Separación de funciones en operaciones financieras                               | **Ampliada** a 21 subroles y 11 incompatibilidades en el MVP                                     |
| Playbooks de migración con retroceso por paso                                    | **Conservados y ampliados** con criterio de reversión en §5                                      |
| Gates legales multi-país                                                         | **Conservados y ampliados** en §7.2                                                              |
| Veinte fichas de construcción de servicios                                       | **Eliminadas**                                                                                   |
| Plataforma de eventos distribuida como contenido de construcción                 | **Eliminada**                                                                                    |
| Quince anexos sin contenido                                                      | **Eliminados**                                                                                   |

*LIBOX PRD BLUEPRINT ENTERPRISE V3 — Anexo direccional de nivel L2. No ejecutable. Gobernado por LBPF V3 conforme a R-02. Su contenido se activa únicamente al satisfacerse los umbrales y señales aquí definidos.*
