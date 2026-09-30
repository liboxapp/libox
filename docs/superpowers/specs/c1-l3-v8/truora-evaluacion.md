---
title: C1 — evaluación prioritaria de Truora
status: borrador
tags: [r0, c1, truora, kyc, kyb]
updated: 2026-09-30
description: Cobertura documentada, brechas de KYB y plan de prueba sin contratación ni datos reales.
---

# Evaluación de Truora

Diego priorizó Truora el 2026-09-30. Estado: **candidato para evaluación**, no
proveedor contratado ni adaptador validado. Mercado Pago es una elección separada.
Las [alternativas](identidad-proveedores.md) quedan disponibles si la cobertura o
el costo no encajan. No se ha contactado al proveedor ni transmitido datos de personas.

## Hallazgos verificables

| Área | Evidencia oficial | Conclusión para Libox |
|---|---|---|
| DNI peruano | Configuración admite `pe_national-id-2005`, `2013`, `2020` y `2025` | Cobertura documental publicada; falta probar documentos sintéticos/autorizados del proveedor |
| Extranjería | `pe_foreign-card-2019` y `2022` | Cobertura publicada, sin asumir otros formatos |
| Pasaporte | Validación con país `ALL` | Comprobar reglas de nacionalidad y residencia que necesita Libox |
| Integración | Creación y consulta de validaciones por API, estados y callbacks | Puede encajar tras un adaptador; no se ha ejecutado |
| Empresas peruanas | La referencia de Checks lista `company` como N/A para PE | No dar KYB Perú por cubierto con Checks estándar; confirmar producto/flujo alternativo por escrito |
| Precio | Sin tarifa pública suficiente para el alcance de Libox | Cotización necesaria; fuera de US$250 de infraestructura |

Fuentes: [versiones de documentos](https://dev.truora.com/guides/config_document/),
[API documental](https://dev.truora.com/guides/document_validation_api/),
[referencia Checks](https://dev.truora.com/docs/) y [productos](https://www.truora.com/).
La referencia Checks se consultó mediante el índice oficial del buscador; su
apertura directa falló. Reconfirmar esa limitación con la referencia vigente y
el proveedor; no equivale a decir que Truora carezca de cualquier solución KYB.

La validación documental admite imágenes JPEG/JPG/PNG hasta 30 MB; PDF corresponde
a facturas de México, no a DNI peruano. Por tanto, los límites de subida del
adaptador deberán diferenciar documento de identidad y evidencias generales.
[Formatos publicados](https://dev.truora.com/guides/document_validation_api/).

## Propuesta de integración

- Usar un flujo alojado del proveedor si satisface captura, consentimiento y
  accesibilidad; confirmar primero la modalidad contratada. Mantener las claves
  en servidor y referencias opacas en la API de Libox.
- Crear una sesión vinculada al usuario o cliente y al propósito. El usuario
  no puede adjuntar una validación de otra cuenta para elevar sus permisos.
- El callback notifica; el servidor consulta el resultado por API autenticada.
  Definir autenticación del callback con la guía del producto contratado: no
  inventar un header o reutilizar la firma de Mercado Pago.
- Separar fallo de identidad de error técnico, expiración y revisión pendiente.
  Una caída del proveedor no debe registrar falsamente a una persona como rechazada.
- Guardar solo los atributos necesarios, resultado y referencia de evidencia.
  DNI, imágenes y biometría no aparecen en logs ni respuestas públicas; HMAC
  versionado para correlación de documento conforme la propuesta de seguridad.
- KYB debe identificar empresa, representante y beneficiarios. El OCR de un DNI
  o una consulta de RUC no sustituye esas comprobaciones.

Es diseño de Libox. No demuestra una garantía comercial ni legal del proveedor.
[Eventos y variables](https://dev.truora.com/guides/webhook_events_and_variables/)
publica estados, razones y tipos; falta validar el mecanismo concreto de autenticación.

## Solicitud de información preparada, sin enviar

> Somos Libox, un marketplace de sorteos digitales con boleto pagado en Perú.
> Evaluamos KYC de personas y KYB de organizadores. Necesitamos confirmar:
>
> 1. Aceptación de nuestro caso de uso y productos exactos ofrecidos.
> 2. Cobertura peruana de DNI/extranjería, prueba de vida, fuentes oficiales y
>    revisión manual, indicando qué controles son opcionales.
> 3. KYB para RUC peruano: existencia, representante/poderes, propietarios y
>    beneficiarios finales. Indicar cobertura automática y documental/manual.
> 4. Precio para 100 y 500 personas/mes y 10 y 50 empresas/mes, mínimos, reintentos,
>    consultas adicionales, conservación y costos de sandbox.
> 5. Acceso a pruebas con datos sintéticos y guía vigente de callbacks autenticados,
>    reintentos, consulta de resultados y límites de API.
> 6. Exportación/borrado de evidencias, retención, región, subencargados y DPA.

Volúmenes de cotización ilustrativos, no pronóstico comercial ni compromiso.
Consentimiento, retención y transferencias internacionales: `[LEGAL→ABOGADO]`.

## Prueba de aceptación preparada

| Caso | Resultado esperado de Libox |
|---|---|
| DNI admitido + prueba de vida satisfactoria | Resultado vinculado a sesión propia; permisos según política del producto |
| Documento ilegible, vencido o rostro discordante | Motivo normalizado sin datos sensibles; reintento según política |
| Timeout o proveedor caído | Pendiente/error recuperable, sin falso rechazo definitivo |
| Callback falso o sesión de otro usuario | Sin cambio de estado ni elevación de permisos |
| Callback duplicado o anterior | Sin regresión ni efectos duplicados |
| Empresa PE con representante y beneficiarios | Evidencia completa de cada componente; no aprobar con solo RUC |
| Exportación y eliminación | Trazabilidad y retención acordadas, sin secretos en logs |

No ejecutadas: falta acceso de prueba, alcance de KYB y acuerdo técnico. C1 conserva
un contrato neutral; una selección comercial no convierte estos casos en pruebas verdes.
