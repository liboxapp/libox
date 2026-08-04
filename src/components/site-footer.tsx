import { LiboxLogo } from '@/components/libox-logo';

export function SiteFooter() {
  return (
    <footer className="mt-16 bg-navy text-white">
      <div className="mx-auto w-full max-w-6xl px-4 py-12">
        <LiboxLogo variant="inverse" />
        <p className="mt-3 text-sm text-white/80">Tu próxima oportunidad.</p>
        {/* [LEGAL→ABOGADO] Placeholder disclaimer pending counsel-approved copy. */}
        <p className="mt-6 max-w-2xl text-xs leading-relaxed text-white/60">
          Libox opera bajo la normativa peruana aplicable a rifas y sorteos con
          venta de tickets. La información legal completa, los términos y
          condiciones y las bases de cada sorteo estarán disponibles antes del
          lanzamiento comercial.
        </p>
        <p className="mt-4 text-xs text-white/40">
          © 2026 Libox. Todos los derechos reservados.
        </p>
      </div>
    </footer>
  );
}
