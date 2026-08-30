# Índice de contenidos

# 0\. Alcance y método

Auditoría del corpus vigente contra las 26 decisiones acumuladas en esta sesión, antes de emitirlas. **El objetivo no es validar: es encontrar lo que se rompe.**

**Método:** verificación programática de invariantes y referencias cruzadas sobre los documentos vigentes, más revisión por dominio. Todo hallazgo cita el invariante o la regla concreta.

| Corpus auditado        | Versión |
| ---------------------- | ------- |
| LBPF                   | V2      |
| Product Strategy       | V2      |
| PRD MVP                | V7      |
| PRD Enterprise         | V3      |
| Especificación Técnica | V6      |
| Design System          | V1      |
| VIES                   | V3      |
| Backlog                | V2      |

**Base medida:** 38 invariantes, 188 reglas de negocio, 119 tablas ejecutándose con cero errores, 21 subroles, 11 incompatibilidades.

# 1\. Veredicto del comité

**El corpus es coherente. Las decisiones nuevas no lo son todavía.**

Las 26 decisiones acumuladas son individualmente buenas y **cuatro de ellas rompen invariantes vigentes** si se emiten tal cual. Ninguna es irreparable; todas exigen una decisión explícita en lugar de una incorporación silenciosa.

| Dimensión                                            | Estado                |
| ---------------------------------------------------- | --------------------- |
| Coherencia interna del corpus vigente                | **Sólida**            |
| Coherencia de las decisiones nuevas entre sí         | **Sólida**            |
| Coherencia de las decisiones nuevas contra el corpus | **Cuatro conflictos** |
| Ejecutabilidad técnica                               | **Verificada**        |
| Control documental                                   | **Sólido**            |
| **Control de alcance**                               | **Deficiente**        |

**Decisión del comité:** emitir, con las cuatro resoluciones de §2 incorporadas y con el cierre de alcance de §5 aplicado.

# 2\. Conflictos que hay que resolver antes de emitir

## C-01 · El techo de ingresos accesorios se rompe 🔴

**L1 V2 §5.7** establece: *“Ninguna fuente accesoria puede superar el 10 % del ingreso total sin revisión estratégica. Si lo hiciera, LIBOX habría dejado de ser infraestructura de confianza para convertirse en otra cosa.”*

Las fuentes accesorias declaradas eran tres: posición destacada, verificación reforzada y operación asistida.

**Las decisiones nuevas añaden dos fuentes de ingreso recurrente:** LIBOX Club y el plan de sorteos promocionales. Y el plan promocional **no es accesorio**: para un cine o una tienda por departamentos es la **única** forma de facturación, porque no hay venta de tickets sobre la que cobrar comisión.

**El conflicto es real:** con estas dos líneas, el ingreso no proveniente de comisión puede superar con holgura el 10 % sin que nada haya salido mal.

**Resolución propuesta.** Separar en tres categorías con techos distintos:

| Categoría             | Contenido                                                          | Techo                                                      |
| --------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------- |
| **Ingreso principal** | Comisión sobre recaudación                                         | Sin techo                                                  |
| **Segunda línea**     | Plan de sorteos promocionales                                      | **Sin techo, con revisión estratégica al superar el 30 %** |
| **Accesorio**         | Destacados, verificación reforzada, operación asistida, LIBOX Club | **10 %**                                                   |

**Fundamento del 30 %:** si más de un tercio del ingreso viene de sorteos promocionales, LIBOX ya no es principalmente un marketplace — es una herramienta de marketing con un marketplace al lado. Puede ser un buen negocio, pero es **otro negocio**, y la estrategia debe decidirse a conciencia y no descubrirse en un informe.

## C-02 · INV-06 no cubre los sorteos sin recaudación 🔴

**INV-06:** *“Ningún participante pierde su aporte en ningún escenario de fallo. El reembolso íntegro está financiado por la recaudación retenida.”*

En un sorteo con entrada gratuita **no hay aporte ni recaudación**. El invariante es literalmente inaplicable, y su promesa —que sostiene toda la confianza del producto— **no cubre a quien participó gratis**.

El riesgo no es teórico: quien pagó y no recibe, recupera su dinero. **Quien participó gratis solo se lleva la decepción, y llegó por la marca LIBOX.**

**Resolución propuesta.** INV-06 se desdobla:

**INV-06-a — Sorteos con recaudación.** Ningún participante pierde su aporte. Reembolso íntegro financiado por la retención.

**INV-06-b — Sorteos sin recaudación.** No hay aporte que devolver, y por eso la protección se traslada al **premio**: verificación de valor igual de estricta, custodia o garantía por encima del umbral, y penalización reputacional agravada por incumplimiento.

**Y una regla nueva:** cuando el premio lo pone el organizador y no LIBOX, **la garantía sustitutiva es condición de publicación**, no una recomendación. Sin dinero retenido, la garantía es lo único que queda.

## C-03 · Los seis gates de liquidación no aplican al organizador promocional 🟠

**INV-23** exige los seis gates para toda liquidación. Un organizador promocional **no recauda, no liquida y no cobra nada** — paga él.

Aplicarle los gates sería incoherente; ignorarlos sin declararlo sería un hueco.

**Resolución propuesta.** Declarar expresamente que el régimen promocional **no genera liquidación**, y sustituir la cadena de gates por una **cadena de conformidad**: verificación de premio → sorteo ejecutado → entrega atestada → cierre. Los tres primeros gates se conservan; G4, G5 y G6 no aplican porque no hay dinero del participante.

**Y el corolario que importa:** el plan promocional **se cobra por adelantado**. Es lo único que te da algo que retener si el organizador incumple.

## C-04 · Bienes registrables en régimen promocional 🔴

Nada en las decisiones nuevas impide que un organizador promocional sortee un **vehículo o un inmueble**. Y es previsible que quiera: una concesionaria haciendo campaña es exactamente el cliente del plan promocional.

**Pero el proceso de bienes registrables se apoya en el escrow.** Todo el diseño de las siete etapas —y en particular la cláusula 4 del instrumento notarial, que es la que convence al organizador de transferir antes de cobrar— parte de que LIBOX retiene \~125 % del valor del premio.

**En régimen promocional no hay nada retenido.** Si el organizador no transfiere el vehículo, no hay reembolso que hacer ni fondos que ejecutar, y el ganador se queda sin nada con la marca LIBOX de por medio.

**Resolución propuesta.** **Las categorías P-C1 y P-C2 quedan prohibidas en régimen promocional y en sorteos con entrada gratuita**, salvo con custodia efectiva del bien o garantía formal previa a la publicación. Se impone en el esquema, no en el procedimiento.

# 3\. Hallazgos menores

| \#   | Hallazgo                                                                      | Resolución                                                                                                                                                                      |
| ---- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| M-01 | La ventana horaria de ejecución desplaza el inicio del plazo de reclamo       | El plazo cuenta desde la **ejecución real**, no desde el cumplimiento de la condición. Ya es la regla —todo plazo cuenta desde un evento de sistema— pero conviene explicitarlo |
| M-02 | El límite de concentración del 30 % no aplica en sorteos con entrada gratuita | Una participación por persona lo hace innecesario. Declararlo para que nadie lo implemente dos veces                                                                            |
| M-03 | `AUDITOR_EXTERNAL` no tiene fila en la matriz de incompatibilidades           | Solo lectura, sin capacidad de mutación, **incompatible con todo subrol operativo**. Y vigencia obligatoria                                                                     |
| M-04 | El código de atribución podría leerse como recompensa por gasto               | RN-190 ya lo prohíbe: se paga por registro verificado, nunca por gasto del referido. **Medir sí, pagar por volumen no**                                                         |
| M-05 | El desglose de aporte de LIBOX a cada organizador es información comercial    | Va al panel privado del organizador. Lo público es el historial de sorteos completados                                                                                          |
| M-06 | La notificación de apagado podría exponer un defecto de seguridad             | Motivo **neutro** en la comunicación externa; el motivo técnico va al registro interno                                                                                          |
| M-07 | El panel de funciones podría revelar capacidades a subroles que no las tienen | Cada vista muestra solo lo que ese subrol domina, con estado y si puede actuar o solo escalar                                                                                   |

# 4\. Lo que la auditoría confirma

No todo son hallazgos. Cuatro cosas resisten el escrutinio y conviene decirlo:

**La arquitectura de configuración aguanta.** Las 26 decisiones nuevas no exigen ni un cambio de fronteras de agregado. Tipos, categorías, planes, ventanas y capacidades entran como datos. **INV-29 —ninguna regla de jurisdicción en el código— se sostiene bajo presión real**, que es la única prueba que vale.

**El motor de sorteo no se toca.** Ni la entrada gratuita, ni el régimen promocional, ni las ventanas horarias alteran el algoritmo. Sigue siendo compromiso, baliza futura y verificación contra la fuente.

**El control de acceso escaló bien.** Añadir un subrol temporal de auditoría externa es una fila en tres tablas. La matriz de otorgamiento con techo de privilegio, que nació de una pregunta tuya hace dos rondas, **absorbió el caso sin rediseño**.

**Y el descubrimiento competitivo reforzó la tesis en lugar de debilitarla.** Raffall, Luna y Ghani validan la demanda y confirman que **nadie está haciendo el marketplace multi-organizador**. La verificabilidad, que parecía un principio, resultó ser el mecanismo que hace posible el modelo entero: es lo que permite comprarle a un organizador desconocido.

# 5\. El hallazgo de gobierno — y es el más importante

**El alcance creció un 24 % en cuatro rondas, y el proceso que lo produjo sigue activo.**

| Momento                        | Alcance      |
| ------------------------------ | ------------ |
| Backlog V2 cerrado             | 745 SP       |
| Tras las decisiones acumuladas | **\~920 SP** |

**Cada ampliación fue justificada.** Ninguna fue capricho: el interruptor global faltaba, los sorteos gratuitos tocan la vía legal, el alta de administradores era un hueco real, y la matriz de casos de uso es un artefacto que L3 ya declaraba.

**Y ese es exactamente el problema.** Un proceso que encuentra huecos legítimos en cada revisión no se detiene por sí solo, porque siempre habrá una pregunta más que descubra algo cierto. La calidad de los hallazgos es lo que hace difícil parar.

**Lo que un comité debe decir aquí no es *deja de encontrar cosas*, sino *deja de emitirlas ahora*.**

## Regla de cierre propuesta

**La línea base se congela con estas 26 decisiones.** Todo hallazgo posterior —y los habrá— entra en **backlog de cambio** y se emite en una versión posterior, con el sistema ya en construcción.

Es el mecanismo que VIES ya tiene en su §14 y que recomendamos elevar a corpus: *las observaciones se registran; no generan versión documental hasta ser aprobadas y aplicadas*.

**Criterio para romper el congelamiento:** solo un hallazgo que impida construir o que exponga a un riesgo legal o patrimonial. Todo lo demás espera.

# 6\. Plan de emisión

## 6.1 Orden y fundamento

El orden no es arbitrario: **cada documento consume al anterior**, y emitirlos al revés produciría documentos implementando reglas que el rector aún no autoriza.

| \# | Documento                                | Versión | Por qué en esta posición                                                                                                                |
| -- | ---------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| 1  | **LBPF**                                 | **V3**  | Autoriza la excepción de neutralidad, el límite de la suscripción y la igualdad de probabilidad. **Sin esto, lo demás sería ilegítimo** |
| 2  | **Product Strategy**                     | **V3**  | Fija la estructura competitiva, la cuña corregida y los techos de C-01                                                                  |
| 3  | **PRD MVP**                              | **V8**  | Reglas de negocio, con INV-06 desdoblado y las prohibiciones de C-03 y C-04                                                             |
| 4  | **Especificación Técnica L3**            | **V7**  | Implementa: tablas, cuentas, restricciones y pruebas                                                                                    |
| 5  | **Matriz de Casos de Uso y SLA**         | **V1**  | Deriva de PRD y L3. **No puede escribirse antes**                                                                                       |
| 6  | **Guía de Extensión y Puntos de Cambio** | **V1**  | Deriva de L3                                                                                                                            |
| 7  | **Backlog**                              | **V3**  | Replanificación sobre el alcance final                                                                                                  |
| 8  | **Registro Maestro**                     | **V4**  | Cierra la línea vigente                                                                                                                 |
| 9  | **Dossier Legal**                        | **V1**  | Independiente. Puede emitirse en paralelo                                                                                               |

**No cambian:** PRD Enterprise V3 · Design System L4 V1 · VIES V3 · tokens L4 V2.

## 6.2 Contenido por documento

**LBPF V3** — Excepción de neutralidad para sorteos promocionales sin contraprestación · límite de la suscripción · **principio nuevo de igualdad de probabilidad entre vía gratuita y pagada** · precisión de R-10 sobre el historial público del organizador · beneficios nunca como descuento de ticket.

**L1 V3** — Raffall, No Hay Sin Suerte y Ghani con sus tres estructuras legales · cuña corregida a marca o creador con comunidad · distribución alquilada · bucle de descubrimiento cruzado · verificabilidad como transferencia de confianza · **tres categorías de ingreso con techos distintos (C-01)** · segunda línea promocional · H-07 con métrica desdoblada.

**PRD MVP V8** — Interruptor global con jerarquía restrictiva · sorteo con entrada gratuita y origen de premio · código de campaña con cupo · código de organizador para atribución · **INV-06 desdoblado (C-02)** · **régimen promocional sin liquidación (C-03)** · **prohibición de registrables sin escrow (C-04)** · directorio y perfil de organizador · marca compartida · LIBOX Club apagado · ventanas operativas · escalada de apagado · degradación por motivo · paneles por subrol · alta de cuenta interna · subroles con vigencia · verificación diferida al reclamo.

**L3 V7** — `platform_capabilities` · `free_entry_codes` y campañas con cupo atómico · `organizer_referral_codes` · `promotional_plans` · `subscriptions` y `benefits` · `subroles` con vigencia · `operating_windows` · `feature_toggle_log` · cuentas de gasto promocional e ingreso diferido · restricción de igualdad de probabilidad · prohibición de registrables sin garantía · casos de prueba negativos de todo lo anterior.

**Matriz de Casos de Uso V1** — \~120 casos en doce procesos, con tres matrices transversales.

**Guía de Extensión V1** — Por función: qué se cambia, dónde, si es configuración o código, y si requiere despliegue.

**Backlog V3** — \~920 SP, \~29 sprints, con las zonas sin generación asistida actualizadas.

**Dossier Legal V1** — Tres estructuras vivas documentadas y las doce preguntas reformuladas, con la clave: *¿la vía de entrada gratuita con probabilidades idénticas saca al sorteo del régimen de juego en Perú?*

## 6.3 Criterio de cierre

Cada documento pasa las nueve pruebas ya vigentes. **Y dos añadidas por esta auditoría:**

**10 · Ninguna decisión nueva contradice un invariante sin derogarlo expresamente.** Los cuatro conflictos de §2 nacieron de no comprobarlo.

**11 · Todo invariante que no aplique a un régimen lo declara explícitamente.** INV-06 e INV-23 fallaban aquí.

# 7\. Lo que sigue sin resolverse, y no lo resuelve un documento

| \#   | Materia                           | Estado                                                                         |
| ---- | --------------------------------- | ------------------------------------------------------------------------------ |
| A-01 | **Dictamen L-01**                 | Camino crítico externo. 2 a 4 meses. Ninguna decisión de producto lo sustituye |
| A-02 | **F0: veinte conversaciones**     | Dos semanas, sin ingeniería. Valida o refuta la cuña corregida                 |
| A-03 | Diseño de las 60 superficies      | 4 a 6 semanas, fuera del alcance en SP                                         |
| A-04 | Arte maestro de marca             | VIES V3 Anexo A lo exige                                                       |
| A-05 | Contratación de proveedores       | Yape confirmado; **Plin por verificar**                                        |
| A-06 | **Manual de operación**           | No existe. Recuperación, cese ordenado, guardia, rotación de claves            |
| A-07 | Relevo operativo antes del mes 12 | Las once incompatibilidades exigen personas distintas                          |

**A-01 y A-02 pueden empezar esta semana y no dependen de nada.** Son, con diferencia, las de mayor valor por unidad de esfuerzo de todo el plan.

*Auditoría de coherencia del comité fundador. Emitida antes de la actualización de la línea base para que los cuatro conflictos de §2 se resuelvan por decisión explícita y no por incorporación silenciosa.*
