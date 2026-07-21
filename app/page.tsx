import { Hero } from "@/features/home/hero";
import { FeaturedProjects } from "@/features/home/featured-projects";
import { Technology } from "@/features/home/technology";
import { Timeline } from "@/features/home/timeline";
import { Experience } from "@/features/home/experience";
import { GitHubSection } from "@/features/home/github-section";
import { ContactCTA } from "@/features/home/contact-cta";
import { PageTransition } from "@/components/page-transition";
import { PROJECTS } from "@/lib/data";

export default function HomePage() {
  return (
    <PageTransition>
      <Hero />
      <FeaturedProjects projects={PROJECTS.filter((p) => p.featured)} />
      <Technology />
      <Timeline />
      <Experience />
      <GitHubSection />
      <ContactCTA />
    </PageTransition>
  );
}
