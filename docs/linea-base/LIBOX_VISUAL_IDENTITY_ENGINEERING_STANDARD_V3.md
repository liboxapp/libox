# Índice de contenidos

# 0\. Control documental, alcance y encaje fundacional

**Documento:** LIBOX\_Visual\_Identity\_Engineering\_Standard\_V3 **Versión:** V3 **Naturaleza:** documento auxiliar controlado de identidad visual **Reemplaza:** VIES V2 (deprecado en su totalidad) **Estado:** vigente · arte de marca **congelado** · **documento autónomo**

**Regla de autonomía.** Este documento contiene la totalidad del estándar de identidad. No remite a versiones anteriores para ningún contenido normativo. Una versión que derogue a la anterior y a la vez dependa de ella para definir el isotipo, la unidad X o el lockup deja ese contenido sin documento vigente.

Conforme a la política de control documental de LIBOX no existen subversiones: todo cambio incrementa la versión completa de V(X) a V(X+1). Esta versión no modifica el arte de marca. Corrige **especificaciones técnicas de aplicación** que resultaban inejecutables o contraproducentes en las plataformas de destino, y precisa el alcance del sistema cromático frente al nivel L4.

## 0.0 Changelog

### Cambios de la versión V3

| Versión | Sección                                             | Qué cambió                                                                             | Por qué                                                                                                                                                                                                                                                                                                   | Decisión que invalida       |
| ------- | --------------------------------------------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| V3      | §1, §2, §3, §5, §7, §8, §9, §10, §12, §13, §14, §15 | **Contenido íntegro incorporado.** Se eliminan todas las remisiones a V1               | V2 declaraba a V1 *deprecado en su totalidad* y a la vez remitía a él en quince pasajes. El isotipo, la unidad X, el plano técnico, el lockup, las variantes, las prohibiciones, los tamaños mínimos, la exportación y la gobernanza **quedaban sin documento vigente**. Era una derogación sin sustituto | Deroga las remisiones de V2 |
| V3      | §8.1                                                | `NP-09` **sustituido por** `NP-09`                                                     | Un código de marcador de posición en un documento que rige a proveedores externos                                                                                                                                                                                                                         | Corrige V2                  |
| V3      | §0.1                                                | Referencias actualizadas a PRD MVP V7, L3 V3 y Enterprise V3                           | La línea funcional vigente cambió                                                                                                                                                                                                                                                                         | Corrige V2                  |
| V3      | Anexo A                                             | Requisito de incorporación del arte maestro mantenido y reforzado con lista de entrega | Sin el arte maestro, cada pieza puede desviarse                                                                                                                                                                                                                                                           | Amplía                      |

### Cambios de la versión V2

| Versión | Sección | Qué cambió                                                                                                                                                       | Por qué                                                                                                                                                                                                                      | Decisión que invalida                           |
| ------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| V2      | §11     | **Corregida la especificación del icono de aplicación.** iOS exige lienzo cuadrado completo sin transparencia; Android exige icono adaptable con capas separadas | *“Isotipo en contenedor redondeado”* es incorrecto en iOS: el sistema aplica su propia máscara y un contenedor ya redondeado produce doble redondeo con halo. En Android, un archivo plano no admite el recorte del lanzador | Deroga la fila de tiendas de aplicaciones de V1 |
| V2      | §11     | **Añadida la especificación de icono de notificación**                                                                                                           | El icono de barra de estado de Android descarta el color y conserva solo el canal alfa. Un isotipo con degradado se renderiza como una mancha blanca sólida, ilegible. Requiere silueta monocroma creada a propósito         | Amplía                                          |
| V2      | §11     | **Añadidos icono enmascarable de PWA, colores de manifiesto e imagen de compartición**                                                                           | El producto nace como web adaptable y aplicación progresiva; faltaban los activos que esa naturaleza exige                                                                                                                   | Amplía                                          |
| V2      | §11     | **Añadidas reglas de correo**                                                                                                                                    | Muchos clientes de correo bloquean SVG, suprimen imágenes de fondo y desactivan imágenes por defecto                                                                                                                         | Amplía                                          |
| V2      | §6      | **Precisado el alcance del sistema cromático** con contrastes medidos, y delimitada la frontera con la paleta de producto de L4                                  | Signal Violet rinde 4,23:1 y Success Green 2,54:1 sobre blanco: ninguno alcanza el mínimo para texto normal. La redacción anterior podía inducir a usarlos como color de texto                                               | Precisa §6 de V1                                |
| V2      | §4      | **Precisado que Manrope ExtraBold es exclusivo del wordmark**                                                                                                    | La redacción anterior podía leerse como tipografía de sistema. Ese peso como base de interfaz es ilegible en párrafo                                                                                                         | Precisa §4 de V1                                |
| V2      | §0.1    | **Declarada la existencia del nivel L4** y la relación de consumo                                                                                                | Al emitirse el Design System, VIES pasa a ser fuente consumida por L4 en materia de marca                                                                                                                                    | Precisa §0.1 de V1                              |
| V2      | Anexo A | **Requisito de adjuntar el arte maestro y los planos**                                                                                                           | La versión anterior declaraba el arte congelado como fuente de verdad sin que estuviera incorporado al paquete                                                                                                               | Amplía                                          |

## 0.1 Encaje con los documentos fundacionales

| Nivel  | Documento                                          | Relación                                                                                                         |
| ------ | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| L0     | LBPF V3                                            | **Gobierna este documento.** Toda aplicación visual se subordina a las zonas conductuales y al veto anti-impulso |
| L1     | Product Strategy                                   | Pendiente de emisión                                                                                             |
| L2     | PRD MVP V9 · PRD Enterprise V3                     | Definen superficies y reglas; VIES no las modifica                                                               |
| L3     | Especificación Técnica L3 V7                       | Define implementación; VIES no la modifica                                                                       |
| **L4** | **Design System & Product Experience Standard V1** | **Consume este documento** en materia de marca y **deriva de él** la paleta de producto                          |

**VIES no es L0, L2, L3 ni L4.** Es un documento auxiliar controlado que gobierna la identidad de marca. La frontera con L4 es la siguiente: **VIES gobierna la marca; L4 gobierna el producto.**

## 0.2 Alcance y no-alcance

**Gobierna:** isotipo LB Opportunity Loop · wordmark LIBOX · lockup oficial · tagline · sistema métrico y unidad X · área segura y tamaños mínimos · colores de marca · variantes autorizadas y usos prohibidos · estándares de exportación · aplicaciones de marca en superficies digitales y corporativas · gobernanza del arte.

**No gobierna:** diseño de pantallas transaccionales · componentes de interfaz · microcopy · movimiento de producto · paleta de estados del producto · tipografía de interfaz · reglas de negocio · arquitectura técnica.

Todo lo del segundo grupo corresponde a **L4**.

# 1\. Arquitectura visual de LIBOX

El sistema visual de LIBOX se organiza en cuatro componentes oficiales: **isotipo LB Opportunity Loop**, **wordmark LIBOX**, **lockup horizontal** y **tagline**. Cada componente tiene una función específica y no sustituye a los demás: el isotipo resuelve el reconocimiento compacto, el wordmark la denominación de marca, el lockup el uso institucional y el tagline la memoria verbal.

La identidad pertenece a la **Ruta 2: geometría más personalidad**. El sistema debe verse tecnológico y confiable sin perder cercanía. La geometría aporta rigor; los radios y la continuidad aportan calidez. La marca evita verse excesivamente bancaria, gubernamental, de videojuego o de especulación con criptoactivos.

El monograma LB representa entrada, participación, verificación y oportunidad. El wordmark refuerza claridad, solidez y escalabilidad. La promesa se expresa en el tagline: **Tu próxima oportunidad.**

> **Criterio de coherencia fundacional.** La identidad debe sostener la tesis de LIBOX como infraestructura de confianza y oportunidad verificable. La marca puede ser aspiracional, pero nunca debe parecer casino, negociación especulativa, entusiasmo cripto ni juego impulsivo.

# 2\. Sistema métrico y unidad X

Todas las medidas se expresan en **X**. La X no es una medida fija en milímetros ni en píxeles: es una unidad proporcional que permite escalar la marca de forma consistente desde el favicon hasta el gran formato.

| Variable    | Valor                    | Uso                                        |
| ----------- | ------------------------ | ------------------------------------------ |
| X           | Unidad base proporcional | Define todas las cotas del sistema         |
| Isotipo     | 10X de alto              | Caja primaria del monograma LB             |
| Wordmark    | 10X de alto visual       | Alineación óptica con el isotipo           |
| Separación  | 1X                       | Distancia oficial entre isotipo y wordmark |
| Tracking    | 0,25X                    | Espaciado oficial del wordmark             |
| Área segura | 1X                       | Protección externa mínima                  |

**La marca escala como conjunto.** No se permite escalar el isotipo con independencia del wordmark ni alterar la separación entre ambos. Cualquier variación produce inconsistencia visual y constituye uso no autorizado.

# 3\. Plano técnico del isotipo LB Opportunity Loop

El isotipo oficial es un monograma simbólico LB integrado en una sola forma continua. La **L** debe ser reconocible como estructura primaria y la **B** debe aparecer integrada, sin convertirse en una B aislada ni leerse como un «13».

| Elemento                       | Regla técnica                                                                                                                              |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Caja de construcción           | 10X × 10X. La caja no equivale necesariamente al área visible exacta, porque el centro óptico compensa masas curvas y extremos redondeados |
| Grosor estructural recomendado | 2,2X                                                                                                                                       |
| Radio exterior                 | 5X                                                                                                                                         |
| Radio interior referencial     | 2,8X                                                                                                                                       |
| Radio de esquinas              | 1,1X                                                                                                                                       |
| Extremos                       | Redondeados. La continuidad visual es obligatoria                                                                                          |
| Centro óptico                  | La alineación con el wordmark se realiza por centro óptico, nunca por centro geométrico                                                    |

El isotipo debe mantener lectura simultánea de L y B. Si la B domina, el símbolo pierde suficiencia como monograma. Si la L domina, pierde personalidad. La versión congelada busca el equilibrio entre legibilidad, fuerza visual y calidez tecnológica.

# 4\. Ingeniería tipográfica del wordmark

*El wordmark se construye conforme a §4 de este documento.* El wordmark LIBOX se compone en **Manrope ExtraBold en mayúsculas**, con el tracking, la altura y las proporciones definidas en el Plano 02.

## 4.1 Precisión sobre el alcance tipográfico

**Manrope ExtraBold es el peso del wordmark. No es la tipografía de interfaz del producto.**

La redacción de V1 podía leerse como si estableciera una tipografía de sistema. No lo hace ni le corresponde: la tipografía de interfaz, su escala y sus pesos son materia de L4.

| Ámbito               | Fuente                                                   |
| -------------------- | -------------------------------------------------------- |
| Wordmark             | **Manrope ExtraBold (800), mayúsculas** — este documento |
| Interfaz de producto | Manrope en pesos 400, 500, 600 y 700 — **L4 §2.3**       |
| Peso 800 en interfaz | **Prohibido.** Ilegible en párrafo y agresivo en titular |

La elección de Manrope para el producto responde a coherencia de familia, no a herencia de peso.

# 5\. Lockup oficial y composición horizontal

La configuración oficial es **LB LIBOX**: isotipo a la izquierda, wordmark a la derecha. Es la versión prioritaria para espacio de trabajo corporativo, sitio web, presentaciones, documentos y comunicación institucional.

| Elemento   | Regla                                                                                                                                                                                            |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Separación | 1X entre isotipo y wordmark. Distancias mayores fragmentan la marca; menores reducen la legibilidad                                                                                              |
| Alineación | Vertical por centro óptico. En aplicaciones digitales el conjunto debe verse centrado aunque geométricamente existan compensaciones                                                              |
| Tagline    | *Tu próxima oportunidad.* puede usarse debajo del wordmark en piezas institucionales, presentaciones a inversionistas y banners. **No debe colocarse dentro del área de seguridad del logotipo** |

# 6\. Sistema cromático

## 6.1 Colores de marca

Sin cambios en los valores. Son los seis colores oficiales de LIBOX.

| Color         | HEX       | RGB           | Uso de marca               |
| ------------- | --------- | ------------- | -------------------------- |
| LIBOX Purple  | `#6D28D9` | 109, 40, 217  | Isotipo y acento primario  |
| Trust Navy    | `#0B1020` | 11, 16, 32    | Wordmark y fondos oscuros  |
| Signal Violet | `#8B5CF6` | 139, 92, 246  | Gradiente y acentos        |
| Success Green | `#10B981` | 16, 185, 129  | Señal de confianza         |
| Light Gray    | `#E5E7EB` | 229, 231, 235 | Fondos y líneas auxiliares |
| White         | `#FFFFFF` | 255, 255, 255 | Fondos y versión negativa  |

## 6.2 Contraste medido

V1 indicaba que el morado sobre fondos oscuros debía verificarse. Esta versión aporta las mediciones completas, porque la redacción anterior podía inducir a emplear como texto colores que no lo admiten.

| Color         | Sobre blanco | Texto normal AA | Texto ≥18 pt  | Sobre Trust Navy    |
| ------------- | ------------ | --------------- | ------------- | ------------------- |
| LIBOX Purple  | **7,10:1**   | Cumple          | Cumple        | 2,66:1 — no apto    |
| Trust Navy    | **18,93:1**  | Cumple          | Cumple        | —                   |
| Signal Violet | **4,23:1**   | **No cumple**   | Cumple        | 4,47:1 — cumple     |
| Success Green | **2,54:1**   | **No cumple**   | **No cumple** | **7,46:1** — cumple |
| Light Gray    | 1,24:1       | No aplica       | No aplica     | 15,29:1             |

## 6.3 Reglas de uso derivadas

| \#    | Regla                                                                                                                                         |
| ----- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| CR-01 | **Signal Violet no se usa como texto de tamaño normal.** Se admite en texto de 18 pt o superior, gradientes y elementos decorativos           |
| CR-02 | **Success Green no se usa como texto sobre fondo claro.** Se admite como relleno con texto oscuro encima, y como texto sobre Trust Navy       |
| CR-03 | **LIBOX Purple no se usa como texto sobre fondos oscuros.** Sobre blanco es apto para texto normal                                            |
| CR-04 | Todo texto sobre gradiente exige capa sólida de oscurecimiento detrás. El gradiente no garantiza contraste por sí solo                        |
| CR-05 | Los gradientes se permiten únicamente de LIBOX Purple a Signal Violet. Prohibidos arcoíris, metálicos, neón excesivo y texturas especulativas |

## 6.4 Frontera con la paleta de producto

Los seis colores de este documento son **la paleta de marca**. Una interfaz transaccional requiere además estados de advertencia, error, información y retención, que la marca no contempla y **que no le corresponde contemplar**.

**L4 §2.2 deriva la paleta de producto a partir de esta**, verificando contraste y añadiendo los estados faltantes. Esa derivación **no altera ningún color de marca**: los colores de marca conservan íntegro su uso en isotipo, wordmark, acentos y superficies de atracción.

Ejemplo de la distinción: el chip *Pagado* del panel de liquidaciones usa `#047857` como texto sobre fondo `#D1FAE5`. No es Success Green porque Success Green no alcanza contraste de texto. La señal de confianza de la marca sigue siendo `#10B981` y se usa como tal.

# 7\. Variantes autorizadas

| Variante          | Uso permitido                                                                                                         |
| ----------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Positivo**      | Isotipo en LIBOX Purple o gradiente oficial; wordmark en Trust Navy; fondo blanco o neutro claro                      |
| **Negativo**      | Isotipo en LIBOX Purple o gradiente oficial; wordmark en blanco; fondo Trust Navy o negro                             |
| **Monocromático** | Negro o blanco, para impresión, sellos, grabados, bordados o cuando el color no sea viable                            |
| **Isotipo solo**  | Favicon, icono de aplicación, avatar de redes, perfil, marcas de agua y todo espacio que no admita el lockup completo |

# 8\. Usos no permitidos

| \#        | Categoría                        | Prohibición                                                                                                                                   |
| --------- | -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| NP-01     | Deformación                      | No estirar, comprimir, sesgar, rotar ni aplicar perspectiva al isotipo, al wordmark o al lockup                                               |
| NP-02     | Alteración de color              | No sustituir los colores oficiales por tonos no aprobados. No usar degradados no autorizados                                                  |
| NP-03     | Alteración tipográfica           | No sustituir Manrope ExtraBold. No alterar el tracking de 0,25X. No reemplazar el wordmark por texto editable sin control                     |
| NP-04     | Sombras y efectos                | No aplicar sombras duras, biselados, resplandor excesivo, metalizados, texturas ni efectos tridimensionales al arte maestro                   |
| NP-05     | Fondos de bajo contraste         | No colocar la marca sobre imágenes o fondos que reduzcan la lectura. Con imagen de fondo, aplicar capa de oscurecimiento o contenedor         |
| NP-06     | Apariencia incompatible con LBPF | No emplear tratamientos que acerquen la marca a casino, videojuego agresivo, especulación con criptoactivos o urgencia emocional falsa        |
| NP-07     | Reconstrucción                   | No redibujar, vectorizar ni trazar manualmente el isotipo a partir de una imagen de referencia                                                |
| NP-08     | Encerramiento                    | No encerrar la marca en formas, marcos ni contenedores no autorizados                                                                         |
| **NP-09** | **Icono de aplicación**          | **Prohibido entregar el icono de aplicación con esquinas redondeadas o transparencia para plataformas que aplican máscara propia.** Ver §11.2 |

# 9\. Tamaños mínimos y rendimiento en escala

| Contexto                      | Regla                                                                                                                                  |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Digital                       | Ancho mínimo del lockup: **120 px**. Por debajo se evalúa el uso del isotipo solo                                                      |
| Favicon e icono de aplicación | El isotipo debe funcionar a **32 px**. A 16 px se usa versión simplificada o mapa de bits optimizado                                   |
| Impresión                     | Ancho mínimo del lockup impreso: **30 mm**. En aplicaciones menores, isotipo solo y sin tagline                                        |
| Prueba de legibilidad         | Toda exportación se prueba a 16, 32, 64, 128 y 512 px. La L y la B deben conservar lectura conceptual incluso en los tamaños reducidos |

**Por debajo de 32 px se usa exclusivamente el isotipo.** El lockup a esa escala es una mancha ilegible.

# 10\. Estándares de exportación

| Formato | Regla de salida                                                                                                                           |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **SVG** | Archivo maestro digital. Vectores limpios, `viewBox` correcto y nombres de capa coherentes. **No incrustar mapas de bits dentro del SVG** |
| **PDF** | Formato vectorial de intercambio para impresión, prensa y proveedores. Arte vectorial con espacio de color adecuado                       |
| **EPS** | Para imprenta, serigrafía, bordado y merchandising cuando el proveedor lo requiera                                                        |
| **PNG** | Raster con transparencia para espacio de trabajo, web, interfaz y redes. **Exportado desde el vector maestro, nunca desde una captura**   |
| **JPG** | Con fondo sólido, para presentaciones y plataformas que no admitan transparencia                                                          |

Los activos digitales de §11 forman parte del paquete de exportación.

> **Regla de proveedor.** Todo proveedor externo recibe archivos oficiales. No se aceptan redibujos, capturas, trazados manuales ni exportaciones derivadas de imágenes de referencia.

# 11\. Aplicaciones digitales: web universal, PWA y futuras aplicaciones

## 11.1 Principio rector

*Íntegro en este documento.*

La identidad visual debe funcionar primero en una **página web adaptable universal**, accesible desde cualquier sistema operativo y dispositivo electrónico compatible con navegador moderno. Esta orientación es coherente con la línea fundacional del MVP: LIBOX nace como experiencia web adaptable y aplicación web progresiva, **sin depender de una aplicación nativa** para operar la oportunidad, la compra, la verificación ni la resolución.

En el mediano plazo, LIBOX podrá incorporar aplicaciones nativas para Android e iOS. **Esa evolución no reemplaza la web: extiende la distribución.** Por tanto, el sistema visual debe estar preparado para funcionar en navegador, aplicación progresiva, icono de aplicación, tiendas, redes, notificaciones, correos y documentos.

Este principio es coherente con **PRD MVP V9 §33.1 e INV-32**, que establecen aplicación web adaptable universal más aplicación progresiva instalable, con las nativas como fase posterior sobre la misma interfaz de programación, y con la web sin depreciar nunca.

## 11.2 Iconos de aplicación — especificación corregida

**Esta es la corrección principal de V2.** La instrucción de V1 —*isotipo en contenedor redondeado*— es incorrecta para las plataformas de destino y produce defectos visibles.

| Plataforma                  | Especificación                                                                                                                            | Por qué                                                                                                                                                                       |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **iOS**                     | Lienzo **cuadrado completo**, 1024 × 1024 px, **sin transparencia y sin esquinas redondeadas**. El isotipo sobre LIBOX Purple sólido      | iOS aplica su propia máscara de esquinas. Entregar un contenedor ya redondeado produce **doble redondeo** con halo del color de fondo, y la transparencia se rellena en negro |
| **Android adaptable**       | **Dos capas separadas** de 108 × 108 dp: fondo en LIBOX Purple sólido y primer plano con el isotipo, con **zona segura central de 66 dp** | El lanzador recorta según la máscara del fabricante —círculo, cuadrado, escudo—. Un archivo plano se recorta mal                                                              |
| **PWA, icono estándar**     | 192 y 512 px, cuadrado completo, sin transparencia                                                                                        | Instalación y lista de aplicaciones                                                                                                                                           |
| **PWA, icono enmascarable** | 512 px con **zona segura del 80 % centrada**                                                                                              | El sistema recorta según su propia máscara                                                                                                                                    |
| **Touch icon de Apple**     | 180 px, cuadrado completo, sin transparencia ni esquinas redondeadas                                                                      | Igual criterio que iOS                                                                                                                                                        |

**Regla común:** el wordmark no se usa dentro de ningún icono de aplicación. El reconocimiento a tamaños pequeños recae exclusivamente en el isotipo.

## 11.3 Iconos de notificación — especificación nueva

**Corrección técnica de consecuencia visible.**

| Plataforma                   | Especificación                                                       | Por qué                                                                                                                                                                                       |
| ---------------------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Android, barra de estado** | **Silueta monocroma con transparencia**, 24 × 24 dp. Solo canal alfa | El sistema **descarta todo el color** y conserva únicamente la forma, que después tiñe. Un isotipo morado con degradado se renderiza como una **mancha blanca sólida**, sin forma reconocible |
| Android, icono grande        | Isotipo a color, 256 × 256 px                                        | Cuerpo expandido de la notificación                                                                                                                                                           |
| Web                          | Isotipo a color, 192 × 192 px                                        | Notificación de navegador                                                                                                                                                                     |
| Insignia                     | Silueta monocroma, 96 × 96 px                                        | Indicador compacto                                                                                                                                                                            |

**Requiere una versión de silueta creada a propósito.** No se obtiene aplanando el isotipo: hay que simplificar el trazo para que resulte legible a 24 dp en una sola tinta.

## 11.4 Manifiesto de la aplicación progresiva

| Propiedad          | Valor                | Efecto                                    |
| ------------------ | -------------------- | ----------------------------------------- |
| `theme_color`      | `#0B1020` Trust Navy | Barra del sistema                         |
| `background_color` | `#FFFFFF`            | Pantalla de arranque durante la carga     |
| `display`          | `standalone`         | Sin barra de navegador                    |
| `orientation`      | `any`                | Ninguna función depende de la orientación |

`background_color` **es blanco y no Trust Navy** por una razón de percepción: la pantalla de arranque debe empalmar con la primera superficie real, que es clara. Un arranque oscuro seguido de una interfaz clara produce un destello desagradable.

## 11.5 Imagen de compartición

| Aspecto               | Especificación                                                                                   |
| --------------------- | ------------------------------------------------------------------------------------------------ |
| Dimensiones           | **1200 × 630 px**, PNG                                                                           |
| Composición           | Imagen del premio · título del sorteo · **precio del ticket y probabilidad** · lockup en esquina |
| Título                | Máximo 60 caracteres                                                                             |
| Descripción           | Premio, precio y probabilidad. Máximo 155 caracteres                                             |
| Reserva institucional | Lockup sobre `gradient.brand` cuando no hay sorteo asociado                                      |

**Incluye la probabilidad de forma deliberada.** Una imagen compartida que mostrase solo premio y precio incumpliría DP-03 fuera de la plataforma. La norma conductual del LBPF **no termina en el borde del dominio**.

## 11.6 Favicon

`favicon.svg` como principal, con variante para esquema oscuro · `favicon.ico` multitamaño de 16, 32 y 48 px como reserva · **solo isotipo**, nunca lockup.

## 11.7 Correo

| Aspecto                | Regla                                            | Por qué                                                                           |
| ---------------------- | ------------------------------------------------ | --------------------------------------------------------------------------------- |
| Formato del logotipo   | **PNG a doble resolución con ancho fijo**        | Muchos clientes bloquean SVG                                                      |
| Fondos                 | Color plano, sin imágenes de fondo               | Muchos clientes las suprimen                                                      |
| Ancho                  | 600 px, con versión fluida para móvil            | Estándar de compatibilidad                                                        |
| Modo oscuro            | Versión negativa del lockup con reserva en claro | El logotipo oscuro desaparece sobre fondo oscuro                                  |
| Texto alternativo      | Obligatorio en toda imagen                       | Las imágenes están bloqueadas por defecto en muchos clientes                      |
| Versión de texto plano | Obligatoria en notificaciones críticas           | Un ganador con imágenes bloqueadas no puede perder su premio por no ver el correo |

## 11.8 Superficies digitales

| Superficie                       | Uso oficial                                                                                                                                                                                              |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Web, aplicación web y progresiva | Lockup horizontal en el encabezado institucional; isotipo para favicon, estados de carga y espacios compactos. **El logotipo no compite con costo, probabilidad, pool ni evidencia en Zona de Decisión** |
| Espacio de trabajo corporativo   | Lockup horizontal 600 × 200 px, fondo transparente o blanco. Sin recortar el isotipo ni ampliar el tracking                                                                                              |
| Instagram y mensajería           | Isotipo solo, 1024 × 1024 px con área segura. Sin wordmark: se pierde a tamaño de avatar                                                                                                                 |
| Red profesional                  | Empresa: lockup. Perfil: isotipo. Cabecera: lockup con tagline opcional                                                                                                                                  |
| Vídeo                            | Avatar: isotipo. Cabecera: lockup con tagline, respetando el área segura central                                                                                                                         |
| **Tiendas de aplicaciones**      | **Según §11.2.** Sin wordmark dentro del icono. Reconocimiento del LB a tamaños pequeños                                                                                                                 |
| Futuras aplicaciones nativas     | El sistema visual se reutiliza. Toda adaptación conserva isotipo, wordmark, paleta, tracking, área segura y criterios de contraste                                                                       |

# 12\. Aplicaciones corporativas

| Aplicación      | Regla                                                                                                                      |
| --------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Documentos      | Lockup horizontal en portadas, encabezados y carátulas. En páginas internas puede usarse el isotipo pequeño                |
| Firma de correo | Lockup pequeño, datos de contacto y tagline opcional. Los iconos de redes no se colocan dentro del área de seguridad       |
| Presentaciones  | Isotipo en diapositivas internas; lockup en portada y cierre. Contraste alto y sin efectos decorativos sobre la marca      |
| Contratos       | Versión monocromática o positiva según la formalidad. Sin gradientes cuando la impresión sea económica o en blanco y negro |

# 13\. Sistema de identidad para inversionistas

| Pieza                   | Regla                                                                                                              |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Presentación            | Portada con lockup, tagline y fondo Trust Navy o blanco. Sin saturación gráfica sobre la marca                     |
| Documento de una página | Logotipo positivo, superior izquierdo o centrado. Jerarquía profesional y narrativa de oportunidades verificables  |
| Sala de datos           | Nomenclatura de archivos `LIBOX_AAAAMMDD_Version`. La marca refuerza percepción de orden y confiabilidad           |
| Dossier de prensa       | Incluye SVG, PDF, PNG con transparencia, JPG con fondo blanco, texto institucional, paleta y reglas básicas de uso |

# 14\. Gobernanza de marca

El arte maestro solo puede ser modificado por responsables de marca autorizados. Toda alteración aprobada registra versión completa, motivo, fecha, responsable, evidencia visual y lista de comprobación de liberación.

| Regla                                 | Mandato                                                                                                                                                                            |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Autoridad de marca**                | El arte maestro solo lo modifican responsables autorizados. Ningún proveedor, diseñador externo ni equipo interno puede redibujar la marca                                         |
| **Versionado entero obligatorio**     | No existen versiones V1.1, V1.2, V2.1 ni subversiones equivalentes. Todo cambio aprobado incrementa la versión completa: V1 → V2 → V3                                              |
| **Observaciones no aplicadas**        | Las observaciones, propuestas, defectos detectados y solicitudes de cambio se registran en un backlog de cambio; **no generan versión documental hasta ser aprobadas y aplicadas** |
| **Cambios que obligan nueva versión** | Toda modificación de isotipo, wordmark, lockup, fuente, tracking, proporciones, tagline, paleta principal, criterios de exportación o gobierno de marca                            |
| **Aprobación de proveedores**         | Los proveedores externos usan exclusivamente el paquete oficial                                                                                                                    |
| **Auditoría visual**                  | Todo uso crítico en web, aplicación, prensa, inversión o documentos oficiales se revisa contra esta especificación antes de publicar                                               |

## 14.1 Precisión sobre el registro de cambios

El mecanismo de V1 —las observaciones se registran en backlog de cambio y **no generan versión documental hasta ser aprobadas y aplicadas**— es correcto y se conserva. Se recomienda su adopción a nivel de corpus completo: es el mecanismo que hace viable el versionado monotónico sin que las correcciones se retrasen por evitar consumir versiones.

# 15\. Lista de comprobación de liberación de marca

| \# | Comprobación                                                                            | Estado requerido |
| -- | --------------------------------------------------------------------------------------- | ---------------- |
| 1  | ¿El isotipo corresponde a la Ruta 2 aprobada?                                           | Sí               |
| 2  | ¿Se percibe LB, y no solo B ni «13»?                                                    | Sí               |
| 3  | ¿El wordmark está en Manrope ExtraBold?                                                 | Sí               |
| 4  | ¿El wordmark usa tracking de 0,25X?                                                     | Sí               |
| 5  | ¿La separación isotipo–wordmark es 1X?                                                  | Sí               |
| 6  | ¿Se respeta el área segura de 1X?                                                       | Sí               |
| 7  | ¿Se usan LIBOX Purple y Trust Navy?                                                     | Sí               |
| 8  | ¿Funciona a 32 px, 120 px y 30 mm?                                                      | Sí               |
| 9  | ¿Los archivos SVG, PDF y EPS son vectoriales?                                           | Sí               |
| 10 | ¿La pieza fue aprobada por control de marca?                                            | Sí               |
| 11 | ¿La pieza evita apariencia de casino, videojuego, especulación o presión emocional?     | Sí               |
| 12 | ¿El contraste se verificó conforme a §6.2?                                              | Sí               |
| 13 | ¿El logotipo no compite con costo, probabilidad, pool ni evidencia en Zona de Decisión? | Sí               |
| 14 | ¿La exportación proviene del vector maestro y no de una captura?                        | Sí               |
| 15 | ¿El proveedor recibió el paquete oficial?                                               | Sí               |

**Comprobaciones de activos digitales:**

| \# | Comprobación                                                                                    |
| -- | ----------------------------------------------------------------------------------------------- |
| 16 | ¿Icono de iOS en lienzo cuadrado completo, sin transparencia ni esquinas redondeadas?           |
| 17 | ¿Icono de Android entregado en dos capas con zona segura de 66 dp?                              |
| 18 | ¿Icono enmascarable de PWA con zona segura del 80 %?                                            |
| 19 | ¿Icono de notificación de Android como silueta monocroma con transparencia?                     |
| 20 | ¿Imagen de compartición de 1200 × 630 px con precio y probabilidad?                             |
| 21 | ¿Logotipo de correo en PNG a doble resolución con texto alternativo y versión para modo oscuro? |
| 22 | ¿Colores del manifiesto declarados?                                                             |
| 23 | ¿Contraste verificado en todos los pares de uso, conforme a §6.2?                               |

# Anexo A — Referencia visual congelada

La referencia visual congelada de la Ruta 2 es la fuente principal de verdad del arte. **Prevalece sobre cualquier descripción textual de este documento.**

## A.1 Requisito de incorporación

**Corrección de proceso introducida en V2.** La versión anterior declaraba el arte congelado como fuente de verdad sin que estuviera incorporado al paquete documental. Un documento que apunta a una referencia que nadie posee no es controlable.

Se requiere incorporar como archivos adjuntos versionados: arte maestro del isotipo en vectorial · arte maestro del wordmark en vectorial y trazado · lockup oficial en sus variantes · Planos 01, 02 y 03 · paquete de exportación completo, incluidos los activos digitales de §11.

**Hasta que el arte maestro esté incorporado, la fuente de verdad efectiva es la descripción textual de este documento**, lo cual es una situación transitoria y no deseable.

# Anexo B — Plano 01: sistema métrico y reglas no negociables

*Pendiente de incorporación conforme al Anexo A.1.*

# Anexo C — Plano 02: wordmark y reglas tipográficas

*Pendiente de incorporación conforme al Anexo A.1.*

# Anexo D — Plano 03: estándares de exportación y aplicaciones

*Pendiente de incorporación conforme al Anexo A.1.* Incluye los activos digitales especificados en §11.

# Anexo E — Matriz de trazabilidad fundacional

| Documento                         | Relación con VIES V3                                                                   |
| --------------------------------- | -------------------------------------------------------------------------------------- |
| LBPF V3 (L0)                      | Gobierna. Zonas conductuales, veto anti-impulso y prevalencia visual                   |
| PRD MVP V9 (L2)                   | §33.1 e INV-32 sustentan el principio rector de §11.1                                  |
| PRD Enterprise V3 (L2)            | Reutilización del sistema visual en fase de aplicaciones nativas                       |
| Especificación Técnica L3 V7 (L3) | Sin relación directa                                                                   |
| **Design System L4 V2**           | **Consume VIES V3.** Deriva de §6 la paleta de producto y de §4 la familia tipográfica |

# Anexo F — Gestión del cambio de V2 a V3

| \# | Cambio                                                  | Naturaleza                                                                  |
| -- | ------------------------------------------------------- | --------------------------------------------------------------------------- |
| 1  | Icono de aplicación para iOS y Android                  | **Corrección técnica.** La especificación anterior producía defecto visible |
| 2  | Icono de notificación de Android                        | **Corrección técnica.** La ausencia producía un icono ilegible              |
| 3  | Activos de aplicación progresiva, compartición y correo | Ampliación coherente con la naturaleza web del producto                     |
| 4  | Contrastes medidos y reglas de uso cromático            | Precisión. Los valores de marca no cambian                                  |
| 5  | Alcance de Manrope ExtraBold                            | Precisión. La construcción del wordmark no cambia                           |
| 6  | Declaración del nivel L4 y su relación                  | Precisión de encaje fundacional                                             |
| 7  | Requisito de incorporación del arte maestro             | Corrección de proceso                                                       |

**Ningún cambio de V2 altera el arte de marca.** Isotipo, wordmark, lockup, tagline, sistema métrico y colores permanecen idénticos.

# Anexo G — Decisión del comité fundador

Se conserva la decisión del comité fundador sobre la Ruta 2 como identidad oficial de LIBOX, con el arte congelado y la gobernanza establecida en §14.

*LIBOX Visual Identity Engineering Standard V3. Documento auxiliar controlado. Gobernado por LBPF V3. Consumido por el Design System L4 V2 en materia de marca.*
