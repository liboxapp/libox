---
title: C1 — MFA, recuperación, subidas y adaptadores
status: borrador
tags: [r0, c1, openapi, l3-v8, seguridad]
updated: 2026-10-01
description: Contratos de MFA, reautenticación de 5 minutos, recuperación y subidas integrados en el borrador; decisión KYB integrada y adaptador KYC/KYB pendiente de proveedor y parámetros de R1.
---

# Identidad, MFA y evidencias

Parte del [diseño de cierre](cierre-contratos.md). Parte del contrato de sesión de la
[nota de seguridad](seguridad.md): Supabase Auth actúa como proveedor de identidad y TOTP, y
Libox es dueño de la sesión aplicativa, los roles y el `aal2` interno. Las operaciones pasan por
la API de Libox (S-2); el adaptador de R1 llama al proveedor.

## MFA, sesión y recuperación, integrados

| `operationId` | Ruta | Contrato | Acceso |
|---|---|---|---|
| `listMfaFactors` | `GET /auth/mfa/factors` | Factores propios, sin secretos | `bearerAuth` |
| `enrollMfaFactor` | `POST /auth/mfa/factors` | `factor_kind: TOTP`; devuelve `otpauth_uri` una sola vez | Reautenticación; 401 `ERR_AUTH_REAUTH_REQUIRED` |
| `verifyMfaFactor` | `POST /auth/mfa/factors/{id}/verify` | `code` de 6 dígitos; sesión con `aal` igual a `aal2` | Límite de intentos |
| `challengeMfa` | `POST /auth/mfa/challenge` | `factor_id` y `code`; sesión `aal2` | Sesión `aal1` propia |
| `revokeMfaFactor` | `POST /auth/mfa/factors/{id}/revoke` | `reason` (10..500); 409 `ERR_AUTH_MFA_REQUIRED` si una cuenta interna quedaría sin factor | Reautenticación |
| `reauthenticate` | `POST /auth/reauthenticate` | `oneOf` por `method`: `PASSWORD` o `TOTP`; devuelve `valid_until`, 300 s después (A10) | Sesión propia |
| `revokeSessions` | `POST /auth/sessions/revoke` | `scope` `CURRENT` o `ALL` | Sesión propia |
| `requestRecovery` | `POST /auth/recovery` | 202 con solo `message` y `trace_id`, exista o no la cuenta (AC-04) | Pública, intercambio de credenciales |
| `completeRecovery` | `POST /auth/recovery/complete` | Revoca sesiones y no entrega tokens | Pública, intercambio de credenciales |
| `changePassword` | `POST /auth/password/change` | Contraseña actual y nueva; revoca las demás sesiones; cubre RN-05-sexies | `bearerAuth` |
| `requestInternalMfaReset` | `POST /internal-users/{id}/mfa-reset` | 202 con solicitud de firma `MFA_RESET_INTERNAL` | `ADMIN_SUPER`, sobre otra persona |

Diferencias frente al diseño anterior:

- La ventana de reautenticación es de 5 minutos, ratificada en A10. Las operaciones que pueden
  responder 401 `ERR_AUTH_REAUTH_REQUIRED` declaran `x-reauthentication-max-age-seconds: 300`.
- `logout` y `revoke-all` se unificaron en `/auth/sessions/revoke` con `scope`. Así la petición
  nunca va vacía.
- El reinicio interno no revoca el subrol (INV-38). La cuenta queda restringida hasta que vuelva
  a enrolar un factor y haga una verificación de identidad con prueba de vida.
- La recuperación del factor de un usuario externo sigue en R1.

## Ciclo de subida, integrado

| `operationId` | Ruta | Contrato |
|---|---|---|
| `createUpload` | `POST /uploads` | `Idempotency-Key` obligatoria. Recibe `purpose`, `target_id`, `content_type`, `size_bytes` y `sha256`, y devuelve una URL firmada con `status: PENDING_UPLOAD` y `version` |
| `completeUpload` | `POST /uploads/{id}/complete` | `expected_version`; deja la subida en `QUARANTINED` tras comprobar existencia, tamaño, tipo y hash |
| `getUpload` | `GET /uploads/{id}` | Estado: `PENDING_UPLOAD`, `QUARANTINED`, `ACCEPTED` o `REJECTED`; `rejection_reason` de enum cerrado |
| `getEvidenceDownloadUrl` | `GET /evidence/{id}/download-url` | URL firmada de corta vigencia; 409 `ERR_EVIDENCE_NOT_ACCEPTED` |

Valores de `purpose`:

- `ROOM_EVIDENCE`
- `DISPUTE_EVIDENCE`
- `KYB_DOCUMENT`
- `VALUATION_EVIDENCE`
- `MARKET_REFERENCE_CAPTURE`
- `PC_STAGE_DOCUMENT`
- `LEGAL_GATE_DOCUMENT`

`target_id` se interpreta según `purpose`. El cliente nunca envía `object_key`. Para pasar a
`ACCEPTED` hace falta el escaneo antimalware y la copia independiente confirmada, como exige la
[nota de operación](operacion.md).

**Pendiente, sin inventar cifras.** La lista de tipos permitidos y el tamaño máximo por
propósito los decide Diego. Hoy `content_type` solo valida la forma `tipo/subtipo`, y el tamaño
tiene únicamente el tope estructural int32. Tampoco se integró la exigencia de que
`EvidenceAttach`, `KybSubmit` y `PcStageSubmit` referencien solo subidas `ACCEPTED`: son
operaciones del inventario y el cambio acompaña a I-08.

## KYC y KYB

**Decisión KYB, integrada (A7).** `decideKyb` (`POST /clients/{id}/kyb/decisions`) la ejecuta
`ADMIN_COMPLIANCE`; `ADMIN_RISK` solo lee con `getClient`. Detalle en
[decisiones privilegiadas](cierre-contratos-decisiones.md).

**Adaptador, pendiente.** Diego priorizó Truora para evaluación; cobertura KYB y adaptador
siguen pendientes. `SubmitKybResponse.status` ya usa los estados de `client_kyb`
(`PENDING`, `APPROVED`, `REJECTED`, `EXPIRED`), sin `VERIFIED`. Esto no valida
el mapeo del proveedor. Se conserva el contrato neutral propuesto:

- `POST /identity/sessions`, con `client_action` que será `REDIRECT` o `SDK` según el flujo del
  proveedor.
- `GET /identity/verifications/{id}`, con mapeo explícito de éxito, fallo
  de identidad, expiración y revisión. Una expiración o error técnico no equivale
  a rechazo definitivo de identidad; concretar estados con el adaptador.
- `POST /webhooks/identity/{adapter_key}`.

Qué forma de `client_action` aplica depende del proveedor, así que no se fija antes. El cambio de
`submitKyb` a documentos tipados necesita el enum `document_kind` por tipo de persona. La
fila "Decisión KYB" de §7.1 se añade en V8 (I-07).

## PSP

Diego eligió **Mercado Pago** (ratificado). Resuelve I-10. El [contrato PSP](mercado-pago.md) documenta el payload,
la firma y `PspNotification` en su nota. El YAML ya incorpora ese payload externo; faltan las pruebas del adaptador real.

## Parámetros de adaptadores (R1)

Se configuran en cada adaptador; no son campos del contrato público.

| Adaptador | Parámetros por fijar |
|---|---|
| MFA (Supabase) | Número máximo de factores; vigencia del desafío; claim `aal`; si hay códigos de respaldo (verificarlo, no suponerlo) |
| Storage | Vigencia de la URL de subida; tamaño máximo; cómo forzar el tipo; destino y retardo de la copia independiente |
| Antimalware | El [paquete de proveedores](proveedores.md) no incluye ninguno. Falta fijar latencia, tipos y códigos de resultado |
| KYC | Truora priorizado para evaluación, alcance final por confirmar. Flujo, vigencia, prueba de vida, documentos PE, mapeo de resultados y firma del webhook. Retención y residencia de datos: [LEGAL→ABOGADO] |
| Correo | Plantillas y dominio de recuperación; ningún enlace revela si la cuenta existe |
