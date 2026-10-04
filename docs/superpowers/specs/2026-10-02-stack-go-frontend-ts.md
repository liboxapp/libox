---
title: Decisión de stack — Go y frontend TypeScript
status: aprobado
tags: [r0, c1, stack, decisiones]
updated: 2026-10-04
description: Decisión final de Diego sobre los lenguajes y alcance pendiente de adaptación de C1.
---

# Decisión de stack — Go y frontend TypeScript

El 2026-10-02 Diego indicó: «mi decision final sera Go + frontend TS para el
stack de desarrollo». Esta instrucción sustituye la elección previa de
TypeScript para el backend registrada el 2026-09-29. No equivale a una emisión
canónica ni a una actualización del doc 20 de Outline.
El análisis de adaptación D-10 se conserva en la [ficha R0](2026-10-02-r0-backend-go-design.md);
las ratificaciones del 04/10 se registran aquí y en su registro C1 enlazado abajo.

## Alcance aprobado

- Backend en **Go**, conservando el monolito modular como arquitectura de partida.
- Frontend en **TypeScript**, conservando Next.js como framework previamente elegido.
- PostgreSQL y compatibilidad con Supabase se mantienen como requisitos.
- API RESTful descrita con OpenAPI y documentación interactiva con Scalar,
  reafirmado por Diego. Los importes siguen
  viajando como cadenas de enteros en unidad mínima, con moneda explícita.
- **Autenticación administrada ratificada el 2026-10-04:** Supabase Auth gestiona
  la identidad; Go valida la identidad y aplica permisos de Libox. La aclaración
  del 02/10 había dejado la recomendación sin ratificar; el punto 4 del
  [registro del 04/10](c1-l3-v8/decisiones-2026-10-04.md) aporta la aprobación posterior.
- La frontera de datos Auth/KMS, sesiones, MFA y revocación sigue pendiente;
  esta decisión no aprueba una excepción de cifrado para los atributos de Auth.
- Mercado Pago y evaluación prioritaria de Truora conservan su elección.
- Se mantiene el techo de infraestructura de US$250/mes; el cambio no acredita
  que una nueva configuración de despliegue cumpla ese presupuesto.

## Adaptación requerida antes de emitir C2

1. Actualizar el candidato L3, programa R0 y plan C1: el dominio y la API pasan
   a Go; los supuestos anteriores sobre endpoints Next.js dejan de ser objetivo.
2. Elegir y validar runtime, despliegue y conectividad de Go con PostgreSQL y
   Supabase Auth. Vercel queda elegido también para el backend el 04/10;
   modalidad, conectividad y límites requieren validación, sin contratación implícita.
3. Conservar Trigger.dev y evaluar su funcionalidad durante los primeros meses,
   según Diego el 04/10. Cerrar su frontera con Go, coste y evidencia de uso;
   no implica mover reglas de negocio a TypeScript ni elegir un reemplazo.
4. Definir tipos internos de dinero, rangos, desbordamientos y serialización Go
   sin cambiar el formato JSON aprobado. Ningún entero de tamaño fijo garantiza
   por sí mismo ausencia de desbordamientos.
5. Preparar comprobaciones de compilación, análisis y pruebas Go, manteniendo las
   pruebas contractuales, SQL y del cliente TypeScript. Los resultados anteriores
   no acreditan un backend Go implementado ni probado.
6. Recalcular operación y costes con el despliegue y ejecutor elegidos, incluido
   el alcance Supabase/KMS aún pendiente, antes de cerrar proveedores para C2.

El candidato L3 y los planes existentes conservan referencias anteriores a
TypeScript: quedan identificados como pendientes de adaptación mediante esta
nota. No se hace una sustitución textual global que altere evidencia histórica,
el frontend, los clientes generados o los bloques protegidos.

## Controles vigentes

C1 continúa abierto y el producto permanece congelado hasta D1. El canon de
`docs/linea-base/` se preserva. Las zonas críticas siguen siendo implementación
humana cualquiera que sea el lenguaje; la revisión humana obligatoria del
desarrollo sigue suspendida hasta reactivación explícita de Diego.

Esta nota registra la decisión y sus consecuencias; no implementa Go, no elige
un framework HTTP, ORM o sistema de workflows, y no cierra la integración Auth/KMS, T1 o P-C.
