# Revisión humana obligatoria suspendida

Instrucción explícita de Diego del 2026-09-29: desactivar la revisión humana
hasta que él la vuelva a activar explícitamente.

- No exigir una aprobación humana ni una segunda persona para integrar cambios
  o habilitar R0. Incluye CODEOWNERS y las zonas de Backlog V3 §1.3.
- No reactivar por incorporación de colaboradores, cambio de fase, auditoría,
  cierre de un PR o recomendación de un agente. Solo una nueva instrucción
  explícita de Diego permite reactivarla.
- Mantener en GitHub cero aprobaciones obligatorias, sin revisión obligatoria
  de dueños, sin aprobación obligatoria del último push ni revisores requeridos.
- Conservar CI obligatorio, pruebas y revisiones automatizadas.
- La suspensión afecta revisión, no implementación: sigue prohibida la generación
  asistida del código de las cinco zonas críticas. Tampoco levanta el freeze
  ni autoriza editar el corpus in-place.

Esta instrucción operativa posterior prevalece sobre referencias a revisión
humana obligatoria en los planes y el backlog. El corpus histórico se conserva;
la suspensión no se presenta como una nueva versión del canon.
