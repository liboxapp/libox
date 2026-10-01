---
title: C1 — baliza ratificada y aceptación del verificador
status: borrador
tags: [r0, c1, sorteo, baliza]
updated: 2026-10-01
description: drand quicknet ratificado como fuente (D1) y requisitos para el aporte humano de H-10 a H-12, sin implementar el motor ni calcular vectores.
---

# Baliza ratificada y entrega humana

Diego ratificó el 2026-09-30 **drand quicknet** como fuente pública de
aleatoriedad ([D1](decisiones-c1-configuracion.md#d1-fuente-de-aleatoriedad-pública)).
La ratificación elige la fuente; no es una implementación del motor ni cierra
H-10, H-11 o H-12. Las restricciones de
[zonas sin IA](../../../../.claude/rules/zonas-sin-ia.md) se mantienen: este documento
especifica aceptación y dependencias, sin generar verificador ni vectores esperados.

## Fuente ratificada

La documentación oficial describe quicknet como red principal con período de
3 segundos y modo no encadenado, identificada por el hash:

`52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971`

Fijar identidad de cadena y clave pública de confianza en la configuración
versionada; no confiar solo en el nombre `quicknet` o en HTTPS. El protocolo
asocia cada ronda a un instante y permite verificar su firma.
[API oficial](https://docs.drand.love/developer/API-v2/drand-http-api/),
[protocolo](https://docs.drand.love/docs/specification/),
[consideraciones de seguridad](https://docs.drand.love/blog/2023/10/16/quicknet-is-live/).

No se ha consultado una ronda para declarar un sorteo válido, comprobado la firma
con una implementación ni calculado ganadores. Antes de implementar falta elegir
una biblioteca compatible con el esquema de firma concreto, con licencia y
mantenimiento comprobados. El SDK genérico de otra cadena no se presume compatible.
El candidato L3 recoge la fuente en §5.8 y deja esos datos en DP-04.

## Contrato que debe cerrar el dueño del motor

| Dato | Significado que debe conservar el diseño final |
|---|---|
| Cadena | Identidad inmutable del beacon y parámetros de confianza versionados |
| Ronda | Identificador de la ronda anunciada antes de conocer su aleatoriedad |
| Instante | Tiempo programado de esa ronda según parámetros de cadena, no tiempo de descarga |
| Aleatoriedad | Valor autenticado de esa ronda; distinto de su identificador |
| Firma | Evidencia verificable contra la clave pública fijada |
| Obtención | Marca operativa de descarga; no demuestra que la ronda fuese futura |

El defecto H-11 compara conceptos diferentes. La aceptación debe comprobar por
separado identidad de cadena, ronda anunciada, instante futuro respecto al
compromiso y aleatoriedad autenticada. No aceptar coincidencia de strings como
sustituto de verificación de firma ni aceptar `latest` como selección de ronda.
La codificación final de cada campo y la interfaz exacta de `verify_draw` las
entrega el dueño humano en el artefacto de motor correspondiente.

## Caída y reanudación

La [política de seguridad propuesta](seguridad.md) conserva compromiso, pool y ronda
ante indisponibilidad. Un relay alternativo puede servir la **misma cadena y ronda**;
no es permiso para cambiar de fuente, sortear con otra ronda o regenerar semilla.
Acotar la espera automática, registrar incidente y reanudar la misma operación al
recuperar evidencia válida. La propuesta existente alerta a los 5 minutos y escala a incidente a los 30;
la resolución de una indisponibilidad prolongada queda sujeta a decisión.
Nunca convertir la caída del beacon en un resultado ficticio de sorteo.

## Entrega mínima pendiente de H-10–H-12

La ratificación de la fuente no cambia esta lista: los vectores siguen pendientes.
Diego es el dueño actual. Debe entregar:

1. Especificación inequívoca e implementación humana del verificador, con la
   serialización exacta, versión de algoritmo y parámetros de cadena fijados.
2. Valores esperados independientes de los cinco vectores del corpus: compromiso,
   pool, derivación y ganadores donde corresponda; procedencia del cálculo.
3. Esquema y acceso a semilla cifrada que permitan restaurar el compromiso sin
   revelarla antes de tiempo. Un backup de DB sin la clave no acredita recuperación.
4. Casos negativos: firma falsa, cadena/ronda distintas, ronda no futura, pool
   alterado, semilla incorrecta y resultado distinto. Casos de caída y reanudación.

C1 necesita artefactos y resultados esperados; R1 ejecuta la integración contra
servicios reales. Ningún ejemplo sintético de OpenAPI cierra estos hallazgos.
La suspensión de revisión humana no elimina esta propiedad de implementación.
