# Guía de contribución

## Versionamiento

El proyecto usa **Semantic Versioning** (`MAJOR.MINOR.PATCH`). Mientras estemos pre-1.0 (`0.x`), las versiones `MINOR` pueden incluir cambios incompatibles; nos estabilizamos en `1.0.0` cuando el MVP salga a producción.

Las versiones y el `CHANGELOG.md` se generan **automáticamente** con [release-please](https://github.com/googleapis/release-please) a partir de los mensajes de commit. No edites la versión a mano.

## Conventional Commits

Cada commit debe seguir [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>(<ámbito opcional>): <descripción>
```

**Tipos** y cómo afectan la versión:

| Tipo | Uso | Efecto en versión |
|---|---|---|
| `feat` | nueva funcionalidad | `MINOR` |
| `fix` | corrección de bug | `PATCH` |
| `docs` | solo documentación (wiki, ADRs, plan) | sin release |
| `chore` | tooling, config, mantenimiento | sin release |
| `refactor` | cambio de código sin alterar comportamiento | sin release |
| `test` | pruebas | sin release |
| `ci` | pipelines / GitHub Actions | sin release |

Un cambio **incompatible** se marca con `!` o footer `BREAKING CHANGE:` → sube `MAJOR` (o `MINOR` mientras seamos `0.x`).

Ejemplos:

```
docs(plan): registra el backend TypeScript ratificado
feat(draw): motor de sorteo configurable de 1 ganador
fix(purchase): idempotencia en webhook duplicado de MP
feat(payments)!: migra de split directo a escrow real
```

**Ámbitos sugeridos**: `wiki`, `decisions`, `plan`, `purchase`, `draw`, `delivery`, `settlement`, `ledger`, `audit`, `payments`, `auth`, `backoffice`.

### Autoría: sin co-autores automáticos

Los commits **no llevan trailers de co-autoría de herramientas de IA**. En concreto, está prohibido añadir:

```
Co-Authored-By: Claude <...>
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

ni cualquier variante equivalente (`Generated with…`, `Co-Authored-By: <bot>`), tampoco en el cuerpo de los Pull Requests.

**Motivo:** la autoría del repositorio corresponde a las personas del equipo. Un trailer `Co-Authored-By` hace que GitHub registre a la herramienta como *contributor* del proyecto — aparece en la lista de contribuidores, en `git shortlog` y en las estadísticas del repo, que es exactamente lo que no queremos para un repositorio que se comparte con socios e inversores.

Que se haya usado asistencia de IA para redactar un cambio no altera esta regla: **el autor del commit es quien lo revisa y lo firma.**

## Ramas y Pull Requests

- `main` es la rama protegida y siempre desplegable. **No se commitea directo a `main`.**
- El trabajo va en ramas `feat/...`, `fix/...`, `docs/...` y entra vía **Pull Request**.
- El merge a `main` es **siempre rebase-and-merge** (único método habilitado en el repo). Cada commit de la rama aterriza individualmente en `main`, por lo que **cada commit debe ser un Conventional Commit válido** (lo valida el check `commitlint`) — son los commits, no el título del PR, los que alimentan a release-please. Limpia la rama (sin *wip*) antes de mergear.
- Un PR debe pasar los ocho checks obligatorios enumerados abajo antes de mergear.

### Correo de autoría: dominio de la organización

Todos los commits llevan como autor un correo **`@liboxapp.com`** — la autoría del repo es corporativa de cara a socios e inversores. Lo valida el check `commitlint` en cada PR (los bots, como release-please, están exentos). En la práctica:

- Añade y **verifica** tu correo `@liboxapp.com` en tu cuenta de GitHub (*Settings → Emails*) — sin esto tus commits quedan sin atribuir.
- Configura el correo **local a este repo** (no toca tus otros proyectos): `git config user.email "tu@liboxapp.com"`.
- Desactiva *Settings → Emails → "Block command line pushes that expose my email"*: con ese toggle activo, GitHub rechaza tus pushes con el error **GH007**.

Detalle paso a paso en [`docs/equipo/onboarding.md`](docs/equipo/onboarding.md).

## Protección de `main` y CI

El ruleset exige PR, rama actualizada, historia lineal y rebase-and-merge.
Los ocho checks obligatorios están activos desde A1:

| Checks | Qué verifican |
|---|---|
| `commitlint` | Convención, correo corporativo y ausencia de atribución automática |
| `markdownlint`, `links` | Documentación y enlaces locales |
| `verify` | Coherencia del corpus |
| `test (3.9)`, `test (3.12)` | Hooks y políticas de CI |
| `protected-paths`, `commit-policy` | Canon/freeze y autoría desde código de la base |

Por instrucción explícita de Diego, `required_approving_review_count` sigue en
cero y la revisión obligatoria de CODEOWNERS está desactivada. Solo Diego puede
reactivar la revisión humana mediante una nueva instrucción explícita; incorporar
colaboradores no la reactiva. Aplica también a las zonas críticas y al gate de R0.
Ver [regla de revisión humana](.claude/rules/revision-humana.md).
`release-please` mantiene versiones en pushes a `main`.
El CI de producto (build, lint, tipos, tests, migraciones y contrato API) entra en D1.

## Stack y reglas de ingeniería

El [programa de R0](docs/superpowers/specs/2026-09-25-habilitar-r0-design.md)
registra el backend en **Go** (D-10, que sustituye la ratificación de TypeScript para el
backend), monolito modular sobre PostgreSQL gestionado; el frontend usa Next.js App Router
y TypeScript. Workflows y hosting del backend se reevalúan en la [adaptación a Go](docs/superpowers/specs/2026-10-02-r0-backend-go-design.md). Los endpoints invocan módulos
separados de dominio. Scalar documentará la API.

L3 V7 sigue siendo el canon registrado; su runtime .NET es la discrepancia que C2
resolverá emitiendo L3 V8. La ratificación no autoriza editar V7 ni levantar el
freeze. D1 requiere L3 V8, CI de código y una transición revisada de la política
que actualmente protege la regla de freeze desde la rama base.

### Reglas de backend independientes del proveedor

Fuente: [L3 V7 §12](docs/linea-base/LIBOX_ESPECIFICACION_TECNICA_L3_V7.md)
y su punto único de transición (§4.2). Aplicarlas respetando las
[zonas sin generación asistida](.claude/rules/zonas-sin-ia.md).

1. **Atomicidad server-side:** las transiciones persisten estado, auditoría y
   `event_outbox` en la misma transacción. Publicar hacia servicios externos
   corresponde al despachador; no a una llamada remota dentro del commit.
2. **Bloqueo autoritativo en la base:** dinero e inventario se protegen con las
   restricciones y operaciones atómicas del canon. Un lock en memoria no es garantía.
3. **Idempotencia:** clave por intento generada por el cliente; misma clave y
   distinto `request_hash` es conflicto. Una operación en curso no se ejecuta de nuevo.
4. **Webhooks:** validar firma y ventana anti-repetición; persistir en `psp_events`,
   deduplicar y responder 200 al duplicado. Procesar con monotonía de estado;
   registrar fallo, reintento y alarma. No renombrar tablas por convenciones de un SDK.

Los límites y defectos conocidos del canon se resuelven en C1/C2; estas reglas no
certifican el ledger ni añaden un umbral de latencia distinto al de L3 §13.2.

### Proveedores pendientes y preparación

**Drizzle, Supabase e Inngest: a confirmar en C1.** También siguen abiertos auth
con MFA por rol, almacenamiento privado y rate limiting. Las menciones históricas
a Supavisor, Upstash o Vercel WAF no constituyen una selección vigente.

- [ ] Cerrar comparativa de proveedores y acceso transaccional desde el backend.
- [ ] Emitir esquema L3 V8 con restricciones, roles, particiones y triggers verificados.
- [ ] Definir y ensayar backups/restauración contra RPO/RTO acordados.
- [ ] Configurar ejecución de trabajos y despacho durable de `event_outbox`.
- [ ] Definir permisos, secretos, almacenamiento de evidencias y política de rate limiting.
- [ ] Correlacionar trazas y alertas; documentar diagnóstico y recuperación.

Las cinco zonas de Backlog MVP V3 §1.3 mantienen implementación humana y propiedad
fija. Diego es el responsable actual. La segunda revisión humana está suspendida
por su instrucción posterior; no constituye un bloqueo mientras no la reactive
explícitamente. La suspensión no autoriza generación asistida en esas zonas.
