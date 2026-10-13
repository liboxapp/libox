---
title: C1 — aceptación técnica del backend Go
status: borrador
tags: [r0, c1, aceptacion, go, render, pruebas]
updated: 2026-10-12
description: Casos de aceptación de arquitectura Go, alojamiento en Render, semilla, privilegios, ledger y revisión; definidos y pendientes de ejecución.
---

# Aceptación técnica del backend Go

Deriva de la [decisión D-10](../2026-10-02-r0-backend-go-design.md), de las
[decisiones técnicas del 04/10](decisiones-tecnicas-2026-10-04.md) (D-14, D-16,
D-17) y de las [decisiones del 12/10](decisiones-2026-10-12.md) (Render y PostgreSQL 17).
**Estado de todos los casos: definido, pendiente de ejecutar.** Esta ficha
especifica resultados observables; no entrega código, SQL crítico ni pruebas
automatizadas de esas zonas. Diego conserva la implementación humana.

El SQL de H-04/H-07/H-09 se verifica en C1 al recibir sus aportes humanos.
La integración Go, los proveedores y la recuperación se prueban en D1/R1.
La validación contable sigue D-05: puede estar pendiente en C1/C2 y debe
cerrarse antes de dinero real. Se conservan F1–F7 y la
[aceptación Cowork](reconciliacion-aceptacion.md).

## Arquitectura y trabajos — D-10

| Caso | Resultado exigido | Evidencia de cierre |
|---|---|---|
| GO-01 · API y worker | Backend en Go; procesos separados consumen los mismos módulos de dominio sin duplicar reglas. Next.js/TypeScript consume el contrato | Compilación de ambos ejecutables, mapa de módulos y prueba de contrato contra la API Go |
| GO-02 · persistencia | Commit de dominio y trabajo pendiente/outbox son atómicos; rollback no deja trabajo huérfano | PostgreSQL real, inspección de registros y fallo inyectado antes/después del commit |
| GO-03 · caída y repetición | Caída tras commit y antes de despacho conserva el trabajo; reentrega y dos ejecutores simultáneos producen un solo efecto | Reinicios y concurrencia reales; estado persistido, auditoría y conteo de efectos. Incluye F3/F6 |
| GO-04 · calendario y plazos | Los 30 trabajos conservan su cadencia con el ejecutor que se fije; outbox cada 10 s, objetivo <60 s normal y alarma >5 min. Reintentos respetan deadline; siguen operativos sin ventas | Medición con carga y sin compras, reloj controlado y casos de reintento agotado |
| GO-05 · importes | Go mantiene importes exactos compatibles con `BIGINT`; JSON usa cadenas decimales. Se rechaza overflow y no se usa punto flotante | Límites válidos/inválidos y contrato `Money`; TypeScript conserva `bigint` donde opere con importes |

El outbox no confía en memoria ni en una llamada HTTP como prueba de persistencia.
La ejecución única patrimonial se verifica en PostgreSQL y el PSP real/sandbox;
ninguna promesa del proveedor sustituye esos invariantes. Quién ejecuta cada
trabajo (worker Go o Trigger.dev) sigue la frontera pendiente de HOST-05.

## Render y Trigger.dev — validaciones del 12/10

Render está elegido para alojar API y worker. Estos casos concretan las
validaciones previas a habilitarlo; si alguno falla, la respuesta corresponde
a Diego y esta ficha no la anticipa.

| Caso | Resultado exigido | Evidencia de cierre |
|---|---|---|
| HOST-01 · despliegue | API y worker como servicios separados de una misma imagen; reiniciar, actualizar o detener uno conserva tareas y reanuda desde PostgreSQL. Orden entre migraciones (`libox_deployer`) y publicación, reversión y entornos separados | Ensayo en Render con parada ordenada, interrupción abrupta y convivencia de versiones durante un despliegue |
| HOST-02 · región y PostgreSQL | Región de Render que cumple la exigencia de región de §0.3 del [candidato L3](LIBOX_ESPECIFICACION_TECNICA_L3_V8_DRAFT.md) respecto de Supabase; TLS, credenciales por componente y pool acotado; conexión directa o pooler en modo sesión si el ejecutor usa LISTEN/NOTIFY. Carga y reconexión no agotan conexiones | Región seleccionada, latencias medidas, presupuesto de conexiones (API, worker, Supabase, migraciones, despliegues) y prueba con Supabase gestionado |
| HOST-03 · secretos | Ubicación confirmada en Render de los secretos de `libox_api` y `libox_worker`, con rotación de 90 días; credencial AWS exclusiva y rotada para KMS. La API no obtiene la clave de la semilla; el worker la usa sin exponerla en logs, respuestas o imágenes | Inventario de permisos, denegación desde la API, ensayo de rotación y revisión de telemetría/artefactos |
| HOST-04 · costo y capacidad | Costo integral bajo el techo de US$250/mes, con objetivo de US$215 antes de impuestos y alertas: Render (API y worker), Vercel Pro, Trigger.dev, Supabase/PITR, KMS, copias, correo, límites, observabilidad, tráfico y tributos/margen | Tarifas verificadas al decidir, tamaños/consumo medidos y escenarios normal/pico/reintentos/sin ventas |
| HOST-05 · frontera con Trigger.dev | Trigger.dev se conserva y se evalúa en los primeros meses (punto 2 del 04/10). La frontera con el worker Go queda definida sin duplicar lógica de dominio ni perder estado | Funcionalidades, fiabilidad, carga de mantenimiento y costo con evidencia de uso; integración con Go y ensayo de reintento/recuperación documentados |

Los logs de la plataforma no sustituyen la auditoría de negocio aprobada el 04/10.
Los escenarios antiguos de [proveedores](proveedores.md) no prueban el costo del
backend Go. Pagos, KYC, SMS y asesoría conservan su presupuesto separado.
No se contratan servicios al redactar esta ficha.

## Semilla y recuperación — D-14

| Caso | Resultado exigido | Evidencia de cierre |
|---|---|---|
| SEED-01 · persistencia | Semilla cifrada autenticada y versión de clave persistidas antes del compromiso; DB y sus copias no contienen semilla ni clave en claro | Inspección autorizada de registros/copias y denegación de descifrado sin clave |
| SEED-02 · reanudación | Reinicio conserva semilla, hash del compromiso, pool congelado y ronda; obtiene el mismo resultado bajo los vectores independientes | Ensayo con implementación humana, fixture de baliza y comparación de identidades antes/después |
| SEED-03 · clave ausente o incorrecta | Se pausa y alerta; no genera semilla, compromiso, pool o ronda sustitutos; no altera fondos ni revela plaintext | Fallos de acceso y autenticación del cifrado, más evidencia de ausencia de mutaciones |
| SEED-04 · restauración | Recuperar datos y clave por canales separados permite reanudar el mismo sorteo; claves antiguas necesarias siguen recuperables | Procedimiento con responsables/permisos y ensayo aislado sin imprimir secretos |

Los vectores no se calculan desde el código bajo prueba. El algoritmo y la
serialización siguen pendientes del dueño humano del motor.

## Privilegios y firmas — D-16

| Caso | Resultado exigido | Evidencia de cierre |
|---|---|---|
| ADMIN-01 · mínimo | De tres administradores activos se puede pasar a dos con autorización; pasar de dos a uno se rechaza por revocación, suspensión o borrado | PostgreSQL real y llamadas al servicio Go; sin vía directa con credencial aplicativa que eluda el control |
| ADMIN-02 · concurrencia | Dos operaciones simultáneas que reducirían el total bajo dos no pueden confirmar ambas | Transacciones concurrentes con barrera; al finalizar quedan al menos dos activos y no hay mutación parcial |
| ADMIN-03 · reactivación | Reactivar equivale a nuevo otorgamiento; exige matriz, incompatibilidades y segundas firmas aplicables | Casos admitidos/denegados; autor, cofirmante independiente y permisos efectivos registrados |
| ADMIN-04 · auditoría | Go concentra permisos, firmas y auditoría; rechazo no deja privilegios ni firmas parcialmente aplicados | Eventos de solicitud/resultado trazables y prueba de rollback; acceso interno refleja revocación |

Se conserva bootstrap con dos personas y las firmas por `action_code` ya
aprobadas. Identidades sintéticas sirven para pruebas, no para operar.

## Cierre técnico y contable — D-17

| Caso | Resultado exigido | Evidencia de cierre |
|---|---|---|
| LEDGER-01 · cuenta/moneda | Toda línea referencia cuenta existente y moneda coherente con cuenta/asiento; cuenta inexistente o moneda distinta se rechazan | Migración completa y pruebas negativas sobre PostgreSQL real, con roles efectivos |
| LEDGER-02 · período cerrado | Un período cerrado rechaza asientos nuevos y líneas tardías; cierre e inserción concurrentes no permiten escribir después del cierre | Casos secuenciales/concurrentes, límites temporales y transacciones reales |
| LEDGER-03 · atomicidad/cuadre | Asiento desbalanceado o línea inválida revierte el conjunto; no se altera el saldo ni se omite el control por otro rol | Contraejemplos y ausencia de efectos parciales; conserva requisitos H-04 |
| LEDGER-04 · validación contable | El contador valida modelo, cuentas y transacciones canónicas; H-01–H-03 y política de devolución/reconocimiento tienen resolución trazable | Dictamen y modelo aprobado aparte del resultado técnico [LEGAL→ABOGADO] donde corresponda |

Mantener dos registros de cierre, técnico y contable, con evidencia y responsable.
Antes de dinero real se exigen ambos, junto con custodia ASS-001 y los demás
gates de R1. Un verde técnico no acredita aprobación del modelo contable.

## Revisión del código — D-22

D-22 coincide con la [suspensión vigente](../../../../.claude/rules/revision-humana.md)
de la revisión humana obligatoria.

| Caso | Resultado exigido | Evidencia de cierre |
|---|---|---|
| REVIEW-01 · integración | CI, pruebas y revisión automatizada obligatorios; CI Go para backend y TypeScript para frontend al habilitar D1 | Ejecución de checks del cambio y revisión automatizada trazable |
| REVIEW-02 · suspensión | No se exige segundo revisor mientras Diego mantenga la suspensión; zonas críticas conservan implementación humana | Política vigente y procedencia humana del código crítico; reactivación solo por instrucción explícita |
| REVIEW-03 · producto | Suspensión de revisión del código no elimina segundas firmas ni controles de privilegios operativos | ADMIN-01–04 y pruebas de firmas por acción |

Cerrar un caso exige su evidencia; esta ficha no marca ninguno como pasado.
