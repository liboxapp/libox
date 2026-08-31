---
name: libox-versionar-doc
description: Emite una nueva versión completa de un documento del corpus canónico (docs/linea-base) cumpliendo CD-01..CD-11. Úsalo siempre que haya que cambiar cualquier documento o artefacto de la línea base.
---

# Versionar un documento del canon

Entrada: `$ARGUMENTS` = nombre del archivo vigente (p. ej. `LIBOX_BACKLOG_MVP_V3.md`) y el motivo.

1. **Justifica el freeze.** La línea base está congelada (CD-07). Solo se emite si el
   cambio impide construir o expone a riesgo legal/patrimonial. Si no, detente y usa
   `libox-registrar-hallazgo` (queda en backlog de cambio / doc 20) — informa al usuario.
2. **Crea la versión siguiente.** Copia `X_V<n>.md` → `X_V<n+1>.md` (CD-01/02). No edites
   la anterior (CD-08; el guard E1 lo impide).
3. **Identidad en cuatro lugares** (CD-03): nombre de archivo, título interno, pie y
   campo de versión de la interfaz deben decir `V<n+1>`.
4. **Changelog interno** (CD-04): añade la fila con fecha, cambio y la decisión que
   invalida (ASS-/CHANGE-/RISK- o "hallazgo de construcción").
5. **Autonomía** (CD-06): la versión nueva no remite a la derogada para nada normativo.
6. **Registro y BASELINE en el mismo acto** (CD-11): actualiza `BASELINE` en
   `verify_corpus.py` (versión + archivo) y el §1 del Registro Maestro. Como el Registro
   es un documento del canon, también sube de versión (repite 2–5 para él).
7. **Verifica** (CD-10): `python3 verify_corpus.py --dir docs/linea-base` hasta
   `RESULTADO: sin fallos`. El guard B3 bloquea el commit si no.
8. **Integra:** rama `docs/<slug>`, commit `docs(canon): emite <DOC> V<n+1> — <motivo>`,
   PR con `libox-pr`. Deja la versión anterior en su sitio (el Registro §2 la marca derogada).
9. **Tras el merge:** pide al humano correr `/libox-outline-sync` para republicar el espejo.
