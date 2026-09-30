---
title: C1 — borrador de seguridad, sesiones y evidencias
status: borrador
tags: [r0, c1, l3-v8]
updated: 2026-09-30
description: Cambios explícitos del contrato de auth y propuestas de protección de datos y sorteo.
---

# Seguridad propuesta para L3 V8

## Autenticación y autorización (§7.3)

Recomendación: Supabase Auth como proveedor de identidad y TOTP; Libox conserva
roles, permisos por recurso, incompatibilidades y sesión aplicativa. Exigir aal2
para cada acceso interno protegido. Enrolar MFA no basta para exigirlo.
[Supabase MFA](https://supabase.com/docs/guides/auth/auth-mfa).

| L3 V7 | Diferencia verificada | Propuesta V8 pendiente de decisión |
|---|---|---|
| Token de acceso de 15 min | Supabase permite configurarlo; un JWT puede sobrevivir al timeout de sesión | JWT de 15 min y comprobación autoritativa de sesión/rol en operaciones internas |
| Refresh rotatorio de 30 días | Refresh no expira por sí solo; timebox limita sesión | Sesión máxima de 30 días, comprobada por Libox además del proveedor |
| Todo reuse revoca familia y emite riesgo | Supabase admite ventana de reutilización de 10 s y token padre activo | Documentar excepciones; definir puente verificable al evento de riesgo Libox |
| Inactividad interna de 30 min | Timeout del proveedor mide renovación, no interacción humana | Sesión aplicativa expira por falta de actividad humana, sin contar refresh/polling |
| Argon2id del diseño de identidad | Supabase gestiona passwords con bcrypt | Si se elige Supabase, registrar sustitución explícita; Libox no mantiene segunda copia de password |

[Sesiones](https://supabase.com/docs/guides/auth/sessions),
[passwords](https://supabase.com/docs/guides/auth/password-security).
No afirmar equivalencia literal. Alternativa Clerk: token de 60 s, otro modelo de sesión;
soporta app nativa pero tampoco acredita la familia de refresh descrita por L3.
[Modelo Clerk](https://clerk.com/docs/guides/how-clerk-works/overview),
[Expo](https://clerk.com/docs/expo/reference/objects/session).

Sesión aplicativa: revocación y cambios de rol efectivos en el siguiente acceso
interno; actividad aceptada solo desde solicitudes autenticadas de interacción,
no un heartbeat que pueda extender indefinidamente. Reautenticación/MFA reciente
para acciones sensibles. Tokens nunca en logs ni URLs. Backend valida issuer,
audience, firma, expiración y sesión; no confía en claims de rol obsoletos.
No exponer tablas de dominio al cliente con service-role ni acceso directo amplio.

INV-38 se conserva: mínimo dos ADMIN_SUPER activos, prohibida revocación del
penúltimo. La excepción de revisión humana del repositorio no permite debilitar
este control del producto. R0 puede usar identidades sintéticas en pruebas; antes
de operar hay que resolver el bootstrap conforme al PRD, sin cuentas ficticias reales.

## DNI, evidencias y transporte

Proponer HMAC-SHA-256 del DNI normalizado con secreto fuera de DB; incluir versión
de clave y mercado/tipo de documento en la definición canónica de entrada. Fijar
normalización exacta por tipo de documento, sin inventar ceros o formatos regionales.
Rotar con período de coexistencia controlado; no reemplazar hashes sin estrategia
de búsqueda/migración. No registrar DNI, payloads KYC o claves en telemetría.

Buckets privados, autorización por objeto y URLs firmadas de corta vigencia;
propuesta inicial de 5 min para descarga, sin usarlas como permiso permanente.
Tamaño, tipo y hash verificados antes de marcar evidencia recibida; cuarentena para
validación y malware. URLs y evidencias no van en caches públicos. DB PITR no cubre
objetos: aplicar recuperación independiente descrita en [operación](operacion.md).
Retención por clase de documento y base legal: [LEGAL→ABOGADO]; no activar retención
indefinida irreversible sobre datos personales sin decisión de conservación.

TLS para cliente/API/DB; cookies web Secure/HttpOnly/SameSite adecuadas cuando se
usen y defensa CSRF. Portabilidad nativa conserva Bearer, sin dependencia exclusiva
de cookies. CSP se define según los orígenes reales de pago/identidad, comienza con
medición y se exige antes de producción; no usar comodines para cerrar el check.

Rate limiting propuesto: login/recuperación por cuenta seudónima+IP, mutaciones por
usuario+recurso, lectura pública por IP y protección perimetral. Umbrales se fijan
tras pruebas, con 429/Retry-After; indisponibilidad del limitador no decide inventario
ni saldo. Webhook válido se persiste/deduplica; no se descarta un pago solo por IP.

## Compromiso, baliza y pago tardío (§5/§12)

Separar identificador de red/ronda, instante programado y bytes de aleatoriedad.
El verificador consulta la ronda comprometida y valida autenticidad de la baliza;
no acepta únicamente retrieved_at suministrado por Libox. Fuente, suite de firmas,
serialización y codificación quedan como parámetros de una especificación cerrada
por el dueño del motor antes de generar resultados esperados.

Seed: cifrado autenticado mediante gestión de claves separada; ciphertext,
identificador/versión de clave y referencia al sorteo persistidos antes de publicar
compromiso. Restringir descifrado al ejecutor autorizado; el plaintext no llega a
logs/backups sin cifrado. Probar restore de clave+datos. No implementar aquí motor,
serialización ni verificación, que siguen siendo zonas sin generación asistida.

Propuesta de baliza tardía: alarma a 5 min y espera operativa máxima de 30 min antes de
escalar a incidente; el vencimiento **no** autoriza otra ronda, seed ni sorteo
manual. Conserva compromiso y fondos bloqueados. La política final de reanudación
o cancelación debe ser explícita; fuente/timeout requieren elección antes de C2.

Propuesta F7: pago aprobado tras reserva vencida o pool congelado no emite boletos
ni amplía pool. Registrar excepción, notificar y conciliar; devolver íntegramente
al medio original por operación idempotente una vez fijado T-03 y la política PSP.
No convertir automáticamente a saldo interno ni asentar comisión como si hubiera
participación. Es política propuesta: confirmación contable/custodia siguen abiertas
[LEGAL→ABOGADO].
