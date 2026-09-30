---
title: C1 — opciones de KYC y KYB para Perú
status: borrador
tags: [r0, c1, proveedores, identidad]
updated: 2026-09-30
description: Comparación de tres proveedores; Truora priorizado para evaluación por Diego y costos fuera de infraestructura.
---

# Opciones de KYC y KYB

Diego pidió opciones y el 2026-09-30 eligió **priorizar Truora para evaluación**.
No equivale a contratación ni a aceptación técnica definitiva.
KYC verifica personas; KYB verifica empresas, representantes y beneficiarios finales.
El presupuesto de US$250/mes cubre infraestructura; estos servicios se estiman aparte.
Precios consultados el 2026-09-30, en USD, sin impuestos ni cotización contractual.

| Opción | KYC publicado | KYB y límites | Encaje propuesto |
|---|---|---|---|
| Veriff | Essential: 0,80/verificación, mínimo 49/mes. Plus: 1,39, mínimo 99/mes | No asumir KYB incluido en estos planes; confirmar solución aparte | Plus para piloto de personas con revisión híbrida y menor mínimo |
| Sumsub | Basic: 1,35/verificación, mínimo 149/mes. Compliance: 1,85, mínimo 299/mes | Producto KYB para empresa, estructura y beneficiarios; requiere cotización específica | Alternativa si Truora no cubre el KYB requerido |
| Truora | Cotización; no se encontró tarifa pública suficiente | Confirmar cobertura peruana y alcance empresarial de la propuesta | Primera opción de evaluación por decisión de Diego |

Fuentes oficiales: [planes Veriff](https://www.veriff.com/plans/self-serve),
[precios Sumsub](https://sumsub.com/es/pricing/),
[KYB Sumsub](https://docs.sumsub.com/docs/business-verification),
[productos Truora](https://www.truora.com/).

Veriff Essential se orienta a menor riesgo; Plus añade revisión humana del proveedor.
Esto no reactiva la revisión humana de desarrollo suspendida por Diego.
PEP/sanciones en Veriff figura como adicional de 0,64 por verificación; no se incluye
silenciosamente en 1,39. [Detalle del plan](https://www.veriff.com/plans/self-serve).
Sumsub Basic no equivale a Compliance: este último anuncia AML y prueba de domicilio.
[Comparación oficial](https://sumsub.com/es/pricing/).

## Recomendación y costo ilustrativo

Evaluar primero **Truora**, por decisión de Diego, condicionado a cobertura y
cotización empresarial. Sumsub queda como alternativa de KYC/KYB conjunto y
Veriff Plus como alternativa de KYC con menor mínimo. No atribuir a Truora
verificación empresarial completa sin alcance contractual. No se ha contactado a ninguno.

Para 100 verificaciones mensuales de personas, sin extras:

| Plan | Cálculo ilustrativo | Total |
|---|---|---:|
| Veriff Plus | máximo entre 99 y 100 × 1,39 |139 |
| Sumsub Basic | máximo entre 149 y 100 × 1,35 |149 |
| Sumsub Compliance | máximo entre 299 y 100 × 1,85 |299 |

Estos planes no son equivalentes en controles. Los ejemplos no incluyen KYB,
reintentos facturables, consultas, conservación ampliada ni impuestos. Confirmar
la unidad facturada, compromisos, sobreconsumo y tratamiento de rechazos al cotizar.

## Evidencia para seleccionar el adaptador

- Documentos peruanos concretos y sus versiones: DNI, pasaporte y documentos
  admitidos para extranjeros; prueba de vida y tratamiento de reintentos.
- Para empresa: RUC, existencia/estado, representante y poderes, estructura de
  propiedad y beneficiarios finales; indicar qué viene de registro y qué de documentos.
- Una consulta de RUC no equivale por sí sola a KYB completo.
  [Explicación de Truora](https://blog.truora.com/es/c%C3%B3mo-validar-un-ruc-y-usarlo-para-un-onboarding-empresarial).
- Aceptación comercial del caso de uso de Libox, costos, tiempos y soporte.
- Sandbox, estados, autenticación y firma de callbacks, duplicados, reintentos,
  consulta de resultado y mecanismos de revisión/corrección.
- Exportación de evidencias, eliminación, retención, subencargados y ubicación de
  datos; consentimiento y transferencias internacionales `[LEGAL→ABOGADO]`.

El catálogo de [países de Veriff](https://www.veriff.com/es/paises-admitidos) incluye
Perú; eso no confirma por sí solo acceso a RENIEC, cobertura de cada documento ni KYB.
Ninguna elección de proveedor resuelve automáticamente las obligaciones legales de Libox.

## Alcance C1

C1 puede definir sesiones y resultados neutrales con proveedor pendiente. La
selección concreta determina el adaptador, payload y pruebas de sandbox. Los
resultados sintéticos de OpenAPI no demuestran identidad real ni autorización.
El [diseño de contratos](cierre-contratos-identidad-evidencias.md) mantiene separado
el resultado del proveedor de la decisión de acceso de Libox.

La [evaluación prioritaria de Truora](truora-evaluacion.md) detalla cobertura,
brechas empresariales, solicitud de información y casos de aceptación.
