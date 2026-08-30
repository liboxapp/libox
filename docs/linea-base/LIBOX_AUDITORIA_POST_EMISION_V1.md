# Índice de contenidos

# 0\. Alcance

Auditoría de la línea base emitida, ejecutada **después** de congelarla y antes de construir. Verificación programática de trazabilidad cruzada entre los doce documentos vigentes, más revisión por dominio del comité.

**Distinción con la auditoría previa.** Aquella verificó las decisiones **antes** de emitirlas y encontró cuatro conflictos de invariante. Esta verifica **la emisión misma**: si lo decidido llegó completo a todos los niveles.

**Base medida:** 47 invariantes, 227 reglas de negocio, 135 tablas ejecutables, 21 subroles, 62 superficies, 136 historias.

# 1\. Veredicto

**La línea base es coherente en su núcleo y tiene un desfase de capa que hay que resolver antes de construir interfaz.**

| Dimensión                                        | Estado                                           |
| ------------------------------------------------ | ------------------------------------------------ |
| Trazabilidad de reglas L2 → L3, Matriz y Backlog | **Completa.** Cero reglas huérfanas              |
| Consistencia de cifras entre documentos          | **Completa**                                     |
| Referencias cruzadas de versión                  | **Cero obsoletas**                               |
| Ejecutabilidad del esquema                       | **Verificada.** 135 tablas, 13 pruebas negativas |
| **Propagación de las decisiones nuevas a L4**    | **Deficiente.** Ver §2                           |
| Registro de invariantes                          | Un huérfano                                      |
| Cobertura de superficies                         | **19 de 62 especificadas**                       |

**Un hallazgo bloqueante para la construcción de interfaz, uno menor, y cuatro observaciones de fondo del comité.**

# 2\. Hallazgo bloqueante · L4 no recibió las decisiones nuevas

## 2.1 La medición

| Elemento nuevo                      | PRD V8      | **L4 V1** | Matriz |
| ----------------------------------- | ----------- | --------- | ------ |
| PU-11 Directorio de organizadores   | 3 menciones | **0**     | 0      |
| PU-12 Perfil público de organizador | 3           | **0**     | 0      |
| Sorteo con entrada gratuita         | 4           | **0**     | 1      |
| Régimen promocional                 | 13          | **0**     | 2      |
| LIBOX Club                          | 3           | **0**     | 0      |
| Parte relacionada                   | 4           | **0**     | 1      |
| Código de campaña                   | 2           | **0**     | 1      |
| **P13 Igualdad de vía**             | 3           | **0**     | 0      |
| **BR-09 Proporción razonable**      | 2           | **0**     | 0      |
| **LINT-011**                        | 1           | **0**     | 0      |

**L4 V1 dice consumir PRD MVP V8 y LBPF V3, y no contiene ninguna de sus decisiones.** La referencia se actualizó en la pasada de coherencia; el contenido no.

## 2.2 Por qué ocurrió, y por qué importa

L4 se emitió **antes** que el PRD V8. La secuencia de emisión fue correcta para L0→L1→L2→L3, pero **L4 quedó fuera del ciclo** porque en el momento de la auditoría previa se decidió no reemitirlo, con el argumento de que las 43 fichas de superficie pendientes dependían del trabajo de diseño.

**Ese argumento sigue siendo válido para las fichas.** No lo es para el resto: los principios nuevos —igualdad de vía, proporción razonable, la prohibición de que un beneficio sea descuento de ticket— son **reglas de interfaz que no dependen de ningún diseño previo**.

**La consecuencia concreta:** el equipo que construya interfaz leerá L4 V1 y **no encontrará ninguna regla sobre sorteos gratuitos, régimen promocional ni suscripción**. Diseñará esas superficies interpretando el rector por su cuenta, que es exactamente el fallo que L4 existe para impedir y que ya ocurrió una vez con las piezas de la línea anterior.

## 2.3 Resolución

**L4 pasa a V2, con alcance acotado:**

| Entra                                               | No entra                               |
| --------------------------------------------------- | -------------------------------------- |
| P13, BR-09 y LINT-011 en el régimen de verificación | Las 43 fichas de superficie pendientes |
| Reglas de interfaz de sorteo con entrada gratuita   | Modo oscuro                            |
| Reglas de superficie del régimen promocional        | Estados vacíos ilustrados              |
| Ficha de PU-11 y PU-12                              |                                        |
| Reglas de LIBOX Club y de marca compartida          |                                        |
| Textos aprobados de los flujos nuevos               |                                        |

**Es una emisión de reglas, no de diseño.** Las fichas siguen esperando al trabajo de diseño, como estaba previsto.

# 3\. Hallazgo menor · Un invariante huérfano

**INV-06-b** se cita en L3 V7 y en el propio cuerpo del PRD, pero **no figura en el registro de invariantes del Anexo D del PRD**. Su gemelo INV-06-a sí.

Es el invariante que cubre la protección en oportunidades sin recaudación — precisamente la resolución del conflicto C-02 de la auditoría previa. **Que no esté en el registro significa que un lector que consulte solo el anexo concluirá que esa protección no existe.**

Corrección de una línea, y confirma el valor del criterio 11 que añadimos: *todo invariante que no aplique a un régimen lo declara explícitamente*.

# 4\. Observaciones del comité

Cuatro cosas que no son inconsistencias documentales, y que el comité considera de mayor consecuencia que los dos hallazgos anteriores.

## 4.1 · El producto creció más rápido que la capacidad de operarlo

**Cinco regímenes económicos coexisten ahora**: pagado, entrada gratuita con tres orígenes de premio, y promocional. Cada uno con su cadena de cierre, su modelo de garantía y su tratamiento contable.

**Con cuatro personas, cada régimen adicional multiplica la superficie de operación**, no la divide. El backlog lo reconoce en la estimación —936 SP— pero **el modelo de operación sigue dimensionado para uno solo**.

**Recomendación:** el encendido progresivo del Backlog §2.2 debe ampliarse para **secuenciar también los regímenes**, no solo los tipos y categorías. Lanzar con régimen pagado únicamente, y encender gratuito y promocional cuando exista relevo operativo.

## 4.2 · La línea promocional sigue sin dueño estratégico

El comité decidió no darle hito propio, y fue una decisión defendible: lanzar con sorteos promocionales posicionaría a LIBOX como agencia de marketing.

**Pero quedó sin nada.** No tiene métrica en L1, no tiene hipótesis, no aparece en la estrategia de captación de §7, y su modelo de costo unitario no está desarrollado — pese a que §6.3 identifica que **consume la misma capacidad operativa que un sorteo pagado sin generar comisión**.

**El riesgo no es que fracase: es que se venda mal.** Un plan de precio fijo mal calibrado contra un costo operativo desconocido pierde dinero en cada cliente y nadie lo nota hasta el cierre trimestral.

**Recomendación:** dos hipótesis en L1 —disposición a pagar y margen unitario— y su cálculo de costo antes de encenderlo.

## 4.3 · El descubrimiento cruzado depende de una superficie que nadie ha diseñado

H-07 —descubrimiento y compra cruzada— es la hipótesis que decide si LIBOX es marketplace o herramienta. **Y todo su mecanismo son PU-11 y PU-12**, que no tienen ficha en L4, ni caso de uso en la Matriz, ni criterio de aceptación más allá de una línea del backlog.

**Es la única funcionalidad crítica del modelo de negocio que llega a construcción sin especificar.** Trece puntos de historia para las dos superficies de las que depende la tesis entera.

**Recomendación:** ficha completa en L4 V2, y elevar US-130 a la revisión de diseño prioritaria junto con el detalle de oportunidad.

## 4.4 · Catorce meses sin usuario real, y el corpus no lo mitiga

El Backlog V3 declara 30 sprints. **El corpus documental es excelente y no reduce ese riesgo en un solo día.**

Lo que sí lo reduciría —F0, organizadores ancla, encendido acotado— está escrito en L1 y en el Backlog **como recomendación, sin fecha ni responsable**.

**Recomendación del comité, y es la única de este informe que no es documental:** F0 debe tener fecha de inicio esta semana y un responsable con nombre. Es lo único del plan que valida la hipótesis central del negocio sin gastar un sprint.

# 5\. Lo que la auditoría confirma

**Trazabilidad completa de reglas.** Cero reglas `RN` citadas en Matriz, L4, L3, Guía o Backlog que no existan en el PRD. La numeración soportó cinco versiones sucesivas sin fugas.

**Consistencia de cifras.** Suelo 1,25×, techo 4,0×, comisión 20 %, concentración 30 %, 21 subroles, 135 tablas, 936 SP: **todos idénticos allí donde aparecen**, en hasta cinco documentos distintos.

**Cero referencias cruzadas obsoletas** tras la corrección de las 53 detectadas en la última pasada.

**El esquema ejecuta y protege.** 135 tablas, cero errores, y trece pruebas negativas que confirman que las restricciones rechazan lo que deben. Es la única forma de saber que un invariante escrito es un invariante real.

**Y una observación de método que vale registrar:** los dos hallazgos de esta auditoría —el desfase de L4 y el invariante huérfano— **solo aparecieron con verificación programática**. Ninguno era visible leyendo. Es la tercera vez en esta sesión que ocurre.

# 6\. Resolución propuesta

| \# | Acción                                                                                               | Documento         | Bloquea                       |
| -- | ---------------------------------------------------------------------------------------------------- | ----------------- | ----------------------------- |
| 1  | **Emitir L4 V2** con reglas de interfaz de los regímenes nuevos, PU-11, PU-12, P13, BR-09 y LINT-011 | Design System     | **Construcción de interfaz**  |
| 2  | Incorporar INV-06-b al registro del Anexo D                                                          | PRD MVP V9        | Nada, pero induce a error     |
| 3  | Secuenciar el encendido **por régimen económico**, no solo por tipo y categoría                      | Backlog V4 §2.2   | Operación                     |
| 4  | Dos hipótesis y modelo de costo de la línea promocional                                              | L1 V4             | Precio del plan               |
| 5  | Ficha completa de PU-11 y PU-12                                                                      | L4 V2 y Matriz V2 | H-07                          |
| 6  | **F0 con fecha y responsable**                                                                       | —                 | **Nada. Y es lo más urgente** |

## 6.1 Sobre el congelamiento

El Backlog V3 declaró la línea base congelada, y el criterio para romperlo era: **un hallazgo que impida construir**.

**El punto 1 cumple ese criterio**: sin reglas de interfaz para los regímenes nuevos, esas superficies se diseñan por interpretación. Los puntos 2 a 5 **no lo cumplen** y pueden agruparse en una emisión posterior.

**Recomendación del comité:** emitir **L4 V2** ahora, agrupar los puntos 2 a 5 en una sola pasada posterior, y **empezar F0 y el encargo legal esta semana con independencia de todo lo anterior**.

*Auditoría de coherencia post-emisión. Ejecutada por verificación programática de trazabilidad cruzada más revisión del comité, sobre la línea base congelada.*
