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
docs(decisions): cierra Z.6 stack tecnológico (Next.js)
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
- Un PR debe pasar los checks de CI (`commitlint`, `docs`) antes de mergear.

## Protección de la rama `main` (configurar en GitHub)

Esto se activa una sola vez desde la web de GitHub (no se puede versionar en el repo):

1. **Settings → Branches → Add branch ruleset** (o "Add rule" clásico) para `main`.
2. Activar **Require a pull request before merging**.
   - Cuando entren más colaboradores: activar **Require approvals** (1+).
3. Activar **Require status checks to pass before merging** y seleccionar:
   - `commitlint`
   - `markdownlint` y `links` (del workflow `docs`)
4. Activar **Require branches to be up to date before merging**.
5. **Require linear history** (coherente con rebase-and-merge, el único método de merge habilitado).

## CI actual

| Workflow | Qué valida | Cuándo |
|---|---|---|
| `commitlint` | mensajes de commit en formato Conventional | en cada PR |
| `docs` | markdownlint + verificación de links locales del wiki | en cambios a `*.md` |
| `release-please` | calcula versión y actualiza `CHANGELOG.md` | en push a `main` |

Cuando entre el código (Next.js), se añadirán jobs de `typecheck`, `test` y `build`.

## Reglas de ingeniería (vigentes desde el scaffold)

Salen del architecture review (agosto 2026) y de las design notes de los
módulos críticos. Son regla dura al escribir código:

1. **Writes de dinero solo por Drizzle server-side.** Todo write que toque
   dinero, tickets, draw, settlement o auditoría va en una **sola transacción
   Drizzle** (`persist → audit_event → outbox`, mismo commit), server-side.
   `supabase-js` queda para reads bajo RLS y realtime — **nunca** para estos
   writes (PostgREST no tiene transacciones multi-statement; el invariante de
   auditoría se rompería en silencio).
2. **Webhooks: ACK rápido, procesa async.** El endpoint valida firma,
   persiste en `webhook_inbox` con idempotency key, responde 200 en < 2s y
   delega a Inngest. Cero lógica de negocio inline. El estado del pago es la
   fuente de verdad, nunca el conteo de webhooks.
3. **Concurrencia se resuelve en la DB.** Unicidad de ticket por constraint
   (`UNIQUE (raffle_id, ticket_number)`), reservas atómicas con TTL, y locks
   explícitos (`SELECT … FOR UPDATE` / advisory lock) en la ejecución del
   draw. La idempotency key es la segunda barrera, no la única.

### Checklist de scaffold

- [ ] Supavisor **modo transacción** + `prepared: false` en el cliente Drizzle.
- [ ] Constraints de unicidad de ticket y balance de ledger en la migración 001.
- [ ] PITR habilitado en Supabase desde el día 1.
- [ ] Job semanal de export del audit store a objeto WORM (object lock) con hash de verificación.
- [ ] Inngest conectado; `webhook_inbox` y outbox publisher como primeras functions.
- [ ] Realtime de contadores por canal broadcast throttled, no `postgres_changes` por insert.
- [ ] Sentry + `trace_id` transversal desde el primer endpoint.
