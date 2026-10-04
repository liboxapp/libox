# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Releases are automated with [release-please](https://github.com/googleapis/release-please)
from [Conventional Commits](https://www.conventionalcommits.org/).

## [0.1.1](https://github.com/liboxapp/libox/compare/v0.1.0...v0.1.1) (2026-10-04)


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
* **harness:** activa la auditoría compartida de Libox ([53f360f](https://github.com/liboxapp/libox/commit/53f360f011ca48d6a964c5be7c18c19bff5660f0))
* **infra:** consolidar candidato C1 y validar contratos y SQL ([1bcee98](https://github.com/liboxapp/libox/commit/1bcee98c35a4a91ecd9b8925ed099004d57fd98d))
* **infra:** integrar decisiones aprobadas de C1 ([d7c88b6](https://github.com/liboxapp/libox/commit/d7c88b632126859b55fccaf6c4df19de2cf87261))
* **os-ia:** agentes Libox en Opus — redactor de docs, auditor de corpus y revisor de PR ([b0dbed4](https://github.com/liboxapp/libox/commit/b0dbed4f0eabdbdc17be69823d0e71e9921bda6d))
* **os-ia:** estado del OS al inicio de sesión (rama, freeze ASS-002, verify_corpus) ([dc2a1f8](https://github.com/liboxapp/libox/commit/dc2a1f85094e3872c5e8e64ee28ba48aa6a6c9ad))
* **os-ia:** guard de Bash — co-autoría, push a main, CD-10 y correo de la org ([8e7cc02](https://github.com/liboxapp/libox/commit/8e7cc02ce8576d83cd3410a47079afd62edc0668))
* **os-ia:** guard de edición — canon in-place, scaffold congelado y naming legacy ([4955b34](https://github.com/liboxapp/libox/commit/4955b34e18c4390600c0aba90fc678746cb13320))
* **os-ia:** skills Libox — versionar doc del canon, registrar hallazgo, outline-sync y PR ([ac615dc](https://github.com/liboxapp/libox/commit/ac615dcbdd07a8f18f86d49b3d0b61c819fb753d))


### Bug Fixes

* **app:** alinea el gradiente del isotipo con el arte congelado del VIES ([7134222](https://github.com/liboxapp/libox/commit/71342220c136fbbae1c174dc5b97b0cf18ca480d))
* **app:** anuncia el subtotal como región viva en el selector de tickets ([a058764](https://github.com/liboxapp/libox/commit/a0587645d202fafbc58b05160e726b4dd825291e))
* **app:** aplica Manrope e Instrument Sans y sube los objetivos táctiles a 44 px ([1a4deaa](https://github.com/liboxapp/libox/commit/1a4deaa3c0042dba2cc8e173f2fb1375eb28f153))
* **app:** pulido post-review — countdown accesible, escape NBSP y comentarios exactos ([6b6e972](https://github.com/liboxapp/libox/commit/6b6e97221daadf8541b71742e463ff40bbda821c))
* **app:** restaura el cableado de la fuente sans tras el init de shadcn ([f90c764](https://github.com/liboxapp/libox/commit/f90c7643c8c6dbcf8a904615c207b76705887688))
* **audit:** aislar snapshots y conservar informes para A4 ([d1b492f](https://github.com/liboxapp/libox/commit/d1b492f62daee15e79b8de18143dac9198c440c8))
* **ci:** fix plan links and relax markdownlint rules for green CI ([dd68834](https://github.com/liboxapp/libox/commit/dd688348727ba158add0cc65f4a73ef3230b5c28))
* **ci:** point outline-sync at liboxapp instance and guard map coverage ([bdf7d1a](https://github.com/liboxapp/libox/commit/bdf7d1ab6412a8d5bccf19eb0a08bae15b7fa68e))
* **ci:** reevalúa la política al cambiar la base del PR ([57baede](https://github.com/liboxapp/libox/commit/57baeded6b6fae27de2375fce7378e515dd4a4bc))
* **docs:** repara los enlaces relativos tras la mudanza a docs/archive ([b54f27d](https://github.com/liboxapp/libox/commit/b54f27da47ece9190644da80927b7e494e385c3a))
* **docs:** rewrap criteria sentence that markdownlint parsed as a list ([3063f62](https://github.com/liboxapp/libox/commit/3063f62fcad55dd4fdc125926f416e8887c27efa))
* **harness:** endurecer guards de rutas y comandos para A3 ([f1122e6](https://github.com/liboxapp/libox/commit/f1122e6bdb2a87ef0853b20a4321e7af7cfe0ffa))
* **harness:** fijar dependencias y acotar entradas externas en A5 ([d9de06c](https://github.com/liboxapp/libox/commit/d9de06c3567d16b3b7b05019e08d550c8c6d7566))
* **infra:** alinear atestación y requisitos sensibles de C1 ([c762b6d](https://github.com/liboxapp/libox/commit/c762b6dacc8662223792af6cb2f04211bbbc97a5))
* **os-ia:** el guard E1 también protege artefactos versionados con guion (-V&lt;n&gt;) ([f2e1249](https://github.com/liboxapp/libox/commit/f2e124904d5bc88ddda2147686d83ab9124666da))
* **os-ia:** el guard E3 bloquea con allowlist — la decisión "ask" no protege en modo auto ([191e409](https://github.com/liboxapp/libox/commit/191e409b5e2e8629659f0f52840f7dd80944a675))
* **os-ia:** el guard permite el commit si verify_corpus.py no puede ejecutarse ([66d9722](https://github.com/liboxapp/libox/commit/66d97222b2c128682cff504abb34e69dab6d4d31))
* **os-ia:** registrar-hallazgo no manda editar el canon — el backlog de cambio vive en el doc 20 ([42b4fd6](https://github.com/liboxapp/libox/commit/42b4fd64c56cecdf70850329166a8fbbc12df1bb))
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
