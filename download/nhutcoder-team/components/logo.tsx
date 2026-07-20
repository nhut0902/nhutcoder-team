import { cn } from "@/lib/utils";

interface LogoProps {
  className?: string;
  /** Hide the wordmark — show only the mark */
  markOnly?: boolean;
}

/**
 * NhutCoder Team — custom wordmark + glyph.
 * The glyph is a terminal prompt `>` morphed into a forward-slash pair,
 * evoking code, momentum, and a stylised "N".
 */
export function Logo({ className, markOnly = false }: LogoProps) {
  return (
    <span className={cn("inline-flex items-center gap-2.5", className)}>
      <span
        aria-hidden="true"
        className="relative grid h-8 w-8 place-items-center rounded-[10px] border border-[var(--color-edge-strong)] bg-[var(--color-surface-2)]"
      >
        <svg
          viewBox="0 0 32 32"
          fill="none"
          className="h-5 w-5"
          aria-hidden="true"
        >
          <path
            d="M8 22V10l12 12V10"
            stroke="url(#lg)"
            strokeWidth="2.4"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <circle cx="24.5" cy="9" r="1.6" fill="var(--color-brand-400)" />
          <defs>
            <linearGradient
              id="lg"
              x1="8"
              y1="10"
              x2="24"
              y2="22"
              gradientUnits="userSpaceOnUse"
            >
              <stop stopColor="var(--color-brand-300)" />
              <stop offset="1" stopColor="var(--color-accent-400)" />
            </linearGradient>
          </defs>
        </svg>
      </span>
      {!markOnly && (
        <span className="flex items-baseline gap-1 font-display text-[15px] font-semibold tracking-tight text-[var(--color-ink-strong)]">
          NhutCoder
          <span className="text-[var(--color-brand-400)]">/</span>
          <span className="text-[var(--color-ink-faint)]">team</span>
        </span>
      )}
    </span>
  );
}
