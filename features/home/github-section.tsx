"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import {
  ArrowUpRight,
  GitBranch,
  GitCommitVertical,
  Star,
  Users,
} from "lucide-react";
import { SectionHeading } from "@/components/section-heading";
import { SITE } from "@/lib/data";
import { Button } from "@marmoui/ui";

/**
 * GitHubSection — a soft "open source by the numbers" section.
 * Pulls from lib/data stats. We avoid live fetches to keep this
 * server-component friendly and resilient to rate limits.
 */
export function GitHubSection() {
  const repos = [
    {
      name: "nebula-cli",
      stars: "3.4k",
      lang: "TypeScript",
      langColor: "oklch(0.7 0.18 250)",
    },
    {
      name: "atlas-ui",
      stars: "1.1k",
      lang: "TypeScript",
      langColor: "oklch(0.7 0.18 250)",
    },
    {
      name: "pulse-rag",
      stars: "820",
      lang: "Rust",
      langColor: "oklch(0.7 0.18 50)",
    },
    {
      name: "ember-engine",
      stars: "1.0k",
      lang: "TypeScript",
      langColor: "oklch(0.7 0.18 250)",
    },
  ];

  return (
    <section className="relative overflow-hidden py-24 md:py-32">
      {/* Background flourish */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 -z-10 bg-dot-faint opacity-40 [mask-image:radial-gradient(ellipse_at_top,black,transparent_70%)]"
      />

      <div className="container-editorial">
        <div className="grid gap-12 lg:grid-cols-12 lg:gap-16">
          {/* Left — narrative */}
          <div className="lg:col-span-5">
            <SectionHeading
              eyebrow="Open Source"
              title={
                <>
                  We default to open.{" "}
                  <span className="text-[var(--color-ink-faint)]">
                    Always have.
                  </span>
                </>
              }
              description="Most of what we build is on GitHub under permissive licenses. We believe in shipping the whole picture — code, decisions, and trade-offs."
            />

            <div className="mt-8 flex flex-wrap items-center gap-3">
              <Link
                href={SITE.github}
                target="_blank"
                rel="noreferrer noopener"
              >
                <Button
                  variant="primary"
                  size="md"
                  rightIcon={<ArrowUpRight className="h-4 w-4" />}
                >
                  Follow on GitHub
                </Button>
              </Link>
              <div className="font-mono text-sm text-[var(--color-ink-faint)]">
                {SITE.github.replace("https://", "")}
              </div>
            </div>

            {/* Stat row */}
            <div className="mt-10 grid grid-cols-3 gap-4">
              <Stat
                icon={<Star className="h-4 w-4" />}
                value="5.4k+"
                label="Stars"
              />
              <Stat
                icon={<GitCommitVertical className="h-4 w-4" />}
                value="1.2k+"
                label="Commits / yr"
              />
              <Stat
                icon={<Users className="h-4 w-4" />}
                value="48"
                label="Contributors"
              />
            </div>
          </div>

          {/* Right — repo list */}
          <div className="lg:col-span-7">
            <div className="overflow-hidden rounded-2xl border border-[var(--color-edge)] bg-[var(--color-panel)]">
              <div className="flex items-center justify-between border-b border-[var(--color-edge)] px-5 py-3">
                <div className="flex items-center gap-2 text-sm text-[var(--color-ink-soft)]">
                  <GitBranch className="h-4 w-4 text-[var(--color-brand-400)]" />
                  <span className="font-mono text-xs">pinned repositories</span>
                </div>
                <span className="font-mono text-[11px] text-[var(--color-ink-faint)]">
                  main
                </span>
              </div>
              <ul className="divide-y divide-[var(--color-edge)]">
                {repos.map((r, i) => (
                  <motion.li
                    key={r.name}
                    initial={{ opacity: 0, y: 8 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.4, delay: i * 0.05 }}
                  >
                    <Link
                      href={`${SITE.github}/${r.name}`}
                      target="_blank"
                      rel="noreferrer noopener"
                      className="group flex items-center justify-between gap-4 px-5 py-4 transition-colors hover:bg-[var(--color-surface-2)]"
                    >
                      <div className="flex min-w-0 items-center gap-3">
                        <span className="grid h-9 w-9 shrink-0 place-items-center rounded-lg border border-[var(--color-edge)] bg-[var(--color-surface-2)] text-[var(--color-ink-soft)] transition-colors group-hover:border-[var(--color-brand-500)] group-hover:text-[var(--color-brand-400)]">
                          <GitBranch className="h-4 w-4" />
                        </span>
                        <div className="min-w-0">
                          <p className="truncate font-mono text-sm text-[var(--color-ink-strong)]">
                            {r.name}
                          </p>
                          <p className="mt-0.5 flex items-center gap-1.5 text-xs text-[var(--color-ink-faint)]">
                            <span
                              className="h-2 w-2 rounded-full"
                              style={{ background: r.langColor }}
                            />
                            {r.lang}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2 text-xs text-[var(--color-ink-soft)]">
                        <Star className="h-3.5 w-3.5 text-[var(--color-ink-faint)]" />
                        <span className="font-mono">{r.stars}</span>
                        <ArrowUpRight className="ml-1 h-3.5 w-3.5 opacity-0 transition-opacity group-hover:opacity-100" />
                      </div>
                    </Link>
                  </motion.li>
                ))}
              </ul>
            </div>

            {/* Contribution graph strip — decorative */}
            <div className="mt-4 overflow-hidden rounded-2xl border border-[var(--color-edge)] bg-[var(--color-panel)] p-5">
              <div className="mb-3 flex items-center justify-between">
                <span className="font-mono text-xs text-[var(--color-ink-faint)]">
                  contribution activity · last 12 weeks
                </span>
                <span className="text-xs text-[var(--color-ink-faint)]">
                  847 commits
                </span>
              </div>
              <div className="grid grid-cols-[repeat(24,minmax(0,1fr))] gap-1 sm:grid-cols-[repeat(36,minmax(0,1fr))] md:grid-cols-[repeat(48,minmax(0,1fr))]">
                {Array.from({ length: 48 }).map((_, i) => {
                  // Pseudo-random but stable pattern
                  const v = (Math.sin(i * 1.7) + Math.cos(i * 0.9) + 2) / 4;
                  const opacity = 0.08 + v * 0.55;
                  return (
                    <motion.span
                      key={i}
                      initial={{ opacity: 0, scale: 0.5 }}
                      whileInView={{ opacity, scale: 1 }}
                      viewport={{ once: true }}
                      transition={{ duration: 0.4, delay: i * 0.005 }}
                      className="block aspect-square rounded-[3px] bg-[var(--color-brand-400)]"
                    />
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function Stat({
  icon,
  value,
  label,
}: {
  icon: React.ReactNode;
  value: string;
  label: string;
}) {
  return (
    <div className="rounded-xl border border-[var(--color-edge)] bg-[var(--color-panel)] p-4">
      <div className="flex items-center gap-2 text-[var(--color-brand-400)]">
        {icon}
      </div>
      <p className="mt-2 font-display text-2xl font-semibold text-[var(--color-ink-strong)]">
        {value}
      </p>
      <p className="text-[11px] uppercase tracking-wide text-[var(--color-ink-faint)]">
        {label}
      </p>
    </div>
  );
}
