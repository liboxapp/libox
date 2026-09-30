# Zonas sin generación asistida

Fuente: [Backlog MVP V3 §1.3](../../docs/linea-base/LIBOX_BACKLOG_MVP_V3.md).
Aplica a todo el repositorio y a todos los agentes, incluido Codex.

Se escriben a mano, con propiedad fija no rotatoria, en estas cinco zonas.
La segunda revisión exigida en el backlog está suspendida por la
[instrucción posterior de Diego](revision-humana.md), hasta reactivación explícita:

- Motor de sorteo, serialización canónica y verificación.
- Asientos contables y transacciones canónicas.
- Concurrencia: reserva de inventario, bloqueo de saldo y ejecución única.
- Comprobaciones de incompatibilidad de subrol en ejecución.
- Cálculo de la comisión y del impuesto incluido.

Las restricciones de rango de recaudación, régimen económico y campaña con
cupo atómico también son código de dinero y concurrencia, según el mismo apartado.
La clasificación depende del comportamiento, no del nombre de carpeta o lenguaje.
No generar ni modificar ese código; delimitar la tarea y remitirla al dueño humano.
Diego (`@DianCotrina`) es el responsable disponible. Arom B. y Martin G. se
incorporarán después; no inventar sus usuarios ni asignarles trabajo anticipadamente.
Su incorporación no reactiva la revisión humana. Solo Diego puede hacerlo
mediante una nueva instrucción explícita.

CODEOWNERS y CI no identifican por sí solos toda la semántica de un cambio.
Mantener CI, pruebas y revisión automatizada. La falta de segundo revisor no
bloquea el cierre durante la suspensión; la implementación sigue siendo humana.
