"use client";

import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";
import Link from "next/link";
import { ArrowUpRight, Sparkles, Terminal } from "lucide-react";
import { Button, Badge } from "@marmoui/ui";
import { AuroraBackground } from "@/components/aurora-background";
import { MagneticButton } from "@/components/magnetic-button";
import { SITE, STATS } from "@/lib/data";
import { AnimatedCounter } from "@/features/home/animated-counter";
import { useMousePosition } from "@/hooks/use-mouse-position";

export function Hero() {
  const ref = useRef<HTMLDivElement>(null);
  const mouse = useMousePosition();

  // Scroll-driven parallax for the hero stack
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end start"],
  });
  const yContent = useTransform(scrollYProgress, [0, 1], [0, 120]);
  const opacityContent = useTransform(scrollYProgress, [0, 0.8], [1, 0]);
  const yGlow = useTransform(scrollYProgress, [0, 1], [0, -80]);

  return (
    <section
      ref={ref}
      className="relative isolate overflow-hidden bg-[var(--color-bg)] pb-20 pt-16 md:pb-28 md:pt-24"
    >
      <AuroraBackground />
      <motion.div
        style={{ y: yGlow }}
        aria-hidden="true"
        className="absolute inset-0 -z-10"
      />

      <motion.div
        style={{ y: yContent, opacity: opacityContent }}
        className="container-editorial relative"
      >
        {/* Top status row */}
        <motion.div
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="flex items-center justify-between gap-4"
        >
          <Badge
            variant="success"
            size="sm"
            leftIcon={<Sparkles className="h-3 w-3" />}
          >
            Open for collaborations · 2025
          </Badge>
          <div className="hidden items-center gap-2 font-mono text-xs text-[var(--color-ink-faint)] md:flex">
            <span className="inline-block h-1.5 w-1.5 rounded-full bg-[var(--color-brand-500)] pulse-glow" />
            {SITE.location}
          </div>
        </motion.div>

        {/* Headline */}
        <div className="mt-12 grid items-end gap-10 md:mt-16 lg:grid-cols-12">
          <div className="lg:col-span-8">
            <motion.h1
              initial={{ opacity: 0, y: 24 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                duration: 0.8,
                delay: 0.05,
                ease: [0.22, 1, 0.36, 1],
              }}
              className="text-balance text-[clamp(2.5rem,7vw,5.5rem)] font-semibold leading-[0.98] tracking-[-0.035em] text-[var(--color-ink-strong)]"
            >
              Building the future
              <br />
              with{" "}
              <span className="relative inline-block">
                <span className="text-gradient-cyber">code &amp; AI</span>
                <motion.span
                  aria-hidden="true"
                  className="absolute -bottom-1 left-0 h-[3px] w-full origin-left bg-gradient-to-r from-[var(--color-brand-400)] to-[var(--color-accent-400)]"
                  initial={{ scaleX: 0 }}
                  animate={{ scaleX: 1 }}
                  transition={{
                    duration: 1,
                    delay: 0.6,
                    ease: [0.22, 1, 0.36, 1],
                  }}
                />
              </span>
              .
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                duration: 0.7,
                delay: 0.2,
                ease: [0.22, 1, 0.36, 1],
              }}
              className="mt-7 max-w-2xl text-pretty text-lg leading-relaxed text-[var(--color-ink-soft)] md:text-xl"
            >
              {SITE.name} is an independent collective shipping{" "}
              <span className="text-[var(--color-ink-strong)]">
                open-source tools
              </span>
              ,{" "}
              <span className="text-[var(--color-ink-strong)]">
                AI products
              </span>
              , and immersive web &amp; game experiences. We ship fast, ship
              openly, and obsess over craft.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                duration: 0.7,
                delay: 0.32,
                ease: [0.22, 1, 0.36, 1],
              }}
              className="mt-9 flex flex-wrap items-center gap-3"
            >
              <MagneticButton
                href="/projects"
                className="rounded-full"
                ariaLabel="View our work"
              >
                <Button
                  size="md"
                  variant="primary"
                  rightIcon={<ArrowUpRight className="h-4 w-4" />}
                >
                  View our work
                </Button>
              </MagneticButton>
              <MagneticButton
                href="/contact"
                className="rounded-full"
                ariaLabel="Start a project"
              >
                <Button size="md" variant="secondary">
                  Start a project
                </Button>
              </MagneticButton>
              <Link
                href={SITE.github}
                target="_blank"
                rel="noreferrer noopener"
                className="group inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium text-[var(--color-ink-soft)] transition-colors hover:text-[var(--color-ink-strong)]"
              >
                <Terminal className="h-4 w-4 text-[var(--color-brand-400)]" />
                <span className="font-mono text-xs">github.com/nhut0902</span>
              </Link>
            </motion.div>
          </div>

          {/* Side panel — terminal-style mini card with mouse parallax */}
          <motion.div
            initial={{ opacity: 0, y: 24, rotateY: 8 }}
            animate={{ opacity: 1, y: 0, rotateY: 0 }}
            transition={{ duration: 0.9, delay: 0.4, ease: [0.22, 1, 0.36, 1] }}
            className="lg:col-span-4"
            style={{
              transform: `perspective(1000px) rotateY(${mouse.nx * 4}deg) rotateX(${mouse.ny * -4}deg)`,
            }}
          >
            <HeroTerminalCard />
          </motion.div>
        </div>

        {/* Stats strip */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.55, ease: [0.22, 1, 0.36, 1] }}
          className="mt-16 grid grid-cols-2 gap-px overflow-hidden rounded-2xl border border-[var(--color-edge)] bg-[var(--color-edge)] md:grid-cols-4"
        >
          {STATS.map((stat) => (
            <div
              key={stat.label}
              className="bg-[var(--color-panel)] p-5 transition-colors hover:bg-[var(--color-surface-2)]"
            >
              <p className="font-display text-3xl font-semibold tracking-tight text-[var(--color-ink-strong)] md:text-4xl">
                <AnimatedCounter value={stat.value} suffix={stat.suffix} />
              </p>
              <p className="mt-1 text-xs text-[var(--color-ink-faint)]">
                {stat.label}
              </p>
            </div>
          ))}
        </motion.div>
      </motion.div>
    </section>
  );
}

/**
 * HeroTerminalCard — a small faux-terminal that reinforces the developer brand.
 * Decorative; uses static content to keep server-render friendly.
 */
function HeroTerminalCard() {
  return (
    <div className="relative overflow-hidden rounded-2xl border border-[var(--color-edge-strong)] bg-[var(--color-surface-1)] shadow-[0_30px_80px_-30px_rgba(0,0,0,0.6)]">
      <div className="flex items-center gap-2 border-b border-[var(--color-edge)] bg-[var(--color-surface-2)] px-4 py-2.5">
        <span className="h-2.5 w-2.5 rounded-full bg-[oklch(0.7_0.2_25)]" />
        <span className="h-2.5 w-2.5 rounded-full bg-[oklch(0.78_0.16_95)]" />
        <span className="h-2.5 w-2.5 rounded-full bg-[oklch(0.7_0.18_150)]" />
        <span className="ml-2 font-mono text-[11px] text-[var(--color-ink-faint)]">
          ~/nhutcoder/team — zsh
        </span>
      </div>
      <div className="space-y-2 p-5 font-mono text-[12.5px] leading-relaxed">
        <p>
          <span className="text-[var(--color-brand-400)]">›</span>{" "}
          <span className="text-[var(--color-ink-soft)]">whoami</span>
        </p>
        <p className="text-[var(--color-ink-faint)]">
          nhutcoder-team — open source · AI · web · games
        </p>
        <p className="pt-2">
          <span className="text-[var(--color-brand-400)]">›</span>{" "}
          <span className="text-[var(--color-ink-soft)]">ls ./shipped</span>
        </p>
        <p className="text-[var(--color-ink-faint)]">
          nebula-cli/ atlas-ui/ pulse-rag/ scriptforge/
        </p>
        <p className="pt-2">
          <span className="text-[var(--color-brand-400)]">›</span>{" "}
          <span className="text-[var(--color-ink-soft)]">
            git log --oneline -3
          </span>
        </p>
        <p className="text-[var(--color-ink-faint)]">
          a4f2c1d feat(atlas): chart primitives
        </p>
        <p className="text-[var(--color-ink-faint)]">
          9b3e8d2 fix(rag): streaming hydration
        </p>
        <p className="text-[var(--color-ink-faint)]">
          7710ace docs: ship faster, calmer
        </p>
        <p className="pt-2">
          <span className="text-[var(--color-brand-400)]">›</span>{" "}
          <span className="text-[var(--color-ink-strong)]">_</span>
          <motion.span
            aria-hidden="true"
            className="ml-0.5 inline-block h-4 w-[7px] translate-y-[2px] bg-[var(--color-brand-400)]"
            animate={{ opacity: [1, 0] }}
            transition={{ duration: 0.9, repeat: Infinity, ease: "easeInOut" }}
          />
        </p>
      </div>
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -right-10 -top-10 h-32 w-32 rounded-full bg-[var(--color-brand-500)]/20 blur-3xl"
      />
    </div>
  );
}
