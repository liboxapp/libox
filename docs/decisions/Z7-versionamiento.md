---
title: Z.7 — Versionamiento y flujo de repositorio
status: cerrada
tags: [libox, decision, versionamiento, git, ci, semver]
decided: 2026-06-06
relates: [docs/plans/libox-plan.md]
updated: 2026-06-06
---

# Z.7 — Versionamiento y flujo de repositorio

**Estado**: Cerrada (2026-06-06).
**Decisor**: Diego.
**Documento canónico**: este archivo.

---

## Decisión

El repositorio adopta, **desde ahora** (etapa pre-código):

- **Semantic Versioning** (`MAJOR.MINOR.PATCH`), arrancando en `0.1.0` y estabilizando en `1.0.0` al salir el MVP.
- **Conventional Commits** como convención de mensajes.
- **release-please** para automatizar versión + `CHANGELOG.md` desde los commits.
- **CHANGELOG.md** formato Keep a Changelog.
- **Rama `main` protegida** + flujo de Pull Requests.
- **GitHub Actions** de alcance creciente: hoy lint de docs + commitlint; con código, typecheck/test/build.

---

## El matiz: el repo es hoy solo-docs

Semver formal versiona releases de software con API. Hoy el repo es un **wiki de decisiones**, no software. Por eso:

- Se **adoptan las convenciones ahora** (Conventional Commits, CHANGELOG, CI de docs) para construir el hábito y dejar la tubería lista.
- El **número de versión arranca en `0.1.0`** marcando el hito "wiki + decisiones cerradas".
- Mientras seamos `0.x`, los `feat` suben `MINOR` y los `fix` suben `PATCH` (config `bump-minor-pre-major`); nada es "estable" hasta `1.0.0`.
- Las decisiones ya estaban versionadas de facto por su número de ADR + fecha; el CHANGELOG las consolida.

---

## Componentes y por qué cada uno

| Componente | Rol | Archivo |
|---|---|---|
| Conventional Commits | hace el versionado y el changelog **automáticos** | `commitlint.config.js`, workflow `commitlint` |
| release-please | calcula versión y abre PR de release con el CHANGELOG | `release-please-config.json`, `.release-please-manifest.json`, workflow `release-please` |
| CHANGELOG.md | historial legible por humanos | `CHANGELOG.md` |
| CI docs | markdownlint + verificación de links locales | workflow `docs`, `.markdownlint-cli2.yaml` |
| Branch protection | `main` siempre verde y revisado | se configura en GitHub (ver [CONTRIBUTING](../../CONTRIBUTING.md)) |

La pieza que une el objetivo: **Conventional Commits → release-please → CHANGELOG + tag** es un pipeline automático. Cada merge a `main` con un `feat`/`fix` hace que release-please abra un PR de release con la versión y el changelog calculados.

---

## Flujo de trabajo

- `main` protegida; nada se commitea directo.
- Ramas `feat/...`, `fix/...`, `docs/...` → **Pull Request** → **rebase-and-merge** (único método habilitado en el repo). Cada commit aterriza en `main` y debe ser Conventional; los commits —no el título del PR— alimentan release-please.
- CI (`commitlint`, `docs`) debe pasar antes de mergear.

> **Actualización 2026-06-20:** la política de merge pasó de *squash merge* a **rebase-and-merge** (decisión de Diego). En GitHub se deshabilitaron *merge commit* y *squash*; solo queda *rebase*. Implica mantener historial lineal y commits limpios y conventional en cada rama.
- Detalle operativo y pasos para activar branch protection en GitHub: [`CONTRIBUTING.md`](../../CONTRIBUTING.md).

---

## Lo que NO se puede versionar en el repo (lo hace Diego en GitHub)

- Crear el repositorio remoto en GitHub y `git push`.
- Activar **branch protection** / rulesets (vive en la config de GitHub, no en archivos).
- Reemplazar `OWNER` por el usuario/org real en los links del `CHANGELOG.md`.

---

## Evolución

Cuando entre el código Next.js:

1. Cambiar `release-type` de `simple` a `node` en `release-please-config.json` (leerá `package.json`).
2. Añadir jobs de CI: `typecheck`, `test`, `build`, y sumarlos a los required status checks.
3. Añadir ámbitos de commit nuevos según los módulos que se construyan.
