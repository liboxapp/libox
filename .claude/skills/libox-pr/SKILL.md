---
name: libox-pr
description: Integra trabajo terminado — comprueba rama, correo y commits, sube la rama y abre el Pull Request con la plantilla del equipo (sin trailers de IA). Úsalo cuando el trabajo esté verificado y listo para revisión.
---

# Abrir un Pull Request conforme

1. **Comprobaciones** (todas deben pasar; si una falla, corrígela antes de seguir):
   - `git branch --show-current` ≠ `main` y con formato `<type>/<kebab>`.
   - `git config user.email` termina en `@liboxapp.com`.
   - `git log origin/main..HEAD --format=%B` no contiene `Co-Authored-By`, `Generated with`
     ni `noreply@anthropic.com`; cada asunto sigue Conventional Commits en español.
   - Árbol limpio (`git status --porcelain` vacío) y verificación del cambio ya ejecutada
     (tests, `verify_corpus.py` si tocó el canon, `markdownlint` si tocó `docs/`).
2. **Sube la rama:** `git push -u origin $(git branch --show-current)` (si ya existía y se
   rebasó: `--force-with-lease`).
3. **Abre el PR** con `gh pr create --base main --title "<type>(<scope>): <resumen>" --body-file <archivo>`
   cuyo cuerpo sigue exactamente:

   ```
   ## Qué
   <una o dos frases>

   ## Por qué
   <motivo, hallazgo o decisión que lo origina; enlaza spec/ADR/ASS si existe>

   ## Verificación
   - [ ] <comando ejecutado y resultado>
   ```

   Nunca añadas "Generated with Claude Code" ni menciones de la herramienta.
4. **Devuelve** la URL del PR y, si el CI tiene checks requeridos, recuerda que el merge es
   rebase-and-merge.
