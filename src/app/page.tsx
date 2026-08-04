import { BadgeCheck, ShieldCheck, Lock } from 'lucide-react';
import { CatalogSection } from '@/components/catalog-section';
import { SiteFooter } from '@/components/site-footer';
import { SiteHeader } from '@/components/site-header';
import { mockRaffles } from '@/lib/mock/raffles';

const TRUST_SEALS = [
  {
    icon: ShieldCheck,
    title: 'Sorteos verificables',
    text: 'Cada sorteo genera una prueba criptográfica que cualquiera puede auditar.',
  },
  {
    icon: BadgeCheck,
    title: 'Organizadores con RUC',
    text: 'Solo personas y empresas verificadas con RUC activo pueden crear rifas.',
  },
  {
    icon: Lock,
    title: 'Pagos protegidos',
    text: 'Tu dinero se procesa con pasarelas reguladas y protocolos seguros.',
  },
];

export default function HomePage() {
  return (
    <>
      <SiteHeader />
      <main>
        <section className="mx-auto w-full max-w-6xl px-4 pb-12 pt-14 text-center sm:pt-20">
          <h1 className="mx-auto max-w-2xl text-4xl font-extrabold tracking-tight sm:text-5xl">
            Tu próxima <span className="text-primary">oportunidad</span>.
          </h1>
          <p className="mx-auto mt-4 max-w-xl text-lg text-muted-foreground">
            Participa en rifas digitales por premios reales, con sorteos
            verificables y organizadores verificados en el Perú.
          </p>
          <ul className="mx-auto mt-10 grid max-w-4xl grid-cols-1 gap-4 text-left sm:grid-cols-3">
            {TRUST_SEALS.map((seal) => (
              <li
                key={seal.title}
                className="rounded-lg border border-border bg-card p-4"
                style={{ boxShadow: 'var(--shadow-card)' }}
              >
                <seal.icon aria-hidden="true" className="h-6 w-6 text-primary" />
                <h2 className="mt-2 text-sm font-bold">{seal.title}</h2>
                <p className="mt-1 text-sm text-muted-foreground">{seal.text}</p>
              </li>
            ))}
          </ul>
        </section>
        <CatalogSection raffles={mockRaffles} />
      </main>
      <SiteFooter />
    </>
  );
}
