import type {
  Project,
  BlogPost,
  Skill,
  TimelineEntry,
  ExperienceEntry,
  NavItem,
  SocialLink,
} from "@/types";

export const SITE = {
  name: "NhutCoder Team",
  tagline: "Building the future with code and AI",
  description:
    "NhutCoder Team — an independent developer collective building open-source tools, AI products, and immersive web & game experiences. We ship fast, ship openly, and obsess over craft.",
  url: process.env.NEXT_PUBLIC_SITE_URL ?? "https://nhutcoder.team",
  github: "https://github.com/nhut0902",
  githubUsername: "nhut0902",
  email: "hello@nhutcoder.team",
  location: "Ho Chi Minh City, Vietnam",
  founded: 2022,
  ogImage: "/og.png",
  keywords: [
    "NhutCoder",
    "NhutCoder Team",
    "Open Source",
    "AI",
    "Web Development",
    "Game Development",
    "Next.js",
    "TypeScript",
    "Developer Portfolio",
  ],
} as const;

export const NAV_ITEMS: NavItem[] = [
  { label: "Home", href: "/" },
  { label: "Projects", href: "/projects" },
  { label: "About", href: "/about" },
  { label: "Blog", href: "/blog" },
  { label: "Contact", href: "/contact" },
];

export const SOCIAL_LINKS: SocialLink[] = [
  {
    label: "GitHub",
    href: "https://github.com/nhut0902",
    handle: "@nhut0902",
    icon: "github",
    category: "code",
  },
  {
    label: "Facebook",
    href: "https://facebook.com/nhutcoder.team",
    handle: "Nhutcoder Team",
    icon: "facebook",
    category: "social",
  },
  {
    label: "TikTok",
    href: "https://www.tiktok.com/@nhutcoderlamcontent",
    handle: "@nhutcoderlamcontent",
    icon: "tiktok",
    category: "social",
  },
];

export const PROJECTS: Project[] = [
  {
    slug: "nebula-cli",
    name: "Nebula CLI",
    tagline: "AI-native command line for shipping faster",
    description:
      "A zero-config TypeScript CLI that scaffolds production-grade Next.js apps with AI coding assistant integration, design tokens, and CI baked in. Used by 1,200+ developers weekly.",
    tags: ["Open Source", "CLI", "AI", "TypeScript"],
    category: "tools",
    featured: true,
    year: 2025,
    stack: ["TypeScript", "Node.js", "OpenAI", "Radix"],
    metrics: [
      { label: "GitHub Stars", value: "3.4k" },
      { label: "Weekly Installs", value: "12k" },
    ],
    repo: "https://github.com/nhut0902/nebula-cli",
    demo: "https://nebula.sh",
    accent: "lime",
  },
  {
    slug: "atlas-ui",
    name: "Atlas UI",
    tagline: "Headless component system for design-driven teams",
    description:
      "A fully accessible React component library with first-class Figma sync, design tokens, and a theming engine built on CSS custom properties. Powers 30+ production apps.",
    tags: ["Open Source", "React", "Design System"],
    category: "libraries",
    featured: true,
    year: 2025,
    stack: ["React", "Radix UI", "Tailwind CSS", "Figma API"],
    metrics: [
      { label: "Components", value: "62" },
      { label: "Weekly Downloads", value: "48k" },
    ],
    repo: "https://github.com/nhut0902/atlas-ui",
    demo: "https://atlas-ui.dev",
    accent: "violet",
  },
  {
    slug: "pulse-rag",
    name: "Pulse RAG",
    tagline: "Self-hosted retrieval engine with one-line deploy",
    description:
      "A retrieval-augmented generation runtime that turns any folder of markdown, PDFs, or code into a queryable knowledge base. Vector store, embeddings, and a streaming API in one binary.",
    tags: ["AI", "Backend", "RAG"],
    category: "ai",
    featured: true,
    year: 2024,
    stack: ["Rust", "Python", "pgvector", "OpenAI"],
    metrics: [
      { label: "Avg. Latency", value: "82ms" },
      { label: "Docs Indexed", value: "1.2M" },
    ],
    repo: "https://github.com/nhut0902/pulse-rag",
    demo: "https://pulse.nhutcoder.team",
    accent: "cyan",
  },
  {
    slug: "kindle-game",
    name: "Kindle",
    tagline: "Narrative adventure built on a custom WebGL engine",
    description:
      "A story-driven isometric puzzle game with hand-drawn art, adaptive music, and a save system synced across devices. Built on a custom TypeScript WebGL2 renderer.",
    tags: ["Game Dev", "WebGL", "TypeScript"],
    category: "games",
    featured: false,
    year: 2024,
    stack: ["TypeScript", "WebGL2", "Howler.js", "Vite"],
    metrics: [
      { label: "Playtime", value: "6 hrs" },
      { label: "Steam Wishlist", value: "8.1k" },
    ],
    repo: "https://github.com/nhut0902/kindle",
    demo: "https://kindle.game",
    accent: "amber",
  },
  {
    slug: "orbit-analytics",
    name: "Orbit Analytics",
    tagline: "Privacy-first, cookie-less web analytics",
    description:
      "A self-hostable analytics platform that respects user privacy — no cookies, no PII, GDPR-by-default. Edge-rendered dashboard with sub-100ms queries.",
    tags: ["Web", "Privacy", "Analytics"],
    category: "web",
    featured: false,
    year: 2024,
    stack: ["Next.js", "ClickHouse", "Cloudflare Workers"],
    metrics: [
      { label: "Events / day", value: "18M" },
      { label: "p95 Query", value: "94ms" },
    ],
    repo: "https://github.com/nhut0902/orbit",
    demo: "https://orbit.nhutcoder.team",
    accent: "lime",
  },
  {
    slug: "scriptforge",
    name: "ScriptForge",
    tagline: "Voice-driven video scripting workspace",
    description:
      "An AI workspace that turns a one-line idea into a structured video script with shot lists, voice-over drafts, and a render queue. Powers the NhutCoder content pipeline.",
    tags: ["AI", "Creator Tools"],
    category: "ai",
    featured: false,
    year: 2023,
    stack: ["Next.js", "OpenAI", "Whisper", "Remotion"],
    metrics: [
      { label: "Scripts / mo", value: "1.4k" },
      { label: "Render Hours", value: "320" },
    ],
    repo: "https://github.com/nhut0902/scriptforge",
    demo: "https://scriptforge.app",
    accent: "violet",
  },
  {
    slug: "linea-commerce",
    name: "Linea Commerce",
    tagline: "Headless storefront starter for Vietnamese SMBs",
    description:
      "A performant headless commerce starter tuned for the Vietnamese market — VNPAY, MoMo, Zalo Pay, and a localized checkout in one deploy.",
    tags: ["Web", "E-commerce"],
    category: "web",
    featured: false,
    year: 2023,
    stack: ["Next.js", "Prisma", "Stripe", "VNPAY"],
    metrics: [
      { label: "Stores Live", value: "47" },
      { label: "GMV / mo", value: "$210k" },
    ],
    repo: "https://github.com/nhut0902/linea",
    demo: "https://linea.nhutcoder.com",
    accent: "cyan",
  },
  {
    slug: "ember-engine",
    name: "Ember Engine",
    tagline: "2D game engine for narrative titles",
    description:
      "A minimalist 2D game engine with a dialogue graph, branching quests, and a hot-reloadable scene format. Open source, MIT-licensed.",
    tags: ["Open Source", "Game Dev"],
    category: "games",
    featured: false,
    year: 2023,
    stack: ["TypeScript", "Canvas", "Web Audio"],
    metrics: [
      { label: "Stars", value: "1.1k" },
      { label: "Forks", value: "84" },
    ],
    repo: "https://github.com/nhut0902/ember-engine",
    demo: "https://ember.nhutcoder.team",
    accent: "amber",
  },
];

export const PROJECT_CATEGORIES = [
  { id: "all", label: "All Work", count: PROJECTS.length },
  {
    id: "ai",
    label: "AI",
    count: PROJECTS.filter((p) => p.category === "ai").length,
  },
  {
    id: "tools",
    label: "Tools",
    count: PROJECTS.filter((p) => p.category === "tools").length,
  },
  {
    id: "libraries",
    label: "Libraries",
    count: PROJECTS.filter((p) => p.category === "libraries").length,
  },
  {
    id: "games",
    label: "Games",
    count: PROJECTS.filter((p) => p.category === "games").length,
  },
  {
    id: "web",
    label: "Web",
    count: PROJECTS.filter((p) => p.category === "web").length,
  },
] as const;

export const SKILLS: Skill[] = [
  { name: "TypeScript", level: 96, group: "Languages", years: 8 },
  { name: "Rust", level: 72, group: "Languages", years: 3 },
  { name: "Python", level: 84, group: "Languages", years: 7 },
  { name: "Go", level: 64, group: "Languages", years: 2 },
  { name: "Next.js", level: 95, group: "Frontend", years: 6 },
  { name: "React", level: 96, group: "Frontend", years: 8 },
  { name: "Tailwind CSS", level: 93, group: "Frontend", years: 5 },
  { name: "WebGL / Three.js", level: 70, group: "Frontend", years: 3 },
  { name: "Node.js", level: 90, group: "Backend", years: 7 },
  { name: "PostgreSQL", level: 84, group: "Backend", years: 6 },
  { name: "Prisma", level: 88, group: "Backend", years: 4 },
  { name: "Redis", level: 76, group: "Backend", years: 4 },
  { name: "OpenAI / LLMs", level: 89, group: "AI", years: 3 },
  { name: "Vector DBs (pgvector)", level: 78, group: "AI", years: 2 },
  { name: "RAG Pipelines", level: 82, group: "AI", years: 2 },
  { name: "Docker / K8s", level: 74, group: "DevOps", years: 5 },
  { name: "CI / CD", level: 86, group: "DevOps", years: 6 },
  { name: "Cloudflare / Vercel", level: 90, group: "DevOps", years: 5 },
];

export const SKILL_GROUPS = [
  "Languages",
  "Frontend",
  "Backend",
  "AI",
  "DevOps",
] as const;

export const TIMELINE: TimelineEntry[] = [
  {
    year: "2025",
    title: "Crossed 5k combined GitHub stars",
    description:
      "Open-source work across Nebula CLI, Atlas UI, and Pulse RAG reached 5,000+ cumulative stars. Started a weekly office-hours stream for contributors.",
    tag: "Milestone",
  },
  {
    year: "2024",
    title: "Shipped Pulse RAG v1",
    description:
      "Released the first stable version of Pulse RAG — a self-hosted retrieval engine now powering internal AI products at three partner companies.",
    tag: "Release",
  },
  {
    year: "2024",
    title: "First AI product launch",
    description:
      "Pulled ScriptForge out of internal tooling and shipped it publicly. The workspace now generates 1,400+ video scripts a month for creators across SEA.",
    tag: "Launch",
  },
  {
    year: "2023",
    title: "Founded NhutCoder Team",
    description:
      "Formalised the collective of three engineers and one designer. Set the mandate: open-source first, AI-native, obsessed with craft.",
    tag: "Founded",
  },
  {
    year: "2022",
    title: "First major open-source release",
    description:
      "Ember Engine — a 2D narrative game engine — hit the front page of Hacker News and crossed 1k stars in its first week.",
    tag: "Release",
  },
  {
    year: "2018",
    title: "Started building in public",
    description:
      'Began publishing tutorials and side projects on GitHub and YouTube. The very first commit message read: "just shipping things."',
    tag: "Origin",
  },
];

export const EXPERIENCE: ExperienceEntry[] = [
  {
    role: "Founder & Principal Engineer",
    company: "NhutCoder Team",
    period: "2023 — Present",
    location: "Ho Chi Minh City, VN",
    summary:
      "Lead a four-person collective shipping open-source tools, AI products, and games. Set technical direction, run architecture reviews, and write the hardest 10% of the code.",
    highlights: [
      "Architected Pulse RAG — 82ms p95 retrieval at 1.2M docs indexed",
      "Grew Atlas UI to 48k weekly downloads across 30+ production apps",
      "Built ScriptForge pipeline that produces 1,400+ video scripts / mo",
    ],
    stack: ["TypeScript", "Rust", "Next.js", "pgvector", "OpenAI"],
  },
  {
    role: "Senior Frontend Engineer",
    company: "Independent Consulting",
    period: "2020 — 2023",
    location: "Remote",
    summary:
      "Advised and contracted with fintech, e-commerce, and creator-economy startups on frontend architecture, performance, and design system maturity.",
    highlights: [
      "Cut Largest Contentful Paint by 47% for a 4M MAU fintech app",
      "Designed and shipped two design systems from scratch",
      "Mentored 12 engineers across four companies",
    ],
    stack: ["React", "Next.js", "Tailwind", "Figma"],
  },
  {
    role: "Full-stack Engineer",
    company: "Vietnamese SaaS Studio",
    period: "2018 — 2020",
    location: "Ho Chi Minh City, VN",
    summary:
      "Built and operated B2B SaaS used by Vietnamese SMBs. Owned the migration from a monolith to a typed service-oriented architecture.",
    highlights: [
      "Migrated 200k-line PHP monolith to a typed Next.js + Node stack",
      "Reduced infrastructure spend by 38% via edge caching",
      "Shipped 14 production features end-to-end",
    ],
    stack: ["Next.js", "Node.js", "PostgreSQL", "Redis"],
  },
];

export const BLOG_POSTS: BlogPost[] = [
  {
    slug: "shipping-fast-without-breaking-things",
    title: "Shipping fast without breaking things",
    excerpt:
      "Our playbook for shipping multiple times a day while keeping production calm. Trunk-based development, deploy previews, and the right amount of typing.",
    date: "2025-02-18",
    readingMinutes: 8,
    category: "Engineering",
    tags: ["Process", "CI/CD", "TypeScript"],
    author: "Nhut Le",
    featured: true,
  },
  {
    slug: "the-rag-stack-we-standardised-on",
    title: "The RAG stack we standardised on",
    excerpt:
      "After six months of building retrieval-augmented products, here's the architecture we landed on — embeddings, vector store, re-ranking, and the boring parts nobody talks about.",
    date: "2025-01-29",
    readingMinutes: 12,
    category: "AI",
    tags: ["RAG", "pgvector", "LLMs"],
    author: "Nhut Le",
    featured: true,
  },
  {
    slug: "design-tokens-actually-worth-shipping",
    title: "Design tokens actually worth shipping",
    excerpt:
      "Most design token systems die in a Figma file. Here's how we structured ours so it survives contact with production — and the engineer who has to use it at 2am.",
    date: "2024-12-11",
    readingMinutes: 9,
    category: "Design Systems",
    tags: ["Design Tokens", "Tailwind", "Figma"],
    author: "Mai Tran",
    featured: false,
  },
  {
    slug: "why-we-wrote-our-own-game-engine",
    title: "Why we wrote our own game engine (and you shouldn't)",
    excerpt:
      "A long answer to a short question. The trade-offs we made building Ember Engine, what we'd do differently, and why we still think it was the right call — for us.",
    date: "2024-11-04",
    readingMinutes: 14,
    category: "Game Dev",
    tags: ["WebGL", "TypeScript", "Architecture"],
    author: "Nhut Le",
    featured: false,
  },
  {
    slug: "edge-first-by-default",
    title: "Edge-first by default",
    excerpt:
      "Running your whole product on the edge is now possible. We break down what's actually worth moving, what isn't, and the latency numbers that changed our minds.",
    date: "2024-10-12",
    readingMinutes: 7,
    category: "Infrastructure",
    tags: ["Cloudflare", "Edge", "Performance"],
    author: "Khoa Nguyen",
    featured: false,
  },
  {
    slug: "open-source-as-a-hiring-funnel",
    title: "Open source as a hiring funnel",
    excerpt:
      "Two of our three engineers came in through open-source contributions. We explain how we structure issues, mentor contributors, and turn pull requests into job offers.",
    date: "2024-09-20",
    readingMinutes: 6,
    category: "Team",
    tags: ["Open Source", "Hiring", "Culture"],
    author: "Nhut Le",
    featured: false,
  },
];

export const BLOG_CATEGORIES = [
  "All",
  "Engineering",
  "AI",
  "Design Systems",
  "Game Dev",
  "Infrastructure",
  "Team",
] as const;

export const TECH_STACK = [
  { name: "TypeScript", category: "Language" },
  { name: "Rust", category: "Language" },
  { name: "Python", category: "Language" },
  { name: "Go", category: "Language" },
  { name: "Next.js", category: "Framework" },
  { name: "React", category: "Framework" },
  { name: "Tailwind CSS", category: "Styling" },
  { name: "Radix UI", category: "Styling" },
  { name: "Node.js", category: "Runtime" },
  { name: "Bun", category: "Runtime" },
  { name: "PostgreSQL", category: "Database" },
  { name: "Prisma", category: "Database" },
  { name: "Redis", category: "Database" },
  { name: "ClickHouse", category: "Database" },
  { name: "OpenAI", category: "AI" },
  { name: "pgvector", category: "AI" },
  { name: "Whisper", category: "AI" },
  { name: "Docker", category: "DevOps" },
  { name: "Kubernetes", category: "DevOps" },
  { name: "Cloudflare", category: "DevOps" },
  { name: "Vercel", category: "DevOps" },
  { name: "GitHub Actions", category: "DevOps" },
  { name: "Figma", category: "Design" },
  { name: "WebGL2", category: "Graphics" },
];

export const STATS = [
  { label: "Combined GitHub stars", value: 5400, suffix: "+" },
  { label: "Weekly downloads", value: 60000, suffix: "+" },
  { label: "Open-source repos", value: 28, suffix: "" },
  { label: "Years shipping", value: 7, suffix: "" },
];
