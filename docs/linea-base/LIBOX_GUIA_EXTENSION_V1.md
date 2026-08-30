# Índice de contenidos

# 0\. Propósito

**Documento:** LIBOX\_GUIA\_EXTENSION\_V1 **Versión:** V1 **Nivel:** L3 — artefacto de referencia **Deriva de:** PRD MVP V9 · Especificación Técnica L3 V7 **Estado:** vigente

## 0.1 Qué responde

**Quiero cambiar X. ¿Dónde se toca, y qué cuesta?**

LIBOX está construido para que la mayoría de los cambios sean **datos y no código**. Esa propiedad es inútil si nadie sabe dónde está el dato. Este documento es el mapa.

## 0.2 Los cuatro niveles de cambio

| Nivel                  | Qué es                                                            | Quién lo hace                                   | ¿Despliegue?   |
| ---------------------- | ----------------------------------------------------------------- | ----------------------------------------------- | -------------- |
| **N1 · Configuración** | Un valor en la configuración del mercado o en una tabla de reglas | `ADMIN_LEGAL_COMPLIANCE` o el subrol competente | **No**         |
| **N2 · Datos semilla** | Una fila nueva en una tabla de catálogo                           | Migración                                       | Sí, sin código |
| **N3 · Adaptador**     | Implementar una interfaz existente                                | Ingeniería                                      | Sí             |
| **N4 · Dominio**       | Nueva entidad, estado o regla de negocio                          | Ingeniería, tras modificar L2                   | Sí             |

**Regla de oro:** si un cambio que debería ser N1 resulta ser N3 o N4, **es un defecto de diseño**, no una limitación aceptable. Se registra y se corrige.

# 1\. Mapa de cambios por función

## 1.1 Reglas de negocio y umbrales

Todo lo siguiente es **N1**. Vive en `market_config` con vigencia por fechas, y **una oportunidad se rige por la versión vigente el día de su publicación** (INV-15).

| Quiero cambiar                       | Dónde                                | Nota                                         |
| ------------------------------------ | ------------------------------------ | -------------------------------------------- |
| Tasa base de comisión                | `fee_schedule.base_fee_bp`           | El techo del 20 % está en el esquema         |
| Tramos de la escala E0–E4            | `fee_schedule.levels`                | Umbrales calibrables                         |
| **Suelo y techo de recaudación**     | `collection_multiple`                | 1,25× y 4,0× por defecto                     |
| Bandas de valoración V1–V4           | `valuation_bands`                    |                                              |
| Regla de desviación                  | `valuation_deviation`                | El rechazo sobre 50 % no es anulable         |
| Plazos de reclamo por tramo          | `deadlines.claim_by_value`           | 7, 15 y 30 días                              |
| Plazos de entrega por categoría      | `deadlines.delivery_by_category`     |                                              |
| Ventana de retención y reserva       | `deadlines`, `settlement.reserve_bp` |                                              |
| Tramos de acreditación financiera    | `aml.tiers`                          |                                              |
| Umbral de concentración              | `concentration.max_bp`               | 30 % por defecto                             |
| Importe mínimo de compra             | `purchase.min_order_amount`          |                                              |
| Rango de precio de ticket            | `purchase.ticket_price_min/max`      |                                              |
| Vigencia de reserva                  | `purchase.reservation_ttl_minutes`   |                                              |
| Impuesto: nombre, tasa y base        | `tax`                                | La fórmula de extracción no cambia           |
| Múltiplo de redondeo del pricing     | `currency.rounding_multiple`         | **Depende de la moneda**                     |
| Parámetros por tipo de sorteo        | `raffle_type_params`                 | Duración de T5, hitos de T4, ediciones de T7 |
| Umbrales de indicadores conductuales | `behavioral.kpi_thresholds`          |                                              |
| Tasa de muestreo de encuesta         | `behavioral.survey_sampling_mode`    |                                              |
| Feriados                             | `holidays_calendar`                  |                                              |
| Zona horaria                         | `markets.timezone`                   |                                              |

## 1.2 Encendido y apagado

**N1 en todos los casos.** Jerarquía de tres capas, **la más restrictiva gana** (INV-45).

| Alcance                        | Dónde                                            | Quién                               |
| ------------------------------ | ------------------------------------------------ | ----------------------------------- |
| Toda la plataforma             | `platform_capabilities`                          | `ADMIN_SUPER` **con segunda firma** |
| Un mercado                     | `market_config.raffle_types`, `prize_categories` | `ADMIN_SUPER`                       |
| Un cliente                     | `client_capabilities`                            | `SUPPORT_SUPERVISOR` o `ADMIN_RISK` |
| Ventana horaria de una función | `operating_windows`                              | `ADMIN_LEGAL_COMPLIANCE`            |
| LIBOX Club                     | `benefits_plan.enabled`                          | `ADMIN_SUPER`, con criterio doble   |

Toda conmutación deja rastro en `feature_toggle_log` con actor, alcance, motivo y afectados.

## 1.3 Catálogos ampliables

| Quiero añadir              | Nivel  | Dónde                                                                    | Condición                                                                          |
| -------------------------- | ------ | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| **Un tipo de sorteo**      | **N2** | Fila en `raffle_type_rules`                                              | **Solo si su disparo encaja en la FSM única.** Si exige un estado nuevo, pasa a N4 |
| Un subrol                  | **N2** | Filas en `subroles`, `subrole_grant_matrix`, `subrole_incompatibilities` | Debe declarar su techo de otorgamiento                                             |
| Una categoría de premio    | **N4** | Requiere régimen de acreditación y evidencia de entrega                  | Toca L2                                                                            |
| Una regla de riesgo        | **N1** | Fila en `risk_rules`                                                     | Las reglas son datos, no código                                                    |
| Una fuerza probatoria      | **N2** | Fila en `evidence_strength_rules`                                        |                                                                                    |
| Un instrumento de encuesta | **N2** | Fila en `survey_instruments`                                             |                                                                                    |
| Un aliado o beneficio      | **N1** | `partners`, `benefits`                                                   | Nunca descuento sobre ticket                                                       |
| Una excepción de tasa      | **N1** | `fee_exceptions`                                                         | Categoría tipificada, con doble firma                                              |
| Un plan de suscripción     | **N2** | `subscription_plans`                                                     | **Jamás con participaciones** (INV-46)                                             |
| Un plan promocional        | **N1** | `promotional_plans`                                                      |                                                                                    |

**El caso del auditor externo** es el ejemplo de por qué esto importa: un subrol temporal de solo lectura, con vigencia y caducidad automática, es **tres filas**. No requiere código.

## 1.4 Proveedores externos

**N3.** La elección es dato; la integración es código.

| Interfaz                | Qué hace                                             | Cambiar de proveedor                                   |
| ----------------------- | ---------------------------------------------------- | ------------------------------------------------------ |
| `IIdentityVerifier`     | Documento y prueba de vida                           | Implementar adaptador; apuntar en `providers.identity` |
| `IPaymentProvider`      | Preferencia, cobro, webhook, reembolso, conciliación | Ídem en `providers.psp`                                |
| `IInvoiceIssuer`        | Comprobante                                          | Ídem                                                   |
| `IRegistryProvider`     | Consulta registral                                   | Ídem                                                   |
| `ITaxDocumentValidator` | Validación de comprobante de compra                  | Ídem                                                   |
| `IEntropyBeacon`        | Baliza pública por ronda                             | **Común a mercados**                                   |

**Ningún adaptador toca el dominio.** Si al añadir un proveedor hiciera falta modificar una entidad, el adaptador está mal diseñado.

## 1.5 Abrir un mercado nuevo

| Paso | Nivel   | Qué                                                      |
| ---- | ------- | -------------------------------------------------------- |
| 1    | Externo | **Dictámenes legales de esa jurisdicción**               |
| 2    | N3      | Adaptadores de identidad, pagos, comprobantes y registro |
| 3    | N2      | Fila en `markets` y calendario de feriados               |
| 4    | N1      | Versión de `market_config` completa, aprobada            |
| 5    | N1      | Categorías y tipos habilitados                           |
| 6    | —       | **Ensayo con dinero real en ese mercado**                |

**Lo que bloquea no es el paso 2 ni el 4: es el paso 1.** El código estará listo mucho antes que los permisos.

## 1.6 Interfaz de usuario

| Quiero cambiar                                   | Nivel  | Dónde                                               |
| ------------------------------------------------ | ------ | --------------------------------------------------- |
| Color, tipografía, espaciado, radios, movimiento | **N1** | `libox-design-tokens.json`                          |
| Textos de una superficie                         | **N1** | Manual de redacción de L4, servido desde el backend |
| Denominación de documento, etiquetas fiscales    | **N1** | `market_config`                                     |
| Un componente nuevo                              | N4     | L4 primero, luego código                            |
| Una superficie nueva                             | N4     | L2 declara, L4 especifica, luego código             |

**La interfaz no fija nada por jurisdicción: lo recibe del servidor** (INV-32). Y todo componente se prueba al 150 % de longitud de texto, porque una etiqueta de tres caracteres en un mercado puede tener veinte en el siguiente.

# 2\. Lo que NO es configurable, y es deliberado

| Elemento                                                                    | Por qué                                                                                                      |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Algoritmo del sorteo**                                                    | Cambiarlo invalidaría toda prueba anterior. Un cambio exige nueva `algorithm_version` y convivencia de ambas |
| **Serialización canónica del pool**                                         | Dos serializaciones distintas producen hashes distintos y rompen la verificación                             |
| **Igualdad de probabilidad entre vías**                                     | INV-42. Impuesto por restricción                                                                             |
| **Cuadre de partida doble**                                                 | Disparador diferido. Un asiento descuadrado aborta la transacción                                            |
| **Unicidad de documento, correo y teléfono**                                | Sostiene concentración, límites, autoexclusión y protección de menores                                       |
| **Las once incompatibilidades de subrol**                                   | Defensa contra fraude interno                                                                                |
| **Mínimo de dos** `ADMIN_SUPER`                                             | INV-38                                                                                                       |
| **Reclamar premio, reembolso, saldo, historial y autoexclusión**            | INV-33. **Ningún interruptor los apaga**                                                                     |
| **Inmutabilidad de ledger, auditoría, mensajes de sala y bases publicadas** | Permisos revocados a nivel de rol de base de datos                                                           |
| **Ningún plan otorga participaciones**                                      | INV-46. Columna que solo admite falso                                                                        |

**Esta lista es corta a propósito.** Todo lo demás debería ser N1 o N2, y si no lo es, hay un defecto que corregir.

# 3\. Fronteras del código

## 3.1 Los 23 agregados

Cada uno es propietario exclusivo de sus tablas. **Ningún módulo escribe en tablas de otro**: la comunicación es por evento en la bandeja de salida, y la compilación falla si hay dependencia de escritura cruzada.

**Consecuencia práctica:** para saber dónde vive una funcionalidad, basta identificar su agregado. La tabla de propiedad está en PRD §3.1.

## 3.2 Zonas de cuidado especial

Cinco zonas donde el cambio exige propiedad fija y revisión de una segunda persona:

| Zona                                             | Por qué                                            |
| ------------------------------------------------ | -------------------------------------------------- |
| Motor de sorteo y verificación                   | Un error silencioso invalida la tesis del producto |
| Asientos contables y transacciones canónicas     | Un desbalance se propaga a todo el histórico       |
| Concurrencia: inventario, saldo, ejecución única | Los errores solo aparecen bajo carga               |
| Incompatibilidades de subrol en ejecución        | Son la defensa contra fraude interno               |
| Cálculo de comisión, impuesto y múltiplo         | Afecta el neto de cada organizador                 |

**En estas cinco no se usa generación asistida de código.**

## 3.3 Preparación para la evolución

Ya construido en el MVP, y es lo que hace que la extracción futura sea un movimiento y no una reescritura:

Fronteras estrictas verificadas en compilación · bandeja de salida y comunicación por evento · adaptadores para todo proveedor externo · particionamiento desde la primera migración · trazabilidad extremo a extremo · autenticación por credencial portable, nunca solo por cookie · interfaz de programación agnóstica del cliente · tokens de diseño en formato portable.

**La extracción de servicios está gobernada por la regla de bloqueo del Enterprise V3**, no por esta guía: nada hasta 10.000 transacciones mensuales pagadas con ledger cuadrado, dos meses consecutivos.

# 4\. Antes de cambiar algo

Cinco preguntas, en orden:

1.  **¿En qué nivel cae?** Si crees que es N4, comprueba primero que no sea N1 mal ubicado.
2.  **¿Toca un invariante?** Si sí, no es un cambio: es una decisión que empieza en L2 o en L0.
3.  **¿Afecta a oportunidades ya publicadas?** La configuración se congela al publicar. Un cambio no las alcanza, y eso es intencional.
4.  **¿Requiere segunda firma?** Consulta §14.1 de la Matriz de Casos de Uso.
5.  **¿Deja rastro?** Todo cambio de configuración, capacidad o subrol se registra con actor y motivo.

**Si un cambio que parece de configuración exige tocar el dominio, escríbelo en el backlog de cambio.** Es la señal más útil que el equipo puede darle a este documento, y la que evita que la propiedad de extensibilidad se degrade sin que nadie lo note.

*Guía de Extensión y Puntos de Cambio V1. Artefacto de nivel L3. Deriva de PRD MVP V9 y Especificación Técnica L3 V7: no crea reglas, indica dónde vive cada una.*
