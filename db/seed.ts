// Seed script — run with: bun db/seed.ts or npm run db:seed
// Requires D1 binding configured locally via wrangler

/* eslint-disable @typescript-eslint/no-unused-vars */
// Seed script — outputs SQL for wrangler d1 execute

import type { drizzle } from "drizzle-orm/d1";
import type { blogPosts, projects } from "./schema";

// This script is meant to run via `wrangler d1 execute` with SQL output
// For local dev: wrangler d1 execute nhutcoder-team-db --local --command="..."

const seedBlogPosts = [
  {
    slug: "building-with-marmo-ui",
    title: "Building with Marmo UI: A Designer's Perspective",
    excerpt: "How we used Marmo UI's component system to craft a premium portfolio site.",
    category: "Design",
    published: true,
  },
  {
    slug: "cloudflare-d1-drizzle-guide",
    title: "Cloudflare D1 + Drizzle ORM: The Complete Guide",
    excerpt: "Set up type-safe database queries on Cloudflare's edge network.",
    category: "Tutorial",
    published: true,
  },
  {
    slug: "nextjs-16-edge-runtime",
    title: "Next.js 16 Edge Runtime: What Changed",
    excerpt: "A deep dive into the new edge runtime features in Next.js 16.",
    category: "Development",
    published: true,
  },
];

const seedProjects = [
  {
    slug: "prism-run",
    name: "Prism Run",
    description: "Neon-drenched endless runner game with 3D graphics.",
    tech: "Phaser, TypeScript, Vite",
    repoUrl: "https://github.com/nhut0902/prism-run",
    featured: true,
  },
  {
    slug: "zombie-escape",
    name: "Zombie Escape",
    description: "Mobile-first 3D zombie survival shooter.",
    tech: "Three.js, Vite, PWA",
    repoUrl: "https://github.com/nhut0902/zombie-escape",
    featured: true,
  },
  {
    slug: "html-playground",
    name: "HTML Playground",
    description: "Online HTML/CSS/JS editor with live preview.",
    tech: "Vanilla JS, PWA",
    repoUrl: "https://github.com/nhut0902/html-playground",
    featured: true,
  },
];

// Output SQL for wrangler d1 execute
function generateSQL() {
  let sql = "";
  for (const p of seedBlogPosts) {
    sql += `INSERT INTO blog_posts (slug, title, excerpt, category, published) VALUES ('${p.slug}', '${p.title}', '${p.excerpt}', '${p.category}', ${p.published ? 1 : 0});\n`;
  }
  for (const p of seedProjects) {
    sql += `INSERT INTO projects (slug, name, description, tech, repo_url, featured) VALUES ('${p.slug}', '${p.name}', '${p.description}', '${p.tech}', '${p.repoUrl}', ${p.featured ? 1 : 0});\n`;
  }
  return sql;
}

console.log("-- Seed SQL for Cloudflare D1");
console.log("-- Run with: wrangler d1 execute nhutcoder-team-db --local --command=\"...\"");
console.log(generateSQL());
