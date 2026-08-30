# LIBOX · Línea base documental vigente

**Fecha del paquete:** 7 de agosto de 2026
**Verificación:** `verify_corpus.py` ejecutado con **cero fallos y cero avisos** antes de empaquetar.

---

## Regla de uso

> **Si un documento no figura en el §1 del Registro Maestro, no rige.**

Sin excepción y sin interpretación. **Empieza por `00_CONTROL/`**: ese documento responde qué está vigente, qué es histórico nulo y qué artefacto existe.

Toda versión distinta a las de este paquete está derogada, aunque siga circulando.

---

## Contenido

### `00_CONTROL/`
**Registro Maestro de Línea Base V6** — qué rige y qué es nulo. **Léelo primero.**

### `L0_RECTOR/`
**Behavioral Product Framework LBPF V3** — axiomas, nueve derechos conductuales, trece principios, límites y gobernanza. **Prevalece sobre todo el corpus.**

### `L1_ESTRATEGIA/`
**Product Strategy V3** — tesis, estructura competitiva, segmentos, comisión y su escala, costos, captación e hipótesis con criterio de falsación.

### `L2_PRODUCTO/`
**PRD Blueprint MVP V9** — contrato de construcción. 49 invariantes, 304 reglas de negocio, 62 superficies.
**PRD Blueprint Enterprise V3** — direccional. **No ejecutable.**

### `L3_TECNICO/`
**Especificación Técnica V7** — esquema, contratos, máquina de estados, motor de sorteo, contabilidad, control de acceso.
**Matriz de Casos de Uso, Permisos y SLA V1** — 107 casos en 12 procesos.
**Guía de Extensión y Puntos de Cambio V1** — dónde se toca cada cosa y qué nivel de cambio exige.

### `L4_EXPERIENCIA/`
**Design System & Product Experience Standard V2** — tokens, 22 componentes, movimiento, accesibilidad y manual de redacción.

### `AUX_MARCA/`
**Visual Identity Engineering Standard V3** — identidad de marca. Arte congelado.

### `PLAN/`
**Backlog MVP V3** en documento y hoja de cálculo — 136 historias, 936 SP, 30 sprints.

### `ARTEFACTOS/`
Archivos que se consumen, no que se leen.

| Archivo | Estado |
|---|---|
| `libox_schema_L3_V7.sql` | **135 tablas, cero errores en PostgreSQL 16, 13 pruebas negativas superadas** |
| `libox_openapi_L3_V7.yaml` | **16 rutas de ~30. Incompleto** — pendiente T-1, 8 SP |
| `libox-design-tokens-L4-V2.json` | 21 claves, 14 componentes |
| `verify_corpus.py` | Verificador de coherencia, 10 controles. **Regla CD-10** |

### `REGISTROS_DECISION/`
No normativos. Consignan por qué se decidió lo que se decidió.

**Dossier Legal V1** — insumo para el encargo de asesoría. Tres estructuras vivas y 22 preguntas.
**Evaluación de Comité y Equipo Técnico V1** — veredicto de viabilidad y condiciones de entrega.
**Auditoría Global de Coherencia V1** — los cuatro conflictos de invariante resueltos antes de emitir.
**Auditoría de Coherencia Post-Emisión V1** — el desfase de L4 y el invariante huérfano.

---

## Precedencia ante conflicto

```
L0  sobre todo
L2  sobre L4 en materia de reglas
L3  sobre L4 en materia técnica
VIES sobre L4 en identidad de marca
```

Ningún nivel puede crear reglas del nivel superior. Si una necesidad de experiencia exige una regla nueva, se eleva a L2 y se incorpora allí.

---

## Versionado

**V1 → V2 → V3.** No existen subversiones. Un número de versión nunca se reutiliza. Todo documento lleva changelog con la columna *decisión que invalida*.

**Regla CD-10:** ninguna versión se emite sin que `verify_corpus.py` pase con cero fallos. La lista `BASELINE` del script es la única fuente de verdad de qué versión rige, y actualizarla es parte del acto de emitir.

---

## Estado del proyecto

**Documentación:** completa y congelada. Los cinco niveles con documento.
**Base técnica:** lista. El sprint 0 puede arrancar.

**Pendientes críticos, ninguno documental:**

| # | Pendiente | Bloquea |
|---|---|---|
| 1 | **Dictamen legal L-01.** El dossier está listo; falta enviarlo | Operar con dinero real |
| 2 | **F0: veinte conversaciones con organizadores.** Cero a la fecha | Validar la hipótesis central |
| 3 | Completar `openapi.yaml` — 8 SP mecánicos | Sprint 4 |
| 4 | Diseño de 41 de 62 superficies — 4 a 6 semanas | Frontend. **Fuera del plan en SP** |
| 5 | Arte maestro de marca | Piezas visuales oficiales |
| 6 | Manual de operación — 13 SP | Operar, no construir |

**Los puntos 1 y 2 no cuestan ingeniería y pueden empezar esta semana.** Son, con diferencia, los de mayor retorno pendiente.
