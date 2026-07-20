"use client";

import { useEffect, useState } from "react";

interface MousePosition {
  x: number;
  y: number;
  /** Normalised to viewport — range -1..1, useful for parallax */
  nx: number;
  ny: number;
}

const initial: MousePosition = { x: 0, y: 0, nx: 0, ny: 0 };

/**
 * Tracks the global mouse position. Returns absolute pixels and a
 * -1..1 normalised vector centred on the viewport.
 *
 * Disabled on touch / small screens to save battery.
 */
export function useMousePosition(): MousePosition {
  const [position, setPosition] = useState<MousePosition>(initial);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const isTouch = window.matchMedia("(hover: none)").matches;
    if (isTouch) return;

    let raf = 0;
    const onMove = (e: MouseEvent) => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const { innerWidth: w, innerHeight: h } = window;
        setPosition({
          x: e.clientX,
          y: e.clientY,
          nx: (e.clientX / w) * 2 - 1,
          ny: (e.clientY / h) * 2 - 1,
        });
      });
    };

    window.addEventListener("mousemove", onMove, { passive: true });
    return () => {
      window.removeEventListener("mousemove", onMove);
      cancelAnimationFrame(raf);
    };
  }, []);

  return position;
}
