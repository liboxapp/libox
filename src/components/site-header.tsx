import Link from 'next/link';
import { LiboxLogo } from '@/components/libox-logo';
import { Button } from '@/components/ui/button';

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-40 border-b border-border bg-background/90 backdrop-blur">
      <div className="mx-auto flex h-16 w-full max-w-6xl items-center justify-between px-4">
        <Link
          href="/"
          aria-label="Libox — inicio"
          className="flex min-h-11 items-center rounded-md transition-opacity hover:opacity-80 focus-visible:outline-2 focus-visible:outline-ring"
        >
          <LiboxLogo />
        </Link>
        <Button variant="outline" disabled title="Disponible próximamente">
          Ingresar
        </Button>
      </div>
    </header>
  );
}
