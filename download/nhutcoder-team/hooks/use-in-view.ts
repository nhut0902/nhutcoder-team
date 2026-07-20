"use client";

import { useEffect, useRef, useState } from "react";

/**
 * useInView — lightweight wrapper around IntersectionObserver.
 * Returns a ref to attach + a boolean for whether the element has entered.
 */
export function useInView<T extends Element = HTMLDivElement>(
  options: IntersectionObserverInit = {
    threshold: 0.2,
    rootMargin: "0px 0px -10% 0px",
  }
) {
  const ref = useRef<T | null>(null);
  const [inView, setInView] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    // SSR / no IO support: just show.
    if (typeof IntersectionObserver === "undefined") {
      setInView(true);
      return;
    }

    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        setInView(true);
        observer.disconnect();
      }
    }, options);

    observer.observe(el);
    return () => observer.disconnect();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return { ref, inView } as const;
}
