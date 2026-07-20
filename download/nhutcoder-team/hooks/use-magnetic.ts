"use client";

import { useEffect, useRef } from "react";
import type { RefObject } from "react";

interface MagneticOptions {
  strength?: number; // 0..1, how strongly the element follows the cursor
  radius?: number; // px, max distance the element can move
}

/**
 * Magnetic hover effect — the bound element drifts toward the cursor while
 * the cursor is inside the element, then springs back on leave.
 *
 * Pair with `transition: transform 0.3s var(--ease-premium)` in CSS.
 */
export function useMagnetic<T extends HTMLElement = HTMLButtonElement>(
  options: MagneticOptions = {}
): RefObject<T | null> {
  const { strength = 0.35, radius = 14 } = options;
  const ref = useRef<T>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const isTouch =
      typeof window !== "undefined" &&
      window.matchMedia("(hover: none)").matches;
    if (isTouch) return;

    const onMove = (e: MouseEvent) => {
      const rect = el.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const dx = (e.clientX - cx) / (rect.width / 2);
      const dy = (e.clientY - cy) / (rect.height / 2);

      const moveX = Math.max(-radius, Math.min(radius, dx * radius * strength));
      const moveY = Math.max(-radius, Math.min(radius, dy * radius * strength));
      el.style.transform = `translate3d(${moveX}px, ${moveY}px, 0)`;
    };

    const onLeave = () => {
      el.style.transform = "translate3d(0,0,0)";
    };

    el.addEventListener("mousemove", onMove);
    el.addEventListener("mouseleave", onLeave);
    return () => {
      el.removeEventListener("mousemove", onMove);
      el.removeEventListener("mouseleave", onLeave);
    };
  }, [strength, radius]);

  return ref;
}
