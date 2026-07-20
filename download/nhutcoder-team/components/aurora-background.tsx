"use client";

import { useEffect, useRef } from "react";
import { useMousePosition } from "@/hooks/use-mouse-position";

/**
 * AuroraBackground — animated gradient mesh that subtly drifts.
 * Responds to mouse position (parallax) for a premium, alive feel.
 * Purely decorative — `aria-hidden`, pointer-events:none.
 */
export function AuroraBackground() {
  const ref = useRef<HTMLDivElement>(null);
  const mouse = useMousePosition();

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    // Map mouse normalised vector to subtle parallax
    el.style.setProperty("--mx", `${mouse.nx * 30}px`);
    el.style.setProperty("--my", `${mouse.ny * 30}px`);
  }, [mouse]);

  return (
    <div
      ref={ref}
      aria-hidden="true"
      className="pointer-events-none absolute inset-0 -z-10 overflow-hidden"
    >
      {/* Base radial — primary brand glow, top right */}
      <div
        className="absolute -right-32 -top-32 h-[640px] w-[640px] rounded-full opacity-60 blur-[140px]"
        style={{
          background:
            "radial-gradient(circle at center, oklch(0.74 0.21 134 / 0.18), transparent 65%)",
          transform: "translate(var(--mx), var(--my))",
        }}
      />
      {/* Secondary — violet, bottom left */}
      <div
        className="absolute -bottom-40 -left-32 h-[560px] w-[560px] rounded-full opacity-50 blur-[150px]"
        style={{
          background:
            "radial-gradient(circle at center, oklch(0.62 0.25 295 / 0.16), transparent 65%)",
          transform: "translate(calc(var(--mx) * -1), calc(var(--my) * -1))",
        }}
      />
      {/* Tertiary — small cyan accent, middle */}
      <div
        className="absolute left-1/2 top-1/2 h-[420px] w-[420px] -translate-x-1/2 -translate-y-1/2 rounded-full opacity-30 blur-[120px]"
        style={{
          background:
            "radial-gradient(circle at center, oklch(0.7 0.18 200 / 0.10), transparent 70%)",
        }}
      />
      {/* Grid overlay */}
      <div className="absolute inset-0 bg-grid-faint [mask-image:radial-gradient(ellipse_at_center,black_30%,transparent_75%)]" />
      {/* Noise overlay */}
      <div className="absolute inset-0 bg-noise opacity-[0.5] mix-blend-soft-light" />
    </div>
  );
}
