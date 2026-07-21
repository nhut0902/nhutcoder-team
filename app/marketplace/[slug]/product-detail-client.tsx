"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { ArrowLeft, Check, ExternalLink, Github, Download } from "lucide-react";
import Link from "next/link";
import type { Product } from "@/lib/marketplace-data";
import { PageTransition } from "@/components/page-transition";
import { ScrollReveal } from "@/components/scroll-reveal";

export function ProductDetailClient({ product }: { product: Product }) {
  const [activeTab, setActiveTab] = useState<"features" | "changelog" | "tech">("features");

  return (
    <PageTransition>
      <div className="min-h-screen pt-24 pb-20 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
        <Link href="/marketplace" className="inline-flex items-center gap-2 text-sm text-[var(--text-muted)] hover:text-[var(--text)] mb-8 transition-colors">
          <ArrowLeft className="w-4 h-4" /> Back to Marketplace
        </Link>

        <ScrollReveal>
          <div className="flex flex-col sm:flex-row gap-6 mb-8">
            <div className="w-24 h-24 flex items-center justify-center text-5xl bg-[var(--surface)] border border-[var(--border)] rounded-2xl flex-shrink-0">
              {product.thumbnail}
            </div>
            <div className="flex-1">
              <h1 className="text-3xl font-bold mb-2">{product.name}</h1>
              <p className="text-lg text-[var(--text-muted)] mb-3">{product.tagline}</p>
              <div className="flex flex-wrap items-center gap-3">
                <span className="text-2xl font-bold text-[var(--accent)]">
                  {product.price === 0 ? "Free" : `$${product.price}`}
                </span>
                <span className="px-2 py-0.5 text-xs rounded-md bg-[var(--surface)] text-[var(--text-muted)]">v{product.version}</span>
                <span className="px-2 py-0.5 text-xs rounded-md bg-[var(--surface)] text-[var(--text-muted)]">{product.category}</span>
              </div>
            </div>
          </div>
        </ScrollReveal>

        <div className="flex flex-wrap gap-3 mb-8">
          {product.demoUrl && (
            <a href={product.demoUrl} target="_blank" rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-[var(--accent)] text-[var(--bg)] rounded-lg font-medium text-sm hover:opacity-90 transition-opacity">
              <ExternalLink className="w-4 h-4" /> Live Demo
            </a>
          )}
          {product.githubUrl && (
            <a href={product.githubUrl} target="_blank" rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-5 py-2.5 border border-[var(--border)] rounded-lg font-medium text-sm hover:bg-[var(--surface-hover)] transition-colors">
              <Github className="w-4 h-4" /> Source Code
            </a>
          )}
          <a href={product.githubUrl} target="_blank" rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-5 py-2.5 border border-[var(--border)] rounded-lg font-medium text-sm hover:bg-[var(--surface-hover)] transition-colors">
            <Download className="w-4 h-4" /> Download
          </a>
        </div>

        <div className="flex gap-2 mb-6 border-b border-[var(--border)]">
          {(["features", "tech", "changelog"] as const).map(tab => (
            <button key={tab} onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 text-sm font-medium capitalize transition-colors border-b-2 ${
                activeTab === tab ? "border-[var(--accent)] text-[var(--accent)]" : "border-transparent text-[var(--text-muted)]"
              }`}>
              {tab === "tech" ? "Technologies" : tab}
            </button>
          ))}
        </div>

        <motion.div key={activeTab} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
          {activeTab === "features" && (
            <ul className="space-y-3">
              {product.features.map((f, i) => (
                <li key={i} className="flex items-start gap-3">
                  <Check className="w-5 h-5 text-[var(--accent)] flex-shrink-0 mt-0.5" />
                  <span className="text-[var(--text)]">{f}</span>
                </li>
              ))}
            </ul>
          )}
          {activeTab === "tech" && (
            <div className="flex flex-wrap gap-2">
              {product.technologies.map(tech => (
                <span key={tech} className="px-3 py-1.5 text-sm rounded-lg bg-[var(--surface)] border border-[var(--border)]">
                  {tech}
                </span>
              ))}
            </div>
          )}
          {activeTab === "changelog" && (
            <div className="space-y-6">
              {product.changelog.map(entry => (
                <div key={entry.version}>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="font-semibold">v{entry.version}</span>
                    <span className="text-sm text-[var(--text-muted)]">{entry.date}</span>
                  </div>
                  <ul className="space-y-1 ml-4">
                    {entry.changes.map((c, i) => (
                      <li key={i} className="text-sm text-[var(--text-muted)] list-disc">{c}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          )}
        </motion.div>

        <div className="mt-12 p-6 bg-[var(--surface)] border border-[var(--border)] rounded-2xl">
          <h3 className="font-semibold mb-2">Description</h3>
          <p className="text-[var(--text-muted)] leading-relaxed">{product.description}</p>
        </div>
      </div>
    </PageTransition>
  );
}
