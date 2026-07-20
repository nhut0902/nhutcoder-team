"use client";

import { motion } from "framer-motion";
import { useRef } from "react";
import { useScroll, useTransform } from "framer-motion";
import { SectionHeading } from "@/components/section-heading";
import { TIMELINE } from "@/lib/data";

/**
 * Timeline — vertical narrative timeline with scroll-driven progress line.
 * Inspired by editorial long-reads (Stripe Press / Linear changelog).
 */
export function Timeline() {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start 70%", "end 60%"],
  });
  const lineHeight = useTransform(scrollYProgress, [0, 1], ["0%", "100%"]);

  return (
    <section className="relative py-24 md:py-32">
      <div className="container-editorial">
        <SectionHeading
          eyebrow="The Path So Far"
          title={
            <>
              Seven years of shipping,{" "}
              <span className="text-[var(--color-ink-faint)]">
                one commit at a time.
              </span>
            </>
          }
          description="From a single GitHub account publishing tutorials to a four-person collective shipping AI infrastructure — here's the path that brought us here."
        />

        <div ref={ref} className="relative mt-16 pl-6 md:pl-10">
          {/* Spine */}
          <div className="absolute left-0 top-0 h-full w-px bg-[var(--color-edge)]" />
          <motion.div
            style={{ height: lineHeight }}
            className="absolute left-0 top-0 w-px bg-gradient-to-b from-[var(--color-brand-400)] via-[var(--color-accent-400)] to-transparent"
          />

          <ul className="space-y-12 md:space-y-16">
            {TIMELINE.map((entry, i) => (
              <motion.li
                key={`${entry.year}-${entry.title}`}
                initial={{ opacity: 0, x: -16 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true, margin: "-15% 0px" }}
                transition={{
                  duration: 0.6,
                  delay: i * 0.04,
                  ease: [0.22, 1, 0.36, 1],
                }}
                className="relative"
              >
                {/* Node */}
                <span className="absolute -left-[1.65rem] top-1.5 grid h-3 w-3 place-items-center md:-left-[2.65rem]">
                  <span className="absolute h-full w-full rounded-full bg-[var(--color-brand-500)] opacity-40 blur-[2px]" />
                  <span className="relative h-2 w-2 rounded-full bg-[var(--color-brand-400)] ring-4 ring-[var(--color-bg)]" />
                </span>

                <div className="grid gap-2 md:grid-cols-12 md:gap-6">
                  <div className="md:col-span-3">
                    <p className="font-mono text-sm text-[var(--color-brand-400)]">
                      {entry.year}
                    </p>
                    <p className="mt-1 inline-flex rounded-full border border-[var(--color-edge)] bg-[var(--color-surface-2)] px-2.5 py-0.5 text-[11px] uppercase tracking-wider text-[var(--color-ink-faint)]">
                      {entry.tag}
                    </p>
                  </div>
                  <div className="md:col-span-9">
                    <h3 className="text-xl font-semibold tracking-tight text-[var(--color-ink-strong)] md:text-2xl">
                      {entry.title}
                    </h3>
                    <p className="mt-2 max-w-2xl text-[15px] leading-relaxed text-[var(--color-ink-soft)]">
                      {entry.description}
                    </p>
                  </div>
                </div>
              </motion.li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
