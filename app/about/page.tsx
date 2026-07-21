import type { Metadata } from "next";
import Link from "next/link";
import { ArrowUpRight, Coffee, Globe2, Heart } from "lucide-react";
import { PageTransition } from "@/components/page-transition";
import { SectionHeading } from "@/components/section-heading";
import { ScrollReveal } from "@/components/scroll-reveal";
import { SkillGrid } from "@/features/about/skill-grid";
import { Timeline } from "@/features/home/timeline";
import { Experience } from "@/features/home/experience";
import { Button } from "@marmoui/ui";
import { SITE, STATS } from "@/lib/data";

export const metadata: Metadata = {
  title: "About",
  description: `The story, skills, and timeline behind ${SITE.name} — an independent collective building open-source tools, AI products, and games.`,
};

const PRINCIPLES = [
  {
    icon: Heart,
    title: "Craft over hype",
    body: "We'd rather ship one thing well than ten things half-finished. Details compound — kerning, latency, error messages, all of it.",
  },
  {
    icon: Globe2,
    title: "Open by default",
    body: "Most of what we build lives on GitHub under permissive licenses. We share decisions, not just code, because that's what we needed when we were starting.",
  },
  {
    icon: Coffee,
    title: "Sustainable pace",
    body: "We're in this for the long arc. No crunch, no heroics — just consistent, careful work over years instead of weeks.",
  },
];

export default function AboutPage() {
  return (
    <PageTransition>
      {/* Hero */}
      <section className="relative overflow-hidden border-b border-[var(--color-edge)] py-20 md:py-28">
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-0 -z-10 bg-grid-faint opacity-30 [mask-image:radial-gradient(ellipse_at_top,black,transparent_70%)]"
        />
        <div className="container-editorial grid gap-12 lg:grid-cols-12">
          <div className="lg:col-span-7">
            <SectionHeading
              eyebrow="About the Team"
              title={
                <>
                  We&apos;re a small team{" "}
                  <span className="text-[var(--color-ink-faint)]">
                    obsessed with the craft.
                  </span>
                </>
              }
              description="NhutCoder Team is an independent collective of four — three engineers and one designer — building open-source tools, AI products, and games from Ho Chi Minh City, Vietnam. Founded in 2023, we've been shipping in public ever since."
            />
            <div className="mt-8 flex flex-wrap items-center gap-3">
              <Link href="/projects">
                <Button
                  variant="primary"
                  size="md"
                  rightIcon={<ArrowUpRight className="h-4 w-4" />}
                >
                  See the work
                </Button>
              </Link>
              <Link href="/contact">
                <Button variant="secondary" size="md">
                  Work with us
                </Button>
              </Link>
            </div>
          </div>

          {/* Stats card */}
          <div className="lg:col-span-5">
            <div className="grid grid-cols-2 gap-px overflow-hidden rounded-2xl border border-[var(--color-edge)] bg-[var(--color-edge)]">
              {STATS.map((stat) => (
                <div key={stat.label} className="bg-[var(--color-panel)] p-5">
                  <p className="font-display text-3xl font-semibold text-[var(--color-ink-strong)]">
                    {stat.value.toLocaleString("en-US")}
                    {stat.suffix}
                  </p>
                  <p className="mt-1 text-xs text-[var(--color-ink-faint)]">
                    {stat.label}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Story */}
      <section className="py-24 md:py-32">
        <div className="container-narrow">
          <ScrollReveal>
            <p className="label-mono mb-4 text-[var(--color-brand-400)]">
              The Story
            </p>
          </ScrollReveal>
          <ScrollReveal delay={0.05}>
            <h2 className="text-balance text-3xl font-semibold leading-[1.15] tracking-tight text-[var(--color-ink-strong)] md:text-4xl">
              It started with a single GitHub commit and a stubborn belief that
              small teams can ship software that feels handcrafted.
            </h2>
          </ScrollReveal>

          <div className="mt-10 space-y-6 text-lg leading-relaxed text-[var(--color-ink-soft)]">
            <ScrollReveal delay={0.1}>
              <p>
                We&apos;ve been writing software individually for years —
                building products for startups, consulting on architecture,
                contributing to open source on weekends. In 2023 we decided to
                formalise the collaboration. NhutCoder Team is the result.
              </p>
            </ScrollReveal>
            <ScrollReveal delay={0.15}>
              <p>
                Today we&apos;re four people who care a lot about a few things:
                typography, latency budgets, accessibility, error messages that
                actually help, and shipping things that feel{" "}
                <span className="text-[var(--color-ink-strong)]">finished</span>
                . We pick boring technology on purpose so we can spend our
                attention on the parts that matter.
              </p>
            </ScrollReveal>
            <ScrollReveal delay={0.2}>
              <p>
                Most of what we build is open source. Some of it becomes a
                product. All of it is shaped by the same set of principles.
              </p>
            </ScrollReveal>
          </div>
        </div>
      </section>

      {/* Principles */}
      <section className="border-y border-[var(--color-edge)] bg-[var(--color-surface-0)] py-24 md:py-32">
        <div className="container-editorial">
          <SectionHeading
            eyebrow="Principles"
            title={
              <>
                Three rules we keep{" "}
                <span className="text-[var(--color-ink-faint)]">
                  coming back to.
                </span>
              </>
            }
          />
          <div className="mt-12 grid gap-6 md:grid-cols-3">
            {PRINCIPLES.map((p, i) => (
              <ScrollReveal key={p.title} delay={i * 0.08}>
                <div className="h-full rounded-2xl border border-[var(--color-edge)] bg-[var(--color-panel)] p-6">
                  <span className="grid h-10 w-10 place-items-center rounded-xl border border-[var(--color-edge)] bg-[var(--color-surface-2)] text-[var(--color-brand-400)]">
                    <p.icon className="h-5 w-5" />
                  </span>
                  <h3 className="mt-4 text-lg font-semibold text-[var(--color-ink-strong)]">
                    {p.title}
                  </h3>
                  <p className="mt-2 text-sm leading-relaxed text-[var(--color-ink-soft)]">
                    {p.body}
                  </p>
                </div>
              </ScrollReveal>
            ))}
          </div>
        </div>
      </section>

      {/* Skills */}
      <section className="py-24 md:py-32">
        <div className="container-editorial">
          <SectionHeading
            eyebrow="Skills"
            title={
              <>
                The tools we&apos;ve{" "}
                <span className="text-[var(--color-ink-faint)]">
                  earned the right to use.
                </span>
              </>
            }
            description="A working snapshot of what we reach for, broken down by area. Levels reflect confidence and years of deliberate practice — not just hours logged."
          />
          <div className="mt-12">
            <SkillGrid />
          </div>
        </div>
      </section>

      {/* Reuse Timeline + Experience from home */}
      <Timeline />
      <Experience />
    </PageTransition>
  );
}
