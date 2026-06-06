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

## Ramas y Pull Requests

- `main` es la rama protegida y siempre desplegable. **No se commitea directo a `main`.**
- El trabajo va en ramas `feat/...`, `fix/...`, `docs/...` y entra vía **Pull Request**.
- Se recomienda **squash merge** con un **título de PR en formato Conventional Commit** (ese título alimenta a release-please).
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
5. (Opcional) **Require linear history** si se usa squash merge.

## CI actual

| Workflow | Qué valida | Cuándo |
|---|---|---|
| `commitlint` | mensajes de commit en formato Conventional | en cada PR |
| `docs` | markdownlint + verificación de links locales del wiki | en cambios a `*.md` |
| `release-please` | calcula versión y actualiza `CHANGELOG.md` | en push a `main` |

Cuando entre el código (Next.js), se añadirán jobs de `typecheck`, `test` y `build`.
