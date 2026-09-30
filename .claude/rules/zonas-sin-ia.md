# Zonas sin generación asistida

Fuente: [Backlog MVP V3 §1.3](../../docs/linea-base/LIBOX_BACKLOG_MVP_V3.md).
Aplica a todo el repositorio y a todos los agentes, incluido Codex.

Se escriben a mano y se revisan por una segunda persona. Propiedad fija,
no rotatoria, en estas cinco zonas:

- Motor de sorteo, serialización canónica y verificación.
- Asientos contables y transacciones canónicas.
- Concurrencia: reserva de inventario, bloqueo de saldo y ejecución única.
- Comprobaciones de incompatibilidad de subrol en ejecución.
- Cálculo de la comisión y del impuesto incluido.

Las restricciones de rango de recaudación, régimen económico y campaña con
cupo atómico también son código de dinero y concurrencia, según el mismo apartado.
La clasificación depende del comportamiento, no del nombre de carpeta o lenguaje.
No generar ni modificar ese código; delimitar la tarea y remitirla al dueño humano.
Una revisión de otro agente no satisface la segunda revisión humana.

Diego (`@DianCotrina`) es el único responsable disponible. La asignación de dueño
fijo y segundo revisor por zona se completará cuando se incorporen Arom B. y
Martin G.; no inventar sus usuarios de GitHub ni asignarles trabajo anticipadamente.
Mientras tanto no declarar cerradas las entregas de esas zonas.

CODEOWNERS y CI no identifican por sí solos toda la semántica de un cambio.
La configuración temporal de cero aprobaciones obligatorias evita bloquear PRs
de preparación; no deroga esta regla ni el canon.
