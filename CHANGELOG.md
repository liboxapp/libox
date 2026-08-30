# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Releases are automated with [release-please](https://github.com/googleapis/release-please)
from [Conventional Commits](https://www.conventionalcommits.org/).

## [0.1.1](https://github.com/liboxapp/libox/compare/v0.1.0...v0.1.1) (2026-08-30)


### Features

* **app:** componentes de progreso, cuenta regresiva y tarjeta de rifa ([66bb827](https://github.com/liboxapp/libox/commit/66bb82767b6a159b932f6ca85c1a26ab716e9139))
* **app:** datos mock de 12 rifas en 5 categorías con estados variados ([5476f11](https://github.com/liboxapp/libox/commit/5476f1143e4dc1acfb39ec3d1404fb65548856b7))
* **app:** design tokens derivados del VIES, tipografías y layout base ([8527c3e](https://github.com/liboxapp/libox/commit/8527c3ea1f133721585bd885113ae5fd85a83b5b))
* **app:** detalle de rifa con selector de tickets, estado finalizado y 404 ([0c304ae](https://github.com/liboxapp/libox/commit/0c304ae180ca0726d4b389521344ab7ecb1be0e0))
* **app:** formato de moneda es-PE desde céntimos con TDD ([0cc70e4](https://github.com/liboxapp/libox/commit/0cc70e433ba7f282d4166595087a56edd9eb326d))
* **app:** header y footer del sitio con lockup y disclaimer legal placeholder ([25585fe](https://github.com/liboxapp/libox/commit/25585fe548f0351167b267e655b647dcc8a9e1b3))
* **app:** home con hero, sellos de confianza y catálogo filtrable ([2aeee45](https://github.com/liboxapp/libox/commit/2aeee451225352a3b5660e347d1d3046e22b998a))
* **app:** logo provisional según el VIES e ilustraciones de premios por categoría ([d12a4f2](https://github.com/liboxapp/libox/commit/d12a4f2cb305f160147ea9e357f5015ec33eae00))
* **app:** tipos y lógica pura del dominio de rifas con TDD ([6cbbb51](https://github.com/liboxapp/libox/commit/6cbbb51e2345f2db319fd8fc92a08fd52bf164d9))


### Bug Fixes

* **app:** alinea el gradiente del isotipo con el arte congelado del VIES ([7134222](https://github.com/liboxapp/libox/commit/71342220c136fbbae1c174dc5b97b0cf18ca480d))
* **app:** anuncia el subtotal como región viva en el selector de tickets ([a058764](https://github.com/liboxapp/libox/commit/a0587645d202fafbc58b05160e726b4dd825291e))
* **app:** aplica Manrope e Instrument Sans y sube los objetivos táctiles a 44 px ([1a4deaa](https://github.com/liboxapp/libox/commit/1a4deaa3c0042dba2cc8e173f2fb1375eb28f153))
* **app:** pulido post-review — countdown accesible, escape NBSP y comentarios exactos ([6b6e972](https://github.com/liboxapp/libox/commit/6b6e97221daadf8541b71742e463ff40bbda821c))
* **app:** restaura el cableado de la fuente sans tras el init de shadcn ([f90c764](https://github.com/liboxapp/libox/commit/f90c7643c8c6dbcf8a904615c207b76705887688))
* **ci:** fix plan links and relax markdownlint rules for green CI ([dd68834](https://github.com/liboxapp/libox/commit/dd688348727ba158add0cc65f4a73ef3230b5c28))
* **ci:** point outline-sync at liboxapp instance and guard map coverage ([bdf7d1a](https://github.com/liboxapp/libox/commit/bdf7d1ab6412a8d5bccf19eb0a08bae15b7fa68e))
* **docs:** repara los enlaces relativos tras la mudanza a docs/archive ([b54f27d](https://github.com/liboxapp/libox/commit/b54f27da47ece9190644da80927b7e494e385c3a))
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
