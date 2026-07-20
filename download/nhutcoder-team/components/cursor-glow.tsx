"use client";

import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";

/**
 * CursorGlow — a soft radial highlight that trails the cursor.
 * Disabled on touch devices and on prefers-reduced-motion.
 * Uses CSS variables so it inherits the brand palette.
 */
export function CursorGlow({ className }: { className?: string }) {
  const [visible, setVisible] = useState(false);
  const [pos, setPos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    if (typeof window === "undefined") return;
    const isTouch = window.matchMedia("(hover: none)").matches;
    const reduce = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;
    if (isTouch || reduce) return;

    let raf = 0;
    let target = { x: 0, y: 0 };
    let current = { x: 0, y: 0 };

    const onMove = (e: MouseEvent) => {
      target = { x: e.clientX, y: e.clientY };
      if (!visible) setVisible(true);
    };

    const onLeave = () => setVisible(false);

    const loop = () => {
      // Easing follow
      current.x += (target.x - current.x) * 0.15;
      current.y += (target.y - current.y) * 0.15;
      setPos({ x: current.x, y: current.y });
      raf = requestAnimationFrame(loop);
    };

    window.addEventListener("mousemove", onMove, { passive: true });
    document.documentElement.addEventListener("mouseleave", onLeave);
    raf = requestAnimationFrame(loop);

    return () => {
      window.removeEventListener("mousemove", onMove);
      document.documentElement.removeEventListener("mouseleave", onLeave);
      cancelAnimationFrame(raf);
    };
  }, [visible]);

  return (
    <div
      aria-hidden="true"
      className={cn(
        "pointer-events-none fixed inset-0 z-[5] hidden md:block",
        className
      )}
      style={{
        opacity: visible ? 1 : 0,
        transition: "opacity 600ms ease",
      }}
    >
      <div
        className="absolute h-[480px] w-[480px] -translate-x-1/2 -translate-y-1/2 rounded-full blur-[120px]"
        style={{
          left: pos.x,
          top: pos.y,
          background:
            "radial-gradient(circle, oklch(0.74 0.21 134 / 0.10), transparent 65%)",
        }}
      />
    </div>
  );
}
