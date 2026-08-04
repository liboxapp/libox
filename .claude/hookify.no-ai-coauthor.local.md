---
name: no-ai-coauthor
enabled: true
event: bash
pattern: git\s+commit[\s\S]*(Co-Authored-By|Generated with Claude|noreply@anthropic\.com)
action: block
---

🚫 **Trailer de co-autoría de IA detectado en el commit.**

Regla firme del repo (ver `CONTRIBUTING.md` → "Autoría: sin co-autores
automáticos"): los commits NO llevan `Co-Authored-By: Claude <...>` ni
"Generated with Claude Code" — GitHub registraría la herramienta como
contributor del repo, que se comparte con socios e inversores.

Reescribe el mensaje del commit sin el trailer y vuelve a intentar.
