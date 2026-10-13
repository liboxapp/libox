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

## Excepción acotada · instrucción de Diego del 2026-10-13

Claude puede redactar el código que cierra INV-01, INV-36, RN-45, RN-96, RN-147
e INV-25 (refutaciones R-14, R-15, R-16, R-10, R-04 y R-12 de la batería V18).
Diego confirma cada cambio antes de integrarlo. Cada regla se cierra cuando su
refutación imprime NO REPRODUCIDO y la batería sigue en verde en PostgreSQL 16
y 17. No se extiende a otras reglas ni zonas, ni levanta los congelamientos de
src/ y docs/linea-base/.
