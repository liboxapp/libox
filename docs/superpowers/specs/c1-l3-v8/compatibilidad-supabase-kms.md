---
title: C1 — compatibilidad de Supabase y cifrado KMS
status: borrador
tags: [r0, c1, seguridad, supabase]
updated: 2026-10-04
description: Alcance aprobado, excepción Auth aún pendiente y verificaciones necesarias para integrar cifrado de dominio con Supabase.
---

# Compatibilidad de Supabase y KMS

Diego aprobó AWS KMS y exigió compatibilidad con Supabase en
[B1-bis](decisiones-c1-datos.md#b1-bis-cifrado-de-datos-personales).
El 2026-10-02 Diego aclaró que pide fundamentos de la recomendación de evitar
autenticación propia en Go. Su descarte no queda ratificado por ese intercambio.
Supabase Auth conserva su elección previa como proveedor administrado; el diseño
propuesto deja en Go la validación de identidad y los permisos del dominio Libox.
El 2026-10-04 ratificó Auth administrada en el punto 4 de las
[decisiones posteriores](decisiones-2026-10-04.md). El inventario de atributos
y la excepción concreta no quedaron enumerados; no se infiere una excepción
general para datos personales. Ver la [decisión de stack](../2026-10-02-stack-go-frontend-ts.md).
La excepción de datos personales para Auth sigue sin aprobarse. Esta ficha
concreta la frontera pendiente; no acredita una integración ejecutada en un
proyecto gestionado.

## Separación propuesta para ratificar

| Superficie | Tratamiento propuesto | Estado |
|---|---|---|
| Dominio Libox | Cifrado de sobre KMS para campos personales; índice HMAC cuando se necesite búsqueda exacta | Enfoque aprobado; inventario, normalización y rotación pendientes |
| Supabase Auth | Conservar solo atributos necesarios para la identidad y acceso, administrados por el proveedor | Excepción pendiente de Diego; enumerar campos antes de aprobarla |
| Vínculo Auth/dominio | Identificador estable; no copiar datos personales por comodidad a metadata de Auth | Propuesta de diseño |
| Archivos KYC/KYB y evidencias | Inventario de objetos y copias, con su cifrado, autorización y recuperación | Diseño pendiente; bucket privado no acredita cifrado de aplicación |
| Logs, exportaciones y reportería | Evitar datos personales en logs; vistas mínimas y exportaciones autorizadas/auditadas | Alcance y pruebas pendientes |

Supabase gestiona usuarios e identidades en el esquema Auth; sus usuarios
permanentes están ligados a email, teléfono o identidad externa. El esquema Auth
no se expone en la API autogenerada. Esa separación de acceso no equivale a
cifrar sus campos con las claves de Libox.
[Usuarios](https://supabase.com/docs/guides/auth/users),
[gestión de datos](https://supabase.com/docs/guides/auth/managing-user-data).

**Dirección ratificada:** Supabase Auth administrada y KMS para el dominio.
Concretar una excepción mínima inventariada para los atributos de identidad;
el punto 4 no suministra por sí solo una lista de campos autorizados.
No cifrar ni reemplazar columnas administradas de Auth como si fueran propias.
La alternativa «cero datos personales legibles en toda la base» requiere otro
análisis de identidad; no se promete que un identificador opaco la resuelva.
Hasta concretar la frontera, no implementar la autenticación definitiva ni
anunciar que toda la base cumple la política de cifrado.

## Auditoría de claves

CloudTrail registra llamadas a la API KMS. Una operación local con una clave de
datos ya obtenida no implica otra llamada KMS: la caché puede reducir dichas
llamadas. Por eso CloudTrail no sustituye la auditoría aplicativa de cada acceso
a datos personales. La aplicación debe registrar actor, propósito, recurso y
resultado sin incluir datos descifrados ni claves.
[Registro KMS](https://docs.aws.amazon.com/kms/latest/developerguide/logging-using-cloudtrail.html),
[caché de claves](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/data-caching-details.html).

## Entregables antes de habilitar el flujo real

- Inventario por campo/objeto: ubicación, dueño, lectura, búsqueda, retención y
  excepción autorizada; incluir metadata del proveedor, logs y exportaciones.
- Diseño de versión de clave y HMAC, migración/rotación, recuperación y revocación;
  separar claves de cifrado y búsqueda. No inferir que rotar KMS recifra cada dato.
- Configuración de acceso KMS por componente, región y tratamiento de credenciales;
  medir coste/latencia con el patrón de acceso antes de fijar TTL de caché.
- Pruebas de registro, acceso y recuperación de cuenta; límites de sesión/MFA y
  autorización por recurso; indisponibilidad de KMS sin guardar texto claro como fallback.
- Restauración de DB, objetos y claves; comprobar que backups, logs y exportaciones
  respetan el alcance aprobado. No generar el código protegido de semilla del sorteo.

Los ensayos con Supabase, KMS y el backend son D1/R1. C1 debe cerrar el alcance y
los criterios; los contratos actuales son candidatos, no evidencia de esos ensayos.
