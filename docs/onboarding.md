---
title: Onboarding de desarrolladores
status: vigente
tags: [equipo, setup, claude-code]
updated: 2026-08-03
---

# Onboarding de desarrolladores

Checklist para incorporarte al equipo Libox con el entorno completo
funcionando. Tiempo estimado: ~30 minutos.

## 1. Accesos

- [ ] Invitación a la organización GitHub **`liboxapp`** (te la envía Diego).
- [ ] Seat en **Claude Team** con acceso a Claude Code (te lo asigna Diego).
- [ ] Cuenta en Outline (`liboxapp.getoutline.com`) — capa compartible del
  wiki con los socios.

## 2. Repo y entorno de Claude Code

- [ ] Clona el repo: `git clone https://github.com/liboxapp/libox.git`
- [ ] Instala [Claude Code](https://claude.com/claude-code) (CLI, app de
  escritorio o extensión del IDE).
- [ ] Abre el repo con Claude Code. El entorno del equipo está **versionado**
  y se aplica solo: plugins (`superpowers`, `frontend-design`,
  `skill-creator`, `hookify`, `claude-md-management`, `context-mode`), skills
  compartidas (`.claude/skills/`), el hook de digest de actividad y las
  reglas hookify (bloquean trailers de co-autoría de IA y push directo a
  `main`). En el primer arranque, acepta la instalación de los plugins y del
  marketplace `context-mode` cuando Claude Code lo pida.
- [ ] Autentica GitHub CLI: `gh auth login` — sin esto, el digest de
  actividad del arranque de sesión falla en silencio y `gh pr create` no
  funciona.
- [ ] Conecta el **MCP de Outline** en tu cuenta de claude.ai (Settings →
  Connectors) para poder leer/escribir la capa compartible desde Claude.
- [ ] Tu configuración personal va en `.claude/settings.local.json` —
  **nunca se commitea** (ya está gitignorada).

## 3. Lectura obligatoria (en este orden)

1. [`docs/README.md`](README.md) — índice del wiki y mapa de documentos.
2. [`CONTRIBUTING.md`](../CONTRIBUTING.md) — versionamiento, Conventional
   Commits en español, flujo de PRs, reglas de ingeniería duras.
3. [`CLAUDE.md`](../CLAUDE.md) (raíz) — cómo trabaja Claude en este repo.
4. [`src/CLAUDE.md`](../src/CLAUDE.md) — reglas de código: flujo Superpowers
   SDD, política de idiomas, stack cerrado (Z.6), orquestación de modelos.
5. Los 8 ADRs de [`docs/decisions/`](decisions/README.md) — las decisiones
   ya cerradas; no se reabren sin evidencia nueva.

## 4. Flujo de trabajo diario

- Rama por feature: `<type>/<short-kebab-name>` desde `main` actualizado.
- Commits = Conventional Commits **en español** (los valida `commitlint`).
- PR → checks (`commitlint`, `markdownlint`, `links`) → **rebase-and-merge**
  (único método habilitado).
- El código es en inglés; todo lo user-facing en español (Perú); la
  conversación con Claude en español.
- La verdad del proyecto vive en `docs/` (versionada). La memoria automática
  de Claude es **personal por máquina** — nada importante puede vivir solo
  ahí: toda decisión cerrada termina en un ADR.

## 5. Para Diego al incorporar cada dev

- [ ] Invitar al team `core` de la org con rol *write*.
- [ ] Asignar seat de Claude Team.
- [ ] Al pasar de 1 colaborador: subir el ruleset de `main` a **1 approval
  requerido** y activar **require code owner review** (el
  [`CODEOWNERS`](../.github/CODEOWNERS) ya está listo).
- [ ] Verificar que el secreto `RELEASE_PLEASE_TOKEN` (PAT fine-grained)
  sigue vigente; documentar fecha de expiración y rotación.
