"use client";

import { motion, useSpring, useTransform } from "framer-motion";
import { useScrollProgress } from "@/hooks/use-scroll-progress";

/**
 * Slim scroll progress bar that lives at the very top of the viewport.
 * Springs smoothly so it never feels jittery on fast scrolls.
 */
export function ScrollProgress() {
  const progress = useScrollProgress();
  const scaleX = useSpring(progress, {
    stiffness: 180,
    damping: 28,
    restDelta: 0.001,
  });
  const width = useTransform(scaleX, (v) => `${v * 100}%`);

  return (
    <div
      aria-hidden="true"
      className="pointer-events-none fixed inset-x-0 top-0 z-[60] h-px"
    >
      <motion.div
        style={{ width }}
        className="h-full origin-left bg-gradient-to-r from-[var(--color-brand-500)] via-[var(--color-accent-400)] to-[var(--color-brand-300)]"
      />
    </div>
  );
}
