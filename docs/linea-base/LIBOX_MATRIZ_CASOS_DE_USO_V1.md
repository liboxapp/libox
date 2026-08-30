# Índice de contenidos

# 0\. Propósito y método

**Documento:** LIBOX\_MATRIZ\_CASOS\_DE\_USO\_V1 **Versión:** V1 **Nivel:** L3 — artefacto de referencia **Deriva de:** PRD MVP V9 (L2) · Especificación Técnica L3 V7 (L3) **Gobernado por:** LBPF V3 **Estado:** vigente

## 0.1 Qué responde

Una sola pregunta, para cualquier punto del sistema: **quién puede hacer qué, cuándo, con qué requisito y en qué plazo.**

**Este documento no crea reglas.** Todo caso de uso deriva de una regla `RN`, un invariante `INV` o una incompatibilidad `INC` ya vigentes. Si algo no está en el PRD o en L3, **es un hueco que se cierra allí primero**, no aquí.

## 0.2 Por qué se ordena por proceso y no por rol

Una matriz de rol por acción con 21 subroles y más de cien acciones sería una tabla de dos mil celdas que nadie consulta. **La pregunta real nunca es *qué puede hacer un SUPPORT\_L2*, sino *quién atesta una entrega y qué necesita*.**

Por eso el cuerpo se ordena en doce procesos, y las tres matrices transversales de §14 quedan al final como referencia de consulta.

## 0.3 Convenciones

| Símbolo | Significado                                               |
| ------- | --------------------------------------------------------- |
| **A**   | Actúa: ejecuta la acción                                  |
| **V**   | Ve: consulta sin mutar                                    |
| **E**   | Escala: informa y deriva, no ejecuta                      |
| **2F**  | Exige segunda firma de otra persona natural y otro subrol |
| **M**   | Exige motivo registrado                                   |
| **—**   | Sin acceso                                                |

**Plazos.** Todos se cuentan desde un evento de sistema con sello de servidor, nunca desde una fecha declarada por una parte (RN-87). Zona horaria del mercado de la oportunidad.

# 1\. Proceso · Alta y acreditación de organizador

| \#   | Paso                                      | Quién actúa                    | Requisito                                                                        | Plazo                                                        | Produce                                               |
| ---- | ----------------------------------------- | ------------------------------ | -------------------------------------------------------------------------------- | ------------------------------------------------------------ | ----------------------------------------------------- |
| 1.1  | Crear cuenta de organizador               | Usuario verificado             | Identidad verificada con prueba de vida                                          | —                                                            | `clients` en estado pendiente                         |
| 1.2  | Declarar régimen: jurídica o natural      | `CLIENT_OWNER`                 | Jurídica exige identificador tributario y giro; natural exige titular verificado | —                                                            | Régimen fijado (RN-03-bis)                            |
| 1.3  | Cargar acreditación                       | `CLIENT_OWNER`                 | Documentos por régimen                                                           | —                                                            | Expediente                                            |
| 1.4  | Verificar acreditación                    | `ADMIN_LEGAL_COMPLIANCE` **M** | Verificación externa cuando exista                                               | 5 días hábiles                                               | Aprobación o rechazo motivado                         |
| 1.5  | Registrar datos de cobro                  | `CLIENT_OWNER` únicamente      | Titularidad coincidente con la acreditación                                      | —                                                            | Cuenta pendiente de verificación                      |
| 1.6  | Verificar datos de cobro                  | `ADMIN_FINANCE`                | Coincidencia de titular                                                          | 3 días hábiles                                               | Cuenta verificada                                     |
| 1.7  | **Cambiar datos de cobro**                | `CLIENT_OWNER` únicamente      | Reverificación de identidad                                                      | **Congelamiento de liquidaciones 48 h** con aviso al titular | RN-04                                                 |
| 1.8  | Alta de subusuarios                       | `CLIENT_OWNER`                 | Máximo 10 en jurídica; **prohibido en natural**                                  | —                                                            | RN-03-ter                                             |
| 1.9  | Habilitar capacidades de tipo y categoría | `ADMIN_RISK` **M**             | Reputación mínima según capacidad                                                | —                                                            | `client_capabilities`                                 |
| 1.10 | Marcar como parte relacionada             | `ADMIN_SUPER` **M**            | —                                                                                | —                                                            | INV-39: **trato idéntico**, marca solo para auditoría |

**RN-04 es el vector de fraude por toma de cuenta más frecuente en marketplaces.** El congelamiento de 48 horas con aviso al titular existe porque un atacante que cambia la cuenta de destino cobra antes de que nadie lo note.

# 2\. Proceso · Creación y aprobación de oportunidad

| \#   | Paso                              | Quién actúa                             | Requisito                                                                                     | Plazo          | Produce                                                   |
| ---- | --------------------------------- | --------------------------------------- | --------------------------------------------------------------------------------------------- | -------------- | --------------------------------------------------------- |
| 2.1  | Crear borrador                    | `CLIENT_MANAGER`                        | Capacidad de tipo habilitada en las tres capas                                                | —              | Estado `DRAFT`                                            |
| 2.2  | Declarar régimen económico        | `CLIENT_MANAGER`                        | Pagado, entrada gratuita o promocional                                                        | —              | Determina todo el resto del flujo                         |
| 2.3  | Declarar categoría de premio      | `CLIENT_MANAGER`                        | Habilitada en el mercado. **Registrables prohibidas sin recaudación** salvo custodia (INV-44) | —              | Checklist de evidencia                                    |
| 2.4  | Simular pricing                   | `CLIENT_MANAGER`                        | Solo régimen pagado                                                                           | —              | Múltiplo, neto y **plazo máximo estimado hasta el cobro** |
| 2.5  | Declarar ruta ante no reclamo     | `CLIENT_MANAGER`                        | **Inmutable tras publicar** (INV-24)                                                          | —              | Publicada en bases                                        |
| 2.6  | Proponer plazo de entrega         | `CLIENT_MANAGER`                        | Mayor al base, nunca menor, con justificación                                                 | —              | RN-89                                                     |
| 2.7  | Enviar a revisión                 | `CLIENT_MANAGER`                        | Evidencia de premio completa                                                                  | —              | `PENDING_VALUATION`                                       |
| 2.8  | Rechazo automático por desviación | Sistema                                 | Desviación superior al 50 %                                                                   | Inmediato      | **No anulable**                                           |
| 2.9  | Rechazo automático por múltiplo   | Sistema                                 | Bajo 1,25×                                                                                    | Inmediato      | INV-40                                                    |
| 2.10 | Aprobar múltiplo sobre 4,0×       | `ADMIN_SUPER` **2F M**                  | —                                                                                             | —              | INV-41                                                    |
| 2.11 | Gate legal                        | `ADMIN_LEGAL_COMPLIANCE` **M**          | Según `gate_scope` del mercado                                                                | 3 días hábiles | `PENDING_APPROVAL`                                        |
| 2.12 | Aprobar o rechazar                | `ADMIN_MODERATION` **M**                | Política de contenido                                                                         | 2 días hábiles | `SCHEDULED` o `ACTIVE`                                    |
| 2.13 | Congelar bases                    | Sistema                                 | Al publicar                                                                                   | Inmediato      | INV-14: inmutables                                        |
| 2.14 | Pausar oportunidad                | `ADMIN_RISK` o `ADMIN_COMPLIANCE` **M** | —                                                                                             | —              | `PAUSED`, cesan las ventas                                |

**El paso 2.2 es el que ramifica todo.** El régimen económico determina si hay escrow, si hay liquidación, si aplican los seis gates y qué categorías de premio son admisibles.

# 3\. Proceso · Verificación de valor del premio

| \#  | Paso                      | Quién actúa                          | Requisito                                                | Plazo          | Produce                                       |
| --- | ------------------------- | ------------------------------------ | -------------------------------------------------------- | -------------- | --------------------------------------------- |
| 3.1 | Cargar evidencia          | `CLIENT_MANAGER` o `CLIENT_OPERATOR` | Checklist cerrado por categoría. **Sin campo otros**     | —              | `prize_valuation_documents`                   |
| 3.2 | Generar código del día    | Sistema                              | Vigencia 72 h                                            | —              | Debe aparecer en imágenes y video             |
| 3.3 | Verificación externa      | Sistema                              | Comprobante, identificador de equipo, consulta registral | —              | Resultado con hash                            |
| 3.4 | Cálculo de desviación     | Sistema                              | Mediana de referencias con antigüedad válida             | Inmediato      | Banda de decisión                             |
| 3.5 | Aprobar banda V1 y V2     | `SUPPORT_VALUATOR` **M**             | V2 con visto de `ADMIN_MODERATION`                       | 3 días hábiles | Valor aprobado                                |
| 3.6 | Aprobar banda V3          | `ADMIN_LEGAL_COMPLIANCE` **M**       | Tasación o certificación                                 | 5 días hábiles | Valor aprobado                                |
| 3.7 | Aprobar banda V4          | `ADMIN_LEGAL_COMPLIANCE` **2F M**    | Verificación registral cuando aplique                    | 7 días hábiles | Valor aprobado                                |
| 3.8 | Excepción a la desviación | Aprobador **2F M**                   | Motivo de 50 caracteres mínimo                           | —              | `valuation_exceptions`, con reporte periódico |
| 3.9 | Observar                  | Verificador **M**                    | —                                                        | —              | Devuelve al organizador                       |

| Restricción                                                 | Regla  |
| ----------------------------------------------------------- | ------ |
| Quien valoró **no atesta** la entrega de esa oportunidad    | INC-06 |
| Ningún nivel de reputación exime de este proceso            | INV-28 |
| Ningún rol con aprobación de valor tiene métrica de volumen | INC-10 |

**INC-10 neutraliza el conflicto de interés estructural:** LIBOX cobra un porcentaje de la recaudación, y la recaudación se dimensiona sobre el valor del premio. Quien aprueba valores no puede ser medido por cuántos aprueba.

# 4\. Proceso · Bienes registrables, siete etapas

Solo régimen pagado. Prohibido sin recaudación salvo custodia efectiva (INV-44).

| \#  | Etapa                          | Quién aprueba                                            | Requisito                                                               | Rechazo automático                         |
| --- | ------------------------------ | -------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------ |
| 4.1 | **E1 Elegibilidad**            | `ADMIN_RISK` **M**                                       | Capacidad habilitada, KYB vigente, **reputación N2 o superior**         | Reputación insuficiente                    |
| 4.2 | **E2 Titularidad**             | `ADMIN_LEGAL_COMPLIANCE` **M**                           | Copia literal con antigüedad ≤ 7 días **por consulta directa de LIBOX** | Cualquier gravamen o litigio inscrito      |
| 4.3 | **E3 Valoración**              | `ADMIN_LEGAL_COMPLIANCE` **2F M**                        | Tasación obligatoria en inmuebles                                       | Desviación superior al 50 %                |
| 4.4 | **E4 Instrumento y bloqueo**   | `ADMIN_LEGAL_COMPLIANCE` **M**                           | Plantilla única versionada y bloqueo registral vigente                  | Bloqueo ausente o insuficiente             |
| 4.5 | **E5 Publicación**             | —                                                        | **Reconsulta registral cada 7 días**                                    | Gravamen sobrevenido: suspensión inmediata |
| 4.6 | **E6 Preparación del ganador** | `SUPPORT_L2` verifica; `ADMIN_LEGAL_COMPLIANCE` habilita | Estado civil, capacidad, **aceptación informada de cargas**             | Rechazo del premio o falta de condiciones  |
| 4.7 | **E7 Transferencia**           | `ADMIN_LEGAL_COMPLIANCE` **2F M**                        | Inscripción verificada **por consulta directa**                         | Observación no subsanable                  |

| \#    | Regla mecánica                                                                               |
| ----- | -------------------------------------------------------------------------------------------- |
| RN-30 | La consulta registral la hace LIBOX. **El documento de una parte nunca es fuente de verdad** |
| RN-31 | La aprobación es una casilla, no una opinión. **No existe aprobar con observaciones**        |
| RN-32 | Motivo de 100 caracteres mínimo en toda aprobación de etapa                                  |
| RN-33 | **Sin avance parcial**, sin excepción por reputación                                         |
| RN-28 | El organizador **acepta el pago como acto propio y firmado** tras la inscripción             |

**RN-27 es la etapa que hace viable todo lo demás.** Entre la verificación del go-live y la inscripción pasan semanas: sin bloqueo registral vigente durante toda la venta, la partida limpia que se verificó es una fotografía caducada.

# 5\. Proceso · Venta y emisión

| \#  | Paso                              | Quién actúa           | Requisito                                                                                                    | Plazo                           | Produce                                         |
| --- | --------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------- | ----------------------------------------------- |
| 5.1 | Comprar tickets                   | `USER_VERIFIED`       | Clave de idempotencia por intento                                                                            | Reserva con vigencia de mercado | `orders`                                        |
| 5.2 | Validación en orden               | Sistema               | Autoexclusión → identidad → tramo → autocompra → concentración → límite propio → importe mínimo → inventario | Inmediato                       | Error tipificado o reserva                      |
| 5.3 | Reserva de inventario             | Sistema               | Actualización atómica condicional                                                                            | Inmediato                       | **Nunca sobreventa**                            |
| 5.4 | Confirmar pago                    | Proveedor vía webhook | Firma válida, sin repetición, estado monótono                                                                | —                               | `PAID`                                          |
| 5.5 | Emitir tickets                    | Sistema               | Misma transacción que los asientos                                                                           | Inmediato                       | Números correlativos. **Anulado no se recicla** |
| 5.6 | Participar gratis                 | `USER_REGISTERED`     | Código de campaña con cupo, **una por persona**                                                              | Hasta agotar cupo               | `free_entry_grants`                             |
| 5.7 | Ampliar cupo                      | `ADMIN_SUPER` **M**   | Solo antes de ejecutar                                                                                       | —                               | **Notificación a los ya inscritos**             |
| 5.8 | Recuperar estado tras desconexión | Sistema               | —                                                                                                            | Inmediato                       | Estado inequívoco, nunca ambiguo                |

**El paso 5.2 va de prohibición absoluta a disponibilidad** para que el mensaje al usuario sea el más informativo posible. Decirle *no quedan tickets* a alguien autoexcluido sería inútil y confuso.

# 6\. Proceso · Sorteo y verificación

| \#  | Paso                         | Quién actúa                       | Requisito                                                                         | Plazo                                   | Produce                    |
| --- | ---------------------------- | --------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------- | -------------------------- |
| 6.1 | Alcanzar condición de sorteo | Sistema                           | Según tipo                                                                        | —                                       | `READY_TO_DRAW`            |
| 6.2 | Congelar pool                | Sistema                           | Al menos un ticket válido                                                         | —                                       | `POOL_FROZEN`              |
| 6.3 | Publicar compromiso          | Sistema                           | Hash de semilla, **ronda de baliza futura anunciada** con su propiedad intrínseca | Antes de ejecutar                       | Verificable por terceros   |
| 6.4 | Ejecutar                     | Sistema                           | Ventana operativa abierta y baliza disponible                                     | Diferido si fuera de ventana            | `DRAW_EXECUTED`            |
| 6.5 | Revelar y generar prueba     | Sistema                           | —                                                                                 | Inmediato                               | Página pública indexable   |
| 6.6 | Verificar                    | **Cualquiera, sin autenticación** | Consulta a la **fuente de baliza**, fuera de LIBOX                                | —                                       | Confirmación independiente |
| 6.7 | Autorizar re-sorteo          | `ADMIN_SUPER` **M**               | Solo por plazo de reclamo vencido. **Máximo uno**                                 | Compromiso nuevo con 24 h de antelación | Cadena visible             |

| \#         | Restricción                                                                                  |
| ---------- | -------------------------------------------------------------------------------------------- |
| INV-19     | Un sorteo ejecutado **no se re-ejecuta**. La garantía es de base de datos                    |
| INV-18-bis | La anterioridad de la baliza es comprobable **contra la fuente**, no contra un dato de LIBOX |
| RN-68      | La prueba **no divulga** identidad de participantes ni concentración                         |
| RN-69      | **Ningún rol adelanta ni retrasa el congelamiento.** Es automático                           |

**Nadie —ni** `ADMIN_SUPER`**— puede alterar un resultado.** Es la única familia de acciones sin actor humano en toda la matriz, y es deliberado.

# 7\. Proceso · Resolución y entrega

| \#   | Paso                      | Quién actúa                                                                                | Requisito                                                                  | Plazo                                      | Produce                                    |
| ---- | ------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- | ------------------------------------------ | ------------------------------------------ |
| 7.1  | Abrir sala                | Sistema                                                                                    | Al ejecutarse el sorteo                                                    | Inmediato                                  | Sala con el código de la oportunidad       |
| 7.2  | Asignar agente            | Sistema                                                                                    | Carga equilibrada, prioridad por valor y plazo                             | —                                          | Un asignado; el resto **ve la cola**       |
| 7.3  | Reclamar premio           | `USER_WINNER`                                                                              | —                                                                          | **7, 15 o 30 días** según valor aprobado   | `CLAIMED`                                  |
| 7.4  | Incorporar al organizador | Sistema                                                                                    | **Solo tras el reclamo y con consentimiento** de compartir datos           | Inmediato                                  | RN-73                                      |
| 7.5  | Cotizar envío             | `CLIENT_OPERATOR`                                                                          | Mínimo dos transportistas formales                                         | —                                          | Opciones                                   |
| 7.6  | Elegir y pagar envío      | `USER_WINNER`                                                                              | A su cargo, ya declarado antes de comprar                                  | 7 días + 7 de gracia                       | O `SHIPPING_ABANDONED`                     |
| 7.7  | Aportar evidencia         | `CLIENT_OPERATOR` o `USER_WINNER`                                                          | Hash, antivirus, tipo validado                                             | Plazo de categoría                         | Clasificada por fuerza                     |
| 7.8  | **Atestar entrega**       | `SUPPORT_L2` **M**                                                                         | Evidencia suficiente. **En registrables:** `ADMIN_LEGAL_COMPLIANCE` **2F** | —                                          | Alimenta gate G2                           |
| 7.9  | Pedir más evidencia       | `SUPPORT_L2` **M**                                                                         | —                                                                          | Pausa hasta 5 días                         | `NEEDS_MORE_EVIDENCE`                      |
| 7.10 | Extender plazo            | `SUPPORT_L2` hasta 10 días · `SUPPORT_SUPERVISOR` hasta 20 más · `ADMIN` **2F** por encima | Motivo                                                                     | **Notificación a todos los participantes** | `sla_extensions`                           |
| 7.11 | Revertir atestación       | `SUPPORT_SUPERVISOR` **M**                                                                 | —                                                                          | —                                          | Congela liquidación                        |
| 7.12 | Exportar paquete forense  | `ADMIN`                                                                                    | —                                                                          | —                                          | Documento firmado con manifiesto de hashes |
| 7.13 | Congelar reloj por rebote | Sistema                                                                                    | Todos los canales rebotan                                                  | —                                          | Escala a SUPPORT antes de vencer           |

| \#     | Restricción                                                                    |
| ------ | ------------------------------------------------------------------------------ |
| INV-07 | **SUPPORT atesta un hecho. No mueve dinero, ledger ni ganador**                |
| INV-20 | Solo `SUPPORT_L2`, `SUPPORT_SUPERVISOR` y `ADMIN` cambian el estado de la sala |
| RN-75  | **Solo agregación.** Nadie edita ni elimina, ni siquiera `ADMIN_SUPER`         |
| RN-82  | Datos de contraparte minimizados: nombre e inicial                             |
| RN-93  | Contacto externo dentro de la sala se **bloquea** con evento de riesgo         |
| RN-94  | Mención de pago entre partes **congela el caso** y escala a `ADMIN_RISK`       |

**RN-94 protege en las dos direcciones a la vez:** contra la extorsión del ganador y contra la colusión entre organizador y ganador. Es el mismo control para dos riesgos opuestos.

# 8\. Proceso · Controversias

| \#  | Paso                         | Quién actúa                    | Requisito                                                 | Plazo                             | Produce                          |
| --- | ---------------------------- | ------------------------------ | --------------------------------------------------------- | --------------------------------- | -------------------------------- |
| 8.1 | Abrir reclamo                | `USER_WINNER` o `CLIENT`       | **Motivo de lista cerrada y evidencia obligatoria**       | —                                 | `disputes`                       |
| 8.2 | Clasificar evidencia         | Sistema                        | Fuerte, media o débil                                     | Inmediato                         | Determina la carga               |
| 8.3 | Escalar por evidencia fuerte | Sistema                        | El organizador aporta evidencia fuerte y el ganador niega | Inmediato                         | **Carga se traslada al ganador** |
| 8.4 | Adjudicar                    | `ADMIN_LEGAL_COMPLIANCE` **M** | Motivo de 100 caracteres mínimo                           | **10 días** desde el escalamiento | Resolución escrita               |
| 8.5 | Notificar                    | Sistema                        | Lenguaje llano y no adversarial                           | Inmediato                         | Ambas partes                     |
| 8.6 | Aplicar reputación           | Sistema                        | Según parte de mala fe                                    | —                                 | **Bidireccional**                |

| \#     | Restricción                                                                        |
| ------ | ---------------------------------------------------------------------------------- |
| INV-22 | **Ningún caso se resuelve por afirmación de una sola parte, en ninguna dirección** |
| INC-08 | Quien adjudica **no atestó** ese caso                                              |
| RN-91  | Sin evidencia fuerte ni media del organizador, prevalece la posición del ganador   |

**La reputación bidireccional es lo que desactiva la extorsión.** Sin ella, el organizador tiene historial y consecuencias y el reclamante no tiene nada que perder — y esa asimetría es lo que hace rentable reclamar en falso.

# 9\. Proceso · Liquidación

Solo régimen pagado. **No aplica al régimen promocional** (INV-43).

| \#  | Paso                     | Quién actúa              | Requisito                             | Plazo     | Produce                        |
| --- | ------------------------ | ------------------------ | ------------------------------------- | --------- | ------------------------------ |
| 9.1 | Devengar                 | Sistema                  | Al confirmarse cada pago              | Inmediato | `ACCRUED`                      |
| 9.2 | Evaluar los seis gates   | Sistema                  | **Determinista, sin criterio humano** | 15 min    | `ELIGIBLE` o `HELD` con motivo |
| 9.3 | Retener por contracargo  | Sistema                  | Ventana de mercado                    | —         | Reserva                        |
| 9.4 | Ejecutar pago en lote    | `ADMIN_FINANCE`          | Cobro verificado y sin congelamiento  | —         | `PAID`                         |
| 9.5 | Ejecutar en registrables | `ADMIN_FINANCE` **2F M** | Caso por caso                         | —         | `PAID`                         |
| 9.6 | Liberar reserva          | Sistema                  | Ventana extendida vencida             | —         | Pago del saldo                 |
| 9.7 | Ajuste de ledger         | `ADMIN_FINANCE` **2F M** | Motivo obligatorio                    | —         | T-14                           |

**Los seis gates:** sorteo con prueba válida · entrega atestada · sin controversias abiertas · ventana de retención cumplida · cobro verificado · ledger cuadrado.

| \#     | Restricción                                                                 |
| ------ | --------------------------------------------------------------------------- |
| INV-23 | **Ninguna liquidación alcanza pagada sin los seis.** Impuesto en el esquema |
| INV-21 | **Ningún rol completa solo la cadena que termina en desembolso**            |
| INC-07 | `ADMIN_FINANCE` **no atesta entregas** en ningún caso                       |
| RN-102 | El estado retenido **siempre con motivo y fecha estimada**                  |

**RN-102 evita el conflicto más frecuente con el organizador:** un estado retenido sin explicación se interpreta como retención indebida.

# 10\. Proceso · Cumplimiento financiero

| \#   | Paso                          | Quién actúa              | Requisito                                                         | Plazo     | Produce                                                  |
| ---- | ----------------------------- | ------------------------ | ----------------------------------------------------------------- | --------- | -------------------------------------------------------- |
| 10.1 | Acumular gasto                | Sistema                  | Día, mes, año y total, por usuario **y por organizador receptor** | Continuo  | Acumuladores                                             |
| 10.2 | Exigir acreditación por tramo | Sistema                  | **Antes de emitir tickets**, no después                           | Inmediato | Bloqueo con mensaje neutro                               |
| 10.3 | Aprobar sobre umbral          | `ADMIN_COMPLIANCE` **M** | Debida diligencia reforzada                                       | 48 h      | Autorización o rechazo                                   |
| 10.4 | Abrir expediente              | `ADMIN_COMPLIANCE`       | —                                                                 | —         | Inmutable, retención prolongada                          |
| 10.5 | **Documentar la no-decisión** | `ADMIN_COMPLIANCE` **M** | Obligatorio también al concluir que no hay problema               | —         | RN-144                                                   |
| 10.6 | Congelar cuenta               | `ADMIN_RISK` **M**       | —                                                                 | —         | **No impide reclamar, reembolsar ni disponer del saldo** |

| \#     | Restricción                                                                                       |
| ------ | ------------------------------------------------------------------------------------------------- |
| RN-142 | **Ningún texto revela análisis ni reporte.** La comunicación es funcional y neutra                |
| RN-143 | La reserva cubre el análisis, **no** el requerimiento documental ni los derechos sobre los fondos |
| INC-03 | `ADMIN_COMPLIANCE` **no toca dinero**                                                             |
| INC-04 | `ADMIN_COMPLIANCE` **no aprueba** las oportunidades que vigila                                    |

**RN-144 es lo que una auditoría pregunta.** No pregunta qué se reportó: pregunta **qué se revisó y por qué se decidió no reportar**.

# 11\. Proceso · Protección del usuario

| \#   | Paso                                 | Quién actúa     | Requisito                             | Plazo                                         |
| ---- | ------------------------------------ | --------------- | ------------------------------------- | --------------------------------------------- |
| 11.1 | Fijar o reducir límite propio        | `USER_VERIFIED` | —                                     | **Inmediato**                                 |
| 11.2 | Aumentar límite propio               | `USER_VERIFIED` | —                                     | **24 h de espera**                            |
| 11.3 | Autoexcluirse                        | `USER_VERIFIED` | Sin fricción, sin retención comercial | **Inmediato e irreversible** durante el plazo |
| 11.4 | Consultar panel de gasto             | `USER_VERIFIED` | —                                     | Fuera del proceso de compra                   |
| 11.5 | Reclamar premio estando autoexcluido | `USER_WINNER`   | —                                     | **Permitido siempre**                         |
| 11.6 | Retirar saldo de reembolso           | `USER_VERIFIED` | Solicitud manual con verificación     | —                                             |

**La asimetría de 11.1 y 11.2 es el núcleo del control.** Sin ella, el límite se eleva en el momento del impulso y la herramienta no protege nada.

**Ningún rol interno puede levantar una autoexclusión antes de su plazo.** No hay fila para esa acción en toda la matriz.

# 12\. Proceso · Administración de plataforma

| \#    | Paso                                | Quién actúa                                    | Requisito                                                                      |
| ----- | ----------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------ |
| 12.1  | Apagar tipo **a un cliente**        | `SUPPORT_SUPERVISOR` o `ADMIN_RISK` **M**      | —                                                                              |
| 12.2  | Apagar tipo **en un mercado**       | `ADMIN_SUPER` **M**                            | **Notificación a afectados**                                                   |
| 12.3  | Apagar tipo **en la plataforma**    | `ADMIN_SUPER` **2F M**                         | Notificación y registro                                                        |
| 12.4  | Suspender mercado en cuatro niveles | `ADMIN_SUPER` **2F M**                         | Aviso con qué sigue operando                                                   |
| 12.5  | Definir ventana operativa           | `ADMIN_LEGAL_COMPLIANCE` **M**                 | Se publica en bases                                                            |
| 12.6  | Cambiar configuración de mercado    | `ADMIN_LEGAL_COMPLIANCE` **M**                 | Versionada con vigencia                                                        |
| 12.7  | Crear cuenta interna                | Según techo de privilegio                      | Correo corporativo, identidad verificada, multifactor, aceptación registrada   |
| 12.8  | Otorgar subrol que toca dinero      | `ADMIN_SUPER` **2F M**                         | —                                                                              |
| 12.9  | Crear `SUPPORT_L1`                  | `SUPPORT_SUPERVISOR` **M**                     | **Único caso de delegación**                                                   |
| 12.10 | **Suspender cuenta interna**        | Cualquier `ADMIN` o `SUPPORT_SUPERVISOR` **M** | **Inmediato.** No elimina ni altera privilegios                                |
| 12.11 | Restaurar cuenta suspendida         | `ADMIN_SUPER` **M**                            | —                                                                              |
| 12.12 | Revocar `ADMIN_SUPER`               | `ADMIN_SUPER` **M**                            | **Bloqueado si quedaría solo uno** (INV-38)                                    |
| 12.13 | Alta de auditor externo             | `ADMIN_SUPER` **M**                            | Solo lectura, **vigencia obligatoria**, incompatible con todo subrol operativo |
| 12.14 | Resolver alarma                     | Dueño nominal **M**                            | **Motivo obligatorio también si no hay problema**                              |

**La asimetría de 12.10 frente a 12.11 es deliberada.** Conceder acceso indebido es un riesgo que se materializa con el tiempo; **mantener acceso indebido es un riesgo que se materializa ahora.**

## 12.1 Regla de vuelo al apagar

| Motivo                             | Oportunidades vivas                                             |
| ---------------------------------- | --------------------------------------------------------------- |
| Comercial, regulatorio o de riesgo | **Terminan normalmente.** Solo se bloquean publicaciones nuevas |
| **Defecto del mecanismo**          | **Se congelan antes de ejecutar**                               |

**Ningún apagado, en ningún nivel, impide reclamar un premio, recibir un reembolso o disponer del saldo** (INV-33).

# 13\. Paneles por subrol

| Subrol                       | Ve                                                        | Actúa sobre                                                    | Escala a                 |
| ---------------------------- | --------------------------------------------------------- | -------------------------------------------------------------- | ------------------------ |
| `SUPPORT_L1`                 | Cola de salas, línea de tiempo por traza                  | Responder, pedir evidencia                                     | `SUPPORT_L2`             |
| `SUPPORT_L2`                 | Lo anterior más su sala asignada                          | **Atestar**, extender hasta 10 días                            | `SUPPORT_SUPERVISOR`     |
| `SUPPORT_VALUATOR`           | Cola de valoración V1 y V2                                | Aprobar valor                                                  | `ADMIN_LEGAL_COMPLIANCE` |
| `SUPPORT_SUPERVISOR`         | Cola completa, plazos, capacidades por cliente            | Reasignar, revertir, **crear** `SUPPORT_L1`, suspender cuentas | `ADMIN`                  |
| `SUPPORT_BEHAVIORAL_ANALYST` | Indicadores conductuales                                  | **Nada.** Solo prepara expediente                              | `ADMIN_BEHAVIORAL`       |
| `ADMIN_MODERATION`           | Cola de aprobación                                        | Aprobar o rechazar oportunidades                               | `ADMIN_SUPER`            |
| `ADMIN_RISK`                 | Alarmas de riesgo, capacidades, cuentas                   | Capacidades, congelar, apagar por cliente                      | `ADMIN_SUPER`            |
| `ADMIN_FINANCE`              | Liquidaciones, conciliación, ledger                       | Ejecutar pagos, ajustes con 2F                                 | `ADMIN_SUPER`            |
| `ADMIN_LEGAL_COMPLIANCE`     | Gate legal, valoración alta, controversias, configuración | Adjudicar, aprobar etapas, cambiar configuración               | `ADMIN_SUPER`            |
| `ADMIN_COMPLIANCE`           | Expedientes, acumuladores, tramos                         | Aprobar sobre umbral, decidir expedientes                      | `ADMIN_SUPER`            |
| `ADMIN_BEHAVIORAL`           | Indicadores y encuestas                                   | **Veto** sobre funcionalidad que rompa guardarraíl             | —                        |
| `ADMIN_SUPER`                | Todo                                                      | Configuración, apagados globales, cuentas, segunda firma       | —                        |
| `AUDITOR_EXTERNAL`           | **Solo lectura, con vigencia**                            | Nada                                                           | —                        |

**Cada panel muestra el estado de cada función** —activa, apagada por plataforma, por mercado o por cliente— **y si el subrol puede actuar o solo escalar**. Un panel por subrol produciría trece superficies que se desincronizan; es una vista, no un producto distinto.

# 14\. Matrices transversales

## 14.1 Acciones que exigen segunda firma

Valoración de premio banda V4 · excepción a la regla de desviación · múltiplo sobre 4,0× · etapas E3 y E7 de registrables · atestación en registrables · liquidación de registrables · ajuste de ledger · excepción de tasa · apagado global de una capacidad · suspensión de mercado · otorgamiento de subrol que toca dinero.

**Criterio: cuanto más ancho el efecto o más cerca del dinero, más manos.**

## 14.2 Acciones sin actor humano

Congelamiento del pool · publicación del compromiso · ejecución del sorteo · generación de la prueba · asignación de número de ticket · evaluación de los seis gates · cálculo de desviación · rechazo automático por desviación o por múltiplo bajo · reconsulta registral periódica · devengo contable.

**Ninguna admite intervención, ni siquiera de** `ADMIN_SUPER`**.** Es lo que hace verificable el sistema.

## 14.3 Acciones que ningún rol puede realizar

| Acción                                           | Protegida por          |
| ------------------------------------------------ | ---------------------- |
| Alterar el resultado de un sorteo ejecutado      | INV-19                 |
| Editar o eliminar un mensaje de sala             | RN-75                  |
| Editar una línea contable                        | Revocación de permisos |
| Levantar una autoexclusión antes de plazo        | RN-128                 |
| Impedir reclamar premio, reembolso o saldo       | **INV-33**             |
| Modificar las bases tras la publicación          | INV-14                 |
| Reasignar un número de ticket anulado            | INV-11                 |
| Otorgarse un subrol a sí mismo                   | RN-05-ter              |
| Revocar al último `ADMIN_SUPER`                  | INV-38                 |
| Crear un plan de suscripción con participaciones | INV-46                 |

**Esta última tabla es la más importante del documento.** Define el perímetro de lo imposible, y todo lo imposible está impuesto en el esquema o en un disparador — **no en un procedimiento que alguien deba recordar.**

# 15\. Plazos, en una tabla

| Proceso                            | Plazo                           | Fuente   |
| ---------------------------------- | ------------------------------- | -------- |
| Verificación de acreditación       | 5 días hábiles                  | §1.4     |
| Verificación de datos de cobro     | 3 días hábiles                  | §1.6     |
| Congelamiento tras cambio bancario | **48 h**                        | RN-04    |
| Gate legal                         | 3 días hábiles                  | §2.11    |
| Aprobación de oportunidad          | 2 días hábiles                  | §2.12    |
| Valoración V1 y V2                 | 3 días hábiles                  | §3.5     |
| Valoración V3                      | 5 días hábiles                  | §3.6     |
| Valoración V4                      | 7 días hábiles                  | §3.7     |
| **Reclamo de premio**              | **7, 15 o 30 días** según valor | RN-107   |
| Elección y pago de envío           | 7 días + 7 de gracia            | RN-84    |
| Entrega P-A y P-B                  | 20 días                         | §6.1 PRD |
| Entrega P-C1                       | 45 días hábiles                 | §6.1 PRD |
| Entrega P-C2                       | 90 días hábiles                 | §6.1 PRD |
| Entrega P-D                        | 30 días                         | §6.1 PRD |
| Entrega P-E                        | 7 días                          | §6.1 PRD |
| Pausa por evidencia                | Máximo 5 días acumulados        | RN-87    |
| Adjudicación de controversia       | **10 días**                     | RN-97    |
| Retención de liquidación           | Ventana de mercado              | RN-103   |
| Aprobación sobre umbral            | 48 h                            | §10.3    |
| Alarma de severidad alta           | **24 h**                        | RN-170   |
| Alarma de severidad media          | 48 h                            | RN-170   |
| Subsanación registral              | 30 días, prorrogables 30        | §8.6 PRD |
| Aumento de límite propio           | **24 h**                        | RN-133   |

*Matriz de Casos de Uso, Permisos y SLA V1. Artefacto de nivel L3. Deriva íntegramente de PRD MVP V9 y Especificación Técnica L3 V7: no crea reglas, las ordena para consulta operativa.*
