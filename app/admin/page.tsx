"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Lock, FileText, Eye, Plus, LogOut, TrendingUp, Users, DollarSign, FileEdit } from "lucide-react";
import { PageTransition } from "@/components/page-transition";
import { PRODUCTS } from "@/lib/marketplace-data";
import { BLOG_POSTS } from "@/lib/blog-data";
import { PROMPTS } from "@/lib/prompt-data";

const ADMIN_PASSWORD = "0902@";

export default function AdminPage() {
  const [authed, setAuthed] = useState(false);
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [tab, setTab] = useState<"dashboard" | "posts" | "products" | "prompts">("dashboard");

  useEffect(() => {
    if (sessionStorage.getItem("admin_authed") === "true") setAuthed(true);
  }, []);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (password === ADMIN_PASSWORD) {
      sessionStorage.setItem("admin_authed", "true");
      setAuthed(true);
      setError("");
    } else {
      setError("Mật khẩu sai!");
    }
  };

  const handleLogout = () => {
    sessionStorage.removeItem("admin_authed");
    setAuthed(false);
  };

  if (!authed) {
    return (
      <PageTransition>
        <div className="min-h-screen flex items-center justify-center px-4 pt-24 pb-12">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
            className="w-full max-w-md bg-[var(--surface)] border border-[var(--border)] rounded-2xl p-8">
            <div className="flex items-center justify-center mb-6">
              <div className="w-12 h-12 rounded-full bg-[var(--accent)]/20 flex items-center justify-center">
                <Lock className="w-6 h-6 text-[var(--accent)]" />
              </div>
            </div>
            <h1 className="text-2xl font-bold mb-6 text-center">Admin Dashboard</h1>
            {error && <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-sm text-red-400">{error}</div>}
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1.5">Mật khẩu</label>
                <input type="password" required value={password} onChange={e => setPassword(e.target.value)}
                  className="w-full px-4 py-2.5 bg-[var(--bg)] border border-[var(--border)] rounded-lg text-sm focus:outline-none focus:border-[var(--accent)]"
                  placeholder="Nhập mật khẩu admin" />
              </div>
              <button type="submit"
                className="w-full py-2.5 bg-[var(--accent)] text-[var(--bg)] rounded-lg font-medium text-sm">
                Đăng nhập Admin
              </button>
            </form>
          </motion.div>
        </div>
      </PageTransition>
    );
  }

  const stats = [
    { label: "Bài viết", value: BLOG_POSTS.length, icon: FileText, color: "text-blue-400" },
    { label: "Sản phẩm", value: PRODUCTS.length, icon: DollarSign, color: "text-green-400" },
    { label: "Prompts", value: PROMPTS.length, icon: TrendingUp, color: "text-purple-400" },
    { label: "Lượt xem", value: "12.4k", icon: Eye, color: "text-orange-400" },
  ];

  const tabs = [
    { id: "dashboard" as const, label: "Tổng quan", icon: TrendingUp },
    { id: "posts" as const, label: "Bài viết", icon: FileText },
    { id: "products" as const, label: "Sản phẩm", icon: DollarSign },
    { id: "prompts" as const, label: "Prompts", icon: Users },
  ];

  return (
    <PageTransition>
      <div className="min-h-screen pt-24 pb-20 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold">Admin Dashboard</h1>
          <button onClick={handleLogout}
            className="flex items-center gap-2 px-4 py-2 text-sm border border-[var(--border)] rounded-lg hover:bg-[var(--surface-hover)] transition-colors text-red-400">
            <LogOut className="w-4 h-4" /> Đăng xuất
          </button>
        </div>

        <div className="flex gap-2 mb-6 overflow-x-auto pb-1">
          {tabs.map(t => {
            const Icon = t.icon;
            return (
              <button key={t.id} onClick={() => setTab(t.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-all ${
                  tab === t.id ? "bg-[var(--accent)] text-[var(--bg)]" : "bg-[var(--surface)] text-[var(--text-muted)]"
                }`}>
                <Icon className="w-4 h-4" /> {t.label}
              </button>
            );
          })}
        </div>

        <motion.div key={tab} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
          {tab === "dashboard" && (
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
              {stats.map(s => {
                const Icon = s.icon;
                return (
                  <div key={s.label} className="bg-[var(--surface)] border border-[var(--border)] rounded-2xl p-5">
                    <Icon className={`w-6 h-6 mb-3 ${s.color}`} />
                    <div className="text-2xl font-bold">{s.value}</div>
                    <div className="text-sm text-[var(--text-muted)]">{s.label}</div>
                  </div>
                );
              })}
            </div>
          )}

          {tab === "posts" && (
            <div>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold">Quản lý bài viết</h2>
                <button className="flex items-center gap-2 px-4 py-2 bg-[var(--accent)] text-[var(--bg)] rounded-lg text-sm font-medium">
                  <Plus className="w-4 h-4" /> Đăng bài
                </button>
              </div>
              <div className="space-y-3">
                {BLOG_POSTS.map(post => (
                  <div key={post.slug} className="flex items-center justify-between p-4 bg-[var(--surface)] border border-[var(--border)] rounded-xl">
                    <div>
                      <div className="font-medium text-sm">{post.title}</div>
                      <div className="text-xs text-[var(--text-muted)]">{post.date} · {post.category} · {post.readingTime} phút</div>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-[var(--text-muted)] flex items-center gap-1"><Eye className="w-3 h-3" /> {Math.floor(Math.random() * 500)}</span>
                      <button className="p-2 hover:bg-[var(--surface-hover)] rounded-lg transition-colors"><FileEdit className="w-4 h-4" /></button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {tab === "products" && (
            <div>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold">Quản lý sản phẩm</h2>
                <button className="flex items-center gap-2 px-4 py-2 bg-[var(--accent)] text-[var(--bg)] rounded-lg text-sm font-medium">
                  <Plus className="w-4 h-4" /> Thêm sản phẩm
                </button>
              </div>
              <div className="space-y-3">
                {PRODUCTS.map(p => (
                  <div key={p.slug} className="flex items-center justify-between p-4 bg-[var(--surface)] border border-[var(--border)] rounded-xl">
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">{p.thumbnail}</span>
                      <div>
                        <div className="font-medium text-sm">{p.name}</div>
                        <div className="text-xs text-[var(--text-muted)]">{p.category} · v{p.version}</div>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-sm font-bold text-[var(--accent)]">{p.price === 0 ? "Free" : `$${p.price}`}</span>
                      <span className="text-xs text-[var(--text-muted)] flex items-center gap-1"><Eye className="w-3 h-3" /> {Math.floor(Math.random() * 1000)}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {tab === "prompts" && (
            <div>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold">Quản lý Prompts</h2>
                <button className="flex items-center gap-2 px-4 py-2 bg-[var(--accent)] text-[var(--bg)] rounded-lg text-sm font-medium">
                  <Plus className="w-4 h-4" /> Thêm prompt
                </button>
              </div>
              <div className="space-y-3">
                {PROMPTS.map(p => (
                  <div key={p.slug} className="flex items-center justify-between p-4 bg-[var(--surface)] border border-[var(--border)] rounded-xl">
                    <div>
                      <div className="font-medium text-sm">{p.title}</div>
                      <div className="text-xs text-[var(--text-muted)]">{p.category} · {p.uses} lượt dùng · ★{p.rating}</div>
                    </div>
                    <span className="text-sm font-bold text-[var(--accent)]">{p.price === 0 ? "Free" : `${p.price}k`}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </PageTransition>
  );
}
