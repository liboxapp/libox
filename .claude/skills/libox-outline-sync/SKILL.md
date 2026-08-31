---
name: libox-outline-sync
description: Republica en Outline los documentos de docs/ que tienen espejo, creando el doc en Outline y registrando su ID en scripts/outline-map.json cuando aún no está mapeado. Solo lo invoca un humano tras un merge en main.
disable-model-invocation: true
---

# Sincronizar el espejo de Outline

Publica fuera del repo: por eso solo lo dispara un humano. Entrada: `$ARGUMENTS` =
rutas a sincronizar (vacío = todas las mapeadas).

1. **Precondiciones:** estás en `main` actualizado (`git pull --ff-only`); `OUTLINE_API_KEY`
   y `OUTLINE_BASE_URL` están en el entorno o en `~/.outline-skills/config.json`.
2. **Detecta archivos sin mapear:** para cada ruta pedida, comprueba si existe como clave en
   `scripts/outline-map.json`. Si no existe:
   a. Crea el documento en Outline con el MCP (`create_document`) en la colección
      "Libox — Negocio", bajo el árbol **Desarrollo**, con el título del frontmatter y un
      cuerpo provisional de una línea.
   b. Añade `"<ruta>": "<id>"` al mapa y commitea: `chore(outline): mapea <ruta>` (rama +
      PR; el mapa vive en el repo).
3. **Sincroniza:** `scripts/outline-sync.sh <rutas>`. Lee la salida: `synced:` es éxito;
   `skip (not mapped)` significa que falta el paso 2; `skip (missing on disk)` señala una
   entrada del mapa cuyo archivo ya no existe (p. ej. rutas movidas a `docs/archive/`):
   propón al humano remapearla o quitarla.
4. **Reporta:** lista de documentos publicados con su enlace y las entradas huérfanas detectadas.
