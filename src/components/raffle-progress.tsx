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
