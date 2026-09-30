---
title: Dependencias fijadas del harness
status: vigente
tags: [harness, dependencias, seguridad]
updated: 2026-09-29
description: Versiones y evidencia de procedencia para actions, Outline CLI y context-mode; límites y actualización.
---

# Dependencias fijadas del harness

A5 del [programa R0](../superpowers/specs/2026-09-25-habilitar-r0-design.md).
Verificación de origen del 2026-09-29: API pública de GitHub
`GET /repos/{owner}/{repo}/commits/{tag}` y JSON oficial de PyPI.
Los tags de la tabla son contexto; los workflows ejecutan los SHA completos.

| Dependencia | Ref consultada | Commit fijado |
|---|---|---|
| [actions/checkout](https://api.github.com/repos/actions/checkout/commits/v4) | v4 | `11d5960a326750d5838078e36cf38b85af677262` |
| [actions/setup-python](https://api.github.com/repos/actions/setup-python/commits/v5) | v5 | `a26af69be951a213d495a4c3e4e4022e16d87065` |
| [wagoid/commitlint-github-action](https://api.github.com/repos/wagoid/commitlint-github-action/commits/v6) | v6 | `b948419dd99f3fd78a6548d48f94e3df7f6bf3ed` |
| [DavidAnson/markdownlint-cli2-action](https://api.github.com/repos/DavidAnson/markdownlint-cli2-action/commits/v16) | v16 | `b4c9feab76d8025d1e83c653fa3990936df0e6c8` |
| [lycheeverse/lychee-action](https://api.github.com/repos/lycheeverse/lychee-action/commits/v2) | v2 | `e7477775783ea5526144ba13e8db5eec57747ce8` |
| [googleapis/release-please-action](https://api.github.com/repos/googleapis/release-please-action/commits/v4) | v4 | `5c625bfb5d1ff62eadeeb3772007f7f66fdcf071` |
| [mksglu/context-mode](https://api.github.com/repos/mksglu/context-mode/commits/v1.0.169) | v1.0.169 | `589d8214d56740a28b5f7bf63167743d586b0b40` |

## Outline CLI

`outline-kb-cli==0.1.5`, verificado en
[PyPI oficial](https://pypi.org/pypi/outline-kb-cli/0.1.5/json).
El wheel `outline_kb_cli-0.1.5-py3-none-any.whl` declara SHA-256
`6b7f4eda510d9096abc243f4d1eaf2bcb87d203db130f6ad64450a00bb6eba05`.
Se inspeccionó el parser del wheel para las consultas de la skill.
CI fija versión directa; dependencias transitivas y runtime del runner no quedan
congelados por este cambio. El digest usa solo biblioteca estándar de Python.

## Marketplace de terceros

La [referencia oficial de Claude Code](https://code.claude.com/docs/en/plugins/marketplace-reference)
distingue catálogo y plugin: el catálogo git acepta `ref` (rama/tag), y el plugin
GitHub acepta `sha`. No añadir un campo `sha` no soportado al catálogo.
El catálogo `settings` permite declarar el plugin GitHub con el SHA anterior,
sin depender de un tag mutable. La versión del manifest verificada es `1.0.169`.
La configuración compartida no reemplaza automáticamente cachés personales ya
instaladas: comprobar el plugin resuelto al actualizar cada entorno.

## Actualización y límites

Actualizar deliberadamente: comprobar origen y manifest, revisar cambios,
actualizar SHA o versión y esta evidencia, ejecutar las pruebas de hooks y CI.
Los pins reducen cambios remotos silenciosos; no certifican el comportamiento
interno de una action, sus descargas, sus dependencias o el proveedor.

El digest aplica un presupuesto total de seis segundos a sus subprocessos, no
hace `fetch` y usa referencias locales potencialmente desactualizadas. Serializa
PR, autores, ramas y asuntos como registros JSON `DATA` acotados; neutraliza
controles, saltos y delimitadores Markdown/HTML. Ningún texto remoto se convierte
en comando. Esto reduce inyección de formato, pero no garantiza que un modelo
ignore semánticamente toda instrucción maliciosa: los registros se marcan como
datos no confiables y no otorgan autoridad.

La skill de Outline es solo lectura. Registrar hallazgos requiere una solicitud
explícita de escritura externa; esa solicitud ya autoriza el registro descrito.
No reactiva la revisión humana de desarrollo suspendida.
