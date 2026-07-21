// Blog post data — stored locally as markdown

export interface BlogPost {
  slug: string;
  title: string;
  excerpt: string;
  content: string;
  category: string;
  tags: string[];
  date: string;
  readingTime: number;
  featured: boolean;
}

export const BLOG_POSTS: BlogPost[] = [
  {
    slug: "building-with-marmo-ui",
    title: "Building with Marmo UI: A Designer's Perspective",
    excerpt: "How we used Marmo UI's component system to craft a premium portfolio site with dark-first editorial design.",
    category: "Design",
    tags: ["Marmo UI", "React", "Design System"],
    date: "2026-07-20",
    readingTime: 5,
    featured: true,
    content: `# Building with Marmo UI

Marmo UI is a React 19 + Tailwind 4 component library that provides 40+ production-ready components. Here's how we used it to build this website.

## Why Marmo UI?

- **40+ components** — Button, Card, Badge, Avatar, DataTable, Chart, Form, etc.
- **React 19 native** — built for the latest React features
- **Tailwind 4** — uses the latest Tailwind CSS engine
- **MIT license** — free for commercial use
- **MCP server** — AI agents can read live component APIs

## Key Components Used

### Button
\`\`\`tsx
<Button variant="primary" size="lg">Click me</Button>
\`\`\`

### Card
\`\`\`tsx
<Card>
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
</Card>
\`\`\`

## Design Decisions

We chose a dark-first editorial layout inspired by Linear, Raycast, and Vercel. The key principles:

1. **Strong typography** — Geist Sans + Geist Mono
2. **Editorial spacing** — generous whitespace
3. **Unique grids** — not generic 3-column layouts
4. **Micro animations** — subtle Framer Motion transitions

## Conclusion

Marmo UI gave us a solid foundation while allowing full creative freedom for custom components like AuroraBackground and MagneticButton.`,
  },
  {
    slug: "cloudflare-d1-drizzle-guide",
    title: "Cloudflare D1 + Drizzle ORM: The Complete Guide",
    excerpt: "Set up type-safe database queries on Cloudflare's edge network with Drizzle ORM and D1.",
    category: "Tutorial",
    tags: ["Cloudflare", "D1", "Drizzle", "Database"],
    date: "2026-07-19",
    readingTime: 8,
    featured: true,
    content: `# Cloudflare D1 + Drizzle ORM

A complete guide to setting up type-safe database queries on Cloudflare's edge network.

## Step 1: Create D1 Database

\`\`\`bash
npx wrangler d1 create nhutcoder-team-db
\`\`\`

## Step 2: Define Schema

\`\`\`typescript
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";

export const contacts = sqliteTable("contacts", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  name: text("name").notNull(),
  email: text("email").notNull(),
  message: text("message").notNull(),
});
\`\`\`

## Step 3: Configure Drizzle

\`\`\`typescript
import { drizzle } from "drizzle-orm/d1";

const db = drizzle(env.DB, { schema });
\`\`\`

## Step 4: Query

\`\`\`typescript
await db.insert(contacts).values({ name, email, message });
\`\`\`

## Conclusion

D1 + Drizzle gives you type-safe SQL queries on the edge, for free.`,
  },
  {
    slug: "nextjs-16-edge-runtime",
    title: "Next.js 16 Edge Runtime: What Changed",
    excerpt: "A deep dive into the new edge runtime features in Next.js 16 and how they affect Cloudflare deployment.",
    category: "Development",
    tags: ["Next.js", "Edge", "Cloudflare"],
    date: "2026-07-18",
    readingTime: 6,
    featured: false,
    content: `# Next.js 16 Edge Runtime

Next.js 16 brings significant improvements to edge runtime support.

## Key Changes

- Improved edge runtime stability
- Better Cloudflare Workers compatibility
- Native OpenNext support
- Faster cold starts

## Deploying to Cloudflare

Use OpenNext for Cloudflare to deploy Next.js apps as Workers:

\`\`\`bash
npx opennextjs-cloudflare build
npx wrangler deploy
\`\`\`

## Conclusion

Next.js 16 + Cloudflare Workers is a powerful combination for edge computing.`,
  },
  {
    slug: "opennext-cloudflare-deploy",
    title: "Deploying Next.js to Cloudflare Workers with OpenNext",
    excerpt: "A step-by-step guide to deploying Next.js apps to Cloudflare Workers using OpenNext.",
    category: "Tutorial",
    tags: ["OpenNext", "Cloudflare", "Deployment"],
    date: "2026-07-17",
    readingTime: 7,
    featured: false,
    content: `# Deploying Next.js to Cloudflare Workers

OpenNext for Cloudflare allows you to deploy Next.js apps as Cloudflare Workers.

## Setup

1. Install OpenNext:
\`\`\`bash
npm install @opennextjs/cloudflare
\`\`\`

2. Create \`open-next.config.ts\`:
\`\`\`typescript
import { defineCloudflareConfig } from "@opennextjs/cloudflare/config";
export default defineCloudflareConfig();
\`\`\`

3. Create \`wrangler.jsonc\`:
\`\`\`json
{
  "name": "my-app",
  "main": ".open-next/worker.js",
  "compatibility_date": "2026-07-01",
  "compatibility_flags": ["nodejs_compat"],
  "assets": {
    "directory": ".open-next/assets",
    "binding": "ASSETS"
  }
}
\`\`\`

4. Build and deploy:
\`\`\`bash
npm run build:cf
npx wrangler deploy
\`\`\`

## Conclusion

OpenNext makes Cloudflare Workers deployment seamless for Next.js apps.`,
  },
  {
    slug: "building-games-with-phaser",
    title: "Building Mobile Games with Phaser 3",
    excerpt: "How we built Prism Run and Candy World — two complete mobile games with Phaser 3 and TypeScript.",
    category: "Game Dev",
    tags: ["Phaser", "Game", "TypeScript"],
    date: "2026-07-16",
    readingTime: 10,
    featured: false,
    content: `# Building Mobile Games with Phaser 3

Phaser 3 is a powerful HTML5 game framework perfect for mobile-first games.

## Prism Run

Prism Run is a neon-drenched endless runner with:
- 5 game modes
- 6 characters
- Boss battles
- PWA support

## Candy World

Candy World is a 2D pixel-art platformer with:
- 3 levels
- Boss battle
- Touch controls
- Procedural textures

## Key Lessons

1. Use procedural textures to avoid asset loading
2. Implement touch controls early
3. Use object pooling for performance
4. PWA makes games installable

## Conclusion

Phaser 3 + TypeScript is an excellent stack for mobile web games.`,
  },
];

export const BLOG_CATEGORIES = ["All", "Design", "Tutorial", "Development", "Game Dev"];

export function getFeaturedPosts(): BlogPost[] {
  return BLOG_POSTS.filter(p => p.featured);
}

export function getPostBySlug(slug: string): BlogPost | undefined {
  return BLOG_POSTS.find(p => p.slug === slug);
}

export function getPostsByCategory(category: string): BlogPost[] {
  if (category === "All") return BLOG_POSTS;
  return BLOG_POSTS.filter(p => p.category === category);
}

export function searchPosts(query: string): BlogPost[] {
  const q = query.toLowerCase();
  return BLOG_POSTS.filter(p =>
    p.title.toLowerCase().includes(q) ||
    p.excerpt.toLowerCase().includes(q) ||
    p.tags.some(t => t.toLowerCase().includes(q))
  );
}

export function getRelatedPosts(slug: string, limit = 3): BlogPost[] {
  const post = getPostBySlug(slug);
  if (!post) return [];
  return BLOG_POSTS
    .filter(p => p.slug !== slug && p.category === post.category)
    .slice(0, limit);
}
