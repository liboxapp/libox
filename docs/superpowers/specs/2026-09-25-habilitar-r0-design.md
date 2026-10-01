---
title: Programa para habilitar R0 — diseño
status: borrador
tags: [libox, r0, harness, programa, spec]
updated: 2026-10-01
description: Programa aprobado por Diego para resolver la auditoría del harness (SY-01 a SY-16) y los defectos del canon, y dejar R0 listo para arrancar sobre el backend TypeScript ratificado. Streams, decisiones, secuencia y criterio de éxito.
---

# Programa para habilitar R0

## Origen

- **Auditoría del harness** `20260925-203710-harness`: dictamen `requiere cambios` con 16 temas (SY-01 a SY-16). La síntesis está en `docs/audits/20260925-203710-harness/synthesis.md`, en el run todavía sin versionar.
- **Revisión de sistema**: 19 hallazgos técnicos del canon en la [nota de hallazgos](2026-09-25-revision-sistema-hallazgos-l3.md). La [nota de trade-offs](2026-09-25-revision-sistema-decisiones-ass.md) queda como antecedente de la ratificación.

El programa no decide ASS-001 (custodia) ni edita el canon en su lugar: el canon cambia solo con `libox-versionar-doc`.

## Decisiones

| ID | Decisión | Fecha y alcance |
|---|---|---|
| D-01 | **ASS-002 ratificada por los socios: backend TypeScript** en un monolito modular. Next.js (App Router) y TypeScript para interfaz y endpoints; módulos de dominio separados (órdenes, pagos, boletos, sorteos, liquidaciones) que los endpoints solo invocan; PostgreSQL gestionado; un servicio de workflows administrado para lo asíncrono. Registrada en el doc 20 (ASS-002 invalidada, revisión 23) | 2026-09-29 · pendiente de alta como DEC-\* |
| D-02 | Revisores: Arom B. y Martin G. Diego los invita desde GitHub; revisión humana suspendida hasta reactivación explícita de Diego | 2026-09-25 · ruleset y CODEOWNERS |
| D-03 | Escrituras por shell: el CI es la garantía y el hook añade una heurística | 2026-09-25 · guards y CI |
| D-04 | Un guard que falla sigue permitiendo, pero con aviso visible | 2026-09-25 · guards |
| D-05 | L3 V8 incluirá el stack ratificado y las correcciones técnicas. El ledger (H-01, H-03) queda como hallazgo hasta tener confirmación contable. [LEGAL→ABOGADO] | 2026-09-25 · canon |
| D-06 | Secuencia en streams paralelos con PRs chicos | 2026-09-25 · programa |
| D-07 | Scalar como documentación de la API del backend | 2026-09-25 · canon §0.3 y backend |
| D-08 | Sin spike: sus fallos deliberados pasan a ser pruebas de aceptación obligatorias (tabla de abajo), y la consola interna de operación entra como épica | 2026-09-29 · R1 y E14 |
| D-09 | Proveedores abiertos (base de datos, workflows, auth, almacenamiento, rate limiting): se cierran con comparativa en C1, antes de emitir L3 V8 | 2026-09-29 · canon §0.3 |

## Criterio de éxito

R0 queda habilitado cuando se cumplen las cinco condiciones:

1. La auditoría del harness, re-ejecutada, da `sin bloqueos en el alcance revisado`.
2. ~~Los socios ratifican ASS-002~~: **cumplido el 2026-09-29** (D-01).
3. El conjunto L3/artefactos reconciliado está emitido con identidad resuelta, stack TypeScript y proveedores cerrados, y `verify_corpus.py` en cero fallos. La [reconciliación Cowork](c1-l3-v8/reconciliacion-linea-base.md) no está cerrada por un check lexical verde.
4. El freeze se levanta en el PR de cierre de ASS-002, con CI de código obligatorio.
5. **Suspendida por instrucción explícita de Diego (2026-09-29):** la revisión
   humana no bloquea R0 hasta que él la reactive explícitamente. La incorporación
   de colaboradores no la reactiva. Ver [regla operativa](../../../.claude/rules/revision-humana.md).

**Fuera de alcance:** construir historias de R0 y decidir ASS-001. ASS-001 no bloquea el gate de R0, pero sí R1 y R2, y se sigue en el doc 20.

## Pruebas de aceptación obligatorias (D-08)

Heredadas del spike descartado. Entran en la definición de terminado del flujo de compra (R1) y del motor de sorteo (E14). Deben pasar contra PostgreSQL real y el sandbox del proveedor de pagos, no solo con mocks.

| ID | Fallo inyectado | Resultado esperado |
|---|---|---|
| F1 | El webhook llega dos veces, en serie y en concurrencia | Un solo procesamiento; ambas llamadas responden 200 |
| F2 | El proveedor acepta el pago y la llamada agota el tiempo | La orden queda pendiente y se resuelve por consulta o conciliación; reintentar con la misma clave no duplica el cobro |
| F3 | El proceso muere después del commit y antes de publicar el evento | El outbox lo publica al reanudar; no se pierde nada |
| F4 | Se pide dos veces el mismo reembolso | Un solo efecto patrimonial |
| F5 | N compras concurrentes por el último boleto | Exactamente una emitida; cero sobreventa |
| F6 | Disparo duplicado del sorteo, reinicio del worker o baliza que se retrasa | Una sola ejecución; espera acotada y alarma si vence el timeout |
| F7 | Expira la reserva y después se confirma el pago | Se aplica la política que fije L3 V8 (H-16) |

Además, cada incidente de F1 a F7 se diagnostica y reintenta desde la consola interna, sin SQL manual.

## Streams y sub-proyectos

Cada sub-proyecto tiene su propio plan de implementación y su propio PR.

### Stream A — Harness (empieza ya)

| ID | Qué entra | Temas | Verificación |
|---|---|---|---|
| A0 | PR del OS de IA (rama local `codex/activate-ai-audit`) con el run de auditoría. Soporte de prefijos en `outline-ignore.txt` y alta de `docs/audits/`. PR aparte para el commit de Scalar (`7ca542f`), que quedó fuera de `main` | SY-16 (parte) | CI verde. `outline-sync` en verde en `main` |
| A1 | `verify-corpus` y `hooks` corren siempre y pasan a ser obligatorios. Job `protected-paths` que falla si se modifica un `docs/linea-base/*_V<n>.*` existente, o si se toca `src/` (salvo los `CLAUDE.md`) o la config del scaffold mientras la regla del freeze exista en la rama del PR. Así el PR de cierre, que borra la regla, puede pasar. Control de trailers de IA en `commitlint` | SY-02, SY-05 | PRs sintéticos rechazados en un repo de prueba |
| A2 | CODEOWNERS con rutas reales, dueño y revisor fijo por zona sin IA, canon y OS. Regla `zonas-sin-ia.md` replicada en `AGENTS.md`. `CONTRIBUTING.md` y `src/CLAUDE.md` alineados al stack ratificado: reglas de backend neutrales extraídas de L3 §12, y los nombres de proveedor (Drizzle, Supabase, Inngest) marcados "a confirmar en C1". `AGENTS.md` aclara que en Codex no hay guards y que aplica el CI. Revisión humana suspendida hasta reactivación explícita de Diego; mantener CI y revisión automatizada | SY-07, SY-08, SY-09 | `revisor-pr` sobre el PR. No exigir aprobación humana mientras dure la suspensión |
| A3 | `guard_edit`: rutas normalizadas (worktree, `realpath`, mayúsculas); allowlist de escritura durante el freeze; E4 que protege los archivos del OS (`scripts/hooks/`, `.claude/settings.json`, `.claude/rules/`, `.claude/agents/`), con una válvula `LIBOX_EDITAR_OS=1` cuyo uso queda avisado en stderr. `guard_bash`: heurística de escrituras por shell y regex B1–B4 endurecidas. Ambos: aviso visible si fallan y timeouts por debajo de 90 s. `session_status`: "regla ausente, verificar el doc 20" | SY-03, SY-04, SY-05, SY-06, SY-10 | Tests rojos primero en `scripts/hooks/tests/`. El ensayo de guards da DENY en S1–S3, W1–W2, B1b, symlink y `vitest.config.ts` |
| A4 | `mcp__*` en `disallowedTools` de los revisores. Un worktree fijo al SHA auditado por revisor. Regla para runs concurrentes y modo `resume <run-id>`. Ensayo de guards versionado con fixtures H-01 y H-02. Saneador de credenciales. E5 contra la sobrescritura de informes | SY-11, SY-12, SY-13 | Tests del saneador y de E5. H-01 a H-08 con evidencia o un límite explícito |
| A5 | `outline-kb-cli` con versión fijada y actions fijadas por SHA. Marketplace de terceros con versión fijada. `outline-skills` limitada a lectura y sin `--api-key` en los ejemplos. Títulos de PR tratados como datos no confiables en el digest. Confirmación humana en `libox-registrar-hallazgo`. Metadata, conteos y docstrings al día | SY-14, SY-15, SY-16 | CI verde con las versiones fijadas |

### Stream C — Canon L3 V8 (empieza tras A1)

- **C1.** Registrar los hallazgos por CD-07 y preparar el borrador de L3 V8:
  - **§0.3 con el stack ratificado** (D-01), Next.js 16 en lugar de 14, y Scalar (D-07).
  - **Comparativa de proveedores** (D-09): Neon o Supabase, Inngest o Trigger.dev, auth con MFA por rol, almacenamiento privado de evidencias y rate limiting. Se evalúan contra lo que exige L3: 30 trabajos con ejecución única, outbox cada 10 s, conexiones desde serverless, límites de pasos y timeouts, costo en R0–R1. Diego decide antes de C2.
  - SQL desplegable: particiones, GRANTs, semillas, triggers prometidos e INV-38.
  - OpenAPI completo (T-1), con al menos las 43 rutas de §11, válido en 3.1.
  - Vectores de prueba con resultado esperado, y `verify_draw` sin ambigüedad.
  - HMAC del DNI, RPO/RTO y backups, almacenamiento de `server_seed`, política de pago tardío (F7) y timeout de la baliza.
  - Las pruebas F1–F7 en §14.
  - El ledger (H-01, H-02, H-03) queda registrado y pendiente de confirmación contable.
- **C2.** Emitir L3 V8 con `libox-versionar-doc` (CD-01 a CD-11): `verify_corpus` en cero, Registro §1 y `BASELINE`. Alta del DEC-\* de ASS-002.

**Ampliación Cowork (2026-10-01).** Se mantiene la secuencia y las decisiones
D-01–D-09. C1 integra las 27 diferencias revisadas por Codex/Opus, conserva
acuerdos de dominio y añade contrato de viabilidad/fianza, relojes, comprador,
canales y backlog. El [plan actualizado](../plans/2026-09-30-r0-c1.md) delimita
trabajo documental y aportes humanos; no ratifica parámetros nuevos ni habilita
dinero real. La mención histórica V8 en C1/C2/D1 queda condicionada a resolver
su emisión: V9 si V8 ya fue formalmente emitida, V8 consolidada si no.
D-05 sigue vigente; ASS-001 y contabilidad se cierran antes de operar sus flujos.

### Stream D — Preparación de R0 (tras C2)

**D1.** Es el PR de cierre de ASS-002, y hace cinco cosas:

- Borra la regla del freeze, las constantes `FROZEN_*` y sus tests.
- Añade el CI de código TypeScript: build, lint, typecheck, test, migraciones sobre PostgreSQL efímero con el esquema V8 y contrato OpenAPI.
- Añade la capa `dev`: agentes `ejecutor`, `tester` y `depurador`, y una regla de backend con los proveedores de L3 V8.
- Suma las rutas de código a CODEOWNERS.
- Registra la consola interna de operación como épica.

El código de las zonas sin IA lo escribe a mano su dueño (Backlog V3 §1.3), también
en R0. La segunda revisión humana queda suspendida por la instrucción posterior
de Diego; CI y revisión automatizada se mantienen.

## Secuencia

```
A0 ─► A1 ─► A2 ─► A3 ─► A4 ─► A5 ───────────────┐
       │                                          ▼
       └─► C1 borrador L3 V8 + proveedores ─► C2 ─► D1 ─► re-auditoría
```

C1 arranca después de A1, así el canon ya corre bajo el gate de CI. A2 mantiene la revisión humana desactivada hasta reactivación explícita de Diego. El cierre re-ejecuta `/libox-system-design-audit` (harness) y `/libox-system-design-audit producto`.

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Activar la revisión obligatoria con una sola persona bloquea todos los PRs | Mantenerla desactivada hasta reactivación explícita de Diego, incluso si aceptan invitados |
| Construir sobre el OS sin integrar | A0 va primero; los PRs posteriores se rebasan sobre `main` |
| Ratificar sin spike deja sin medir los límites del proveedor de workflows | La comparativa de C1 los evalúa contra los requisitos de L3, y F1–F7 los prueban en R1 contra servicios reales |
| L3 V8 es grande (OpenAPI de 16 a 43 o más operaciones) | Se prepara en paralelo y se estima en el plan de C1. T-1 cotizado en 8 SP es probablemente bajo |
| Presupuesto de infraestructura calculado sobre otro stack | 08. Finanzas se reestima al cerrar los proveedores en C1 |
