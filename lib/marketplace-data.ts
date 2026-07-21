// Marketplace product data — local JSON data source

export interface Product {
  slug: string;
  name: string;
  tagline: string;
  description: string;
  features: string[];
  technologies: string[];
  version: string;
  price: number;
  category: string;
  thumbnail: string;
  demoUrl: string;
  githubUrl: string;
  changelog: { version: string; date: string; changes: string[] }[];
  featured: boolean;
}

export const PRODUCTS: Product[] = [
  {
    slug: "prism-run",
    name: "Prism Run",
    tagline: "Neon-drenched endless runner game",
    description: "A complete mobile-first HTML5 endless runner with 3D-style graphics, 5 game modes, 6 characters, boss battles, achievements, and full PWA support. Built with Phaser 3 + TypeScript + Vite.",
    features: ["5 game modes", "6 unlockable characters", "Boss battles every 5 waves", "Achievement system (12 badges)", "Daily rewards with streak", "PWA installable", "Touch controls", "Procedural audio system"],
    technologies: ["Phaser 3", "TypeScript", "Vite", "PWA", "Web Audio API"],
    version: "1.0.0",
    price: 49,
    category: "Game",
    thumbnail: "🎮",
    demoUrl: "https://prism-run.vercel.app",
    githubUrl: "https://github.com/nhut0902/prism-run",
    changelog: [
      { version: "1.0.0", date: "2026-07-17", changes: ["Initial release", "5 game modes", "6 characters", "Boss battle system", "Achievement system"] },
    ],
    featured: true,
  },
  {
    slug: "zombie-escape",
    name: "Zombie Escape",
    tagline: "3D zombie survival shooter",
    description: "Mobile-first 3D zombie survival shooter built with Three.js. Features 6 zombie types, 3 weapons, wave-based survival, procedural audio, and PWA support.",
    features: ["3D graphics (Three.js)", "6 zombie types with AI", "3 weapons (pistol/rifle/shotgun)", "Wave-based survival", "Boss zombies", "Procedural audio", "PWA installable", "Touch controls"],
    technologies: ["Three.js", "Vite", "PWA", "Web Audio API", "WebGL"],
    version: "1.0.0",
    price: 59,
    category: "Game",
    thumbnail: "🧟",
    demoUrl: "https://zombie-escape.vercel.app",
    githubUrl: "https://github.com/nhut0902/zombie-escape",
    changelog: [
      { version: "1.0.0", date: "2026-07-18", changes: ["Initial release", "6 zombie types", "3 weapons", "Wave system", "Real 3D models"] },
    ],
    featured: true,
  },
  {
    slug: "html-playground",
    name: "HTML Playground",
    tagline: "Online HTML/CSS/JS editor",
    description: "A mobile-first HTML/CSS/JS editor with live preview, 15 templates, console panel, theme toggle, and share via URL. Single HTML file — zero dependencies.",
    features: ["Live preview iframe", "15 built-in templates", "Console output panel", "Dark/light theme", "Share via URL", "Auto-save", "Line numbers", "Format code", "Download HTML", "Copy to clipboard"],
    technologies: ["Vanilla JS", "PWA", "Web Audio API"],
    version: "1.1.0",
    price: 0,
    category: "Tool",
    thumbnail: "⚡",
    demoUrl: "https://html-playground.vercel.app",
    githubUrl: "https://github.com/nhut0902/html-playground",
    changelog: [
      { version: "1.1.0", date: "2026-07-19", changes: ["Added console panel", "Added 7 more templates", "Added theme toggle", "Added line numbers"] },
      { version: "1.0.0", date: "2026-07-18", changes: ["Initial release", "8 templates", "Live preview", "Share via URL"] },
    ],
    featured: true,
  },
  {
    slug: "subway-surfers-web",
    name: "Subway Surfers Web",
    tagline: "3D WebGL endless runner",
    description: "A Subway Surfers-style 3D endless runner that runs entirely in the browser. WebGL 2.0 with real 3D models, player + police chaser, trains, coins, and background music.",
    features: ["WebGL 2.0 rendering", "Real 3D models (GLB)", "Player + police chaser", "Trains, barriers, coins", "Power-ups", "Background music", "Keyboard + touch controls", "23MB assets included"],
    technologies: ["WebGL 2.0", "Vanilla JS", "GLB models"],
    version: "1.0.0",
    price: 39,
    category: "Game",
    thumbnail: "🚇",
    demoUrl: "https://subway-surfers-web.vercel.app",
    githubUrl: "https://github.com/nhut0902/subway-surfers-web",
    changelog: [
      { version: "1.0.0", date: "2026-07-18", changes: ["Initial release", "WebGL 2.0", "Real 3D models", "Touch controls"] },
    ],
    featured: false,
  },
  {
    slug: "candy-world",
    name: "Candy World",
    tagline: "2D pixel-art platformer",
    description: "A complete 2D pixel-art platformer game with 3 levels, boss battles, 7 abilities, touch controls, and procedural pixel-art textures. Built with Phaser 3.",
    features: ["3 levels with progression", "Boss battle (Sour King)", "7 player abilities", "Touch controls (virtual joystick)", "29 collectibles", "Procedural pixel-art (no external assets)", "Save system", "60 FPS target"],
    technologies: ["Phaser 3", "TypeScript", "Vite", "PWA"],
    version: "2.0.0",
    price: 29,
    category: "Game",
    thumbnail: "🍬",
    demoUrl: "https://candy-world.vercel.app",
    githubUrl: "https://github.com/nhut0902/candy-world",
    changelog: [
      { version: "2.0.0", date: "2026-07-17", changes: ["3 levels", "Boss battle", "Touch controls", "Mobile optimizations"] },
    ],
    featured: false,
  },
  {
    slug: "nhutcoder-team-website",
    name: "NhutCoder Team Website",
    tagline: "Premium portfolio + marketplace template",
    description: "This very website — a production-grade Next.js 16 portfolio with blog, code marketplace, auth system, D1 database, and Cloudflare Workers deployment. Built with Marmo UI + Framer Motion.",
    features: ["Next.js 16 App Router", "Marmo UI components", "Blog system with markdown", "Code marketplace", "Auth system", "Cloudflare D1 + Drizzle ORM", "OpenNext deployment", "SEO optimized", "Dark theme", "Framer Motion animations"],
    technologies: ["Next.js 16", "TypeScript", "Tailwind CSS 4", "Marmo UI", "Framer Motion", "Drizzle ORM", "Cloudflare D1"],
    version: "2.0.0",
    price: 99,
    category: "Template",
    thumbnail: "🌐",
    demoUrl: "https://nhutcoder-team.workers.dev",
    githubUrl: "https://github.com/nhut0902/nhutcoder-team",
    changelog: [
      { version: "2.0.0", date: "2026-07-21", changes: ["Blog system", "Code marketplace", "Auth system", "Dashboard", "Cloudflare Workers deploy"] },
      { version: "1.0.0", date: "2026-07-20", changes: ["Initial release", "5 pages", "Marmo UI", "Framer Motion"] },
    ],
    featured: true,
  },
];

export const PRODUCT_CATEGORIES = ["All", "Game", "Tool", "Template"];

export function getFeaturedProducts(): Product[] {
  return PRODUCTS.filter(p => p.featured);
}

export function getProductBySlug(slug: string): Product | undefined {
  return PRODUCTS.find(p => p.slug === slug);
}

export function getProductsByCategory(category: string): Product[] {
  if (category === "All") return PRODUCTS;
  return PRODUCTS.filter(p => p.category === category);
}

export function searchProducts(query: string): Product[] {
  const q = query.toLowerCase();
  return PRODUCTS.filter(p =>
    p.name.toLowerCase().includes(q) ||
    p.tagline.toLowerCase().includes(q) ||
    p.description.toLowerCase().includes(q) ||
    p.technologies.some(t => t.toLowerCase().includes(q))
  );
}
