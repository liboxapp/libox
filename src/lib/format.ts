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
  // Covers both U+00A0 (NBSP) and U+202F (narrow NBSP), which ICU may emit.
  return penFormatter.format(cents / 100).replace(/[\u00A0\u202F]/g, ' ');
}
