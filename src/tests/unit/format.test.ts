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
