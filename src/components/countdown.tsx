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
    // eslint-disable-next-line react-hooks/set-state-in-effect
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
