"use client";

import { useState, useMemo } from "react";
import { Search, PenTool } from "lucide-react";
import { BLOG_POSTS, BLOG_CATEGORIES } from "@/lib/blog-data";
import { PageTransition } from "@/components/page-transition";
import { ScrollReveal } from "@/components/scroll-reveal";
import Link from "next/link";

export default function BlogPage() {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("Tất cả");

  const filtered = useMemo(() => {
    let result = BLOG_POSTS;
    if (category !== "Tất cả") result = result.filter(p => p.category === category);
    if (search) {
      const q = search.toLowerCase();
      result = result.filter(p =>
        p.title.toLowerCase().includes(q) ||
        p.excerpt.toLowerCase().includes(q) ||
        p.tags.some(t => t.toLowerCase().includes(q))
      );
    }
    return result;
  }, [search, category]);

  return (
    <PageTransition>
      <div className="min-h-screen pt-24 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <ScrollReveal>
          <div className="text-center mb-12">
            <h1 className="text-4xl sm:text-5xl font-bold tracking-tight">
              <span className="text-[var(--accent)]">Blog</span>
            </h1>
            <p className="mt-4 text-lg text-[var(--text-muted)] max-w-2xl mx-auto">
              Chia sẻ kiến thức, hướng dẫn và kinh nghiệm phát triển phần mềm.
            </p>
          </div>
        </ScrollReveal>

        {BLOG_POSTS.length > 0 ? (
          <>
            <div className="flex flex-col sm:flex-row gap-4 mb-8">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--text-muted)]" />
                <input
                  type="text"
                  placeholder="Tìm bài viết..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 bg-[var(--surface)] border border-[var(--border)] rounded-lg text-sm focus:outline-none focus:border-[var(--accent)] transition-colors"
                />
              </div>
              <div className="flex gap-2 overflow-x-auto pb-1">
                {BLOG_CATEGORIES.map(cat => (
                  <button
                    key={cat}
                    onClick={() => setCategory(cat)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-all ${
                      category === cat
                        ? "bg-[var(--accent)] text-[var(--bg)]"
                        : "bg-[var(--surface)] text-[var(--text-muted)] hover:text-[var(--text)]"
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {filtered.map((post, i) => (
                <ScrollReveal key={post.slug} delay={i * 0.05}>
                  <Link href={`/blog/${post.slug}`}
                    className="group block bg-[var(--surface)] border border-[var(--border)] rounded-2xl p-5 hover:border-[var(--accent)] transition-colors">
                    <span className="text-xs px-2 py-0.5 rounded-md bg-[var(--bg)] text-[var(--text-muted)] mb-2 inline-block">{post.category}</span>
                    <h3 className="font-semibold text-lg mb-2 group-hover:text-[var(--accent)] transition-colors">{post.title}</h3>
                    <p className="text-sm text-[var(--text-muted)] line-clamp-2 mb-3">{post.excerpt}</p>
                    <div className="text-xs text-[var(--text-muted)]">{post.date} · {post.readingTime} phút đọc</div>
                  </Link>
                </ScrollReveal>
              ))}
            </div>
          </>
        ) : (
          <div className="text-center py-20">
            <PenTool className="w-12 h-12 text-[var(--text-muted)] mx-auto mb-4" />
            <p className="text-lg text-[var(--text-muted)] mb-2">Chưa có bài viết nào</p>
            <p className="text-sm text-[var(--text-muted)]">Bài viết sẽ được đăng sớm. Quay lại sau nhé!</p>
          </div>
        )}
      </div>
    </PageTransition>
  );
}
