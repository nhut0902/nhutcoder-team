"use client";

import { useMemo } from "react";
import { motion } from "framer-motion";
import { ArrowLeft, Clock, Tag } from "lucide-react";
import Link from "next/link";
import type { BlogPost } from "@/lib/blog-data";
import { PageTransition } from "@/components/page-transition";
import { ScrollReveal } from "@/components/scroll-reveal";

export function BlogPostClient({ post, related }: { post: BlogPost; related: BlogPost[] }) {
  const headings = useMemo(() => {
    return post.content.match(/^#{2,3}\s+.+$/gm)?.map(h => {
      const match = h.match(/^#+/);
      return {
        level: match ? match[0].length : 2,
        text: h.replace(/^#+\s+/, ""),
      };
    }) || [];
  }, [post.content]);

  const renderContent = (content: string) => {
    return content.split("\n").map((line, i) => {
      if (line.startsWith("# ")) return <h1 key={i} className="text-3xl font-bold mt-8 mb-4">{line.slice(2)}</h1>;
      if (line.startsWith("## ")) return <h2 key={i} className="text-2xl font-bold mt-8 mb-4" id={line.slice(3).toLowerCase().replace(/\s+/g, "-")}>{line.slice(3)}</h2>;
      if (line.startsWith("### ")) return <h3 key={i} className="text-xl font-semibold mt-6 mb-3">{line.slice(4)}</h3>;
      if (line.startsWith("- ")) return <li key={i} className="ml-6 text-[var(--text-muted)] list-disc">{line.slice(2)}</li>;
      if (line.startsWith("```")) return null;
      if (line.trim() === "") return <div key={i} className="h-4" />;
      return <p key={i} className="text-[var(--text-muted)] leading-relaxed mb-4">{line}</p>;
    });
  };

  return (
    <PageTransition>
      <div className="min-h-screen pt-24 pb-20 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto">
        <Link href="/blog" className="inline-flex items-center gap-2 text-sm text-[var(--text-muted)] hover:text-[var(--text)] mb-8 transition-colors">
          <ArrowLeft className="w-4 h-4" /> Back to Blog
        </Link>

        <ScrollReveal>
          <div className="flex items-center gap-3 mb-4 text-sm text-[var(--text-muted)]">
            <span className="px-2 py-0.5 rounded-md bg-[var(--surface)]">{post.category}</span>
            <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {post.readingTime} min read</span>
            <span>{post.date}</span>
          </div>
          <h1 className="text-4xl font-bold mb-4">{post.title}</h1>
          <p className="text-lg text-[var(--text-muted)] mb-8">{post.excerpt}</p>
        </ScrollReveal>

        {headings.length > 0 && (
          <div className="mb-8 p-4 bg-[var(--surface)] border border-[var(--border)] rounded-xl">
            <h3 className="text-sm font-semibold mb-2 text-[var(--text-muted)]">Table of Contents</h3>
            <ul className="space-y-1">
              {headings.map((h, i) => (
                <li key={i} className={`text-sm ${h.level === 2 ? "" : "ml-4"}`}>
                  <a href={`#${h.text.toLowerCase().replace(/\s+/g, "-")}`} className="text-[var(--text-muted)] hover:text-[var(--accent)] transition-colors">
                    {h.text}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}

        <article className="prose prose-invert max-w-none">
          {renderContent(post.content)}
        </article>

        <div className="flex flex-wrap gap-2 mt-8 pt-8 border-t border-[var(--border)]">
          {post.tags.map(tag => (
            <span key={tag} className="inline-flex items-center gap-1 px-3 py-1 text-xs rounded-lg bg-[var(--surface)] border border-[var(--border)]">
              <Tag className="w-3 h-3" /> {tag}
            </span>
          ))}
        </div>

        {related.length > 0 && (
          <div className="mt-12">
            <h3 className="text-xl font-bold mb-4">Related Posts</h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {related.map(r => (
                <Link key={r.slug} href={`/blog/${r.slug}`}
                  className="block p-4 bg-[var(--surface)] border border-[var(--border)] rounded-xl hover:border-[var(--accent)] transition-colors">
                  <h4 className="font-medium text-sm mb-1">{r.title}</h4>
                  <p className="text-xs text-[var(--text-muted)] line-clamp-2">{r.excerpt}</p>
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </PageTransition>
  );
}
