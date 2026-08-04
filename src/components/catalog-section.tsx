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
              'inline-flex min-h-11 items-center rounded-full border px-5 text-sm font-medium transition-[transform,opacity] duration-150',
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
