"use client";

import { useState, useMemo } from "react";
import { motion } from "framer-motion";
import { Search, Filter, ArrowRight, Check } from "lucide-react";
import { PRODUCTS, PRODUCT_CATEGORIES, type Product } from "@/lib/marketplace-data";
import { PageTransition } from "@/components/page-transition";
import { ScrollReveal } from "@/components/scroll-reveal";
import Link from "next/link";

export default function MarketplacePage() {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All");

  const filtered = useMemo(() => {
    let result = PRODUCTS;
    if (category !== "All") result = result.filter(p => p.category === category);
    if (search) {
      const q = search.toLowerCase();
      result = result.filter(p =>
        p.name.toLowerCase().includes(q) ||
        p.tagline.toLowerCase().includes(q) ||
        p.technologies.some(t => t.toLowerCase().includes(q))
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
              Code <span className="text-[var(--accent)]">Marketplace</span>
            </h1>
            <p className="mt-4 text-lg text-[var(--text-muted)] max-w-2xl mx-auto">
              Premium source code, game templates, and developer tools. Buy once, use forever.
            </p>
          </div>
        </ScrollReveal>

        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--text-muted)]" />
            <input
              type="text"
              placeholder="Search products..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 bg-[var(--surface)] border border-[var(--border)] rounded-lg text-sm focus:outline-none focus:border-[var(--accent)] transition-colors"
            />
          </div>
          <div className="flex gap-2 overflow-x-auto pb-1">
            {PRODUCT_CATEGORIES.map(cat => (
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
          {filtered.map((product, i) => (
            <ScrollReveal key={product.slug} delay={i * 0.05}>
              <ProductCard product={product} />
            </ScrollReveal>
          ))}
        </div>

        {filtered.length === 0 && (
          <div className="text-center py-20 text-[var(--text-muted)]">
            No products found. Try a different search.
          </div>
        )}
      </div>
    </PageTransition>
  );
}

function ProductCard({ product }: { product: Product }) {
  return (
    <motion.div
      whileHover={{ y: -4 }}
      className="group relative bg-[var(--surface)] border border-[var(--border)] rounded-2xl overflow-hidden hover:border-[var(--accent)] transition-colors"
    >
      <div className="aspect-video flex items-center justify-center text-6xl bg-gradient-to-br from-[var(--surface-hover)] to-[var(--surface)]">
        {product.thumbnail}
      </div>
      <div className="p-5">
        <div className="flex items-start justify-between gap-2 mb-2">
          <h3 className="font-semibold text-lg group-hover:text-[var(--accent)] transition-colors">
            {product.name}
          </h3>
          <span className="text-lg font-bold text-[var(--accent)] whitespace-nowrap">
            {product.price === 0 ? "Free" : `$${product.price}`}
          </span>
        </div>
        <p className="text-sm text-[var(--text-muted)] mb-3 line-clamp-2">{product.tagline}</p>
        <div className="flex flex-wrap gap-1.5 mb-4">
          {product.technologies.slice(0, 3).map(tech => (
            <span key={tech} className="px-2 py-0.5 text-xs rounded-md bg-[var(--bg)] text-[var(--text-muted)]">
              {tech}
            </span>
          ))}
        </div>
        <div className="flex gap-2">
          <Link
            href={`/marketplace/${product.slug}`}
            className="flex-1 text-center py-2 text-sm font-medium bg-[var(--accent)] text-[var(--bg)] rounded-lg hover:opacity-90 transition-opacity"
          >
            View Details
          </Link>
          {product.demoUrl && (
            <a
              href={product.demoUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="px-3 py-2 text-sm border border-[var(--border)] rounded-lg hover:bg-[var(--surface-hover)] transition-colors"
            >
              Demo
            </a>
          )}
        </div>
      </div>
    </motion.div>
  );
}
