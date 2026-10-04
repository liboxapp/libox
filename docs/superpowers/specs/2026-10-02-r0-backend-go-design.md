---
title: R0 — adaptación del backend a Go
status: aprobado
tags: [libox, r0, backend, go, decision]
updated: 2026-10-04
description: Decisión de Diego de implementar el backend en Go (D-10), qué cambia frente a D-01, herramientas propuestas, presupuesto e impacto en L3, planes y harness.
---

# Adaptación del backend a Go

**Ratificaciones del 04/10:** Diego eligió Vercel para el backend, conservar
Trigger.dev y Auth administrada; mantuvo el techo de US$250/mes. Las propuestas
de hosting alternativo y reemplazo de workflows de esta ficha quedan sustituidas
por el [registro posterior](c1-l3-v8/decisiones-2026-10-04.md). Despliegue,
frontera Go/Trigger.dev y excepción Auth/KMS aún requieren validación y detalle.
La respuesta sobre herramientas no enumera una selección concreta; ver
[alcance de stack](2026-10-02-stack-go-frontend-ts.md).

## Decisión

**D-10 (Diego, 2026-10-02): el backend de Libox se implementa en Go**, como
monolito modular. Es una decisión tomada y sin cambios pendientes. Sustituye la
parte de backend de **D-01** (TypeScript, ratificado el 2026-09-29) en el
[programa de R0](2026-09-25-habilitar-r0-design.md). El resto de D-01 se mantiene.

| Se mantiene | Cambia |
|---|---|
| Frontend Next.js + TypeScript en Vercel Pro | Backend: de TypeScript en Next.js a un servicio Go propio |
| Monolito modular con módulos de dominio separados | Hosting del backend: fuera de Vercel |
| PostgreSQL en Supabase como autoridad de dinero e inventario | Workflows: Trigger.dev se reevalúa (ver abajo) |
| REST + OpenAPI 3.1 como contrato; Scalar (D-07) | CI de D1: Go y TypeScript |
| Supabase Auth, Mercado Pago, Truora en evaluación | — |
| Zonas sin IA, freeze hasta D1, CD-07 | — |

El cambio de lenguaje no altera las zonas sin generación asistida: su código se
escribe a mano en Go. El pseudocódigo de referencia de L3 sigue en Python.

Falta trasladar D-10 al doc 20 de Outline, donde vive ASS-002, y al canon al
emitir el conjunto reconciliado en C2.

## Arquitectura objetivo

```text
Navegador ─► Next.js (Vercel) ──REST/OpenAPI──► Go: API ─┐
                                                 Go: worker ─┼─► PostgreSQL (Supabase)
                     Supabase Auth (JWT) ◄──────────────────┘     AWS KMS (cifrado)
```

- **Una imagen Go, dos modos:** API HTTP y worker persistente, con los mismos
  módulos de dominio. Las reglas no se duplican entre endpoints y trabajos.
- **Contrato primero:** el artefacto OpenAPI genera el servidor Go y el cliente
  TypeScript del frontend. El cliente TS y sus pruebas se conservan; D1 añade la
  conformidad del servidor Go con el contrato.
- **Invariantes en la base:** los controles que deben valer con cualquier lenguaje
  (cuadre del ledger, INV-38, reactivación con los controles del otorgamiento) son
  barrera obligatoria en PostgreSQL. Go añade autenticación, sesión, autorización
  contextual e incompatibilidades en ejecución. Todo eso es implementación humana.

## Herramientas propuestas

Salen del debate entre Claude Opus y Codex del 2026-10-02. **Son propuestas:**
quedan pendientes de la confirmación de Diego y no se ratifican con esta decisión.

| Capa | Propuesta | Motivo y condición |
|---|---|---|
| HTTP | `net/http` (Go ≥1.22) + oapi-codegen en modo estricto | Servidor generado desde el contrato |
| Datos | pgx + sqlc | SQL escrito a mano, coherente con el SQL canónico; sin ORM |
| Migraciones | goose, SQL numerado, versión fijada | Triggers, funciones, particiones y permisos en SQL explícito. Un solo pipeline, que incluye las migraciones de River |
| Trabajos | River (cola sobre PostgreSQL) en el worker | Encolado en la misma transacción que el dato de negocio. Despacho del outbox cada 10 s desde el worker. `create-next-partitions` sigue en `pg_cron` (B3) |
| Importes | `int64` en Go, `BIGINT` en PostgreSQL, cadena decimal en JSON | Nunca punto flotante (C-06) |
| Hosting | Fly.io, si se verifica la federación OIDC hacia AWS STS para KMS; si no, Render con credencial exclusiva y rotada | ECS gana prioridad si se prohíben las claves AWS permanentes |

**Límites de River.** Necesita conexión directa o pooler en modo sesión
(LISTEN/NOTIFY), no el modo transacción. Requiere un presupuesto de conexiones para
API, worker, listener, servicios de Supabase, migraciones y despliegues, frente al
límite del cómputo Small. Encolar una sola vez **no garantiza** un efecto
patrimonial único: idempotencia persistente, conciliación y recuperación siguen
siendo controles humanos.

## Sesión y permisos en Go

Supabase Auth administra credenciales, factores y renovación. Go valida el JWT:

- firma con claves asimétricas (JWKS), algoritmo permitido, emisor y audiencia;
- expiración, y `aal2` para el personal interno;
- subroles leídos de la base de Libox en cada petición, para que una revocación
  sea inmediata.

La sesión del personal interno, con 30 minutos de inactividad y revocación, es de
Libox. **Por verificar:** que el token acredite la reautenticación de los últimos
5 minutos (A10). Si no lo hace, Go registra la reautenticación en su propia sesión.

La convivencia de Supabase Auth con B1-bis (datos personales cifrados con KMS) se
trata en las [decisiones de datos](c1-l3-v8/decisiones-c1-datos.md). La propuesta
del debate es una excepción acotada para el email y el teléfono de Auth, que
exige modificar B1-bis de forma explícita.

## Presupuesto

Sobre el escenario R1 de [proveedores](c1-l3-v8/proveedores.md), de US$208,39:

| Concepto | Efecto |
|---|---|
| Sin Trigger.dev (si se adopta River) | −23,39 |
| Hosting Go (API + worker) | +25 a +50 |
| AWS KMS (claves y uso) | +2 a +5 |
| **Total R1** | **≈ US$212–240** |

Por debajo del techo de US$250, pero el objetivo de US$215 reserva margen para
impuestos y variación. Se elige hosting cerca del extremo inferior y se mide antes
de ampliar. No se recorta PITR ni la copia independiente para pagar cómputo.

## Impacto en documentos y harness

| Ámbito | Cambio | Cuándo |
|---|---|---|
| Programa R0 | D-10 y criterio de éxito sin "stack TypeScript" | Este cambio |
| Borrador L3 V8 §0.3, §0.4 y menciones de lenguaje | Pila Go, presupuesto y CI | Este cambio |
| `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md` | Backend Go | Este cambio |
| `.claude/rules/src-congelado.md`, `scripts/hooks/session_status.py`, `guard_edit.py` | Mensajes y rutas que nombran TypeScript. Son archivos del OS (E4): requieren `LIBOX_EDITAR_OS=1` | PR del OS aparte o D1 |
| D1 | CI Go (build, `go vet`, linter, `go test`, migraciones en PostgreSQL 17 efímero, conformidad con OpenAPI) más el CI del frontend; directorio del backend fuera de `src/`; CODEOWNERS y freeze del nuevo directorio | D1 |
| Specs y planes con fecha anterior | No se editan: son registro histórico | — |
| Canon (`docs/linea-base/`) | Sin cambios hasta C2 (CD-07) | C2 |

## Pendientes de Diego

1. Confirmar las herramientas propuestas, en especial River frente a Trigger.dev.
2. Hosting: verificar la federación de Fly.io o aceptar Render con credencial rotada.
3. Excepción de Supabase Auth en B1-bis.
4. Registrar D-10 en el doc 20 de Outline.
