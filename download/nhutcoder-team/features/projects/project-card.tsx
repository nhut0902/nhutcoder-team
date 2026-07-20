"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowUpRight, GitBranch } from "lucide-react";
import type { Project } from "@/types";
import { cn } from "@/lib/utils";

interface ProjectCardProps {
  project: Project;
  index?: number;
}

const accentTextMap: Record<Project["accent"], string> = {
  lime: "text-[var(--color-brand-300)]",
  violet: "text-[var(--color-accent-300)]",
  cyan: "text-[oklch(0.8_0.15_200)]",
  amber: "text-[oklch(0.85_0.14_95)]",
  rose: "text-[oklch(0.82_0.16_15)]",
};

const accentGlowMap: Record<Project["accent"], string> = {
  lime: "bg-[var(--color-brand-500)]/20",
  violet: "bg-[var(--color-accent-500)]/20",
  cyan: "bg-[oklch(0.7_0.18_200_/_0.2)]",
  amber: "bg-[oklch(0.78_0.16_95_/_0.2)]",
  rose: "bg-[oklch(0.7_0.2_15_/_0.2)]",
};

export function ProjectCard({ project, index = 0 }: ProjectCardProps) {
  const href = project.demo ?? project.repo ?? "/projects";
  const external = Boolean(project.demo ?? project.repo);

  return (
    <motion.article
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.55,
        delay: Math.min(index * 0.06, 0.36),
        ease: [0.22, 1, 0.36, 1],
      }}
      className="group relative h-full"
    >
      <Link
        href={href}
        target={external ? "_blank" : undefined}
        rel={external ? "noreferrer noopener" : undefined}
        className="relative flex h-full flex-col overflow-hidden rounded-2xl border border-[var(--color-edge)] bg-[var(--color-panel)] p-6 transition-all duration-500 hover:-translate-y-1 hover:border-[var(--color-edge-strong)]"
      >
        {/* Hover glow */}
        <div
          aria-hidden="true"
          className={cn(
            "pointer-events-none absolute -right-16 -top-16 h-40 w-40 rounded-full opacity-0 blur-3xl transition-opacity duration-700 group-hover:opacity-100",
            accentGlowMap[project.accent]
          )}
        />

        <div className="relative flex items-start justify-between">
          <div className="flex items-center gap-2">
            <span className="rounded-md border border-[var(--color-edge)] bg-[var(--color-surface-2)] px-2 py-0.5 font-mono text-[11px] uppercase tracking-wide text-[var(--color-ink-faint)]">
              {project.category}
            </span>
            <span className="font-mono text-xs text-[var(--color-ink-faint)]">
              {project.year}
            </span>
          </div>
          <span className="grid h-8 w-8 place-items-center rounded-full border border-[var(--color-edge)] text-[var(--color-ink-soft)] transition-all duration-500 group-hover:border-[var(--color-brand-500)] group-hover:text-[var(--color-brand-400)] group-hover:rotate-12">
            <ArrowUpRight className="h-3.5 w-3.5" />
          </span>
        </div>

        <div className="relative mt-5">
          <h3 className="text-xl font-semibold tracking-tight text-[var(--color-ink-strong)]">
            {project.name}
          </h3>
          <p className="mt-1.5 text-sm text-[var(--color-ink-soft)]">
            {project.tagline}
          </p>
          <p className="mt-3 text-[13.5px] leading-relaxed text-[var(--color-ink-soft)]">
            {project.description}
          </p>
        </div>

        <div className="relative mt-auto flex flex-wrap gap-x-6 gap-y-2 pt-6">
          {project.metrics.slice(0, 2).map((m) => (
            <div key={m.label}>
              <p
                className={cn(
                  "font-display text-base font-semibold",
                  accentTextMap[project.accent]
                )}
              >
                {m.value}
              </p>
              <p className="text-[10px] uppercase tracking-wide text-[var(--color-ink-faint)]">
                {m.label}
              </p>
            </div>
          ))}
        </div>

        <div className="relative mt-4 flex flex-wrap items-center gap-1.5">
          {project.stack.slice(0, 4).map((s) => (
            <span
              key={s}
              className="rounded-md border border-[var(--color-edge)] bg-[var(--color-surface-2)] px-2 py-0.5 font-mono text-[11px] text-[var(--color-ink-faint)]"
            >
              {s}
            </span>
          ))}
        </div>

        {project.repo && (
          <div className="relative mt-4 flex items-center gap-1.5 text-[11px] text-[var(--color-ink-faint)]">
            <GitBranch className="h-3 w-3" />
            <span className="truncate font-mono">
              {project.repo.replace("https://github.com/", "")}
            </span>
          </div>
        )}
      </Link>
    </motion.article>
  );
}
