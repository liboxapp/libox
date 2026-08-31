---
title: Onboarding de desarrolladores
status: vigente
tags: [equipo, onboarding, claude-code]
updated: 2026-08-30
description: Checklist para incorporarte al equipo Libox con el entorno completo funcionando (accesos, repo, Claude Code, lectura obligatoria, flujo diario).
---

# Onboarding de desarrolladores

Checklist para incorporarte al equipo Libox con el entorno completo
funcionando. Tiempo estimado: ~30 minutos.

## 1. Accesos

- [ ] Añade y **verifica** tu correo **`@liboxapp.com`** en tu cuenta de
  GitHub (*Settings → Emails*). **Requisito previo a la invitación** — Diego
  no invita cuentas sin el correo de la org verificado.
- [ ] Desactiva *Settings → Emails → "Block command line pushes that expose
  my email"* — con ese toggle activo, GitHub rechaza tus pushes con el error
  **GH007** (este repo commitea con el correo corporativo visible).
- [ ] Invitación a la organización GitHub **`liboxapp`** (te la envía Diego).
- [ ] Seat en **Claude Team** con acceso a Claude Code (te lo asigna Diego).
- [ ] Cuenta en Outline (`liboxapp.getoutline.com`) — capa compartible del
  wiki con los socios.

## 2. Repo y entorno de Claude Code

- [ ] Clona el repo: `git clone https://github.com/liboxapp/libox.git`
- [ ] Configura el correo corporativo **local al repo**:
  `git config user.email "tu@liboxapp.com"`. El guard B4 bloquea commits con
  otro dominio y el CI rechaza PRs con commits fuera de `@liboxapp.com`.
- [ ] Python 3.9 o superior disponible como `python3` (lo usan los guards y
  `verify_corpus.py`).
- [ ] Instala [Claude Code](https://claude.com/claude-code) (CLI, app de
  escritorio o extensión del IDE).
- [ ] Abre el repo con Claude Code. El **sistema operativo de IA** está
  versionado y se aplica solo: reglas por ruta, guards (co-autoría, push a
  `main`, canon in-place, `src/` congelado, naming), skills `libox-*`, agentes
  y plugins del equipo. En el primer arranque acepta la instalación de los
  plugins y del marketplace `context-mode` cuando Claude Code lo pida. Cada
  sesión empieza con el digest de actividad y el bloque "Estado del OS de IA".
- [ ] Autentica GitHub CLI: `gh auth login` — sin esto, el digest falla en
  silencio y `gh pr create` no funciona.
- [ ] Conecta el **MCP de Outline** en tu cuenta de claude.ai (Settings →
  Connectors) para leer/escribir la capa compartible desde Claude.
- [ ] Tu configuración personal va en `.claude/settings.local.json` —
  **nunca se commitea** (ya está gitignorada). Ahí van también las válvulas
  de escape de los guards (`"env"`), solo con acuerdo explícito.

## 3. Lectura obligatoria (en este orden)

1. [`docs/README.md`](../README.md) — índice del wiki y mapa de documentos.
2. [`sistema-operativo-ia.md`](sistema-operativo-ia.md) — cómo trabaja Claude
   Code en este repo: capas, guards, skills, agentes, orquestación.
3. [`CONTRIBUTING.md`](../../CONTRIBUTING.md) — versionamiento, Conventional
   Commits en español, flujo de PRs, reglas de ingeniería duras.
4. [`CLAUDE.md`](../../CLAUDE.md) (raíz) — reglas firmes y punteros.
5. [`estilo-documentacion.md`](estilo-documentacion.md) — cómo se escribe.
6. [`src/CLAUDE.md`](../../src/CLAUDE.md) — reglas de código para cuando se
   levante el freeze de ASS-002.
7. Los 8 ADRs históricos de [`docs/archive/decisions/`](../archive/decisions/README.md)
   — contexto de las decisiones; no se reabren sin evidencia nueva.

## 4. Flujo de trabajo diario

- Rama por cambio: `<type>/<short-kebab-name>` desde `main` actualizado.
- Commits = Conventional Commits **en español** (los valida `commitlint`).
- PR con `/libox-pr` → checks (`commitlint`, `markdownlint`, `links`,
  `verify-corpus`, `hooks`) → **rebase-and-merge** (único método habilitado).
- El código es en inglés; todo lo user-facing y la conversación con Claude,
  en español (Perú).
- La verdad del proyecto vive en `docs/` (versionada). La memoria automática
  de Claude es **personal por máquina** — nada importante puede vivir solo
  ahí: se promueve a `docs/` por PR.

## 5. Para Diego al incorporar cada dev

- [ ] Verificar que el dev ya tiene su correo `@liboxapp.com` **verificado**
  en su cuenta GitHub (pedirle captura de *Settings → Emails*); solo
  entonces invitar.
- [ ] Invitar al team `core` de la org con rol *write*.
- [ ] Asignar seat de Claude Team.
- [ ] Al pasar de 1 colaborador: subir el ruleset de `main` a **1 approval
  requerido** y activar **require code owner review** (el
  [`CODEOWNERS`](../../.github/CODEOWNERS) ya está listo).
- [ ] Verificar que el secreto `RELEASE_PLEASE_TOKEN` (PAT fine-grained)
  sigue vigente; documentar fecha de expiración y rotación.
