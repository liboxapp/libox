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
    <html lang="es-PE">
      <body className={`${manrope.variable} ${instrumentSans.variable} antialiased`}>
        {children}
      </body>
    </html>
  );
}
