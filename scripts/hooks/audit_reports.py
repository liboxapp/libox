"""Clasificación E5: informes existentes son inmutables por herramientas de edición."""
from pathlib import Path


NON_REPORTS = {'manifest.md', 'checks.md', 'codex-prompt.md'}


def _report_path(candidate):
    parts = [part.casefold() for part in candidate.parts]
    return (candidate.suffix.casefold() == '.md'
            and candidate.name.casefold() not in NON_REPORTS
            and any(parts[index:index + 2] == ['docs', 'audits']
                    for index in range(len(parts) - 3)))


def is_existing_report(path):
    """Reconoce rutas léxicas y resueltas; incluye intentos y síntesis, sin escape env."""
    path = Path(path)
    if not (path.exists() or path.is_symlink()):
        return False
    # Evaluar la ruta léxica antes de resolver: un ciclo de symlink no debe
    # convertir un informe conocido en un error que active fail-open del guard.
    if _report_path(path.absolute()):
        return True
    try:
        return _report_path(path.resolve())
    except (OSError, RuntimeError):
        return False
