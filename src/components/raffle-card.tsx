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
