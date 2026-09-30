Instrucciones compartidas de Libox.

Lee `CLAUDE.md` y las reglas aplicables en `.claude/rules/` antes de trabajar.
El corpus y el scaffold conservan sus restricciones de cambio.
Para auditorías usa `.claude/skills/libox-system-design-audit/SKILL.md` en modo
revisor Codex y `docs/equipo/ai-audit-harness.md`. No simules revisiones de Claude.

## Stack y controles para Codex

Backend TypeScript ratificado: monolito modular con Next.js y PostgreSQL.
Proveedores a confirmar en C1; canon L3 V8 y levantamiento del freeze pendientes.
Lee el [programa de R0](docs/superpowers/specs/2026-09-25-habilitar-r0-design.md).
La mención de ASS-002 abierto en la regla antigua no revoca la ratificación.

Los hooks de `.claude/settings.json` no se ejecutan automáticamente en Codex.
No asumas que sus guards bloquean tus herramientas: aplica las mismas reglas
antes de escribir. Los checks obligatorios de CI son la barrera de integración
común; no son un sandbox local ni sustituyen la revisión humana.

## Zonas sin generación asistida

Backlog MVP V3 §1.3: implementación humana y revisión de otra persona, con
propiedad fija, para estas cinco zonas:

- Motor de sorteo, serialización canónica y verificación.
- Asientos contables y transacciones canónicas.
- Concurrencia: reserva de inventario, bloqueo de saldo y ejecución única.
- Comprobaciones de incompatibilidad de subrol en ejecución.
- Cálculo de comisión e impuesto incluido.

Incluye las restricciones de rango de recaudación, régimen económico y campaña
con cupo atómico. Aplica por comportamiento, aunque cambien la ruta o el lenguaje.
No generes ni modifiques su código; delimita la tarea y remítela al dueño humano.
El detalle compartido está en [.claude/rules/zonas-sin-ia.md](.claude/rules/zonas-sin-ia.md).
Diego es el único responsable actual; el segundo revisor está pendiente.
No interpretes las cero aprobaciones requeridas en GitHub como una excepción
al backlog. Una revisión por otro agente no sustituye a la segunda persona.

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
