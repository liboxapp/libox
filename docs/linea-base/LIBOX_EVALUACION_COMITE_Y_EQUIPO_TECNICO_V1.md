# Índice de contenidos

# 0\. Alcance y método

Dos evaluaciones independientes sobre la misma línea base, con criterios distintos y deliberadamente en tensión.

**El comité fundador** juzga si el proyecto es viable, defendible y financiable. **El equipo técnico contratado** juzga si con estos documentos puede construir el producto, cotizarlo y entregarlo.

Ambas parten de métricas medidas, no de impresión.

## 0.1 El corpus, en cifras

| Concepto                  | Valor                                                            |
| ------------------------- | ---------------------------------------------------------------- |
| Documentos vigentes       | 14                                                               |
| Volumen total             | 743.000 caracteres                                               |
| Repetición media          | **0,3 %** — solo L3 supera el 1 %, por cabeceras de esquema      |
| Invariantes               | 49                                                               |
| Reglas de negocio         | 304                                                              |
| Tablas ejecutables        | 135, con 199 restricciones, 148 claves foráneas y 5 disparadores |
| Casos de uso documentados | 107 en 12 procesos                                               |
| Plan de construcción      | 136 historias · 936 SP · 30 sprints                              |
| Verificación automática   | 8 controles, **cero fallos**                                     |

# PARTE I · COMITÉ FUNDADOR

# 1\. Veredicto

> **GO para construir. NO-GO para operar con dinero real.**

| Dimensión                    | Valoración                                          |
| ---------------------------- | --------------------------------------------------- |
| Tesis de producto            | **Sólida y diferenciada**                           |
| Posición competitiva         | **Clara, con un espacio real desatendido**          |
| Modelo de negocio            | Coherente, **con la hipótesis central sin validar** |
| Marco de riesgo y protección | **Superior a todo lo observado en el sector**       |
| Base técnica                 | **Ejecutable y probada**                            |
| Viabilidad legal             | **Sin resolver.** Riesgo existencial                |
| Capacidad de ejecución       | **Insuficiente para el alcance comprometido**       |
| Validación de mercado        | **Cero contacto con clientes reales**               |

**Las dos últimas filas son la razón por la que este comité no aprueba operación.** No son problemas del corpus: son problemas del proyecto que el corpus dejó visibles.

# 2\. Qué sostiene la tesis

## 2.1 El espacio desatendido es real, y está medido

Tres competidores analizados con información pública. **Ninguno es un marketplace multi-organizador operando en el mercado objetivo.**

|                   | Qué es                                        | Escala observada                           |
| ----------------- | --------------------------------------------- | ------------------------------------------ |
| Raffall           | Marketplace real, fuera de la región          | Casos de seis cifras por campaña           |
| No Hay Sin Suerte | **Operador único** con audiencia propia       | Dos Récords Guinness                       |
| Ghani             | Se presenta como marketplace; **es operador** | **\~191 tickets vendidos, cero ganadores** |

**Ghani es la evidencia más valiosa del análisis**, y en dos direcciones opuestas. Confirma que el espacio está libre —nadie hace el marketplace de verdad— y demuestra que **el catálogo sin comunidad no vende**, por grande que sea el premio.

## 2.2 La ventaja es estructural, no técnica

Cualquiera puede implementar compromiso criptográfico y revelación. **Lo que casi nadie acepta es el costo de las restricciones:** mostrar la probabilidad con el mismo peso que el precio, prohibir la urgencia fabricada, publicar un enlace que saca al usuario del propio dominio en la superficie más valiosa.

Esas decisiones cuestan conversión hoy y construyen defensa mañana. **Un competidor que copie el producto sin copiar las restricciones acaba en otra categoría** — y esa categoría tiene, tarde o temprano, un problema regulatorio.

## 2.3 El reencuadre que cambia el valor de la inversión

Durante esta línea base el comité identificó que la verificabilidad **no es un principio ético con costo**. Es el mecanismo que transfiere confianza del organizador conocido al desconocido, y por tanto **la palanca del modelo entero**: sin ella, quien llegó por una marca no compra a otra, y LIBOX se queda en herramienta.

Eso convierte la inversión en L0 y L3 de gasto de conciencia en infraestructura de negocio.

# 3\. Lo que el comité no aprueba

## 3.1 · Riesgo legal sin resolver — existencial

**LIBOX es el único de los cuatro actores analizados que conserva pago, azar y premio íntegros.** Los tres competidores rompen deliberadamente uno de los tres elementos.

No es un descuido: todo el diseño técnico hace el sorteo **más demostrablemente aleatorio**, que es precisamente el elemento que los demás eliminaron.

**Sin dictamen, no hay decisión posible sobre la ruta.** El Dossier Legal está preparado y las cuatro rutas analizadas con su costo. **Falta encargarlo.**

## 3.2 · La hipótesis central del negocio nunca se ha contrastado

**El 20 % de comisión no se ha discutido con un solo organizador real.** Está en el ledger, en el simulador, en el modelo de costos y en 936 puntos de historia de construcción.

Y el referente global —Raffall— cobra 10 % con suscripción. **La disposición a pagar de un organizador peruano frente a la gratuidad de sortear por su cuenta es la variable de la que depende el negocio, y es desconocida.**

Cuatro hipótesis de F0 se resuelven en dos semanas, con veinte conversaciones y cero ingeniería. **Que sigan sin resolver mientras se planifican catorce meses de construcción es el mayor error de secuencia del proyecto.**

## 3.3 · Capacidad de ejecución insuficiente

|                                         |                                             |
| --------------------------------------- | ------------------------------------------- |
| Alcance                                 | 936 SP · 30 sprints · 14 meses              |
| Equipo                                  | 4 personas generalistas                     |
| Incompatibilidades de control de acceso | 11, que exigen personas naturales distintas |

**Con cuatro personas, las once incompatibilidades son el mínimo exacto sin redundancia.** Si falta quien tiene `ADMIN_FINANCE`, no se liquida nada.

**Y el problema no es el mes 14: es el mes 15.** Las mismas cuatro personas que construyeron pasan a operar salas de resolución, valorar premios, resolver alarmas con plazo de 24 horas y adjudicar controversias en 10 días. **Operar el alcance completo no cabe en cuatro personas**, y el corpus lo reconoce sin resolverlo.

## 3.4 · Catorce meses sin señal de mercado

El corpus es excelente y **no reduce ese riesgo un solo día**. Lo que sí lo reduciría está escrito como recomendación, sin fecha ni responsable.

# 4\. Condiciones del comité

| \#  | Condición                                         | Antes de                          |
| --- | ------------------------------------------------- | --------------------------------- |
| C-1 | **Dictamen L-01 encargado** con el Dossier        | Esta semana                       |
| C-2 | **F0 con fecha y responsable**: 20 conversaciones | Esta semana                       |
| C-3 | Modelo de costo unitario instrumentado            | Fijar precio del plan promocional |
| C-4 | Plan de contratación de operación                 | Mes 12                            |
| C-5 | Compromisos previos de organizadores ancla        | Mes 8                             |
| C-6 | Ensayo con dinero real completo                   | Primera venta al público          |

**C-1 y C-2 no cuestan ingeniería y son las de mayor valor por unidad de esfuerzo de todo el plan.**

# PARTE II · EQUIPO TÉCNICO DE IMPLEMENTACIÓN

Evaluación desde la posición de quien recibe estos documentos y debe cotizar, construir y entregar.

# 5\. Veredicto técnico

> **Aceptamos el encargo. La documentación es la mejor que hemos recibido, y hay tres huecos que debemos cerrar antes del sprint 1.**

| Criterio                                       | Valoración                        |
| ---------------------------------------------- | --------------------------------- |
| ¿Podemos cotizar sin ambigüedad?               | **Sí, con reserva en frontend**   |
| ¿Podemos arrancar el sprint 0?                 | **Sí, el lunes**                  |
| ¿El esquema es utilizable?                     | **Sí. Se ejecuta y está probado** |
| ¿Los contratos son suficientes?                | **No. Cubren la mitad**           |
| ¿Podemos construir la interfaz?                | **No todavía**                    |
| ¿Los criterios de aceptación son verificables? | **Sí**                            |
| Riesgo de retrabajo por especificación         | **Bajo**, salvo en frontend       |

# 6\. Lo que este equipo valora

## 6.1 · El esquema se ejecuta, y eso es infrecuente

**135 tablas, cero errores, 199 restricciones, 13 pruebas negativas superadas.**

Recibir un esquema que arranca es raro. Recibir uno cuyas restricciones han sido **probadas contra los casos que deben rechazar** no nos había pasado. La diferencia es concreta: normalmente descubrimos en el sprint 3 que una restricción compilaba y no protegía nada, y aquí eso ya ocurrió y se corrigió.

**Nos ahorra entre dos y tres sprints de descubrimiento.**

## 6.2 · Las reglas viven en el motor, no en el manual

199 restricciones y 5 disparadores hacen cumplir cosas que normalmente se dejan al código de aplicación: cuadre contable, techo de comisión, igualdad de probabilidad entre vías, mínimo de administradores, imposibilidad de que un plan otorgue participaciones.

**Eso reduce nuestra superficie de error**, y sobre todo reduce el riesgo de que un desarrollador nuevo rompa un invariante sin saber que existía.

## 6.3 · Los criterios de aceptación son comprobables

136 historias, **todas trazadas a una regla o un invariante verificable por prueba automatizada**. Cero reglas huérfanas.

Es la diferencia entre *“el sorteo debe ser justo”* y *“*`ck_commit_beacon_future` *rechaza una ronda anterior al compromiso”*. La segunda se prueba; la primera se discute.

## 6.4 · Sabemos dónde no usar asistencia de IA

261 SP marcados como zona sin generación asistida, con propiedad fija y revisión de segunda persona. **Que el cliente lo haya decidido nos evita esa conversación**, y coincidimos con las cinco zonas elegidas.

# 7\. Los tres huecos que bloquean

## 7.1 · Contratos incompletos — bloquea el sprint 4

|                                     |        |
| ----------------------------------- | ------ |
| Endpoints referenciados en L3 §11   | \~30   |
| Rutas en `libox_openapi_L3_V7.yaml` | **16** |

**Falta aproximadamente la mitad.** Y la regla `BR-03` del backlog exige que los contratos y tipos **se generen** desde el YAML: sin las rutas restantes no hay generación, ni pruebas de contrato, ni servidor simulado para el frontend.

Las que faltan no son marginales: alta de organizador, etapas de bienes registrables, controversias, cumplimiento, alarmas, configuración de mercado.

**Estimación para completarlo: 8 SP.** Es mecánico —el esquema y el catálogo de errores ya existen— pero **debe estar antes de que arranque el trabajo de cliente**.

## 7.2 · 41 superficies sin ficha — bloquea el frontend

|                                  |        |
| -------------------------------- | ------ |
| Superficies declaradas en el PRD | 62     |
| Con ficha en L4                  | **21** |
| **Sin especificar**              | **41** |

L4 V2 cubre las de mayor carga conductual y es explícito al respecto. **Para nosotros eso significa que no podemos cotizar el frontend con precisión.**

Los tokens, los 22 componentes y las reglas de zona reducen mucho la ambigüedad —podemos construir sin inventar estética—, pero **composición, jerarquía y estados de 41 pantallas siguen sin definir**.

**No es un defecto del documento:** depende del trabajo de diseño que el propio corpus declara pendiente, con 4 a 6 semanas y fuera de los 936 SP. **Es camino crítico y no está en el plan con fecha.**

Nuestra posición: **cotizamos frontend con banda de incertidumbre del ±30 %** hasta que existan las fichas, o cotizamos en firme cuando el diseño entre.

## 7.3 · Sin manual de operación — no bloquea construir, bloquea entregar

No existe procedimiento de recuperación ante desastre, objetivo de tiempo de restauración, rotación de claves de cifrado, ni plan de cese ordenado.

**Nos afecta en tres puntos concretos:**

No podemos dimensionar la infraestructura sin objetivo de recuperación. No podemos diseñar la estrategia de respaldo sin saber cuánta pérdida de datos es tolerable. **Y no podemos probar una restauración completa sin saber cómo debe comportarse la cadena de hashes de auditoría al restaurar.**

Ese último punto es serio: **un sistema con auditoría encadenada por hash y ledger inmutable tiene un procedimiento de restauración no trivial**, y nadie lo ha escrito.

**Estimación: 13 SP**, y proponemos escribirlo nosotros durante R3, con validación del comité.

# 8\. Observaciones técnicas

## 8.1 · Sobre la estimación

**936 SP a 32 por sprint asume velocidad constante desde el sprint 1.** En nuestra experiencia los tres primeros rinden entre el 50 % y el 70 % mientras el equipo absorbe el dominio — y este dominio es grande: 49 invariantes, 21 subroles, 5 regímenes económicos.

**Recomendamos planificar R0 a 20 SP por sprint** y ajustar con velocidad medida a partir del sprint 4. En la práctica añade uno o dos sprints al total.

## 8.2 · Sobre el factor de asistencia de IA

El factor por bloque nos parece bien calibrado, con una salvedad: **0,45 en esquema y migraciones es optimista**. Generar el DDL es transcripción, pero las migraciones reversibles, los datos semilla y las pruebas de migración no lo son. **Sugerimos 0,55.**

En el resto coincidimos, y especialmente en el 1,00 del motor de sorteo.

## 8.3 · Sobre la capacidad concurrente

Los objetivos de §32.4 —500 sorteos activos, 50 órdenes por segundo— **son razonables y no están validados**. Con instancia única particionada el techo hay que medirlo.

**Solicitamos que la prueba de carga se adelante a R2**, no R6. Descubrir en el sprint 26 que el diseño no sostiene el pico de un sorteo relámpago sería caro.

## 8.4 · Lo que agradecemos y no es habitual

La **Guía de Extensión** nos dice dónde tocar cada cosa y qué nivel de cambio implica. La **Matriz de Casos de Uso** responde permisos y plazos sin abrir cinco documentos. El **verificador de coherencia** nos permite integrar cambios documentales sin miedo a que el corpus divergja.

**Los tres son artefactos que normalmente construimos nosotros durante los primeros dos meses.** Aquí ya existen.

# 9\. Condiciones del equipo técnico

| \#  | Condición                                  | Antes de               |
| --- | ------------------------------------------ | ---------------------- |
| T-1 | `openapi.yaml` **completo**, \~30 rutas    | Sprint 4               |
| T-2 | **Fichas de las 41 superficies restantes** | Sprint de frontend, R1 |
| T-3 | Manual de operación, que podemos redactar  | Fin de R3              |
| T-4 | Prueba de carga adelantada a R2            | R2                     |
| T-5 | Velocidad de R0 planificada al 60 %        | Sprint 1               |
| T-6 | Acceso a un entorno de proveedor de pagos  | Sprint 8               |

**T-1 y T-2 son las únicas que bloquean.** El resto es ajuste de plan.

# 10\. Conclusión conjunta

**El comité y el equipo técnico coinciden en el diagnóstico y difieren en el énfasis**, que es como debe ser.

|                    | Principal preocupación                                                                                                            |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| **Comité**         | El riesgo legal y la hipótesis de precio sin validar. **Puede construirse algo excelente que nadie compre o que no pueda operar** |
| **Equipo técnico** | Contratos y superficies incompletos. **Puede cotizarse mal algo que sí se puede construir**                                       |

**Ambos coinciden en que la base técnica es sólida y que la construcción puede empezar.**

Y ambos señalan la misma asimetría: **la calidad de la preparación documental es muy superior a la de la validación de mercado.** Se han escrito 743.000 caracteres y no se ha tenido una sola conversación con un organizador real.

**Eso es corregible en dos semanas y no cuesta ingeniería.** Es, con diferencia, la acción de mayor retorno pendiente.

*Evaluación de línea base. Comité fundador y equipo técnico de implementación, sobre métricas medidas del corpus vigente.*
