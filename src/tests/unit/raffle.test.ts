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
