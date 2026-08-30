# Índice de contenidos

# 0\. Control documental

**Documento:** LIBOX\_PRD\_BLUEPRINT\_MVP\_V9 **Versión:** V9 **Nivel:** L2 — Contrato de construcción **Reemplaza:** LIBOX PRD Blueprint MVP V8 (deprecado en su totalidad) **Alimentado por:** Product Strategy L1 V3 **Gobernado por:** LBPF V3 (nivel L0), por referencia normativa conforme a R-02 **Implementado por:** Especificación Técnica L3 V7 **Materializado por:** Design System L4 V2 **Estado:** vigente

**Nota de versionado.** La política documental de LIBOX no admite subversiones: todo cambio incrementa la versión completa de V(X) a V(X+1). Por eso esta corrección no es una V2.1.

## 0.1 Qué es y qué no es este documento

Este PRD **declara qué existe y bajo qué reglas de negocio**. No contiene esquema de base de datos, ni contratos de API tipados, ni implementación de algoritmos: esos artefactos viven en el nivel L3 y este documento los referencia.

La versión V1 absorbió contenido de L3 —DDL, contratos, clases— y al no caber en el formato se degradó a plantilla. La corrección estructural de V2 es devolver cada contenido a su nivel.

| Contenido                                             | Nivel | Artefacto                  |
| ----------------------------------------------------- | ----- | -------------------------- |
| Qué entidades existen y qué invariantes cumplen       | L2    | Este documento, §3         |
| Columnas, tipos, índices, restricciones               | L3    | `libox_schema_L3_V7.sql`   |
| Qué endpoints existen y qué reglas aplican            | L2    | Este documento, §35        |
| Request y response tipados, códigos, ejemplos         | L3    | `libox_openapi_L3_V7.yaml` |
| Qué estados existen y qué transiciones son legales    | L2    | Este documento, §4         |
| Implementación de la máquina de estados               | L3    | `raffle-fsm.md`            |
| Que el sorteo es verificable y qué garantiza          | L2    | Este documento, §12        |
| Algoritmo, serialización canónica, vectores de prueba | L3    | `draw-engine-spec.md`      |

## 0.2 Changelog

### Cambios de la versión V9

Emitida tras la auditoría de coherencia posterior a la emisión, que verificó por trazabilidad cruzada si lo decidido llegó completo a todos los niveles.

| Versión | Sección  | Qué cambió                                                                         | Por qué                                                                                                                                                                                                             | Decisión que invalida    |
| ------- | -------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| V9      | Anexo D  | `INV-06-b` **incorporado al registro de invariantes**                              | Se citaba en el cuerpo y en L3, y faltaba en el registro. **Quien consultara solo el anexo concluiría que la protección de quien participa gratis no existe**                                                       | Corrige el Anexo D de V8 |
| V9      | §5.7     | **Secuenciación de encendido por régimen económico**, no solo por tipo y categoría | Los cinco regímenes coexistían desde el primer día. Cada uno añade cadena de cierre, modelo de garantía y tratamiento contable propios: **con equipo reducido, cada régimen multiplica la superficie de operación** | Amplía                   |
| V9      | §5.6.1   | **Gate de habilitación del régimen promocional**                                   | Los demás regímenes tenían gate —capacidad, reputación, garantía—. El promocional entraba solo por plan contratado                                                                                                  | Amplía                   |
| V9      | Cabecera | Título interno corregido                                                           | Arrastraba V7 desde dos versiones atrás. **Incumplía CD-03: coherencia de identidad en cuatro lugares**                                                                                                             | Corrige                  |

### Cambios de la versión V8

Emitida tras la auditoría global de coherencia, que detectó cuatro conflictos entre las decisiones acumuladas y los invariantes vigentes. Las resoluciones se incorporan de forma expresa.

| Versión | Sección | Qué cambió                                                                                                             | Por qué                                                                                                                    | Decisión que invalida                 |
| ------- | ------- | ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| V8      | §1.2    | **Régimen de parte relacionada.** Una entidad vinculada organiza como cliente, con tarifas publicadas y trato idéntico | LIBOX necesita organizar sorteos promocionales propios; hacerlo directamente vulneraría INV-02 e INV-04                    | Amplía; evita derogarlos              |
| V8      | §1.3.2  | **Rango de recaudación** de 1,25× a 4,0× del valor verificado, con cuatro zonas                                        | BR-09 del rector. El suelo financia el reembolso; el techo protege al participante                                         | Amplía                                |
| V8      | §1.5    | **INV-06 desdoblado** en régimen con y sin recaudación                                                                 | *Ningún participante pierde su aporte* es inaplicable donde no hay aporte, y dejaba sin cobertura a quien participa gratis | **Deroga INV-06 de V7**               |
| V8      | §5.5    | **Sorteo con entrada gratuita**, tres orígenes de premio, sujeto a P13                                                 | Canal de adquisición sin costo y posible pieza de la estructura legal                                                      | Amplía                                |
| V8      | §5.6    | **Régimen promocional**: sin recaudación, sin liquidación, con cadena de conformidad                                   | Sin venta de tickets no hay comisión ni gates aplicables                                                                   | Amplía; INV-23 declarado no aplicable |
| V8      | §6.5    | **Categorías registrables prohibidas** en régimen promocional y en sorteos gratuitos, salvo custodia efectiva          | El proceso de siete etapas se apoya en la retención; sin fondos, el ganador queda desprotegido                             | Amplía                                |
| V8      | §2.8    | **Interruptor global de plataforma**, jerarquía restrictiva de tres capas                                              | Existía control por cliente y por mercado; faltaba la plataforma completa                                                  | Amplía                                |
| V8      | §2.9    | **Escalada de apagado por alcance** y **degradación controlada según motivo**                                          | Sin regla de vuelo habría que decidir caso por caso sobre sorteos ya vendidos                                              | Amplía                                |
| V8      | §2.10   | **Ventanas operativas** por función y mercado, con diferimiento en lugar de fallo                                      | Permite acompañar las ejecuciones con equipo reducido                                                                      | Amplía                                |
| V8      | §2.11   | **Panel de funciones por subrol** y **alta de cuenta interna**                                                         | Cada rol debe ver qué domina, su estado, y si puede actuar o solo escalar                                                  | Amplía                                |
| V8      | §26     | **Códigos de campaña y de atribución**, marca compartida y **LIBOX Club apagado**                                      | Instrumentan la adquisición por comunidad y la medición de H-07                                                            | Amplía                                |
| V8      | §27     | **PU-11 directorio y PU-12 perfil público de organizador**                                                             | Sin ellos el participante ve oportunidades sueltas y el descubrimiento cruzado no arranca                                  | Amplía                                |
| V8      | §31     | **Auditoría de consulta** de rol interno a datos de terceros                                                           | Se registraba toda mutación; consultar datos ajenos no dejaba rastro                                                       | Amplía                                |

### Cambios de la versión V7

| Versión | Sección | Qué cambió                                                                                                                           | Por qué                                                                                                                                                                                                            | Decisión que invalida |
| ------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------- |
| V7      | §2.6.1  | **Matriz de otorgamiento de subroles con techo de privilegio.** `SUPPORT_SUPERVISOR` puede crear y suspender únicamente `SUPPORT_L1` | La creación de usuarios era exclusiva de `ADMIN_SUPER`: punto único de fallo con un equipo de cuatro y cuello administrativo al crecer soporte                                                                     | Amplía                |
| V7      | §2.6.1  | **Asimetría de otorgamiento y revocación.** Conceder es lento y concentrado; suspender es inmediato y distribuido                    | Conceder acceso indebido es un riesgo que se materializa con el tiempo; **mantener acceso indebido es un riesgo que se materializa ahora**                                                                         | Amplía                |
| V7      | §2.6.2  | **Alta del primer administrador y regla de dos titulares mínimos**                                                                   | No existía ruta de arranque ni protección contra el bloqueo total si se pierde el único `ADMIN_SUPER`                                                                                                              | Amplía                |
| V7      | §2.7    | **Límites de usuarios y de organizadores activos**                                                                                   | No existía ningún tope declarado. El límite real es operativo y no técnico, y conviene que sea explícito                                                                                                           | Amplía                |
| V7      | §32.4   | **Objetivos de capacidad concurrente**                                                                                               | Había objetivos de latencia y disponibilidad, y **ningún número de sorteos simultáneos, órdenes por segundo ni tickets por minuto**. Se sabía que el sistema no se corrompe; no a partir de qué volumen se degrada | Amplía                |
| V7      | §24.2   | Proveedor concreto de cada adaptador **en la configuración por mercado**                                                             | Los adaptadores estaban definidos sin proveedor nombrado. Correcto en el documento normativo, insuficiente para el equipo que debe integrar                                                                        | Amplía                |

### Cambios de la versión V6

| Versión | Sección    | Qué cambió                                                                                                     | Por qué                                                                                                                                                                     | Decisión que invalida                  |
| ------- | ---------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| V6      | §2.3, §3.1 | **Dos regímenes de organizador: persona natural y persona jurídica**, con acreditación diferenciada            | El modelo se diseñó sobre el comercio formal. El particular estaba declarado como segmento y no modelado: el identificador tributario obligatorio **impedía darlo de alta** | Amplía                                 |
| V6      | §2.3       | Identificador tributario **exigible solo a persona jurídica**                                                  | En el mercado objetivo, muchas personas naturales no disponen de él. La restricción bloqueaba un segmento declarado en L1 §3.1                                              | Deroga la obligatoriedad general de V5 |
| V6      | §1.3.1     | **E4 deja de ser “por acuerdo”.** Se sustituye por **excepciones tipificadas** con criterio objetivo publicado | *Por acuerdo* contradecía RN-01-quater y abría la puerta que §5.6 de L1 cierra. Una ambigüedad en materia de precio se convierte en hecho consumado                         | Deroga la redacción de E4 en V5        |
| V6      | §1.3.1     | Regla **RN-01-nonies**: toda excepción de tasa es tipificada, temporal, con segunda firma y reportable         | Sin criterio objetivo, la excepción es tarifa negociada con otro nombre                                                                                                     | Amplía                                 |
| V6      | §9         | Precisión sobre emisión de comprobante según tipo de organizador                                               | Un particular sin identificador tributario no puede emitir. Cambia la pregunta L-05                                                                                         | Amplía                                 |

### Cambios de la versión V5

| Versión | Sección | Qué cambió                                                                                                                                         | Por qué                                                                                                                                       | Decisión que invalida                          |
| ------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| V5      | §1.3    | **Escala de progresión de comisión.** El 20 % pasa de tasa permanente a **tasa base y techo**, con niveles E0 a E4 por volumen liquidado acumulado | Decisión estratégica de L1 V1 §5. La tasa plana no tenía ruta de evolución y anclaba el precio sin recompensar la permanencia del organizador | Amplía. No deroga el 20 %, lo sitúa como techo |
| V5      | §1.3    | Siete reglas de la escala, con la tasa congelada por sorteo al publicar                                                                            | Sin ellas, una tasa variable se convierte en tarifa negociada, incompatible con el marco conductual                                           | Amplía                                         |
| V5      | §1.2    | Precisión de INV-01: la comisión es idéntica **sea cual sea el resultado**, y esa es la neutralidad que se protege                                 | La redacción podía leerse como uniformidad entre organizadores. La escala varía por volumen, nunca por quién gana                             | Precisa INV-01                                 |
| V5      | §24.2   | `fee_schedule` incorporado a la configuración por mercado                                                                                          | Los umbrales son parámetro de negocio calibrable, no constante de código                                                                      | Amplía                                         |

### Cambios de la versión V4

| Versión | Sección | Qué cambió                                                                               | Por qué                                                                                                                                                                                                                                    | Decisión que invalida            |
| ------- | ------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------- |
| V4      | §3.1    | `processed_webhooks` **renombrada a** `processed_psp_events`                             | El nombre del agregado divergía del de la tabla real. Cuatro nombres divergentes entre L2 y L3 producen cuatro discusiones en el primer sprint de migraciones                                                                              | Deroga la denominación de V3     |
| V4      | §3.1    | `sessions` **sustituida por** `refresh_tokens`                                           | La sesión no es una entidad persistida: se materializa en credenciales de vida corta y testigos de renovación rotatorios                                                                                                                   | Deroga la entidad `sessions`     |
| V4      | §3.1    | `order_items` **derogada.** Se declara la regla **una orden, un sorteo**                 | No era una divergencia de nombre sino una decisión sin tomar. Una orden multi-sorteo rompe el desglose de comisión congelado, los gates de liquidación y la atribución de tickets, porque la orden tiene un solo sorteo y un solo desglose | Deroga la entidad `order_items`  |
| V4      | §3.1    | `ticket_pools` **derogada.** El pool se deriva de los tickets emitidos                   | Entidad heredada del modelo anterior. La serialización canónica ya opera sobre los tickets con estado emitido                                                                                                                              | Deroga la entidad `ticket_pools` |
| V4      | §3.1    | Nueva regla: **todo agregado declarado tiene tabla real o se marca como derivado**       | Criterio de cierre de §0.3 punto 2, aplicado a los agregados y no solo a las tablas                                                                                                                                                        | Amplía                           |
| V4      | §35     | `libox_openapi_L3_V7.yaml` **emitido como artefacto físico**                             | El Anexo A lo declara bloqueante de toda la construcción del cliente, y no existía como archivo                                                                                                                                            | Amplía                           |
| V4      | Todo    | Nomenclatura de versiones normalizada sin dígito menor, también en el registro histórico | La política documental no admite subversiones. El registro no se reescribe: se normaliza el nombre                                                                                                                                         | Amplía                           |

### Cambios de la versión V3

| Versión | Sección    | Qué cambió                                                                                      | Por qué                                                                                                                                         | Decisión que invalida                                   |
| ------- | ---------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| V3      | §4.1, §4.2 | `MILESTONE_REACHED` **incorporado a la máquina de estados** con sus dos transiciones            | T4 declaraba un estado que no existía en la lista de estados, ni en las transiciones, ni en el esquema. Un sorteo de tipo T4 no era construible | Corrige §4 de V2                                        |
| V3      | §5.2       | **Resuelta la contradicción de T2**                                                             | §5.2 disparaba al vencer el plazo y §4.2 al alcanzar el umbral. Eran dos productos distintos descritos como uno                                 | Deroga la definición de T2 de V2                        |
| V3      | §5.2       | **T4 y T7 completados**: hitos declarados e inmutables, y ediciones independientes con su serie | Ambos estaban enunciados sin soporte de datos ni reglas                                                                                         | Amplía                                                  |
| V3      | §5.2       | **Duración máxima de T5** incorporada a la configuración por mercado                            | El tipo declaraba un límite que no existía en ninguna parte                                                                                     | Amplía                                                  |
| V3      | §5.4       | **Semilla obligatoria de los ocho tipos** como requisito de aceptación                          | Sin ella, “T1–T8 son configuración sobre una FSM única” era afirmación y no hecho                                                               | Amplía                                                  |
| V3      | §9.2       | **Impuesto incluido en la comisión, con fórmula e invariantes**                                 | Sin la regla, el neto del organizador y el margen quedaban indeterminados                                                                       | Amplía                                                  |
| V3      | §12.2      | **Propiedad intrínseca de la ronda de baliza** en compromiso y verificación                     | La verificación se apoyaba en una marca temporal escrita por LIBOX: comprobaba consistencia aritmética, no honestidad                           | Refuerza INV-18; deroga la verificación de baliza de V2 |
| V3      | §24.2      | Parámetros por tipo de sorteo en la configuración por mercado                                   | Los límites de tipo estaban dispersos o ausentes                                                                                                | Amplía                                                  |
| V3      | Todo       | Nomenclatura normalizada sin dígito menor                                                       | La política documental no admite subversiones                                                                                                   | Amplía                                                  |

### Cambios de la versión V2

| Versión | Fecha      | Sección         | Qué cambió                                                                              | Por qué                                                                                                                   | Decisión que invalida                           |
| ------- | ---------- | --------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| V2      | 2026-08-06 | §7, §8 V1       | Esquema de datos y contratos de API migrados a L3                                       | El PRD absorbía L3 y se degradó a plantilla: 39 de 45 tablas sin columnas, 26 de 26 contratos sin esquema                 | Deroga §7 y §8 de V1                            |
| V2      | 2026-08-06 | §9 V1           | Eliminada                                                                               | Los 15 “Core Engine Books” eran una sola clase copiada quince veces; `DrawEngine` era idéntico a `NotificationEngine`     | Deroga §9 de V1 completa                        |
| V2      | 2026-08-06 | §6 V1           | Reescrita                                                                               | La columna de tablas por módulo estaba desplazada: el dominio Raffle aparecía asignado a `devices` y `verification_cases` | Deroga §6 de V1                                 |
| V2      | 2026-08-06 | §3 V1           | T1–T8 consolidados en una FSM única con los tipos como configuración                    | V1 declaraba ocho listas de estados sin intersección; no existía máquina de estados de `raffles`                          | Deroga §3 de V1                                 |
| V2      | 2026-08-06 | §2 V1           | 54 fichas de pantalla reescritas sin los siete campos idénticos repetidos               | Cada ficha tenía 6 campos variables y 7 clonados                                                                          | Deroga §2 de V1                                 |
| V2      | 2026-08-06 | Anexos          | 14 de 16 anexos vacíos: escritos o eliminados                                           | Un anexo referenciado sin contenido es peor que su ausencia                                                               | Deroga los anexos vacíos de V1                  |
| V2      | 2026-08-06 | §2 nueva        | SUPPORT gana atestación de hechos operativos; sigue sin tocar dinero, ledger ni ganador | Decisión D-01.1                                                                                                           | Modifica el invariante de V1 §1, §2.4, §5 y §11 |
| V2      | 2026-08-06 | §7 nueva        | Gate obligatorio de verificación de valor del premio                                    | Decisión D-01.4                                                                                                           | Amplía                                          |
| V2      | 2026-08-06 | §2 nueva        | 21 subroles con 11 incompatibilidades duras                                             | Decisiones D-01.11, D-02.7, D-03.16                                                                                       | Amplía                                          |
| V2      | 2026-08-06 | §10 nueva       | Ledger de partida doble con plan de cuentas, migrado desde Enterprise                   | El MVP declaraba tablas de ledger sin plan de cuentas ni función de asiento                                               | Amplía                                          |
| V2      | 2026-08-06 | §12 nueva       | Draw Engine con commit-reveal y baliza pública futura                                   | En V1 la palabra `seed` no aparecía en 176.365 caracteres; el algoritmo del Enterprise permitía reintento                 | Amplía y corrige Enterprise §5                  |
| V2      | 2026-08-06 | §13–§16 nuevas  | Sala de Resolución, disputas simétricas, liquidación con gates, no entrega y re-sorteo  | Decisiones D-01 y D-04                                                                                                    | Amplía                                          |
| V2      | 2026-08-06 | §17–§19 nuevas  | Identidad con prueba de vida, unicidad, juego responsable y prevención financiera       | Decisión D-03                                                                                                             | Amplía                                          |
| V2      | 2026-08-06 | §22, §23 nuevas | Analítica conductual, seis KPI activos y Panel Único de Alarmas                         | Decisión D-02                                                                                                             | Amplía                                          |
| V2      | 2026-08-06 | §24, §25 nuevas | `market_config` versionado y kill switch por mercado                                    | Decisión D-05                                                                                                             | Amplía                                          |
| V2      | 2026-08-06 | §26 nueva       | Módulo Growth & Commercial                                                              | Decisión D-06                                                                                                             | Amplía                                          |
| V2      | 2026-08-06 | §33             | Web responsive universal + PWA; se elimina “USER Mobile App Book”                       | Decisión D-05.1                                                                                                           | Deroga la denominación de app nativa en el MVP  |

## 0.3 Criterio de cierre de versión

Sustituye a la autoevaluación con umbral 9,5 de V1, que otorgó 9,6 a quince copias de la misma clase y a veintiséis contratos sin esquema. Un documento no se cierra sin pasar seis pruebas ejecutables por script:

1.  Ningún párrafo de más de 60 caracteres aparece más de dos veces.
2.  Toda tabla declarada tiene columnas reales en `libox_schema_L3_V7.sql`.
3.  Todo endpoint declarado tiene request y response tipados en `libox_openapi_L3_V7.yaml`.
4.  Todo anexo referenciado tiene contenido.
5.  Toda `ERR_*` utilizada existe en el catálogo de errores.
6.  Prueba de compilación humana: un desarrollador ajeno a la redacción implementa una historia leyendo solo el PRD, sin preguntar.

## 0.4 Convenciones

  - **Zona horaria:** `America/Lima` para el mercado PE. Toda fecha y plazo se calcula y se muestra en la zona del mercado del sorteo.
  - **Moneda:** montos como entero de la unidad mínima, siempre acompañados del código ISO. Nunca punto flotante.
  - **Identificadores:** UUID v4 para entidades; `raffle_code` legible con formato `LBX-YYYYMM-XXXXX` para uso humano.
  - **Trazabilidad:** todo cambio de estado propaga `trace_id`.
  - **Nomenclatura de reglas:** `RN-nn` regla de negocio, `INV-nn` invariante, `ERR_*` error.

# 1\. Visión, modelo de negocio y posición estructural

## 1.1 Qué es LIBOX

LIBOX es infraestructura de confianza para sorteos. Conecta a organizadores que disponen de un bien o servicio de valor con participantes que adquieren tickets, y garantiza que el proceso completo —publicación, venta, sorteo, entrega y liquidación— sea verificable, trazable y financieramente seguro para las tres partes.

El valor que LIBOX aporta no es el sorteo: es que el sorteo sea **demostrable**. Un organizador puede sortear por su cuenta; lo que no puede es probar que no lo amañó, ni garantizar al comprador que recibirá su dinero de vuelta si el premio no existe.

## 1.2 Neutralidad económica frente al azar

> **LIBOX no lucra con el azar. Percibe una comisión por el uso de su sistema de sorteos.**

Condiciones que el producto debe sostener permanentemente (LBPF V3 §13):

| \#     | Condición                                                                                                                                                                   |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| INV-01 | La comisión **nunca depende del resultado del sorteo**. Es idéntica gane quien gane. Puede variar por organizador según la escala publicada de §1.3, jamás por el desenlace |
| INV-02 | LIBOX no participa del premio ni retiene parte de él                                                                                                                        |
| INV-03 | LIBOX no ofrece instrumento, producto ni mecanismo cuyo valor dependa de quién resulte ganador                                                                              |
| INV-04 | LIBOX no adquiere participaciones en las oportunidades que aloja                                                                                                            |
| INV-05 | Los ingresos de LIBOX son indiferentes a la identidad del ganador                                                                                                           |

Toda propuesta que comprometa estas condiciones exige BDR de clase B4 y revisión legal previa.

### 1.2.1 Régimen de parte relacionada

LIBOX organiza oportunidades propias —sorteos promocionales de activación, campañas conjuntas, premios de adquisición— **sin vulnerar la neutralidad y sin abrir excepción a ella** (LBPF V3 §13.1).

> **Una entidad vinculada a LIBOX opera exclusivamente en condición de cliente.**

| \#                  | Regla                                                                                                                             |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **RN-02-bis**       | Paga las **tarifas publicadas**. Sin tarifa especial ni condición no disponible para cualquier otro organizador                   |
| **RN-02-ter**       | Pasa **todos los gates**: valoración de premio, gate legal, atestación de entrega, resolución y controversias                     |
| **RN-02-quater**    | Se marca como **parte relacionada** en el registro contable y en auditoría                                                        |
| **INV-39**          | **El sistema la trata igual que a cualquier organizador.** Ninguna ruta de código, configuración ni permiso admite trato distinto |
| **RN-02-quinquies** | No accede a datos de otros organizadores ni a información no disponible para el resto                                             |

**INV-39 es la condición que hace creíble la estructura.** Una separación societaria que dentro del sistema se traduzca en privilegios no es separación.

## 1.3 Modelo de comisión

Comisión **all-inclusive del 20 %** sobre la recaudación bruta. El organizador conoce su monto neto antes de publicar y no existen descuentos posteriores no declarados.

    gross_required   = redondeo_superior( target_net / 0.80 , multiplo_mercado )
    libox_fee        = gross_required × 0.20
    client_net       = gross_required − libox_fee
    ticket_price     = definido por el organizador dentro de rango del mercado
    total_tickets    = techo( gross_required / ticket_price )

  - `multiplo_mercado` proviene de `market_config` (§24). En PE es 10. No es constante de código.
  - `client_net` resultante es siempre **igual o superior** al `target_net` solicitado, por efecto del redondeo superior.
  - El desglose se congela en cada orden para inmutabilidad histórica, con invariante `client_net + libox_fee = gross`.

## 1.3.1 Escala de progresión de la comisión

**El 20 % es la tasa base y el techo, no el precio permanente.** A partir del cuarto trimestre de operación se habilita una escala por volumen liquidado acumulado del organizador en 12 meses móviles.

| Nivel           | Tasa       | Puntos básicos |
| --------------- | ---------- | -------------- |
| E0 Inicial      | **20,0 %** | 2000           |
| E1 Establecido  | 18,0 %     | 1800           |
| E2 Recurrente   | 16,0 %     | 1600           |
| E3 Volumen      | 14,0 %     | 1400           |
| E4 Volumen alto | 12,0 %     | 1200           |

Los umbrales provienen de `market_config` y se calibran con el costo unitario real (L1 V1 §6). **No son constantes de código.**

| \#                  | Regla                                                                                                                                                                                                                                                      |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **RN-01-bis**       | La tasa se **congela en el sorteo al publicarlo**. Un cambio de nivel no altera sorteos ya publicados ni órdenes ya emitidas                                                                                                                               |
| **RN-01-ter**       | La escala es **pública**: umbrales, tasas y método de cálculo, accesibles sin registro. Una tarifa negociada en privado es incompatible con el marco conductual                                                                                            |
| **RN-01-quater**    | El nivel se gana por **volumen liquidado, nunca por negociación**. No existe tarifa acordada caso por caso                                                                                                                                                 |
| **RN-01-quinquies** | Se asciende por volumen; se desciende **solo por incumplimiento grave**, con motivo registrado y notificación                                                                                                                                              |
| **RN-01-sexies**    | El volumen se mide sobre lo **liquidado**, no sobre lo recaudado. Un organizador que recauda y no entrega no progresa                                                                                                                                      |
| **RN-01-septies**   | **Ningún nivel exime del gate de valoración de premio ni de ningún control** (INV-28). El precio no compra excepciones                                                                                                                                     |
| **RN-01-octies**    | La tasa **nunca depende del resultado del sorteo** (INV-01)                                                                                                                                                                                                |
| **RN-01-nonies**    | **No existe tasa negociada.** Toda tasa por debajo de la escala corresponde a una **excepción tipificada** con criterio objetivo publicado, vigencia limitada, segunda firma de otra persona natural, motivo registrado y reporte periódico a la dirección |

### Excepciones tipificadas

La escala se gana por volumen. Fuera de ella existen **categorías de excepción con nombre y criterio objetivo**, publicadas como la propia escala. Ninguna se acuerda caso por caso.

| Categoría                | Criterio objetivo                                                                      | Vigencia             | Aprueba                                  |
| ------------------------ | -------------------------------------------------------------------------------------- | -------------------- | ---------------------------------------- |
| `ANCHOR_LAUNCH`          | Organizador de los primeros N sorteos de un mercado, con premio verificado y aprobado  | 12 meses o N sorteos | `ADMIN_SUPER` + segunda firma            |
| `VERIFIED_NONPROFIT`     | Entidad sin fin de lucro acreditada documentalmente, con destino de fondos verificable | Por sorteo           | `ADMIN_LEGAL_COMPLIANCE` + segunda firma |
| `INSTITUTIONAL_ALLIANCE` | Acuerdo institucional con condiciones publicadas                                       | Vigencia del acuerdo | `ADMIN_SUPER` + segunda firma            |

**Diferencia operativa.** *Existe una categoría de organizador ancla con condiciones publicadas* es defendible ante cualquier organizador y ante una autoridad de consumo. *Con este cliente acordamos una tasa* no lo es, y además destruye el precio uniforme como instrumento de medición.

**INV-37 — Ninguna excepción supera el techo.** Ninguna categoría, acuerdo ni contrato puede fijar una tasa **superior** a la base del mercado. Se impone en el esquema, no en el procedimiento.

**Fundamento del congelamiento.** El desglose de cada orden es inmutable y cumple `client_net + libox_fee = gross`. Si la tasa cambiara sobre un sorteo en venta, dos órdenes del mismo sorteo tendrían desgloses distintos y el neto del organizador dejaría de ser conocible antes de publicar, que es precisamente la promesa del modelo all-inclusive.

**Sin cambio de esquema.** `raffles.libox_fee_bp` ya es un valor por sorteo con 2000 por defecto, y la fórmula de §1.3 ya usa la tasa del sorteo y no una constante.

## 1.3.2 Rango de recaudación

Implementa **BR-09** del rector. La recaudación bruta guarda relación acotada con el **valor verificado del premio**, no con el declarado.

| Múltiplo       | Neto del organizador     | Tratamiento                                            |
| -------------- | ------------------------ | ------------------------------------------------------ |
| Bajo **1,25×** | —                        | **Bloqueado**                                          |
| 1,25× a 2,5×   | 1,00× a 2,00× del premio | Habitual, sin fricción                                 |
| 2,5× a 4,0×    | 2,00× a 3,20×            | Permitido, con aviso al organizador y marca en el gate |
| Sobre **4,0×** | —                        | **Aprobación de ADMIN con segunda firma y motivo**     |

| \#                  | Regla                                                                                                                                |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **INV-40**          | Ninguna oportunidad se publica con múltiplo inferior al suelo del mercado                                                            |
| **INV-41**          | Ninguna oportunidad supera el techo sin aprobación registrada con doble firma                                                        |
| **RN-01-decies**    | El múltiplo se calcula sobre el **valor aprobado en el gate**, nunca sobre el declarado                                              |
| **RN-01-undecies**  | El múltiplo **no es información pública**. Visible para el organizador en su simulador y para LIBOX en el gate y el panel de alarmas |
| **RN-01-duodecies** | El simulador muestra el múltiplo resultante y una **recomendación con su fundamento** antes de enviar a revisión                     |
| **RN-01-terdecies** | La zona de 2,5× a 4,0× genera **alerta informativa acumulable** por organizador                                                      |

**Fundamento del suelo.** En 1,25× el organizador recupera exactamente el valor del premio; por debajo pierde frente a vender el bien, y **la recaudación deja de cubrir el reembolso**, que es la garantía de §1.5.

**Fundamento del techo.** Sobre 4,0× el participante recibe menos de veinticinco céntimos de valor esperado por cada sol.

**Fundamento de la no divulgación.** La recaudación del organizador es su información comercial, como el margen de cualquier comercio, y **no es condición de la compra**. Lo que sí es obligatorio y público —precio, probabilidad, tamaño del pool y valor verificado del premio— basta para decidir.

**RN-01-terdecies existe por un motivo concreto:** un organizador que sistemáticamente recauda cerca del techo es un patrón que conviene ver antes de que sean diez organizadores.

Los cuatro umbrales provienen de `market_config` y se calibran con datos.

**RN-01.** El precio del ticket es único e inmutable para todos los participantes de un sorteo. Las promociones se instrumentan como crédito aplicable, nunca como precio diferenciado (LBPF V3 §12.2).

## 1.4 Trust Loop

    Identidad verificada → Organizador acreditado → Premio verificado → Gate legal
       → Publicación → Venta → Congelamiento del pool → Sorteo verificable
       → Sala de Resolución → Entrega atestada → Gates de liquidación → Pago y asientos
       → Auditoría

Cada eslabón produce evidencia consultable. Ningún eslabón puede saltarse.

## 1.5 Garantía patrimonial

LIBOX retiene el 100 % de la recaudación desde la venta hasta la verificación de la entrega. Dado que el dimensionamiento parte del valor del premio, la suma retenida excede estructuralmente ese valor.

> **INV-06-a — En oportunidades con recaudación, ningún participante pierde su aporte en ningún escenario de fallo.** El reembolso íntegro está financiado por la recaudación retenida.
> 
> **INV-06-b — En oportunidades sin recaudación no hay aporte que devolver, y la protección se traslada al premio.** Verificación de valor igual de estricta, **garantía sustitutiva como condición de publicación**, y penalización reputacional agravada por incumplimiento.

**Por qué se desdobla.** El invariante original era inaplicable donde no hay pago, y esa laguna dejaba sin cobertura precisamente a quien participa gratis: **quien pagó recupera su dinero; quien no pagó solo se lleva la decepción, y llegó por la marca LIBOX.**

**RN-02-sexies — La garantía sustitutiva es condición de publicación**, no recomendación. En una oportunidad sin recaudación no existe palanca financiera sobre la entrega: sin dinero retenido, la garantía es lo único que queda.

**RN-02.** Ninguna suspensión operativa, decisión de riesgo, análisis de cumplimiento o cierre de mercado puede impedir que una persona reclame su premio, reciba su reembolso o disponga de su saldo.

**Límite declarado:** la custodia protege contra el incumplimiento; **no protege contra la sobrevaloración del premio**. Contra la sobrevaloración protege únicamente el gate de §7.

## 1.6 Alcance del MVP

| Dentro                                              | Fuera (declarado y deshabilitado por configuración) |
| --------------------------------------------------- | --------------------------------------------------- |
| Tipos de sorteo T1–T8 según §5                      | —                                                   |
| Categorías de premio P-A, P-B, P-C1, P-C2, P-D, P-E | P-F efectivo y equivalentes                         |
| Mercado PE / moneda PEN                             | Otros mercados (arquitectura lista)                 |
| Web responsive universal + PWA                      | Apps nativas iOS/Android                            |
| Asignación automática de número de ticket           | Selección manual de número                          |
| Saldo de reembolso                                  | Wallet con recarga                                  |
| Multi-moneda por mercado                            | Conversión de divisa y compra transfronteriza       |

# 2\. Roles, subroles y control de acceso

## 2.1 Los cuatro tipos y sus 21 subroles

| Tipo        | Subroles                                                                                                                                 |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **USER**    | `USER_GUEST` · `USER_REGISTERED` · `USER_VERIFIED` · `USER_WINNER` · `USER_RESTRICTED`                                                   |
| **CLIENT**  | `CLIENT_OWNER` · `CLIENT_MANAGER` · `CLIENT_OPERATOR` · `CLIENT_VIEWER`                                                                  |
| **SUPPORT** | `SUPPORT_L1` · `SUPPORT_L2` · `SUPPORT_VALUATOR` · `SUPPORT_SUPERVISOR` · `SUPPORT_BEHAVIORAL_ANALYST`                                   |
| **ADMIN**   | `ADMIN_MODERATION` · `ADMIN_RISK` · `ADMIN_FINANCE` · `ADMIN_LEGAL_COMPLIANCE` · `ADMIN_COMPLIANCE` · `ADMIN_BEHAVIORAL` · `ADMIN_SUPER` |

## 2.2 USER

| Subrol            | Se obtiene                                                           | Capacidades                                                                                                                                | Prohibiciones                                        |
| ----------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------- |
| `USER_GUEST`      | Sin registro                                                         | Navegar catálogo, ver detalle de oportunidad, consultar prueba pública de sorteos ejecutados                                               | Comprar; ver datos de terceros                       |
| `USER_REGISTERED` | Correo y teléfono verificados y únicos                               | Lo anterior, más favoritos, lista de espera y notificaciones                                                                               | **Comprar tickets**                                  |
| `USER_VERIFIED`   | Documento verificado con prueba de vida y mayoría de edad acreditada | Comprar tickets; consultar Mis Tickets; reclamar premio; abrir disputa; autoexcluirse; fijar límites propios; gestionar saldo de reembolso | Alterar resultados; ver datos de otros participantes |
| `USER_WINNER`     | Capacidad transitoria por sorteo                                     | Acceder a su Sala de Resolución, aportar evidencia, confirmar recepción, rechazar el premio                                                | Cambiar el estado de la sala; atestar                |
| `USER_RESTRICTED` | Autoexclusión activa, bloqueo de riesgo o documento vencido          | Consultar historial, reclamar premios pendientes, gestionar saldo                                                                          | **Comprar**; recibir comunicación comercial          |

**RN-03.** `USER_VERIFIED` es prerrequisito ineludible de la primera compra. La verificación no bloquea la navegación ni el registro.

## 2.3 CLIENT

| Subrol            | Capacidades                                                                                         | Prohibiciones                                      |
| ----------------- | --------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `CLIENT_OWNER`    | Todo lo del cliente; gestionar datos bancarios, representación legal y altas y bajas de subusuarios | —                                                  |
| `CLIENT_MANAGER`  | Crear, editar y enviar sorteos a revisión; consultar ventas y liquidaciones                         | Modificar datos bancarios ni legales               |
| `CLIENT_OPERATOR` | Aportar evidencia de entrega, participar en la Sala de Resolución, gestionar logística              | Crear ni publicar sorteos; consultar liquidaciones |
| `CLIENT_VIEWER`   | Lectura de ventas, liquidaciones y reportes                                                         | Cualquier mutación                                 |

### 2.3.1 Regímenes de organizador

Existen dos, con acreditación diferenciada. El modelo original se construyó sobre la persona jurídica; el particular quedaba declarado como segmento sin poder darse de alta.

|                                 | **Persona jurídica**                 | **Persona natural**                                               |
| ------------------------------- | ------------------------------------ | ----------------------------------------------------------------- |
| Identificador tributario        | **Obligatorio**                      | **Opcional.** Se identifica por documento de identidad verificado |
| Representación legal            | Obligatoria, con vigencia de poderes | No aplica                                                         |
| Beneficiario final              | **Obligatorio**                      | El propio titular                                                 |
| Actividad económica concordante | **Obligatoria** (§19.3)              | No aplica                                                         |
| Verificación de identidad       | Del representante legal              | **Del titular, con prueba de vida**                               |
| Acreditación del premio         | Comprobante a nombre de la entidad   | **Titularidad a nombre del titular**                              |
| Cuenta de cobro                 | A nombre de la entidad               | A nombre del titular verificado                                   |
| Subusuarios                     | Hasta cuatro subroles                | **Titular único.** No hay delegación                              |
| Emisión de comprobante          | Emite el organizador                 | **Sujeto a dictamen L-05**                                        |

**RN-03-bis — El identificador tributario es exigible únicamente a la persona jurídica.** La persona natural se identifica por documento verificado con prueba de vida, único conforme a INV-08.

**RN-03-ter — El organizador persona natural es titular único.** No admite subusuarios ni delegación: quien crea el sorteo, aporta la evidencia y cobra es la misma persona verificada.

**RN-03-quater — Un mismo documento no puede sostener dos organizadores.** La unicidad de INV-08 se extiende al alta de organizador persona natural.

**RN-03-quinquies — El organizador persona natural sigue sujeto a la prohibición de autocompra** (RN-150) en sus propios sorteos, y puede participar libremente en los de terceros.

*Consideración de negocio, registrada en L1 §3.1:* el particular es el organizador más atractivo comercialmente y el menos rentable. Sortea una sola vez, consume el mismo costo de verificación que uno recurrente y no acumula volumen liquidado, de modo que **nunca asciende en la escala de comisión**. Es coherente que su encendido sea posterior.

**RN-04.** El cambio de datos bancarios exige `CLIENT_OWNER`, reverificación de identidad, y **congelamiento de liquidaciones durante 48 horas con notificación al titular por todos los canales registrados**. Es el vector de fraude por toma de cuenta más frecuente en marketplaces.

## 2.4 SUPPORT

| Subrol                       | Capacidades                                                                                                               | Prohibiciones                                     |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| `SUPPORT_L1`                 | Buscar por `trace_id`; consultar línea de tiempo; abrir caso; responder en salas asignadas; solicitar evidencia adicional | Atestar; cambiar estado terminal; extender plazos |
| `SUPPORT_L2`                 | Todo lo de L1; **atestar entrega**; extender plazos dentro de límite; marcar necesidad de evidencia adicional             | Tocar dinero, ledger, ganador o liquidación       |
| `SUPPORT_VALUATOR`           | Validar valoración de premio en bandas V1 y V2                                                                            | Atestar la entrega del sorteo que valoró          |
| `SUPPORT_SUPERVISOR`         | Reasignar salas; escalar a ADMIN; revertir atestaciones de L2 con motivo; gestionar cola y plazos                         | Tocar dinero, ledger o ganador                    |
| `SUPPORT_BEHAVIORAL_ANALYST` | Monitorear indicadores conductuales; triangular alertas; preparar expediente de BDR                                       | Decidir sobre alertas; mutar datos                |

**INV-07.** SUPPORT **atesta hechos operativos**. En ningún caso mueve dinero, altera el ledger ni modifica el resultado de un sorteo. Esta es la evolución del invariante de V1, no su derogación.

## 2.5 ADMIN

| Subrol                   | Capacidades                                                                                                                                                | Prohibiciones                                          |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| `ADMIN_MODERATION`       | Aprobar y rechazar sorteos; aplicar política de contenido; visto en banda V2                                                                               | Ejecutar liquidaciones ni pagos                        |
| `ADMIN_RISK`             | Habilitar capacidades T1–T8 y P-C; nivel de riesgo del cliente; congelar cuentas; resolver alertas de fraude                                               | Ejecutar pagos; aprobar sorteos                        |
| `ADMIN_FINANCE`          | Ejecutar liquidaciones y pagos; reembolsos; ajustes de ledger con motivo; conciliación                                                                     | **Atestar entregas**; aprobar sorteos; valorar premios |
| `ADMIN_LEGAL_COMPLIANCE` | Gate legal; valoración en bandas V3 y V4; términos y bases; solicitudes sobre datos personales; **adjudicar disputas**; aprobar cambios de `market_config` | Ejecutar pagos                                         |
| `ADMIN_COMPLIANCE`       | Aprobar operaciones sobre umbral; resolver alertas de prevención financiera; gestionar expedientes de debida diligencia                                    | Mover dinero; aprobar sorteos                          |
| `ADMIN_BEHAVIORAL`       | Propiedad de los indicadores conductuales; aprobar instrumentos de encuesta; convocar BDR; **veto sobre funcionalidades que vulneren un guardarraíl**      | Ejecutar pagos                                         |
| `ADMIN_SUPER`            | Gestión de usuarios internos; configuración; feature flags; **segunda firma**; activación del kill switch                                                  | Ser segunda firma de una acción propia                 |

## 2.6 Incompatibilidades duras

Validadas por el motor de RBAC en tiempo de asignación y en tiempo de ejecución, nunca por procedimiento manual.

| \#     | Incompatibilidad                                                            | Fundamento                                          |
| ------ | --------------------------------------------------------------------------- | --------------------------------------------------- |
| INC-01 | `ADMIN_MODERATION` + `ADMIN_FINANCE`                                        | Aprobar y pagar                                     |
| INC-02 | `ADMIN_LEGAL_COMPLIANCE` + `ADMIN_FINANCE`                                  | Valorar y pagar                                     |
| INC-03 | `ADMIN_COMPLIANCE` + `ADMIN_FINANCE`                                        | Vigilar el dinero y moverlo                         |
| INC-04 | `ADMIN_COMPLIANCE` + `ADMIN_MODERATION`                                     | Vigilar y aprobar lo vigilado                       |
| INC-05 | `ADMIN_BEHAVIORAL` + `ADMIN_FINANCE`                                        | Independencia del guardarraíl                       |
| INC-06 | `SUPPORT_VALUATOR` no atesta la entrega del sorteo que valoró               | Autocontrol                                         |
| INC-07 | `ADMIN_FINANCE` no atesta entregas en ningún caso                           | Separación de funciones                             |
| INC-08 | Quien adjudica una disputa no atestó ese caso                               | Imparcialidad (DP-16)                               |
| INC-09 | La segunda firma proviene de otra persona natural y otro subrol             | Doble control efectivo                              |
| INC-10 | Ningún rol con aprobación de valor tiene métrica de volumen de aprobaciones | Neutralización del conflicto de interés (LBPF §5.5) |
| INC-11 | `ADMIN_SUPER` no es segunda firma de una acción propia                      | Doble control efectivo                              |

### 2.6.1 Otorgamiento y revocación de subroles

**Fundamento.** Quien puede crear usuarios puede crear privilegios. Si un rol pudiera otorgar subroles superiores al suyo, fabricaría una cuenta con capacidades que él no tiene y la usaría para eludir una incompatibilidad. **La creación de usuarios internos es la puerta trasera de todo sistema de control de acceso**, y por eso se acota con techo de privilegio en lugar de concentrarse en una sola persona.

| Quién otorga          | Puede crear y suspender     | Requisito                               |
| --------------------- | --------------------------- | --------------------------------------- |
| `ADMIN_SUPER`         | Cualquier subrol            | Segunda firma para los que tocan dinero |
| `SUPPORT_SUPERVISOR`  | `SUPPORT_L1` **únicamente** | Motivo obligatorio                      |
| Cualquier otro subrol | Ninguno                     | —                                       |

**Las tres reglas de techo:**

**RN-05-bis — Nadie otorga un subrol que no posee.** Un supervisor de soporte no puede crear un valuador, porque él mismo no lo es.

**RN-05-ter — Nadie se otorga a sí mismo**, ni directamente ni mediante una cuenta que acaba de crear.

**RN-05-quater — Los subroles que tocan dinero exigen segunda firma para ser otorgados.** `ADMIN_FINANCE`, `ADMIN_COMPLIANCE` y `ADMIN_LEGAL_COMPLIANCE` no los concede una sola persona, ni siquiera `ADMIN_SUPER`.

**RN-05-quinquies — Asimetría de otorgamiento y revocación.** Cualquier `ADMIN` y cualquier `SUPPORT_SUPERVISOR` puede **suspender de inmediato** una cuenta interna, con motivo obligatorio y notificación. No puede eliminarla ni alterar sus privilegios: solo cortar el acceso. **Restaurar exige** `ADMIN_SUPER`**.**

*Fundamento de la asimetría:* conceder acceso indebido es un riesgo que se materializa con el tiempo; mantener acceso indebido es un riesgo que se materializa ahora. Cuando alguien deja el equipo, revocar su acceso a salas con datos personales y evidencia probatoria no puede esperar a que vuelva de viaje quien tiene la llave.

### 2.6.2 Arranque y continuidad de la administración

**RN-05-sexies — El primer administrador nace en la migración de datos semilla**, con credencial de un solo uso y cambio obligatorio en el primer ingreso. La credencial semilla queda inutilizable tras ese cambio.

**INV-38 — Existen al menos dos** `ADMIN_SUPER` **activos en todo momento.** El sistema impide revocar al penúltimo y emite alarma de severidad alta si el número desciende a uno.

*Fundamento:* con un equipo de cuatro personas, la pérdida del único titular de la administración produce bloqueo total sin ruta de recuperación. No es un escenario remoto: es una baja médica o un viaje.

**RN-05-septies — La cuenta interna no se elimina, se cierra.** Toda asignación de subrol conserva su historial con actor, motivo y fecha, porque la auditoría de quién tuvo qué privilegio y cuándo es parte del expediente.

**RN-05.** Todo subrol interno exige autenticación multifactor y sesión de expiración corta. **RN-06.** Toda acción de subrol interno registra actor, `trace_id`, entidad afectada, motivo cuando aplica, y resultado, en el registro de auditoría inmutable.

## 2.7 Límites de cuentas

No existe tope técnico de usuarios: la base de datos sostiene volúmenes muy superiores a los operables. **Los límites son de capacidad de operación y se declaran como configuración por mercado.**

| Límite                                         | Valor por defecto               | Fundamento                                                                         |
| ---------------------------------------------- | ------------------------------- | ---------------------------------------------------------------------------------- |
| Usuarios participantes                         | **Sin tope**                    | No consume capacidad de operación                                                  |
| Organizadores registrados                      | **Sin tope**                    | El alta no consume operación; publicar sí                                          |
| **Organizadores con sorteo activo simultáneo** | **Parámetro de mercado**        | Es el límite real: cada sorteo activo consume valoración, sala y atestación humana |
| Subusuarios por organizador persona jurídica   | **10**                          | Evita que un organizador convierta su cuenta en una organización sin control       |
| Subusuarios por organizador persona natural    | **1**                           | Titular único, sin delegación (RN-03-ter)                                          |
| `ADMIN_SUPER` activos                          | **Mínimo 2**, sin tope superior | INV-38                                                                             |
| Cuentas internas totales                       | Sin tope                        | Acotado por las once incompatibilidades                                            |

**RN-06-quinquies.** Al alcanzarse el límite de organizadores con sorteo activo, las nuevas publicaciones entran en cola con fecha estimada, **no se rechazan**. Rechazar a un organizador que superó el gate de valoración destruye el trabajo de captación más caro del embudo.

## 2.8 Control de funciones en tres capas

Toda función de LIBOX se enciende y se apaga sin detener procesos en curso. La resolución es en tres capas y **la más restrictiva gana**:

    plataforma  →  mercado  →  cliente

| \#               | Regla                                                                                                                                                  |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **INV-45**       | Si una capa superior apaga una función, ninguna inferior puede encenderla. Encenderla arriba **no** la activa donde una capa inferior la tiene apagada |
| **RN-06-sexies** | Toda conmutación registra **quién, cuándo, qué alcance, con qué motivo y a quiénes afectó**, y es consultable como cualquier otro evento de auditoría  |

**Tres categorías de función**, y la tercera es deliberada:

| Categoría                      | Comportamiento                                                                                                                   |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| **Conmutable en caliente**     | Tipos de sorteo, categorías, superficies, canales de pago, LIBOX Club, sorteos gratuitos, plan promocional, destaques, referidos |
| **Con degradación controlada** | Motor de sorteo, liquidación, resolución, contabilidad. No se apagan en seco: hay dinero y compromisos en curso                  |
| **No conmutable**              | **Reclamar un premio, recibir un reembolso, disponer del saldo, consultar el historial y la autoexclusión**                      |

**La tercera categoría es una limitación intencional.** INV-33 la protege: un interruptor capaz de apagarlas convertiría un problema regulatorio en uno de consumidor.

## 2.9 Escalada de apagado y regla de vuelo

| Alcance                           | Quién                               | Requisito                             |
| --------------------------------- | ----------------------------------- | ------------------------------------- |
| Un tipo a **un cliente**          | `SUPPORT_SUPERVISOR` o `ADMIN_RISK` | Motivo                                |
| Un tipo en **un mercado**         | `ADMIN_SUPER`                       | Motivo + **notificación a afectados** |
| Un tipo en **toda la plataforma** | `ADMIN_SUPER` + **segunda firma**   | Motivo + notificación + registro      |
| **Mercado completo**              | `ADMIN_SUPER` + segunda firma       | Los cuatro niveles de §25             |

**RN-06-septies — Regla de vuelo.** Qué ocurre con lo ya iniciado **depende del motivo del apagado**:

| Motivo                             | Oportunidades vivas                                                                                     |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Comercial, regulatorio o de riesgo | **Terminan normalmente.** Se ejecutan, se entregan y se liquidan. Solo se bloquean publicaciones nuevas |
| **Defecto en el mecanismo**        | **Se congelan antes de ejecutar.** No se sortea con un motor del que se duda                            |

**Fundamento.** Cancelar oportunidades vivas obliga a reembolsar a quienes no hicieron nada mal, y rara vez es proporcionado. Pero si el motor tiene un defecto, **ejecutar sería peor que congelar**.

**RN-06-octies — La notificación es obligatoria y de motivo neutro.** Si la causa es un defecto de seguridad, describirlo a todos los organizadores lo expone. Se informa el efecto y la continuidad; el motivo técnico queda en el registro interno.

## 2.10 Ventanas operativas

**RN-06-nonies.** Cada función puede restringirse a una ventana horaria por mercado: ejecución de sorteos, publicación, liquidaciones, verificación de valor.

| \#                  | Regla                                                                                                                                       |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **RN-06-decies**    | **La ventana difiere, no cancela.** Una oportunidad que cumple su condición fuera de ventana pasa a `READY_TO_DRAW` y se ejecuta al abrirse |
| **RN-06-undecies**  | La ventana **se publica en las bases** y se congela al publicar. El participante debe conocerla antes de comprar                            |
| **RN-06-duodecies** | Con ventana definida, **se notifica al organizador**. Sin restricción, no se notifica nada                                                  |

**Fundamento.** Concentrar ejecuciones en una franja permite acompañarlas, que es lo que necesita un equipo reducido. Y es donde vive el modo en vivo.

## 2.11 Panel de funciones y alta de cuenta interna

**RN-06-terdecies — Panel único con vistas por subrol.** Cada persona ve las funciones que domina, con su estado —activa, apagada por plataforma, por mercado o para un cliente— y **si puede actuar o solo informar y escalar**. Un panel por subrol produciría doce superficies que se desincronizan.

**RN-06-quaterdecies — Alta de cuenta interna.** Toda cuenta de rol interno exige, antes de que la asignación quede activa: correo del dominio corporativo · **verificación de identidad completa con prueba de vida** · multifactor configurado · aceptación registrada de confidencialidad y del marco conductual · vigencia cuando el rol sea temporal.

**Fundamento de la verificación completa.** Quien accede a salas de resolución con datos personales y evidencia probatoria debe estar identificado con el mismo rigor que se exige a un participante antes de su primera compra.

**RN-06-quindecies — Subroles con vigencia.** Todo subrol admite fecha de caducidad, y al vencer se revoca automáticamente. Es lo que permite un rol temporal de auditoría externa **de solo lectura**, incompatible con todo subrol operativo, sin dejar acceso abierto cuando termina el encargo.

# 3\. Dominio

## 3.1 Agregados y propiedad de datos

Corrige el desplazamiento de la tabla de módulos de V1. Cada agregado es propietario exclusivo de sus entidades; ningún módulo escribe en entidades de otro.

| Agregado            | Responsabilidad                                                                                  | Entidades propias                                                                                                                                                |
| ------------------- | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Identity**        | Identidad, autenticación, unicidad, verificación de edad                                         | `users`, `credentials`, `refresh_tokens`, `identity_verifications`, `age_verifications`, `devices`, `identity_documents`, `blocked_documents`                    |
| **Client**          | Organizadores en sus dos regímenes, acreditación, subusuarios, datos de cobro, nivel de comisión | `clients`, `client_members`, `client_kyb`, `payout_instructions`, `client_capabilities`, `client_fee_levels`                                                     |
| **Raffle**          | Oportunidad, ciclo de vida, bases, configuración de tipo                                         | `raffles`, `raffle_terms`, `raffle_type_rules`, `raffle_media`, `state_transitions`                                                                              |
| **Prize**           | Premio, categoría, valoración, custodia, registrables                                            | `prizes`, `prize_valuations`, `prize_valuation_documents`, `prize_market_references`, `registrable_assets`, `registry_queries`, `registry_blocks`                |
| **Order**           | Compra e idempotencia. **Una orden, un sorteo**                                                  | `orders`, `idempotency_keys`                                                                                                                                     |
| **Payment**         | Cobro, PSP, webhooks, conciliación                                                               | `payments`, `psp_events`, `processed_psp_events`, `reconciliation_batches`, `reconciliation_exceptions`                                                          |
| **Ticket**          | Emisión y numeración. **El pool es derivado, no persistido**                                     | `tickets`                                                                                                                                                        |
| **Draw**            | Congelamiento, compromiso, ejecución, prueba                                                     | `draw_commitments`, `draw_executions`, `draw_proofs`, `redraws`                                                                                                  |
| **Resolution**      | Sala, evidencia, atestación, entrega                                                             | `resolution_rooms`, `room_participants`, `room_messages`, `room_evidence`, `room_internal_notes`, `room_assignments`, `delivery_attestations`, `shipping_quotes` |
| **Dispute**         | Controversia, adjudicación                                                                       | `disputes`, `dispute_evidence`, `dispute_adjudications`                                                                                                          |
| **Settlement**      | Devengo, gates, liquidación                                                                      | `settlements`, `settlement_items`, `settlement_holds`                                                                                                            |
| **Ledger**          | Contabilidad de partida doble                                                                    | `ledger_accounts`, `journal_entries`, `journal_lines`                                                                                                            |
| **RefundCredit**    | Saldo de reembolso                                                                               | `refund_credits`, `refund_credit_entries`, `refund_credit_withdrawals`                                                                                           |
| **Risk**            | Riesgo, fraude, correlación                                                                      | `risk_events`, `risk_rules`, `risk_cases`                                                                                                                        |
| **Compliance**      | Prevención financiera, acumuladores, expedientes                                                 | `spend_accumulators`, `aml_thresholds`, `aml_cases`, `aml_case_documents`, `operation_register`                                                                  |
| **ResponsiblePlay** | Protección del usuario                                                                           | `self_exclusions`, `spending_limits`, `spending_limit_changes`, `responsible_play_events`                                                                        |
| **Reputation**      | Reputación de cliente y de usuario                                                               | `client_reputation`, `client_reputation_history`, `user_reputation`                                                                                              |
| **Analytics**       | Eventos de decisión, encuestas, indicadores                                                      | `analytics_events`, `survey_instruments`, `survey_responses`, `kpi_snapshots`                                                                                    |
| **Notification**    | Canales, plantillas, intentos, consentimiento                                                    | `notification_templates`, `notification_attempts`, `notification_preferences`                                                                                    |
| **Alarm**           | Panel único                                                                                      | `alarms`, `alarm_assignments`, `alarm_resolutions`                                                                                                               |
| **Market**          | Configuración por jurisdicción                                                                   | `markets`, `market_config_versions`, `market_legal_requirements`, `market_prize_categories`, `holidays_calendar`                                                 |
| **Growth**          | Atribución, referidos, promociones, campañas                                                     | `attribution_touches`, `referrals`, `promotions`, `promotion_grants`, `waitlists`, `campaigns`, `leads`                                                          |
| **Audit**           | Trazabilidad inmutable                                                                           | `audit_events`, `audit_emergency_queue`, `event_outbox`                                                                                                          |

**RN-06-bis — Toda entidad declarada existe como tabla real o se marca expresamente como derivada.** Un agregado que declare una entidad sin respaldo en `libox_schema_L3_V7.sql` incumple el criterio de cierre de §0.3.

**RN-06-ter — Una orden, un sorteo.** Una orden de compra corresponde a exactamente un sorteo. No existe carrito multi-sorteo en el MVP.

*Fundamento:* la orden congela su propio desglose de comisión y neto del organizador, con invariante `client_net + libox_fee = gross`. Con varios sorteos en una orden ese desglose deja de ser único, los gates de liquidación pierden su referencia y la atribución de tickets se vuelve ambigua. La cantidad de tickets sí es libre dentro de un mismo sorteo.

**RN-06-quater — El pool es derivado.** El pool de un sorteo es el conjunto de tickets con estado emitido en el instante del congelamiento. No se persiste como entidad propia; su fotografía inmutable vive en la instantánea del documento de prueba.

**RN-07.** La comunicación entre agregados es por evento publicado en `event_outbox`, nunca por escritura directa en tablas ajenas. Un módulo que necesita datos de otro los consulta por su interfaz pública o los recibe por evento.

**RN-08.** La compilación falla si existe dependencia de escritura cruzada entre agregados. Es criterio de aceptación de la historia de arranque del proyecto.

## 3.2 Invariantes de dominio

| \#     | Invariante                                                                                                    |
| ------ | ------------------------------------------------------------------------------------------------------------- |
| INV-08 | Un documento de identidad, un correo y un teléfono corresponden a exactamente un usuario activo               |
| INV-09 | Un ticket válido no existe sin un pago confirmado que lo respalde                                             |
| INV-10 | La suma de los asientos de una transacción cuadra: débitos igual a créditos                                   |
| INV-11 | Un número de ticket anulado no se reasigna jamás dentro del mismo sorteo                                      |
| INV-12 | Un sorteo ejecutado no se re-ejecuta; el re-sorteo es una entidad distinta y encadenada                       |
| INV-13 | Ningún participante posee más del umbral de concentración del mercado en un mismo sorteo                      |
| INV-14 | Las bases de un sorteo son inmutables desde la publicación                                                    |
| INV-15 | Un sorteo se rige por la versión de `market_config` vigente el día de su publicación                          |
| INV-16 | La recaudación retenida de un sorteo activo es siempre suficiente para reembolsar la totalidad de sus tickets |

# 4\. Ciclo de vida del sorteo

## 4.1 Máquina de estados única

V1 declaraba ocho listas de estados sin intersección, de modo que no existía una máquina de estados de `raffles`. V2 estableció **una sola FSM**; los ocho tipos son configuración sobre ella.

| Estado              | Significado                                                |
| ------------------- | ---------------------------------------------------------- |
| `DRAFT`             | En edición por el organizador                              |
| `PENDING_VALUATION` | Enviado; premio en verificación de valor                   |
| `PENDING_LEGAL`     | Valor aprobado; en gate legal y documental                 |
| `PENDING_APPROVAL`  | Gates superados; en decisión de moderación                 |
| `REJECTED`          | Rechazado con motivo estructurado (terminal)               |
| `SCHEDULED`         | Aprobado, con inicio de venta futuro                       |
| `ACTIVE`            | En venta                                                   |
| `PAUSED`            | Venta suspendida por riesgo, cumplimiento o kill switch    |
| `SOLD_OUT`          | Pool completo                                              |
| `ENDED_TIME`        | Cierre por plazo                                           |
| `THRESHOLD_REACHED` | Umbral mínimo alcanzado (tipos con umbral)                 |
| `THRESHOLD_FAILED`  | Plazo vencido sin alcanzar el umbral                       |
| `MILESTONE_REACHED` | Hito de progresión alcanzado (T4)                          |
| `READY_TO_DRAW`     | Condición de sorteo satisfecha; pendiente de congelamiento |
| `POOL_FROZEN`       | Pool congelado; compromiso y baliza publicados             |
| `DRAW_EXECUTED`     | Sorteo ejecutado; prueba generada                          |
| `IN_RESOLUTION`     | Sala abierta; reclamo y entrega en curso                   |
| `DELIVERY_ATTESTED` | Entrega atestada                                           |
| `SETTLED`           | Liquidado al organizador; asientos registrados             |
| `CLOSED`            | Cerrado contable y operativamente (terminal)               |
| `CANCELLED`         | Cancelado con reembolso íntegro (terminal)                 |
| `SUSPENDED_MARKET`  | Detenido por suspensión de mercado                         |

## 4.2 Transiciones legales

| Desde                                                                 | Hacia                  | Disparador                                              | Autoriza                                                  |
| --------------------------------------------------------------------- | ---------------------- | ------------------------------------------------------- | --------------------------------------------------------- |
| `DRAFT`                                                               | `PENDING_VALUATION`    | Envío a revisión                                        | `CLIENT_MANAGER`                                          |
| `PENDING_VALUATION`                                                   | `PENDING_LEGAL`        | Valor aprobado                                          | `SUPPORT_VALUATOR` / `ADMIN_LEGAL_COMPLIANCE` según banda |
| `PENDING_VALUATION`                                                   | `REJECTED`             | Desviación superior al 50 %                             | Sistema, automático y no anulable                         |
| `PENDING_VALUATION`                                                   | `DRAFT`                | Observación                                             | Verificador                                               |
| `PENDING_LEGAL`                                                       | `PENDING_APPROVAL`     | Gate legal superado                                     | `ADMIN_LEGAL_COMPLIANCE`                                  |
| `PENDING_APPROVAL`                                                    | `SCHEDULED` / `ACTIVE` | Aprobación                                              | `ADMIN_MODERATION`                                        |
| `PENDING_APPROVAL`                                                    | `REJECTED`             | Rechazo con motivo                                      | `ADMIN_MODERATION`                                        |
| `SCHEDULED`                                                           | `ACTIVE`               | Llegada del inicio                                      | Sistema                                                   |
| `ACTIVE`                                                              | `PAUSED`               | Alerta de riesgo, gravamen sobrevenido, cumplimiento    | `ADMIN_RISK` / `ADMIN_COMPLIANCE` / Sistema               |
| `PAUSED`                                                              | `ACTIVE`               | Causa resuelta                                          | Quien pausó, con motivo                                   |
| `ACTIVE`                                                              | `SOLD_OUT`             | Pool completo                                           | Sistema                                                   |
| `ACTIVE`                                                              | `ENDED_TIME`           | Llegada del cierre                                      | Sistema                                                   |
| `ACTIVE`                                                              | `THRESHOLD_REACHED`    | Umbral alcanzado                                        | Sistema                                                   |
| `ACTIVE`                                                              | `MILESTONE_REACHED`    | Hito alcanzado en T4                                    | Sistema                                                   |
| `MILESTONE_REACHED`                                                   | `ACTIVE`               | Quedan hitos pendientes en la progresión                | Sistema                                                   |
| `ENDED_TIME`                                                          | `THRESHOLD_FAILED`     | Cierre con umbral no alcanzado                          | Sistema                                                   |
| `THRESHOLD_FAILED`                                                    | `CANCELLED`            | Cancelación automática con reembolso íntegro            | Sistema                                                   |
| `SOLD_OUT` / `ENDED_TIME` / `THRESHOLD_REACHED` / `MILESTONE_REACHED` | `READY_TO_DRAW`        | Condición satisfecha y al menos un ticket válido        | Sistema                                                   |
| `ENDED_TIME` sin tickets válidos                                      | `CANCELLED`            | Sin participantes                                       | Sistema                                                   |
| `READY_TO_DRAW`                                                       | `POOL_FROZEN`          | Congelamiento, compromiso y baliza publicados           | Sistema                                                   |
| `POOL_FROZEN`                                                         | `DRAW_EXECUTED`        | Baliza disponible y ejecución                           | Sistema                                                   |
| `DRAW_EXECUTED`                                                       | `IN_RESOLUTION`        | Apertura de sala                                        | Sistema                                                   |
| `IN_RESOLUTION`                                                       | `DELIVERY_ATTESTED`    | Atestación                                              | `SUPPORT_L2` / `ADMIN_LEGAL_COMPLIANCE` en P-C            |
| `IN_RESOLUTION`                                                       | `CANCELLED`            | Ruta de no entrega o no reclamo con ruta de cancelación | `ADMIN`                                                   |
| `DELIVERY_ATTESTED`                                                   | `SETTLED`              | Seis gates satisfechos y pago ejecutado                 | `ADMIN_FINANCE`                                           |
| `SETTLED`                                                             | `CLOSED`               | Ventana de retención vencida sin incidencias            | Sistema                                                   |
| Cualquiera anterior a `DRAW_EXECUTED`                                 | `SUSPENDED_MARKET`     | Kill switch                                             | `ADMIN_SUPER`                                             |

**RN-09.** Toda transición se registra en `state_transitions` con actor, motivo cuando aplica, `trace_id` y marca temporal de servidor. **RN-10.** No existe transición desde estados terminales `CLOSED`, `CANCELLED` y `REJECTED`. **RN-11.** El re-sorteo no es una transición: es una entidad `redraws` que genera un nuevo `draw_execution` encadenado (§16.4).

# 5\. Tipos de sorteo T1–T8

## 5.1 Principio

Los ocho tipos son **configuración sobre la FSM única**, no motores distintos. Cada tipo declara su condición de disparo, sus estados aplicables y sus controles. Ningún tipo altera el algoritmo del sorteo: **T8 modifica la experiencia visual, no la matemática** (INV-17).

## 5.2 Definición

| Tipo   | Nombre               | Condición de disparo                                      | Estados propios                         | Controles específicos                                                                                                                                                                                                |
| ------ | -------------------- | --------------------------------------------------------- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **T1** | Sold-out             | `tickets_sold = total_tickets`                            | `SOLD_OUT`                              | Sin plazo de cierre; requiere política de expiración del mercado                                                                                                                                                     |
| **T2** | Umbral mínimo        | Llegada de `end_at`, con `tickets_issued ≥ min_threshold` | `THRESHOLD_REACHED`, `THRESHOLD_FAILED` | `min_threshold` y `end_at` obligatorios; cancelación automática con reembolso íntegro si no se alcanza                                                                                                               |
| **T3** | Por tiempo           | Llegada de `end_at`                                       | `ENDED_TIME`                            | Cancelación si no hay tickets válidos                                                                                                                                                                                |
| **T4** | Progresivo por hitos | Alcance del hito marcado como disparador                  | `MILESTONE_REACHED`                     | Entre 2 y 6 hitos, con umbral de tickets y efecto declarado; publicados en bases e **inmutables desde la publicación**                                                                                               |
| **T5** | Flash                | Ventana corta con cierre por tiempo o pool                | `ENDED_TIME`, `SOLD_OUT`                | `end_at` obligatorio; **duración entre el mínimo y el máximo del mercado**; reserva de inventario reforzada con vigencia corta; métrica de sobreventa                                                                |
| **T6** | Multi-ganador        | Igual que T1 o T3 según configuración                     | —                                       | Sorteo **sin reemplazo**; `k` ganadores declarados en bases; premios diferenciados por posición                                                                                                                      |
| **T7** | Recurrente           | Programación periódica de la serie                        | —                                       | La serie define frecuencia y número máximo de ediciones. **Cada edición es un** `raffle` **independiente con su propio pool, su propio compromiso y su propia prueba.** Ninguna edición hereda estado de la anterior |
| **T8** | Live                 | Igual que el tipo base                                    | —                                       | Ejecución en horario anunciado con transmisión. **Modo de presentación, no motor**                                                                                                                                   |

**RN-11-bis — Resolución de la ambigüedad de T2.** T2 **no cierra anticipadamente** al alcanzar el umbral: continúa vendiendo hasta `end_at` y en ese momento evalúa si lo alcanzó. El umbral es condición de viabilidad, no de cierre. El cierre anticipado por umbral queda como parámetro de mercado, deshabilitado por defecto, porque convierte a T2 en un producto distinto y debe decidirse con datos.

**RN-11-ter — Hitos de T4.** Cada hito declara umbral de tickets, descripción y efecto: premio adicional, mejora de premio o disparo del sorteo. **Exactamente uno es el disparador y es el de mayor umbral.** Los hitos se publican en las bases y son inmutables desde la publicación (INV-14): modificarlos con tickets vendidos alteraría el contrato después de cobrar.

**RN-11-quater — Ediciones de T7.** La serie define frecuencia, separación mínima y número máximo de ediciones. Cada edición se crea como sorteo nuevo que pasa por el gate de valoración de premio como cualquier otro. **La reputación del organizador no exime a ninguna edición de ese gate** (INV-28).

**RN-12.** Todo tipo se habilita por capacidad del cliente (`client_capabilities`) y por mercado (`market_prize_categories` y configuración de tipos). Un tipo deshabilitado no aparece en el asistente de creación.

**RN-13.** T6 exige sorteo sin reemplazo especificado en `draw-engine-spec.md` (L3 V7). El pool remanente se recalcula tras cada extracción y la prueba incluye la secuencia completa.

**RN-14.** T1 requiere política de expiración: un sorteo T1 que no completa su pool en el plazo máximo del mercado pasa a `CANCELLED` con reembolso íntegro. Sin esta regla, un T1 que no vende queda congelado indefinidamente.

## 5.3 Capacidades por defecto

| Tipo           | Estado inicial de la capacidad               | Habilita                                                                              |
| -------------- | -------------------------------------------- | ------------------------------------------------------------------------------------- |
| T1, T3         | Habilitado tras aprobación del primer sorteo | `ADMIN_RISK`                                                                          |
| T2, T4, T6, T7 | Deshabilitado                                | `ADMIN_RISK`, con reputación N1 o superior                                            |
| T5             | Deshabilitado                                | `ADMIN_RISK`, con reputación N2 o superior                                            |
| T8             | Deshabilitado                                | `ADMIN_RISK`, con reputación N1 o superior y verificación de capacidad de transmisión |

## 5.4 Semilla de tipos

**RN-14-bis.** Los ocho tipos existen como **datos cargados en la migración inicial**, no como condicionales en el código. La tabla de reglas de tipo se puebla con los ocho, con su disparador, sus requisitos de plazo y umbral, su condición de multi-ganador y su modo de presentación. La semilla completa está en L3 V7 §4.1.1 y es **requisito de aceptación de la historia de arranque**.

Sin ella, la afirmación de que T1–T8 son configuración sobre una máquina de estados única es una descripción, no un hecho verificable.

## 5.5 Sorteo con entrada gratuita

Oportunidad sin contraprestación del participante. Sujeta a **P13 del rector: igualdad de probabilidad entre vía gratuita y pagada.**

**Tres orígenes del premio**, declarados por oportunidad:

| Origen           | Quién lo pone                           | Régimen                               |
| ---------------- | --------------------------------------- | ------------------------------------- |
| `LIBOX_RELATED`  | Entidad vinculada como cliente (§1.2.1) | Gasto promocional                     |
| `JOINT_CAMPAIGN` | Ambos, con reparto declarado            | Gasto compartido                      |
| `ORGANIZER`      | El organizador                          | **Requiere reputación N2 o superior** |

| \#                  | Regla                                                                                                                                                      |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **INV-42**          | Toda participación en una oportunidad con entrada gratuita tiene **idéntica probabilidad**. Prohibida cualquier ventaja derivada del gasto (P13, LINT-011) |
| **RN-14-quater**    | **Una participación por persona**, sobre la unicidad de INV-08                                                                                             |
| **RN-14-quinquies** | **Verificación diferida**: participar exige correo y teléfono únicos; la verificación de identidad se exige **al reclamar el premio**                      |
| **RN-14-sexies**    | El **código de campaña** tiene cupo publicado. El decremento es atómico: **nunca se emiten más participaciones que el cupo**                               |
| **RN-14-septies**   | Agotado el cupo, el código se cierra e informa. Sin error genérico                                                                                         |
| **RN-14-octies**    | La **ampliación de cupo la autoriza ADMIN** con motivo, solo antes de ejecutar, y **se notifica a los ya inscritos**                                       |
| **RN-14-nonies**    | Sin recaudación no hay escrow: aplica INV-06-b y la garantía sustitutiva                                                                                   |

**Fundamento de RN-14-octies.** El cupo determina la probabilidad. Ampliar de mil a cinco mil **diluye a quien ya entró**, y eso es información esencial que cambia después de su decisión.

**Fundamento de la verificación diferida.** Cada verificación de identidad tiene costo. Una campaña de cinco mil participantes produciría cinco mil verificaciones pagadas por un premio de marketing. Diferirla al reclamo produce **una sola verificación** sin debilitar ningún control: la unicidad de correo y teléfono ya impide la multicuenta.

**El límite de concentración no aplica** a estas oportunidades: una participación por persona lo hace innecesario.

## 5.6 Régimen promocional

Organizador que sortea **sin cobrar al participante**: cines, tiendas por departamentos, marcas en campaña.

| Aspecto             | Marketplace                | **Promocional**                                 |
| ------------------- | -------------------------- | ----------------------------------------------- |
| Ingreso de LIBOX    | Comisión sobre recaudación | **Plan de precio fijo, cobrado por adelantado** |
| Recaudación         | Sí                         | **No**                                          |
| Retención de fondos | Sí                         | **No hay fondos que retener**                   |
| Liquidación         | Seis gates                 | **No aplica**                                   |
| Cadena de cierre    | Gates de liquidación       | **Cadena de conformidad**                       |

| \#                  | Regla                                                                                                                                                                                |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **INV-43**          | El régimen promocional **no genera liquidación**. INV-23 no le aplica y se declara expresamente                                                                                      |
| **RN-14-decies**    | La **cadena de conformidad** sustituye a los gates: valoración aprobada → sorteo ejecutado → entrega atestada → cierre. G4, G5 y G6 no aplican porque no hay dinero del participante |
| **RN-14-undecies**  | El plan **se cobra por adelantado**. Es lo único que otorga algo retenible ante incumplimiento                                                                                       |
| **RN-14-duodecies** | Consume **cupo propio** dentro del límite de oportunidades activas del mercado                                                                                                       |
| **RN-14-terdecies** | Auditoría completa de extremo a extremo, con expediente exportable como cualquier otra oportunidad                                                                                   |

**Fundamento del cupo propio.** Un sorteo promocional consume **la misma capacidad de valoración, sala y atestación** que uno pagado. No es ingreso incremental gratuito: compite por el recurso más escaso, y su precio debe cubrir ese costo operativo.

### 5.6.1 Gate de habilitación del régimen promocional

Los demás regímenes tienen condición de entrada: capacidad habilitada, reputación acreditada, garantía constituida. **El promocional entraba únicamente por plan contratado**, y eso es insuficiente.

| \#                     | Requisito                                                                                                    |
| ---------------------- | ------------------------------------------------------------------------------------------------------------ |
| **RN-14-quaterdecies** | Reputación **N1 o superior**, o acreditación reforzada para organizador nuevo con respaldo formal verificado |
| **RN-14-quindecies**   | Capacidad `PROMOTIONAL` habilitada por `ADMIN_RISK`, como cualquier otra capacidad                           |
| **RN-14-sexdecies**    | Garantía sustitutiva constituida antes de publicar, conforme a INV-06-b                                      |
| **RN-14-septdecies**   | Plan vigente y **pagado por adelantado**, con cupo mensual disponible                                        |

**Fundamento.** En este régimen el participante **no arriesga dinero, pero sí su tiempo, sus datos y su expectativa**, y llegó por la marca LIBOX. Sin dinero retenido no hay reembolso que ofrecer si el organizador incumple: **la reputación previa y la garantía son la única protección disponible**, y por eso son condición de entrada y no de salida.

## 5.7 Secuenciación de encendido

El encendido progresivo ya secuencia tipos de sorteo y categorías de premio. **Faltaba secuenciar los regímenes económicos**, que son los que más carga operativa añaden.

| Momento     | Régimen habilitado                                          | Condición                                                                                     |
| ----------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Lanzamiento | **Pagado únicamente**                                       | —                                                                                             |
| \+2 meses   | **Promocional**                                             | Modelo de costo unitario calculado con datos reales, y **precio del plan validado contra él** |
| \+3 meses   | **Entrada gratuita**, origen `LIBOX_RELATED`                | Relevo operativo contratado                                                                   |
| \+4 meses   | **Entrada gratuita**, origen `ORGANIZER` y `JOINT_CAMPAIGN` | Al menos tres campañas propias ejecutadas sin incidencia                                      |

**RN-14-octodecies.** Ningún régimen se enciende sin que el anterior haya operado un ciclo completo —publicación, sorteo, entrega atestada y cierre— sin incidencia grave.

**Fundamento.** Cada régimen añade su propia cadena de cierre, su modelo de garantía y su tratamiento contable. **No dividen la carga operativa: la multiplican**, porque un caso de resolución en régimen gratuito no se parece a uno pagado y exige criterio propio.

El orden no es arbitrario. El régimen pagado tiene escrow y por tanto la protección más fuerte. El promocional se enciende segundo porque su cliente es empresa formal y su volumen de participantes es acotado. **La entrada gratuita va al final por ser la de mayor exposición**: máximo número de participantes, mínima protección financiera, y el daño reputacional recae íntegro sobre LIBOX.

**RN-14-ter.** T8 exige `base_type` y ningún otro tipo lo admite. La restricción se impone en el esquema, no en el servicio, para que ningún camino de código pueda crear un sorteo Live sin tipo base ni un tipo base en un sorteo que no es Live.

# 6\. Taxonomía de premios

## 6.1 Categorías

La categoría de premio es atributo de primera clase y determina régimen de acreditación, evidencia de entrega, plazo y criterio de conformidad.

| Cat.     | Tipo                    | Régimen                | “Entregado” significa                                       | Plazo base de entrega | MVP                                         |
| -------- | ----------------------- | ---------------------- | ----------------------------------------------------------- | --------------------- | ------------------------------------------- |
| **P-A**  | Bien físico nuevo       | Existente o producible | Posesión física por el ganador                              | 20 días               | Activo                                      |
| **P-B**  | Bien físico usado       | Existente              | Posesión física, con estado concordante con lo declarado    | 20 días               | Activo                                      |
| **P-C1** | Vehículo                | Existente              | **Transferencia registral inscrita**                        | 45 días               | Activo                                      |
| **P-C2** | Inmueble                | Existente              | **Transferencia registral inscrita**                        | 90 días               | Activo, se enciende tras tres P-C1 exitosos |
| **P-D**  | Servicio o experiencia  | Producible             | **Puesta a disposición completa e irrevocable**, no consumo | 30 días               | Activo                                      |
| **P-E**  | Digital o canjeable     | Producible             | Código entregado, canjeado y validado con el emisor         | 7 días                | Activo                                      |
| **P-F**  | Efectivo y equivalentes | —                      | —                                                           | —                     | **Declarado y deshabilitado**               |

**RN-15 — Definición de entrega en P-D.** *Entregado* significa puesta a disposición completa e irrevocable, no consumo. Un viaje se entrega cuando el paquete está emitido a nombre del ganador, con localizadores verificables, y el organizador ya no puede revertirlo — aunque la fecha de viaje sea posterior. Sin esta definición, la liquidación de un sorteo de experiencia quedaría bloqueada meses y ningún organizador publicaría en esta categoría.

**RN-16 — P-F.** Permanece en el modelo de datos con la capacidad deshabilitada por configuración. Su habilitación futura exige dictamen específico en materia de prevención financiera, verificación reforzada del ganador y revisión de la calificación regulatoria del producto. No es una categoría más: es un producto distinto.

## 6.2 Regímenes de acreditación

| Régimen          | Aplica cuando                                     | Se acredita                                                                                                                                                                        |
| ---------------- | ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **R-EXISTENTE**  | El bien existe y es identificable hoy             | Titularidad o posesión legítima: comprobante a nombre del organizador, identificador único, evidencia gráfica con código del día                                                   |
| **R-PRODUCIBLE** | El bien se adquiere o produce después de la venta | Capacidad comercial y respaldo: actividad económica concordante, antecedentes de operación, cotización o carta de proveedor formal, y la retención de la recaudación como garantía |

**Fundamento.** Exigir título de propiedad a una agencia de viajes por un paquete que aún no existe, o a un comercio por un equipo que comprará, deja fuera precisamente a los organizadores formales. En R-PRODUCIBLE el gate no verifica *“tienes el bien”*, verifica *“puedes producirlo y el dinero que respalda a los participantes está retenido”*.

## 6.3 Evidencia de entrega por categoría

| Cat.       | Evidencia de conformidad                                                                                                                                                                     |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| P-A        | Guía de transporte con seguimiento y constancia de recepción; evidencia gráfica del bien con el ganador y el código del día; confirmación del ganador                                        |
| P-B        | Lo anterior, más acta de conformidad de estado firmada por el ganador                                                                                                                        |
| P-C1, P-C2 | Copia literal de la partida con el ganador como titular, obtenida **por consulta directa de LIBOX**; acta o escritura de transferencia; aceptación del organizador; confirmación del ganador |
| P-D        | Documentos del paquete emitidos a nombre del ganador con localizadores verificables; confirmación del proveedor; confirmación del ganador                                                    |
| P-E        | Constancia de canje emitida por el emisor; confirmación del ganador                                                                                                                          |

**RN-17.** En categorías registrables, un documento aportado por una de las partes **nunca es fuente de verdad**. La verificación se realiza por consulta directa de LIBOX al registro correspondiente.

## 6.4 Costos de recepción

## 6.5 Categorías registrables fuera del régimen con recaudación

**INV-44 — Las categorías P-C1 y P-C2 quedan prohibidas en régimen promocional y en oportunidades con entrada gratuita**, salvo custodia efectiva del bien o garantía formal constituida antes de la publicación.

**Fundamento.** Todo el proceso de siete etapas se apoya en la retención de aproximadamente el 125 % del valor del premio, y en particular la cláusula de custodia del instrumento notarial —que es lo que convence al organizador de transferir antes de cobrar—. **Sin recaudación retenida esa cláusula queda vacía**: si el organizador no transfiere, no hay reembolso que hacer ni fondos que ejecutar, y el ganador queda sin nada con la marca LIBOX de por medio.

Se impone en el esquema, no en el procedimiento.

**RN-18.** El costo de envío lo asume el ganador. El **rango estimado por macrozona** se publica en el detalle de la oportunidad **antes de la compra** (BR-08). Un costo revelado después de la compra es un costo oculto y constituye infracción del framework.

**RN-19.** En categorías registrables, los costos notariales, registrales y tributarios se declaran por sorteo, con indicación expresa de quién los asume, y se publican en las bases. Se declaran igualmente las **cargas recurrentes** que el ganador heredará.

# 7\. Gate de verificación de valor del premio

## 7.1 Obligatoriedad

**RN-20.** Ningún sorteo se publica sin verificación documental del valor del premio, contrastada contra referencias de mercado. **Sin excepción por reputación, antigüedad ni volumen del organizador.**

**Fundamento.** El valor del premio es la variable sobre la que el participante evalúa si la oportunidad merece su dinero. Un valor no verificado convierte toda la información de la tarjeta —costo, probabilidad, evidencia— en una comparación contra una cifra inventada. Y la garantía patrimonial de §1.5 no protege contra la sobrevaloración: un premio inflado se entrega íntegramente y el escrow no detecta nada.

## 7.2 Bandas de verificación

| Banda  | Valor declarado (PE) | Profundidad                                                                                   | Aprueba                                            |
| ------ | -------------------- | --------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| **V1** | ≤ S/ 1.000           | Documental básica y dos referencias de mercado                                                | `SUPPORT_VALUATOR`                                 |
| **V2** | S/ 1.001 – 10.000    | Lo anterior, más identificadores únicos y verificación externa disponible                     | `SUPPORT_VALUATOR` con visto de `ADMIN_MODERATION` |
| **V3** | S/ 10.001 – 50.000   | Lo anterior, más tasación o certificación de distribuidor y evidencia en video                | `ADMIN_LEGAL_COMPLIANCE`                           |
| **V4** | \> S/ 50.000         | Lo anterior, más verificación registral cuando aplique y revisión del instrumento contractual | `ADMIN_LEGAL_COMPLIANCE` con **segunda firma**     |

Los umbrales provienen de `market_config` y se calibran con datos reales.

## 7.3 Regla de desviación

Ejecutada por el sistema sin criterio humano. Es el control que neutraliza el conflicto de interés estructural.

    mediana_ref = mediana( referencias de mercado con URL y fecha ≤ 30 días )
    desviación  = ( valor_declarado − mediana_ref ) / mediana_ref
    
    desviación ≤ 0,20          → APROBABLE
    0,20 < desviación ≤ 0,50   → EXIGE TASACIÓN + SEGUNDA FIRMA
    desviación > 0,50          → RECHAZO AUTOMÁTICO, NO ANULABLE

**RN-21.** En categorías con tasación obligatoria, el valor rector es la tasación, no la declaración del organizador. **RN-22.** Toda excepción exige segunda firma de otra persona natural, motivo de al menos 50 caracteres, y queda registrada con reporte periódico a la dirección. **RN-23 (INC-10).** Ningún rol con capacidad de aprobar valor tiene métrica de desempeño ligada al volumen de sorteos aprobados.

## 7.4 Código del día

**RN-24.** LIBOX genera por sorteo una cadena corta con vigencia de 72 horas que debe aparecer visible en las fotografías y el video del bien. Impide reutilizar imágenes de internet o de un sorteo anterior. Es el control de mejor relación costo-efectividad del gate.

## 7.5 Verificaciones externas

Implementadas por interfaz común con adaptador por mercado (§24.4).

| Aplicación             | Método                                                                                                                             |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Comprobante de pago    | Validación de comprobante electrónico ante la autoridad tributaria del mercado. Convierte una imagen de factura en dato verificado |
| Terminales móviles     | Verificación de identificador de equipo: validación de formato y consulta de estado en bases de equipos reportados                 |
| Vehículos e inmuebles  | Consulta registral directa: titularidad, gravámenes, cargas y características                                                      |
| Referencias de mercado | Al menos dos comercios formales, con dirección web y fecha de captura no mayor a 30 días                                           |

# 8\. Workflow de premios registrables (P-C)

## 8.1 Naturaleza y posición de LIBOX

**RN-25.** La transferencia del bien es **directa entre organizador y ganador**. LIBOX **no es parte** de la transferencia.

| LIBOX responde por                                   | LIBOX no responde por                      |
| ---------------------------------------------------- | ------------------------------------------ |
| Que el proceso sea legal, trazable y verificable     | La calidad o el estado del bien            |
| La custodia íntegra de la recaudación                | Vicios ocultos o defectos de título        |
| La verificación documental en cada etapa             | El saneamiento físico o legal del bien     |
| La verificación registral final por consulta directa | La resolución de observaciones registrales |
| El reembolso íntegro si el proceso falla             | Asesoría legal a las partes                |

**Fundamento de la estructura.** Si el bien transfiriera organizador → LIBOX → ganador habría dos transferencias, con duplicación de tributos de transferencia y LIBOX figurando como titular registral con las obligaciones asociadas. La transferencia directa evita ambas cosas y acota la responsabilidad de LIBOX al proceso, que es donde puede responder con la garantía patrimonial detrás.

Esta delimitación se redacta en lenguaje llano en las bases de todo sorteo P-C y es aceptada expresamente por el organizador y por el ganador.

## 8.2 Instrumento notarial

**RN-26.** Todo sorteo P-C exige instrumento notarial, sobre **plantilla única aprobada y versionada**, firmado antes del go-live entre organizador y LIBOX, al que el ganador se adhiere posteriormente. No se admiten documentos aportados libremente por el organizador: haría inauditable el proceso.

Contenido mínimo:

1.  Identificación plena del bien con copia literal vigente anexa
2.  Declaración jurada de titularidad y de ausencia de gravámenes, cargas, embargos y litigios
3.  Compromiso irrevocable de transferencia a quien resulte ganador del sorteo identificado
4.  **Declaración de custodia:** LIBOX retiene el 100 % de la recaudación y la libera únicamente contra inscripción registral verificada
5.  Asignación expresa de costos notariales, registrales, tributarios y de saneamiento
6.  Autorización y compromiso de mantener vigente el bloqueo registral durante toda la venta
7.  Delimitación de responsabilidades conforme a §8.1
8.  Consecuencias del incumplimiento, con reembolso íntegro con cargo a la recaudación retenida
9.  Ruta ante fallo no imputable a las partes, con plazo de subsanación
10. Sometimiento a jurisdicción y mecanismo de solución de controversias

La cláusula 4 es la que hace viable el modelo: convierte la retención operativa en obligación oponible, y es lo que permite que el organizador transfiera antes de cobrar.

## 8.3 Las siete etapas

Ninguna avanza sola. Cada una exige documentos de lista cerrada, verificación externa cuando existe, y aprobación humana explícita con motivo.

| Etapa                          | Contenido                                                                                                                                                                                                     | Aprueba                                                  | Rechazo automático                                    |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- | ----------------------------------------------------- |
| **E1 Elegibilidad**            | Capacidad P-C1 o P-C2 habilitada; KYB completo y vigente; **reputación N2 o superior** o autorización expresa; sin disputas abiertas                                                                          | `ADMIN_RISK`                                             | Reputación insuficiente                               |
| **E2 Titularidad**             | Copia literal con antigüedad no mayor a 7 días obtenida por consulta directa; certificados de no adeudo; verificación física del identificador único en video con código del día; declaración de estado civil | `ADMIN_LEGAL_COMPLIANCE`                                 | Cualquier gravamen, carga, embargo o litigio inscrito |
| **E3 Valoración**              | Tasación por perito, obligatoria en P-C2; referencias de mercado; regla de desviación de §7.3                                                                                                                 | `ADMIN_LEGAL_COMPLIANCE` + **segunda firma**             | Desviación superior al 50 %                           |
| **E4 Instrumento y bloqueo**   | Instrumento notarial de §8.2; **constancia de bloqueo registral vigente**; vigencia de poderes si el organizador es persona jurídica                                                                          | `ADMIN_LEGAL_COMPLIANCE`                                 | Bloqueo ausente o de vigencia insuficiente            |
| **E5 Publicación y venta**     | Divulgación obligatoria de §8.4; **reconsulta registral automática cada 7 días**                                                                                                                              | —                                                        | Gravamen sobrevenido: suspensión inmediata            |
| **E6 Preparación del ganador** | Identidad verificada; declaración de estado civil; capacidad legal; datos para el acto; **aceptación expresa e informada del premio incluidas cargas y costos**                                               | `SUPPORT_L2` verifica; `ADMIN_LEGAL_COMPLIANCE` habilita | Ganador no acredita condiciones o rechaza el premio   |
| **E7 Transferencia**           | Firma del acto; pago de tributos y derechos; presentación al registro; **verificación de inscripción por consulta directa**; aceptación del organizador; confirmación del ganador; atestación                 | `ADMIN_LEGAL_COMPLIANCE` + segunda firma                 | Observación no subsanable                             |

**RN-27 — Bloqueo registral.** El bloqueo debe cubrir toda la venta más el plazo de transferencia. Si su vigencia es menor, el sorteo se dimensiona para cerrar antes del vencimiento o se renueva antes de publicar. **Sin bloqueo vigente el sorteo P-C no se aprueba.**

**Fundamento.** Entre la verificación registral del go-live y la inscripción a nombre del ganador transcurren semanas o meses. En esa ventana el bien puede ser embargado, hipotecado o vendido, y un organizador arrepentido tiene incentivo para venderlo por fuera. La partida limpia verificada en el gate es una fotografía que caduca.

**RN-28 — Aceptación del pago por el organizador.** En E7, el organizador declara expresamente, como acto propio y firmado, que la transferencia se completó conforme a lo pactado y que acepta el pago. No es LIBOX quien lo declara por él.

## 8.4 Divulgación obligatoria en P-C

Antes de la compra: valor de tasación con fecha · todos los costos de transferencia y quién los asume · **cargas recurrentes que el ganador heredará** · plazo estimado de transferencia · requisitos que el ganador deberá cumplir · estado de ocupación cuando aplique · advertencia tributaria cuando el dictamen legal del mercado la determine.

## 8.5 Qué significa proceso mecánico

Manual no puede significar discrecional: si una persona decide con criterio propio sobre un activo de alto valor, no hay proceso, hay una persona.

| \#    | Regla                                                                                                        |
| ----- | ------------------------------------------------------------------------------------------------------------ |
| RN-29 | Lista cerrada de documentos por etapa, cada uno con estado tipificado. No existe campo “otros”               |
| RN-30 | La consulta registral la realiza LIBOX directamente; el documento de una parte nunca es fuente de verdad     |
| RN-31 | La aprobación es una casilla, no una opinión. **No existe “aprobar con observaciones”**                      |
| RN-32 | Motivo obligatorio de al menos 100 caracteres en toda aprobación de etapa P-C                                |
| RN-33 | Sin avance parcial: no se pasa a la etapa siguiente con la anterior incompleta, sin excepción por reputación |
| RN-34 | Cada verificación registra quién, cuándo, contra qué fuente, con qué resultado y con hash del documento      |
| RN-35 | Cada etapa tiene plazo propio; el vencimiento escala automáticamente                                         |
| RN-36 | Todo cambio de etapa se publica en la línea de tiempo pública del sorteo                                     |

**RN-37 — Criterio de automatización.** El proceso se automatiza únicamente cuando exista una vía técnica de verificación registral reconocida por la autoridad del mercado. Hasta entonces permanece mecánico. Es criterio, no estado de hecho.

## 8.6 Rutas de fallo en P-C

| Fallo                                                             | Etapa | Resolución                                                                                   | Comisión    | Participantes     |
| ----------------------------------------------------------------- | ----- | -------------------------------------------------------------------------------------------- | ----------- | ----------------- |
| Gravamen detectado durante la venta                               | E5    | Suspensión inmediata y cancelación                                                           | No se cobra | Reembolso íntegro |
| Bloqueo vencido sin renovar                                       | E5    | 15 días para renovar; en su defecto, cancelación                                             | No se cobra | Reembolso íntegro |
| Ganador rechaza el premio o no acredita                           | E6    | Ruta declarada del sorteo (§16)                                                              | Según ruta  | Según ruta        |
| Organizador no firma el acto                                      | E7    | Cancelación, penalización máxima y evaluación de acciones                                    | No se cobra | Reembolso íntegro |
| Observación registral subsanable                                  | E7    | 30 días de subsanación, prorrogables 30 con motivo                                           | Suspendida  | Informados        |
| Observación no subsanable                                         | E7    | Cancelación                                                                                  | No se cobra | Reembolso íntegro |
| Organizador se niega a aceptar el pago con transferencia inscrita | E7    | Escala a `ADMIN_SUPER`; con inscripción verificada se libera el pago con resolución motivada | Se cobra    | Sin efecto        |

**RN-38.** En toda cancelación el reembolso está financiado por la recaudación retenida. El costo de la comisión del proveedor de pagos, ya devengado, lo absorbe LIBOX: es el precio de un gate mal aplicado y el argumento operativo para que E2 y E4 sean estrictos.

# 9\. Pricing y modelo financiero

## 9.1 Fórmula

Definida en §1.3. El asistente de creación incluye un **simulador** que muestra al organizador, antes de enviar a revisión, la recaudación bruta requerida, la comisión, su neto, el precio de ticket propuesto y el número de tickets resultante.

**RN-39.** El simulador es público y accesible sin registro. Es la superficie de captación de organizadores de mayor conversión y utiliza la fórmula real, no una aproximación.

## 9.2 Composición del resultado

    recaudación_bruta   = tickets_vendidos × precio_ticket
    comisión_libox      = recaudación_bruta × 0,20
    costo_psp           = f( canal, monto, mercado )
    impuesto            = f( régimen del mercado )
    neto_liquidable     = recaudación_bruta − comisión_libox − ajustes
    ingreso_libox       = comisión_libox − costo_psp − impuesto

**RN-40.** `costo_psp` e `impuesto` se registran como asientos propios en el ledger. No se descuentan implícitamente. Sin asentarlos, el margen reportado es falso desde la primera transacción.

**RN-40-ter — La emisión de comprobante depende del régimen del organizador.** Una persona natural sin identificador tributario no puede emitir comprobante, de modo que la pregunta de quién emite al comprador del ticket **tiene dos respuestas posibles según el régimen**. Es materia del dictamen L-05 y determina si el régimen de persona natural es operable en cada mercado.

**RN-40-bis — El impuesto está incluido en la comisión, no se añade sobre ella.**

    impuesto        = redondeo( comision_libox × tasa / (1 + tasa) )
    ingreso_neto    = comision_libox − impuesto

Es la única lectura compatible con la promesa comercial: si el impuesto fuera adicional, el organizador recibiría menos del 80 % del bruto y “comisión all-inclusive” sería falso.

| \#     | Invariante                                                                                                  |
| ------ | ----------------------------------------------------------------------------------------------------------- |
| INV-34 | `neto_liquidable` es siempre el 80 % del bruto, con independencia del régimen tributario del mercado        |
| INV-35 | El impuesto nunca supera la comisión. Un resultado mayor indica configuración errónea y aborta la operación |
| INV-36 | La diferencia por redondeo se imputa al ingreso de la plataforma, **jamás al neto del organizador**         |

La tasa, la base y el sujeto obligado provienen de la configuración por mercado. **Que el impuesto aplique sobre la comisión permanece sujeto a dictamen (L-05);** lo que esta versión fija es la mecánica: si aplica, se extrae de la comisión.

**RN-41.** El desglose se congela en cada orden, con invariante `client_net + libox_fee = gross`.

## 9.3 Rango y mínimos

| Parámetro                        | Origen          |
| -------------------------------- | --------------- |
| Precio mínimo y máximo de ticket | `market_config` |
| Importe mínimo de compra         | `market_config` |
| Múltiplo de redondeo             | `market_config` |

**RN-42 — Importe mínimo de compra.** Existe un importe mínimo por operación, definido por mercado, cuyo propósito es amortizar el costo fijo del proveedor de pagos sin elevar el precio unitario del ticket. Se expresa en importe, no en cantidad de tickets.

# 10\. Contabilidad

## 10.1 Partida doble

**RN-43.** Toda operación con efecto patrimonial se registra como asiento balanceado: la suma de débitos iguala la suma de créditos por transacción (INV-10). Un asiento que no cuadra no se persiste; la operación falla.

## 10.2 Plan de cuentas

| Cuenta                    | Naturaleza | Contenido                                              |
| ------------------------- | ---------- | ------------------------------------------------------ |
| `cash_clearing`           | Activo     | Efectivo en tránsito                                   |
| `psp_clearing`            | Activo     | Fondos en poder del proveedor de pagos                 |
| `purchase_liability`      | Pasivo     | Obligación frente al participante por tickets vendidos |
| `client_payable`          | Pasivo     | Obligación frente al organizador, por cliente          |
| `refund_credit_liability` | Pasivo     | Saldo de reembolso pendiente de uso o retiro           |
| `platform_revenue`        | Ingreso    | Comisión devengada                                     |
| `psp_fee_expense`         | Gasto      | Comisión del proveedor de pagos                        |
| `tax_payable`             | Pasivo     | Impuesto por pagar                                     |
| `refund_reserve`          | Pasivo     | Provisión de reembolsos                                |
| `chargeback_reserve`      | Pasivo     | Retención por ventana de contracargo                   |
| `adjustment`              | Resultado  | Ajustes administrativos con motivo                     |

**RN-44.** Las cuentas se instancian por moneda. No existe cuenta multimoneda ni conversión en el MVP.

## 10.3 Transacciones canónicas

| \#   | Transacción                              | Débito                              | Crédito                                   |
| ---- | ---------------------------------------- | ----------------------------------- | ----------------------------------------- |
| T-01 | Confirmación de pago                     | `psp_clearing`                      | `purchase_liability`                      |
| T-02 | Devengo de comisión del PSP              | `psp_fee_expense`                   | `psp_clearing`                            |
| T-03 | Emisión de tickets                       | —                                   | Sin efecto patrimonial; evento de dominio |
| T-04 | Devengo de comisión de plataforma        | `purchase_liability`                | `platform_revenue`                        |
| T-05 | Devengo de obligación con el organizador | `purchase_liability`                | `client_payable`                          |
| T-06 | Devengo de impuesto                      | `platform_revenue`                  | `tax_payable`                             |
| T-07 | Retención por contracargo                | `client_payable`                    | `chargeback_reserve`                      |
| T-08 | Liquidación al organizador               | `client_payable`                    | `cash_clearing`                           |
| T-09 | Liberación de retención                  | `chargeback_reserve`                | `client_payable`                          |
| T-10 | Cancelación de sorteo                    | `purchase_liability`                | `refund_credit_liability`                 |
| T-11 | Uso de saldo de reembolso en compra      | `refund_credit_liability`           | `purchase_liability`                      |
| T-12 | Retiro de saldo de reembolso             | `refund_credit_liability`           | `cash_clearing`                           |
| T-13 | Contracargo recibido                     | `purchase_liability` o `adjustment` | `psp_clearing`                            |
| T-14 | Ajuste administrativo                    | Según naturaleza                    | Según naturaleza, con motivo obligatorio  |

**RN-45.** T-04, T-05 y T-06 se devengan al confirmarse el pago, no al liquidar. La liquidación (T-08) mueve una obligación ya devengada. **RN-46.** T-14 exige motivo y segunda firma.

## 10.4 Reconciliación

**RN-47.** Ejecución diaria de conciliación contra el reporte del proveedor de pagos, con emparejamiento por referencia y **cola de excepciones con plazo de resolución**. Toda excepción sin resolver genera alarma.

**RN-48.** Verificación diaria de invariantes: cuadre de asientos por transacción, correspondencia entre saldo de reembolso agregado y su cuenta de pasivo, y suficiencia de la recaudación retenida frente a la obligación de reembolso de cada sorteo activo (INV-16). Toda divergencia genera alarma de severidad alta.

## 10.5 Pago al organizador

**RN-49.** El desembolso exige datos de cobro verificados y a nombre del mismo titular del KYB. Sin coincidencia no hay liquidación. **RN-50.** El desembolso lo ejecuta `ADMIN_FINANCE`. En categorías registrables se ejecuta caso por caso con **segunda firma**; en el resto, por lote. **RN-51.** Todo pago registra instrucción, referencia bancaria, constancia y asiento asociado.

# 11\. Pagos

## 11.1 Modelo

Checkout directo por operación. **No existe wallet con recarga.** El único saldo del usuario es el saldo de reembolso (§16.5), que no admite carga voluntaria.

## 11.2 Idempotencia

**RN-52.** Toda operación mutante de dinero exige cabecera de idempotencia con clave **provista por el cliente y única por intento**.

**Corrección respecto de V1.** V1 derivaba la clave de un hash del cuerpo de la solicitud. Dos compras legítimas del mismo usuario, en el mismo sorteo, por la misma cantidad, producían el mismo hash: la segunda devolvía la respuesta de la primera y **el usuario no recibía sus tickets**. La clave debe ser generada por el cliente por intento, no derivada del contenido.

**RN-53.** La clave es única por actor, endpoint y clave, con vigencia de 24 horas. La respuesta almacenada se devuelve ante repetición.

## 11.3 Reserva de inventario

**RN-54.** La reserva de tickets es atómica y condicional sobre el propio contador del sorteo, verificando filas afectadas. Serializar por usuario es insuficiente: la carrera real ocurre sobre el pool.

**RN-55.** La reserva expira con la preferencia del proveedor de pagos y libera el inventario. El plazo proviene de `market_config`.

**RN-56.** El bloqueo autoritativo de saldo y de inventario es de base de datos. Un bloqueo distribuido en memoria es optimización, nunca garantía: un fallo de conmutación produciría dos poseedores del mismo bloqueo y doble gasto.

## 11.4 Webhooks

**RN-57.** Validación de firma con ventana anti-repetición sobre la marca temporal del proveedor. **RN-58.** Deduplicación por identificador de evento del proveedor. Todo evento se persiste con su carga original y su hash antes de procesarse. **RN-59 — Monotonía de estado.** Un evento tardío no retrocede un estado ya avanzado. Los webhooks llegan desordenados y duplicados. **RN-60.** Todo evento no procesable entra en cola de excepciones con alarma, nunca se descarta.

## 11.5 Contracargos

**RN-61.** Un contracargo recibido genera asiento T-13, alarma de severidad alta, y evaluación de riesgo sobre el usuario. **RN-62.** Un contracargo **no invalida tickets de un sorteo ya ejecutado**. Invalidar retroactivamente rompería la integridad del pool y la prueba criptográfica. La pérdida se gestiona contra la reserva y contra el usuario. **RN-63.** La existencia de contracargos abiertos sobre un sorteo bloquea el gate G4 de liquidación.

## 11.6 Reembolsos

**RN-64.** Todo reembolso por cancelación se abona como saldo de reembolso (T-10), es inmediato y no requiere acción del usuario. **RN-65.** Existe ruta de retiro a cuenta bancaria por solicitud manual con verificación de identidad (§16.5).

# 12\. Motor de sorteo

## 12.1 Garantía

Un sorteo de LIBOX es **verificable por un tercero sin confiar en LIBOX**. Esto exige que la aleatoriedad esté comprometida públicamente **antes** de conocerse el resultado.

**Problema que V2 corrigió.** V1 no contenía el algoritmo: la palabra `seed` no aparecía en el documento. El algoritmo del PRD Enterprise obtenía entropía pública **en el momento de ejecutar**, sin compromiso previo, de modo que quien opera el sorteo podía obtenerla, calcular el resultado y, si no le convenía, repetir la operación. Su función de verificación recomputaba a partir del valor almacenado por LIBOX: verificaba **consistencia aritmética, no honestidad**.

## 12.2 Esquema de compromiso y revelación

**En el congelamiento del pool (**`POOL_FROZEN`**)** se publica y sella temporalmente:

| Elemento                       | Contenido                                                                 |
| ------------------------------ | ------------------------------------------------------------------------- |
| `pool_hash`                    | Hash del pool canónicamente serializado, ordenado por número de ticket    |
| `commitment`                   | Hash de una semilla secreta de servidor, aún no revelada                  |
| `beacon_source` y `beacon_ref` | Fuente pública de entropía y **ronda futura anunciada**, aún no producida |

**En la ejecución:**

    seed_material = H( server_seed ‖ beacon_value ‖ pool_hash ‖ raffle_id ‖ algorithm_version )

Se revela `server_seed`.

**Verificación pública, sin autenticación:**

1.  `H(server_seed)` coincide con el `commitment` publicado **antes** del sorteo
2.  La ronda comprometida es **posterior** a la publicación del compromiso, comprobado **contra la fuente de baliza**, no contra un dato de LIBOX
3.  `beacon_value` corresponde a esa ronda en la fuente
4.  Recomputación del resultado a partir de los valores publicados

**INV-18.** Existe una ventana mínima entre la publicación del compromiso y la disponibilidad de la baliza. La ronda de baliza es futura respecto de la publicación del compromiso. El plazo mínimo proviene de `market_config`.

**INV-18-bis — La anterioridad del compromiso debe ser comprobable sin confiar en LIBOX.** Junto al identificador de la ronda se publica una **propiedad intrínseca de esa ronda** —número, altura o instante—, verificable consultando la propia fuente de baliza.

Una marca temporal de obtención escrita por LIBOX no sirve como prueba: un tercero no puede distinguir “esta ronda no existía al comprometer” de “declaramos haberla obtenido después”. Sin la propiedad intrínseca se verifica que la aritmética cuadra, no que el sorteo fue honesto, que es precisamente la brecha que este diseño existe para cerrar.

**INV-19.** El resultado de un sorteo no es re-ejecutable. La garantía es una restricción de unicidad sobre la ejecución en base de datos; el bloqueo distribuido es optimización.

## 12.3 Requisitos delegados a L3

`draw-engine-spec.md` especifica de forma completa y con vectores de prueba: serialización canónica del pool al byte, incluyendo orden, codificación y separadores; función de derivación y selección; **selección sin reemplazo para T6**; e implementación de la verificación pública.

**RN-66.** Sin serialización canónica especificada al byte y con vectores de prueba, dos implementaciones honestas producen hashes distintos y la verificación falla. Es requisito de aceptación, no detalle.

## 12.4 Superficie pública de verificación

**RN-67.** Existe una página pública, sin autenticación e indexable, por cada sorteo ejecutado, que muestra: identificador del sorteo, pool y su hash, compromiso con su marca temporal, fuente de baliza con la **propiedad intrínseca de la ronda**, semilla revelada, resultado, y el procedimiento de verificación en lenguaje llano con enlace a la especificación y a la fuente de baliza.

**RN-67-bis.** La página indica explícitamente qué debe comprobarse **fuera de LIBOX**: la ronda de baliza y su valor se consultan en la fuente pública. Una verificación que solo consultara a LIBOX confirmaría la aritmética de la parte cuya honestidad pretende comprobar.

**RN-68.** La página **no divulga identidad de participantes ni distribución de tenencia** (R-10). Muestra números de ticket y el número ganador.

## 12.5 Congelamiento

**RN-69.** El congelamiento del pool es automático al satisfacerse la condición del tipo. Ningún rol lo adelanta ni lo retrasa. **RN-70.** Congelado el pool, no se admiten nuevas ventas, anulaciones ni modificaciones sobre él. **RN-71.** Un sorteo sin tickets válidos no llega a congelamiento: transita a cancelación.

# 13\. Sala de Resolución y conformidad de entrega

## 13.1 Creación y participación

**RN-72.** Al ejecutarse el sorteo, el sistema crea automáticamente una Sala de Resolución identificada con el `raffle_code`.

| Participante             | Entra cuando                                                         | Escribe | Aporta evidencia   | Cambia estado                                      |
| ------------------------ | -------------------------------------------------------------------- | ------- | ------------------ | -------------------------------------------------- |
| USER ganador             | Al ejecutarse el sorteo                                              | Sí      | Sí                 | No                                                 |
| CLIENT                   | **Cuando el ganador reclama y consiente compartir datos de entrega** | Sí      | Sí                 | No                                                 |
| SUPPORT asignado         | Asignación automática                                                | Sí      | Sí, notas internas | Sí, atesta                                         |
| Resto de SUPPORT y ADMIN | —                                                                    | No      | No                 | No. **Consultan la cola completa en solo lectura** |
| `SUPPORT_SUPERVISOR`     | Bajo demanda                                                         | Sí      | Sí                 | Sí, reasigna y revierte                            |

**RN-73.** El organizador no accede a la sala antes del reclamo. Los datos del ganador no se exponen hasta que este acepta participar en la entrega.

**RN-74 — Asignación.** Distribución equilibrada por carga, con prioridad por valor del premio y por plazo próximo a vencer. Reasignación por `SUPPORT_SUPERVISOR` con motivo.

**Fundamento de la visibilidad en solo lectura.** Incorporar a la totalidad del equipo como participante de cada sala produce, con volumen operativo real, que cada agente pertenezca a centenares de salas y que ninguna notificación signifique nada, además de vulnerar el principio de menor privilegio. La cola compartida entrega la supervisión sin el ruido.

## 13.2 Naturaleza probatoria

La sala **es la prueba** en una eventual controversia ante autoridad de consumo o judicial. No es un canal de soporte.

| \#    | Requisito                                                                                                                               |
| ----- | --------------------------------------------------------------------------------------------------------------------------------------- |
| RN-75 | Solo agregación. Ningún mensaje se edita ni se elimina, por nadie, incluido ADMIN. Retractarse se hace publicando una corrección        |
| RN-76 | Cada mensaje incorpora hash de su contenido y hash del mensaje anterior. Manipular el historial rompe la cadena de forma detectable     |
| RN-77 | Sellado temporal con hora de servidor                                                                                                   |
| RN-78 | Toda evidencia con hash, tipo validado, análisis antivirus, límite de tamaño y almacenamiento con dirección firmada de expiración corta |
| RN-79 | Separación estricta entre mensajes visibles a las partes y notas internas                                                               |
| RN-80 | Exportable como paquete forense firmado: documento consolidado, adjuntos y manifiesto de hashes                                         |
| RN-81 | Al cerrar el caso, la sala pasa a solo lectura y se archiva con su hash raíz                                                            |

## 13.3 Minimización de datos personales

**RN-82.** Se comparte con el organizador exclusivamente lo necesario para entregar: nombre y apellido inicial, y dirección de entrega únicamente si el premio es físico y con consentimiento explícito registrado. Nunca documento completo, ni correo, ni teléfono. Si la logística requiere contacto telefónico, se realiza mediante intermediación de la plataforma con enmascaramiento.

**RN-83.** Todo consentimiento es informado, específico, registrado y revocable.

## 13.4 Ciclo de resolución

| Estado                                                          | Significado                   | Plazo                      |
| --------------------------------------------------------------- | ----------------------------- | -------------------------- |
| `ROOM_OPENED`                                                   | Sala creada                   | —                          |
| `AWAITING_CLAIM`                                                | Esperando reclamo del ganador | Por tramo de valor (§16.2) |
| `CLAIMED`                                                       | Ganador reclamó               | —                          |
| `SHIPPING_QUOTED`                                               | Organizador cotizó envío      | 7 días para elegir y pagar |
| `SHIPPING_PAID` / `PICKUP_AGREED`                               | Logística resuelta            | —                          |
| `AWAITING_DELIVERY`                                             | En entrega                    | Por categoría (§6.1)       |
| `EVIDENCE_SUBMITTED`                                            | Evidencia aportada            | —                          |
| `NEEDS_MORE_EVIDENCE`                                           | Evidencia insuficiente        | Retorna a entrega          |
| `ATTESTED`                                                      | Entrega atestada              | Alimenta gate G2           |
| `DISPUTED`                                                      | Controversia abierta          | §14                        |
| `SHIPPING_ABANDONED`                                            | Envío no pagado ni recogido   | §16                        |
| `NO_CLAIM_EXPIRED`                                              | Plazo de reclamo vencido      | §16                        |
| `RESOLVED_DELIVERED` · `RESOLVED_REDRAW` · `RESOLVED_CANCELLED` | Terminales                    | —                          |

**INV-20.** Solo `SUPPORT_L2`, `SUPPORT_SUPERVISOR` y `ADMIN` cambian el estado de la sala. Organizador y ganador aportan hechos y evidencia; no mueven la máquina.

**RN-84 — Envío no pagado.** Cotización con al menos dos opciones de transportista formal; 7 días para elegir y pagar, más 7 de gracia; vencidos, `SHIPPING_ABANDONED`, que se trata como no reclamo a efectos de §16.

**RN-85 — Atestación en registrables.** En P-C1 y P-C2 la atestación no la emite SUPPORT: la emite `ADMIN_LEGAL_COMPLIANCE` con segunda firma, y exige verificación de inscripción por consulta directa, aceptación del organizador y confirmación del ganador.

## 13.5 Cadena de atestación a liquidación

    SUPPORT_L2 emite DELIVERY_ATTESTED
       → No mueve dinero. Es un hecho operativo firmado.
       → Alimenta el gate G2.
    
    El SISTEMA evalúa los seis gates de forma determinista, sin criterio humano.
       → Satisfechos los seis: la liquidación pasa a ELIGIBLE automáticamente.
    
    ADMIN_FINANCE ejecuta el desembolso.
       → Único punto donde el dinero se mueve.
       → La comisión se devenga en el mismo asiento.

**INV-21.** Ningún rol puede completar por sí solo la cadena que termina en un desembolso.

## 13.6 Plazos: casuística

**RN-86.** Zona horaria del mercado del sorteo. Días calendario, salvo categorías registrables que usan días hábiles por depender de notaría y registro. Calendario de feriados por mercado; vencimiento en feriado se corre al siguiente hábil.

**RN-87.** Todo plazo se cuenta desde un evento de sistema con sello de servidor, nunca desde una fecha declarada por una parte.

| Evento                                               | Efecto sobre el plazo                                                              |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Solicitud de dato o evidencia al ganador             | Pausa hasta respuesta, máximo 5 días acumulados                                    |
| Necesidad de evidencia adicional emitida por SUPPORT | Pausa hasta nueva aportación, máximo 5 días                                        |
| Controversia abierta                                 | Congela plazo y liquidación hasta resolución                                       |
| Extensión por `SUPPORT_L2`                           | Máximo 10 días, con motivo y **notificación a todos los participantes del sorteo** |
| Extensión por `SUPPORT_SUPERVISOR`                   | Hasta 20 días adicionales, motivo reforzado                                        |
| Extensión mayor                                      | Solo ADMIN con segunda firma                                                       |
| Caso fortuito o fuerza mayor documentado             | Suspensión con revisión cada 15 días                                               |

**RN-88.** Toda extensión se publica en la sala y se notifica a los participantes del sorteo, no solo al ganador. Quienes no ganaron también tienen derecho a saber que el sorteo sigue abierto.

**RN-89 — Propuesta de plazo por el organizador.** LIBOX propone el plazo base de la categoría. El organizador puede proponer uno **mayor, nunca menor**, justificándolo documentalmente. El aprobador del gate lo valida. **El plazo aprobado se publica en la tarjeta y en las bases antes de la venta** y es inmutable tras publicar.

# 14\. Controversias

## 14.1 Principio

**INV-22 (DP-16).** Toda controversia se resuelve **sobre evidencia clasificada por fuerza probatoria, nunca sobre la afirmación de una sola parte, en ninguna de las dos direcciones.**

Marco de referencia: normas internacionales de gestión de quejas y de resolución externa de controversias, y notas técnicas sobre resolución de controversias en línea, cuyos principios rectores son imparcialidad, transparencia, debido proceso y decisión basada en evidencia.

## 14.2 Jerarquía de evidencia

Clasificada por el sistema, no por el agente.

| Fuerza     | Evidencia                                                                                                                                                                                                                                           |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **FUERTE** | Guía de transportista formal con seguimiento y constancia de recepción firmada · Partida registral inscrita obtenida por consulta directa · Documentos de servicio emitidos con localizador verificable · Constancia de canje emitida por el emisor |
| **MEDIA**  | Evidencia gráfica del bien con el ganador y el código del día · Acta de entrega firmada por ambas partes · Confirmación del proveedor                                                                                                               |
| **DÉBIL**  | Imagen sin código del día · Captura de conversación · Declaración de una parte                                                                                                                                                                      |

## 14.3 Inversión de la carga de la prueba

**RN-90.** Si el organizador aporta evidencia FUERTE y el ganador niega la recepción, el caso **no lo cierra SUPPORT**: escala a `ADMIN_LEGAL_COMPLIANCE` como controversia adjudicada, y el ganador debe rebatir con evidencia, no con aserción.

**RN-91.** Simétricamente, sin evidencia FUERTE ni MEDIA del organizador, prevalece la posición del ganador.

**Fundamento.** Un procedimiento que resuelve por afirmación crea incentivo a afirmar en falso, y ese incentivo recae siempre sobre la parte con menos que perder. La simetría probatoria, junto con consecuencias reputacionales para ambas partes, desactiva ese incentivo.

## 14.4 Controles de integridad del canal

| \#    | Control                                                                                                                                                                                                                                                                          |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RN-92 | **Reclamo estructurado.** Quien niega la recepción selecciona un motivo de lista cerrada y aporta evidencia obligatoria. Un reclamo sin motivo tipificado y sin evidencia no abre controversia                                                                                   |
| RN-93 | **Contacto confinado.** Compartir teléfono, correo, redes o datos bancarios dentro de la sala se detecta y bloquea, con evento de riesgo. La coordinación logística usa campos estructurados                                                                                     |
| RN-94 | **Detección de oferta monetaria.** Toda mención de transferencia, pago, arreglo o compensación entre las partes genera alerta, congela el caso y escala a `ADMIN_RISK`. Protege simultáneamente contra la extorsión del ganador y contra la colusión entre organizador y ganador |
| RN-95 | **Reputación bidireccional.** Un reclamo de mala fe determinado por adjudicación penaliza al usuario, y la reincidencia le retira la condición de verificado                                                                                                                     |

## 14.5 Adjudicación

**RN-96.** Adjudica `ADMIN_LEGAL_COMPLIANCE`, nunca quien atestó ni quien valoró el sorteo (INC-08). **RN-97.** Resolución escrita y motivada sobre la jerarquía de §14.2, en plazo de 10 días desde el escalamiento. **RN-98.** Notificación a ambas partes con el fundamento, en lenguaje llano y no adversarial. **RN-99.** Consecuencias reputacionales para la parte de mala fe, en cualquiera de las dos direcciones. **RN-100.** Todo el expediente integra el paquete forense exportable.

# 15\. Liquidación

## 15.1 Los seis gates

**RN-101.** Una liquidación pasa de devengada a elegible únicamente cuando se satisfacen **todos**:

| Gate                 | Condición                                                            |
| -------------------- | -------------------------------------------------------------------- |
| **G1** Sorteo        | Ejecutado con prueba válida y verificable                            |
| **G2** Entrega       | Atestación emitida por el rol competente según categoría             |
| **G3** Controversias | Cero controversias abiertas sobre el sorteo                          |
| **G4** Contracargos  | Ventana de retención cumplida y sin contracargos abiertos            |
| **G5** Cobro         | Datos de cobro verificados y a nombre del titular del KYB            |
| **G6** Contabilidad  | Ledger del sorteo cuadrado, sin excepciones de conciliación abiertas |

**INV-23.** La evaluación de los seis gates es determinista y automática. Ningún rol la sustituye por criterio.

## 15.2 Estados

`ACCRUED` → `ELIGIBLE` → `APPROVED` → `PAID`, con estados alternativos `HELD` y `REVERSED`.

**RN-102.** El estado `HELD` se muestra al organizador como **Retenido**, con el motivo y el plazo estimado. El panel del organizador expone tres estados: Pendiente, Retenido y Pagado.

## 15.3 Retención por contracargo

**RN-103.** El gate G4 exige una ventana de retención desde la atestación, cuyo plazo proviene de `market_config`.

**RN-104 — Reserva de contracargo.** Se retiene un porcentaje del neto, definido por mercado, hasta el vencimiento de la ventana extendida de contracargo, con asiento T-07 y liberación T-09.

**Fundamento.** La ventana de contracargo de un medio de pago supera con holgura el plazo que separa la entrega de la liquidación. Sin retención ni reserva, existe un descalce estructural que constituye la pérdida no acotada más probable del negocio.

## 15.4 Visibilidad de plazos al organizador

**RN-105.** Antes de publicar, el organizador visualiza el plazo máximo estimado hasta el cobro, compuesto por el plazo de reclamo aplicable, el de entrega de la categoría y la ventana de retención. En categorías registrables y en escenarios con re-sorteo el plazo se recalcula y se comunica.

**Fundamento.** Un organizador que desconoce que su cobro puede demorar meses interpreta la espera como retención indebida. La transparencia del plazo evita el conflicto antes de que exista.

# 16\. Premio no reclamado o no entregado

## 16.1 Ruta declarada

**INV-24.** La ruta de resolución —re-sorteo o cancelación— **la elige el organizador al crear el sorteo**, se publica en las bases y es **inmutable tras la publicación**. Ningún operador la elige caso por caso.

**Fundamento.** El operador decide **cuándo** se dispara un vencimiento y **si** la evidencia es suficiente. No decide **qué** ocurre después. Lo contrario convertiría una decisión patrimonial de alto valor en criterio de un agente, y sería indefendible ante una reclamación.

**RN-106.** En categorías registrables la ruta es **cancelación obligatoria**. El re-sorteo exigiría que el nuevo ganador repitiera la acreditación legal completa mientras el bloqueo registral sigue corriendo, y puede no caber en su vigencia.

## 16.2 Plazos de reclamo por valor

| Valor aprobado del premio | Plazo de reclamo |
| ------------------------- | ---------------- |
| ≤ S/ 3.000                | **7 días**       |
| S/ 3.001 – 10.000         | **15 días**      |
| \> S/ 10.000              | **30 días**      |

**RN-107.** El valor rector es el **valor aprobado en el gate**, no el declarado, y queda congelado al publicar. Los límites son inclusivos hacia arriba. Los umbrales provienen de `market_config`.

## 16.3 Escenarios

**Ganador no reclama**

    AWAITING_CLAIM → vencimiento del plazo del tramo
      → SUPPORT confirma agotamiento de contacto
      → NO_CLAIM_EXPIRED
           ├─ ruta re-sorteo   → §16.4, sin costo para el nuevo ganador
           └─ ruta cancelación → reembolso íntegro a saldo de reembolso

**Organizador no entrega**

    AWAITING_DELIVERY → vencimiento del plazo de categoría
      → recordatorio y advertencia de penalización
      → NO_DELIVERY → CANCELACIÓN OBLIGATORIA
           · Reembolso íntegro a todos los participantes
           · LIBOX no cobra comisión: no hubo servicio prestado
           · Penalización reputacional, suspensión de capacidades
             y evaluación de acciones

**INV-25.** El re-sorteo **nunca** aplica al incumplimiento del organizador. Si el premio no existe, re-sortearlo es sortear nada.

## 16.4 Re-sorteo seguro

**RN-108.** Condiciones acumulativas, todas obligatorias:

1.  Causa exclusiva: plazo de reclamo vencido con contacto agotado y documentado
2.  Ruta declarada en las bases publicadas antes de la primera venta
3.  Pool derivado excluyendo los tickets del ganador original
4.  **Compromiso nuevo y completo**: hash de nueva semilla y ronda de baliza futura publicados con al menos 24 horas de antelación
5.  Encadenamiento explícito a la ejecución original; la página pública muestra la cadena completa y el motivo
6.  **Máximo un re-sorteo por sorteo.** Al segundo fallo, cancelación y reembolso íntegro
7.  Autoriza ADMIN. SUPPORT no autoriza re-sorteos
8.  **Los plazos se reevalúan** y se recomunican a todos los participantes

**Fundamento del punto 4.** Un re-sorteo que reutiliza el compromiso original con entropía nueva obtenida en el momento institucionaliza el ataque por repetición y entrega un mecanismo formal para repetir sorteos. El compromiso nuevo con baliza futura anunciada lo impide.

## 16.5 Saldo de reembolso

**INV-26.** El saldo de reembolso se origina **exclusivamente** en cancelaciones y en concesiones promocionales. **No admite carga voluntaria por el usuario.**

| Propiedad    | Regla                                                                           |
| ------------ | ------------------------------------------------------------------------------- |
| Vigencia     | **No expira**                                                                   |
| Uso          | Aplicable a la compra de tickets en la plataforma, en la misma moneda de origen |
| Retiro       | A cuenta bancaria **por solicitud manual con verificación de identidad**        |
| Cómputo      | **Cuenta como gasto** en los acumuladores y frente a los límites autoimpuestos  |
| Contabilidad | Cuenta de pasivo propia; asientos T-10, T-11 y T-12                             |

**Fundamento del cómputo.** Si el uso del saldo no contara como gasto, sería una vía trivial para eludir el límite que el propio usuario se fijó, y la herramienta perdería sentido.

**RN-109.** Reporte periódico de antigüedad del saldo no utilizado y comunicación proactiva al titular. Un pasivo dormido creciente es un problema contable si escala.

## 16.6 Contacto con el ganador

**RN-110.** Los avisos críticos se emiten obligatoriamente por **correo y por mensajería o SMS**. La notificación instantánea nunca es canal único: en algunos sistemas operativos móviles solo funciona con la aplicación web instalada, lo que no puede presumirse.

**RN-111.** Cadencia por tramo de plazo:

| Tramo   | Días de contacto       |
| ------- | ---------------------- |
| 7 días  | 0, 1, 3, 5, 6          |
| 15 días | 0, 1, 3, 7, 11, 14     |
| 30 días | 0, 1, 3, 7, 14, 21, 28 |

**RN-112.** Cada intento registra canal, destino enmascarado, plantilla, sello temporal de servidor y estado devuelto por el proveedor. **RN-113.** En premios superiores al primer tramo, **llamada telefónica registrada por SUPPORT** antes del vencimiento. **RN-114.** Si todos los canales rebotan, **se congela el plazo** y escala a SUPPORT para búsqueda alternativa antes de declarar el vencimiento. Un dato de contacto desactualizado no es negligencia del ganador.

# 17\. Identidad, edad y verificación

## 17.1 Unicidad

**INV-08.** Un documento de identidad, un correo y un teléfono corresponden a exactamente un usuario activo.

**RN-115.** La unicidad se hace cumplir en el registro y en la verificación. Un intento de registro con documento ya asociado se rechaza con error tipificado y genera evento de riesgo.

**Fundamento.** La unicidad no es un control antifraude accesorio: es la condición para que los límites de concentración, los topes de gasto, la autoexclusión y la protección de menores signifiquen algo. Sin ella, todos los controles son evadibles creando otra cuenta.

## 17.2 Verificación de mayoría de edad

| Puerta               | Momento                        | Método                                                                                   | Bloquea               |
| -------------------- | ------------------------------ | ---------------------------------------------------------------------------------------- | --------------------- |
| **G-A** Declaración  | Registro                       | Fecha de nacimiento obligatoria y aceptación expresa                                     | Registro si es menor  |
| **G-B** Verificación | **Antes de la primera compra** | Documento de identidad validado contra fuente oficial del mercado **más prueba de vida** | Compra, no navegación |

**RN-116.** La prueba de vida es obligatoria y es el control que ata la edad a la persona. La unicidad previene multicuenta; **solo la prueba de vida impide que alguien use el documento de otro**.

**RN-117.** No se exige comprobante de domicilio para la verificación de edad: acredita domicilio, no edad, y su exigencia en el registro destruye la conversión sin aportar al control.

**RN-118.** La fecha de nacimiento no es editable tras la verificación.

**RN-119.** Todo intento de registro de un menor se registra como evento de riesgo y bloquea permanentemente el documento.

## 17.3 Menor detectado con posterioridad

**RN-120.** Existe protocolo escrito con casuística por categoría de premio, aprobado por asesoría legal. Marco: bloqueo permanente de la cuenta; reembolso íntegro de tickets en sorteos no ejecutados; en sorteos ya ejecutados los tickets permanecen válidos en el pool —no se altera la prueba— y el premio se gestiona con el representante legal conforme a la casuística de la categoría.

**Fundamento de no invalidar retroactivamente.** Anular tickets de un sorteo ya ejecutado rompería la integridad del pool y de la prueba criptográfica, perjudicando a terceros que actuaron de buena fe.

## 17.4 Titularidad del medio de pago

**RN-121.** El titular del medio de pago **puede** ser distinto del usuario verificado. Cada caso genera registro auditable.

**RN-122.** El cambio recurrente de titular del medio de pago acumula alertas y eleva el nivel de riesgo del usuario.

**RN-123 — Medio de pago compartido:**

| Usuarios distintos con el mismo medio | Tratamiento               |
| ------------------------------------- | ------------------------- |
| 2                                     | Normal, sin alerta        |
| 3 a 4                                 | Alerta informativa        |
| 5 o más                               | Alerta media con revisión |

Cruce obligatorio con dispositivo, dirección de red y concentración de compras en sorteos de un mismo organizador.

## 17.5 Vigencia documental

**RN-124.** Los documentos se conservan con monitoreo de vigencia. Aviso 30 días antes del vencimiento. **RN-125.** Con documento vencido, el usuario **puede reclamar premios y disponer de su saldo, y no puede comprar** hasta reverificar. Bloquear todo sería desproporcionado y contrario a RN-02.

## 17.6 Niveles de verificación

| Nivel  | Verificación                                  | Acumulado 30 días                 |
| ------ | --------------------------------------------- | --------------------------------- |
| **L0** | Correo y teléfono verificados y únicos        | Hasta el primer umbral de mercado |
| **L1** | Documento validado                            | Hasta el segundo umbral           |
| **L2** | Documento con prueba de vida y unicidad plena | **Sin techo**, sujeto a §19       |

**RN-126.** Los acumuladores de gasto se calculan por día, mes calendario, año y total, en la zona horaria del mercado, e incluyen el uso de saldo de reembolso. **RN-127.** El sistema notifica al usuario y a LIBOX al aproximarse y al superar cada umbral.

# 18\. Protección del usuario

## 18.1 Alcance en el MVP

Conjunto mínimo viable, con la arquitectura preparada para su ampliación. Todo control diferido está declarado en el modelo y deshabilitado por configuración, nunca ausente (LBPF V3 §10.4).

| Control                                         | Estado                   |
| ----------------------------------------------- | ------------------------ |
| Verificación de edad antes de la primera compra | Activo                   |
| Panel de gasto visible                          | Activo                   |
| Límites de gasto autoimpuestos con asimetría    | Activo                   |
| Autoexclusión                                   | Activo                   |
| Aviso de independencia probabilística           | Activo                   |
| Enfriamiento de 24 horas                        | Declarado, deshabilitado |
| Aviso de sesión prolongada                      | Declarado, deshabilitado |
| Detección de patrón de gasto                    | Declarado, deshabilitado |
| Autoexclusión federada entre operadores         | Fuera de alcance         |

## 18.2 Autoexclusión

**RN-128.** El usuario puede autoexcluirse por 7, 30 o 90 días, o de forma permanente. **Es irreversible durante el plazo elegido.** **RN-129.** Activación inmediata, sin fricción, sin retención comercial ni oferta de disuasión. **RN-130.** Bloquea la compra y toda comunicación comercial. **No bloquea** el acceso al historial, el reclamo de premios pendientes ni la disposición del saldo. **RN-131.** Los tickets ya adquiridos **permanecen válidos**; si el usuario resulta ganador, conserva íntegro su derecho a reclamar. La autoexclusión impide comprar, no despoja de lo comprado.

## 18.3 Límites autoimpuestos

**RN-132.** El usuario configura límites diario, semanal y mensual. **RN-133 — Asimetría obligatoria.** Reducir un límite aplica de inmediato; aumentarlo requiere 24 horas de espera. Sin la asimetría, el límite se eleva en el momento del impulso y la herramienta no protege. **RN-134.** El uso de saldo de reembolso computa contra el límite.

## 18.4 Panel de gasto y comunicación

**RN-135.** El gasto del periodo y el acumulado son visibles en el perfil y en el proceso de compra. **RN-136.** El aviso es **neutro y no culpabilizante**. Se informa la cifra, no se juzga la conducta. **RN-137.** El aviso **no se muestra durante el checkout**: situarlo ahí lo convertiría en fricción en zona de decisión, contrariando su propósito. **RN-138.** El aviso de independencia probabilística —los resultados anteriores no modifican la probabilidad de este sorteo— es persistente y no descartable en la superficie de tickets del usuario.

# 19\. Prevención financiera

## 19.1 Postura

**RN-139.** LIBOX **se diseña como si fuera sujeto obligado**, por decisión de control interno, con independencia de que la evaluación legal del mercado concluya que no lo es. El PRD deja constancia de ambas cosas: explica por qué existen controles que ninguna autoridad exige hoy, y permite endurecerlos sin rediseño si la calificación cambia.

## 19.2 Verificación previa por tramo

**INV-27.** No existe techo de gasto. Existe **acreditación previa por tramo**: la exigencia se solicita **al alcanzar el tramo, antes de emitir tickets**, nunca con posterioridad.

| Acumulado 30 días    | Requisito                                   | Efecto                      |
| -------------------- | ------------------------------------------- | --------------------------- |
| Tramo 1              | Verificación L1                             | Compra libre                |
| Tramo 2              | Verificación L2                             | Compra libre                |
| Tramo 3              | Declaración de origen de fondos             | Alerta media                |
| Tramo 4              | Sustento documental del origen              | Alerta alta y revisión      |
| **Sobre S/ 100.000** | **Aprobación previa de** `ADMIN_COMPLIANCE` | Debida diligencia reforzada |

Los importes provienen de `market_config`.

**RN-140 — Denominación.** El umbral superior se denomina **umbral de acreditación reforzada**, no límite. Cualquier persona puede superarlo acreditando el origen de sus fondos. Denominarlo límite induciría a error a un usuario legítimo con capacidad de gasto.

**Fundamento de la anterioridad.** Con diligencia posterior, el hallazgo llega cuando los fondos ya ingresaron, los tickets se emitieron y el sorteo pudo ejecutarse, y en ese punto no existen buenas salidas: anular tickets tras un sorteo rompe el pool y la prueba.

## 19.3 Vectores vigilados

| Vector                                | Control                                                                                                                                                                                                                                                       |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Concentración**                     | Límite del 30 % por usuario y sorteo (§20.2)                                                                                                                                                                                                                  |
| **Colusión organizador–participante** | Correlación de dispositivo, dirección de red, medio de pago y datos entre organizador y compradores; alerta ante concentración de compras de un mismo usuario en sorteos de un mismo organizador; gate de entrega que obliga a que el bien se mueva realmente |
| **Fragmentación**                     | Unicidad documental, más correlación por dispositivo y medio de pago                                                                                                                                                                                          |
| **Salida por el organizador**         | KYB reforzado con beneficiario final, actividad económica concordante y cuenta a nombre del titular verificado; **acumuladores y alertas sobre el organizador receptor**                                                                                      |

**RN-141.** El organizador receptor es el punto de salida del dinero y está sujeto a acumuladores y alertas propios, no solo el comprador.

## 19.4 Reserva y trazabilidad

**RN-142 — Prohibición de advertencia.** Al usuario **no se le comunica** que es objeto de análisis por sospecha ni que se ha generado un reporte. La comunicación es funcional y neutra. Constituye la única excepción a la transparencia del framework (LBPF V3 §0.3) y debe reflejarse en el manual de redacción, no solo en el procedimiento.

**RN-143 — Alcance estricto de la reserva.** Cubre el análisis y el reporte. **No cubre** el requerimiento de documentación, que se comunica con claridad, ni los derechos del usuario sobre sus fondos, que permanecen intactos.

**RN-144 — Trazabilidad de la no-decisión.** Concluir que no existe problema se documenta con motivo, igual que la decisión de actuar. Una auditoría no pregunta qué se reportó: pregunta qué se revisó y por qué se decidió no reportar.

**RN-145.** Registro de operaciones apto para reporte, expediente de debida diligencia inmutable con retención prolongada, y reporte periódico de mayores volúmenes a `ADMIN_COMPLIANCE`.

# 20\. Riesgo y antifraude

## 20.1 Motor de reglas

**RN-146.** Motor de reglas configurable que evalúa por umbral, velocidad y correlación, y emite al Panel Único (§23). Las reglas son datos, no código.

| Familia                | Señales                                                                                            |
| ---------------------- | -------------------------------------------------------------------------------------------------- |
| Velocidad              | Intentos de autenticación, registros, compras por unidad de tiempo, por usuario, dispositivo y red |
| Correlación            | Coincidencia de dispositivo, red, medio de pago y datos entre organizador y compradores            |
| Concentración          | Porcentaje de tickets por usuario y sorteo                                                         |
| Financiera             | Umbrales de acumulado, cambio de titular del medio de pago, contracargos                           |
| Documental             | Rechazos de verificación, reutilización de imágenes, ausencia de código del día                    |
| Comportamiento en sala | Datos de contacto externos, ofertas monetarias entre partes                                        |

## 20.2 Concentración

**INV-13.** Ningún participante posee más del umbral de concentración del mercado en un mismo sorteo. Valor por defecto: **30 %**.

**RN-147.** Se declara en los Términos y Condiciones y se hace cumplir en el sistema, bloqueando la compra que superaría el umbral. **RN-148.** Alertas escalonadas: informativa al 15 %, media al 25 %, alta con bloqueo al 30 %. **RN-149.** La concentración **no se divulga públicamente** (R-10). Su vigilancia es íntegramente interna, mediante el Panel Único.

## 20.3 Prohibición de autocompra

**RN-150.** Un organizador no puede adquirir tickets de sus propios sorteos, ni directamente ni mediante cuentas vinculadas por documento, medio de pago, dispositivo o relación societaria detectada.

## 20.4 Congelamiento y caso

**RN-151.** `ADMIN_RISK` puede congelar una cuenta con motivo. El congelamiento impide comprar y publicar; **no impide reclamar premios, recibir reembolsos ni disponer del saldo** (RN-02). **RN-152.** Todo congelamiento abre caso con plazo de resolución y notificación al titular en términos neutros.

# 21\. Reputación

## 21.1 Reputación del organizador

| Nivel  | Requisitos acumulados                                  | Efecto **exclusivo** sobre conformidad de entrega                                                       |
| ------ | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| **N0** | 0 a 2 sorteos                                          | Revisión manual completa                                                                                |
| **N1** | ≥ 5 exitosos, 0 controversias perdidas, ≥ 90 días      | Conformidad abreviada si la evidencia cumple la lista automática                                        |
| **N2** | ≥ 20 exitosos, tasa de controversia \< 2 %, ≥ 180 días | Conformidad automática con evidencia FUERTE y confirmación del ganador. Auditoría por muestreo del 10 % |
| **N3** | ≥ 50 exitosos, tasa \< 1 %, ≥ 365 días                 | Automática con liquidación acelerada. Auditoría por muestreo del 5 %                                    |

    score = 30 · tasa_entrega_exitosa
          + 20 · ( 1 − tasa_controversia )
          + 15 · puntualidad_dentro_de_plazo
          + 15 · calidad_de_evidencia
          + 10 · antigüedad_normalizada
          + 10 · satisfacción_del_ganador
          −      penalizaciones

Penalizaciones: controversia perdida −15 · entrega fallida −25 · valor inflado detectado −40.

## 21.2 Reglas de seguridad

| \#     | Regla                                                                                                                        |
| ------ | ---------------------------------------------------------------------------------------------------------------------------- |
| INV-28 | **La reputación nunca exime de la verificación de valor del premio.** Acelera únicamente la conformidad de entrega           |
| RN-153 | Descenso inmediato ante controversia perdida; ascenso solo con el periodo mínimo cumplido. El nivel no se compra con volumen |
| RN-154 | Premio en banda V3 o V4 exige revisión manual completa, sin importar el nivel                                                |
| RN-155 | Cambio de categoría de premio respecto del historial devuelve al organizador a N0 **para ese sorteo**                        |
| RN-156 | En categorías registrables la reputación es **prerrequisito de acceso** (N2 mínimo), no atajo                                |

**Fundamento de INV-28.** Un organizador con historial extenso que decide defraudar lo hará con el premio de mayor valor, que es exactamente el sorteo que debe pasar por el gate completo.

## 21.3 Reputación del usuario

**RN-157.** Los reclamos de mala fe determinados por adjudicación penalizan al usuario; la reincidencia retira la condición de verificado.

**Fundamento.** Sin reputación del usuario, el organizador tiene historial y consecuencias y el reclamante no tiene nada que perder. Esa asimetría es lo que hace rentable la extorsión, y corregirla la desactiva.

**RN-158.** La reputación del usuario **no es pública** ni afecta su probabilidad, su precio ni su acceso al catálogo. Solo determina el tratamiento probatorio de sus reclamos y, en caso extremo, la pérdida de la condición de verificado.

# 22\. Analítica conductual e indicadores

## 22.1 Los seis indicadores activos

**RN-159.** El MVP mide seis indicadores. Los seis restantes del LBPF permanecen como norma auditable, no como métrica de seguimiento continuo (LBPF V3 §7.1).

| Indicador                             | Umbral                                  | Capa                  | Método                                                                                                                                                                                                                                                                 |
| ------------------------------------- | --------------------------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **P1** Confianza antes que conversión | Acceso a evidencia \< 95 %              | Telemetría            | Sesiones de detalle en que identidad, costo y probabilidad fueron visibles en el área visible antes del primer renderizado del llamado a la acción, sobre sesiones de detalle. Se mide por observación de visibilidad real, no por presencia en el árbol del documento |
| **P3** Probabilidad objetiva          | Comprensión \< 85 %                     | Encuesta              | Respuestas correctas sobre el total de tickets del sorteo, con tolerancia del 10 %                                                                                                                                                                                     |
| **P5** Evidencia a la mano            | Accesibilidad \< 95 %                   | Telemetría            | Aperturas del cajón de evidencia sin navegación de página, sobre aperturas totales                                                                                                                                                                                     |
| **P6** Fricción protectora            | Error \> 0,5 % o arrepentimiento \> 3 % | Telemetría y encuesta | Error: órdenes con reembolso solicitado en menos de 60 minutos por compra equivocada. Arrepentimiento: encuesta a las 24 horas                                                                                                                                         |
| **P7** Defaults conservadores         | Umbral cero                             | Verificación estática | Recuento de opciones monetarias o de comunicación premarcadas. **Bloquea la integración**                                                                                                                                                                              |
| **P8** Calma en momentos críticos     | Umbral cero                             | Verificación estática | Recuento de animaciones en zona de decisión con duración superior a 240 ms o repetición infinita. **Bloquea la integración**                                                                                                                                           |

## 22.2 Las tres capas

| Capa                                              | Indicadores              | Naturaleza                                                                                                                  |
| ------------------------------------------------- | ------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| **Verificación estática en integración continua** | P7, P8                   | Se calculan sobre el código. Son normas de umbral cero ya decididas, no hipótesis. **Bloquean el merge**, no el lanzamiento |
| **Telemetría**                                    | P1, P5, P6 (error)       | Requieren el esquema de eventos de decisión                                                                                 |
| **Encuesta muestral**                             | P3, P6 (arrepentimiento) | Miden creencias y percepciones. Ningún evento de interacción mide una creencia                                              |

**RN-160.** Bloquear la integración no retrasa un lanzamiento: detiene el código antes de que exista en ningún entorno. Lanzar un patrón oscuro para medir su impacto significa que personas reales lo reciben mientras se mide.

## 22.3 Instrumento de encuesta

**RN-161.** De cinco a siete preguntas breves, de las que se muestran una o dos por sesión, **nunca durante el proceso de compra**.

| \# | Pregunta                                                       | Alimenta                                              |
| -- | -------------------------------------------------------------- | ----------------------------------------------------- |
| 1  | Total de tickets del sorteo en que participó                   | P3                                                    |
| 2  | Probabilidad aproximada de ganar                               | P3                                                    |
| 3  | Facilidad para encontrar costo y probabilidad antes de comprar | P1, P5                                                |
| 4  | Correspondencia entre expectativa y experiencia                | P6                                                    |
| 5  | **Percepción de presión para comprar rápido**                  | Detección de urgencia desde la percepción del usuario |
| 6  | Intención de volver a participar                               | Señal general                                         |
| 7  | Efecto de elegir el número sobre la probabilidad               | P10, **solo si se habilitase selección manual**       |

La quinta pregunta mide urgencia desde la percepción real, complementando la verificación estática que la mide desde el código.

**RN-162 — Muestreo adaptativo.** La tasa se ajusta al volumen con objetivo aproximado de 150 respuestas mensuales por instrumento: al inicio se consulta la totalidad de las compras y decrece conforme el volumen crece. Parámetro en `market_config`. Una tasa fija baja produce muestras inservibles en etapas tempranas.

## 22.4 Criterio de ruptura

**RN-163.** Un indicador se declara en ruptura solo cuando concurren:

1.  **n ≥ 100** respuestas o eventos válidos en la ventana. Por debajo se reporta como sin datos suficientes, nunca como incumplido
2.  **Intervalo de confianza de Wilson al 95 %** con límite superior por debajo del umbral. No se usa la proporción cruda
3.  **Dos ventanas consecutivas** de 30 días

**Fundamento.** Una alerta emitida sobre ruido enseña al equipo que las alertas no importan, y desde ese momento el sistema de gobernanza está muerto aunque siga funcionando.

## 22.5 Consecuencia

**RN-164.** La ruptura confirmada **no bloquea automáticamente**. Genera alerta clasificada dirigida a `ADMIN_BEHAVIORAL`, quien decide con criterio y registra la decisión. La decisión de no actuar es válida y se documenta con motivo.

## 22.6 Evento de decisión

**RN-165.** Todo evento de decisión incorpora: nombre, `trace_id`, sesión, actor cuando exista, **zona conductual**, clase de decisión, patrones aplicados, superficie, entidad, propiedades específicas, sello temporal de servidor y versión de aplicación.

**RN-166.** La analítica propia es la fuente de verdad. Un espejo anonimizado hacia herramienta externa es opcional y **nunca contiene identificadores directos ni importes asociados a persona identificable**.

# 23\. Panel Único de Alarmas

## 23.1 Unicidad

**RN-167.** Existe **un solo panel**. Concentra alertas conductuales, de riesgo y fraude, de vencimiento de plazos, de concentración, de prevención financiera y de excepciones de conciliación.

**Fundamento.** Cuatro fuentes de alerta con cuatro pantallas producen cuatro paneles que nadie consulta.

## 23.2 Esquema común

Tipo · severidad (alta, media, informativa) · entidad afectada · `trace_id` · **dueño nominal** · plazo de atención · estado · resolución con motivo.

**RN-168.** Acceso restringido a ADMIN y SUPPORT, con visibilidad acotada por subrol.

## 23.3 Reglas de operación

| \#     | Regla                                                                                             |
| ------ | ------------------------------------------------------------------------------------------------- |
| RN-169 | Toda alerta tiene **una persona responsable**, nunca un colectivo                                 |
| RN-170 | Plazo de 24 horas para severidad alta y 48 para media                                             |
| RN-171 | Escalamiento automático al vencer sin atención                                                    |
| RN-172 | **La conclusión de que no hay problema se documenta con motivo**, igual que la decisión de actuar |

**RN-173.** El Panel Único es **condición de validez de R-10**. Al no divulgarse públicamente la concentración ni la identidad, la detección de anomalías recae íntegramente en él. Si el panel no opera con dueños y plazos reales, la confidencialidad de participación pierde su justificación y debe revisarse.

# 24\. Configuración por mercado

## 24.1 Principio

**INV-29 (R-09).** Ninguna regla de jurisdicción vive en el código. Adaptarse a un cambio regulatorio es una operación de configuración con aprobación de `ADMIN_LEGAL_COMPLIANCE`, **no un despliegue de software**. Si adaptarse exige tocar código, el diseño falló.

## 24.2 Alcance

| Dominio                  | Contenido                                                                                                                                                                              |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Identidad y verificación | Documento válido, **proveedor concreto por adaptador**, requisitos por nivel                                                                                                           |
| Umbrales financieros     | Tramos, umbral de acreditación reforzada, anterioridad de la diligencia                                                                                                                |
| Tributario               | Denominación y tasa del impuesto, base imponible, emisor del comprobante, retenciones                                                                                                  |
| Gate legal               | Documento habilitante, autoridad, `gate_scope`                                                                                                                                         |
| Plazos                   | Reclamo por tramo, entrega por categoría, retención de liquidación, ventana de contracargo                                                                                             |
| Categorías de premio     | Habilitadas por mercado                                                                                                                                                                |
| **Escala de comisión**   | `fee_schedule`: tasa base, umbrales de E1 a E4 y sus tasas, y si la escala está activa en el mercado                                                                                   |
| Tipos de sorteo          | Habilitados por mercado, **con sus parámetros**: cierre anticipado de T2, número de hitos de T4, duración mínima y máxima de T5, ganadores máximos de T6, ediciones y separación de T7 |
| Moneda                   | Código, unidad mínima, formato, **múltiplo de redondeo del pricing**                                                                                                                   |
| Contenido                | Política de premios permitidos, calendario de feriados, zona horaria                                                                                                                   |
| Protección del usuario   | Controles exigibles en la jurisdicción                                                                                                                                                 |
| Conductual               | Tasa de muestreo, umbrales de indicadores                                                                                                                                              |
| Concentración            | Umbral por usuario y sorteo                                                                                                                                                            |
| Compra                   | Importe mínimo, rango de precio de ticket, vigencia de reserva                                                                                                                         |

**RN-174 —** `gate_scope`**.** Valor configurable con dominio `per_raffle`, `per_operator` o `none`. Si una jurisdicción exige autorización por operador en lugar de por sorteo, el gate se desplaza de la creación del sorteo al alta del organizador. Modelarlo como valor evita que sea un rediseño.

**RN-175 — Redondeo.** El múltiplo del pricing depende de la moneda y proviene de la configuración. No es constante de código.

## 24.3 Versionado

**INV-15.** Toda configuración se versiona con fechas de vigencia. **Un sorteo se rige por la versión vigente el día de su publicación, no por la actual.**

**Fundamento.** Sin versionado con vigencia es imposible demostrar ante una autoridad que se cumplió la norma vigente en el momento de los hechos.

**RN-176.** Toda versión se conserva indefinidamente. El cambio exige aprobación de `ADMIN_LEGAL_COMPLIANCE` con motivo.

## 24.4 Integraciones por adaptador

**RN-177.** Verificación de identidad, proveedor de pagos y emisión de comprobantes se implementan mediante **interfaz común con adaptador por proveedor**. La configuración indica cuál se instancia. La integración concreta es código; la elección es dato.

**RN-177-bis — El proveedor concreto se nombra en la configuración del mercado, no en este documento.** Nombrar proveedores en el documento normativo lo ataría a una jurisdicción, pero omitirlos por completo deja al equipo sin saber contra qué integrar. La configuración de cada mercado declara el proveedor real de cada adaptador: verificación de identidad contra fuente oficial de identificación, validación de comprobantes ante la autoridad tributaria, consulta registral ante el registro competente, y proveedor de pagos.

## 24.5 Multi-moneda

**INV-30.** Multi-moneda **por mercado, sin conversión**. Un sorteo tiene una moneda; todo su ciclo ocurre en esa moneda; el ledger separa cuentas por moneda. **No hay tipo de cambio, ni riesgo cambiario, ni operación transfronteriza en el MVP.**

**INV-31.** **El mercado pertenece al sorteo, no a la persona.** No existe compra transfronteriza.

**RN-178.** La escalabilidad regional es abrir mercados, no convertir divisas. La conversión, si alguna vez se requiere, es alcance posterior con su propio modelo contable.

**RN-179.** Lo que bloquea la expansión regional no es la moneda sino el marco legal de sorteos de cada jurisdicción. La existencia de la configuración no implica habilitación.

## 24.6 Frontend independiente del mercado

**INV-32.** Existe **una sola aplicación cliente**: mismo código, mismos componentes, mismas pantallas.

**RN-180.** La aplicación cliente **no fija** símbolo ni formato de moneda, denominación del documento de identidad, etiquetas tributarias, plazos, categorías disponibles ni textos legales. Todo proviene del servidor. **La aplicación no decide por jurisdicción: presenta.**

**RN-181 — Tolerancia de composición.** El diseño debe soportar variación sustancial en la longitud de los textos. Una etiqueta de tres caracteres en un mercado puede tener veinte en otro. Es requisito de diseño desde el MVP: un componente compuesto sobre la longitud de una jurisdicción se rompe al abrir la siguiente, y corregirlo después supone revisar la totalidad de las pantallas.

# 25\. Suspensión de mercado

**RN-182.** Existe capacidad de suspender la operación de un mercado por niveles, con efecto inmediato.

| Nivel              | Detiene                           | Continúa                                                         |
| ------------------ | --------------------------------- | ---------------------------------------------------------------- |
| **L1 Ventas**      | Compra de tickets                 | Sorteos vigentes se ejecutan; entregas y liquidaciones continúan |
| **L2 Publicación** | Nuevos sorteos                    | Los publicados completan su ciclo                                |
| **L3 Registro**    | Altas de usuarios y organizadores | Todo lo existente opera                                          |
| **L4 Total**       | Toda operación                    | Resolución de casos abiertos y reembolsos                        |

**INV-33.** **Ningún nivel puede impedir reclamar un premio, recibir un reembolso o disponer del saldo propio.** Suspender la operación jamás puede convertirse en retener dinero de terceros.

**RN-183.** Activa `ADMIN_SUPER` con motivo obligatorio. Reversión con segunda firma. **RN-184.** Notificación automática a todos los usuarios del mercado explicando qué continúa operando.

# 26\. Growth y comercial

## 26.1 Separación de ámbitos

**RN-185.** La estrategia de marketing, adquisición y ventas es externa al diseño del producto. El producto **provee los datos e instrumentos** y **establece los límites**, porque toda comunicación comercial es superficie conductual sujeta a R-01.

## 26.2 Capacidades

| Capacidad                  | Contenido                                                                                            |
| -------------------------- | ---------------------------------------------------------------------------------------------------- |
| Atribución                 | Captura de origen de campaña en registro y compra; embudo por etapa                                  |
| Referidos                  | Recompensa por **registro verificado**, nunca por gasto del referido                                 |
| Promociones                | Concesión de crédito de reembolso, configurable por importe, vigencia y segmento                     |
| Lista de espera            | Aviso por organizador y por categoría                                                                |
| Campañas                   | Segmentación y envío con respeto automático de exclusión, baja y horarios de descanso                |
| Descubrimiento orgánico    | Superficies públicas indexables por categoría, organizador y sorteo                                  |
| Captación de organizadores | Página comercial, **simulador público de recaudación**, incorporación asistida, captura de contactos |
| Reputación como sello      | Nivel del organizador visible como distintivo verificable                                            |
| Panel comercial            | Consulta de datos por las áreas de marketing y ventas sin intervención de ingeniería                 |

## 26.3 Límites

| \#     | Límite                                                                                                                                                                       |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RN-186 | **Precio único.** El precio del ticket es idéntico para todos los participantes. Las promociones se instrumentan como crédito aplicable, nunca como precio diferenciado      |
| RN-187 | **Promoción identificada.** Toda posición destacada por contraprestación se identifica visiblemente como tal y se presenta separada del ordenamiento orgánico                |
| RN-188 | **Ordenamiento explicable.** Todo ordenamiento expone su criterio en una interacción: cierre próximo, volumen de sorteos completados por el organizador, velocidad de venta  |
| RN-189 | **Equidad de descubrimiento.** Todo destaque basado en historial reserva cuota para organizadores nuevos verificados. Un ordenamiento que se retroalimenta cierra el mercado |
| RN-190 | **Referido por registro.** Retribuir el gasto de un tercero configura un incentivo de captación en cadena, incompatible con R-08                                             |
| RN-191 | **Simetría de reglas.** La comunicación comercial está sujeta a las mismas reglas de probabilidad, costo, urgencia y evidencia que la interfaz transaccional                 |
| RN-192 | **Consentimiento impuesto por el sistema.** La exclusión voluntaria, la baja y los horarios de descanso los hace cumplir el sistema. No es política: es restricción          |

## 26.4 Códigos, marca compartida y suscripción de beneficios

**RN-194-bis — Código de campaña.** Un solo código público con cupo por oportunidad gratuita. Los primeros N que lo usan entran; al agotarse se cierra solo. Reglas en §5.5.

**RN-194-ter — Código de organizador.** Permanente, sin cupo, **no otorga participación**. Marca el origen del usuario y permite responder qué parte de las ventas de un organizador vino de su comunidad y qué parte del catálogo de LIBOX. Es la instrumentación directa de H-07.

**RN-194-quater — La atribución se mide, nunca se paga por gasto del referido.** La recompensa se paga por **registro verificado** (RN-190). Retribuir el gasto de terceros configura captación en cadena e incumple R-08.

**RN-194-quinquies — El desglose de aporte de LIBOX a cada organizador es información de esa relación**, visible en su panel privado. Lo público es el historial de oportunidades completadas y entregadas.

**RN-194-sexies — Marca compartida.** La oportunidad es del organizador y se presenta como suya; **LIBOX es visible como garante** —sello de verificación, prueba, retención—. La mención de LIBOX en la promoción externa del organizador forma parte del acuerdo, no de la buena voluntad.

**RN-194-septies — LIBOX Club.** Suscripción de beneficios con aliados externos. Se construye en el MVP y **se enciende por configuración**, no al lanzar.

| \#              | Regla                                                                                                                                   |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **INV-46**      | **Ninguna suscripción otorga participaciones, entradas, ventajas de probabilidad ni acceso preferente a oportunidades** (LBPF V3 §13.2) |
| RN-194-octies   | Los beneficios son **con aliados externos**, jamás descuento sobre el precio del ticket                                                 |
| RN-194-nonies   | Cancelar es tan simple como suscribirse: dos pasos o menos                                                                              |
| RN-194-decies   | Ingreso **diferido**: se devenga día a día, con prorrateo en la baja                                                                    |
| RN-194-undecies | **Criterio doble de encendido**: aliados con beneficio activo **y** volumen de usuarios verificados. Ninguno se salta                   |

**Fundamento del criterio doble.** Un plan de beneficios sin aliados es una promesa vacía: el valor no lo pone LIBOX, lo ponen los comercios. Encenderlo antes destruiría la percepción del plan justo cuando más importa.

**RN-193 — Escasez auténtica.** La escasez en LIBOX es estructuralmente verificable: pool finito con venta pública. Su comunicación es legítima y deseable. Lo prohibido es fabricarla. LIBOX no necesita urgencia falsa porque dispone de urgencia real, que además resiste el escrutinio.

# 27\. Superficies

## 27.1 Principio de especificación

V1 describía 54 pantallas con seis campos variables y siete idénticos repetidos en todas. V2 especificó cada superficie por lo que la distingue: propósito, zona conductual, datos rectores, acciones y reglas propias. Los aspectos comunes se declaran una sola vez aquí y no se repiten.

**Comunes a toda superficie:** estados de carga, vacío, error, restringido y éxito · propagación de `trace_id` · etiquetas provenientes del servidor · composición tolerante a longitud variable · objetivos táctiles suficientes · operación sin dependencia de puntero.

## 27.2 Públicas

| ID        | Superficie                          | Zona         | Datos rectores                                                                                  | Reglas propias                                                                                                                                                                                  |
| --------- | ----------------------------------- | ------------ | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PU-01     | Inicio                              | Atracción    | Sorteos activos con premio, precio, vendidos y pool                                             | Ordenamiento con criterio visible (RN-188). Prueba social solo de resultados reales                                                                                                             |
| PU-02     | Catálogo y búsqueda                 | Atracción    | Filtros por categoría, rango de precio, cierre                                                  | Sin urgencia fabricada                                                                                                                                                                          |
| PU-03     | **Detalle de oportunidad**          | **Decisión** | Las seis zonas de la Verified Opportunity Card                                                  | **Costo, probabilidad y pool visibles antes del llamado a la acción.** Plazos, ruta de resolución y costo de recepción visibles (BR-08). Sin animación superior a 240 ms ni repetición infinita |
| PU-04     | Bases del sorteo                    | Decisión     | Bases inmutables con hash                                                                       | Accesible en una interacción desde PU-03                                                                                                                                                        |
| PU-05     | **Verificación pública de sorteo**  | Decisión     | Pool, hash, compromiso, baliza, semilla revelada, resultado, procedimiento                      | Sin autenticación, indexable. **No divulga identidad ni concentración**                                                                                                                         |
| PU-06     | Ganadores                           | Atracción    | Resultados reales con ventana temporal                                                          | Identidad minimizada y solo con consentimiento                                                                                                                                                  |
| PU-07     | Cómo funciona                       | Atracción    | Explicación del motor y de la garantía patrimonial                                              | Lenguaje llano                                                                                                                                                                                  |
| PU-08     | **Simulador de recaudación**        | Atracción    | Fórmula real de §1.3                                                                            | Público, sin registro. Muestra bruto, comisión, neto y tickets                                                                                                                                  |
| PU-09     | Página comercial para organizadores | Atracción    | Propuesta de valor y captura de contacto                                                        | —                                                                                                                                                                                               |
| PU-10     | Legales                             | Decisión     | Términos, privacidad, canal de reclamaciones                                                    | Versionados                                                                                                                                                                                     |
| **PU-11** | **Directorio de organizadores**     | Atracción    | Organizadores con oportunidades activas e históricas                                            | Ordenamiento con criterio visible. **Sin datos de participantes ni recaudación**                                                                                                                |
| **PU-12** | **Perfil público de organizador**   | Atracción    | Historial de oportunidades completadas y entregadas, nivel de reputación, oportunidades activas | **Es la garantía que ofrece quien pide dinero al público** (LBPF V3 R-10). No muestra recaudación ni identidad de participantes                                                                 |

**Fundamento de PU-11 y PU-12.** Sin ellas el participante ve oportunidades sueltas y nunca a quién está detrás. **Son el mecanismo que permite comprar a un organizador desconocido**, y por tanto lo que convierte el catálogo en marketplace en lugar de una suma de herramientas.

## 27.3 Acceso

| ID    | Superficie                           | Reglas propias                                                                                      |
| ----- | ------------------------------------ | --------------------------------------------------------------------------------------------------- |
| AC-01 | Registro                             | Correo y teléfono únicos. Fecha de nacimiento obligatoria. Rechazo si es menor                      |
| AC-02 | Verificación de contacto             | Código con vigencia y límite de intentos                                                            |
| AC-03 | Ingreso                              | Límite de intentos por dirección y dispositivo                                                      |
| AC-04 | Recuperación                         | Sin revelar existencia de la cuenta                                                                 |
| AC-05 | **Verificación de identidad y edad** | Documento validado contra fuente oficial **más prueba de vida**. Prerrequisito de la primera compra |

## 27.4 Usuario

| ID    | Superficie                  | Zona         | Reglas propias                                                                                                                    |
| ----- | --------------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| US-01 | Compra                      | **Decisión** | Importe mínimo de mercado. Idempotencia por clave del cliente. Sin opciones premarcadas. **Recuperación de estado al reconectar** |
| US-02 | Retorno de pago             | Decisión     | Estado real, sin ambigüedad. Ante incertidumbre, indica procesamiento en curso                                                    |
| US-03 | Mis tickets                 | Decisión     | Números asignados y estado del pool. **Aviso de independencia probabilística persistente y no descartable**                       |
| US-04 | Detalle de participación    | Decisión     | Pool, hash y enlace a PU-05                                                                                                       |
| US-05 | Mi cuenta                   | Decisión     | Perfil, verificación, vigencia documental                                                                                         |
| US-06 | **Panel de gasto**          | Decisión     | Gasto del periodo y acumulado. **Neutro y no culpabilizante.** No se muestra durante la compra                                    |
| US-07 | **Límites y autoexclusión** | Decisión     | Asimetría: reducir inmediato, aumentar con 24 horas. Autoexclusión sin fricción ni retención comercial                            |
| US-08 | Saldo de reembolso          | Decisión     | Saldo, movimientos, solicitud de retiro con verificación                                                                          |
| US-09 | **Sala de Resolución**      | Decisión     | Solo agregación. Evidencia con hash. Datos de contraparte minimizados                                                             |
| US-10 | Reclamo de premio           | Decisión     | Aceptación informada incluidas cargas y costos. **Derecho a rechazar**                                                            |
| US-11 | Envío                       | Decisión     | Al menos dos opciones formales. Costo a cargo del ganador, ya declarado en PU-03                                                  |
| US-12 | Controversia                | Decisión     | **Motivo de lista cerrada y evidencia obligatoria**                                                                               |
| US-13 | Notificaciones              | Decisión     | Baja alcanzable en dos pasos                                                                                                      |

## 27.5 Organizador

| ID    | Superficie                       | Reglas propias                                                                              |
| ----- | -------------------------------- | ------------------------------------------------------------------------------------------- |
| CL-01 | Panel                            | Ventas, sorteos activos, liquidaciones, reputación                                          |
| CL-02 | Alta y KYB                       | Beneficiario final, actividad económica, representación                                     |
| CL-03 | Subusuarios                      | Asignación de subrol conforme a §2.3                                                        |
| CL-04 | **Datos de cobro**               | Solo `CLIENT_OWNER`. Reverificación y **congelamiento de 48 horas con notificación**        |
| CL-05 | Asistente de creación            | Tipo, premio, categoría, valor, precio y tickets, **ruta de resolución**, plazos propuestos |
| CL-06 | **Simulador de pricing**         | Fórmula real; muestra el plazo máximo estimado hasta el cobro (RN-105)                      |
| CL-07 | **Carga de evidencia de premio** | Lista cerrada por categoría. Código del día visible en imágenes y video                     |
| CL-08 | **Etapas P-C**                   | Siete etapas con documentos tipificados. Sin avance parcial                                 |
| CL-09 | Mis sorteos                      | Filtrado por estado de la FSM                                                               |
| CL-10 | Detalle de sorteo                | Ventas, pool, línea de tiempo pública                                                       |
| CL-11 | Sala de Resolución               | Entra al reclamar el ganador                                                                |
| CL-12 | **Liquidaciones**                | Estados Pendiente, **Retenido** y Pagado, con motivo y plazo estimado                       |
| CL-13 | Reportes                         | Ventas, conversión, entregas, controversias                                                 |
| CL-14 | Configuración                    | Notificaciones, preferencias                                                                |

## 27.6 Soporte

| ID    | Superficie               | Reglas propias                                          |
| ----- | ------------------------ | ------------------------------------------------------- |
| SU-01 | Cola de salas            | **Todo el equipo en solo lectura**, con estado y plazo  |
| SU-02 | Sala asignada            | Único punto de escritura y atestación                   |
| SU-03 | **Atestación**           | Lista de evidencia por categoría. No mueve dinero       |
| SU-04 | Búsqueda por `trace_id`  | Línea de tiempo completa, solo lectura                  |
| SU-05 | **Valoración de premio** | Bandas V1 y V2. No atesta el sorteo que valoró          |
| SU-06 | Gestión de plazos        | Extensión dentro de límite, con motivo y notificación   |
| SU-07 | Casos de usuario         | Sin acceso a dinero, ledger ni resultado                |
| SU-08 | Indicadores conductuales | Solo `SUPPORT_BEHAVIORAL_ANALYST`. Monitorea, no decide |

## 27.7 Administración

| ID    | Superficie                        | Reglas propias                                                             |
| ----- | --------------------------------- | -------------------------------------------------------------------------- |
| AD-01 | Moderación de sorteos             | Política de contenido; motivo estructurado                                 |
| AD-02 | **Gate legal**                    | Documento habilitante según `gate_scope`                                   |
| AD-03 | **Valoración V3 y V4**            | Segunda firma en V4                                                        |
| AD-04 | Etapas P-C                        | Aprobación por casilla; **no existe aprobar con observaciones**            |
| AD-05 | Capacidades y riesgo              | Habilitación de tipos y categorías por organizador                         |
| AD-06 | **Panel Único de Alarmas**        | Dueño nominal, plazo, escalamiento, resolución con motivo                  |
| AD-07 | **Prevención financiera**         | Expedientes, aprobación sobre umbral. **Comunicación neutra**              |
| AD-08 | **Liquidaciones**                 | Seis gates visibles. Lote, o caso a caso con segunda firma en registrables |
| AD-09 | Conciliación                      | Excepciones con plazo                                                      |
| AD-10 | **Adjudicación de controversias** | Jerarquía de evidencia. Quien adjudica no atestó                           |
| AD-11 | Auditoría                         | Consulta inmutable; exportación forense                                    |
| AD-12 | **Configuración de mercado**      | Versionado con vigencia; aprobación de `ADMIN_LEGAL_COMPLIANCE`            |
| AD-13 | **Suspensión de mercado**         | Cuatro niveles; motivo obligatorio; reversión con segunda firma            |
| AD-14 | Usuarios internos                 | Validación de las once incompatibilidades                                  |
| AD-15 | Comercial                         | Atribución, campañas, promociones, contactos                               |

# 28\. Notificaciones

**RN-194.** Canales: correo, mensajería o SMS, notificación instantánea y notificación en aplicación. **RN-195.** Los avisos críticos —resultado de sorteo, reclamo de premio, vencimiento de plazo, suspensión de mercado, requerimiento documental— **no dependen nunca de la notificación instantánea como canal único** (RN-110). **RN-196.** Toda plantilla es versionada y forma parte del manual de redacción, sujeta al framework conductual. **RN-197.** Horarios de descanso y límite de frecuencia por mercado. Los avisos críticos y los de seguridad quedan exceptuados del límite de frecuencia, no del registro. **RN-198.** La exclusión voluntaria suprime toda comunicación comercial y conserva las operativas y de seguridad. **RN-199.** Todo envío registra canal, destino enmascarado, plantilla, sello temporal y estado devuelto por el proveedor.

# 29\. Catálogo de errores

**RN-200.** Todo error expone código estable, mensaje al usuario en lenguaje llano y no culpabilizante, causa técnica en el registro, y `trace_id`. El catálogo completo con correspondencia a códigos de estado reside en `error-catalog.md` (L3 V7).

**RN-201.** Ningún mensaje de error revela existencia de cuentas, datos de terceros, ni información que facilite enumeración.

| Familia             | Cubre                                                             |
| ------------------- | ----------------------------------------------------------------- |
| `ERR_AUTH_*`        | Autenticación, sesión, multifactor                                |
| `ERR_IDENTITY_*`    | Unicidad, verificación, prueba de vida, edad, vigencia documental |
| `ERR_RBAC_*`        | Permisos, subroles, incompatibilidades, segunda firma             |
| `ERR_RAFFLE_*`      | Estado, transición, capacidad, tipo                               |
| `ERR_PRIZE_*`       | Categoría, evidencia, desviación de valor, código del día         |
| `ERR_REGISTRABLE_*` | Etapas, bloqueo registral, gravamen, inscripción                  |
| `ERR_ORDER_*`       | Idempotencia, importe mínimo, inventario, reserva expirada        |
| `ERR_PAYMENT_*`     | Proveedor, webhook, firma, conciliación, contracargo              |
| `ERR_DRAW_*`        | Congelamiento, compromiso, baliza, verificación, re-sorteo        |
| `ERR_RESOLUTION_*`  | Sala, evidencia, atestación, plazos                               |
| `ERR_DISPUTE_*`     | Motivo, evidencia, adjudicación                                   |
| `ERR_SETTLEMENT_*`  | Gates, cobro, retención                                           |
| `ERR_LIMIT_*`       | Concentración, límites propios, acumuladores                      |
| `ERR_COMPLIANCE_*`  | Tramos, acreditación, aprobación sobre umbral                     |
| `ERR_MARKET_*`      | Configuración, categoría no habilitada, suspensión                |
| `ERR_LEGAL_GATE`    | Documento habilitante ausente o inválido                          |

# 30\. Eventos de dominio

**RN-202.** Todo cambio de estado relevante publica evento en `event_outbox` con `trace_id`, actor, entidad, versión de esquema y sello temporal. El catálogo completo reside en `analytics-events.md` (L3 V7).

| Familia               | Eventos                                                                                               |
| --------------------- | ----------------------------------------------------------------------------------------------------- |
| Identidad             | Registro, verificación de contacto, verificación de identidad, prueba de vida, vencimiento documental |
| Organizador           | Alta, KYB, cambio de datos de cobro, cambio de capacidad, cambio de reputación                        |
| Sorteo                | Creación, envío, valoración, gate legal, aprobación, publicación, pausa, cierre                       |
| Premio                | Valoración solicitada, aprobada, observada, rechazada; etapa registrable avanzada                     |
| Orden y pago          | Creación, confirmación, expiración, reembolso, contracargo                                            |
| Ticket                | Emisión, anulación                                                                                    |
| Sorteo ejecutado      | Congelamiento, compromiso publicado, ejecución, prueba generada, re-sorteo                            |
| Resolución            | Apertura, reclamo, cotización de envío, evidencia, atestación, controversia, cierre                   |
| Liquidación           | Devengo, elegibilidad, aprobación, pago, retención, reversión                                         |
| Riesgo y cumplimiento | Evento de riesgo, alerta, congelamiento, expediente, aprobación sobre umbral                          |
| Protección            | Límite fijado o modificado, autoexclusión, aviso de gasto                                             |
| Mercado               | Cambio de configuración, suspensión, reanudación                                                      |

# 31\. Auditoría y trazabilidad

**RN-203.** Registro de auditoría inmutable de toda acción de rol interno y de todo cambio de estado con efecto patrimonial o sobre derechos del usuario. **RN-204.** Un fallo del registro de auditoría **nunca revierte una operación de cobro exitosa**: el evento entra en cola de emergencia con alarma y reintento. Un cobro confirmado por el proveedor y revertido por un fallo de registro produce un usuario sin tickets y con cargo. **RN-203-bis — Auditoría de consulta.** Toda **consulta de un rol interno a datos de terceros** —sala de resolución, expediente de cumplimiento, documento de identidad, evidencia— se registra en auditoría con actor, subrol, entidad consultada y motivo cuando aplique.

**Fundamento.** La versión anterior registraba toda mutación y ninguna lectura. **Quién miró qué es tan relevante como quién cambió qué** cuando el sistema custodia datos personales y evidencia probatoria, y es lo primero que pregunta una auditoría ante una filtración.

**La navegación de participantes y organizadores no va a auditoría**: va a analítica, con otra retención. Registrar cada pantalla inflaría la tabla sin aportar defensa y crearía un problema de datos personales.

**RN-205.** Toda consulta por `trace_id` reconstruye la línea de tiempo completa de la operación. **RN-206.** Exportación forense firmada, con manifiesto de hashes, para salas y expedientes. **RN-207.** Los registros de auditoría, ledger, eventos y expedientes tienen política de retención y particionamiento definidos en L3. Crecen sin techo por diseño.

# 32\. Calidad

## 32.1 Estrategia

| Tipo                            | Alcance                                                                              | Ejecución                      |
| ------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------ |
| Unitaria                        | Reglas de negocio y cálculo                                                          | Cada integración               |
| Integración                     | Flujos entre agregados                                                               | Cada integración               |
| **Propiedad sobre invariantes** | Cuadre de asientos; inexistencia de ticket válido sin pago; suficiencia de reembolso | Cada integración               |
| Concurrencia                    | Últimos tickets del pool; webhooks duplicados en paralelo; bloqueo de saldo          | Diaria                         |
| RBAC y separación de funciones  | Las once incompatibilidades; SUPPORT no toca dinero, ledger ni resultado             | **Obligatoria, bloqueante**    |
| Conductual estática             | P7 y P8 sobre el código                                                              | **Bloquea la integración**     |
| Reproducción de auditoría       | Reconstrucción por `trace_id`                                                        | Diaria                         |
| Verificación de sorteo          | Recomputación independiente con vectores de prueba                                   | **Obligatoria, bloqueante**    |
| Extremo a extremo               | Recorridos completos por rol                                                         | Diaria                         |
| Rendimiento                     | Presupuesto de §33.3                                                                 | Semanal                        |
| **Ensayo con dinero real**      | Ciclo completo con importe simbólico real                                            | **Gate de fase, innegociable** |

## 32.2 Ensayo con dinero real

**RN-208.** Antes de cerrar la fase de construcción se ejecuta un ciclo completo con dinero real y de bajo importe: alta de organizador, aprobación, verificación de premio, publicación, compra, congelamiento, sorteo, verificación pública, sala, evidencia, atestación, gates, liquidación y asientos. **Es gate binario.** Ningún resultado parcial lo satisface.

## 32.4 Objetivos de capacidad

Los objetivos de §33.3 cubren latencia y disponibilidad. Faltaba lo que ocurre bajo volumen: **la corrección bajo concurrencia está garantizada por diseño; el punto de degradación debe medirse, no estimarse.**

| Objetivo                                    | Valor de referencia MVP | Se mide con                           |
| ------------------------------------------- | ----------------------- | ------------------------------------- |
| Sorteos en estado activo simultáneos        | 500                     | Prueba de carga sostenida             |
| Órdenes por segundo en pico                 | 50                      | Escenario de cierre de sorteo popular |
| Tickets emitidos por minuto en pico         | 600                     | Escenario de venta relámpago          |
| Compradores concurrentes en un mismo sorteo | 200                     | Escenario de últimos tickets          |
| Notificaciones por minuto                   | 1.000                   | Cierre simultáneo de varios sorteos   |
| Salas de resolución abiertas                | 300                     | Acumulación de casos                  |

**Son valores de referencia, no compromisos.** Se validan en la prueba de carga de R5 y se ajustan con la medición. Lo que sí es compromiso: **ninguno de estos escenarios puede producir sobreventa, doble emisión de ticket, doble ejecución de sorteo ni descuadre contable**, y eso está cubierto por las pruebas de concurrencia obligatorias.

**RN-211-bis.** La prueba de carga declara el punto de degradación observado. Sin esa cifra, el dimensionamiento de infraestructura sería estimación y no medición.

## 32.3 Criterios de no liberación

No se libera si: un invariante de dinero falla · un caso de RBAC falla · la verificación independiente del sorteo no reproduce el resultado · existe animación infinita o superior a 240 ms en zona de decisión · existe opción monetaria premarcada · una superficie de decisión omite costo, probabilidad o pool · una oportunidad puede publicarse sin valor verificado · faltan plazos, ruta de resolución o costos exigidos por BR-08.

# 33\. Plataforma

## 33.1 Decisión

**INV-32.** **Aplicación web adaptable universal, más aplicación web progresiva instalable.** Funciona correctamente en cualquier navegador y sistema operativo, en computadora, tableta y teléfono. Las aplicaciones nativas son fase posterior sobre la misma interfaz de programación. **La web no se depreca nunca**: es el canal de descubrimiento, el que se indexa y el que garantiza acceso universal.

Queda derogada la denominación de aplicación móvil nativa presente en V1, así como las superficies que la presuponían.

## 33.2 Diseño para móvil primero

**RN-209.** Las superficies se diseñan **desde el móvil**, no como reducción del escritorio. Es trabajo de diseño completo, no adaptación de estilos, y debe estar explícitamente estimado.

**RN-210.** Objetivos táctiles suficientes, sin dependencia de estados de puntero, y teclado virtual que no oculta el campo activo.

## 33.3 Presupuesto de rendimiento

**RN-211.** Presupuesto medido en red móvil de calidad media y dispositivo de gama media: renderizado del contenido principal por debajo de 2,5 segundos; código inicial por debajo de 200 KB comprimidos; imágenes en formatos modernos con juegos de resolución. Sin presupuesto escrito y verificado, el rendimiento se degrada silenciosamente.

**RN-212.** Matriz de compatibilidad declarada y verificada en integración continua, incluyendo el motor obligatorio de los navegadores de sistemas móviles cerrados.

## 33.4 Preparación para aplicaciones nativas

| \#     | Decisión                                                                                                                                            |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| RN-213 | Autenticación por credencial portable con renovación. **Nunca exclusivamente por cookie de navegador**: una aplicación nativa no puede reutilizarla |
| RN-214 | Interfaz de programación completamente agnóstica del cliente. Sin marcado renderizado en respuestas, sin lógica de negocio en el cliente            |
| RN-215 | Tokens de diseño en formato portable, capaces de generar temas para plataformas nativas                                                             |
| RN-216 | Ninguna ruta de dinero depende de capacidades exclusivas de navegador                                                                               |
| RN-217 | Aplicación web progresiva desde el MVP: manifiesto, trabajador de servicio e instalabilidad                                                         |

## 33.5 Recuperación de estado

**RN-218.** La compra sobrevive a la pérdida de conexión: al reconectar, la aplicación recupera el estado real de la orden y comunica con claridad si el pago está en proceso, confirmado o fallido. La ambigüedad en este punto es una de las principales causas de contracargo.

# 34\. Modelo de datos

**RN-219.** El esquema completo —tablas, columnas, tipos, restricciones, índices, particionamiento y retención— reside en `libox_schema_L3_V7.sql` (L3 V7). Este documento declara qué entidades existen y de qué agregado son (§3.1), y qué invariantes cumplen (§3.2).

**RN-220.** Toda tabla incorpora identificador, marcas de creación y actualización, y `trace_id` cuando su mutación proviene de una operación trazable.

**RN-221.** Toda entidad monetaria almacena importe como entero de la unidad mínima junto con el código de moneda. Nunca punto flotante.

**RN-222.** Los registros de crecimiento sin techo —auditoría, asientos, eventos, salas— se particionan desde la primera migración. Particionar al inicio es gratuito; hacerlo con volumen acumulado, no.

**RN-223.** Ningún entorno distinto de producción contiene datos personales reales sin anonimización.

# 35\. Interfaz de programación

**RN-224.** Los contratos completos —request, response, códigos, ejemplos y errores— residen en `libox_openapi_L3_V7.yaml` (L3 V7). Este documento declara qué endpoints existen y qué reglas de negocio aplican.

**RN-225.** Toda operación mutante de dinero exige clave de idempotencia provista por el cliente. **RN-226.** Toda respuesta incorpora `trace_id`. **RN-227.** Versionado explícito. Ningún cambio incompatible sin nueva versión.

| Familia                  | Cubre                                                    |
| ------------------------ | -------------------------------------------------------- |
| Identidad                | Registro, verificación, sesión, prueba de vida, vigencia |
| Organizador              | Alta, KYB, subusuarios, datos de cobro, capacidades      |
| Catálogo                 | Listado, búsqueda, detalle, bases                        |
| **Verificación pública** | Consulta de prueba de sorteo, **sin autenticación**      |
| Sorteo                   | Creación, edición, envío, publicación, estado            |
| Premio                   | Valoración, documentos, etapas registrables              |
| Compra                   | Orden, retorno de pago, tickets                          |
| Pagos                    | Webhooks, conciliación, reembolsos                       |
| Resolución               | Sala, mensajes, evidencia, atestación, envío             |
| Controversias            | Apertura, evidencia, adjudicación                        |
| Liquidación              | Consulta, gates, ejecución                               |
| Saldo de reembolso       | Consulta, movimientos, retiro                            |
| Protección               | Límites, autoexclusión, panel de gasto                   |
| Cumplimiento             | Acumuladores, tramos, expedientes                        |
| Alarmas                  | Consulta, asignación, resolución                         |
| Mercado                  | Configuración, suspensión                                |
| Analítica                | Eventos, encuestas, indicadores                          |
| Growth                   | Atribución, referidos, promociones, contactos            |

# Anexo A — Artefactos de nivel L3

| Artefacto                  | Contenido                                                                                                                  | Bloquea                          |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| `libox_schema_L3_V7.sql`   | Esquema completo con restricciones, índices, particionamiento y retención                                                  | Arranque del proyecto            |
| `libox_openapi_L3_V7.yaml` | Contratos tipados de todos los endpoints                                                                                   | Toda la construcción del cliente |
| `raffle-fsm.md`            | Implementación de la máquina de estados y su tabla de transiciones                                                         | Dominio completo                 |
| `draw-engine-spec.md`      | Algoritmo, serialización canónica al byte, sorteo sin reemplazo, verificación contra fuente de baliza y vectores de prueba | Motor de sorteo                  |
| `chart-of-accounts.md`     | Plan de cuentas y las catorce transacciones canónicas balanceadas                                                          | Contabilidad y liquidación       |
| `error-catalog.md`         | Catálogo completo de errores                                                                                               | Cliente y soporte                |
| `analytics-events.md`      | Esquema de eventos de dominio y de decisión                                                                                | Analítica e indicadores          |
| `market-config-spec.md`    | Estructura, versionado y vigencia de la configuración por mercado                                                          | Multi-mercado                    |
| `copy-deck.md`             | Textos aprobados conforme al framework conductual                                                                          | Toda superficie                  |
| `rbac-matrix.md`           | Matriz completa de subroles, permisos e incompatibilidades                                                                 | Seguridad                        |

# Anexo B — Trazabilidad con LBPF V3

| Norma LBPF                                   | Sección de este PRD                |
| -------------------------------------------- | ---------------------------------- |
| R-04 Neutralidad probabilística              | §12, asignación automática en §1.6 |
| R-09 Adaptabilidad regulatoria               | §24                                |
| R-10 Confidencialidad de participación       | §12.4, §20.2, §27.2                |
| BR-08 Integridad del proceso                 | §6.4, §15.4, §16.1, §27.2          |
| §5.4 Custodia patrimonial                    | §1.5, §8.1, §16.5                  |
| §5.5 Verificación de valor e identidad única | §7, §17.1                          |
| §6.2 Verified Opportunity Card               | §27.2 PU-03                        |
| §6.2.2 Límite de concentración               | §20.2                              |
| §6.3 y §6.4 Veto anti-impulso y Motion Calm  | §32.3                              |
| §7 Indicadores                               | §22                                |
| §9.1 Régimen de linter                       | §22.2, §32.1                       |
| §10.7 Panel Único                            | §23                                |
| §11 Multi-mercado                            | §24, §25                           |
| §12 Ética comercial                          | §26                                |
| §13 Neutralidad económica                    | §1.2                               |
| §0.3 Reserva en prevención financiera        | §19.4                              |
| DP-16 Controversia simétrica                 | §14                                |

# Anexo C — Materias sujetas a dictamen legal

Ninguna de estas materias se implementa sin respuesta escrita de asesoría colegiada del mercado correspondiente. Se listan como dependencias externas del plan, no como advertencias genéricas.

| \#   | Materia                                                                        | Bloquea                          |
| ---- | ------------------------------------------------------------------------------ | -------------------------------- |
| L-01 | Figura jurídica de LIBOX y necesidad de autorización propia como operador      | Puesta en marcha                 |
| L-02 | Naturaleza jurídica de la transferencia de un bien registrable como premio     | P-C completo                     |
| L-03 | Obligado al tributo de transferencia y base de cálculo                         | P-C2                             |
| L-04 | Consecuencias tributarias para el ganador de un premio de alto valor           | Advertencia obligatoria en bases |
| L-05 | Emisor del comprobante al comprador del ticket y base imponible                | Motor de liquidación             |
| L-06 | Calificación de LIBOX como sujeto obligado en materia de prevención financiera | Carga operativa de §19           |
| L-07 | Admisibilidad de LIBOX como agente de custodia de fondos                       | Modelo de garantía patrimonial   |
| L-08 | Plazo, requisitos y renovación del bloqueo registral                           | Duración máxima de venta en P-C  |
| L-09 | Requisitos del cónyuge cuando el bien es social                                | P-C                              |
| L-10 | Límite de responsabilidad oponible al consumidor                               | Términos y condiciones           |
| L-11 | Plantilla notarial única, versionada                                           | P-C                              |
| L-12 | Protocolo de menor detectado con posterioridad, por categoría                  | §17.3                            |

# Anexo D — Registro de invariantes

| \#              | Invariante                                                                                                                   | Sección      |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------ |
| INV-01 a INV-05 | Neutralidad económica frente al azar                                                                                         | §1.2         |
| INV-06-a        | En oportunidades con recaudación, ningún participante pierde su aporte                                                       | §1.5         |
| INV-06-b        | En oportunidades sin recaudación la protección se traslada al premio, con garantía sustitutiva como condición de publicación | §1.5         |
| INV-07          | SUPPORT atesta, no mueve dinero                                                                                              | §2.4         |
| INV-08          | Unicidad de documento, correo y teléfono                                                                                     | §17.1        |
| INV-09          | No hay ticket válido sin pago confirmado                                                                                     | §3.2         |
| INV-10          | Los asientos cuadran                                                                                                         | §10.1        |
| INV-11          | Los números anulados no se reasignan                                                                                         | §3.2         |
| INV-12          | Un sorteo ejecutado no se re-ejecuta                                                                                         | §12.2        |
| INV-13          | Límite de concentración                                                                                                      | §20.2        |
| INV-14          | Bases inmutables desde la publicación                                                                                        | §3.2         |
| INV-15          | Vigencia de configuración al publicar                                                                                        | §24.3        |
| INV-16          | Suficiencia de la recaudación retenida                                                                                       | §10.4        |
| INV-17          | T8 no altera la matemática                                                                                                   | §5.1         |
| INV-18          | Ventana entre compromiso y baliza                                                                                            | §12.2        |
| INV-19          | Unicidad de ejecución del sorteo                                                                                             | §12.2        |
| INV-20          | Solo roles internos mueven la sala                                                                                           | §13.4        |
| INV-21          | Nadie completa solo la cadena al desembolso                                                                                  | §13.5        |
| INV-22          | Controversia resuelta por evidencia                                                                                          | §14.1        |
| INV-23          | Evaluación determinista de gates                                                                                             | §15.1        |
| INV-24          | Ruta de resolución declarada e inmutable                                                                                     | §16.1        |
| INV-25          | El re-sorteo no aplica al incumplimiento del organizador                                                                     | §16.3        |
| INV-26          | El saldo de reembolso no admite carga voluntaria                                                                             | §16.5        |
| INV-27          | Sin techo, con acreditación previa por tramo                                                                                 | §19.2        |
| INV-28          | La reputación no exime de la verificación de valor                                                                           | §21.2        |
| INV-29          | Ninguna regla de jurisdicción en el código                                                                                   | §24.1        |
| INV-30          | Multi-moneda sin conversión                                                                                                  | §24.5        |
| INV-31          | El mercado pertenece al sorteo                                                                                               | §24.5        |
| INV-32          | Aplicación cliente única                                                                                                     | §24.6, §33.1 |
| INV-33          | La suspensión nunca retiene dinero de terceros                                                                               | §25          |
| INV-34          | El neto del organizador es el 80 % sea cual sea el régimen tributario                                                        | §9.2         |
| INV-35          | El impuesto nunca supera la comisión                                                                                         | §9.2         |
| INV-36          | El redondeo tributario nunca reduce el neto del organizador                                                                  | §9.2         |
| INV-18-bis      | La anterioridad de la baliza es comprobable contra la fuente, sin confiar en LIBOX                                           | §12.2        |
| INV-37          | Ninguna excepción de tasa supera el techo del mercado                                                                        | §1.3.1       |
| INV-38          | Existen al menos dos `ADMIN_SUPER` activos en todo momento                                                                   | §2.6.2       |
| INV-39          | El sistema trata a una parte relacionada igual que a cualquier organizador                                                   | §1.2.1       |
| INV-40          | Ninguna oportunidad se publica bajo el suelo de recaudación                                                                  | §1.3.2       |
| INV-41          | Ninguna supera el techo sin doble firma registrada                                                                           | §1.3.2       |
| INV-42          | Igualdad de probabilidad entre vía gratuita y pagada                                                                         | §5.5         |
| INV-43          | El régimen promocional no genera liquidación                                                                                 | §5.6         |
| INV-44          | Registrables prohibidos sin recaudación, salvo custodia efectiva                                                             | §6.5         |
| INV-45          | La capa más restrictiva gana en el control de funciones                                                                      | §2.8         |
| INV-46          | Ninguna suscripción otorga participaciones ni probabilidad                                                                   | §26.4        |

*LIBOX PRD BLUEPRINT MVP V9 — Nivel L2. Gobernado por LBPF V3 conforme a R-02. Los artefactos de nivel L3 del Anexo A son requisito previo al arranque de la construcción.*
