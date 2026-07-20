import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { Logo } from "@/components/logo";
import { NAV_ITEMS, SITE, SOCIAL_LINKS } from "@/lib/data";

export function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="relative mt-24 border-t border-[var(--color-edge)] bg-[var(--color-bg)]">
      {/* Top hairline accent */}
      <div
        aria-hidden="true"
        className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-[var(--color-brand-500)]/40 to-transparent"
      />
      <div className="container-editorial py-14">
        <div className="grid gap-10 md:grid-cols-12">
          {/* Brand column */}
          <div className="md:col-span-5">
            <Logo />
            <p className="mt-4 max-w-sm text-sm leading-relaxed text-[var(--color-ink-soft)]">
              {SITE.description}
            </p>
            <a
              href={`mailto:${SITE.email}`}
              className="mt-5 inline-flex items-center gap-1.5 text-sm font-medium text-[var(--color-brand-400)] hover:text-[var(--color-brand-300)]"
            >
              {SITE.email}
              <ArrowUpRight className="h-3.5 w-3.5" />
            </a>
          </div>

          {/* Nav columns */}
          <div className="grid grid-cols-2 gap-8 md:col-span-4 md:grid-cols-2">
            <FooterCol
              title="Navigate"
              items={NAV_ITEMS.map((n) => ({ label: n.label, href: n.href }))}
            />
            <FooterCol
              title="Open Source"
              items={[
                { label: "GitHub", href: SITE.github, external: true },
                {
                  label: "Nebula CLI",
                  href: "https://github.com/nhut0902/nebula-cli",
                  external: true,
                },
                {
                  label: "Atlas UI",
                  href: "https://github.com/nhut0902/atlas-ui",
                  external: true,
                },
                {
                  label: "Pulse RAG",
                  href: "https://github.com/nhut0902/pulse-rag",
                  external: true,
                },
              ]}
            />
          </div>

          {/* Social */}
          <div className="md:col-span-3">
            <p className="label-mono mb-3">Connect</p>
            <ul className="space-y-2.5">
              {SOCIAL_LINKS.map((s) => (
                <li key={s.label}>
                  <a
                    href={s.href}
                    target="_blank"
                    rel="noreferrer noopener"
                    className="group flex items-center justify-between text-sm text-[var(--color-ink-soft)] hover:text-[var(--color-ink-strong)]"
                  >
                    <span>{s.label}</span>
                    <span className="font-mono text-xs text-[var(--color-ink-faint)] transition-colors group-hover:text-[var(--color-brand-400)]">
                      {s.handle}
                    </span>
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-12 flex flex-col items-start justify-between gap-3 border-t border-[var(--color-edge)] pt-6 text-xs text-[var(--color-ink-faint)] sm:flex-row sm:items-center">
          <p>
            © {year} {SITE.name}. Built with care in {SITE.location}.
          </p>
          <p className="font-mono">
            <span className="mr-1.5 inline-block h-1.5 w-1.5 translate-y-[-1px] rounded-full bg-[var(--color-brand-500)] pulse-glow align-middle" />
            All systems operational
          </p>
        </div>
      </div>
    </footer>
  );
}

interface FooterLink {
  label: string;
  href: string;
  external?: boolean;
}

function FooterCol({ title, items }: { title: string; items: FooterLink[] }) {
  return (
    <div>
      <p className="label-mono mb-3">{title}</p>
      <ul className="space-y-2.5">
        {items.map((item) => (
          <li key={item.label}>
            {item.external ? (
              <a
                href={item.href}
                target="_blank"
                rel="noreferrer noopener"
                className="text-sm text-[var(--color-ink-soft)] transition-colors hover:text-[var(--color-ink-strong)]"
              >
                {item.label}
              </a>
            ) : (
              <Link
                href={item.href}
                className="text-sm text-[var(--color-ink-soft)] transition-colors hover:text-[var(--color-ink-strong)]"
              >
                {item.label}
              </Link>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
