import type { Metadata } from "next";
import { PageTransition } from "@/components/page-transition";
import { SectionHeading } from "@/components/section-heading";
import { BlogList } from "@/features/blog/blog-list";
import { BLOG_POSTS, BLOG_CATEGORIES } from "@/lib/data";

export const metadata: Metadata = {
  title: "Blog",
  description:
    "Field notes on engineering, AI, design systems, game development, and the slow craft of shipping software. Written by the NhutCoder Team.",
};

export default function BlogPage() {
  return (
    <PageTransition>
      <section className="relative overflow-hidden border-b border-[var(--color-edge)] py-20 md:py-28">
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-0 -z-10 bg-grid-faint opacity-30 [mask-image:radial-gradient(ellipse_at_top,black,transparent_70%)]"
        />
        <div className="container-editorial">
          <SectionHeading
            eyebrow="Field Notes"
            title={
              <>
                Writing that{" "}
                <span className="text-[var(--color-ink-faint)]">
                  earns your attention.
                </span>
              </>
            }
            description="Long-form notes on engineering, AI, design systems, and the slow craft of shipping software. No hot takes — just what we've learned the hard way."
          />
        </div>
      </section>

      <section className="py-16 md:py-20">
        <div className="container-editorial">
          <BlogList posts={BLOG_POSTS} categories={BLOG_CATEGORIES} />
        </div>
      </section>
    </PageTransition>
  );
}
