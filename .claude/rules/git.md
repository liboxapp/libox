# Git y Pull Requests

Normativo: `CONTRIBUTING.md`. Resumen operativo:

- **Rama por cambio:** `<type>/<kebab>` desde `main` actualizado. Nunca commits ni
  push directos a `main` (el guard B2 y la regla hookify lo bloquean).
- **Conventional Commits en español** (`feat`, `fix`, `docs`, `chore`, `ci`,
  `refactor`, `test`), cuerpo que explica el porqué. Los valida `commitlint` en CI.
- **Correo de autoría `@liboxapp.com`** (`git config user.email`). El guard B4 lo
  exige antes de commitear; el CI rechaza commits con otros dominios.
- **Sin trailers de IA:** nunca `Co-Authored-By: Claude ...` ni "Generated with
  Claude Code" (guard B1 + hookify). La autoría es de quien revisa y firma.
- **Si el commit toca `docs/linea-base/` o `verify_corpus.py`**, el guard B3 corre
  `verify_corpus.py` y bloquea si hay fallos (CD-10).
- **PR:** `gh pr create` con cuerpo *Qué / Por qué / Verificación*; rebase-and-merge;
  ramas en vuelo se rebasan (`git push --force-with-lease`). Usa el skill `libox-pr`.
