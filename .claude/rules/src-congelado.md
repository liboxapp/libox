---
paths:
  - "src/**"
  - "package.json"
  - "package-lock.json"
  - "next.config.ts"
  - "tsconfig.json"
  - "components.json"
  - "eslint.config.mjs"
  - "postcss.config.mjs"
---

# Scaffold congelado — ASS-002 abierto

El canon (L3 V7 §0.3) fija **.NET 8** como runtime; ADR Z.6 y el scaffold real son
**Next.js**. La derogación de facto de Z.6 no fue ratificada por los socios
(ASS-002, doc 20 de Outline). Hasta que se cierre:

- **No crear ni extender código** bajo `src/` ni tocar la configuración del scaffold.
  El guard `guard_edit.py` (E2) bloquea cualquier escritura en estas rutas.
  `src/**/CLAUDE.md` queda exento: es documentación, no código.
- **Excepciones admitidas:** fixes al PR #15 ya abierto y cambios que exija el CI.
  Válvula de escape: `LIBOX_DESCONGELAR_SRC=1` en el entorno o en `env` de
  `.claude/settings.local.json`, solo para esa sesión y con acuerdo explícito.
- **Cómo se levanta el freeze:** el PR que cierre ASS-002 (nueva versión de L3 o
  registro de la ratificación) borra este archivo y la constante `FROZEN_PREFIX` /
  `FROZEN_FILES` de `scripts/hooks/guard_edit.py` (con sus tests), y actualiza
  `src/CLAUDE.md`. Ese mismo PR puede añadir la capa `dev` del OS (agentes
  ejecutor/tester/depurador).
