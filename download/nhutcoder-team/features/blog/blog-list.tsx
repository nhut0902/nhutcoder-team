"use client";

import { useMemo, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import type { BlogPost } from "@/types";
import { BlogCard } from "./blog-card";
import { cn } from "@/lib/utils";

interface BlogListProps {
  posts: BlogPost[];
  categories: readonly string[];
}

export function BlogList({ posts, categories }: BlogListProps) {
  const [active, setActive] = useState<string>("All");

  const filtered = useMemo(() => {
    if (active === "All") return posts;
    return posts.filter((p) => p.category === active);
  }, [posts, active]);

  const [featured, ...rest] = filtered;

  return (
    <div>
      {/* Categories */}
      <div className="flex flex-wrap gap-1.5">
        {categories.map((cat) => (
          <button
            key={cat}
            type="button"
            onClick={() => setActive(cat)}
            className={cn(
              "relative rounded-full border px-3.5 py-1.5 text-sm font-medium transition-colors",
              active === cat
                ? "border-[var(--color-brand-500)] bg-[var(--color-brand-500)]/10 text-[var(--color-brand-300)]"
                : "border-[var(--color-edge)] bg-[var(--color-panel)] text-[var(--color-ink-soft)] hover:border-[var(--color-border-hover)] hover:text-[var(--color-ink-strong)]"
            )}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Result count */}
      <div className="mt-6 flex items-center justify-between border-b border-[var(--color-edge)] pb-3 text-xs text-[var(--color-ink-faint)]">
        <span className="font-mono">
          {filtered.length} {filtered.length === 1 ? "article" : "articles"}
        </span>
        <span className="font-mono">most recent first</span>
      </div>

      {/* Grid */}
      <div className="mt-8 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
        <AnimatePresence mode="popLayout">
          {featured && (
            <motion.div
              key={`featured-${featured.slug}`}
              layout
              initial={{ opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.96 }}
              transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
              className="md:col-span-2 lg:col-span-2 lg:row-span-2"
            >
              <BlogCard post={featured} index={0} featured />
            </motion.div>
          )}
          {rest.map((post, i) => (
            <motion.div
              key={post.slug}
              layout
              initial={{ opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.96 }}
              transition={{
                duration: 0.4,
                delay: Math.min((i + 1) * 0.05, 0.3),
                ease: [0.22, 1, 0.36, 1],
              }}
            >
              <BlogCard post={post} index={i + 1} />
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {filtered.length === 0 && (
        <div className="mt-16 rounded-2xl border border-dashed border-[var(--color-edge-strong)] py-20 text-center">
          <p className="font-display text-xl font-semibold text-[var(--color-ink-strong)]">
            No articles in this category yet
          </p>
          <p className="mt-2 text-sm text-[var(--color-ink-faint)]">
            Check back soon — we publish roughly twice a month.
          </p>
        </div>
      )}
    </div>
  );
}
