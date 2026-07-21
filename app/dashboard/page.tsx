"use client";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { User, Package, Heart, Bookmark, Settings, LogOut } from "lucide-react";
import Link from "next/link";
import { PageTransition } from "@/components/page-transition";
import { PRODUCTS } from "@/lib/marketplace-data";
import { BLOG_POSTS } from "@/lib/blog-data";
import { PROJECTS } from "@/lib/data";

type Tab = "profile" | "purchases" | "favorites" | "saved" | "settings";

export default function DashboardPage() {
  const [tab, setTab] = useState<Tab>("profile");
  const [user, setUser] = useState<{ name: string; email: string } | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      window.location.href = "/login";
      return;
    }
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      setUser({ name: payload.name || "User", email: payload.email || "" });
    } catch {
      window.location.href = "/login";
    }
  }, []);

  if (!user) return null;

  const tabs: { id: Tab; label: string; icon: typeof User }[] = [
    { id: "profile", label: "Profile", icon: User },
    { id: "purchases", label: "Purchased", icon: Package },
    { id: "favorites", label: "Favorites", icon: Heart },
    { id: "saved", label: "Saved Blogs", icon: Bookmark },
    { id: "settings", label: "Settings", icon: Settings },
  ];

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  return (
    <PageTransition>
      <div className="min-h-screen pt-24 pb-20 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto">
        <div className="flex flex-col sm:flex-row gap-6">
          <div className="sm:w-56 flex-shrink-0">
            <div className="bg-[var(--surface)] border border-[var(--border)] rounded-2xl p-4">
              <div className="flex items-center gap-3 mb-4 pb-4 border-b border-[var(--border)]">
                <div className="w-10 h-10 rounded-full bg-[var(--accent)] flex items-center justify-center text-[var(--bg)] font-bold">
                  {user.name[0]?.toUpperCase()}
                </div>
                <div>
                  <div className="font-medium text-sm">{user.name}</div>
                  <div className="text-xs text-[var(--text-muted)] truncate max-w-[120px]">{user.email}</div>
                </div>
              </div>
              <nav className="space-y-1">
                {tabs.map(t => {
                  const Icon = t.icon;
                  return (
                    <button key={t.id} onClick={() => setTab(t.id)}
                      className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors ${
                        tab === t.id ? "bg-[var(--accent)] text-[var(--bg)]" : "text-[var(--text-muted)] hover:bg-[var(--surface-hover)]"
                      }`}>
                      <Icon className="w-4 h-4" /> {t.label}
                    </button>
                  );
                })}
                <button onClick={handleLogout}
                  className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-red-400 hover:bg-red-500/10 transition-colors">
                  <LogOut className="w-4 h-4" /> Logout
                </button>
              </nav>
            </div>
          </div>

          <div className="flex-1">
            <motion.div key={tab} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
              {tab === "profile" && (
                <div className="bg-[var(--surface)] border border-[var(--border)] rounded-2xl p-6">
                  <h2 className="text-xl font-bold mb-4">Profile</h2>
                  <div className="space-y-3">
                    <div><span className="text-sm text-[var(--text-muted)]">Name</span><p>{user.name}</p></div>
                    <div><span className="text-sm text-[var(--text-muted)]">Email</span><p>{user.email}</p></div>
                    <div><span className="text-sm text-[var(--text-muted)]">Member since</span><p>July 2026</p></div>
                  </div>
                </div>
              )}
              {tab === "purchases" && (
                <div>
                  <h2 className="text-xl font-bold mb-4">Purchased Products</h2>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {PRODUCTS.filter(p => p.price > 0).slice(0, 2).map(p => (
                      <Link key={p.slug} href={`/marketplace/${p.slug}`}
                        className="flex items-center gap-3 p-4 bg-[var(--surface)] border border-[var(--border)] rounded-xl hover:border-[var(--accent)] transition-colors">
                        <span className="text-3xl">{p.thumbnail}</span>
                        <div><div className="font-medium text-sm">{p.name}</div><div className="text-xs text-[var(--text-muted)]">v{p.version}</div></div>
                      </Link>
                    ))}
                  </div>
                </div>
              )}
              {tab === "favorites" && (
                <div>
                  <h2 className="text-xl font-bold mb-4">Favorite Projects</h2>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {PROJECTS.slice(0, 2).map((p: any) => (
                      <Link key={p.slug} href={`/projects`}
                        className="flex items-center gap-3 p-4 bg-[var(--surface)] border border-[var(--border)] rounded-xl hover:border-[var(--accent)] transition-colors">
                        <span className="text-3xl">{p.accent === "lime" ? "⚡" : "🎮"}</span>
                        <div><div className="font-medium text-sm">{p.name}</div><div className="text-xs text-[var(--text-muted)]">{p.category}</div></div>
                      </Link>
                    ))}
                  </div>
                </div>
              )}
              {tab === "saved" && (
                <div>
                  <h2 className="text-xl font-bold mb-4">Saved Blogs</h2>
                  <div className="space-y-3">
                    {BLOG_POSTS.slice(0, 3).map(p => (
                      <Link key={p.slug} href={`/blog/${p.slug}`}
                        className="block p-4 bg-[var(--surface)] border border-[var(--border)] rounded-xl hover:border-[var(--accent)] transition-colors">
                        <div className="font-medium text-sm">{p.title}</div>
                        <div className="text-xs text-[var(--text-muted)] mt-1">{p.date} · {p.readingTime} min read</div>
                      </Link>
                    ))}
                  </div>
                </div>
              )}
              {tab === "settings" && (
                <div className="bg-[var(--surface)] border border-[var(--border)] rounded-2xl p-6">
                  <h2 className="text-xl font-bold mb-4">Settings</h2>
                  <div className="space-y-4">
                    <label className="flex items-center justify-between"><span className="text-sm">Email notifications</span><input type="checkbox" defaultChecked className="w-4 h-4" /></label>
                    <label className="flex items-center justify-between"><span className="text-sm">Marketing emails</span><input type="checkbox" className="w-4 h-4" /></label>
                    <button className="px-4 py-2 bg-[var(--accent)] text-[var(--bg)] rounded-lg text-sm font-medium">Save Changes</button>
                  </div>
                </div>
              )}
            </motion.div>
          </div>
        </div>
      </div>
    </PageTransition>
  );
}
