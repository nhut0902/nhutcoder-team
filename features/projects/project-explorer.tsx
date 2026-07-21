"use client";

import { useMemo, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Search } from "lucide-react";
import type { Project } from "@/types";
import { Input } from "@marmoui/ui";
import { ProjectCard } from "./project-card";
import { cn } from "@/lib/utils";

interface ProjectExplorerProps {
  projects: Project[];
  categories: { id: string; label: string; count: number }[];
}

export function ProjectExplorer({
  projects,
  categories,
}: ProjectExplorerProps) {
  const [active, setActive] = useState<string>("all");
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    return projects.filter((p) => {
      const matchesCat = active === "all" || p.category === active;
      const q = query.trim().toLowerCase();
      const matchesQuery =
        !q ||
        p.name.toLowerCase().includes(q) ||
        p.tagline.toLowerCase().includes(q) ||
        p.tags.some((t) => t.toLowerCase().includes(q)) ||
        p.stack.some((t) => t.toLowerCase().includes(q));
      return matchesCat && matchesQuery;
    });
  }, [projects, active, query]);

  return (
    <div>
      {/* Controls */}
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex flex-wrap gap-1.5">
          {categories.map((cat) => (
            <button
              key={cat.id}
              type="button"
              onClick={() => setActive(cat.id)}
              className={cn(
                "relative rounded-full border px-3.5 py-1.5 text-sm font-medium transition-colors",
                active === cat.id
                  ? "border-[var(--color-brand-500)] bg-[var(--color-brand-500)]/10 text-[var(--color-brand-300)]"
                  : "border-[var(--color-edge)] bg-[var(--color-panel)] text-[var(--color-ink-soft)] hover:border-[var(--color-border-hover)] hover:text-[var(--color-ink-strong)]"
              )}
            >
              {cat.label}
              <span className="ml-1.5 font-mono text-[10px] opacity-60">
                {cat.count}
              </span>
            </button>
          ))}
        </div>

        <div className="relative w-full max-w-xs">
          <Input
            value={query}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setQuery(e.target.value)
            }
            placeholder="Search projects, tags, stack…"
            className="pl-9"
            aria-label="Search projects"
          />
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--color-ink-faint)]" />
        </div>
      </div>

      {/* Result count */}
      <div className="mt-6 flex items-center justify-between border-b border-[var(--color-edge)] pb-3 text-xs text-[var(--color-ink-faint)]">
        <span className="font-mono">
          Showing {filtered.length} of {projects.length}
        </span>
        <span className="font-mono">sorted by recency</span>
      </div>

      {/* Grid */}
      <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <AnimatePresence mode="popLayout">
          {filtered.map((p, i) => (
            <motion.div
              key={p.slug}
              layout
              initial={{ opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.96 }}
              transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
              className="h-full"
            >
              <ProjectCard project={p} index={i} />
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {filtered.length === 0 && (
        <div className="mt-16 flex flex-col items-center justify-center rounded-2xl border border-dashed border-[var(--color-edge-strong)] py-20 text-center">
          <p className="font-display text-2xl font-semibold text-[var(--color-ink-strong)]">
            No projects found
          </p>
          <p className="mt-2 text-sm text-[var(--color-ink-faint)]">
            Try a different search term or category.
          </p>
          <button
            type="button"
            onClick={() => {
              setActive("all");
              setQuery("");
            }}
            className="mt-5 rounded-full border border-[var(--color-edge)] bg-[var(--color-panel)] px-4 py-2 text-sm font-medium text-[var(--color-ink-soft)] transition-colors hover:text-[var(--color-ink-strong)]"
          >
            Reset filters
          </button>
        </div>
      )}
    </div>
  );
}
