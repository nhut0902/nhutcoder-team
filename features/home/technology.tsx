"use client";

import { motion } from "framer-motion";
import { SectionHeading } from "@/components/section-heading";
import { TECH_STACK } from "@/lib/data";

/**
 * Technology — a marquee-driven "stack we use" section.
 * Includes a tabular grid on the right + an infinite marquee on the left.
 */
export function Technology() {
  // Duplicate for seamless marquee loop
  const marqueeItems = [...TECH_STACK, ...TECH_STACK];

  return (
    <section className="relative overflow-hidden border-y border-[var(--color-edge)] bg-[var(--color-surface-0)] py-24 md:py-32">
      {/* Background grid */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 bg-grid-faint opacity-50 [mask-image:radial-gradient(ellipse_at_center,black,transparent_75%)]"
      />

      <div className="container-editorial relative">
        <SectionHeading
          eyebrow="The Stack"
          title={
            <>
              Boring tech, sharp tools,{" "}
              <span className="text-[var(--color-ink-faint)]">
                opinionated defaults.
              </span>
            </>
          }
          description="We pick technologies that compound — fast to write today, easy to maintain five years from now. Here's what's currently in heavy rotation."
        />

        <div className="mt-12 grid gap-8 lg:grid-cols-12">
          {/* Marquee column */}
          <div className="lg:col-span-7">
            <div className="relative -mx-6 overflow-hidden mask-fade-x">
              <div className="marquee-track py-3">
                {marqueeItems.map((tech, i) => (
                  <div
                    key={`${tech.name}-${i}`}
                    className="flex items-center gap-3 whitespace-nowrap"
                  >
                    <span className="h-1.5 w-1.5 rounded-full bg-[var(--color-brand-500)]" />
                    <span className="font-display text-2xl font-medium text-[var(--color-ink-soft)] md:text-3xl">
                      {tech.name}
                    </span>
                    <span className="font-mono text-xs uppercase tracking-wider text-[var(--color-ink-faint)]">
                      {tech.category}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Second marquee — opposite direction, smaller */}
            <div className="relative -mx-6 mt-2 overflow-hidden mask-fade-x">
              <div
                className="marquee-track py-3"
                style={{
                  animationDirection: "reverse",
                  animationDuration: "55s",
                }}
              >
                {[...marqueeItems].reverse().map((tech, i) => (
                  <div
                    key={`${tech.name}-rev-${i}`}
                    className="flex items-center gap-3 whitespace-nowrap opacity-50"
                  >
                    <span className="font-mono text-xs text-[var(--color-ink-faint)]">
                      ↳
                    </span>
                    <span className="font-display text-xl font-medium text-[var(--color-ink-soft)]">
                      {tech.name}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right column — categorised list */}
          <div className="lg:col-span-5">
            <div className="grid grid-cols-2 gap-px overflow-hidden rounded-2xl border border-[var(--color-edge)] bg-[var(--color-edge)]">
              {Object.entries(groupByCategory(TECH_STACK))
                .slice(0, 8)
                .map(([cat, items], i) => (
                  <motion.div
                    key={cat}
                    initial={{ opacity: 0, y: 12 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5, delay: i * 0.05 }}
                    className="bg-[var(--color-panel)] p-4"
                  >
                    <p className="label-mono mb-2 text-[var(--color-brand-400)]">
                      {cat}
                    </p>
                    <ul className="space-y-1">
                      {items.slice(0, 4).map((t) => (
                        <li
                          key={t.name}
                          className="text-sm text-[var(--color-ink-soft)]"
                        >
                          {t.name}
                        </li>
                      ))}
                    </ul>
                  </motion.div>
                ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function groupByCategory(items: typeof TECH_STACK) {
  return items.reduce<Record<string, typeof TECH_STACK>>((acc, item) => {
    (acc[item.category] = acc[item.category] || []).push(item);
    return acc;
  }, {});
}
