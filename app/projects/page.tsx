import type { Metadata } from "next";
import { PageTransition } from "@/components/page-transition";
import { SectionHeading } from "@/components/section-heading";
import { ProjectExplorer } from "@/features/projects/project-explorer";
import { PROJECTS, PROJECT_CATEGORIES } from "@/lib/data";

export const metadata: Metadata = {
  title: "Projects",
  description:
    "Explore the open-source tools, AI products, and game titles shipped by the NhutCoder Team. Filter by category or search by stack.",
};

export default function ProjectsPage() {
  const categories = PROJECT_CATEGORIES.map((c) => ({
    id: c.id,
    label: c.label,
    count: c.count,
  }));

  return (
    <PageTransition>
      {/* Page header */}
      <section className="relative overflow-hidden border-b border-[var(--color-edge)] py-20 md:py-28">
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-0 -z-10 bg-grid-faint opacity-30 [mask-image:radial-gradient(ellipse_at_top,black,transparent_70%)]"
        />
        <div className="container-editorial">
          <SectionHeading
            eyebrow="The Work"
            title={
              <>
                Things we&apos;ve built,{" "}
                <span className="text-[var(--color-ink-faint)]">
                  in production.
                </span>
              </>
            }
            description="A working archive of the products, libraries, and experiments we've shipped. Some are open source — fork them, learn from them, ship your own."
          />
        </div>
      </section>

      {/* Explorer */}
      <section className="py-16 md:py-20">
        <div className="container-editorial">
          <ProjectExplorer projects={PROJECTS} categories={categories} />
        </div>
      </section>
    </PageTransition>
  );
}
