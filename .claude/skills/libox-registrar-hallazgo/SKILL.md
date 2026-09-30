---
name: libox-registrar-hallazgo
description: Registra un supuesto (ASS-), solicitud de cambio (CHANGE-), riesgo (RISK-) o idea (IDEA-) en el doc 20 de Outline y, si aplica, en el backlog de cambio (CD-07), sin abrir una versión del canon. Usar solo ante solicitud explícita del usuario de registrar un hallazgo.
disable-model-invocation: true
---

# Registrar un hallazgo

Entrada: `$ARGUMENTS` = descripción libre del hallazgo.

La invocación explícita de este skill o una solicitud explícita de registrar el
hallazgo autoriza la escritura externa descrita, sin pedir confirmación repetida.
Si solo se detectó un hallazgo y no existe esa autorización, preparar y mostrar
un borrador con destino y texto; solicitar autorización antes de escribir en Outline.
Esta autorización de escritura externa no es revisión humana del código ni
reactiva la revisión humana de desarrollo suspendida.

1. **Clasifica** con una sola etiqueta:
   - `ASS-` supuesto sobre el que se está construyendo y que alguien debe ratificar.
   - `CHANGE-` cambio propuesto a un documento del canon (va también al backlog de cambio).
   - `RISK-` riesgo con probabilidad e impacto.
   - `IDEA-` idea de producto/negocio sin compromiso.
2. **Localiza el registro** en Outline (MCP): colección "Libox — Negocio", documento cuyo
   título empieza por `20` (registro de asunciones y cambios). Usa `list_documents` /
   búsqueda por título; lee la última entrada para tomar el siguiente número correlativo.
3. **Redacta la entrada** con esta plantilla y añádela al final de la tabla del tipo
   correspondiente con `update_document` (no reescribas el resto del documento):

   | ID | Fecha | Origen | Descripción | Impacto | Dueño | Estado |
   |---|---|---|---|---|---|---|
   | `<TIPO>-<nnn>` | `YYYY-MM-DD` | doc/sección o PR que lo originó | una o dos frases | qué bloquea o qué cambia si se confirma | persona | `abierto` |

4. **Si es `CHANGE-`**, márcala en el doc 20 como candidata al **backlog de cambio** (CD-07):
   añade la columna/etiqueta `backlog: sí` en la fila y enlaza el documento del canon afectado
   por nombre (p. ej. `LIBOX_BACKLOG_MVP_V3.md`). **El canon no se toca**: ningún archivo de
   `docs/linea-base/` se edita in-place; cuando el cambio se apruebe, se aplica emitiendo la
   versión siguiente con `libox-versionar-doc`.
5. **Devuelve al usuario** el ID asignado, el enlace al documento y la frase exacta registrada.
