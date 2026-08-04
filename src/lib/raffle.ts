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
