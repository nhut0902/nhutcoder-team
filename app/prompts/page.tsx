"use client";

import { useState, useMemo } from "react";
import { motion } from "framer-motion";
import { Search, Copy, Check, Star, Users } from "lucide-react";
import { PROMPTS, PROMPT_CATEGORIES } from "@/lib/prompt-data";
import { PageTransition } from "@/components/page-transition";
import { ScrollReveal } from "@/components/scroll-reveal";

export default function PromptsPage() {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("Tất cả");
  const [copied, setCopied] = useState<string | null>(null);

  const filtered = useMemo(() => {
    let result = PROMPTS;
    if (category !== "Tất cả") result = result.filter(p => p.category === category);
    if (search) {
      const q = search.toLowerCase();
      result = result.filter(p =>
        p.title.toLowerCase().includes(q) ||
        p.description.toLowerCase().includes(q) ||
        p.tags.some(t => t.toLowerCase().includes(q))
      );
    }
    return result;
  }, [search, category]);

  const copyPrompt = (slug: string, content: string) => {
    navigator.clipboard.writeText(content);
    setCopied(slug);
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <PageTransition>
      <div className="min-h-screen pt-24 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <ScrollReveal>
          <div className="text-center mb-12">
            <h1 className="text-4xl sm:text-5xl font-bold tracking-tight">
              Kho <span className="text-[var(--accent)]">Prompt</span>
            </h1>
            <p className="mt-4 text-lg text-[var(--text-muted)] max-w-2xl mx-auto">
              Bộ sưu tập prompt AI chất lượng cao — miễn phí và trả phí. Copy và dùng ngay.
            </p>
          </div>
        </ScrollReveal>

        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--text-muted)]" />
            <input
              type="text"
              placeholder="Tìm prompt..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 bg-[var(--surface)] border border-[var(--border)] rounded-lg text-sm focus:outline-none focus:border-[var(--accent)] transition-colors"
            />
          </div>
          <div className="flex gap-2 overflow-x-auto pb-1">
            {PROMPT_CATEGORIES.map(cat => (
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
          {filtered.map((prompt, i) => (
            <ScrollReveal key={prompt.slug} delay={i * 0.05}>
              <motion.div
                whileHover={{ y: -4 }}
                className="group bg-[var(--surface)] border border-[var(--border)] rounded-2xl p-5 hover:border-[var(--accent)] transition-colors"
              >
                <div className="flex items-start justify-between gap-2 mb-2">
                  <h3 className="font-semibold text-lg group-hover:text-[var(--accent)] transition-colors">
                    {prompt.title}
                  </h3>
                  <span className="text-sm font-bold text-[var(--accent)] whitespace-nowrap">
                    {prompt.price === 0 ? "Free" : `${prompt.price}k`}
                  </span>
                </div>
                <p className="text-sm text-[var(--text-muted)] mb-3 line-clamp-2">{prompt.description}</p>
                <div className="flex flex-wrap gap-1.5 mb-3">
                  {prompt.tags.map(tag => (
                    <span key={tag} className="px-2 py-0.5 text-xs rounded-md bg-[var(--bg)] text-[var(--text-muted)]">
                      {tag}
                    </span>
                  ))}
                </div>
                <div className="flex items-center gap-3 text-xs text-[var(--text-muted)] mb-3">
                  <span className="flex items-center gap-1"><Star className="w-3 h-3 text-yellow-500" /> {prompt.rating}</span>
                  <span className="flex items-center gap-1"><Users className="w-3 h-3" /> {prompt.uses}</span>
                </div>
                <button
                  onClick={() => copyPrompt(prompt.slug, prompt.content)}
                  className="w-full flex items-center justify-center gap-2 py-2 text-sm font-medium bg-[var(--accent)] text-[var(--bg)] rounded-lg hover:opacity-90 transition-opacity"
                >
                  {copied === prompt.slug ? <><Check className="w-4 h-4" /> Đã copy!</> : <><Copy className="w-4 h-4" /> Copy Prompt</>}
                </button>
              </motion.div>
            </ScrollReveal>
          ))}
        </div>

        {filtered.length === 0 && (
          <div className="text-center py-20 text-[var(--text-muted)]">
            Không tìm thấy prompt nào. Thử từ khóa khác.
          </div>
        )}
      </div>
    </PageTransition>
  );
}
