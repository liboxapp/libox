# Marketplace Mock (Rebanada 1) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold real de la app Libox (Next.js App Router en la raíz del repo, convención `src/`) con las 2 pantallas core del comprador (home/catálogo y detalle de rifa) alimentadas por 12 rifas mock, aplicando la identidad congelada del VIES v1.0.

**Architecture:** Monolito modular Next.js (App Router) según ADR Z.6. Server Components para las páginas; Client Components solo donde hay interacción (countdown, filtros, selector de tickets). Lógica pura en `src/lib/` desarrollada con TDD (Vitest); los componentes solo consumen esas funciones. Sin backend, sin auth, sin pagos.

**Tech Stack:** Next.js (App Router) + TypeScript strict · Tailwind CSS v4 + shadcn/ui (incluye `lucide-react`) · Vitest · `next/font` (Manrope + Instrument Sans).

**Spec:** [docs/superpowers/specs/2026-08-03-marketplace-mock-design.md](../specs/2026-08-03-marketplace-mock-design.md)

## Global Constraints

- **Rama:** `feat/marketplace-mock` (ya existe, partió de `main`). Nombres de rama en inglés.
- **Commits:** Conventional Commits **en español**, correo `dcotrina@liboxapp.com` (ya configurado local). **PROHIBIDO** cualquier trailer `Co-Authored-By` de IA o "Generated with Claude Code" (regla raíz de CLAUDE.md).
- **Idioma:** código, identificadores y comentarios en **inglés**; todo string user-facing en **español (Perú)**.
- **Skill obligatorio:** invocar **frontend-design** en la sesión de ejecución ANTES de escribir cualquier código de UI (aplica desde la Task 3).
- **Paleta congelada (VIES §6.1):** LIBOX Purple `#6D28D9`, Trust Navy `#0B1020`, Signal Violet `#8B5CF6`, Success Green `#10B981`, Light Gray `#E5E7EB`, White `#FFFFFF`. Gradiente oficial: Purple → Signal Violet. **Nunca** usar la paleta gris/violeta por defecto de Tailwind; neutros teñidos de navy; sombras teñidas de navy, nunca negro puro.
- **Tipografía:** Manrope (títulos, cifras, countdown con `tabular-nums`; wordmark en ExtraBold uppercase) + Instrument Sans (cuerpo). Vía `next/font/google`.
- **Animaciones:** solo `transform`/`opacity`. Estados `hover`/`focus-visible`/`active` completos en todo elemento interactivo.
- **Mobile-first.** Verificación visual solo desde `http://localhost:3000` (nunca `file:///`).
- **No tocar:** `.gitignore` de la raíz (ya cubre Node/Next), `src/assets/`, `docs/` (salvo lo que este plan indica), `.claude/settings.local.json`.
- **No crear `README.md`** en la raíz (el repo-wiki tiene su propia documentación).
- **Dependencias:** solo las del stack Z.6 + shadcn/ui y sus dependencias (`lucide-react` incluido) + Vitest. Nada más sin ADR.
- **TDD:** las funciones de `src/lib/` se escriben test-first. Nunca declarar un test en verde sin haberlo corrido y visto la salida.

---

### Task 1: Scaffold base de Next.js en la raíz

**Files:**
- Create: `package.json`, `package-lock.json`, `next.config.ts`, `tsconfig.json`, `eslint.config.mjs`, `postcss.config.mjs`, `vitest.config.ts`, `next-env.d.ts`, `src/app/layout.tsx`, `src/app/page.tsx`, `src/app/globals.css`, `public/` (vacío)
- **NO copiar del scaffold temporal:** `.gitignore`, `README.md`, `public/*.svg` (logos de Vercel/Next)

**Interfaces:**
- Produces: proyecto npm `libox@0.1.0` con scripts `dev`, `build`, `start`, `lint`, `typecheck`, `test`, `test:watch`; alias `@/*` → `./src/*`.

- [ ] **Step 1: Generar scaffold en directorio temporal** (create-next-app rechaza directorios no vacíos)

```bash
cd "$SCRATCHPAD"  # directorio scratchpad de la sesión
npx create-next-app@latest libox-tmp --ts --eslint --tailwind --app --src-dir \
  --import-alias "@/*" --use-npm --turbopack --yes
```

Si algún prompt no cubierto aparece (p. ej. React Compiler), aceptar el default.

- [ ] **Step 2: Copiar los archivos del scaffold a la raíz del repo**

```bash
REPO="/Users/diegocotrina/Claude/Cowork/Liboxapp/Project"
cd "$SCRATCHPAD/libox-tmp"
cp package.json package-lock.json next.config.ts tsconfig.json \
   eslint.config.mjs postcss.config.mjs "$REPO/"
mkdir -p "$REPO/src/app" "$REPO/public"
cp src/app/layout.tsx src/app/page.tsx src/app/globals.css "$REPO/src/app/"
```

Verificar que `git status` en el repo NO muestre cambios en `.gitignore` ni un `README.md` nuevo.

- [ ] **Step 3: Ajustar `package.json`** — editar en la raíz del repo: `"name": "libox"`, `"version": "0.1.0"`, y dejar los scripts así:

```json
"scripts": {
  "dev": "next dev",
  "build": "next build",
  "start": "next start",
  "lint": "eslint .",
  "typecheck": "tsc --noEmit",
  "test": "vitest run",
  "test:watch": "vitest"
}
```

- [ ] **Step 4: Instalar dependencias + Vitest**

```bash
cd "$REPO" && npm install && npm install -D vitest
```

- [ ] **Step 5: Crear `vitest.config.ts`**

```ts
import path from 'node:path';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  resolve: {
    alias: { '@': path.resolve(__dirname, 'src') },
  },
  test: {
    include: ['src/tests/**/*.test.ts'],
  },
});
```

- [ ] **Step 6: Excluir artefactos en `eslint.config.mjs`** — asegurar que el config exportado incluya un bloque de ignores (añadirlo si el generado no lo trae):

```js
{ ignores: ['.next/**', 'node_modules/**', 'docs/**', 'scripts/**', 'coverage/**'] },
```

- [ ] **Step 7: Verificar que todo corre**

```bash
npm run lint && npm run typecheck && npm run build
```

Expected: los tres en verde (typecheck puede regenerar `next-env.d.ts`; se versiona). `npm test` aún reporta "no test files found" — correcto en esta task.

- [ ] **Step 8: Smoke del dev server**

```bash
npm run dev &   # (o run_in_background)
sleep 5 && curl -sf http://localhost:3000 | head -5
```

Expected: HTML de la página default de Next. Dejar el server corriendo para tasks siguientes o matarlo — a elección.

- [ ] **Step 9: Commit**

```bash
git add package.json package-lock.json next.config.ts tsconfig.json \
  eslint.config.mjs postcss.config.mjs vitest.config.ts next-env.d.ts src/app public
git commit -m "chore(app): scaffold base de Next.js con TypeScript y Tailwind en la raíz"
```

---

### Task 2: shadcn/ui inicializado con componentes base

**Files:**
- Create: `components.json`, `src/lib/utils.ts`, `src/components/ui/button.tsx`, `src/components/ui/badge.tsx`, `src/components/ui/card.tsx`
- Modify: `src/app/globals.css` (shadcn agrega variables), `package.json`

**Interfaces:**
- Produces: `<Button>`, `<Badge>`, `<Card>`/`<CardContent>` de shadcn/ui; helper `cn()` en `@/lib/utils`; `lucide-react` disponible.

- [ ] **Step 1: Inicializar shadcn**

```bash
npx shadcn@latest init --yes --base-color neutral
```

- [ ] **Step 2: Agregar componentes**

```bash
npx shadcn@latest add button badge card --yes
```

- [ ] **Step 3: Verificar**

```bash
npm run lint && npm run typecheck && npm run build
```

Expected: verde.

- [ ] **Step 4: Commit**

```bash
git add components.json src/lib/utils.ts src/components/ui src/app/globals.css package.json package-lock.json
git commit -m "chore(app): inicializa shadcn/ui con button, badge y card"
```

---

### Task 3: Design tokens del VIES, tipografías y layout base

> Antes de esta task el ejecutor invoca el skill **frontend-design** (regla de src/CLAUDE.md: antes de cualquier código de UI, cada sesión).

**Files:**
- Modify: `src/app/globals.css` (reescribir con tokens VIES), `src/app/layout.tsx`, `src/app/page.tsx` (placeholder mínimo en español)

**Interfaces:**
- Produces: variables CSS `--primary #6D28D9`, `--accent #8B5CF6`, `--foreground #0B1020`, `--success #10B981`, neutros teñidos de navy, `--gradient-brand`, sombras `--shadow-card`/`--shadow-card-hover`; fuentes `--font-manrope` y `--font-instrument`; clase utilitaria `font-display` no — usar `font-[family-name:var(--font-manrope)]` vía tokens Tailwind (`--font-sans`, `--font-heading`).

- [ ] **Step 1: Reescribir `src/app/globals.css`** — conservar el bloque `@theme inline`/dark que shadcn generó como base, pero mapear TODOS los valores a la paleta VIES. Contenido completo:

```css
@import 'tailwindcss';

/*
 * Libox design tokens — derived from the frozen brand standard
 * src/assets/LIBOX_Visual_Identity_Engineering_Standard_v1_0.pdf (VIES v1.0).
 * Palette: VIES §6.1-6.2 · Gradient: §6.4 · Shape echoes isotype radii §3.3.
 * Neutrals are navy-tinted derivations of Light Gray #E5E7EB → Trust Navy
 * #0B1020 (never default Tailwind grays). Shadows are navy-tinted.
 */

:root {
  /* VIES frozen palette */
  --libox-purple: #6d28d9;   /* VIES: LIBOX Purple */
  --signal-violet: #8b5cf6;  /* VIES: Signal Violet */
  --trust-navy: #0b1020;     /* VIES: Trust Navy */
  --success-green: #10b981;  /* VIES: Success Green */

  /* Semantic tokens (light mode only in this slice) */
  --background: #f7f7fb;
  --foreground: #0b1020;
  --card: #ffffff;
  --card-foreground: #0b1020;
  --popover: #ffffff;
  --popover-foreground: #0b1020;
  --primary: #6d28d9;
  --primary-foreground: #ffffff;
  --secondary: #eeedf6;
  --secondary-foreground: #0b1020;
  --muted: #eeedf6;
  --muted-foreground: #545a73; /* navy-tinted gray */
  --accent: #8b5cf6;
  --accent-foreground: #ffffff;
  --success: #10b981;
  --success-foreground: #ffffff;
  --destructive: #b3261e;
  --border: #e2e2ee;
  --input: #e2e2ee;
  --ring: #8b5cf6;
  --radius: 1rem; /* generous rounding echoing the isotype corner radius */

  /* Brand gradient (VIES §6.4: Purple → Signal Violet only) */
  --gradient-brand: linear-gradient(135deg, #6d28d9 0%, #8b5cf6 100%);

  /* Layered navy-tinted shadows (never pure black) */
  --shadow-card: 0 1px 2px rgb(11 16 32 / 0.05), 0 4px 14px rgb(11 16 32 / 0.07);
  --shadow-card-hover: 0 2px 4px rgb(11 16 32 / 0.06), 0 10px 28px rgb(11 16 32 / 0.12);
}

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-success: var(--success);
  --color-success-foreground: var(--success-foreground);
  --color-destructive: var(--destructive);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --color-navy: var(--trust-navy);
  --font-sans: var(--font-instrument), ui-sans-serif, system-ui, sans-serif;
  --font-heading: var(--font-manrope), ui-sans-serif, system-ui, sans-serif;
  --radius-sm: calc(var(--radius) - 8px);
  --radius-md: calc(var(--radius) - 4px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 8px);
}

body {
  background: var(--background);
  color: var(--foreground);
  font-family: var(--font-sans);
}

h1, h2, h3, h4 {
  font-family: var(--font-heading);
}

.tabular-nums {
  font-variant-numeric: tabular-nums;
}
```

Si el `globals.css` de shadcn traía `@custom-variant dark` o bloque `.dark`, eliminarlos (esta rebanada es solo modo claro).

- [ ] **Step 2: Reescribir `src/app/layout.tsx`**

```tsx
import type { Metadata } from 'next';
import { Instrument_Sans, Manrope } from 'next/font/google';
import './globals.css';

const manrope = Manrope({
  subsets: ['latin'],
  variable: '--font-manrope',
  weight: ['400', '600', '700', '800'],
});

const instrumentSans = Instrument_Sans({
  subsets: ['latin'],
  variable: '--font-instrument',
  weight: ['400', '500', '600'],
});

export const metadata: Metadata = {
  title: {
    default: 'Libox — Tu próxima oportunidad',
    template: '%s · Libox',
  },
  description:
    'Marketplace de rifas digitales con sorteos verificables. Participa por premios reales con organizadores verificados en el Perú.',
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="es-PE">
      <body className={`${manrope.variable} ${instrumentSans.variable} antialiased`}>
        {children}
      </body>
    </html>
  );
}
```

- [ ] **Step 3: Reemplazar `src/app/page.tsx` por un placeholder en español** (se reescribe en Task 9):

```tsx
export default function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center">
      <h1 className="text-2xl font-extrabold text-primary">Libox — en construcción</h1>
    </main>
  );
}
```

- [ ] **Step 4: Verificar** — `npm run lint && npm run typecheck && npm run build`, luego con el dev server arriba abrir `http://localhost:3000` y confirmar fondo `#F7F7FB`, título morado y tipografías cargadas (inspección rápida, sin ronda formal de screenshots todavía).

- [ ] **Step 5: Commit**

```bash
git add src/app
git commit -m "feat(app): design tokens derivados del VIES, tipografías y layout base"
```

---

### Task 4: Formato de moneda es-PE (TDD)

**Files:**
- Create: `src/lib/format.ts`
- Test: `src/tests/unit/format.test.ts`

**Interfaces:**
- Produces: `formatPEN(cents: number): string` — recibe céntimos, devuelve `"S/ 20.00"` (es-PE, espacio normal, coma de miles, punto decimal). Lanza `RangeError` si `cents` no es finito.

- [ ] **Step 1: Escribir el test que falla** — `src/tests/unit/format.test.ts`:

```ts
import { describe, expect, it } from 'vitest';
import { formatPEN } from '@/lib/format';

describe('formatPEN', () => {
  it('formats whole soles from cents', () => {
    expect(formatPEN(2000)).toBe('S/ 20.00');
  });

  it('formats cents', () => {
    expect(formatPEN(1250)).toBe('S/ 12.50');
  });

  it('uses comma as thousands separator (es-PE)', () => {
    expect(formatPEN(1000000)).toBe('S/ 10,000.00');
  });

  it('formats zero', () => {
    expect(formatPEN(0)).toBe('S/ 0.00');
  });

  it('throws on non-finite input', () => {
    expect(() => formatPEN(Number.NaN)).toThrow(RangeError);
  });
});
```

- [ ] **Step 2: Correr y verlo fallar**

```bash
npm test -- src/tests/unit/format.test.ts
```

Expected: FAIL — módulo `@/lib/format` no existe.

- [ ] **Step 3: Implementación mínima** — `src/lib/format.ts`:

```ts
const penFormatter = new Intl.NumberFormat('es-PE', {
  style: 'currency',
  currency: 'PEN',
});

/** Formats an amount in cents as Peruvian soles, e.g. 2000 -> "S/ 20.00". */
export function formatPEN(cents: number): string {
  if (!Number.isFinite(cents)) {
    throw new RangeError('cents must be a finite number');
  }
  // Intl emits a non-breaking space after "S/"; normalize for consistent UI text.
  return penFormatter.format(cents / 100).replace(/\u00A0/g, ' ');
}
```

- [ ] **Step 4: Correr y verlo pasar** — mismo comando. Expected: PASS (5 tests). Si el separador difiere en tu Node (ICU), ajustar la implementación con `formatToParts` — los valores esperados del test son la verdad, no se relajan.

- [ ] **Step 5: Commit**

```bash
git add src/lib/format.ts src/tests/unit/format.test.ts
git commit -m "feat(app): formato de moneda es-PE desde céntimos con TDD"
```

---

### Task 5: Dominio de rifa — tipos y lógica pura (TDD)

**Files:**
- Create: `src/lib/raffle.ts`
- Test: `src/tests/unit/raffle.test.ts`

**Interfaces:**
- Produces (los componentes y el mock dependen de esto — nombres exactos):

```ts
export const RAFFLE_CATEGORIES = ['tecnologia', 'vehiculos', 'viajes', 'hogar', 'efectivo'] as const;
export type RaffleCategory = (typeof RAFFLE_CATEGORIES)[number];
export const CATEGORY_LABELS: Record<RaffleCategory, string>; // 'Tecnología', 'Vehículos', 'Viajes', 'Hogar', 'Efectivo'
export type RaffleStatus = 'activa' | 'finalizada';
export interface RaffleOrganizer { name: string; ruc: string }
export interface RaffleWinner { name: string; ticketNumber: number }
export interface Raffle {
  id: string; slug: string; title: string; prize: string; description: string;
  category: RaffleCategory; ticketPriceCents: number; totalTickets: number;
  soldTickets: number; endsAt: Date; status: RaffleStatus;
  organizer: RaffleOrganizer; winner?: RaffleWinner;
}
export const MAX_TICKETS_PER_PURCHASE = 20;
export interface CountdownParts { days: number; hours: number; minutes: number; seconds: number; totalMs: number }
export function computeProgressPercent(soldTickets: number, totalTickets: number): number;
export function availableTickets(raffle: Pick<Raffle, 'totalTickets' | 'soldTickets'>): number;
export function getCountdownParts(endsAt: Date, now: Date): CountdownParts;
export function formatCountdown(parts: CountdownParts): string; // "2d 04:10:33" | "04:10:33" | "00:00:00"
export function isClosed(endsAt: Date, now: Date): boolean;
export function clampTicketQuantity(quantity: number, available: number, max?: number): number;
export function computeSubtotalCents(quantity: number, ticketPriceCents: number): number;
export type BadgeTone = 'success' | 'warning' | 'closed';
export function getRaffleBadge(raffle: Raffle, now: Date): { label: string; tone: BadgeTone };
```

- [ ] **Step 1: Escribir los tests que fallan** — `src/tests/unit/raffle.test.ts`:

```ts
import { describe, expect, it } from 'vitest';
import {
  clampTicketQuantity,
  computeProgressPercent,
  computeSubtotalCents,
  formatCountdown,
  getCountdownParts,
  getRaffleBadge,
  isClosed,
  type Raffle,
} from '@/lib/raffle';

const NOW = new Date('2026-08-04T12:00:00Z');

function makeRaffle(overrides: Partial<Raffle> = {}): Raffle {
  return {
    id: 'r1',
    slug: 'iphone-16-pro',
    title: 'iPhone 16 Pro',
    prize: 'iPhone 16 Pro 256 GB',
    description: 'Sorteo de prueba',
    category: 'tecnologia',
    ticketPriceCents: 2000,
    totalTickets: 1000,
    soldTickets: 500,
    endsAt: new Date('2026-08-10T12:00:00Z'),
    status: 'activa',
    organizer: { name: 'Tiendas Conecta SAC', ruc: '20512345678' },
    ...overrides,
  };
}

describe('computeProgressPercent', () => {
  it('computes rounded percentage', () => {
    expect(computeProgressPercent(500, 1000)).toBe(50);
    expect(computeProgressPercent(333, 1000)).toBe(33);
  });
  it('clamps above 100 and below 0', () => {
    expect(computeProgressPercent(1200, 1000)).toBe(100);
    expect(computeProgressPercent(-5, 1000)).toBe(0);
  });
  it('returns 0 when total is 0', () => {
    expect(computeProgressPercent(10, 0)).toBe(0);
  });
});

describe('getCountdownParts / formatCountdown', () => {
  it('splits remaining time into parts', () => {
    const parts = getCountdownParts(new Date('2026-08-06T16:10:33Z'), NOW);
    expect(parts).toMatchObject({ days: 2, hours: 4, minutes: 10, seconds: 33 });
  });
  it('clamps to zero when past', () => {
    const parts = getCountdownParts(new Date('2026-08-01T00:00:00Z'), NOW);
    expect(parts.totalMs).toBe(0);
    expect(formatCountdown(parts)).toBe('00:00:00');
  });
  it('formats with days prefix only when days > 0', () => {
    expect(
      formatCountdown(getCountdownParts(new Date('2026-08-06T16:10:33Z'), NOW)),
    ).toBe('2d 04:10:33');
    expect(
      formatCountdown(getCountdownParts(new Date('2026-08-04T18:05:07Z'), NOW)),
    ).toBe('06:05:07');
  });
});

describe('isClosed', () => {
  it('is closed at or after endsAt', () => {
    expect(isClosed(new Date('2026-08-04T12:00:00Z'), NOW)).toBe(true);
    expect(isClosed(new Date('2026-08-04T12:00:01Z'), NOW)).toBe(false);
  });
});

describe('clampTicketQuantity', () => {
  it('keeps quantity within 1..max', () => {
    expect(clampTicketQuantity(5, 100)).toBe(5);
    expect(clampTicketQuantity(0, 100)).toBe(1);
    expect(clampTicketQuantity(25, 100)).toBe(20); // MAX_TICKETS_PER_PURCHASE
  });
  it('caps at available tickets when fewer than max', () => {
    expect(clampTicketQuantity(10, 3)).toBe(3);
  });
  it('returns 0 when nothing is available', () => {
    expect(clampTicketQuantity(1, 0)).toBe(0);
  });
  it('truncates fractional input', () => {
    expect(clampTicketQuantity(2.9, 100)).toBe(2);
  });
});

describe('computeSubtotalCents', () => {
  it('multiplies quantity by price', () => {
    expect(computeSubtotalCents(3, 2000)).toBe(6000);
  });
  it('never returns negative', () => {
    expect(computeSubtotalCents(-2, 2000)).toBe(0);
  });
});

describe('getRaffleBadge', () => {
  it('finalizada wins over everything', () => {
    const r = makeRaffle({ status: 'finalizada', winner: { name: 'Rosa Q.', ticketNumber: 842 } });
    expect(getRaffleBadge(r, NOW)).toEqual({ label: 'Finalizada', tone: 'closed' });
  });
  it('cerrada when countdown reached zero', () => {
    const r = makeRaffle({ endsAt: new Date('2026-08-04T11:00:00Z') });
    expect(getRaffleBadge(r, NOW)).toEqual({ label: 'Cerrada', tone: 'closed' });
  });
  it('agotada when no tickets left', () => {
    const r = makeRaffle({ soldTickets: 1000 });
    expect(getRaffleBadge(r, NOW)).toEqual({ label: 'Agotada', tone: 'closed' });
  });
  it('por agotarse at >= 90% sold', () => {
    const r = makeRaffle({ soldTickets: 950 });
    expect(getRaffleBadge(r, NOW)).toEqual({ label: 'Por agotarse', tone: 'warning' });
  });
  it('cierra pronto within 24h', () => {
    const r = makeRaffle({ endsAt: new Date('2026-08-05T10:00:00Z') });
    expect(getRaffleBadge(r, NOW)).toEqual({ label: 'Cierra pronto', tone: 'warning' });
  });
  it('activa otherwise', () => {
    expect(getRaffleBadge(makeRaffle(), NOW)).toEqual({ label: 'Activa', tone: 'success' });
  });
});
```

- [ ] **Step 2: Correr y verlo fallar** — `npm test -- src/tests/unit/raffle.test.ts`. Expected: FAIL (módulo no existe).

- [ ] **Step 3: Implementar `src/lib/raffle.ts`**

```ts
export const RAFFLE_CATEGORIES = [
  'tecnologia',
  'vehiculos',
  'viajes',
  'hogar',
  'efectivo',
] as const;

export type RaffleCategory = (typeof RAFFLE_CATEGORIES)[number];

export const CATEGORY_LABELS: Record<RaffleCategory, string> = {
  tecnologia: 'Tecnología',
  vehiculos: 'Vehículos',
  viajes: 'Viajes',
  hogar: 'Hogar',
  efectivo: 'Efectivo',
};

export type RaffleStatus = 'activa' | 'finalizada';

export interface RaffleOrganizer {
  name: string;
  ruc: string;
}

export interface RaffleWinner {
  name: string;
  ticketNumber: number;
}

export interface Raffle {
  id: string;
  slug: string;
  title: string;
  prize: string;
  description: string;
  category: RaffleCategory;
  ticketPriceCents: number;
  totalTickets: number;
  soldTickets: number;
  endsAt: Date;
  status: RaffleStatus;
  organizer: RaffleOrganizer;
  winner?: RaffleWinner;
}

export const MAX_TICKETS_PER_PURCHASE = 20;

const CLOSING_SOON_MS = 24 * 60 * 60 * 1000;

export function computeProgressPercent(soldTickets: number, totalTickets: number): number {
  if (totalTickets <= 0) return 0;
  const percent = Math.round((soldTickets / totalTickets) * 100);
  return Math.min(100, Math.max(0, percent));
}

export function availableTickets(raffle: Pick<Raffle, 'totalTickets' | 'soldTickets'>): number {
  return Math.max(0, raffle.totalTickets - raffle.soldTickets);
}

export interface CountdownParts {
  days: number;
  hours: number;
  minutes: number;
  seconds: number;
  totalMs: number;
}

export function getCountdownParts(endsAt: Date, now: Date): CountdownParts {
  const totalMs = Math.max(0, endsAt.getTime() - now.getTime());
  const totalSeconds = Math.floor(totalMs / 1000);
  return {
    days: Math.floor(totalSeconds / 86_400),
    hours: Math.floor((totalSeconds % 86_400) / 3600),
    minutes: Math.floor((totalSeconds % 3600) / 60),
    seconds: totalSeconds % 60,
    totalMs,
  };
}

const pad2 = (value: number) => String(value).padStart(2, '0');

export function formatCountdown(parts: CountdownParts): string {
  const hms = `${pad2(parts.hours)}:${pad2(parts.minutes)}:${pad2(parts.seconds)}`;
  return parts.days > 0 ? `${parts.days}d ${hms}` : hms;
}

export function isClosed(endsAt: Date, now: Date): boolean {
  return getCountdownParts(endsAt, now).totalMs === 0;
}

export function clampTicketQuantity(
  quantity: number,
  available: number,
  max: number = MAX_TICKETS_PER_PURCHASE,
): number {
  const cap = Math.min(available, max);
  if (cap <= 0) return 0;
  return Math.min(cap, Math.max(1, Math.trunc(quantity)));
}

export function computeSubtotalCents(quantity: number, ticketPriceCents: number): number {
  return Math.max(0, Math.trunc(quantity)) * Math.max(0, ticketPriceCents);
}

export type BadgeTone = 'success' | 'warning' | 'closed';

export function getRaffleBadge(
  raffle: Raffle,
  now: Date,
): { label: string; tone: BadgeTone } {
  if (raffle.status === 'finalizada') return { label: 'Finalizada', tone: 'closed' };
  if (isClosed(raffle.endsAt, now)) return { label: 'Cerrada', tone: 'closed' };
  if (availableTickets(raffle) === 0) return { label: 'Agotada', tone: 'closed' };
  if (computeProgressPercent(raffle.soldTickets, raffle.totalTickets) >= 90) {
    return { label: 'Por agotarse', tone: 'warning' };
  }
  if (raffle.endsAt.getTime() - now.getTime() <= CLOSING_SOON_MS) {
    return { label: 'Cierra pronto', tone: 'warning' };
  }
  return { label: 'Activa', tone: 'success' };
}
```

- [ ] **Step 4: Correr y ver pasar TODO** — `npm test`. Expected: PASS (format + raffle).

- [ ] **Step 5: Commit**

```bash
git add src/lib/raffle.ts src/tests/unit/raffle.test.ts
git commit -m "feat(app): tipos y lógica pura del dominio de rifas con TDD"
```

---

### Task 6: Datos mock — 12 rifas en 5 categorías

**Files:**
- Create: `src/lib/mock/raffles.ts`

**Interfaces:**
- Consumes: `Raffle`, `RaffleCategory` de `@/lib/raffle`.
- Produces: `buildMockRaffles(now?: Date): Raffle[]` (offsets relativos a `now` para countdowns siempre vivos), `mockRaffles: Raffle[]`, `getRaffleBySlug(slug: string): Raffle | undefined`.

- [ ] **Step 1: Crear `src/lib/mock/raffles.ts`**

```ts
import type { Raffle } from '@/lib/raffle';

const HOUR_MS = 60 * 60 * 1000;

/**
 * Mock catalog for the first slice. `endsAt` is generated relative to `now`
 * so countdowns always look alive in demos. States are deliberately varied:
 * freshly launched, advanced, almost sold out, closing in hours, finished.
 */
export function buildMockRaffles(now: Date = new Date()): Raffle[] {
  const hoursFromNow = (hours: number) => new Date(now.getTime() + hours * HOUR_MS);

  return [
    {
      id: 'raf-001',
      slug: 'iphone-16-pro',
      title: 'iPhone 16 Pro 256 GB',
      prize: 'iPhone 16 Pro 256 GB color titanio',
      description:
        'Participa por el iPhone 16 Pro de 256 GB, nuevo y sellado, con garantía oficial de un año. El sorteo se ejecuta con prueba criptográfica verificable.',
      category: 'tecnologia',
      ticketPriceCents: 2000,
      totalTickets: 2500,
      soldTickets: 1830,
      endsAt: hoursFromNow(5 * 24),
      status: 'activa',
      organizer: { name: 'Tiendas Conecta SAC', ruc: '20512345678' },
    },
    {
      id: 'raf-002',
      slug: 'laptop-gamer-legion',
      title: 'Laptop gamer Lenovo Legion',
      prize: 'Lenovo Legion 5, RTX 4060, 16 GB RAM',
      description:
        'Una laptop gamer de alto rendimiento para trabajo y juego. Nueva, sellada y con garantía de tienda.',
      category: 'tecnologia',
      ticketPriceCents: 1500,
      totalTickets: 3000,
      soldTickets: 620,
      endsAt: hoursFromNow(12 * 24),
      status: 'activa',
      organizer: { name: 'GamerZone Perú EIRL', ruc: '20601234567' },
    },
    {
      id: 'raf-003',
      slug: 'playstation-5-bundle',
      title: 'PlayStation 5 + 2 juegos',
      prize: 'PS5 edición estándar con 2 juegos a elección',
      description:
        'Consola PlayStation 5 con lector de discos y dos juegos a elección del ganador. Quedan pocos tickets.',
      category: 'tecnologia',
      ticketPriceCents: 1000,
      totalTickets: 2000,
      soldTickets: 1980,
      endsAt: hoursFromNow(2 * 24),
      status: 'activa',
      organizer: { name: 'GamerZone Perú EIRL', ruc: '20601234567' },
    },
    {
      id: 'raf-004',
      slug: 'moto-honda-navi',
      title: 'Moto Honda Navi 2026',
      prize: 'Honda Navi 2026 0 km, tarjeta y SOAT',
      description:
        'Moto Honda Navi del año, cero kilómetros, con tarjeta de propiedad y SOAT incluidos. Entrega en Lima o provincia.',
      category: 'vehiculos',
      ticketPriceCents: 2500,
      totalTickets: 4000,
      soldTickets: 2400,
      endsAt: hoursFromNow(9 * 24),
      status: 'activa',
      organizer: { name: 'Autonort Selva SAC', ruc: '20487654321' },
    },
    {
      id: 'raf-005',
      slug: 'auto-kia-picanto',
      title: 'Auto Kia Picanto 2026',
      prize: 'Kia Picanto 2026 0 km full equipo',
      description:
        'El gran premio del año: un Kia Picanto 2026 cero kilómetros, full equipo, con todos los gastos de transferencia pagados.',
      category: 'vehiculos',
      ticketPriceCents: 5000,
      totalTickets: 10000,
      soldTickets: 3100,
      endsAt: hoursFromNow(30 * 24),
      status: 'activa',
      organizer: { name: 'Autonort Selva SAC', ruc: '20487654321' },
    },
    {
      id: 'raf-006',
      slug: 'viaje-cusco-para-dos',
      title: 'Cusco para dos, todo incluido',
      prize: 'Viaje a Cusco 4D/3N para 2 personas',
      description:
        'Vuelos, hotel 4 estrellas, tours a Machu Picchu y Valle Sagrado para dos personas. Fechas flexibles.',
      category: 'viajes',
      ticketPriceCents: 1200,
      totalTickets: 1500,
      soldTickets: 1120,
      endsAt: hoursFromNow(6 * 24),
      status: 'activa',
      organizer: { name: 'Andes Travel Group SAC', ruc: '20556677889' },
    },
    {
      id: 'raf-007',
      slug: 'punta-cana-7-noches',
      title: 'Punta Cana, 7 noches para dos',
      prize: 'Resort todo incluido en Punta Cana',
      description:
        'Siete noches en resort 5 estrellas todo incluido para dos personas, con vuelos desde Lima.',
      category: 'viajes',
      ticketPriceCents: 3000,
      totalTickets: 5000,
      soldTickets: 900,
      endsAt: hoursFromNow(21 * 24),
      status: 'activa',
      organizer: { name: 'Andes Travel Group SAC', ruc: '20556677889' },
    },
    {
      id: 'raf-008',
      slug: 'combo-cocina-refrigeradora',
      title: 'Cocina + refrigeradora Samsung',
      prize: 'Combo Samsung: cocina 6 hornillas + refrigeradora 384 L',
      description:
        'Renueva tu hogar: cocina de 6 hornillas y refrigeradora side-by-side Samsung, con delivery incluido.',
      category: 'hogar',
      ticketPriceCents: 800,
      totalTickets: 1200,
      soldTickets: 460,
      endsAt: hoursFromNow(10 * 24),
      status: 'activa',
      organizer: { name: 'Electrohogar del Norte SRL', ruc: '20334455667' },
    },
    {
      id: 'raf-009',
      slug: 'juego-de-sala-completo',
      title: 'Juego de sala completo',
      prize: 'Sofá 3-2-1 + mesa de centro + rack de TV',
      description:
        'Juego de sala moderno en tela antimanchas: sofá 3-2-1, mesa de centro y rack para TV de hasta 65".',
      category: 'hogar',
      ticketPriceCents: 1000,
      totalTickets: 1000,
      soldTickets: 720,
      endsAt: hoursFromNow(4 * 24),
      status: 'activa',
      organizer: { name: 'Electrohogar del Norte SRL', ruc: '20334455667' },
    },
    {
      id: 'raf-010',
      slug: 'diez-mil-soles-efectivo',
      title: 'S/ 10,000 en efectivo',
      prize: 'S/ 10,000 depositados en tu cuenta',
      description:
        'Diez mil soles transferidos directamente a la cuenta bancaria del ganador. Cierra hoy: últimas horas para participar.',
      category: 'efectivo',
      ticketPriceCents: 2000,
      totalTickets: 3000,
      soldTickets: 2650,
      endsAt: hoursFromNow(10),
      status: 'activa',
      organizer: { name: 'Fundación Impulsa Perú', ruc: '20112233445' },
    },
    {
      id: 'raf-011',
      slug: 'cinco-mil-soles-efectivo',
      title: 'S/ 5,000 en efectivo',
      prize: 'S/ 5,000 depositados en tu cuenta',
      description:
        'Cinco mil soles para lo que tú decidas, transferidos al ganador con constancia del sorteo verificable.',
      category: 'efectivo',
      ticketPriceCents: 1000,
      totalTickets: 1500,
      soldTickets: 610,
      endsAt: hoursFromNow(8 * 24),
      status: 'activa',
      organizer: { name: 'Fundación Impulsa Perú', ruc: '20112233445' },
    },
    {
      id: 'raf-012',
      slug: 'macbook-air-m4',
      title: 'MacBook Air M4',
      prize: 'MacBook Air 13" chip M4, 16 GB',
      description:
        'Sorteo finalizado. La MacBook Air M4 ya tiene dueña: felicitaciones a la ganadora, elegida con prueba criptográfica verificable.',
      category: 'tecnologia',
      ticketPriceCents: 1800,
      totalTickets: 2000,
      soldTickets: 2000,
      endsAt: hoursFromNow(-3 * 24),
      status: 'finalizada',
      organizer: { name: 'Tiendas Conecta SAC', ruc: '20512345678' },
      winner: { name: 'Rosa Q.', ticketNumber: 842 },
    },
  ];
}

export const mockRaffles: Raffle[] = buildMockRaffles();

export function getRaffleBySlug(slug: string): Raffle | undefined {
  return mockRaffles.find((raffle) => raffle.slug === slug);
}
```

- [ ] **Step 2: Verificar** — `npm run typecheck && npm run lint`. Expected: verde.

- [ ] **Step 3: Commit**

```bash
git add src/lib/mock/raffles.ts
git commit -m "feat(app): datos mock de 12 rifas en 5 categorías con estados variados"
```

---

### Task 7: Logo provisional del VIES e ilustraciones de premios

**Files:**
- Create: `src/components/libox-logo.tsx`, `src/components/prize-art.tsx`, `src/app/icon.svg`

**Interfaces:**
- Consumes: `RaffleCategory`, `CATEGORY_LABELS` de `@/lib/raffle`; íconos de `lucide-react`.
- Produces: `<LiboxIsotype className? />`, `<LiboxLogo variant?: 'default' | 'inverse' />` (lockup isotipo + wordmark), `<PrizeArt category size?: 'card' | 'hero' />`.

- [ ] **Step 1: Extraer la referencia congelada del VIES para comparar**

```bash
python3 -c "
from pypdf import PdfReader
r = PdfReader('src/assets/LIBOX_Visual_Identity_Engineering_Standard_v1_0.pdf')
img = r.pages[0].images[3]  # frozen reference art (Im8.jpg)
open('$SCRATCHPAD/vies-reference.jpg', 'wb').write(img.data)
"
```

Ver la imagen con la herramienta Read: el isotipo es un monograma LB continuo (stem vertical de la L = espina de la B, pie horizontal de la L, dos lóbulos de la B a la derecha), trazo grueso redondeado, gradiente morado.

- [ ] **Step 2: Crear `src/components/libox-logo.tsx`**

```tsx
import { cn } from '@/lib/utils';

/*
 * PROVISIONAL brand asset — recreated from the frozen technical blueprint in
 * src/assets/LIBOX_Visual_Identity_Engineering_Standard_v1_0.pdf (VIES v1.0):
 * 10X x 10X box, 2.2X stroke, rounded caps, official Purple -> Violet gradient.
 * Replace with the official master SVG when the brand export package lands.
 * Do not deform, recolor, or change proportions (VIES §8).
 */
export function LiboxIsotype({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 100 100"
      fill="none"
      aria-hidden="true"
      className={className}
    >
      <defs>
        <linearGradient id="libox-brand-gradient" x1="0" y1="0" x2="100" y2="100" gradientUnits="userSpaceOnUse">
          <stop stopColor="#6D28D9" />
          <stop offset="1" stopColor="#8B5CF6" />
        </linearGradient>
      </defs>
      <path
        d="M 27 12 L 27 56 Q 27 78 49 78 L 55 78 Q 74 78 74 63 Q 74 51 60 50 Q 74 49 74 36 Q 74 22 55 22 L 49 22"
        stroke="url(#libox-brand-gradient)"
        strokeWidth="17"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function LiboxLogo({
  variant = 'default',
  className,
}: {
  variant?: 'default' | 'inverse';
  className?: string;
}) {
  return (
    <span className={cn('flex items-center gap-1.5', className)}>
      <LiboxIsotype className="h-8 w-8" />
      <span
        className={cn(
          // VIES: wordmark in Manrope ExtraBold, uppercase, tight tracking (0.25X)
          'font-[family-name:var(--font-manrope)] text-xl font-extrabold uppercase tracking-[0.02em]',
          variant === 'inverse' ? 'text-white' : 'text-navy',
        )}
      >
        Libox
      </span>
    </span>
  );
}
```

- [ ] **Step 3: Crear `src/app/icon.svg`** (favicon: isotipo solo, VIES §7.4) — mismo `<defs>` y `<path>` del isotipo:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="100" y2="100" gradientUnits="userSpaceOnUse">
      <stop stop-color="#6D28D9"/>
      <stop offset="1" stop-color="#8B5CF6"/>
    </linearGradient>
  </defs>
  <path d="M 27 12 L 27 56 Q 27 78 49 78 L 55 78 Q 74 78 74 63 Q 74 51 60 50 Q 74 49 74 36 Q 74 22 55 22 L 49 22"
        stroke="url(#g)" stroke-width="17" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

- [ ] **Step 4: Comparar el isotipo contra la referencia** — con el dev server arriba, capturar el header o un preview del componente y compararlo con `vies-reference.jpg` (Read de ambas imágenes). **Iterar el `d` del path hasta que la lectura sea "LB" (no "B" ni "13")** y las masas se parezcan a la referencia. Este es el único elemento con imagen de referencia: debe igualarla.

- [ ] **Step 5: Crear `src/components/prize-art.tsx`** — ilustración local por categoría (sin fotos externas): fondo con gradiente de marca suave + ícono lucide grande.

```tsx
import {
  Banknote,
  Car,
  Laptop,
  Plane,
  Sofa,
  type LucideIcon,
} from 'lucide-react';
import { CATEGORY_LABELS, type RaffleCategory } from '@/lib/raffle';
import { cn } from '@/lib/utils';

const CATEGORY_ART: Record<RaffleCategory, { icon: LucideIcon; from: string; to: string }> = {
  tecnologia: { icon: Laptop, from: '#6D28D9', to: '#8B5CF6' },
  vehiculos: { icon: Car, from: '#4C1D95', to: '#6D28D9' },
  viajes: { icon: Plane, from: '#5B21B6', to: '#8B5CF6' },
  hogar: { icon: Sofa, from: '#6D28D9', to: '#A78BFA' },
  efectivo: { icon: Banknote, from: '#0B1020', to: '#6D28D9' },
};

export function PrizeArt({
  category,
  size = 'card',
  className,
}: {
  category: RaffleCategory;
  size?: 'card' | 'hero';
  className?: string;
}) {
  const art = CATEGORY_ART[category];
  const Icon = art.icon;
  return (
    <div
      role="img"
      aria-label={`Ilustración de la categoría ${CATEGORY_LABELS[category]}`}
      className={cn(
        'flex items-center justify-center overflow-hidden',
        size === 'card' ? 'aspect-[16/10]' : 'aspect-[16/9] rounded-xl',
        className,
      )}
      style={{ background: `linear-gradient(135deg, ${art.from} 0%, ${art.to} 100%)` }}
    >
      <Icon
        aria-hidden="true"
        className={cn('text-white/85', size === 'card' ? 'h-14 w-14' : 'h-24 w-24')}
        strokeWidth={1.5}
      />
    </div>
  );
}
```

- [ ] **Step 6: Verificar** — `npm run lint && npm run typecheck && npm run build`. Expected: verde.

- [ ] **Step 7: Commit**

```bash
git add src/components/libox-logo.tsx src/components/prize-art.tsx src/app/icon.svg
git commit -m "feat(app): logo provisional según el VIES e ilustraciones de premios por categoría"
```

---

### Task 8: Header y footer del sitio

**Files:**
- Create: `src/components/site-header.tsx`, `src/components/site-footer.tsx`

**Interfaces:**
- Consumes: `LiboxLogo` de `@/components/libox-logo`, `Button` de `@/components/ui/button`.
- Produces: `<SiteHeader />`, `<SiteFooter />` (se montan en las páginas, no en el layout, para mantener el 404 simple).

- [ ] **Step 1: Crear `src/components/site-header.tsx`**

```tsx
import Link from 'next/link';
import { LiboxLogo } from '@/components/libox-logo';
import { Button } from '@/components/ui/button';

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-40 border-b border-border bg-background/90 backdrop-blur">
      <div className="mx-auto flex h-16 w-full max-w-6xl items-center justify-between px-4">
        <Link
          href="/"
          aria-label="Libox — inicio"
          className="rounded-md transition-opacity hover:opacity-80 focus-visible:outline-2 focus-visible:outline-ring"
        >
          <LiboxLogo />
        </Link>
        <Button variant="outline" disabled title="Disponible próximamente">
          Ingresar
        </Button>
      </div>
    </header>
  );
}
```

- [ ] **Step 2: Crear `src/components/site-footer.tsx`**

```tsx
import { LiboxLogo } from '@/components/libox-logo';

export function SiteFooter() {
  return (
    <footer className="mt-16 bg-navy text-white">
      <div className="mx-auto w-full max-w-6xl px-4 py-12">
        <LiboxLogo variant="inverse" />
        <p className="mt-3 text-sm text-white/80">Tu próxima oportunidad.</p>
        {/* [LEGAL→ABOGADO] Placeholder disclaimer pending counsel-approved copy. */}
        <p className="mt-6 max-w-2xl text-xs leading-relaxed text-white/60">
          Libox opera bajo la normativa peruana aplicable a rifas y sorteos con
          venta de tickets. La información legal completa, los términos y
          condiciones y las bases de cada sorteo estarán disponibles antes del
          lanzamiento comercial.
        </p>
        <p className="mt-4 text-xs text-white/40">
          © 2026 Libox. Todos los derechos reservados.
        </p>
      </div>
    </footer>
  );
}
```

- [ ] **Step 3: Verificar** — `npm run lint && npm run typecheck`. Expected: verde (los componentes aún no se montan; se integran en Task 9 y 10).

- [ ] **Step 4: Commit**

```bash
git add src/components/site-header.tsx src/components/site-footer.tsx
git commit -m "feat(app): header y footer del sitio con lockup y disclaimer legal placeholder"
```

---

### Task 9: Componentes de rifa — progreso, countdown y tarjeta

**Files:**
- Create: `src/components/raffle-progress.tsx`, `src/components/countdown.tsx`, `src/components/raffle-card.tsx`

**Interfaces:**
- Consumes: `computeProgressPercent`, `getCountdownParts`, `formatCountdown`, `isClosed`, `getRaffleBadge`, tipo `Raffle` de `@/lib/raffle`; `formatPEN` de `@/lib/format`; `PrizeArt`; `Badge`, `Card`, `Button` de shadcn.
- Produces: `<RaffleProgress sold total showNumbers? />`, `<Countdown endsAt variant?: 'compact' | 'large' />` (client), `<RaffleCard raffle />`.

- [ ] **Step 1: Crear `src/components/raffle-progress.tsx`**

```tsx
import { computeProgressPercent } from '@/lib/raffle';

export function RaffleProgress({
  sold,
  total,
  showNumbers = false,
}: {
  sold: number;
  total: number;
  showNumbers?: boolean;
}) {
  const percent = computeProgressPercent(sold, total);
  return (
    <div>
      {showNumbers && (
        <div className="mb-1.5 flex items-baseline justify-between text-sm">
          <span className="font-medium text-foreground">
            <span className="tabular-nums">{sold.toLocaleString('es-PE')}</span>
            <span className="text-muted-foreground"> de {total.toLocaleString('es-PE')} tickets</span>
          </span>
          <span className="font-semibold tabular-nums text-primary">{percent}%</span>
        </div>
      )}
      <div
        role="progressbar"
        aria-valuenow={percent}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={`${percent}% de tickets vendidos`}
        className="h-2 overflow-hidden rounded-full bg-secondary"
      >
        <div
          className="h-full origin-left rounded-full transition-transform"
          style={{
            background: 'var(--gradient-brand)',
            transform: `scaleX(${percent / 100})`,
          }}
        />
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Crear `src/components/countdown.tsx`** (client; evita mismatch de hidratación rendereando placeholder hasta montar)

```tsx
'use client';

import { useEffect, useMemo, useState } from 'react';
import { formatCountdown, getCountdownParts, isClosed } from '@/lib/raffle';
import { cn } from '@/lib/utils';

export function Countdown({
  endsAt,
  variant = 'compact',
  className,
}: {
  endsAt: Date | string;
  variant?: 'compact' | 'large';
  className?: string;
}) {
  const target = useMemo(() => new Date(endsAt), [endsAt]);
  const [now, setNow] = useState<Date | null>(null);

  useEffect(() => {
    setNow(new Date());
    const id = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  const base = cn(
    'font-[family-name:var(--font-manrope)] font-bold tabular-nums',
    variant === 'large' ? 'text-2xl' : 'text-sm',
    className,
  );

  if (!now) {
    return <span className={base} aria-hidden="true">--:--:--</span>;
  }

  if (isClosed(target, now)) {
    return <span className={cn(base, 'text-muted-foreground')}>Cerrada</span>;
  }

  return (
    <time dateTime={target.toISOString()} className={base} aria-label="Tiempo restante">
      {formatCountdown(getCountdownParts(target, now))}
    </time>
  );
}
```

- [ ] **Step 3: Crear `src/components/raffle-card.tsx`**

```tsx
import Link from 'next/link';
import { Countdown } from '@/components/countdown';
import { PrizeArt } from '@/components/prize-art';
import { RaffleProgress } from '@/components/raffle-progress';
import { Badge } from '@/components/ui/badge';
import { formatPEN } from '@/lib/format';
import { CATEGORY_LABELS, getRaffleBadge, type BadgeTone, type Raffle } from '@/lib/raffle';
import { cn } from '@/lib/utils';
import { Timer } from 'lucide-react';

const TONE_CLASSES: Record<BadgeTone, string> = {
  success: 'bg-success text-success-foreground',
  warning: 'bg-accent text-accent-foreground',
  closed: 'bg-navy text-white',
};

export function RaffleCard({ raffle }: { raffle: Raffle }) {
  const badge = getRaffleBadge(raffle, new Date());
  return (
    <Link
      href={`/rifas/${raffle.slug}`}
      className="group block rounded-lg focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
    >
      <article
        className="overflow-hidden rounded-lg border border-border bg-card transition-transform duration-200 group-hover:-translate-y-1 group-active:translate-y-0"
        style={{ boxShadow: 'var(--shadow-card)' }}
      >
        <div className="relative">
          <PrizeArt category={raffle.category} size="card" />
          <div className="absolute left-3 top-3 flex gap-2">
            <Badge variant="secondary">{CATEGORY_LABELS[raffle.category]}</Badge>
            <Badge className={cn('border-transparent', TONE_CLASSES[badge.tone])}>
              {badge.label}
            </Badge>
          </div>
        </div>
        <div className="space-y-3 p-4">
          <h3 className="line-clamp-1 text-base font-bold">{raffle.title}</h3>
          <div className="flex items-baseline justify-between">
            <p className="text-sm text-muted-foreground">Precio por ticket</p>
            <p className="font-[family-name:var(--font-manrope)] text-lg font-extrabold tabular-nums text-primary">
              {formatPEN(raffle.ticketPriceCents)}
            </p>
          </div>
          <RaffleProgress sold={raffle.soldTickets} total={raffle.totalTickets} />
          <div className="flex items-center justify-between pt-1">
            <span className="flex items-center gap-1.5 text-sm text-muted-foreground">
              <Timer aria-hidden="true" className="h-4 w-4" />
              <Countdown endsAt={raffle.endsAt} />
            </span>
            <span className="text-sm font-semibold text-primary transition-transform duration-200 group-hover:translate-x-0.5">
              Ver rifa →
            </span>
          </div>
        </div>
      </article>
    </Link>
  );
}
```

- [ ] **Step 4: Verificar** — `npm run lint && npm run typecheck && npm test`. Expected: verde.

- [ ] **Step 5: Commit**

```bash
git add src/components/raffle-progress.tsx src/components/countdown.tsx src/components/raffle-card.tsx
git commit -m "feat(app): componentes de progreso, cuenta regresiva y tarjeta de rifa"
```

---

### Task 10: Home — hero, sellos de confianza y catálogo con filtros

**Files:**
- Create: `src/components/catalog-section.tsx`
- Modify: `src/app/page.tsx` (reemplaza el placeholder de Task 3)

**Interfaces:**
- Consumes: `mockRaffles` de `@/lib/mock/raffles`; `RaffleCard`; `SiteHeader`/`SiteFooter`; `RAFFLE_CATEGORIES`, `CATEGORY_LABELS`, tipo `Raffle`.
- Produces: página `/` completa.

- [ ] **Step 1: Crear `src/components/catalog-section.tsx`** (client: estado del filtro)

```tsx
'use client';

import { useState } from 'react';
import { RaffleCard } from '@/components/raffle-card';
import { CATEGORY_LABELS, RAFFLE_CATEGORIES, type Raffle, type RaffleCategory } from '@/lib/raffle';
import { cn } from '@/lib/utils';

type Filter = RaffleCategory | 'todas';

export function CatalogSection({ raffles }: { raffles: Raffle[] }) {
  const [filter, setFilter] = useState<Filter>('todas');
  const visible = filter === 'todas' ? raffles : raffles.filter((r) => r.category === filter);
  const options: { value: Filter; label: string }[] = [
    { value: 'todas', label: 'Todas' },
    ...RAFFLE_CATEGORIES.map((c) => ({ value: c as Filter, label: CATEGORY_LABELS[c] })),
  ];

  return (
    <section aria-label="Catálogo de rifas" className="mx-auto w-full max-w-6xl px-4">
      <div role="group" aria-label="Filtrar por categoría" className="flex flex-wrap gap-2">
        {options.map((option) => (
          <button
            key={option.value}
            type="button"
            aria-pressed={filter === option.value}
            onClick={() => setFilter(option.value)}
            className={cn(
              'rounded-full border px-4 py-1.5 text-sm font-medium transition-[transform,opacity] duration-150',
              'hover:opacity-90 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring active:scale-95',
              filter === option.value
                ? 'border-transparent bg-primary text-primary-foreground'
                : 'border-border bg-card text-foreground',
            )}
          >
            {option.label}
          </button>
        ))}
      </div>
      {visible.length === 0 ? (
        <p className="mt-10 text-center text-muted-foreground">
          No hay rifas en esta categoría por ahora.
        </p>
      ) : (
        <ul className="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {visible.map((raffle) => (
            <li key={raffle.id}>
              <RaffleCard raffle={raffle} />
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
```

- [ ] **Step 2: Reescribir `src/app/page.tsx`**

```tsx
import { BadgeCheck, ShieldCheck, Lock } from 'lucide-react';
import { CatalogSection } from '@/components/catalog-section';
import { SiteFooter } from '@/components/site-footer';
import { SiteHeader } from '@/components/site-header';
import { mockRaffles } from '@/lib/mock/raffles';

const TRUST_SEALS = [
  {
    icon: ShieldCheck,
    title: 'Sorteos verificables',
    text: 'Cada sorteo genera una prueba criptográfica que cualquiera puede auditar.',
  },
  {
    icon: BadgeCheck,
    title: 'Organizadores con RUC',
    text: 'Solo personas y empresas verificadas con RUC activo pueden crear rifas.',
  },
  {
    icon: Lock,
    title: 'Pagos protegidos',
    text: 'Tu dinero se procesa con pasarelas reguladas y protocolos seguros.',
  },
];

export default function HomePage() {
  return (
    <>
      <SiteHeader />
      <main>
        <section className="mx-auto w-full max-w-6xl px-4 pb-12 pt-14 text-center sm:pt-20">
          <h1 className="mx-auto max-w-2xl text-4xl font-extrabold tracking-tight sm:text-5xl">
            Tu próxima <span className="text-primary">oportunidad</span>.
          </h1>
          <p className="mx-auto mt-4 max-w-xl text-lg text-muted-foreground">
            Participa en rifas digitales por premios reales, con sorteos
            verificables y organizadores verificados en el Perú.
          </p>
          <ul className="mx-auto mt-10 grid max-w-4xl grid-cols-1 gap-4 text-left sm:grid-cols-3">
            {TRUST_SEALS.map((seal) => (
              <li
                key={seal.title}
                className="rounded-lg border border-border bg-card p-4"
                style={{ boxShadow: 'var(--shadow-card)' }}
              >
                <seal.icon aria-hidden="true" className="h-6 w-6 text-primary" />
                <h2 className="mt-2 text-sm font-bold">{seal.title}</h2>
                <p className="mt-1 text-sm text-muted-foreground">{seal.text}</p>
              </li>
            ))}
          </ul>
        </section>
        <CatalogSection raffles={mockRaffles} />
      </main>
      <SiteFooter />
    </>
  );
}
```

- [ ] **Step 3: Verificar** — `npm run lint && npm run typecheck && npm run build`, y con el dev server abrir `http://localhost:3000`: hero + 3 sellos + chips de filtro + grilla con 12 tarjetas; el filtro "Vehículos" deja 2. Countdowns corriendo.

- [ ] **Step 4: Commit**

```bash
git add src/app/page.tsx src/components/catalog-section.tsx
git commit -m "feat(app): home con hero, sellos de confianza y catálogo filtrable"
```

---

### Task 11: Detalle de rifa, selector de tickets y 404

**Files:**
- Create: `src/components/ticket-selector.tsx`, `src/app/rifas/[slug]/page.tsx`, `src/app/not-found.tsx`

**Interfaces:**
- Consumes: `getRaffleBySlug`; `availableTickets`, `clampTicketQuantity`, `computeSubtotalCents`, `MAX_TICKETS_PER_PURCHASE`, `CATEGORY_LABELS`, `getRaffleBadge`; `formatPEN`; `Countdown`, `RaffleProgress`, `PrizeArt`, `SiteHeader`, `SiteFooter`; `Badge`, `Button`.
- Produces: página `/rifas/[slug]` completa y 404 en español.

- [ ] **Step 1: Crear `src/components/ticket-selector.tsx`** (client)

```tsx
'use client';

import { useState } from 'react';
import { Minus, Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { formatPEN } from '@/lib/format';
import { clampTicketQuantity, computeSubtotalCents, MAX_TICKETS_PER_PURCHASE } from '@/lib/raffle';

export function TicketSelector({
  ticketPriceCents,
  available,
}: {
  ticketPriceCents: number;
  available: number;
}) {
  const [quantity, setQuantity] = useState(() => clampTicketQuantity(1, available));
  const update = (next: number) => setQuantity(clampTicketQuantity(next, available));
  const maxSelectable = Math.min(available, MAX_TICKETS_PER_PURCHASE);

  return (
    <div className="rounded-lg border border-border bg-card p-5" style={{ boxShadow: 'var(--shadow-card)' }}>
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium">Cantidad de tickets</span>
        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            size="icon"
            aria-label="Quitar un ticket"
            disabled={quantity <= 1}
            onClick={() => update(quantity - 1)}
          >
            <Minus aria-hidden="true" className="h-4 w-4" />
          </Button>
          <span className="w-8 text-center text-lg font-bold tabular-nums" aria-live="polite">
            {quantity}
          </span>
          <Button
            variant="outline"
            size="icon"
            aria-label="Agregar un ticket"
            disabled={quantity >= maxSelectable}
            onClick={() => update(quantity + 1)}
          >
            <Plus aria-hidden="true" className="h-4 w-4" />
          </Button>
        </div>
      </div>
      <p className="mt-1 text-xs text-muted-foreground">
        Máximo {maxSelectable} tickets por compra.
      </p>
      <div className="mt-4 flex items-baseline justify-between border-t border-border pt-4">
        <span className="text-sm text-muted-foreground">Subtotal</span>
        <span className="font-[family-name:var(--font-manrope)] text-2xl font-extrabold tabular-nums text-primary">
          {formatPEN(computeSubtotalCents(quantity, ticketPriceCents))}
        </span>
      </div>
      <Button className="mt-4 w-full" size="lg" disabled>
        Comprar tickets
      </Button>
      <p className="mt-2 text-center text-xs text-muted-foreground">
        Las compras estarán disponibles próximamente.
      </p>
    </div>
  );
}
```

- [ ] **Step 2: Crear `src/app/rifas/[slug]/page.tsx`**

```tsx
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { BadgeCheck, PartyPopper, ShieldCheck, Ticket, Trophy } from 'lucide-react';
import { Countdown } from '@/components/countdown';
import { PrizeArt } from '@/components/prize-art';
import { RaffleProgress } from '@/components/raffle-progress';
import { SiteFooter } from '@/components/site-footer';
import { SiteHeader } from '@/components/site-header';
import { TicketSelector } from '@/components/ticket-selector';
import { Badge } from '@/components/ui/badge';
import { formatPEN } from '@/lib/format';
import { getRaffleBySlug } from '@/lib/mock/raffles';
import { availableTickets, CATEGORY_LABELS } from '@/lib/raffle';

const HOW_IT_WORKS = [
  {
    icon: Ticket,
    title: 'Participa',
    text: 'Elige cuántos tickets quieres y asegura tu número.',
  },
  {
    icon: ShieldCheck,
    title: 'Sorteo auditable',
    text: 'El ganador se elige con una prueba criptográfica pública que cualquiera puede verificar.',
  },
  {
    icon: Trophy,
    title: 'Entrega del premio',
    text: 'Coordinamos la entrega con el organizador y publicamos la constancia.',
  },
];

type Params = { slug: string };

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { slug } = await params;
  const raffle = getRaffleBySlug(slug);
  return { title: raffle ? raffle.title : 'Rifa no encontrada' };
}

export default async function RafflePage({ params }: { params: Promise<Params> }) {
  const { slug } = await params;
  const raffle = getRaffleBySlug(slug);
  if (!raffle) notFound();

  const finished = raffle.status === 'finalizada';

  return (
    <>
      <SiteHeader />
      <main className="mx-auto w-full max-w-6xl px-4 pt-8">
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-[1.2fr_1fr]">
          <div>
            <PrizeArt category={raffle.category} size="hero" />
            <section aria-label="Cómo funciona" className="mt-8">
              <h2 className="text-xl font-bold">Cómo funciona</h2>
              <ol className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-3">
                {HOW_IT_WORKS.map((step, index) => (
                  <li
                    key={step.title}
                    className="rounded-lg border border-border bg-card p-4"
                    style={{ boxShadow: 'var(--shadow-card)' }}
                  >
                    <step.icon aria-hidden="true" className="h-6 w-6 text-primary" />
                    <h3 className="mt-2 text-sm font-bold">
                      {index + 1}. {step.title}
                    </h3>
                    <p className="mt-1 text-sm text-muted-foreground">{step.text}</p>
                  </li>
                ))}
              </ol>
            </section>
          </div>

          <div className="space-y-5">
            <Badge variant="secondary">{CATEGORY_LABELS[raffle.category]}</Badge>
            <h1 className="text-3xl font-extrabold tracking-tight">{raffle.title}</h1>
            <p className="flex items-center gap-1.5 text-sm text-muted-foreground">
              <BadgeCheck aria-hidden="true" className="h-4 w-4 text-success" />
              {raffle.organizer.name} · RUC verificado {raffle.organizer.ruc}
            </p>
            <p className="text-muted-foreground">{raffle.description}</p>

            <div className="flex items-baseline justify-between rounded-lg bg-secondary px-4 py-3">
              <span className="text-sm text-muted-foreground">Precio por ticket</span>
              <span className="font-[family-name:var(--font-manrope)] text-2xl font-extrabold tabular-nums text-primary">
                {formatPEN(raffle.ticketPriceCents)}
              </span>
            </div>

            <RaffleProgress sold={raffle.soldTickets} total={raffle.totalTickets} showNumbers />

            {finished ? (
              <div
                className="rounded-lg border border-border bg-card p-5 text-center"
                style={{ boxShadow: 'var(--shadow-card)' }}
              >
                <PartyPopper aria-hidden="true" className="mx-auto h-8 w-8 text-primary" />
                <h2 className="mt-2 text-lg font-bold">Sorteo finalizado</h2>
                <p className="mt-1 text-muted-foreground">
                  Ganadora: <strong>{raffle.winner?.name}</strong> con el ticket{' '}
                  <strong className="tabular-nums">
                    #{String(raffle.winner?.ticketNumber).padStart(4, '0')}
                  </strong>
                </p>
              </div>
            ) : (
              <>
                <div className="flex items-center justify-between rounded-lg bg-secondary px-4 py-3">
                  <span className="text-sm text-muted-foreground">Cierra en</span>
                  <Countdown endsAt={raffle.endsAt} variant="large" className="text-primary" />
                </div>
                <TicketSelector
                  ticketPriceCents={raffle.ticketPriceCents}
                  available={availableTickets(raffle)}
                />
              </>
            )}
          </div>
        </div>
      </main>
      <SiteFooter />
    </>
  );
}
```

- [ ] **Step 3: Crear `src/app/not-found.tsx`**

```tsx
import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function NotFound() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 px-4 text-center">
      <h1 className="text-4xl font-extrabold">Página no encontrada</h1>
      <p className="max-w-md text-muted-foreground">
        La rifa que buscas no existe o ya no está disponible.
      </p>
      <Button asChild>
        <Link href="/">Volver al catálogo</Link>
      </Button>
    </main>
  );
}
```

- [ ] **Step 4: Verificar** — `npm run lint && npm run typecheck && npm run build && npm test`. En el navegador: `/rifas/iphone-16-pro` (activa, selector clampa en 20 y el CTA está deshabilitado con su nota), `/rifas/macbook-air-m4` (finalizada: ganadora visible, sin selector), `/rifas/no-existe` (404 en español).

- [ ] **Step 5: Commit**

```bash
git add src/components/ticket-selector.tsx src/app/rifas src/app/not-found.tsx
git commit -m "feat(app): detalle de rifa con selector de tickets, estado finalizado y 404"
```

---

### Task 12: Verificación visual — ≥ 2 rondas de screenshots

**Files:**
- Modify: cualquier archivo de UI que necesite ajuste (commits `style(app): ...`)

**Interfaces:**
- Consumes: dev server en `http://localhost:3000`; referencia `vies-reference.jpg` extraída en Task 7.

- [ ] **Step 1: Preparar captura**

```bash
npx playwright install chromium
```

- [ ] **Step 2: Ronda 1 — capturar 6 vistas**

```bash
npm run dev &  # si no está corriendo
for view in "390,844 mobile" "1440,900 desktop"; do
  set -- $view
  npx playwright screenshot --viewport-size "$1" --full-page \
    http://localhost:3000 "$SCRATCHPAD/round1-home-$2.png"
  npx playwright screenshot --viewport-size "$1" --full-page \
    http://localhost:3000/rifas/iphone-16-pro "$SCRATCHPAD/round1-detail-$2.png"
  npx playwright screenshot --viewport-size "$1" --full-page \
    http://localhost:3000/rifas/macbook-air-m4 "$SCRATCHPAD/round1-finished-$2.png"
done
```

- [ ] **Step 3: Revisar las capturas (herramienta Read) contra este checklist**
  - Logo: lectura "LB" (no "B" ni "13"), sin deformación, safe area ~1X, igualar la referencia `vies-reference.jpg`.
  - Paleta: morados `#6D28D9`/`#8B5CF6`, navy `#0B1020`; cero grises Tailwind por defecto; sombras teñidas, no negras.
  - Tipografía: Manrope en títulos/cifras (countdown con dígitos tabulares que no "saltan"), Instrument Sans en cuerpo.
  - Mobile-first: sin overflow horizontal en 390 px; targets táctiles ≥ 44 px; grilla 1 col móvil / 3 desktop.
  - Estados: badges correctos por rifa (Activa / Por agotarse / Cierra pronto / Finalizada); CTA de compra deshabilitado y con nota; ganadora visible en la finalizada.
  - Todo string visible en español (Perú); sin lorem ipsum ni texto en inglés.

- [ ] **Step 4: Corregir todo lo detectado** y commitear:

```bash
git add -A src/
git commit -m "style(app): ajustes visuales de la ronda 1 de verificación"
```

- [ ] **Step 5: Ronda 2 — recapturar las 6 vistas** (mismo comando con `round2-`) y volver a revisar. Si aún hay defectos, iterar (ronda 3+) hasta que el checklist pase completo. Commit final `style(app): ajustes visuales de la ronda 2 de verificación` (si hubo cambios).

---

### Task 13: Commands reales, reglas de tests y tanda 2 de plugins

**Files:**
- Modify: `src/CLAUDE.md` (sección Commands), `src/tests/CLAUDE.md` (segunda viñeta), `.claude/settings.json`

- [ ] **Step 1: Reemplazar la sección `## Commands` de `src/CLAUDE.md`** (hoy dice "Pending scaffold.") por:

```markdown
## Commands

Run from the repo root (`package.json` lives there; app code in `src/`):

- `npm run dev` — dev server at `http://localhost:3000`
- `npm run build` — production build
- `npm run lint` — ESLint over the repo
- `npm run typecheck` — `tsc --noEmit`
- `npm test` — Vitest suite (single run)
- `npm test -- src/tests/unit/raffle.test.ts` — a single test file
- `npm run test:watch` — Vitest in watch mode
```

- [ ] **Step 2: En `src/tests/CLAUDE.md`**, reemplazar la viñeta "**Commands pending scaffold** …" por:

```markdown
- **Commands**: `npm test` (full suite) · `npm test -- <path/to/file.test.ts>`
  (single file) · `npm run test:watch` (watch mode). Unit tests live in
  `src/tests/unit/`.
```

- [ ] **Step 3: Habilitar la tanda 2 de plugins en `.claude/settings.json`** — dentro de `enabledPlugins`, después de `"context-mode@context-mode": true`, agregar:

```json
"security-guidance@claude-plugins-official": true,
"claude-security@claude-plugins-official": true,
"typescript-lsp@claude-plugins-official": true,
"pr-review-toolkit@claude-plugins-official": true,
"vercel@claude-plugins-official": true
```

Validar el JSON (`python3 -m json.tool .claude/settings.json`). Si al reiniciar sesión algún id no existe en el marketplace oficial, corregirlo al id real publicado (la intención — qué plugin es — está en el plan de plugins de `src/CLAUDE.md`).

- [ ] **Step 4: Verificar markdownlint**

```bash
npx --yes markdownlint-cli2 "src/CLAUDE.md" "src/tests/CLAUDE.md"
```

Expected: 0 issues.

- [ ] **Step 5: Commit**

```bash
git add src/CLAUDE.md src/tests/CLAUDE.md .claude/settings.json
git commit -m "docs(claude): comandos reales del scaffold y tanda 2 de plugins"
```

---

### Task 14: Gate final y Pull Request

- [ ] **Step 1: Suite completa desde cero**

```bash
npm run lint && npm run typecheck && npm run build && npm test && \
npx --yes markdownlint-cli2 "docs/**/*.md"
```

Expected: todo verde. Cualquier fallo se arregla antes de continuar (verification-before-completion: no declarar éxito sin ver esta salida).

- [ ] **Step 2: Revisar el diff completo de la rama** (`git log --oneline main..HEAD` + `git diff main --stat`): sin archivos fuera de alcance (`.gitignore` intacto, sin `README.md`, sin cambios en `docs/` salvo spec/plan, `src/assets/` intacto).

- [ ] **Step 3: Push y PR** (sin atribución de IA en el body — regla raíz):

```bash
git push -u origin feat/marketplace-mock
gh pr create --title "feat: primera rebanada del frontend — marketplace con datos mock" --body "$(cat <<'EOF'
## Qué incluye

- Scaffold real de la app en la raíz del repo (Next.js App Router + TypeScript + Tailwind v4 + shadcn/ui + Vitest), según el spec aprobado `docs/superpowers/specs/2026-08-03-marketplace-mock-design.md`.
- Design tokens derivados del estándar de identidad congelado (VIES v1.0 en `src/assets/`), tipografías Manrope + Instrument Sans y logo provisional recreado del plano técnico (pendiente de reemplazo por el arte maestro).
- Home/catálogo con hero, sellos de confianza, filtros por categoría y 12 rifas mock en 5 categorías con estados variados.
- Detalle de rifa con progreso, cuenta regresiva viva, selector de tickets con subtotal y CTA de compra deshabilitado; estado finalizado con ganadora; 404 en español.
- Lógica pura con TDD (Vitest): progreso, countdown, moneda es-PE y clamp del selector.
- Mismo PR: sección Commands de `src/CLAUDE.md` y `src/tests/CLAUDE.md` actualizadas; tanda 2 de plugins habilitada en `.claude/settings.json`.

## Verificación

- `lint`, `typecheck`, `build` y Vitest en verde.
- ≥ 2 rondas de verificación visual por screenshots (móvil 390px y desktop 1440px) desde localhost.
- Sin backend: todo es mock; el CTA de compra queda deshabilitado a propósito.
EOF
)"
```

- [ ] **Step 4: Confirmar checks del PR en verde** (`gh pr checks --watch`): `commitlint` (correo @liboxapp.com), `markdownlint`, `links`. Diego hace el rebase-and-merge (approvals en 0).

---

## Self-Review (ya aplicado)

- **Cobertura del spec:** scaffold raíz+src (T1), shadcn (T2), tokens+tipografías+tono (T3), moneda (T4), lógica pura TDD (T5), 12 rifas/5 categorías/estados (T6), logo provisional+ilustraciones (T7), header/footer+disclaimer `[LEGAL→ABOGADO]` (T8), card/progreso/countdown (T9), home+filtros+sellos (T10), detalle+selector+CTA deshabilitado+finalizada+404 (T11), ≥2 rondas visuales (T12), Commands+tests-doc+plugins (T13), gate+PR (T14). Criterios de aceptación del spec cubiertos por T12 (visual), T14 (checks) y T5 (TDD).
- **Placeholders:** ninguno — todo el código es completo y ejecutable tal cual.
- **Consistencia de tipos:** los nombres de `@/lib/raffle` (Interfaces de T5) son los mismos consumidos en T6, T9, T10 y T11.
