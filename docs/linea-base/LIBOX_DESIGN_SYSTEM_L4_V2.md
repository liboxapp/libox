# Índice de contenidos

# 0\. Propósito, alcance y control documental

**Documento:** LIBOX\_DESIGN\_SYSTEM\_L4\_V2 **Versión:** V2 **Nivel:** L4 — Design System, UI Kit, Motion y Copy **Reemplaza:** ninguno. Primera versión de un nivel declarado y hasta ahora vacío. **Gobernado por:** LBPF V2 (L0) conforme a R-01 y R-02 **Consume:** PRD MVP V9 (L2) · Especificación Técnica L3 V7 (L3) · VIES V3 (identidad visual) **Estado:** vigente

## 0.1 Por qué existe este documento

El nivel L4 está declarado desde la primera versión de la pirámide documental, en **LBPF V3 §0.2** y en **L3 V7 §0.1**. Lo que no existía era el documento.

La consecuencia era concreta: las 60 superficies del PRD tenían reglas de negocio y contratos técnicos, pero ninguna especificación de cómo materializarlas. Cada equipo interpretaba el LBPF por su cuenta. Cuando eso ocurrió con las piezas visuales de la línea anterior, el resultado fueron once incumplimientos simultáneos del documento rector: tarjetas sin probabilidad ni tamaño de pool, claims absolutos, urgencia sin plazo real y llamados a la acción coercitivos.

**El LBPF dice qué es admisible. Este documento dice cómo se hace.** Sin él, la distancia entre norma y pantalla la rellena el criterio de quien esté diseñando ese día.

## 0.2 Qué gobierna y qué no

| Gobierna                                                                                                  | No gobierna                                                               |
| --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Traducción operativa del LBPF a interfaz: qué es obligatorio y qué está prohibido en cada zona conductual | Reglas de negocio, tipos de sorteo, pricing, liquidación, motor de sorteo |
| Tokens de producto: color, tipografía, espaciado, radios, elevación, movimiento                           | Esquema de datos, contratos de interfaz, máquinas de estado               |
| Biblioteca de componentes con sus ranuras obligatorias y estados                                          | Identidad de marca: isotipo, wordmark, lockup, tagline                    |
| Especificación de las superficies del MVP                                                                 | Formatos de exportación de marca y control de proveedores                 |
| Manual de redacción y textos aprobados                                                                    | Obligaciones legales no declaradas en L0, L2 o L3                         |
| Accesibilidad y verificación conductual estática                                                          | Estrategia comercial y de adquisición                                     |
| Especificación de activos digitales de producto                                                           | Arte maestro de marca                                                     |

**Regla de subordinación.** Este documento no crea reglas de negocio. Si una necesidad de experiencia exige una regla nueva, se eleva a L2 y se incorpora allí; L4 la implementa después. Un requisito funcional que apareciera por primera vez aquí sería un defecto de proceso.

**Regla de precedencia.** Ante conflicto: L0 sobre todo (R-01) · L2 sobre L4 en materia de reglas · L3 sobre L4 en materia técnica · **VIES sobre L4 en identidad de marca**.

## 0.3 Relación con VIES V3

VIES gobierna la **marca**; este documento gobierna el **producto**. Son ámbitos distintos y el propio VIES lo declara al decir que no es L4 y que no define pantallas transaccionales ni microcopy.

| Materia                                                                              | Fuente                  |
| ------------------------------------------------------------------------------------ | ----------------------- |
| Isotipo, wordmark, lockup, tagline, área segura, tamaños mínimos                     | **VIES V3**             |
| Colores de marca: LIBOX Purple, Trust Navy, Signal Violet, Success Green, Light Gray | **VIES V3**             |
| Tipografía del wordmark: Manrope ExtraBold en mayúsculas                             | **VIES V3**             |
| Activos de marca: favicon, icono de aplicación, avatares, iconos de notificación     | **VIES V3**             |
| **Colores de estado del producto** derivados y verificados para contraste            | **Este documento §2.2** |
| **Tipografía de interfaz** y su escala                                               | **Este documento §2.3** |
| Componentes, superficies, movimiento, textos                                         | **Este documento**      |

**Por qué la paleta de producto se deriva y no se copia.** VIES define seis colores de marca, suficientes para identidad y insuficientes para una interfaz transaccional. Faltan advertencia y error, y dos de los que existen no alcanzan el contraste mínimo para texto. La derivación de §2.2 resuelve ambas cosas **sin alterar un solo color de marca**.

## 0.4 Changelog

| Versión | Sección | Qué cambió                                                      | Por qué                                                                                                                                      |
| ------- | ------- | --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| V1      | —       | Primera emisión del nivel L4                                    | El nivel estaba declarado en LBPF V2 y L3 V2 sin documento; las superficies se diseñaban interpretando el rector                             |
| V1      | §2.2    | Paleta de producto derivada de VIES V2 con contraste verificado | Signal Violet rinde 4,23:1 y Success Green 2,54:1 sobre blanco: ninguno sirve como color de texto, y Success Green es el del estado *Pagado* |
| V1      | §2.2    | Incorporados advertencia, error, información y retenido         | VIES no los contempla; sin ellos los estados *Pendiente*, *Retenido* y *Revertido* no tienen color oficial                                   |
| V1      | §2.3    | Tipografía de interfaz declarada                                | VIES fija Manrope ExtraBold **para el wordmark**. Ese peso como base de interfaz sería ilegible                                              |
| V1      | §5.1    | Verified Opportunity Card con sus seis ranuras obligatorias     | Resuelve los incumplimientos de LINT-002 y de DP-01 de las piezas anteriores                                                                 |
| V1      | §7      | Manual de redacción y textos aprobados                          | El LBPF regula el copy exhaustivamente y no existía un solo texto aprobado                                                                   |
| V1      | §7.5    | Textos de cumplimiento sin revelar análisis                     | Aplicación literal de la excepción de reserva de LBPF V2 §0.3                                                                                |

# 1\. Del principio a la pantalla

## 1.1 Las dos zonas

LBPF V3 §6.1 divide toda superficie en dos zonas. **El límite lo define la intención, no la ubicación:** cualquier superficie que contenga un llamado a la acción de compra o que muestre un resultado es Zona de Decisión, aunque esté en la página de inicio.

|                      | **Zona de Atracción**                                      | **Zona de Decisión**                                                                                                  |
| -------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Superficies          | Inicio, catálogo, rankings, ganadores, contenido editorial | Detalle, compra, resultado de pago, prueba, mis tickets, sala, disputa, panel de gasto, liquidaciones, administración |
| Color rector         | LIBOX Purple                                               | Trust Navy                                                                                                            |
| Fondo                | `surface.attraction`                                       | `surface.canvas`                                                                                                      |
| Perfil de movimiento | `attraction`                                               | `calm`                                                                                                                |
| Elevación            | Suave, admite profundidad                                  | Funcional y mínima                                                                                                    |
| Imágenes             | Aspiracionales permitidas                                  | Solo funcionales: el bien, la evidencia, el documento                                                                 |

**Los dos colores de VIES mapean exactamente sobre las dos zonas.** LIBOX Purple para descubrir, Trust Navy para decidir. No es una interpretación libre: es la lectura que hace coherente la paleta de marca con la arquitectura conductual del rector.

## 1.2 Obligatorio y prohibido por zona

| \#    | En Zona de Decisión es obligatorio                                                                                     |
| ----- | ---------------------------------------------------------------------------------------------------------------------- |
| OB-01 | Costo total, probabilidad objetiva y tamaño del pool visibles **antes** del primer renderizado del llamado a la acción |
| OB-02 | Valor verificado del premio con fuente y fecha                                                                         |
| OB-03 | Plazo de reclamo, plazo de entrega, ruta ante no reclamo y costo estimado de recepción (BR-08)                         |
| OB-04 | Acceso a la evidencia en una sola interacción                                                                          |
| OB-05 | Paso de revisión que preserva los datos al retroceder, antes de todo compromiso irreversible                           |
| OB-06 | Llamado a la acción descriptivo: *Revisar y participar*                                                                |
| OB-07 | Aviso de independencia probabilística persistente y no descartable en la superficie de tickets                         |
| OB-08 | Criterio visible en todo ordenamiento o recomendación                                                                  |

| \#    | En Zona de Decisión está prohibido                                   |
| ----- | -------------------------------------------------------------------- |
| PR-01 | Animación de duración superior a 240 ms                              |
| PR-02 | Animación de repetición infinita                                     |
| PR-03 | Opción monetaria o de comunicación premarcada                        |
| PR-04 | Partículas, destellos, confeti, luces de premio                      |
| PR-05 | Regalos tridimensionales flotantes                                   |
| PR-06 | Sonido de premio                                                     |
| PR-07 | Animación de casi acierto                                            |
| PR-08 | Contador de demanda simulado                                         |
| PR-09 | Pulso de llamado a la acción de alta frecuencia                      |
| PR-10 | Claim absoluto: *garantizado*, *100 % seguro*, *tu premio te espera* |
| PR-11 | Cuenta atrás no ligada a un cierre real                              |
| PR-12 | Prueba social no proveniente de resultados reales                    |
| PR-13 | Costo revelado después de la compra                                  |
| PR-14 | Copy que culpa o avergüenza por no comprar                           |

**PR-01 a PR-03 y PR-15 bloquean la integración** (LBPF V3 §9.1). El resto se verifica en la lista de comprobación de §9.

**PR-15 merece una nota.** Es la traducción de interfaz de P13, y la tentación de vulnerarlo llegará disfrazada de buena idea comercial: *“a los suscriptores les damos una participación extra”*. Esa frase es exactamente lo que el rector prohíbe, y por eso la regla bloquea el merge en lugar de advertir.

**PR-17 tiene el fundamento inverso al resto.** Aquí la opacidad protege: la recaudación es información comercial del organizador y no es condición de la compra. Lo obligatorio y público sigue siendo precio, probabilidad, tamaño del pool y valor verificado del premio.

## 1.3 Lo que la Zona de Atracción sí permite

El rector restringe la zona de decisión, no el descubrimiento. En atracción están permitidos: imágenes aspiracionales del premio, profundidad y gradiente de marca, microinteracciones no coercitivas, transiciones de hasta 240 ms, ordenamientos destacados con su criterio visible, y **escasez auténtica**.

**La escasez de LIBOX es estructuralmente verificable:** pool finito con venta pública. *Quedan 23 de 1.000 tickets* es un hecho comprobable y comunicarlo es legítimo y deseable. Lo prohibido no es la urgencia: es fabricarla. LIBOX no necesita urgencia falsa porque dispone de urgencia real, que además resiste el escrutinio.

## 1.4 Metadatos obligatorios de componente

Todo componente de oportunidad o decisión declara, y sin ellos no pasa la verificación estática:

    behavioral_zone     attraction | decision
    decision_class      B0 | B1 | B2 | B3 | B4
    lbpf_patterns       ["DP-01","DP-03", …]
    probability_source  origen del dato de probabilidad
    evidence_source     origen del dato de evidencia
    motion_profile      attraction | calm
    tracking_events     eventos de decisión que emite

# 2\. Fundamentos visuales

## 2.1 Colores de marca — provienen de VIES V2, no se alteran

| Token          | Valor     | Uso                                                               |
| -------------- | --------- | ----------------------------------------------------------------- |
| `brand.purple` | `#6D28D9` | Color rector de Zona de Atracción, botón primario, isotipo        |
| `brand.navy`   | `#0B1020` | Color rector de Zona de Decisión, texto principal, fondos oscuros |
| `brand.violet` | `#8B5CF6` | Acento y gradiente. **Nunca como texto de tamaño normal**         |
| `brand.green`  | `#10B981` | Señal de confianza. **Nunca como texto**                          |
| `brand.gray`   | `#E5E7EB` | Bordes y líneas auxiliares                                        |
| `brand.white`  | `#FFFFFF` | Superficie y versión negativa                                     |

## 2.2 Paleta de producto — derivada y verificada

Contrastes medidos, no estimados. `AA` exige 4,5:1 en texto normal y 3:1 en texto de 18 pt o superior.

### Texto y superficie

| Token                | Valor     | Sobre  | Contraste   | Uso                                      |
| -------------------- | --------- | ------ | ----------- | ---------------------------------------- |
| `text.primary`       | `#0B1020` | blanco | **18,93:1** | Titulares y cifras                       |
| `text.secondary`     | `#3E4661` | blanco | **9,32:1**  | Texto de apoyo                           |
| `text.muted`         | `#667085` | blanco | **4,97:1**  | Metadatos, organizador, marcas de tiempo |
| `text.onDark`        | `#FFFFFF` | navy   | **18,93:1** | Texto sobre fondo profundo               |
| `surface.canvas`     | `#F7F8FA` | —      | —           | Fondo de Zona de Decisión                |
| `surface.attraction` | `#F6F1FE` | —      | —           | Fondo de Zona de Atracción               |
| `surface.card`       | `#FFFFFF` | —      | —           | Tarjetas y paneles                       |
| `surface.border`     | `#E5E7EB` | —      | —           | Bordes y divisores                       |

`text.muted` **se elevó de** `#8B82A3` **a** `#667085`**.** El valor anterior rendía 3,10:1 y no pasaba AA. Es la clase que llevan el nombre del organizador y las marcas de tiempo: el dato menos importante seguía siendo dato.

### Estados

Cada estado tiene color de texto verificado sobre blanco y par de fondo con texto verificado encima.

| Estado    | `.text`   | s/blanco   | `.bg`     | texto s/fondo | Aplica a                                 |
| --------- | --------- | ---------- | --------- | ------------- | ---------------------------------------- |
| `success` | `#047857` | **5,48:1** | `#D1FAE5` | **4,84:1**    | Pagado · Entregado · Verificado          |
| `warning` | `#B45309` | **5,02:1** | `#FEF3C7` | **4,51:1**    | Pendiente · Por vencer · Requiere acción |
| `danger`  | `#B91C1C` | **6,47:1** | `#FEE2E2` | **5,30:1**    | Revertido · Rechazado · Disputa          |
| `info`    | `#1D4ED8` | **6,70:1** | `#DBEAFE` | **5,49:1**    | Informativo · En proceso                 |
| `held`    | `#3E4661` | **9,32:1** | `#E9ECF3` | **7,88:1**    | **Retenido**                             |
| `brand`   | `#5B21B6` | 7,57:1     | `#EDE9FE` | **7,57:1**    | Destacado · En curso                     |

**Por qué** `success.text` **no es el verde de VIES.** Success Green `#10B981` rinde **2,54:1** sobre blanco: falla incluso para texto de 18 pt. Y es precisamente el color del chip *Pagado* del panel de liquidaciones. El verde de marca conserva su uso como **relleno con texto oscuro encima o sobre fondo navy**, donde rinde 7,46:1. Como color de texto sobre claro se usa `#047857`.

**Signal Violet** `#8B5CF6` rinde 4,23:1: apto para texto de 18 pt o superior, gradientes y elementos decorativos. **Prohibido en texto de cuerpo.**

**Por qué existe** `held`**.** El PRD introdujo el estado *Retenido* en liquidaciones —ventana de contracargo cumpliéndose— y VIES no tiene color para él. Deliberadamente es neutro y no ámbar: retenido no es un problema del organizador ni una falta suya, es un plazo corriendo. Colorearlo de advertencia comunicaría culpa donde no la hay.

### Acentos

| Token         | Valor     | Contraste | Nota                                                                 |
| ------------- | --------- | --------- | -------------------------------------------------------------------- |
| `accent.rank` | `#A16207` | 4,92:1    | Distintivo de ranking. El dorado `#B8860B` rinde 3,25:1 y no pasa AA |
| `accent.live` | `#047857` | 5,48:1    | Indicador de transmisión en vivo                                     |
| `partner.mp`  | `#00B1EA` | —         | Solo como logotipo de aliado, nunca como texto                       |

### Gradientes

| Token            | Valor                                       | Zona                       |
| ---------------- | ------------------------------------------- | -------------------------- |
| `gradient.brand` | `linear-gradient(135deg, #6D28D9, #8B5CF6)` | Atracción                  |
| `gradient.hero`  | `linear-gradient(135deg, #4C1D95, #6D28D9)` | Atracción                  |
| `gradient.trust` | `linear-gradient(180deg, #0B1020, #1E2947)` | Decisión, fondos profundos |

**Regla de legibilidad sobre gradiente.** Todo texto sobre gradiente exige una capa sólida `rgba(11,16,32,0.35)` detrás. El gradiente por sí solo no garantiza contraste, y el punto de menor contraste de una superficie con degradado no es evidente a simple vista.

## 2.3 Tipografía de interfaz

**Familia:** Manrope, con `system-ui` y `sans-serif` como reserva. Se elige por coherencia con el wordmark de VIES, no por herencia: **Manrope ExtraBold es el peso del wordmark y no se usa en interfaz**, donde resultaría ilegible en párrafo y agresivo en titular.

| Peso          | Valor   | Uso                                               |
| ------------- | ------- | ------------------------------------------------- |
| Regular       | 400     | Texto de cuerpo                                   |
| Medium        | 500     | Énfasis suave, etiquetas                          |
| SemiBold      | 600     | Subtítulos, encabezados de tabla                  |
| Bold          | 700     | Titulares, cifras monetarias                      |
| **ExtraBold** | **800** | **Exclusivo del wordmark. Prohibido en interfaz** |

### Escala, móvil primero

| Token         | Móvil       | Escritorio  | Peso    | Uso                       |
| ------------- | ----------- | ----------- | ------- | ------------------------- |
| `display`     | 28 / 34     | 40 / 46     | 700     | Titular de portada        |
| `h1`          | 24 / 30     | 32 / 38     | 700     | Título de superficie      |
| `h2`          | 20 / 26     | 24 / 30     | 600     | Sección                   |
| `h3`          | 17 / 23     | 18 / 24     | 600     | Título de tarjeta         |
| `body`        | 16 / 24     | 15 / 23     | 400     | Cuerpo                    |
| `bodyStrong`  | 16 / 24     | 15 / 23     | 600     | Cuerpo con énfasis        |
| `caption`     | 14 / 20     | 13 / 18     | 400     | Metadatos                 |
| `micro`       | 12 / 16     | 11 / 15     | 600     | Chips y etiquetas         |
| `money`       | 24 / 30     | 28 / 32     | 700     | Importes                  |
| `probability` | **16 / 24** | **15 / 23** | **700** | **Probabilidad objetiva** |

**El cuerpo es mayor en móvil que en escritorio.** No es un error: es la lectura a distancia corta con luz variable y en movimiento. Reducir por debajo de 16 px en móvil está prohibido en Zona de Decisión.

`probability` **iguala el peso de** `money` **y ocupa el mismo bloque visual.** DP-03 exige emparejamiento de costo y probabilidad; si el precio va en 700 y la probabilidad en caption, el emparejamiento se incumple aunque ambos datos estén presentes.

**Cifras:** `font-variant-numeric: tabular-nums` obligatorio en importes, contadores, cuentas atrás y números de ticket. Sin ello las cifras bailan al actualizarse.

## 2.4 Espaciado, forma y elevación

**Espaciado.** Unidad de 4 px. Escala: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80.

**Radios:** `sm` 8 · `md` 12 · `lg` 16 · `xl` 20 · `pill` 999.

**Elevación**, siempre tintada en `brand.navy` y nunca en negro puro:

| Token             | Valor                           | Zona                           |
| ----------------- | ------------------------------- | ------------------------------ |
| `shadow.card`     | `0 1px 3px rgba(11,16,32,.08)`  | Ambas                          |
| `shadow.hover`    | `0 4px 12px rgba(11,16,32,.12)` | Atracción                      |
| `shadow.raised`   | `0 8px 24px rgba(11,16,32,.16)` | Atracción                      |
| `shadow.decision` | `0 1px 2px rgba(11,16,32,.10)`  | **Decisión, máximo permitido** |

En Zona de Decisión la elevación es funcional y mínima. Sin resplandor, sin sombras de color saturado, sin elevación creciente al acercar el puntero.

## 2.5 Rejilla y puntos de corte

**Móvil primero, sin excepción.** Las superficies se componen desde 360 px y se expanden. Componer en escritorio y reducir produce la degradación que ya se observó en la línea anterior, cuyas piezas estaban compuestas a 1200 px.

| Corte | Desde | Columnas | Margen             | Canal |
| ----- | ----- | -------- | ------------------ | ----- |
| `xs`  | 360   | 4        | 16                 | 12    |
| `sm`  | 640   | 8        | 24                 | 16    |
| `md`  | 768   | 8        | 24                 | 20    |
| `lg`  | 1024  | 12       | 32                 | 24    |
| `xl`  | 1280  | 12       | máx. 1200 centrado | 24    |

**Regla de tolerancia de longitud.** Ningún componente se compone sobre la longitud del texto de un mercado. Una etiqueta de tres caracteres puede tener veinte en el siguiente. Todo componente se prueba con texto al 150 % de su longitud de referencia y con la palabra más larga del catálogo de errores.

**Áreas táctiles:** mínimo 44×44 px, con 8 px de separación entre objetivos adyacentes. Ninguna función depende de estados de puntero. El teclado virtual nunca oculta el campo activo.

# 3\. Movimiento

## 3.1 Perfiles

| Interacción              | `attraction`                                                   | `calm`               |
| ------------------------ | -------------------------------------------------------------- | -------------------- |
| Realce al acercar        | 160 ms                                                         | 120 ms               |
| Cambio de estado         | 220 ms                                                         | 160 ms               |
| Transición de superficie | 240 ms                                                         | 180 ms               |
| Confirmación de éxito    | 240 ms                                                         | 180 ms, una sola vez |
| Repetición               | Permitida si es pausable y no representa evidencia inexistente | **Prohibida**        |

**Curvas:** entrada `cubic-bezier(0,0,0,1)` · estándar `cubic-bezier(0.2,0,0,1)` · salida `cubic-bezier(0.4,0,1,1)`.

## 3.2 Límites duros en Zona de Decisión

Verificados en integración continua. **Bloquean el merge.**

| Límite              | Valor     | Regla    |
| ------------------- | --------- | -------- |
| Duración máxima     | 240 ms    | LINT-003 |
| Repetición infinita | prohibida | LINT-004 |
| Opción premarcada   | prohibida | LINT-005 |

## 3.3 Revelación del resultado

Es el momento de mayor tentación de todo el producto y por eso tiene norma propia.

| Fase       | Duración     | Contenido                                                            |
| ---------- | ------------ | -------------------------------------------------------------------- |
| Entrada    | 200 ms       | Aparece el panel del resultado                                       |
| Revelación | 400 ms       | Se muestra el número ganador, sin aceleración ni suspenso artificial |
| Reposo     | 200 ms       | Estado final estable                                                 |
| **Total**  | **≤ 800 ms** |                                                                      |

Prohibido sin excepción: casi acierto, números girando, confeti, sonido, repetición, y cualquier variación de la secuencia según si el usuario ganó o no. **La secuencia es idéntica para quien gana y para quien pierde.** Un tratamiento distinto convierte la pérdida en castigo y la victoria en refuerzo, que es exactamente la mecánica que el rector prohíbe.

El enlace a la prueba pública está presente en el mismo cuadro que el resultado, no tras una transición.

## 3.4 Esqueletos de carga

Pulso de opacidad de 0,6 a 1,0 en 1.200 ms, **permitido solo mientras hay una petición en curso**. Al resolverse, cesa. Un esqueleto que sigue latiendo sin petición viva es una repetición infinita en zona de decisión.

## 3.5 Movimiento reducido

Ante `prefers-reduced-motion: reduce`: se suprime toda transición no funcional, el punto de transmisión en vivo deja de pulsar, los esqueletos pasan a estado sólido, y la revelación del resultado se muestra de forma directa. **La información nunca depende del movimiento.**

# 4\. Accesibilidad

**Objetivo: WCAG 2.1 AA.** No es aspiración: es criterio de liberación.

| \#    | Requisito                                                                           |
| ----- | ----------------------------------------------------------------------------------- |
| AC-01 | Texto normal 4,5:1 · texto de 18 pt o superior 3:1 · elementos de interfaz 3:1      |
| AC-02 | Foco visible de 2 px en `brand.purple` con 2 px de separación, nunca suprimido      |
| AC-03 | Orden de tabulación coincidente con el orden visual                                 |
| AC-04 | Toda función alcanzable por teclado                                                 |
| AC-05 | Áreas táctiles de 44×44 px con 8 px de separación                                   |
| AC-06 | El color nunca es el único portador de significado: todo estado lleva texto o icono |
| AC-07 | Toda imagen informativa con texto alternativo; las decorativas se ocultan al lector |
| AC-08 | Formularios con etiqueta asociada; el error se anuncia y se vincula al campo        |
| AC-09 | Un solo `h1` por superficie, jerarquía sin saltos                                   |
| AC-10 | Cambios dinámicos anunciados por región activa                                      |
| AC-11 | Ningún contenido depende exclusivamente de la orientación del dispositivo           |
| AC-12 | Zoom hasta 200 % sin pérdida de contenido ni desplazamiento horizontal              |

**AC-06 importa especialmente aquí.** Los chips de liquidación se distinguen por color; un usuario con deficiencia de percepción cromática necesita leer *Pagado*, *Pendiente* o *Retenido*. El color acompaña, nunca sustituye.

# 5\. Biblioteca de componentes

Cada ficha declara: propósito, zona, ranuras obligatorias, estados, movimiento y reglas de verificación. Los aspectos comunes —estados de carga, vacío, error y restringido, tolerancia de longitud, área táctil y foco— se declaran una vez en §8 y no se repiten por componente.

## 5.1 VerifiedOpportunityCard

**Zona:** atracción en catálogo, **decisión** en detalle. **Sustituye a:** la tarjeta de sorteo de la línea anterior, que incumplía DP-01, DP-03, AP-10 y LINT-002.

### Las seis ranuras obligatorias

| Ranura             | Contenido                                                                                                                                      | Obligatoria            |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| **A · Encabezado** | Premio, categoría, organizador con su nivel de reputación, sello de verificación. **Sin claim absoluto**                                       | Sí                     |
| **B · Valor**      | Precio total del ticket **y valor verificado del premio con fuente y fecha**                                                                   | Sí                     |
| **C · Decisión**   | **Probabilidad objetiva y tamaño del pool**                                                                                                    | Sí — LINT-002 la exige |
| **D · Reglas**     | Cierre, tipo, elegibilidad, **plazo de reclamo y de entrega, ruta ante no reclamo, costo estimado de recepción**. Accesible en ≤ 1 interacción | Sí — BR-08             |
| **E · Evidencia**  | Política de prueba e historial auténtico. **No decorativa**                                                                                    | Sí                     |
| **F · Acción**     | Llamado descriptivo y no coercitivo                                                                                                            | Sí                     |

**Un componente al que le falte C, D o E no compila.** No es una advertencia de diseño: es una regla de verificación estática.

### Formato de la probabilidad

DP-02 exige presentación triple. En una sola línea, con peso `probability`:

    1 de 1.000  ·  0,10 %  ·  1 por cada 1.000 tickets

Las tres expresan lo mismo. Están las tres porque la comprensión de probabilidad varía mucho entre personas, y P3 la mide.

### Composición en móvil

    ┌──────────────────────────────┐
    │  imagen del premio           │
    │  [chip verificado]           │
    ├──────────────────────────────┤
    │  A · Premio                  │  h3
    │     Organizador · N2  ✓      │  caption + text.muted
    ├──────────────────────────────┤
    │  B · S/ 5,00 por ticket      │  money
    │     Premio S/ 4.500 verif.   │  caption
    │     Ref. mercado · 02 ago    │  micro + text.muted
    ├──────────────────────────────┤
    │  C · 1 de 1.000 · 0,10 %     │  probability  ← mismo bloque que B
    │     ▓▓▓▓▓▓░░░░  750/1.000    │  progreso
    ├──────────────────────────────┤
    │  D · Cierra 12 ago · 20 días │  caption
    │     Envío desde S/ 15  ⌄     │  caption, expande
    ├──────────────────────────────┤
    │  E · Ver evidencia  ⌄        │  caption, expande sin navegar
    ├──────────────────────────────┤
    │  F · [ Revisar y participar ]│  botón primario
    └──────────────────────────────┘

**B y C ocupan bloques adyacentes con el mismo peso tipográfico.** Es la aplicación literal de DP-03: si el costo va destacado y la probabilidad al pie, hay emparejamiento nominal y no real.

### Prohibiciones específicas

Cuenta atrás que se acelere cerca del cierre · barra de progreso animada en bucle · contador de personas viéndolo · *quedan pocos* sin cifra real · llamado a la acción que pulse · imagen de premio con destellos superpuestos.

### Textos del llamado a la acción

| Permitido                  | Prohibido              |
| -------------------------- | ---------------------- |
| Revisar y participar       | ¡Gana ya\!             |
| Ver oportunidad            | ¡No te lo pierdas\!    |
| Participar                 | ¡Últimos tickets\!     |
| Ver detalle y probabilidad | ¡Tu premio te espera\! |

## 5.2 ProbabilityBlock

**Zona:** decisión. Componente independiente porque aparece en tarjeta, detalle, compra y tickets, y **debe ser idéntico en las cuatro**.

Ranuras: expresión triple · denominador con tickets vendidos y total · **nota de independencia** cuando el usuario ya posee tickets del sorteo.

Estados: `pool_open` con denominador vivo · `pool_frozen` con denominador definitivo · `insufficient_data` cuando aún no hay ventas.

**Regla:** al actualizarse el denominador, **transición de 160 ms sin animación de conteo**. Un número que sube contando dramatiza la venta y es urgencia fabricada.

## 5.3 PoolProgress

Altura 8 px, radio de píldora. Vía `#DDD3F7`, relleno `brand.purple`. Sobre fondo profundo: vía blanca al 22 %, relleno blanco.

**Siempre acompañada de la cifra literal** `750 / 1.000`. La barra sola no es información: es sensación.

Prohibido: animación en bucle · aceleración cerca del 100 % · cambio de color al acercarse al final · pulso.

## 5.4 CountdownChip

Fondo `surface.card`, borde `surface.border`, texto `text.secondary`, radio de píldora.

| \#    | Requisito                                                                                                  |
| ----- | ---------------------------------------------------------------------------------------------------------- |
| CD-01 | Ligado a `end_at` real. Sin plazo verdadero **no existe el componente**                                    |
| CD-02 | **Sincronizado con hora de servidor.** Un reloj de cliente adelantado mostraría 00:00 en un sorteo abierto |
| CD-03 | En Zona de Decisión: sin pulso, sin cambio de color por proximidad, sin cambio de tamaño                   |
| CD-04 | Por debajo de una hora muestra minutos; por encima, días y horas. Sin décimas de segundo                   |

CD-04 evita el efecto casino del contador de milisegundos, que no aporta información y sí presión.

## 5.5 StatusChip

| Estado       | Texto        | Color         | Icono          |
| ------------ | ------------ | ------------- | -------------- |
| Pagado       | Pagado       | `success`     | comprobación   |
| Pendiente    | Pendiente    | `warning`     | reloj          |
| **Retenido** | **Retenido** | `held`        | **candado**    |
| Revertido    | Revertido    | `danger`      | flecha inversa |
| En proceso   | En proceso   | `info`        | círculo        |
| En vivo      | EN VIVO      | `accent.live` | punto          |

**El chip *Retenido* siempre acompaña motivo y fecha estimada.** Un estado retenido sin explicación se interpreta como retención indebida, y ese malentendido con el organizador es evitable escribiendo dos líneas.

El punto de *EN VIVO* pulsa a 2.000 ms **solo en Zona de Atracción** y se detiene con movimiento reducido.

## 5.6 RankBadge

34 px, esquina superior izquierda con desplazamiento de −6 px. Fondo `accent.rank`, texto blanco.

**Exige metadata de razón visible en una interacción** (DP-12, LINT-006): *por cierre próximo*, *organizador con 47 sorteos completados*, *nuevo en LIBOX · verificado*, *destacado*. Sin razón, el componente no pasa la verificación.

Los destaques por contraprestación llevan etiqueta **Destacado** visible y se presentan **separados del ordenamiento orgánico**.

## 5.7 TicketQuantitySelector

**Zona:** decisión.

| \#    | Regla                                                                                  |
| ----- | -------------------------------------------------------------------------------------- |
| TQ-01 | **Valor inicial 1.** Ninguna cantidad mayor viene preseleccionada — LINT-005           |
| TQ-02 | Muestra el total en vivo y **recalcula la probabilidad** al cambiar la cantidad        |
| TQ-03 | Si el importe no alcanza el mínimo de mercado, lo indica con la cifra exacta que falta |
| TQ-04 | Al aproximarse al tope de concentración, avisa. Al alcanzarlo, bloquea con explicación |
| TQ-05 | Sin paquetes preseleccionados ni destacados como *más popular*                         |

**TQ-04 sin revelar el tope de otros.** El mensaje es *has alcanzado el máximo de tickets por participante en este sorteo*, sin exponer distribución de tenencia (R-10).

## 5.8 CheckoutSummary

Ranuras: sorteo con enlace de vuelta · cantidad y precio unitario · **probabilidad resultante** · saldo de reembolso aplicable, no preseleccionado · total a pagar · costo estimado de recepción · plazos · **paso de revisión con retroceso que preserva datos** (OB-05) · aceptación de bases con enlace.

| \#    | Regla                                                        |
| ----- | ------------------------------------------------------------ |
| CS-01 | El retroceso **nunca pierde los datos introducidos**         |
| CS-02 | El total es la cifra de mayor peso, sin cargos posteriores   |
| CS-03 | El saldo de reembolso se ofrece, jamás se aplica por defecto |
| CS-04 | Sin cuenta atrás de sesión que presione                      |
| CS-05 | La probabilidad sigue visible en la superficie de pago       |

**CS-05 es deliberado.** Es tentador retirar la probabilidad en el último paso para no enfriar la conversión. Retirarla es exactamente lo que P1 mide y lo que R-03 prohíbe.

## 5.9 PaymentStatus

Estados: `processing` · `confirmed` · `failed` · `expired` · `unknown`.

`unknown` **es el estado más importante y el que suele faltar.** Cuando se pierde la conexión a mitad del pago, el usuario no debe ver un error ni un éxito: debe ver *estamos confirmando tu pago*, con recuperación automática de estado y sin permitir un segundo intento que duplicaría el cargo. La ambigüedad en este punto es de las principales causas de contracargo.

Al confirmarse: transición de 180 ms, una sola vez, con los números de ticket asignados. **Sin confeti, sin sonido, sin celebración** — comprar un ticket no es ganar.

## 5.10 ProofViewer

**Zona:** decisión. Superficie pública sin autenticación.

| Ranura       | Contenido                                                                             |
| ------------ | ------------------------------------------------------------------------------------- |
| Resultado    | Número ganador y posición                                                             |
| Pool         | Tamaño, hash, enlace a la instantánea completa                                        |
| Compromiso   | Valor y **momento de publicación**                                                    |
| Baliza       | Fuente, **propiedad intrínseca de la ronda**, valor, y **enlace a la fuente pública** |
| Revelación   | Semilla revelada                                                                      |
| Derivación   | Material de semilla y fórmula                                                         |
| Verificación | Los cuatro pasos en lenguaje llano                                                    |
| Cadena       | Si hubo re-sorteo, la cadena completa con su motivo                                   |

**Regla de honestidad de la interfaz.** El visor indica explícitamente **qué debe comprobarse fuera de LIBOX**: la ronda de baliza y su valor se consultan en la fuente pública, cuyo enlace es visible y sale del dominio. Un visor que solo consultara a LIBOX confirmaría la aritmética de la parte cuya honestidad se pretende comprobar.

**Nunca muestra** identidad de participantes ni distribución de tenencia (R-10). Muestra números de ticket.

Los datos técnicos se presentan con explicación en lenguaje llano y el detalle criptográfico plegado. Un usuario no debe necesitar entender SHA-256 para confiar; debe poder llegar a él si quiere.

## 5.11 EvidenceDrawer

**Se abre en la misma superficie, sin navegación de página** — es lo que mide P5. Un cajón que navega a otra página no cumple *evidencia a la mano*.

Contenido: valor verificado con fuente y fecha · documentos de valoración disponibles · historial del organizador · política de prueba del sorteo · enlace a la prueba pública si ya se ejecutó.

Movimiento: 180 ms de despliegue, perfil calma.

## 5.12 ResolutionRoom

**Zona:** decisión. Es la superficie con mayor carga probatoria del producto.

| Ranura     | Contenido                                                           |
| ---------- | ------------------------------------------------------------------- |
| Encabezado | Código del sorteo, premio, estado, **plazo restante con su motivo** |
| Partes     | Ganador, organizador y agente asignado, **con datos minimizados**   |
| Cronología | Mensajes en orden, sin edición ni borrado posibles                  |
| Evidencia  | Adjuntos con su tipo y fuerza probatoria                            |
| Acciones   | Según rol y estado                                                  |
| Aviso      | Recordatorio de que la coordinación ocurre dentro de la sala        |

| \#    | Regla                                                                                                                   |
| ----- | ----------------------------------------------------------------------------------------------------------------------- |
| RR-01 | **La interfaz no ofrece editar ni eliminar.** Retractarse se hace publicando una corrección, visible como tal           |
| RR-02 | Datos de contraparte minimizados: nombre e inicial. Nunca documento, correo ni teléfono                                 |
| RR-03 | Al detectarse datos de contacto externos o mención de pago entre partes, **el envío se bloquea con explicación neutra** |
| RR-04 | Las notas internas son visualmente inequívocas y jamás se mezclan con los mensajes de las partes                        |
| RR-05 | El plazo se muestra siempre con su motivo y su fecha, nunca como cuenta atrás sola                                      |

**RR-03 se redacta sin acusar.** El mensaje es *por seguridad de ambas partes, la coordinación se realiza dentro de la sala*, no *hemos detectado un intento de contacto externo*. La primera protege; la segunda acusa a quien puede estar actuando de buena fe.

## 5.13 DisputeForm

| \#    | Regla                                                                                                                                                                        |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DF-01 | **Motivo de lista cerrada.** No llegó · llegó dañado · no corresponde a lo publicado · incompleto · artículo equivocado · servicio no prestado · transferencia no completada |
| DF-02 | **Evidencia obligatoria.** Sin adjunto no se abre reclamo                                                                                                                    |
| DF-03 | Antes de enviar, muestra qué ocurre después y en qué plazo                                                                                                                   |
| DF-04 | Lenguaje no adversarial: *reclamo*, no *denuncia*                                                                                                                            |
| DF-05 | Indica que la resolución se basa en evidencia, no en la palabra de ninguna parte                                                                                             |

**DF-05 es prevención, no formalismo.** Comunicar de antemano que la decisión será por evidencia desactiva el reclamo como palanca de presión antes de que se presente.

## 5.14 SettlementTable

Columnas: sorteo · recaudado · comisión · **neto** · estado · fecha estimada · acción.

| \#    | Regla                                                                            |
| ----- | -------------------------------------------------------------------------------- |
| ST-01 | El estado *Retenido* siempre con motivo y fecha estimada                         |
| ST-02 | Los seis gates consultables en una interacción, con cuál falta                   |
| ST-03 | El desglose de comisión visible sin cargos posteriores                           |
| ST-04 | Antes de publicar, el organizador ve el **plazo máximo estimado hasta el cobro** |

**ST-04 evita el conflicto más frecuente con el organizador.** Quien desconoce que su cobro puede demorar meses interpreta la espera como retención indebida. Decirlo antes cuesta una línea.

## 5.15 StageChecklist

Para el flujo mecánico de bienes registrables.

| \#    | Regla                                                                                   |
| ----- | --------------------------------------------------------------------------------------- |
| SC-01 | Cada documento es un elemento tipificado con su estado. **No existe campo *otros***     |
| SC-02 | Sin avance parcial: la etapa siguiente aparece bloqueada con su motivo                  |
| SC-03 | La aprobación es una casilla, no una opinión. **No existe *aprobar con observaciones*** |
| SC-04 | El motivo obligatorio muestra los caracteres restantes                                  |
| SC-05 | Toda verificación externa indica **contra qué fuente** se hizo y cuándo                 |

## 5.16 SpendPanel

| \#    | Regla                                                                                                               |
| ----- | ------------------------------------------------------------------------------------------------------------------- |
| SP-01 | **Neutro y no culpabilizante.** Se informa la cifra, no se juzga la conducta                                        |
| SP-02 | **No se muestra durante la compra.** Situarlo ahí lo convierte en fricción en zona de decisión, contra su propósito |
| SP-03 | Muestra periodo y acumulado, con el saldo de reembolso computado                                                    |
| SP-04 | El acceso a límites y autoexclusión está siempre a una interacción                                                  |

| Permitido                           | Prohibido                                |
| ----------------------------------- | ---------------------------------------- |
| Has participado con S/ 240 este mes | Cuidado, estás gastando mucho            |
| Configura un límite si quieres      | ¿No crees que deberías parar?            |
| Tu límite mensual: S/ 300           | Ya casi alcanzas tu límite, ¡aprovecha\! |

## 5.17 LimitsAndSelfExclusion

| \#    | Regla                                                                                                      |
| ----- | ---------------------------------------------------------------------------------------------------------- |
| LS-01 | Reducir un límite aplica **de inmediato**; aumentarlo muestra la espera de 24 horas **antes** de confirmar |
| LS-02 | La autoexclusión **no tiene fricción, ni retención comercial, ni oferta de disuasión**                     |
| LS-03 | Antes de confirmar, explica con precisión qué se bloquea y qué sigue disponible                            |
| LS-04 | **Deja claro que es irreversible durante el plazo elegido**                                                |
| LS-05 | Sin llamado a la acción alternativo en la superficie de autoexclusión                                      |

**LS-05 es explícito porque la tentación es evidente.** Un *¿seguro? mira estos sorteos antes de irte* es AP-04, y en esta superficie es además una falta grave: el usuario está ejerciendo una protección, no navegando.

## 5.20 FreeEntryBlock

**Zona:** decisión. Aparece en toda oportunidad con entrada gratuita.

| Ranura               | Contenido                                                                                  | Obligatoria |
| -------------------- | ------------------------------------------------------------------------------------------ | ----------- |
| **A · Vía**          | Cómo participar sin pagar, con el mismo peso que la vía pagada                             | Sí — OB-09  |
| **B · Probabilidad** | **Idéntica para ambas vías**, en un solo bloque                                            | Sí — OB-10  |
| **C · Cupo**         | Plazas usadas y totales, en cifra literal                                                  | Sí          |
| **D · Requisitos**   | Correo y teléfono. **La verificación de identidad se exige al reclamar**, no al participar | Sí          |
| **E · Acción**       | *Participar sin costo*                                                                     | Sí          |

| \#    | Regla                                                                                                |
| ----- | ---------------------------------------------------------------------------------------------------- |
| FE-01 | **Una sola presentación de probabilidad.** Mostrarla dos veces sugeriría que difieren, y no difieren |
| FE-02 | El cupo se muestra como cifra literal —*340 de 1.000 disponibles*—, **nunca como barra sola**        |
| FE-03 | **Sin cuenta atrás** sobre el cupo. La escasez es real y no necesita dramatizarse                    |
| FE-04 | Agotado el cupo, el mensaje es informativo: *se agotaron las 1.000 plazas de esta campaña*           |
| FE-05 | **Prohibido cualquier elemento que sugiera que comprar mejora las opciones** (PR-15)                 |

**FE-03 es la regla que más se va a discutir.** Un cupo agotándose es urgencia legítima, y aun así **el contador regresivo está prohibido**: la cifra informa, el reloj presiona. La diferencia es exactamente la que separa escasez auténtica de urgencia fabricada.

## 5.21 CampaignCodeInput

**Zona:** decisión. Es donde se canjea el código de campaña.

Ranuras: campo de código · estado de la campaña con plazas restantes · resultado del canje · **enlace a las bases de la oportunidad**.

| \#    | Regla                                                                                                                                                          |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CC-01 | El estado se consulta **antes** de que el usuario introduzca datos personales. Pedir el registro y después decir que el cupo se agotó es una fricción evitable |
| CC-02 | Código inválido y campaña agotada son **mensajes distintos**. Confundirlos deja al usuario sin saber si reintentar                                             |
| CC-03 | Un código ya usado por esa persona informa: *ya participas en esta oportunidad*                                                                                |
| CC-04 | **Sin sugerir que introducir el código varias veces aumente las opciones**                                                                                     |

## 5.22 OrganizerBrandBar

**Zona:** ambas. Implementa la marca compartida.

> **La oportunidad es del organizador y se ve suya. LIBOX es visible como garante.**

| Ranura                    | Contenido                                          |
| ------------------------- | -------------------------------------------------- |
| Identidad del organizador | Nombre, logotipo si lo aportó, nivel de reputación |
| **Sello de LIBOX**        | Verificación, prueba pública y retención de fondos |
| Enlace                    | Al perfil público del organizador                  |

| \#    | Regla                                                                                                |
| ----- | ---------------------------------------------------------------------------------------------------- |
| OB-01 | La identidad del organizador es la dominante; **el sello de LIBOX es secundario y siempre presente** |
| OB-02 | El sello **no compite** con costo, probabilidad, pool ni evidencia en zona de decisión               |
| OB-03 | El enlace al perfil no interrumpe el flujo de compra: abre el directorio, no lo reemplaza            |

**Fundamento.** Si la superficie llevara solo la marca del organizador, el visitante nunca sabría que existe un catálogo y **el descubrimiento cruzado no arrancaría**. Si llevara solo la de LIBOX, el organizador sentiría que se le quita la relación con su cliente. La proporción resuelve las dos cosas.

## 5.18 AlarmCard

Ranuras: tipo y familia · severidad · entidad afectada · identificador de traza · **dueño nominal** · plazo · estado · acciones.

| \#    | Regla                                                                              |
| ----- | ---------------------------------------------------------------------------------- |
| AL-01 | El dueño es **una persona con nombre**, nunca un equipo                            |
| AL-02 | El plazo se muestra en positivo — *vence en 18 h* — y en negativo cuando ya venció |
| AL-03 | **Resolver exige motivo, también cuando la conclusión es que no hay problema**     |
| AL-04 | La severidad se distingue por color **y por etiqueta**                             |

## 5.19 AdminDecisionModal

Para aprobaciones de valoración, etapas, liquidaciones y adjudicaciones.

| \#    | Regla                                                                                  |
| ----- | -------------------------------------------------------------------------------------- |
| AD-01 | Muestra **qué se está decidiendo y qué consecuencia tiene**, con importe cuando aplica |
| AD-02 | Motivo obligatorio con mínimo de caracteres visible                                    |
| AD-03 | Si exige segunda firma, lo indica **antes** de la decisión, no después                 |
| AD-04 | Ninguna acción destructiva o irreversible tiene foco inicial                           |
| AD-05 | Sin opción preseleccionada                                                             |

**AD-04 evita el error por costumbre.** Un operador que aprueba cincuenta expedientes al día pulsa la tecla de confirmación por hábito. Que el foco inicial no esté en la acción irreversible es de las medidas más baratas de todo el sistema.

# 6\. Superficies

## 6.1 Cómo leer esta sección

El PRD MVP V9 §27 declara **qué** hace cada superficie. Aquí se declara **cómo se compone**. Solo se detallan las que tienen composición no evidente o carga conductual alta; el resto se resuelve por aplicación directa de la biblioteca de §5.

## 6.2 PU-03 · Detalle de oportunidad

**La superficie más importante del producto.** Es donde se decide, donde P1 se mide y donde fracasó la línea anterior.

### Orden en móvil, de arriba abajo

    1  Imagen del premio · sello de verificación
    2  Título · organizador con su nivel
    3  BLOQUE DE DECISIÓN  ← precio, probabilidad, pool, juntos
    4  Barra de progreso con cifra literal
    5  Valor verificado del premio con fuente y fecha
    6  Cierre y plazos
    7  Costo estimado de recepción por macrozona
    8  Ruta ante no reclamo
    9  Evidencia (cajón)
    10 Bases (una interacción)
    11 [ Revisar y participar ]     ← nunca antes del punto 3
    12 Organizador: historial y reputación
    13 Cómo funciona el sorteo · enlace a verificación

| \#      | Regla                                                                                                                                                                                                                               |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PU03-01 | **El llamado a la acción no se renderiza antes que el bloque de decisión.** No basta con que esté presente en el árbol: debe haber sido visible en pantalla. Es lo que mide P1 y se instrumenta por observación de visibilidad real |
| PU03-02 | En escritorio, el bloque de decisión va en columna lateral fija, **siempre visible al desplazar**                                                                                                                                   |
| PU03-03 | La imagen del premio no lleva superposiciones decorativas                                                                                                                                                                           |
| PU03-04 | Cero animación superior a 240 ms y cero repetición infinita                                                                                                                                                                         |
| PU03-05 | Los plazos se muestran en días, no solo como fecha: *hasta 20 días para la entrega*                                                                                                                                                 |
| PU03-06 | El costo de recepción aparece **antes** del llamado a la acción, nunca después de comprar                                                                                                                                           |

**PU03-01 es la regla más importante del documento.** Es la traducción literal de *confianza antes que conversión*, y es la única que se verifica con telemetría de visibilidad real en lugar de con inspección de código.

## 6.3 US-01 · Compra

    1  Resumen del sorteo, con vuelta al detalle
    2  Cantidad  ← inicia en 1
    3  PROBABILIDAD RESULTANTE  ← se recalcula en vivo
    4  Saldo de reembolso disponible, no preseleccionado
    5  Total
    6  Costo estimado de recepción
    7  Plazos y ruta de resolución
    8  Aceptación de bases con enlace
    9  [ Revisar y pagar ]  → paso de revisión  → [ Confirmar pago ]

Sin cuenta atrás de sesión · sin *quedan X viendo esto* · sin paquete destacado · el retroceso conserva los datos · la probabilidad sigue visible en el paso final.

## 6.4 PU-05 · Verificación pública

Sin autenticación, indexable, compartible. **Es la superficie que sostiene la tesis del producto.**

    1  Resultado: número ganador
    2  "Este sorteo puede verificarse sin confiar en LIBOX"
    3  Los cuatro pasos en lenguaje llano
    4  Baliza: fuente + ronda + ENLACE EXTERNO
    5  Datos criptográficos (plegado)
    6  Instantánea del pool (descargable)
    7  Cadena de re-sorteo si la hubo

El punto 4 lleva enlace que **sale del dominio de LIBOX**, con indicación explícita de que ese es el dato que debe comprobarse fuera. Es contraintuitivo enviar tráfico afuera en la superficie más valiosa; es también lo único que hace verdadera la promesa.

## 6.5 US-03 · Mis tickets

    1  Sorteos con participación activa
    2  Por sorteo: números, probabilidad actual, estado del pool
    3  AVISO DE INDEPENDENCIA  ← persistente, no descartable
    4  Historial de participaciones cerradas
    5  Acceso a la prueba de cada sorteo ejecutado

**El aviso de independencia es visible sin desplazar y no se puede cerrar.** Es la contramedida a la falacia del jugador y su presencia es criterio de liberación.

El historial muestra resultados anteriores **sin acentuar rachas**: nada de *llevas 5 sin ganar* ni *tu suerte está por cambiar*.

## 6.6 CL-12 · Liquidaciones del organizador

    1  Resumen: pendiente, retenido, pagado
    2  Tabla por sorteo con estado y fecha estimada
    3  Detalle: seis gates con cuál falta y por qué
    4  Historial de pagos con referencia

El estado *Retenido* siempre con motivo y fecha. El desglose sin cargos posteriores. El plazo estimado hasta el cobro visible **antes** de publicar el sorteo.

## 6.9 PU-11 · Directorio de organizadores

**Zona:** atracción. **Es la mitad del mecanismo del que depende H-07.**

    1  Título y explicación en una línea
    2  Filtros: categoría, con oportunidad activa, nivel de reputación
    3  Ordenamiento CON CRITERIO VISIBLE
    4  Tarjetas de organizador: nombre, nivel, completadas, activas
    5  Paginación

| \#      | Regla                                                                                                           |
| ------- | --------------------------------------------------------------------------------------------------------------- |
| PU11-01 | El ordenamiento **expone su criterio en una interacción** (LINT-006). Sin razón visible, la lista no se publica |
| PU11-02 | La tarjeta muestra **oportunidades completadas y entregadas**, no publicadas. Publicar no acredita nada         |
| PU11-03 | **Nunca muestra recaudación, múltiplo ni identidad de participantes** (PR-17, R-10)                             |
| PU11-04 | Un organizador sin historial se marca como **nuevo y verificado**; no se oculta ni se penaliza visualmente      |
| PU11-05 | Las posiciones destacadas llevan etiqueta y van **separadas del orden orgánico**                                |

**PU11-04 importa más de lo que parece.** Todo organizador empieza sin historial, y una interfaz que castigue visualmente al recién llegado hace imposible el arranque del lado de la oferta — que es el lado escaso.

## 6.10 PU-12 · Perfil público de organizador

**Zona:** atracción. **Es la garantía que ofrece quien pide dinero al público** (LBPF V3 R-10).

    1  Identidad: nombre, logotipo, nivel de reputación, verificación
    2  HISTORIAL: completadas, entregadas, tiempo medio de entrega
    3  Oportunidades activas
    4  Oportunidades históricas con enlace a su prueba pública
    5  Controversias resueltas, si las hubo

| \#      | Regla                                                                                                      |
| ------- | ---------------------------------------------------------------------------------------------------------- |
| PU12-01 | El historial es **el contenido principal**, no un apéndice. Es lo que permite comprar a un desconocido     |
| PU12-02 | Cada oportunidad histórica enlaza a **su prueba pública verificable**                                      |
| PU12-03 | **Nunca muestra recaudación, múltiplo, identidad de participantes ni concentración**                       |
| PU12-04 | Las controversias resueltas se muestran **con su resultado**, sin narrativa ni identidad de la contraparte |
| PU12-05 | Los datos del organizador persona natural se limitan a **nombre e inicial**                                |

**PU12-04 es contraintuitivo y deliberado.** Ocultar las controversias haría el perfil más vendedor y menos creíble: **un historial sin ninguna incidencia en cincuenta oportunidades parece maquillado.** Mostrarlas resueltas es lo que hace confiable el resto.

**Fundamento de ambas superficies.** Sin ellas el participante ve oportunidades sueltas y nunca a quién está detrás. **Son el mecanismo que transfiere la confianza del organizador conocido al desconocido**, y por tanto lo que convierte el catálogo en marketplace en lugar de una suma de herramientas.

## 6.7 AD-06 · Panel único de alarmas

Un solo panel para las nueve familias. Filtros por familia, severidad, dueño y estado. Vista por defecto: **mis alarmas abiertas, ordenadas por plazo**.

Resolver exige motivo, también cuando la conclusión es que no hay problema. Sin dueño nominal la alarma no puede crearse.

## 6.8 Superficies de administración

Comunes a todas: identificador de traza visible y copiable · cronología completa de la entidad · toda mutación con motivo · segunda firma señalada antes de decidir · foco inicial nunca en la acción irreversible.

# 7\. Manual de redacción y textos aprobados

## 7.1 Principios

| \#    | Principio                                                                            |
| ----- | ------------------------------------------------------------------------------------ |
| CP-01 | **Claro antes que ingenioso.** Se escribe para quien está decidiendo con dinero      |
| CP-02 | **Sin claims absolutos.** Nada es *garantizado*, *100 % seguro* ni *infalible*       |
| CP-03 | **Sin coerción.** No se apura, no se avergüenza, no se culpa                         |
| CP-04 | **Sin urgencia fabricada.** Solo se comunica escasez y plazos reales                 |
| CP-05 | **La probabilidad se dice, no se insinúa**                                           |
| CP-06 | **El error no culpa al usuario**                                                     |
| CP-07 | **La reserva en materia financiera se respeta sin excepción** (§7.5)                 |
| CP-08 | Segunda persona, voz activa, frases cortas                                           |
| CP-09 | Cifras con separador de miles y símbolo de moneda del mercado                        |
| CP-10 | Sin jerga técnica en superficies de usuario: *prueba del sorteo*, no *hash del pool* |

## 7.2 Vocabulario

| Se dice              | No se dice            |
| -------------------- | --------------------- |
| Oportunidad · sorteo | Juego · apuesta       |
| Participar           | Jugar · apostar       |
| Ticket               | Boleto de la suerte   |
| Organizador          | Vendedor              |
| Probabilidad         | Chance · suerte       |
| Prueba del sorteo    | Algoritmo             |
| Saldo de reembolso   | Billetera · monedero  |
| Retenido             | Bloqueado · congelado |
| Reclamo              | Denuncia · queja      |

*Jugar* y *apostar* se evitan por precisión: LIBOX no lucra con el azar, cobra comisión por el uso de su sistema. El vocabulario debe sostener esa posición estructural.

## 7.3 Textos obligatorios

Aparecen literalmente y no se reescriben por superficie.

**Independencia probabilística** — persistente en US-03: \> Los resultados anteriores no aumentan ni reducen la probabilidad de este sorteo. Cada sorteo es independiente.

**Probabilidad** — formato en toda superficie: \> 1 de 1.000 · 0,10 % · 1 por cada 1.000 tickets

**Valor del premio:** \> Valor verificado: S/ 4.500. Referencia de mercado del 2 de agosto de 2026.

**Verificación pública** — encabezado de PU-05: \> Este sorteo puede verificarse sin confiar en LIBOX. El valor de la baliza se consulta en su fuente pública, fuera de nuestros sistemas.

**Garantía de reembolso** — en bases y en detalle: \> Si el sorteo se cancela por cualquier causa, se devuelve el importe íntegro de todos los tickets. El dinero permanece retenido hasta que la entrega esté verificada.

**Estado retenido:** \> Retenido hasta el 25 de agosto. Se libera al cumplirse el plazo de seguridad por contracargo.

**Envío a cargo del ganador** — antes de comprar: \> El costo de envío lo asume quien gana. Estimado a tu zona: desde S/ 15.

**Concentración alcanzada:** \> Has alcanzado el máximo de tickets por participante en este sorteo.

**Límite propio alcanzado:** \> Esta compra supera el límite mensual que configuraste (S/ 300). Puedes revisarlo en tu cuenta.

**Autoexclusión, antes de confirmar:** \> Durante 30 días no podrás comprar tickets ni recibirás comunicación comercial. **Esta decisión no puede revertirse antes de ese plazo.** Podrás seguir consultando tu historial, reclamar premios pendientes y disponer de tu saldo.

**Aumento de límite:** \> Reducir un límite se aplica de inmediato. Aumentarlo se aplica en 24 horas.

## 7.4 Errores

Los códigos completos están en L3 V7 §8. Aquí, el texto visible. **Ninguno culpa al usuario ni revela existencia de cuentas.**

| Código                               | Texto                                                                                                          |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| `ERR_AUTH_INVALID_CREDENTIALS`       | Los datos de acceso no son correctos.                                                                          |
| `ERR_IDENTITY_EMAIL_TAKEN`           | No fue posible completar el registro con esos datos.                                                           |
| `ERR_IDENTITY_DOCUMENT_TAKEN`        | Ese documento ya está asociado a una cuenta.                                                                   |
| `ERR_IDENTITY_UNDERAGE`              | Debes ser mayor de edad para participar en LIBOX.                                                              |
| `ERR_IDENTITY_VERIFICATION_REQUIRED` | Verifica tu identidad para realizar tu primera compra.                                                         |
| `ERR_IDENTITY_LIVENESS_FAILED`       | No pudimos completar la verificación. Vuelve a intentarlo con buena iluminación.                               |
| `ERR_IDENTITY_DOCUMENT_EXPIRED`      | Tu documento está vencido. Actualízalo para poder comprar. Puedes seguir reclamando premios y usando tu saldo. |
| `ERR_ORDER_MIN_AMOUNT`               | El monto mínimo de compra es S/ 10,00. Te faltan S/ 5,00.                                                      |
| `ERR_ORDER_INSUFFICIENT_INVENTORY`   | Quedan 3 tickets disponibles. Ajusta la cantidad para continuar.                                               |
| `ERR_ORDER_RESERVATION_EXPIRED`      | La reserva expiró y los tickets volvieron al pool. Puedes intentarlo de nuevo.                                 |
| `ERR_ORDER_SELF_PURCHASE`            | No es posible comprar tickets de un sorteo propio.                                                             |
| `ERR_LIMIT_CONCENTRATION`            | Has alcanzado el máximo de tickets por participante en este sorteo.                                            |
| `ERR_LIMIT_SELF_EXCLUDED`            | Tu cuenta tiene una autoexclusión activa hasta el 12 de septiembre.                                            |
| `ERR_PAYMENT_PROVIDER_ERROR`         | No pudimos procesar el pago. No se realizó ningún cargo. Puedes intentarlo de nuevo.                           |
| `ERR_RESOLUTION_EXTERNAL_CONTACT`    | Por seguridad de ambas partes, la coordinación se realiza dentro de esta sala.                                 |
| `ERR_RESOLUTION_CLAIM_EXPIRED`       | El plazo para reclamar este premio venció el 20 de agosto.                                                     |
| `ERR_DISPUTE_EVIDENCE_REQUIRED`      | Adjunta al menos un documento o imagen para abrir el reclamo.                                                  |
| `ERR_SETTLEMENT_PAYOUT_FROZEN`       | Los cobros están en espera por un cambio reciente de datos bancarios. Se liberan el 9 de agosto.               |
| `ERR_MARKET_SUSPENDED`               | La operación está temporalmente suspendida en tu país. Tus premios, reembolsos y saldo siguen disponibles.     |
| `ERR_RAFFLE_NOT_ACTIVE`              | Este sorteo ya no admite compras.                                                                              |

**Nota sobre** `ERR_PAYMENT_PROVIDER_ERROR`**.** *No se realizó ningún cargo* solo aparece cuando el sistema tiene certeza. Ante duda se muestra el estado `unknown` de §5.9, nunca una afirmación que podría ser falsa.

**Nota sobre** `ERR_MARKET_SUSPENDED`**.** La segunda frase es obligatoria: INV-33 establece que ninguna suspensión retiene dinero de terceros, y el usuario debe saberlo en el momento en que ve el bloqueo.

## 7.5 Textos de cumplimiento financiero

**Aplicación literal de la excepción de reserva de LBPF V3 §0.3.** Es la única materia en la que LIBOX no es transparente con el usuario sobre lo que ocurre, y esa reserva se sostiene en el copy o no se sostiene en absoluto.

| Situación            | Texto permitido                                                                      | **Prohibido**                             |
| -------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------- |
| Tramo de declaración | Para continuar, necesitamos que declares el origen de los fondos.                    | Hemos detectado actividad inusual         |
| Tramo documental     | Para continuar, necesitamos documentación que respalde el origen de los fondos.      | Tu cuenta está bajo revisión por sospecha |
| Aprobación previa    | Esta operación requiere una revisión previa. Te avisaremos en un máximo de 48 horas. | Estamos analizando tu caso                |
| Caso abierto         | *Sin comunicación específica*                                                        | Cualquier mención de análisis o reporte   |

**Regla absoluta:** ningún texto, notificación, correo o mensaje de soporte revela la existencia de un análisis por sospecha o de un reporte. El requerimiento documental sí se comunica con claridad; el motivo real, nunca.

## 7.6 Notificaciones críticas

Van obligatoriamente por correo **y** por mensajería o SMS. La notificación instantánea nunca es canal único.

| Evento               | Asunto                                             | Cuerpo                                                                                                                                               |
| -------------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ganador              | Ganaste el sorteo LBX-202608-A7K3M                 | Tu ticket 743 resultó ganador de: iPhone 17 Pro Max. Tienes hasta el 20 de agosto para reclamarlo. Verifica el sorteo aquí.                          |
| Recordatorio         | Te quedan 3 días para reclamar tu premio           | Tu premio del sorteo LBX-202608-A7K3M sigue disponible. Si no lo reclamas antes del 20 de agosto, se aplicará la ruta publicada en las bases.        |
| Cancelación          | El sorteo LBX-202608-A7K3M fue cancelado           | Se devolvió el importe íntegro de tus tickets a tu saldo de reembolso: S/ 25,00. Puedes usarlo en cualquier sorteo o solicitar su transferencia.     |
| Re-sorteo            | Se realizará un nuevo sorteo de LBX-202608-A7K3M   | El ganador anterior no reclamó dentro del plazo. Tus tickets siguen participando. El nuevo sorteo se ejecutará el 25 de agosto y podrás verificarlo. |
| Liquidación retenida | Tu liquidación está retenida hasta el 25 de agosto | Se libera al cumplirse el plazo de seguridad por contracargo. Puedes ver el detalle en tu panel.                                                     |

**Ninguna notificación comercial se envía a usuarios autoexcluidos.** Las operativas y de seguridad sí, porque son derechos, no promoción.

# 8\. Estados de superficie

Comunes a toda superficie. Se declaran una vez.

| Estado           | Regla                                                                                                                           |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Carga**        | Esqueleto con la forma del contenido esperado, no un girador centrado. Cesa el pulso al resolverse                              |
| **Vacío**        | Explica por qué está vacío y ofrece una acción concreta. Nunca solo *no hay resultados*                                         |
| **Error**        | Qué ocurrió, si se perdió algo, y qué hacer. Con identificador de traza copiable en superficies de organizador y administración |
| **Sin conexión** | Indica el estado y conserva lo introducido. En compra, aplica la recuperación de §5.9                                           |
| **Restringido**  | Explica por qué y qué sí está disponible. Nunca una pantalla en blanco                                                          |
| **Éxito**        | Confirmación de 180 ms, una vez. Sin celebración                                                                                |
| **Parcial**      | Cuando parte del contenido falla, se muestra lo disponible y se marca lo que no                                                 |

**Ejemplos de estado vacío, por superficie:**

| Superficie              | Texto                                                                                          |
| ----------------------- | ---------------------------------------------------------------------------------------------- |
| Catálogo sin resultados | No hay sorteos que coincidan con estos filtros. Prueba ampliando el rango de precio.           |
| Mis tickets             | Aún no participas en ningún sorteo. Explora las oportunidades disponibles.                     |
| Liquidaciones           | Todavía no tienes liquidaciones. Aparecerán cuando se complete la entrega de tu primer sorteo. |
| Alarmas                 | No tienes alarmas asignadas.                                                                   |
| Sala de resolución      | La conversación empieza cuando el ganador reclame el premio.                                   |

# 9\. Verificación conductual

## 9.1 Bloquean la integración

| Regla        | Verifica                                                                                                   |
| ------------ | ---------------------------------------------------------------------------------------------------------- |
| **LINT-003** | Ninguna animación superior a 240 ms en Zona de Decisión                                                    |
| **LINT-004** | Ninguna animación de repetición infinita en Zona de Decisión                                               |
| **LINT-005** | Ninguna opción monetaria o de comunicación premarcada                                                      |
| **LINT-011** | Ninguna participación adicional ni ventaja de probabilidad derivada del gasto, la suscripción o el volumen |

Se ejecutan sobre el árbol de componentes y sus metadatos declarados, no sobre el sistema en ejecución. **Bloquean el merge, no el lanzamiento:** el defecto se detiene antes de existir en ningún entorno, y quien lo escribió lo corrige en minutos.

## 9.2 Advierten y se calibran

`LINT-001` urgencia atada a plazo real · `LINT-002` presencia de costo, probabilidad y evidencia · `LINT-006` recomendación con metadata de razón · `LINT-007` copy sin claim absoluto · `LINT-008` baja en dos pasos · `LINT-009` propagación de traza · `LINT-010` etiquetas accesibles.

## 9.3 Lista de comprobación por superficie

Se aplica antes de liberar cualquier superficie nueva o modificada.

| \# | Comprobación                                                                                           |
| -- | ------------------------------------------------------------------------------------------------------ |
| 1  | ¿Costo, probabilidad y tamaño de pool visibles antes del llamado a la acción?                          |
| 2  | ¿Valor del premio verificado, con fuente y fecha?                                                      |
| 3  | ¿Plazos, ruta de resolución y costos de recepción publicados antes de comprar?                         |
| 4  | ¿Evidencia accesible en una interacción, sin navegar?                                                  |
| 5  | ¿Llamado a la acción descriptivo y no coercitivo?                                                      |
| 6  | ¿Cero animación superior a 240 ms o infinita en zona de decisión?                                      |
| 7  | ¿Cero opciones premarcadas?                                                                            |
| 8  | ¿Prueba social exclusivamente de resultados reales?                                                    |
| 9  | ¿Todo ordenamiento con su criterio visible?                                                            |
| 10 | ¿Corrección posible antes del compromiso irreversible, sin pérdida de datos?                           |
| 11 | ¿Baja alcanzable en dos pasos o menos?                                                                 |
| 12 | ¿Identidad y concentración **no** divulgadas?                                                          |
| 13 | ¿Etiquetas y textos provenientes del servidor?                                                         |
| 14 | ¿Composición probada al 150 % de longitud de texto?                                                    |
| 15 | ¿Contraste AA verificado en todos los pares de la superficie?                                          |
| 16 | ¿Operable por teclado, con foco visible?                                                               |
| 17 | ¿Estados de carga, vacío, error, sin conexión y restringido definidos?                                 |
| 18 | ¿Movimiento reducido respetado?                                                                        |
| 19 | En oportunidad con entrada gratuita, **¿ambas vías con la misma prominencia y la misma probabilidad?** |
| 20 | **¿Cero elementos que sugieran ventaja de probabilidad por gasto o suscripción?**                      |
| 21 | ¿Recaudación y múltiplo **fuera** de toda superficie pública?                                          |
| 22 | ¿El sello de LIBOX presente y sin competir con costo, probabilidad, pool ni evidencia?                 |

## 9.4 Criterios de no liberación

No se libera una superficie que: omita costo, probabilidad o pool en zona de decisión · incumpla un límite duro de movimiento · introduzca una opción premarcada monetaria · presente prueba social no auténtica · oculte un costo hasta después de la compra · use color como único portador de significado en un estado · divulgue identidad o concentración de participantes.

# 10\. Activos digitales de producto

Complementa VIES V3 §11, que gobierna el arte. Aquí, la especificación técnica de implementación.

## 10.1 Aplicación web progresiva

| Activo                         | Especificación                                                                 |
| ------------------------------ | ------------------------------------------------------------------------------ |
| `icon-192.png`, `icon-512.png` | Cuadrado completo, sin transparencia, isotipo sobre `brand.purple`             |
| `icon-maskable-512.png`        | **Zona segura del 80 % centrada.** El lanzador recorta según su propia máscara |
| `apple-touch-icon.png`         | 180 px, cuadrado completo, **sin esquinas redondeadas y sin transparencia**    |
| `theme_color`                  | `#0B1020` — barra del sistema                                                  |
| `background_color`             | `#FFFFFF` — pantalla de arranque                                               |
| `display`                      | `standalone`                                                                   |
| `orientation`                  | `any` — AC-11 prohíbe depender de la orientación                               |

**La zona segura del icono enmascarable no es opcional.** Un isotipo que ocupe el lienzo completo aparecerá recortado en los lanzadores que aplican máscara circular.

## 10.2 Favicon

`favicon.svg` como principal, con variante para esquema oscuro mediante consulta de medios · `favicon.ico` multitamaño de 16, 32 y 48 px como reserva · en tamaños de 16 y 32 px se usa **solo el isotipo**, nunca el lockup, que a esa escala es una mancha.

## 10.3 Compartir en redes

| Activo                 | Especificación                                                  |
| ---------------------- | --------------------------------------------------------------- |
| Imagen de compartición | **1200 × 630 px**, PNG                                          |
| Composición            | Imagen del premio · título · **precio y probabilidad** · lockup |
| Título                 | Título del sorteo, máximo 60 caracteres                         |
| Descripción            | Premio, precio del ticket y probabilidad, máximo 155 caracteres |

**Es el activo de crecimiento más importante del producto** y no estaba especificado. Compartir un sorteo es la palanca de adquisición natural de un marketplace de este tipo.

**Y lleva la probabilidad**, porque una imagen compartida que muestre solo el premio y el precio incumpliría DP-03 fuera de la plataforma. La norma conductual no termina en el borde del dominio.

## 10.4 Notificaciones

| Plataforma                   | Especificación                                                          |
| ---------------------------- | ----------------------------------------------------------------------- |
| **Android, barra de estado** | **Silueta monocroma con transparencia**, 24 × 24 dp. El sistema la tiñe |
| Android, icono grande        | Isotipo a color, 256 × 256 px                                           |
| Web                          | Isotipo a color, 192 × 192 px                                           |
| Insignia                     | Silueta monocroma, 96 × 96 px                                           |

**El icono monocromo de Android es una corrección técnica, no una preferencia.** El sistema descarta el color y conserva únicamente el canal alfa: un isotipo morado con degradado se renderiza como una **mancha blanca sólida**, ilegible. Requiere una versión de silueta creada a propósito.

## 10.5 Correo

| Aspecto                | Regla                                                                       |
| ---------------------- | --------------------------------------------------------------------------- |
| Formato del logotipo   | **PNG a doble resolución con ancho fijo.** Muchos clientes bloquean SVG     |
| Fondos                 | Sin imágenes de fondo; color plano. Muchos clientes los suprimen            |
| Ancho                  | 600 px, con versión fluida para móvil                                       |
| Modo oscuro            | Versión negativa del lockup con `prefers-color-scheme` y reserva en claro   |
| Texto alternativo      | Obligatorio en todas las imágenes: muchos clientes las bloquean por defecto |
| Versión de texto plano | Obligatoria en notificaciones críticas                                      |

**La versión de texto plano no es cortesía.** Si un ganador tiene las imágenes bloqueadas y el correo depende de ellas, pierde su premio por un plazo vencido.

## 10.6 Documentos

Bases del sorteo, actas y paquetes forenses: lockup horizontal en el encabezado · marca de agua del isotipo al 4 % de opacidad · pie con código del sorteo, versión del documento y hash cuando aplique.

# Anexo A — Tokens

    {
      "brand": { "purple":"#6D28D9","navy":"#0B1020","violet":"#8B5CF6",
                 "green":"#10B981","gray":"#E5E7EB","white":"#FFFFFF" },
      "text": { "primary":"#0B1020","secondary":"#3E4661","muted":"#667085",
                "onDark":"#FFFFFF" },
      "surface": { "canvas":"#F7F8FA","attraction":"#F6F1FE","card":"#FFFFFF",
                   "border":"#E5E7EB","overlay":"rgba(11,16,32,0.60)" },
      "state": {
        "success":{"text":"#047857","bg":"#D1FAE5"},
        "warning":{"text":"#B45309","bg":"#FEF3C7"},
        "danger" :{"text":"#B91C1C","bg":"#FEE2E2"},
        "info"   :{"text":"#1D4ED8","bg":"#DBEAFE"},
        "held"   :{"text":"#3E4661","bg":"#E9ECF3"},
        "brand"  :{"text":"#5B21B6","bg":"#EDE9FE"}
      },
      "accent": { "rank":"#A16207","live":"#047857" },
      "gradient": {
        "brand":"linear-gradient(135deg,#6D28D9,#8B5CF6)",
        "hero" :"linear-gradient(135deg,#4C1D95,#6D28D9)",
        "trust":"linear-gradient(180deg,#0B1020,#1E2947)",
        "textOverlay":"rgba(11,16,32,0.35)"
      },
      "typography": {
        "family":"Manrope, system-ui, sans-serif",
        "weights":{"regular":400,"medium":500,"semibold":600,"bold":700},
        "wordmarkOnly":{"extrabold":800},
        "scale":{
          "display":{"mobile":[28,34],"desktop":[40,46],"weight":700},
          "h1":{"mobile":[24,30],"desktop":[32,38],"weight":700},
          "h2":{"mobile":[20,26],"desktop":[24,30],"weight":600},
          "h3":{"mobile":[17,23],"desktop":[18,24],"weight":600},
          "body":{"mobile":[16,24],"desktop":[15,23],"weight":400},
          "caption":{"mobile":[14,20],"desktop":[13,18],"weight":400},
          "micro":{"mobile":[12,16],"desktop":[11,15],"weight":600},
          "money":{"mobile":[24,30],"desktop":[28,32],"weight":700},
          "probability":{"mobile":[16,24],"desktop":[15,23],"weight":700}
        }
      },
      "radius": {"sm":8,"md":12,"lg":16,"xl":20,"pill":999},
      "spacing": [4,8,12,16,20,24,32,40,48,64,80],
      "shadow": {
        "card":"0 1px 3px rgba(11,16,32,.08)",
        "hover":"0 4px 12px rgba(11,16,32,.12)",
        "raised":"0 8px 24px rgba(11,16,32,.16)",
        "decision":"0 1px 2px rgba(11,16,32,.10)"
      },
      "motion": {
        "attraction":{"hover":160,"state":220,"screen":240},
        "calm":{"hover":120,"state":160,"screen":180},
        "drawReveal":{"enter":200,"reveal":400,"settle":200,"total":800},
        "easing":{"standard":"cubic-bezier(0.2,0,0,1)","enter":"cubic-bezier(0,0,0,1)"},
        "hardLimits":{"maxDecisionMs":240,"infiniteInDecision":false}
      },
      "breakpoints": {"xs":360,"sm":640,"md":768,"lg":1024,"xl":1280},
      "touch": {"minTarget":44,"minGap":8}
    }

# Anexo B — Trazabilidad con LBPF V3

| Norma                                  | Implementación                                       |
| -------------------------------------- | ---------------------------------------------------- |
| R-03 Prevalencia del usuario           | §1.2 OB-01 · §6.3 CS-05                              |
| R-04 Neutralidad probabilística        | §7.3 texto de independencia · §5.2                   |
| R-05 Evidencia antes de persuasión     | §6.2 PU03-01 · §5.11                                 |
| R-08 Prohibición de vulnerabilidad     | §5.16 SP-01 · §5.17 LS-05                            |
| R-10 Confidencialidad de participación | §5.7 TQ-04 · §5.10 · §6.10 PU12-03 · §9.3 punto 12   |
| BR-01 Comprensión                      | §5.1 ranura C · §5.2                                 |
| BR-02 Reversibilidad                   | §5.8 CS-01                                           |
| BR-03 Control                          | §5.17                                                |
| BR-04 Dignidad                         | §7.1 CP-03 · §7.4                                    |
| BR-05 Evidencia                        | §5.11                                                |
| BR-06 Descanso                         | §7.6                                                 |
| BR-08 Integridad del proceso           | §5.1 ranura D · §6.2                                 |
| **BR-09 Proporción razonable**         | **§1.2 PR-17 · §6.9 PU11-03 · §6.10 PU12-03**        |
| §0.3 Reserva financiera                | **§7.5**                                             |
| §5.4 Custodia patrimonial              | §7.3 garantía de reembolso                           |
| §6.2 Verified Opportunity Card         | **§5.1**                                             |
| §6.3 Veto anti-impulso                 | §1.2 PR-04 a PR-09                                   |
| §6.4 Motion Calm                       | **§3**                                               |
| §7 Indicadores                         | §6.2 PU03-01 · §5.11                                 |
| §9.1 Régimen de linter                 | **§9.1**                                             |
| **P13 Igualdad de vía**                | **§1.2 OB-09, OB-10, PR-15 · §5.20 · §9.1 LINT-011** |
| **§13.2 Límite de suscripción**        | **§7.8 texto obligatorio de suscripción**            |
| §12.2 Ética comercial                  | §5.6 · §10.3                                         |
| §13 Neutralidad económica              | §7.2 vocabulario                                     |

# Anexo C — Trazabilidad con PRD MVP V9

| Superficie del PRD            | Sección            |
| ----------------------------- | ------------------ |
| PU-03 Detalle                 | §6.2               |
| PU-05 Verificación pública    | §6.4 · §5.10       |
| PU-08 Simulador               | §5.14 ST-04        |
| US-01 Compra                  | §6.3 · §5.7 · §5.8 |
| US-02 Retorno de pago         | §5.9               |
| US-03 Mis tickets             | §6.5               |
| US-06 Panel de gasto          | §5.16              |
| US-07 Límites y autoexclusión | §5.17              |
| US-09 Sala de resolución      | §5.12              |
| US-12 Controversia            | §5.13              |
| CL-08 Etapas registrables     | §5.15              |
| CL-12 Liquidaciones           | §6.6 · §5.14       |
| AD-06 Panel de alarmas        | §6.7 · §5.18       |
| AD-01 a AD-15                 | §6.8 · §5.19       |

# Anexo D — Pendientes de L4 V2

| \#   | Materia                                                                                            |
| ---- | -------------------------------------------------------------------------------------------------- |
| D-01 | Composición detallada de las 60 superficies. Esta versión especifica las de mayor carga conductual |
| D-02 | Modo oscuro de producto. Trust Navy da la base; la paleta completa está pendiente                  |
| D-03 | Ilustración y estados vacíos ilustrados                                                            |
| D-04 | Sonido: hoy no existe y la ausencia es deliberada                                                  |
| D-05 | Textos de mercados adicionales, cuando se abran                                                    |
| D-06 | Componentes de administración avanzados: conciliación y expedientes de cumplimiento                |

*LIBOX Design System & Product Experience Standard — Nivel L4 V2. Gobernado por LBPF V3 conforme a R-01 y R-02. Consume PRD MVP V9, Especificación Técnica L3 V7 y VIES V3. Este documento no crea reglas de negocio: las materializa.*
