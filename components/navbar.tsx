"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Menu, X, LogIn } from "lucide-react";
import { cn } from "@/lib/utils";
import { NAV_ITEMS, SITE, SOCIAL_LINKS } from "@/lib/data";
import { Logo } from "@/components/logo";
import { ThemeToggle } from "@/components/theme-toggle";

export function Navbar() {
  const pathname = usePathname();
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => setMobileOpen(false), [pathname]);

  useEffect(() => {
    document.body.style.overflow = mobileOpen ? "hidden" : "";
    return () => { document.body.style.overflow = ""; };
  }, [mobileOpen]);

  return (
    <header className="fixed inset-x-0 top-0 z-50">
      <div
        className={cn(
          "mx-auto flex h-16 max-w-[88rem] items-center justify-between gap-4 px-4 transition-all duration-500 md:px-6",
          scrolled && "h-14 border-b border-[var(--color-edge)] bg-[var(--color-bg)]/80 backdrop-blur-xl"
        )}
      >
        <Link href="/" className="group relative flex items-center" aria-label={`${SITE.name} — home`}>
          <Logo />
        </Link>

        {/* Desktop nav */}
        <nav className="hidden items-center gap-0.5 lg:flex">
          {NAV_ITEMS.map((item) => {
            const active = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "relative rounded-full px-3 py-1.5 text-sm font-medium transition-colors duration-300",
                  active ? "text-[var(--color-ink-strong)]" : "text-[var(--color-ink-soft)] hover:text-[var(--color-ink-strong)]"
                )}
              >
                {active && (
                  <motion.span
                    layoutId="nav-active"
                    className="absolute inset-0 -z-10 rounded-full bg-[var(--color-muted)] ring-1 ring-inset ring-[var(--color-edge-strong)]"
                    transition={{ type: "spring", bounce: 0.18, duration: 0.5 }}
                  />
                )}
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center gap-2">
          <ThemeToggle />
          <Link
            href="/login"
            className="hidden sm:inline-flex items-center gap-1.5 rounded-full border border-[var(--color-border)] bg-[var(--color-panel)] px-3.5 py-1.5 text-sm font-medium text-[var(--color-ink-strong)] transition-colors hover:border-[var(--color-border-hover)]"
          >
            <LogIn className="h-3.5 w-3.5" />
            Đăng nhập
          </Link>

          {/* Mobile menu trigger */}
          <button
            type="button"
            aria-label="Open menu"
            aria-expanded={mobileOpen}
            onClick={() => setMobileOpen((s) => !s)}
            className="grid h-9 w-9 place-items-center rounded-full border border-[var(--color-border)] bg-[var(--color-panel)] text-[var(--color-ink-strong)] lg:hidden"
          >
            {mobileOpen ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
          </button>
        </div>
      </div>

      {/* Mobile drawer */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.25 }}
            className="fixed inset-0 top-14 z-40 lg:hidden"
          >
            <div className="absolute inset-0 bg-[var(--color-bg)]/80 backdrop-blur-xl" onClick={() => setMobileOpen(false)} aria-hidden="true" />
            <motion.nav
              initial={{ y: -8, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: -8, opacity: 0 }}
              transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
              className="relative mx-4 mt-2 overflow-hidden rounded-2xl border border-[var(--color-edge-strong)] bg-[var(--color-panel)] p-2"
            >
              {NAV_ITEMS.map((item, i) => {
                const active = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
                return (
                  <motion.div key={item.href} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.04 * i }}>
                    <Link
                      href={item.href}
                      className={cn(
                        "flex items-center justify-between rounded-xl px-4 py-3 text-base",
                        active ? "bg-[var(--color-muted)] text-[var(--color-ink-strong)]" : "text-[var(--color-ink-soft)]"
                      )}
                    >
                      {item.label}
                    </Link>
                  </motion.div>
                );
              })}
              <Link
                href="/login"
                className="mt-2 flex items-center gap-2 rounded-xl border border-[var(--color-edge)] px-4 py-3 text-base text-[var(--color-ink-strong)]"
              >
                <LogIn className="h-4 w-4" /> Đăng nhập
              </Link>
            </motion.nav>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
