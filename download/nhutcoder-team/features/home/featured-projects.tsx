"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowUpRight, GitBranch } from "lucide-react";
import type { Project } from "@/types";
import { cn } from "@/lib/utils";
import { SectionHeading } from "@/components/section-heading";
import { ScrollReveal } from "@/components/scroll-reveal";
import { Button, Badge } from "@marmoui/ui";

interface FeaturedProjectsProps {
  projects: Project[];
}

const accentMap: Record<
  Project["accent"],
  { ring: string; chip: string; glow: string; text: string }
> = {
  lime: {
    ring: "group-hover:border-[var(--color-brand-500)]/60",
    chip: "bg-[var(--color-brand-500)]/10 text-[var(--color-brand-300)] border-[var(--color-brand-500)]/20",
    glow: "from-[var(--color-brand-500)]/20",
    text: "text-[var(--color-brand-300)]",
  },
  violet: {
    ring: "group-hover:border-[var(--color-accent-500)]/60",
    chip: "bg-[var(--color-accent-500)]/10 text-[var(--color-accent-300)] border-[var(--color-accent-500)]/20",
    glow: "from-[var(--color-accent-500)]/20",
    text: "text-[var(--color-accent-300)]",
  },
  cyan: {
    ring: "group-hover:border-[oklch(0.7_0.18_200_/_0.6)]",
    chip: "bg-[oklch(0.7_0.18_200_/_0.1)] text-[oklch(0.8_0.15_200)] border-[oklch(0.7_0.18_200_/_0.2)]",
    glow: "from-[oklch(0.7_0.18_200_/_0.2)]",
    text: "text-[oklch(0.8_0.15_200)]",
  },
  amber: {
    ring: "group-hover:border-[oklch(0.78_0.16_95_/_0.6)]",
    chip: "bg-[oklch(0.78_0.16_95_/_0.1)] text-[oklch(0.85_0.14_95)] border-[oklch(0.78_0.16_95_/_0.2)]",
    glow: "from-[oklch(0.78_0.16_95_/_0.2)]",
    text: "text-[oklch(0.85_0.14_95)]",
  },
  rose: {
    ring: "group-hover:border-[oklch(0.7_0.2_15_/_0.6)]",
    chip: "bg-[oklch(0.7_0.2_15_/_0.1)] text-[oklch(0.82_0.16_15)] border-[oklch(0.7_0.2_15_/_0.2)]",
    glow: "from-[oklch(0.7_0.2_15_/_0.2)]",
    text: "text-[oklch(0.82_0.16_15)]",
  },
};

export function FeaturedProjects({ projects }: FeaturedProjectsProps) {
  const [featured, ...rest] = projects;
  const secondary = rest.slice(0, 3);

  return (
    <section className="relative py-24 md:py-32">
      <div className="container-editorial">
        <div className="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
          <SectionHeading
            eyebrow="Selected Work"
            title={
              <>
                Projects we&apos;ve{" "}
                <span className="text-[var(--color-ink-faint)]">
                  shipped, broken, and rebuilt.
                </span>
              </>
            }
            description="A small slice of what the team has been building. Some are open source, some are products, all of them are loved."
          />
          <ScrollReveal delay={0.1}>
            <Link href="/projects">
              <Button
                variant="secondary"
                size="md"
                rightIcon={<ArrowUpRight className="h-4 w-4" />}
              >
                All projects
              </Button>
            </Link>
          </ScrollReveal>
        </div>

        <div className="mt-14 grid gap-6 lg:grid-cols-12">
          {/* Featured (large) */}
          <ScrollReveal className="lg:col-span-7" delay={0}>
            <FeaturedProjectCard project={featured} large />
          </ScrollReveal>

          {/* Secondary column */}
          <div className="grid gap-6 lg:col-span-5">
            {secondary.map((p, i) => (
              <ScrollReveal key={p.slug} delay={0.1 * (i + 1)}>
                <FeaturedProjectCard project={p} />
              </ScrollReveal>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function FeaturedProjectCard({
  project,
  large = false,
}: {
  project: Project;
  large?: boolean;
}) {
  const accent = accentMap[project.accent];

  return (
    <Link
      href={project.demo ?? project.repo ?? "/projects"}
      target={project.demo ? "_blank" : undefined}
      rel={project.demo ? "noreferrer noopener" : undefined}
      className={cn(
        "group relative block h-full overflow-hidden rounded-3xl border border-[var(--color-edge)] bg-[var(--color-panel)] p-6 transition-all duration-500 hover:-translate-y-1 md:p-8",
        accent.ring,
        large && "min-h-[460px] md:min-h-[520px]"
      )}
    >
      {/* Decorative glow */}
      <div
        aria-hidden="true"
        className={cn(
          "pointer-events-none absolute -right-20 -top-20 h-64 w-64 rounded-full bg-gradient-to-b to-transparent opacity-0 blur-3xl transition-opacity duration-700 group-hover:opacity-100",
          accent.glow
        )}
      />

      <div className="relative flex h-full flex-col">
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-center gap-2">
            <span
              className={cn(
                "inline-flex items-center rounded-full border px-2.5 py-1 text-[11px] font-medium",
                accent.chip
              )}
            >
              {project.category}
            </span>
            <span className="font-mono text-xs text-[var(--color-ink-faint)]">
              {project.year}
            </span>
          </div>
          <span className="grid h-9 w-9 place-items-center rounded-full border border-[var(--color-edge)] text-[var(--color-ink-soft)] transition-all duration-500 group-hover:border-[var(--color-brand-500)] group-hover:text-[var(--color-brand-400)] group-hover:rotate-12">
            <ArrowUpRight className="h-4 w-4" />
          </span>
        </div>

        <div className="mt-6">
          <h3
            className={cn(
              "font-semibold tracking-tight text-[var(--color-ink-strong)]",
              large ? "text-3xl md:text-4xl" : "text-2xl"
            )}
          >
            {project.name}
          </h3>
          <p
            className={cn(
              "mt-2 text-[var(--color-ink-soft)]",
              large ? "text-lg" : "text-[15px]"
            )}
          >
            {project.tagline}
          </p>
        </div>

        {large && (
          <p className="mt-4 max-w-xl text-[15px] leading-relaxed text-[var(--color-ink-soft)]">
            {project.description}
          </p>
        )}

        {/* Metrics row */}
        <div
          className={cn(
            "flex flex-wrap gap-x-8 gap-y-3",
            large ? "mt-auto pt-8" : "mt-4"
          )}
        >
          {project.metrics.map((m) => (
            <div key={m.label}>
              <p
                className={cn(
                  "font-display text-xl font-semibold text-[var(--color-ink-strong)]",
                  accent.text
                )}
              >
                {m.value}
              </p>
              <p className="text-[11px] uppercase tracking-wide text-[var(--color-ink-faint)]">
                {m.label}
              </p>
            </div>
          ))}
        </div>

        {/* Stack chips */}
        <div className="mt-5 flex flex-wrap items-center gap-1.5">
          {project.stack.slice(0, large ? 6 : 4).map((s) => (
            <span
              key={s}
              className="rounded-md border border-[var(--color-edge)] bg-[var(--color-surface-2)] px-2 py-0.5 font-mono text-[11px] text-[var(--color-ink-faint)]"
            >
              {s}
            </span>
          ))}
        </div>

        {project.repo && (
          <div className="mt-5 flex items-center gap-1.5 text-xs text-[var(--color-ink-faint)]">
            <GitBranch className="h-3.5 w-3.5" />
            <span className="font-mono">
              {project.repo.replace("https://github.com/", "")}
            </span>
          </div>
        )}
      </div>

      {/* Featured badge */}
      {project.featured && (
        <motion.div
          aria-hidden="true"
          className="absolute right-6 top-6 hidden md:block"
          initial={{ opacity: 0, scale: 0.8 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
        >
          <Badge
            variant="normal"
            size="sm"
            className="border-[var(--color-edge-strong)]"
          >
            Featured
          </Badge>
        </motion.div>
      )}
    </Link>
  );
}
