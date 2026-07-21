"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowUpRight, Mail } from "lucide-react";
import { MagneticButton } from "@/components/magnetic-button";
import { Button } from "@marmoui/ui";
import { SITE, SOCIAL_LINKS } from "@/lib/data";

/**
 * ContactCTA — big editorial "let's build something" closer.
 */
export function ContactCTA() {
  return (
    <section className="relative py-24 md:py-36">
      <div className="container-editorial">
        <div className="relative overflow-hidden rounded-[2rem] border border-[var(--color-edge-strong)] bg-[var(--color-surface-1)] px-6 py-16 md:px-16 md:py-24">
          {/* Background flourish */}
          <div
            aria-hidden="true"
            className="pointer-events-none absolute inset-0 -z-10 bg-grid-faint opacity-40 [mask-image:radial-gradient(ellipse_at_top,black,transparent_75%)]"
          />
          <motion.div
            aria-hidden="true"
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 1.2, ease: [0.22, 1, 0.36, 1] }}
            className="pointer-events-none absolute -right-32 -top-32 h-[460px] w-[460px] rounded-full bg-[var(--color-brand-500)]/15 blur-[140px]"
          />
          <motion.div
            aria-hidden="true"
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 1.2, delay: 0.1, ease: [0.22, 1, 0.36, 1] }}
            className="pointer-events-none absolute -bottom-32 -left-32 h-[460px] w-[460px] rounded-full bg-[var(--color-accent-500)]/15 blur-[140px]"
          />

          <div className="relative mx-auto max-w-3xl text-center">
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="inline-flex items-center gap-2 rounded-full border border-[var(--color-edge)] bg-[var(--color-surface-2)] px-3 py-1 text-xs"
            >
              <span className="inline-block h-1.5 w-1.5 rounded-full bg-[var(--color-brand-500)] pulse-glow" />
              <span className="font-mono text-[var(--color-ink-soft)]">
                Currently accepting projects for Q2 2025
              </span>
            </motion.div>

            <motion.h2
              initial={{ opacity: 0, y: 18 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{
                duration: 0.7,
                delay: 0.05,
                ease: [0.22, 1, 0.36, 1],
              }}
              className="mt-6 text-balance text-4xl font-semibold leading-[1.05] tracking-tight text-[var(--color-ink-strong)] md:text-6xl"
            >
              Let&apos;s build something{" "}
              <span className="text-gradient-cyber">worth shipping.</span>
            </motion.h2>

            <motion.p
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.7, delay: 0.18 }}
              className="mx-auto mt-5 max-w-xl text-pretty text-base leading-relaxed text-[var(--color-ink-soft)] md:text-lg"
            >
              Whether you have a fully-specced product or just a half-formed
              idea on a napkin — we&apos;d love to hear about it. Expect a reply
              within one business day.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.7, delay: 0.28 }}
              className="mt-9 flex flex-wrap items-center justify-center gap-3"
            >
              <MagneticButton href="/contact" ariaLabel="Get in touch">
                <Button
                  size="lg"
                  variant="primary"
                  rightIcon={<ArrowUpRight className="h-4 w-4" />}
                >
                  Get in touch
                </Button>
              </MagneticButton>
              <Link
                href={`mailto:${SITE.email}`}
                className="inline-flex items-center gap-2 rounded-full border border-[var(--color-edge)] bg-[var(--color-panel)] px-5 py-2.5 text-sm font-medium text-[var(--color-ink-soft)] transition-colors hover:border-[var(--color-border-hover)] hover:text-[var(--color-ink-strong)]"
              >
                <Mail className="h-4 w-4 text-[var(--color-brand-400)]" />
                <span className="font-mono">{SITE.email}</span>
              </Link>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="mt-12 flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-xs text-[var(--color-ink-faint)]"
            >
              <span className="font-mono">Or find us on</span>
              {SOCIAL_LINKS.map((s) => (
                <Link
                  key={s.label}
                  href={s.href}
                  target="_blank"
                  rel="noreferrer noopener"
                  className="font-mono transition-colors hover:text-[var(--color-brand-400)]"
                >
                  {s.label}
                </Link>
              ))}
            </motion.div>
          </div>
        </div>
      </div>
    </section>
  );
}
