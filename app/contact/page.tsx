import type { Metadata } from "next";
import Link from "next/link";
import { ArrowUpRight, Clock, Mail, MapPin } from "lucide-react";
import { PageTransition } from "@/components/page-transition";
import { SectionHeading } from "@/components/section-heading";
import { ContactForm } from "@/features/contact/contact-form";
import { SITE, SOCIAL_LINKS } from "@/lib/data";

export const metadata: Metadata = {
  title: "Contact",
  description: `Get in touch with ${SITE.name}. We reply to every enquiry within one business day.`,
};

export default function ContactPage() {
  return (
    <PageTransition>
      <section className="relative overflow-hidden border-b border-[var(--color-edge)] py-20 md:py-28">
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-0 -z-10 bg-grid-faint opacity-30 [mask-image:radial-gradient(ellipse_at_top,black,transparent_70%)]"
        />
        <div className="container-editorial">
          <SectionHeading
            eyebrow="Get in Touch"
            title={
              <>
                Tell us what you&apos;re{" "}
                <span className="text-[var(--color-ink-faint)]">
                  trying to build.
                </span>
              </>
            }
            description="Whether it's a fully-specced product or a half-formed idea, we'd love to hear about it. We read every message and reply within one business day."
          />
        </div>
      </section>

      <section className="py-16 md:py-24">
        <div className="container-editorial grid gap-10 lg:grid-cols-12 lg:gap-12">
          {/* Form */}
          <div className="lg:col-span-7">
            <ContactForm />
          </div>

          {/* Sidebar */}
          <aside className="lg:col-span-5">
            <div className="space-y-6">
              <div className="rounded-2xl border border-[var(--color-edge)] bg-[var(--color-panel)] p-6">
                <p className="label-mono mb-4">Direct channels</p>
                <ul className="space-y-4">
                  <li>
                    <a
                      href={`mailto:${SITE.email}`}
                      className="group flex items-start gap-3"
                    >
                      <span className="grid h-9 w-9 shrink-0 place-items-center rounded-lg border border-[var(--color-edge)] bg-[var(--color-surface-2)] text-[var(--color-brand-400)] transition-colors group-hover:border-[var(--color-brand-500)]">
                        <Mail className="h-4 w-4" />
                      </span>
                      <span>
                        <span className="block text-sm font-medium text-[var(--color-ink-strong)]">
                          Email
                        </span>
                        <span className="block font-mono text-xs text-[var(--color-ink-faint)]">
                          {SITE.email}
                        </span>
                      </span>
                    </a>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="grid h-9 w-9 shrink-0 place-items-center rounded-lg border border-[var(--color-edge)] bg-[var(--color-surface-2)] text-[var(--color-ink-soft)]">
                      <MapPin className="h-4 w-4" />
                    </span>
                    <span>
                      <span className="block text-sm font-medium text-[var(--color-ink-strong)]">
                        Location
                      </span>
                      <span className="block font-mono text-xs text-[var(--color-ink-faint)]">
                        {SITE.location} · GMT+7
                      </span>
                    </span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="grid h-9 w-9 shrink-0 place-items-center rounded-lg border border-[var(--color-edge)] bg-[var(--color-surface-2)] text-[var(--color-ink-soft)]">
                      <Clock className="h-4 w-4" />
                    </span>
                    <span>
                      <span className="block text-sm font-medium text-[var(--color-ink-strong)]">
                        Response time
                      </span>
                      <span className="block font-mono text-xs text-[var(--color-ink-faint)]">
                        Within 1 business day
                      </span>
                    </span>
                  </li>
                </ul>
              </div>

              <div className="rounded-2xl border border-[var(--color-edge)] bg-[var(--color-panel)] p-6">
                <p className="label-mono mb-4">Find us on</p>
                <ul className="space-y-2.5">
                  {SOCIAL_LINKS.map((s) => (
                    <li key={s.label}>
                      <a
                        href={s.href}
                        target="_blank"
                        rel="noreferrer noopener"
                        className="group flex items-center justify-between rounded-lg border border-transparent px-2 py-1.5 transition-colors hover:border-[var(--color-edge)] hover:bg-[var(--color-surface-2)]"
                      >
                        <span className="text-sm text-[var(--color-ink-soft)] group-hover:text-[var(--color-ink-strong)]">
                          {s.label}
                        </span>
                        <span className="flex items-center gap-2 font-mono text-xs text-[var(--color-ink-faint)]">
                          {s.handle}
                          <ArrowUpRight className="h-3 w-3 opacity-0 transition-opacity group-hover:opacity-100" />
                        </span>
                      </a>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="relative overflow-hidden rounded-2xl border border-[var(--color-edge-strong)] bg-[var(--color-surface-1)] p-6">
                <div
                  aria-hidden="true"
                  className="pointer-events-none absolute -right-12 -top-12 h-32 w-32 rounded-full bg-[var(--color-brand-500)]/20 blur-3xl"
                />
                <p className="label-mono mb-2 text-[var(--color-brand-400)]">
                  Working with us
                </p>
                <p className="text-sm leading-relaxed text-[var(--color-ink-soft)]">
                  We work in 6–12 week sprints, ship to production weekly, and
                  hand over a codebase your team can actually maintain. Equity,
                  retainer, and fixed-scope engagements all welcome.
                </p>
                <Link
                  href="/projects"
                  className="mt-4 inline-flex items-center gap-1.5 text-sm font-medium text-[var(--color-brand-400)] hover:text-[var(--color-brand-300)]"
                >
                  See past work
                  <ArrowUpRight className="h-3.5 w-3.5" />
                </Link>
              </div>
            </div>
          </aside>
        </div>
      </section>
    </PageTransition>
  );
}
