import Link from 'next/link';
import { buttonVariants } from '@/components/ui/button';
import { cn } from '@/lib/utils';

export default function NotFound() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 px-4 text-center">
      <h1 className="text-4xl font-extrabold">Página no encontrada</h1>
      <p className="max-w-md text-muted-foreground">
        La rifa que buscas no existe o ya no está disponible.
      </p>
      <Link href="/" className={cn(buttonVariants({ size: 'default' }))}>
        Volver al catálogo
      </Link>
    </main>
  );
}
