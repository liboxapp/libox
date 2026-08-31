---
paths:
  - "docs/linea-base/**"
---

# Corpus canónico (`docs/linea-base/`)

Gobernado por el Registro Maestro V6 (`LIBOX_REGISTRO_MAESTRO_LINEA_BASE_V6.md`, §1 y §4).
Si un documento no figura en su §1, no rige. La línea base está **congelada**.

- **Nunca edites un documento vigente in-place.** Todo cambio es una versión
  completa nueva `X_V<n>` → `X_V<n+1>` (CD-01, CD-02). La anterior se archiva sin
  editar (CD-08). El guard `guard_edit.py` bloquea la edición de archivos `_V<n>`
  existentes; la válvula de escape es `LIBOX_PERMITIR_INPLACE=1` en el entorno
  (o en `env` de `.claude/settings.local.json`) y solo se usa con acuerdo explícito.
- **Identidad en cuatro lugares** (CD-03): nombre de archivo, título interno, pie
  y campo de versión deben coincidir.
- **Changelog interno** con la columna "decisión que invalida" (CD-04).
- **Autonomía** (CD-06): la versión nueva no remite a la derogada para contenido normativo.
- **Emisión = un solo acto** (CD-10, CD-11): `python3 verify_corpus.py --dir docs/linea-base`
  con cero fallos + alta en `BASELINE` (`verify_corpus.py`) + Registro §1, en el mismo commit.
  Si el Registro cambia, también sube de versión.
- **Hallazgos que no justifican romper el freeze** (CD-07: solo rompe lo que impide
  construir o expone a riesgo legal/patrimonial) van al backlog de cambio o al doc 20
  de Outline (ASS-/CHANGE-/RISK-). Usa el skill `libox-registrar-hallazgo`.
- **Precedencia ante conflicto:** L0 > L2 > L3 > L4; VIES manda en identidad de marca.
- Para emitir una versión, sigue el skill `libox-versionar-doc`.
