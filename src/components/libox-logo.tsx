import { cn } from '@/lib/utils';

/*
 * PROVISIONAL brand asset — the "LB Opportunity Loop" isotype, retraced from
 * the frozen reference art in the brand standard
 * src/assets/LIBOX_Visual_Identity_Engineering_Standard_v1_0.pdf (VIES v1.0).
 *
 * VIES 3.1 is the acceptance test: the L must read as the primary structure
 * and the B must stay integrated — never a lone B, never a "13".
 *
 * Centerlines were measured off the frozen art and normalised to this 100x100
 * box (VIES 3.2 warns the 10X construction box is not the visible area, so the
 * box below is ours; the art is what the path reproduces):
 *   - Stroke 1 "L + lower lobe": stem, bottom-left corner (r 9.43), foot,
 *     then the lower lobe as an exact right-hand semicircle (r 16.29) that
 *     lands on the waist and runs left to a free cap.
 *   - Stroke 2 "upper lobe": top bar from a free cap, quarter arc (r 12.17),
 *     short vertical, quarter arc back into the waist — where the two strokes
 *     fuse into the "sola forma continua" of VIES 3.1.
 * The B lobes bulge right off an implied spine; the L stem carries the mark.
 * Round caps and joins (VIES 3.3). Purple -> Violet gradient (VIES 6.4).
 *
 * Replace with the official master SVG when the brand export package lands.
 * Do not deform, recolor, or change proportions (VIES 8, usos no permitidos).
 */
const ISOTYPE_PATH =
  'M16.23 19.14 V71.43 A9.43 9.43 0 0 0 25.66 80.86 H67.49 A16.29 16.29 0 0 0 67.49 48.28 H48.97 ' +
  'M43.49 20.52 H62.69 A12.17 12.17 0 0 1 74.86 32.69 V36.11 A12.17 12.17 0 0 1 62.69 48.28';

export function LiboxIsotype({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 100 100"
      fill="none"
      aria-hidden="true"
      className={className}
    >
      <defs>
        <linearGradient
          id="libox-brand-gradient"
          x1="0"
          y1="0"
          x2="100"
          y2="100"
          gradientUnits="userSpaceOnUse"
        >
          <stop stopColor="#6D28D9" />
          <stop offset="1" stopColor="#8B5CF6" />
        </linearGradient>
      </defs>
      <path
        d={ISOTYPE_PATH}
        stroke="url(#libox-brand-gradient)"
        strokeWidth="12"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function LiboxLogo({
  variant = 'default',
  className,
}: {
  variant?: 'default' | 'inverse';
  className?: string;
}) {
  /*
   * Lockup (VIES 5) measured off the official horizontal lockup art: isotype
   * height : wordmark cap height = 1.9 : 1, optically centred, separation
   * ~0.3x the isotype height. Heads-up: the VIES 2.2 table instead states
   * 10X : 10X with a 1X gap — the frozen lockup art does not agree with its
   * own table, and the art is what we reproduce. Flagged for the brand owner.
   * `gap-1` reads tight in the markup because the isotype's 100x100 box already
   * carries its safe area, so the rendered gap lands on the art. Re-measure if
   * that padding ever changes.
   */
  return (
    <span className={cn('flex items-center gap-1', className)}>
      <LiboxIsotype className="h-9 w-9 shrink-0" />
      <span
        className={cn(
          // VIES 4: wordmark in Manrope ExtraBold, uppercase, tracking 0.25X
          'font-[family-name:var(--font-manrope)] text-xl font-extrabold uppercase tracking-[0.02em]',
          variant === 'inverse' ? 'text-white' : 'text-navy',
        )}
      >
        Libox
      </span>
    </span>
  );
}
