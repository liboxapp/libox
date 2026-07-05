# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Releases are automated with [release-please](https://github.com/googleapis/release-please)
from [Conventional Commits](https://www.conventionalcommits.org/).

## [0.1.1](https://github.com/liboxapp/libox/compare/v0.1.0...v0.1.1) (2026-07-05)


### Bug Fixes

* **ci:** fix plan links and relax markdownlint rules for green CI ([dd68834](https://github.com/liboxapp/libox/commit/dd688348727ba158add0cc65f4a73ef3230b5c28))
* **docs:** rewrap criteria sentence that markdownlint parsed as a list ([3063f62](https://github.com/liboxapp/libox/commit/3063f62fcad55dd4fdc125926f416e8887c27efa))
* **outline:** correct plan path in sync map and collection name in script ([aa7d03c](https://github.com/liboxapp/libox/commit/aa7d03c2368bd6300245c95afdf5c90d97b1e9e2))

## [Unreleased]

## [0.1.0] - 2026-06-06

Hito: wiki de planificación y decisiones de producto cerradas (etapa pre-código).

### Added

- Wiki del proyecto en `docs/` con índice (`docs/README.md`).
- PRD del socio Libox v11 en `docs/prd/`.
- Plan vivo de producto y arquitectura (`docs/plans/libox-plan.md`) con Anexo Z (bitácora de decisiones).
- Glosario de términos (`docs/glosario.md`).
- Documento de trabajo de compliance Perú (`docs/compliance-peru.md`).
- Registros de decisión (ADRs):
  - Z.1 Custodia del dinero — Modelo C (escrow conceptual).
  - Z.2 Elección de PSP — Mercado Pago primario, split en la fuente, Culqi 2º rail.
  - Z.3 Tipo de organizador — cualquiera con RUC activo (natural o jurídica).
  - Z.4 Tipos de sorteo MVP-1 — motor configurable de 1 ganador (T1–T4 presets).
  - Z.5 T8 LIVE — diferido a MVP-3.
  - Z.6 Stack tecnológico — Next.js para todo.
  - Z.7 Versionamiento — semver + Conventional Commits + release-please.
- Vault de Obsidian (`.obsidian/app.json`) con links en markdown estándar.
- Infraestructura de versionamiento: Conventional Commits, CHANGELOG, CI de docs, release-please.

[Unreleased]: https://github.com/liboxapp/libox/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/liboxapp/libox/releases/tag/v0.1.0
