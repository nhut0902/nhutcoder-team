"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowUpRight, Clock } from "lucide-react";
import type { BlogPost } from "@/types";
import { formatDate } from "@/lib/utils";
import { cn } from "@/lib/utils";

interface BlogCardProps {
  post: BlogPost;
  index?: number;
  featured?: boolean;
}

export function BlogCard({ post, index = 0, featured = false }: BlogCardProps) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.55,
        delay: Math.min(index * 0.06, 0.36),
        ease: [0.22, 1, 0.36, 1],
      }}
      className={cn(
        "group relative h-full overflow-hidden rounded-2xl border border-[var(--color-edge)] bg-[var(--color-panel)] transition-all duration-500 hover:border-[var(--color-edge-strong)]",
        featured && "md:col-span-2 md:row-span-2"
      )}
    >
      <Link
        href={`/blog/${post.slug}`}
        className="flex h-full flex-col p-6 md:p-8"
      >
        {/* Meta */}
        <div className="flex items-center gap-2 text-xs text-[var(--color-ink-faint)]">
          <span className="rounded-md border border-[var(--color-edge)] bg-[var(--color-surface-2)] px-2 py-0.5 font-mono uppercase tracking-wide text-[var(--color-brand-400)]">
            {post.category}
          </span>
          <span className="font-mono">{formatDate(post.date)}</span>
          <span className="h-1 w-1 rounded-full bg-[var(--color-ink-faint)]" />
          <span className="inline-flex items-center gap-1 font-mono">
            <Clock className="h-3 w-3" />
            {post.readingMinutes} min
          </span>
        </div>

        {/* Title */}
        <h3
          className={cn(
            "mt-4 font-semibold tracking-tight text-[var(--color-ink-strong)] transition-colors group-hover:text-[var(--color-brand-300)]",
            featured ? "text-2xl md:text-3xl" : "text-xl"
          )}
        >
          {post.title}
        </h3>

        {/* Excerpt */}
        <p
          className={cn(
            "mt-3 text-[var(--color-ink-soft)]",
            featured ? "text-base leading-relaxed" : "text-sm leading-relaxed"
          )}
        >
          {post.excerpt}
        </p>

        {/* Footer */}
        <div className="mt-auto flex items-center justify-between gap-3 pt-6">
          <div className="flex items-center gap-2">
            <span className="grid h-7 w-7 place-items-center rounded-full bg-gradient-to-br from-[var(--color-brand-500)] to-[var(--color-accent-500)] text-[10px] font-semibold text-[var(--color-primary-contrast)]">
              {post.author
                .split(" ")
                .map((n) => n[0])
                .join("")
                .slice(0, 2)}
            </span>
            <span className="text-xs text-[var(--color-ink-soft)]">
              {post.author}
            </span>
          </div>
          <span className="grid h-7 w-7 place-items-center rounded-full border border-[var(--color-edge)] text-[var(--color-ink-soft)] transition-all duration-500 group-hover:border-[var(--color-brand-500)] group-hover:text-[var(--color-brand-400)] group-hover:rotate-12">
            <ArrowUpRight className="h-3.5 w-3.5" />
          </span>
        </div>

        {/* Tags */}
        <div className="mt-4 flex flex-wrap gap-1.5">
          {post.tags.map((t) => (
            <span
              key={t}
              className="rounded-md border border-[var(--color-edge)] bg-[var(--color-surface-2)] px-2 py-0.5 font-mono text-[10px] text-[var(--color-ink-faint)]"
            >
              {t}
            </span>
          ))}
        </div>
      </Link>
    </motion.article>
  );
}
