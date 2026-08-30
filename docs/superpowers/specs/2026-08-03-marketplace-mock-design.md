---
title: "Spec — Rebanada 1 del frontend: marketplace con datos mock"
status: aprobado
tags: [spec, frontend, marketplace, mvp]
updated: 2026-08-03
---

# Rebanada 1 del frontend: marketplace con datos mock

Spec de diseño aprobado en brainstorming (Superpowers SDD) el 2026-08-03.
Define la primera rebanada de código real de Libox: el scaffold de la app y
las dos pantallas core del comprador, alimentadas con datos mock. Sin backend,
sin auth, sin pagos.

## Contexto y decisiones de entrada

- **Stack cerrado** por [ADR Z.6](../../archive/decisions/Z6-stack-tecnologico.md):
  Next.js (App Router) + TypeScript, Tailwind CSS + shadcn/ui, Vercel.
  Esta rebanada no introduce dependencias fuera del stack.
- **Identidad visual congelada**: existe el estándar
  `src/assets/LIBOX_Visual_Identity_Engineering_Standard_v1_0.pdf`
  (VIES v1.0, modelo "Ruta 2"). La UI **deriva** sus tokens de ese documento;
  no se inventa color ni tipografía de marca. El VIES cierra además la
  pregunta de tono: "tecnológico y confiable sin perder cercanía", evitando
  verse bancario, gubernamental, gaming o crypto.
- Decisiones tomadas en este brainstorming (Diego, 2026-08-03):
  1. **Ubicación del scaffold**: raíz del repo + convención `src/` de Next.js.
  2. **Logo**: SVG provisional del isotipo recreado desde el plano técnico
     del VIES, marcado `PROVISIONAL`, reemplazable por el arte maestro.
  3. **Datos mock**: 12 rifas en 5 categorías con estados variados.
  4. **Aceptación**: verificación visual + TDD de la lógica pura
     (sin E2E en esta rebanada).

## Alcance

**Incluye**: scaffold real de la app; design tokens derivados del VIES;
componente de logo provisional; home/catálogo; detalle de rifa; datos mock
tipados; lógica pura con tests; actualización de `src/CLAUDE.md` (Commands) y
habilitación de la tanda 2 de plugins en el mismo PR.

**Excluye** (YAGNI en esta rebanada): backend y persistencia, auth, checkout
y pagos, dark mode (la variante negativa del VIES lo habilita después),
E2E/Playwright, i18n más allá de es-PE, SEO avanzado.

## 1. Arquitectura del scaffold

Configuración en la raíz del repo: `package.json`, `next.config.ts`,
`tsconfig.json` (strict), ESLint, Tailwind CSS v4, shadcn/ui
(`components.json`) y Vitest. El código vive en `src/` (convención `src/` de
Next.js). Las carpetas existentes `src/assets/`, `src/tests/`, `src/tools/` y
`src/workflows/` quedan intactas.

```
src/
  app/
    layout.tsx            # fuentes next/font, metadata es-PE
    page.tsx              # home/catálogo
    rifas/[slug]/page.tsx # detalle de rifa
    not-found.tsx         # 404 en español
    globals.css           # design tokens (@theme) comentados citando el VIES
  components/
    ui/                   # shadcn/ui
    libox-logo.tsx        # lockup provisional (isotipo SVG + wordmark)
    raffle-card.tsx
    raffle-progress.tsx
    countdown.tsx
    ticket-selector.tsx
    category-filter.tsx
    site-header.tsx
    site-footer.tsx
  lib/
    raffle.ts             # lógica pura testeable
    format.ts             # moneda y fechas es-PE
    mock/raffles.ts       # datos mock tipados
```

Rama: `feat/marketplace-mock` (nombres de rama en inglés; commits en
español, Conventional Commits, correo `@liboxapp.com`, sin trailers de IA).

## 2. Identidad aplicada — design tokens

Los tokens se documentan en `globals.css` (bloque `@theme` con comentarios
que citan la sección del VIES de la que derivan). Resumen normativo:

| Token | Valor | Fuente VIES | Uso |
|---|---|---|---|
| `primary` | `#6D28D9` (LIBOX Purple) | §6.1 | Acciones, acentos, isotipo |
| `accent` | `#8B5CF6` (Signal Violet) | §6.1 | Gradiente y acentos secundarios |
| `foreground` / fondos oscuros | `#0B1020` (Trust Navy) | §6.1 | Texto principal, footer |
| `success` | `#10B981` (Success Green) | §6.1 | Confirmaciones, progreso alto |
| Neutros | escala derivada `#E5E7EB` → `#0B1020` | §6.1–6.2 | Fondos, bordes, texto secundario |
| Gradiente oficial | Purple → Signal Violet | §6.4 | Isotipo, hero, barra de progreso |

Reglas duras (guardrails de [src/CLAUDE.md](../../../src/CLAUDE.md)):

- **Nunca** paleta Tailwind por defecto; neutros teñidos de navy, sombras en
  capas teñidas de navy (nunca negro puro).
- **Par tipográfico** vía `next/font`: **Manrope** (títulos, cifras, precios
  y countdown con `tabular-nums`; coherente con el wordmark) +
  **Instrument Sans** (cuerpo y labels).
- El wordmark del header respeta el VIES: Manrope ExtraBold, uppercase,
  tracking 0.25X; lockup `LB LIBOX` con separación 1X y safe area 1X.
- Radios generosos que hacen eco del isotipo (esquinas 1.1X); animaciones
  solo `transform`/`opacity`; estados `hover`/`focus-visible`/`active`
  completos.
- **Logo provisional**: SVG del isotipo recreado según el plano técnico del
  VIES (caja 10X×10X, trazo 2.2X, radio exterior 5X, interior 2.8X, esquinas
  1.1X, extremos redondeados, gradiente oficial), marcado `PROVISIONAL` en
  el código y validado visualmente contra la referencia congelada. Se
  reemplaza por el arte maestro cuando llegue el paquete oficial de
  exportación; queda prohibido deformarlo, recolorearlo o alterar sus
  proporciones (VIES §8).
- **Tono verbal**: cercano-confiable, trato de "tú", es-PE, sin jerga gamer
  ni bancaria. Tagline oficial *"Tu próxima oportunidad."* en hero y footer.
- Solo modo claro en esta rebanada.

## 3. Pantallas

### Home/catálogo (`/`)

- Header: lockup Libox + navegación mínima.
- Hero compacto: tagline oficial + 3 sellos de confianza (sorteo
  verificable, organizadores con RUC, pagos protegidos — copy mock).
- Chips de filtro por categoría (estado client-side, sin URL state).
- Grilla responsive (1 columna móvil → 3 desktop) de `RaffleCard`:
  ilustración del premio, badge de categoría y de estado, título, precio por
  ticket en S/, barra de progreso vendidos/total, countdown compacto y CTA
  "Ver rifa".
- Footer: tagline, disclaimer legal placeholder marcado `[LEGAL→ABOGADO]`.

### Detalle de rifa (`/rifas/[slug]`)

- Ilustración grande del premio; título; organizador con badge
  "RUC verificado" (mock).
- Precio por ticket; progreso con cifras (vendidos/total y %); **cuenta
  regresiva viva** hasta el cierre.
- **Selector de tickets**: stepper 1–20 con subtotal calculado en S/.
- **CTA "Comprar tickets" deshabilitado** con nota "Disponible próximamente".
- Sección "Cómo funciona" en 3 pasos: participa → sorteo auditable con
  prueba criptográfica ([ADR Z.4](../../archive/decisions/Z4-tipos-de-sorteo.md)) →
  entrega del premio.
- Rifa finalizada: muestra ganador mock y oculta selector y CTA.
- Slug inexistente → `notFound()` con 404 en español.

Mobile-first en ambas pantallas.

## 4. Datos mock

`src/lib/mock/raffles.ts` exporta un arreglo tipado `Raffle`:

- Campos: `id`, `slug`, `title`, `prize`, `category`, `ticketPriceCents`
  (PEN), `totalTickets`, `soldTickets`, `endsAt`, `status`, `organizer`
  (nombre + RUC mock), `image`.
- **12 rifas, 5 categorías**: Tecnología, Vehículos, Viajes, Hogar,
  Efectivo — premios creíbles del mercado peruano.
- Estados deliberadamente variados: recién lanzada, avanzada, por agotarse,
  cierra en horas y 1 finalizada con ganador — para que barra de progreso,
  countdown y badges muestren todos sus estados reales.
- `endsAt` se genera con offsets relativos al arranque, así los countdowns
  siempre se ven vivos en demos.
- Imágenes: ilustraciones SVG locales teñidas con la marca por categoría
  (sin fotos externas: evita derechos de autor y dependencia de red).

## 5. Lógica testeable y manejo de errores

Funciones puras en `src/lib/raffle.ts` y `src/lib/format.ts`, desarrolladas
con TDD (Vitest, reglas de [tests/CLAUDE.md](../../../src/tests/CLAUDE.md)):

- Progreso de venta con clamp a 100 %.
- Tiempo restante y formato de countdown; al llegar a 0 la rifa pasa a
  estado "Cerrada".
- Formato de moneda con `Intl.NumberFormat('es-PE')` desde céntimos.
- Clamp del selector de tickets (mín. 1, máx. 20 o disponibles) y subtotal.

Los componentes consumen estas funciones; no se testean píxeles ni
snapshots visuales.

## 6. Obligaciones del mismo PR

- Actualizar la sección **Commands** de [src/CLAUDE.md](../../../src/CLAUDE.md)
  con los comandos reales (`dev`, `build`, `lint`, `typecheck`, `test`).
- Habilitar la **tanda 2 de plugins** en `.claude/settings.json`:
  `security-guidance`, `claude-security`, `typescript-lsp`,
  `pr-review-toolkit`, `vercel`.

## 7. Criterios de aceptación

1. `lint`, `typecheck` y `build` en verde; suites Vitest en verde.
2. Verificación visual desde localhost (nunca `file:///`) con **≥ 2 rondas
   de screenshots** en móvil y desktop; el skill **frontend-design** se
   invoca antes de escribir cualquier código de UI en la sesión de
   ejecución.
3. Todo string user-facing en español (Perú); código e identificadores en
   inglés.
4. Design tokens documentados en `globals.css` citando el VIES.
5. CTA de compra visiblemente deshabilitado con su nota explicativa.
6. El logo pasa el checklist básico del VIES: sin deformación, safe area
   1X, contraste AA, lectura "LB" (no "B" ni "13").
7. Las dos pantallas navegan entre sí con las 12 rifas mock y todos los
   estados visibles (activa, por agotarse, cierra en horas, finalizada).

## Notas de ejecución

- Flujo: este spec → **writing-plans** → ejecución por subagentes con TDD,
  según [src/CLAUDE.md](../../../src/CLAUDE.md) (orquestación Fable → Opus).
- El PR se abre contra `main` (rebase-and-merge; checks `commitlint`,
  `markdownlint`, `links`).
