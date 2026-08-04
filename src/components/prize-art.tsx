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

/*
 * Local prize illustrations — no stock photography, no external requests.
 * Each category gets its own cut of the brand gradient so a catalogue of
 * cards reads as one family while still being told apart at a glance.
 * Ramps derive from the brand violet range; tints beyond the 4 frozen VIES
 * colors are pending brand-owner ratification.
 */
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
        'relative flex items-center justify-center overflow-hidden',
        size === 'card' ? 'aspect-[16/10]' : 'aspect-[16/9] rounded-xl',
        className,
      )}
      style={{ background: `linear-gradient(135deg, ${art.from} 0%, ${art.to} 100%)` }}
    >
      {/*
       * Brand echo: the isotype's lower lobe — the "opportunity loop" — as an
       * exact semicircle bleeding off the top and bottom edges, so no stroke
       * cap ever reads as a stray blob. Echoes the mark's rounded arc language,
       * so a prize tile is recognisably Libox without repeating the logo.
       */}
      <svg
        viewBox="0 0 160 100"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
        fill="none"
        className="pointer-events-none absolute inset-0 h-full w-full"
      >
        <path
          d="M78 -12 A62 62 0 0 1 78 112"
          stroke="#FFFFFF"
          strokeOpacity="0.08"
          strokeWidth="16"
        />
      </svg>
      <Icon
        aria-hidden="true"
        className={cn('relative text-white/85', size === 'card' ? 'h-14 w-14' : 'h-24 w-24')}
        strokeWidth={1.5}
      />
    </div>
  );
}
