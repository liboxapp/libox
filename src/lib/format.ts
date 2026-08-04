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
  return penFormatter.format(cents / 100).replace(/ /g, ' ');
}
