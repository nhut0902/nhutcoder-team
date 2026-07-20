"use client";

import { motion } from "framer-motion";
import { MapPin } from "lucide-react";
import { SectionHeading } from "@/components/section-heading";
import { EXPERIENCE } from "@/lib/data";

/**
 * Experience — editorial resume-style section.
 * Each role uses a card with hover state + a stack chip row.
 */
export function Experience() {
  return (
    <section className="relative py-24 md:py-32">
      <div className="container-editorial">
        <SectionHeading
          eyebrow="Experience"
          title={
            <>
              Where we&apos;ve been{" "}
              <span className="text-[var(--color-ink-faint)]">building.</span>
            </>
          }
          description="A condensed history of the work that shaped how we ship today."
        />

        <div className="mt-14 space-y-4">
          {EXPERIENCE.map((exp, i) => (
            <motion.article
              key={`${exp.company}-${exp.role}`}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-10% 0px" }}
              transition={{
                duration: 0.6,
                delay: i * 0.06,
                ease: [0.22, 1, 0.36, 1],
              }}
              className="group relative overflow-hidden rounded-3xl border border-[var(--color-edge)] bg-[var(--color-panel)] p-6 transition-colors duration-500 hover:border-[var(--color-edge-strong)] md:p-8"
            >
              {/* Hover gradient strip */}
              <div
                aria-hidden="true"
                className="pointer-events-none absolute inset-y-0 left-0 w-px bg-gradient-to-b from-transparent via-[var(--color-brand-500)] to-transparent opacity-0 transition-opacity duration-500 group-hover:opacity-100"
              />

              <div className="grid gap-6 md:grid-cols-12 md:gap-8">
                {/* Left: role + company */}
                <div className="md:col-span-5">
                  <div className="flex items-center gap-2 text-xs text-[var(--color-ink-faint)]">
                    <span className="font-mono">{exp.period}</span>
                    <span className="h-1 w-1 rounded-full bg-[var(--color-ink-faint)]" />
                    <span className="inline-flex items-center gap-1">
                      <MapPin className="h-3 w-3" />
                      {exp.location}
                    </span>
                  </div>
                  <h3 className="mt-3 text-xl font-semibold tracking-tight text-[var(--color-ink-strong)] md:text-2xl">
                    {exp.role}
                  </h3>
                  <p className="mt-1 text-[var(--color-brand-400)]">
                    {exp.company}
                  </p>
                </div>

                {/* Right: summary + highlights */}
                <div className="md:col-span-7">
                  <p className="text-[15px] leading-relaxed text-[var(--color-ink-soft)]">
                    {exp.summary}
                  </p>
                  <ul className="mt-4 space-y-2">
                    {exp.highlights.map((h) => (
                      <li
                        key={h}
                        className="flex gap-2.5 text-sm leading-relaxed text-[var(--color-ink-soft)]"
                      >
                        <span
                          aria-hidden="true"
                          className="mt-[7px] h-1 w-1 shrink-0 rounded-full bg-[var(--color-brand-500)]"
                        />
                        <span>{h}</span>
                      </li>
                    ))}
                  </ul>
                  <div className="mt-5 flex flex-wrap gap-1.5">
                    {exp.stack.map((s) => (
                      <span
                        key={s}
                        className="rounded-md border border-[var(--color-edge)] bg-[var(--color-surface-2)] px-2 py-0.5 font-mono text-[11px] text-[var(--color-ink-faint)]"
                      >
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}
