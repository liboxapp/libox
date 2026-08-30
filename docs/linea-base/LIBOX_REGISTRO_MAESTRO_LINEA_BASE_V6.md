# Índice de contenidos

# 0\. Propósito

Este registro responde una sola pregunta: **¿qué documento rige hoy?**

Existe porque el corpus de LIBOX acumula varias líneas documentales sucesivas, y porque ya ocurrió el fallo que este registro previene: un documento derogado permaneció accesible, se leyó como vigente y produjo un ciclo completo de análisis sobre una base inválida.

**Regla de uso:** si un documento no aparece en §1 como vigente, no rige. Ninguna excepción, ninguna interpretación.

| Campo         | Valor                                                                    |
| ------------- | ------------------------------------------------------------------------ |
| Documento     | LIBOX\_REGISTRO\_MAESTRO\_LINEA\_BASE\_V6                                |
| Versión       | V6                                                                       |
| Naturaleza    | Registro de control. No normativo sobre producto                         |
| Actualización | Obligatoria en cada emisión de versión de cualquier documento del corpus |
| Responsable   | Gobierno documental                                                      |

# 1\. Línea base vigente

| Nivel    | Documento                                   | Versión | Estado                                   | Gobierna                                                                                              |
| -------- | ------------------------------------------- | ------- | ---------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **L0**   | LIBOX Behavioral Product Framework (LBPF)   | **V3**  | Vigente · rector                         | Axiomas, **nueve derechos conductuales**, **trece principios**, zonas, límites, gobernanza            |
| **L1**   | Product Strategy                            | **V3**  | Vigente                                  | Tesis, **estructura competitiva real**, segmentos, comisión y su escala, costos, captación, hipótesis |
| **L2**   | PRD Blueprint MVP                           | **V9**  | Vigente · contrato de construcción       | Qué existe y bajo qué reglas de negocio                                                               |
| **L2**   | PRD Blueprint Enterprise                    | **V3**  | Vigente · direccional, **no ejecutable** | Cuándo y por qué evoluciona la arquitectura                                                           |
| **L3**   | Especificación Técnica                      | **V7**  | Vigente · base de implementación         | Cómo se implementa                                                                                    |
| **L3**   | **Matriz de Casos de Uso, Permisos y SLA**  | **V1**  | Vigente · referencia operativa           | Quién puede hacer qué, cuándo y en qué plazo                                                          |
| **L3**   | **Guía de Extensión y Puntos de Cambio**    | **V1**  | Vigente · referencia de ingeniería       | Dónde se toca cada cosa y qué nivel de cambio exige                                                   |
| **L4**   | Design System & Product Experience Standard | **V2**  | Vigente                                  | Cómo se ve, se entiende y se dice                                                                     |
| Auxiliar | Visual Identity Engineering Standard (VIES) | **V3**  | Vigente · arte **congelado**             | Identidad de marca                                                                                    |
| Plan     | Backlog MVP                                 | **V3**  | Vigente                                  | 136 historias · 936 SP · 30 sprints                                                                   |
| Registro | Auditoría Global de Coherencia              | **V1**  | Histórico de decisión                    | Los cuatro conflictos resueltos antes de emitir                                                       |
| Registro | **Auditoría de Coherencia Post-Emisión**    | **V1**  | Histórico de decisión                    | El desfase de L4 y el invariante huérfano, detectados por trazabilidad cruzada                        |
| Legal    | **Dossier Legal**                           | **V1**  | Vigente · insumo de encargo              | Tres estructuras vivas y 22 preguntas para la asesoría                                                |
| Registro | **Evaluación de Comité y Equipo Técnico**   | **V1**  | Histórico de decisión                    | Veredicto de viabilidad y las seis condiciones técnicas de entrega                                    |

## 1.0.1 Documentos de registro histórico

Tres documentos del corpus tienen naturaleza distinta: **registran un momento en el tiempo**, no una norma vigente.

| Documento                                    | Qué registra                                                  |
| -------------------------------------------- | ------------------------------------------------------------- |
| Auditoría Global de Coherencia V1            | Los cuatro conflictos de invariante resueltos antes de emitir |
| Auditoría de Coherencia Post-Emisión V1      | El desfase de L4 y el invariante huérfano                     |
| **Evaluación de Comité y Equipo Técnico V1** | Veredicto de viabilidad y condiciones de entrega              |

**Sus referencias a versiones anteriores son su contenido, no un defecto.** Una auditoría que dijera *“L4 V1 tiene un hueco”* y se reescribiera a *“L4 V2 tiene un hueco”* estaría falseando lo que ocurrió.

**Por eso** `verify_corpus.py` **los verifica en existencia e identidad, y no en referencias cruzadas.** Están declarados en la línea base para que su presencia sea legítima, y quedan fuera del control de versiones cruzadas porque su propósito lo exige.

## 1.1 Artefactos ejecutables

Un artefacto ejecutable es un archivo que el equipo consume directamente, no un documento que se lee.

| Artefacto                        | Versión | Estado                                                                                  | Origen        | Consumido por                                                |
| -------------------------------- | ------- | --------------------------------------------------------------------------------------- | ------------- | ------------------------------------------------------------ |
| `libox_schema_L3_V7.sql`         | V7      | **Vigente · 135 tablas, cero errores en PostgreSQL 16, 13 pruebas negativas superadas** | L3 V7 §1–§3   | Migraciones, pruebas de propiedad                            |
| `libox_openapi_L3_V7.yaml`       | V7      | **Vigente**                                                                             | L3 V7 §11     | Generación de tipos, pruebas de contrato, servidor simulado  |
| `libox-design-tokens-L4-V2.json` | V2      | **Vigente**                                                                             | L4 V1 Anexo A | Implementación de interfaz                                   |
| `LIBOX_BACKLOG_MVP_V3.xlsx`      | V3      | Vigente                                                                                 | Backlog V3    | Planificación y seguimiento                                  |
| `verify_corpus.py`               | **V1**  | **Vigente · ejecuta con cero fallos**                                                   | Regla CD-10   | **Verificación de coherencia en cada integración y emisión** |

## 1.2 Contenido que vive dentro de un documento y no como archivo

Declarado expresamente para que nadie los busque como ficheros sueltos.

| Contenido                                               | Ubicación                     |
| ------------------------------------------------------- | ----------------------------- |
| Máquina de estados implementable                        | L3 V7 §4                      |
| Especificación del motor de sorteo y vectores de prueba | L3 V7 §5                      |
| Plan de cuentas y transacciones canónicas               | L3 V7 §6                      |
| Matriz de control de acceso                             | L3 V7 §7                      |
| Catálogo de errores                                     | L3 V7 §8                      |
| Catálogo de eventos                                     | L3 V7 §9                      |
| Estructura de configuración por mercado                 | L3 V7 §10                     |
| Manual de redacción y textos aprobados                  | L4 V2 §7                      |
| **Casos de uso, permisos y plazos**                     | **Matriz de Casos de Uso V1** |
| **Puntos de cambio y niveles de extensión**             | **Guía de Extensión V1**      |

**Criterio.** Se emite como archivo lo que una herramienta consume: esquema, contratos y tokens. Lo demás permanece en su documento, porque duplicarlo en ficheros sueltos crea dos fuentes que divergen.

# 2\. Material histórico nulo

**Ninguno de estos documentos rige.** No se consultan, no se citan y no se usan como referencia. Aparecen aquí para ser reconocidos y descartados.

| Documento                                                | Motivo de nulidad                                                                                   |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `ALAZAR_PRD_TECH_ARCHITECTURE_MASTER_v8`                 | Línea de marca y producto anterior. Sustituido íntegramente                                         |
| Piezas de diseño ALAZAR (logo, home, panel)              | Marca anterior. Incumplen VIES y once normas del LBPF                                               |
| `LIBOX_Behavioral_Product_Framework_LBPF_v1`             | Sustituido por LBPF V2                                                                              |
| `LIBOX_PRD_BLUEPRINT_MVP_V1` y toda la línea V11 a V12.4 | Sustituidos. 41,5 % de texto repetido, 39 de 45 tablas sin columnas, 26 de 26 contratos sin esquema |
| `LIBOX_PRD_BLUEPRINT_ENTERPRISE_V1`                      | Sustituido. Contenía veinte fichas de microservicios que contradecían su propia regla de bloqueo    |
| **PRD MVP V2 a V8**                                      | Sustituidos por V9                                                                                  |
| PRD Enterprise V2                                        | Sustituido por V3                                                                                   |
| **Especificación Técnica L3 V1 a V6**                    | Sustituidas por V7                                                                                  |
| VIES V1 y V2                                             | Sustituidos por V3                                                                                  |
| `LIBOX_BACKLOG_-_MVP_v1.xlsx`                            | Sustituido por Backlog V2. Planificaba 191 SP contra un alcance real de 745                         |
| `libox-design-tokens-L4-V1.json`                         | Sustituido por V2                                                                                   |
| **Design System L4 V1**                                  | Sustituido por V2                                                                                   |
| **Registro Maestro V4**                                  | Sustituido por V5                                                                                   |
| **Product Strategy L1 V1 y V2**                          | Sustituidos por V3                                                                                  |
| **LBPF V1 y V2**                                         | Sustituidos por V3                                                                                  |
| **Backlog MVP v1 y V2**                                  | Sustituidos por V3. El v1 planificaba 191 SP contra un alcance real de 936                          |
| **Registro Maestro V1 a V5**                             | Sustituidos por V6                                                                                  |

**Acción operativa pendiente:** retirar el `ALAZAR_PRD_TECH_ARCHITECTURE_MASTER_v8` del repositorio de conocimiento activo. Mientras permanezca ahí se inyecta en cada sesión nueva como si fuera vigente, que es exactamente el fallo que este registro previene.

# 3\. Historial de versiones del corpus

| Documento                 | V1        | V2          | V3          | V4        | V5        | V6        | V7          | V8        | V9          |
| ------------------------- | --------- | ----------- | ----------- | --------- | --------- | --------- | ----------- | --------- | ----------- |
| LBPF                      | histórico | histórico   | **vigente** | —         | —         | —         | —           | —         | —           |
| PRD MVP                   | histórico | histórico   | histórico   | histórico | histórico | histórico | histórico   | histórico | **vigente** |
| PRD Enterprise            | histórico | histórico   | **vigente** | —         | —         | —         | —           | —         | —           |
| Especificación Técnica L3 | histórico | histórico   | histórico   | histórico | histórico | histórico | **vigente** | —         | —           |
| Design System L4          | histórico | **vigente** | —           | —         | —         | —         | —           | —         | —           |
| **Product Strategy L1**   | histórico | histórico   | **vigente** | —         | —         | —         | —           | —         | —           |
| VIES                      | histórico | histórico   | **vigente** | —         | —         | —         | —           | —         | —           |
| Backlog                   | histórico | histórico   | **vigente** | —         | —         | —         | —           | —         | —           |
| Tokens                    | histórico | **vigente** | —           | —         | —         | —         | —           | —         | —           |

## 3.1 Qué motivó cada emisión

| Emisión                       | Motivo                                                                                                          |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------- |
| PRD MVP V2                    | Devolver a L3 el contenido que el PRD absorbía y se degradó a plantilla                                         |
| PRD MVP V3                    | Cerrar los ocho tipos de sorteo, el impuesto incluido y la verificabilidad de la baliza                         |
| PRD MVP V5                    | Coherencia de entidades con L3: cuatro nombres divergentes entre capas\*\*                                      |
| L3 V2                         | Corregir defectos que impedían ejecutar el esquema y debilitaban la verificación                                |
| L3 V3                         | Referencia final corregida, correspondencia de agregados y emisión del OpenAPI                                  |
| **L3 V4**                     | **Tablas de la escala de comisión y su trabajo de recálculo**                                                   |
| L1 V1                         | Primera emisión: el nivel llevaba declarado desde el inicio sin documento                                       |
| **PRD MVP V6**                | **Dos regímenes de organizador y excepciones tipificadas de tasa**                                              |
| **L3 V5**                     | `tax_id` **opcional en persona natural,** `fee_exceptions` **y reglas de régimen**                              |
| **L1 V2**                     | **E4 por umbral en vez de por acuerdo; régimen de persona natural**                                             |
| Registro Maestro V2           | Actualización de la línea vigente                                                                               |
| **PRD MVP V7**                | **Techo de privilegio en el otorgamiento de subroles, límites de cuentas y objetivos de capacidad concurrente** |
| **L3 V6**                     | **Matriz de otorgamiento, suspensión distribuida, mínimo de administradores y proveedores en configuración**    |
| Registro Maestro V3           | Actualización de la línea vigente                                                                               |
| **LBPF V3**                   | **Regla de parte relacionada, límite de suscripción, BR-09 proporción razonable y P13 igualdad de vía**         |
| **L1 V3**                     | **Estructura competitiva real, cuña corregida, tres categorías de ingreso, rango de recaudación**               |
| **PRD MVP V8**                | **Las cuatro resoluciones de la auditoría más las 26 decisiones acumuladas**                                    |
| **L3 V7**                     | **Regímenes sin recaudación, control de funciones, códigos, suscripción y sus restricciones**                   |
| **Matriz de Casos de Uso V1** | **107 casos en 12 procesos, con las tres matrices transversales**                                               |
| **Guía de Extensión V1**      | **Mapa de puntos de cambio por función y nivel**                                                                |
| **Backlog V3**                | **936 SP, 30 sprints, R5 dividida y congelamiento de alcance**                                                  |
| Registro Maestro V4           | Cierre de la línea base congelada                                                                               |
| **PRD MVP V9**                | `INV-06-b` **al registro, secuenciación por régimen económico y gate del régimen promocional**                  |
| **Design System L4 V2**       | **P13, BR-09 y LINT-011; componentes de los regímenes sin recaudación; fichas de PU-11 y PU-12; textos nuevos** |
| Registro Maestro V5           | Cierre tras la auditoría post-emisión                                                                           |
| **Registro Maestro V6**       | **Alta de la Evaluación de Comité, categoría de registro histórico y regla CD-11**                              |
| Enterprise V2                 | Eliminar los Build Books prematuros y conservar la regla de bloqueo                                             |
| **Enterprise V3**             | **Actualización a la línea funcional vigente**                                                                  |
| VIES V2                       | Corregir iconos de aplicación y notificación, y precisar el alcance cromático                                   |
| **VIES V3**                   | **Contenido íntegro y eliminación del marcador** `NP-XX`                                                        |
| L4 V1                         | Primera emisión de un nivel declarado y vacío                                                                   |
| Tokens V2                     | Cerrar foco, elevación, esqueleto, cajón, aliado y nomenclatura por componente                                  |
| Backlog V2                    | Replanificación sobre el alcance real                                                                           |

# 4\. Política de control documental

| \#    | Regla                                                                                                                                                                               |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CD-01 | **No existen subversiones.** Todo cambio incrementa la versión completa de V(X) a V(X+1). No hay V2.1 ni V1.1                                                                       |
| CD-02 | Un número de versión **nunca se reutiliza**                                                                                                                                         |
| CD-03 | **Coherencia de identidad en cuatro lugares:** nombre de archivo, título interno, pie de página y campo de versión de la interfaz                                                   |
| CD-04 | Todo documento lleva **changelog interno** con la columna *decisión que invalida*                                                                                                   |
| CD-05 | El registro histórico **no se reescribe**: se normaliza la nomenclatura del documento anterior                                                                                      |
| CD-06 | **Regla de autonomía.** Una versión que derogue a la anterior no puede depender de ella para contenido normativo. Una derogación sin sustituto deja contenido sin documento vigente |
| CD-07 | Las observaciones y solicitudes de cambio se registran en **backlog de cambio**; no generan versión hasta ser aprobadas y aplicadas                                                 |
| CD-08 | La versión anterior se archiva **sin editar**                                                                                                                                       |
| CD-09 | **Este registro se actualiza en cada emisión.** Un registro maestro desactualizado es peor que su ausencia                                                                          |

**CD-06 nació de un fallo real:** VIES V2 declaraba a V1 *deprecado en su totalidad* y a la vez remitía a él en quince pasajes. El isotipo, la unidad X, el lockup, las variantes y la gobernanza quedaban sin documento vigente. VIES V3 lo corrige incorporando el contenido íntegro.

## 4.1 Regla CD-10 · Verificación programática obligatoria

> **Ninguna versión de ningún documento del corpus se emite sin que** `verify_corpus.py` **pase con cero fallos.**

Es regla, no recomendación, y tiene fundamento empírico: durante la construcción de esta línea base, **cuatro rondas sucesivas de hallazgos aparecieron únicamente por verificación programática**. Ninguno era visible leyendo, y varios los produjo el mismo equipo que había revisado el documento minutos antes.

| Ronda | Qué encontró el script                                   | Qué habría pasado sin él                                                 |
| ----- | -------------------------------------------------------- | ------------------------------------------------------------------------ |
| 1     | Un `CHECK` con `CURRENT_DATE`                            | **El esquema no se ejecutaba.** Descubierto en el sprint de migraciones  |
| 2     | Un `CHECK` de lógica de tres valores                     | Restricción que compilaba y **no protegía nada**                         |
| 3     | 53 referencias cruzadas obsoletas                        | Cuatro entidades divergentes entre capas, discutidas en el primer sprint |
| 4     | Desfase completo de L4 e invariante huérfano             | Superficies diseñadas sin reglas, y una protección declarada inexistente |
| 5     | Bloque de control de L4 aún en V1, tras haber emitido V2 | Un documento identificándose con la versión que deroga                   |

**La quinta ocurrió al ejecutar el propio verificador contra un corpus que este comité acababa de declarar limpio.** Ese es el argumento: la revisión humana de un corpus de esta escala tiene un límite estructural, y no es de diligencia.

### Los ocho controles

| Control                    | Qué verifica                                                  | Origen                                                              |
| -------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------- |
| `documento-ausente`        | Todo documento de la línea base existe                        | Preventivo                                                          |
| `referencias-obsoletas`    | Ninguna referencia cruzada apunta a una versión derogada      | 53 + 33 hallazgos reales                                            |
| `invariantes-huerfanos`    | Todo `INV` citado existe en el registro del PRD               | `INV-06-b` ausente                                                  |
| `reglas-huerfanas`         | Toda `RN` citada se declara en el PRD                         | Preventivo                                                          |
| `identidad-documental`     | CD-03: título, campo de versión y pie coinciden               | PRD arrastrando V7 dos versiones                                    |
| `cifras-compartidas`       | Las cifras propagadas son idénticas en todos los documentos   | Preventivo                                                          |
| `repeticion`               | Ningún párrafo largo se repite más de dos veces               | PRD V1 con 41,5 % de repetición                                     |
| `derogacion-sin-sustituto` | CD-06: ningún documento depende de la versión que deroga      | VIES V2 remitiendo 15 veces a V1                                    |
| `documento-no-declarado`   | **Todo documento presente en el corpus está declarado en §1** | **Evaluación de Comité V1, distribuida sin figurar en el Registro** |

### CD-11 · Todo documento distribuido está declarado

> **Un documento que existe, se distribuye y no figura en §1 crea una contradicción de gobierno.**

Por la regla de uso del propio Registro **no rige**, y a la vez está en manos del equipo como si rigiera. Ambas lecturas son razonables, y **esa ambigüedad es peor que su ausencia**.

**Origen.** Una revisión externa detectó que la Evaluación de Comité y Equipo Técnico V1 se emitió después del Registro V5 y nunca se incorporó. **El verificador no lo detectó porque comprobaba que todo documento declarado existiera, y no lo inverso.** El control faltaba, y esa asimetría es el tipo de hueco que solo aparece cuando alguien ajeno mira.

**Regla de emisión ampliada.** Toda emisión de un documento nuevo incluye, en el mismo acto: su alta en §1 del Registro, su alta en `BASELINE` del verificador, y su clasificación como norma vigente o registro histórico.

### Operación

**El script vive en el repositorio, junto al código.** Se ejecuta en cada integración y en cada emisión de versión. Su salida en modo JSON se integra al pipeline; un fallo detiene la integración igual que una prueba en rojo.

**La lista** `BASELINE` **del script es la única fuente de verdad de qué versión rige.** Actualizarla es parte del acto de emitir: un documento nuevo que no se registre allí no se verifica, y una versión anterior que permanezca hará fallar a todos los que la referencien correctamente.

**Los falsos positivos se corrigen en el script, no se ignoran.** Un verificador que el equipo aprende a saltarse deja de existir aunque siga ejecutándose. Cuando marque algo legítimo —una cita de changelog, una sección de historial—, la corrección es afinar el contexto reconocido.

## 4.2 Criterio de cierre de versión

Seis pruebas ejecutables por script. Ninguna versión se emite sin pasarlas:

1.  Ningún párrafo de más de 60 caracteres aparece más de dos veces
2.  Toda tabla declarada tiene columnas reales en el esquema
3.  Todo endpoint declarado tiene request y response tipados
4.  Todo anexo referenciado tiene contenido
5.  Toda `ERR_*` utilizada existe en el catálogo
6.  Prueba de compilación humana: alguien ajeno a la redacción implementa una historia leyendo solo el documento

**Añadidas en esta emisión:**

7.  **El esquema se ejecuta con cero errores** y sus restricciones se prueban contra casos que deben fallar
8.  **Toda entidad declarada en un agregado existe como tabla real** o está marcada como derivada
9.  **Ningún documento remite a una versión que él mismo deroga**

**10 · Ninguna decisión nueva contradice un invariante sin derogarlo expresamente.**

**11 · Todo invariante que no aplique a un régimen lo declara explícitamente.**

La séptima nació de ejecutar el esquema y encontrar un `CHECK` que compilaba y no protegía nada. La octava, de las cuatro entidades divergentes. La novena, de VIES. **Las dos últimas, de la auditoría global**: INV-06-a e INV-06-b e INV-23 fallaban al no declarar que no aplicaban a los regímenes sin recaudación.

## 4.3 Congelamiento de la línea base

> **La línea base queda congelada con las versiones de §1.**

El alcance creció un 26 % en la última revisión, de 745 a 936 puntos de historia, y **cada ampliación estuvo justificada**. Ese es precisamente el motivo del congelamiento: un proceso de revisión que encuentra huecos legítimos en cada pasada no se detiene por sí solo, porque siempre habrá una pregunta más que descubra algo cierto.

Todo hallazgo posterior entra en **backlog de cambio** y se emite en una versión futura, con el sistema ya en construcción.

**Único criterio para romper el congelamiento:** un hallazgo que impida construir, o que exponga a un riesgo legal o patrimonial. Todo lo demás espera.

# 5\. Estado de preparación

| Frente                          | Estado                                                                                        |
| ------------------------------- | --------------------------------------------------------------------------------------------- |
| Arquitectura documental         | **Completa y congelada.** Los cinco niveles con documento, más dos artefactos de referencia   |
| Base técnica ejecutable         | **Lista.** Esquema validado, contratos emitidos, tokens completos                             |
| Plan de construcción            | **Listo.** 136 historias, 936 SP, 30 sprints                                                  |
| Diseño de las 60 superficies    | **Pendiente.** 4 a 6 semanas, camino crítico paralelo, fuera de los 745 SP                    |
| Arte maestro de marca           | **Pendiente.** VIES V3 Anexo A lo exige                                                       |
| Dictámenes legales              | **Pendientes.** 12 materias, 2 a 4 meses, camino crítico externo                              |
| Proveedores de pago e identidad | **Pendiente contratación.** Declarados como `PENDING_CONTRACT` en la configuración de mercado |
| Go-live comercial               | **No autorizado** hasta cerrar dictámenes y ensayo con dinero real                            |

## 5.1 Los tres bloqueos externos

Ninguno depende del equipo de construcción, y los tres deben arrancar ya.

| \#   | Bloqueo                                                                                      | Duración         | Bloquea                                                          |
| ---- | -------------------------------------------------------------------------------------------- | ---------------- | ---------------------------------------------------------------- |
| B-01 | **Dictamen L-01: figura jurídica de LIBOX y necesidad de autorización propia como operador** | 2–4 meses        | Puesta en marcha. Es la pregunta que decide si la empresa existe |
| B-02 | Diseño de las 60 superficies                                                                 | 4–6 semanas      | Construcción de interfaz desde R1                                |
| B-03 | Arte maestro y planos de marca                                                               | Con el proveedor | Toda pieza visual oficial                                        |

*LIBOX Registro Maestro de Línea Base V6. Documento de control. Se actualiza en cada emisión de versión de cualquier documento del corpus.*
