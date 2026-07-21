import Link from "next/link";
import { ArrowLeft, Compass } from "lucide-react";
import { Button } from "@marmoui/ui";

export default function NotFound() {
  return (
    <section className="relative flex min-h-[70vh] items-center justify-center overflow-hidden py-24">
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 -z-10 bg-grid-faint opacity-30 [mask-image:radial-gradient(ellipse_at_center,black,transparent_70%)]"
      />
      <div className="container-narrow text-center">
        <span className="inline-grid h-12 w-12 place-items-center rounded-2xl border border-[var(--color-edge-strong)] bg-[var(--color-surface-2)] text-[var(--color-brand-400)]">
          <Compass className="h-5 w-5" />
        </span>
        <p className="mt-6 font-mono text-sm text-[var(--color-brand-400)]">
          404 · not found
        </p>
        <h1 className="mt-3 text-balance text-4xl font-semibold tracking-tight text-[var(--color-ink-strong)] md:text-5xl">
          This page drifted off the grid.
        </h1>
        <p className="mx-auto mt-4 max-w-md text-pretty text-base text-[var(--color-ink-soft)]">
          The URL you followed doesn&apos;t exist — or it shipped to a different
          repo. Let&apos;s get you back on solid ground.
        </p>
        <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
          <Link href="/">
            <Button
              variant="primary"
              size="md"
              leftIcon={<ArrowLeft className="h-4 w-4" />}
            >
              Back home
            </Button>
          </Link>
          <Link href="/projects">
            <Button variant="secondary" size="md">
              Browse projects
            </Button>
          </Link>
        </div>
      </div>
    </section>
  );
}
