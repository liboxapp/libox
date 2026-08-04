'use client';

import { useState } from 'react';
import { Minus, Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { formatPEN } from '@/lib/format';
import { clampTicketQuantity, computeSubtotalCents, MAX_TICKETS_PER_PURCHASE } from '@/lib/raffle';

export function TicketSelector({
  ticketPriceCents,
  available,
}: {
  ticketPriceCents: number;
  available: number;
}) {
  const [quantity, setQuantity] = useState(() => clampTicketQuantity(1, available));
  const update = (next: number) => setQuantity(clampTicketQuantity(next, available));
  const maxSelectable = Math.min(available, MAX_TICKETS_PER_PURCHASE);

  return (
    <div className="rounded-lg border border-border bg-card p-5" style={{ boxShadow: 'var(--shadow-card)' }}>
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium">Cantidad de tickets</span>
        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            size="icon"
            aria-label="Quitar un ticket"
            disabled={quantity <= 1}
            onClick={() => update(quantity - 1)}
          >
            <Minus aria-hidden="true" className="h-4 w-4" />
          </Button>
          <span className="w-8 text-center text-lg font-bold tabular-nums" aria-live="polite">
            {quantity}
          </span>
          <Button
            variant="outline"
            size="icon"
            aria-label="Agregar un ticket"
            disabled={quantity >= maxSelectable}
            onClick={() => update(quantity + 1)}
          >
            <Plus aria-hidden="true" className="h-4 w-4" />
          </Button>
        </div>
      </div>
      <p className="mt-1 text-xs text-muted-foreground">
        Máximo {maxSelectable} tickets por compra.
      </p>
      <div className="mt-4 flex items-baseline justify-between border-t border-border pt-4">
        <span className="text-sm text-muted-foreground">Subtotal</span>
        <span className="font-[family-name:var(--font-manrope)] text-2xl font-extrabold tabular-nums text-primary">
          {formatPEN(computeSubtotalCents(quantity, ticketPriceCents))}
        </span>
      </div>
      <Button className="mt-4 w-full" size="lg" disabled>
        Comprar tickets
      </Button>
      <p className="mt-2 text-center text-xs text-muted-foreground">
        Las compras estarán disponibles próximamente.
      </p>
    </div>
  );
}
