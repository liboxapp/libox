import type { Metadata } from 'next';
import { Instrument_Sans, Manrope } from 'next/font/google';
import './globals.css';

const manrope = Manrope({
  subsets: ['latin'],
  variable: '--font-manrope',
  weight: ['400', '600', '700', '800'],
});

const instrumentSans = Instrument_Sans({
  subsets: ['latin'],
  variable: '--font-instrument',
  weight: ['400', '500', '600'],
});

export const metadata: Metadata = {
  title: {
    default: 'Libox — Tu próxima oportunidad',
    template: '%s · Libox',
  },
  description:
    'Marketplace de rifas digitales con sorteos verificables. Participa por premios reales con organizadores verificados en el Perú.',
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    /*
     * The next/font variable classes must live on <html>, not <body>: the
     * `@theme inline` block in globals.css declares --font-sans/--font-heading
     * on :root referencing --font-instrument/--font-manrope. A var() that is
     * undefined on the element where it is read makes the whole custom property
     * compute to the guaranteed-invalid value, which then inherits down — so
     * declaring the fonts on <body> left every base rule falling back to the
     * system stack.
     */
    <html lang="es-PE" className={`${manrope.variable} ${instrumentSans.variable}`}>
      <body className="antialiased">{children}</body>
    </html>
  );
}
