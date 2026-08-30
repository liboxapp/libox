---
title: Compliance Perú (documento de trabajo)
status: borrador
tags: [libox, compliance, peru, legal]
updated: 2026-07-05
---

# Compliance Perú — documento de trabajo

> ⚠️ Este es un **documento de trabajo**, no asesoría legal. Las afirmaciones aquí son lectura del autor sobre normativa pública peruana y deben ratificarse con el abogado contratado por el equipo Libox antes de tomar acción operativa.

## Propósito

El PRD del socio fue **agnóstico geográficamente** hasta V11; desde **V12.3** incluye el **Anexo K — Legal & Compliance Readiness Perú-first** (matriz regulatoria, documentos legales versionados y gates técnicos de producto: LEGAL_ACK_GATE, AGE_GATE, TAX_SPLIT_GATE, etc.). Este documento sigue siendo la pieza de trabajo con el abogado y **no queda reemplazado por el Anexo K**: el anexo define mecánica de producto, no resuelve las preguntas legales abiertas — en particular la **pregunta 0 (DL 1411)**: el Anexo K asume "autorización ante la autoridad competente" tramitada por el organizador sin identificar el marco aplicable, el mismo supuesto que esta doc marca en duda. El campo `authorization_ref` de V12 (C-11) y `Raffle.autorizacion_municipal_url` del modelo previo son el mismo supuesto y deben alinearse cuando el abogado responda. Vive separada del PRD por decisión consciente para que el PRD evolucione como blueprint técnico mientras este documento evoluciona con el abogado.

## Estado

Esqueleto inicial. Cada sección debajo es un **stub** que enumera los temas que el equipo + abogado deben cubrir, sin pretender resolverlos todavía.

---

## 1. Marco regulatorio aplicable (a confirmar con abogado)

Normativa relevante identificada:

- **Ley General del Sistema Financiero — Ley 26702**: define qué actividades requieren autorización SBS. Captar fondos del público es la actividad central regulada.
- **Ley de Dinero Electrónico — Ley 29985** y su reglamento: define las Empresas Emisoras de Dinero Electrónico (EEDE).
- **Reglamento de las EEDE — Res. SBS 6283-2013**: capital mínimo (~S/ 2.25M histórico), fideicomiso de respaldo, oficial de cumplimiento, auditoría externa.
- **Régimen PLAFT — Res. SBS 789-2018** y modificatorias: prevención de lavado de activos y financiamiento del terrorismo.
- **Sujetos obligados ante UIF-Perú — Ley 27693** y modificatorias: incluye administradores de juegos de azar y apuestas.
- **Régimen tributario SUNAT**: IGV, factura electrónica vía PSE, retención de IR de 2da categoría sobre premios.
- **Marco municipal de sorteos / rifas**: autorización municipal para rifas con boleto pagado (varía por municipalidad).
- **DL 1411 (y modif. DU 009-2020) — juegos de lotería y similares** `[LEGAL→ABOGADO]`: reserva la organización de loterías y juegos similares a las **Sociedades de Beneficencia**, directamente o vía contratos de asociación en participación con operadores privados (cargas: 1% de ventas brutas al MIMP; ≥5% a la Beneficencia en contratos de asociación). Lectura del autor: una **rifa lucrativa con boleto pagado podría calificar como "lotería y similar"**, en cuyo caso un organizador privado con RUC no podría venderla por cuenta propia y la autorización municipal no bastaría.
- **DS 010-2016-IN (MININTER/DGIN)** `[LEGAL→ABOGADO]`: regula **promociones comerciales** (sorteos gratuitos ligados a compra), **rifas con fines sociales** (sin lucro) y colectas públicas, con autorización y garantía. No cubre rifas lucrativas.

### Preguntas para abogado

0. **(Prioritaria — condiciona el modelo de negocio)** ¿Una rifa con boleto pagado y fin de lucro califica como "juego de lotería y similares" bajo el **DL 1411** (exclusivo de Sociedades de Beneficencia), o basta la autorización municipal que asume el modelo actual? Si aplica el DL 1411: ¿qué vía habilita el marketplace — asociación en participación con una Beneficencia, restricción a rifas con fin social (DS 010-2016-IN), o reformulación como promoción comercial? ⚠️ La respuesta **tensiona la decisión cerrada [Z.3](decisions/Z3-tipo-de-organizador.md)** ("cualquier RUC activo puede organizar") y el KYC del propio PSP, que suele exigir acreditar la autorización del rubro juegos.
1. ¿Operar un marketplace de rifas con boleto pagado bajo organizador RUC califica a Libox como **sujeto obligado UIF-Perú** (administrador de juegos de azar)? Si sí, se requiere oficial de cumplimiento PLAFT y manual **desde día 1**, sin importar el modelo de custodia. Nota: si la vía resultara ser asociación con Beneficencia (pregunta 0), la probabilidad de calificar como sujeto obligado aumenta.
2. ¿Bajo el [Modelo C de custodia](decisions/Z1-custodia-del-dinero.md), la actividad de Libox queda fuera del régimen SBS de captación de fondos del público?
3. ¿Qué califica como "rifa" vs "sorteo promocional" para el municipio / MINCETUR, y cuáles aplican a Libox?
4. ¿Qué umbrales de monto activan retención de IR de 2da categoría sobre el premio, y quién debe ejecutar la retención (organizador o Libox)?
5. ¿Es obligatorio el acta notarial del sorteo, o se admite acta digital con firma cripto-verificable?

---

## 2. Facturación electrónica SUNAT

- ¿Quién emite el comprobante al participante por la compra del boleto?
  - Bajo Modelo C (operativa marketplace): probablemente el **organizador** factura al participante (factura electrónica B2B si el participante también es RUC, boleta si es persona natural).
  - Libox factura comisión **al organizador** (siempre B2B con RUC).
- PSE candidatos: Nubefact, Defontana, Bizlinks, Facturador SUNAT (gratuito pero limitado).
- Volúmenes esperados, criterios de selección de PSE: pendiente.

---

## 3. Autorización del sorteo

> ⚠️ `[LEGAL→ABOGADO]` Esta sección asume que la **autorización municipal habilita la rifa pagada**. Ese supuesto está en duda por el DL 1411 (ver pregunta 0 de la sección 1): si la rifa lucrativa califica como "lotería y similar", la vía no sería municipal. El campo `Raffle.autorizacion_municipal_url` del modelo de datos hereda este supuesto.

- Sorteos con boleto pagado típicamente requieren autorización municipal. La municipalidad varía por jurisdicción del organizador.
- En el modelo de datos del MVP, el campo `Raffle.autorizacion_municipal_url` ya está previsto: el organizador sube el documento al crear el sorteo, y la aprobación admin no se concede sin él.
- Cobertura geográfica: si Libox opera nacional, cada sorteo debe declarar su jurisdicción municipal de origen.

### Preguntas para abogado

1. ¿Existe un trámite homologado entre municipalidades, o cada una tiene su propio procedimiento?
2. ¿Libox como plataforma necesita una autorización aparte, o solo el organizador?
3. ¿Hay un umbral de monto del premio o cantidad de boletos que active obligaciones adicionales (MINCETUR, otros)?

---

## 4. Retención y declaración de impuestos sobre el premio

- Premios > X monto activan retención de IR de 2da categoría (X = umbral legal vigente).
- ¿Quién retiene: organizador o Libox?
  - Bajo Modelo C, Libox no toca el dinero del premio, así que la retención debería ejecutarla el organizador. Confirmar con abogado.
  - Libox podría tener obligación de **reportar** las operaciones aunque no retenga.

---

## 5. KYC

### KYC del organizador (al onboarding)

- Validación de RUC contra el padrón SUNAT (API pública).
- Documentos: ficha RUC, representante legal con DNI, vigencia de poderes si jurídica.
- Posibles fuentes para verificación adicional: SBS, INDECOPI.

### KYC del participante

- Identificación básica al registro (email + verificación).
- DNI obligatorio solo al momento de ganar un premio por encima de cierto umbral (para retención y declaración).
- Persona extranjera: pasaporte / CE.

### KYC del ganador (al momento del pago del premio)

- Si premio > umbral legal: DNI + datos completos para reportes UIF/SUNAT.

---

## 6. PLAFT / UIF-Perú

- Si Libox califica como sujeto obligado:
  - Oficial de cumplimiento titulado.
  - Manual PLAFT.
  - Sistema de reporte de operaciones sospechosas a la UIF.
  - Capacitación de personal.
- Si no califica: aún así, **buenas prácticas** sugieren registro de operaciones sobre cierto umbral y due diligence reforzado para organizadores con riesgo elevado.

---

## 7. Auditabilidad legal del sorteo

- El [PRD Libox v11](prd/) propone proof criptográfico reproducible (`pool_hash + external_entropy + seed_material + random_value`).
- Pregunta clave para abogado: **¿esta evidencia digital es suficiente ante una eventual disputa, auditoría municipal, o requerimiento SUNAT, o se necesita acta notarial física complementaria?**
- Si se necesita notario: integración con notario digital (Reniec / notaría que firme electrónicamente) o notario presencial agendado.

---

## 8. Términos y Condiciones

- T&C del participante deben declarar explícitamente:
  - El modelo de custodia de Libox ([Modelo C](decisions/Z1-custodia-del-dinero.md): Libox no custodia fondos; el organizador es responsable de la entrega del premio).
  - Mecanismo de disputa.
  - Manejo de datos personales (Ley 29733 de Protección de Datos Personales).
  - Jurisdicción aplicable.

- Contrato B2B con el organizador debe cubrir:
  - Obligaciones del organizador respecto al premio y su entrega.
  - Causales de baneo del marketplace.
  - Manejo de reembolsos cuando el sorteo se cancela.
  - Comisión y forma de cobro.

---

## 9. Próximos pasos concretos

1. Compartir este documento con el abogado al momento de su contratación.
2. Trabajar con el abogado punto por punto para convertir los stubs en decisiones cerradas.
3. Cuando una decisión se cierre, moverla al [Anexo Z del plan](plans/libox-plan.md) y/o crear un ADR en [`decisions/`](decisions/).
