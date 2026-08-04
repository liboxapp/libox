import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { BadgeCheck, PartyPopper, ShieldCheck, Ticket, Trophy } from 'lucide-react';
import { Countdown } from '@/components/countdown';
import { PrizeArt } from '@/components/prize-art';
import { RaffleProgress } from '@/components/raffle-progress';
import { SiteFooter } from '@/components/site-footer';
import { SiteHeader } from '@/components/site-header';
import { TicketSelector } from '@/components/ticket-selector';
import { Badge } from '@/components/ui/badge';
import { formatPEN } from '@/lib/format';
import { getRaffleBySlug } from '@/lib/mock/raffles';
import { availableTickets, CATEGORY_LABELS } from '@/lib/raffle';

const HOW_IT_WORKS = [
  {
    icon: Ticket,
    title: 'Participa',
    text: 'Elige cuántos tickets quieres y asegura tu número.',
  },
  {
    icon: ShieldCheck,
    title: 'Sorteo auditable',
    text: 'El ganador se elige con una prueba criptográfica pública que cualquiera puede verificar.',
  },
  {
    icon: Trophy,
    title: 'Entrega del premio',
    text: 'Coordinamos la entrega con el organizador y publicamos la constancia.',
  },
];

type Params = { slug: string };

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { slug } = await params;
  const raffle = getRaffleBySlug(slug);
  return { title: raffle ? raffle.title : 'Rifa no encontrada' };
}

export default async function RafflePage({ params }: { params: Promise<Params> }) {
  const { slug } = await params;
  const raffle = getRaffleBySlug(slug);
  if (!raffle) notFound();

  const finished = raffle.status === 'finalizada';

  return (
    <>
      <SiteHeader />
      <main className="mx-auto w-full max-w-6xl px-4 pt-8">
        {/*
          * Three grid children in reading order: art, raffle, explainer. On
          * mobile that is the order a buyer needs — prize, price, countdown,
          * checkout — with "Cómo funciona" after it instead of between the art
          * and the product. The explicit lg placement puts the explainer back
          * under the art in the left column on desktop.
          */}
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-[1.2fr_1fr]">
          <PrizeArt
            category={raffle.category}
            size="hero"
            className="lg:col-start-1 lg:row-start-1"
          />

          <div className="space-y-5 lg:col-start-2 lg:row-span-2 lg:row-start-1">
            <Badge variant="secondary">{CATEGORY_LABELS[raffle.category]}</Badge>
            <h1 className="text-3xl font-extrabold tracking-tight">{raffle.title}</h1>
            <p className="flex items-center gap-1.5 text-sm text-muted-foreground">
              <BadgeCheck aria-hidden="true" className="h-4 w-4 text-success" />
              {raffle.organizer.name} · RUC verificado {raffle.organizer.ruc}
            </p>
            <p className="text-muted-foreground">{raffle.description}</p>

            <div className="flex items-baseline justify-between rounded-lg bg-secondary px-4 py-3">
              <span className="text-sm text-muted-foreground">Precio por ticket</span>
              <span className="font-[family-name:var(--font-manrope)] text-2xl font-extrabold tabular-nums text-primary">
                {formatPEN(raffle.ticketPriceCents)}
              </span>
            </div>

            <RaffleProgress sold={raffle.soldTickets} total={raffle.totalTickets} showNumbers />

            {finished ? (
              <div
                className="rounded-lg border border-border bg-card p-5 text-center"
                style={{ boxShadow: 'var(--shadow-card)' }}
              >
                <PartyPopper aria-hidden="true" className="mx-auto h-8 w-8 text-primary" />
                <h2 className="mt-2 text-lg font-bold">Sorteo finalizado</h2>
                {raffle.winner && (
                  <p className="mt-1 text-muted-foreground">
                    Ganadora: <strong>{raffle.winner.name}</strong> con el ticket{' '}
                    <strong className="tabular-nums">
                      #{String(raffle.winner.ticketNumber).padStart(4, '0')}
                    </strong>
                  </p>
                )}
              </div>
            ) : (
              <>
                <div className="flex items-center justify-between rounded-lg bg-secondary px-4 py-3">
                  <span className="text-sm text-muted-foreground">Cierra en</span>
                  <Countdown endsAt={raffle.endsAt} variant="large" className="text-primary" />
                </div>
                <TicketSelector
                  ticketPriceCents={raffle.ticketPriceCents}
                  available={availableTickets(raffle)}
                />
              </>
            )}
          </div>

          <section
            aria-label="Cómo funciona"
            className="lg:col-start-1 lg:row-start-2"
          >
            <h2 className="text-xl font-bold">Cómo funciona</h2>
            <ol className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-3">
              {HOW_IT_WORKS.map((step, index) => (
                <li
                  key={step.title}
                  className="rounded-lg border border-border bg-card p-4"
                  style={{ boxShadow: 'var(--shadow-card)' }}
                >
                  <step.icon aria-hidden="true" className="h-6 w-6 text-primary" />
                  <h3 className="mt-2 text-sm font-bold">
                    {index + 1}. {step.title}
                  </h3>
                  <p className="mt-1 text-sm text-muted-foreground">{step.text}</p>
                </li>
              ))}
            </ol>
          </section>
        </div>
      </main>
      <SiteFooter />
    </>
  );
}
