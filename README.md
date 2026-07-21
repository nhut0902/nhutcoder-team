# NhutCoder Team

> Building the future with code and AI.

A production-grade marketing & portfolio website for **NhutCoder Team** — an
independent developer collective shipping open-source tools, AI products, and
immersive web & game experiences.

The site is built with **Next.js 16 (App Router)**, **TypeScript**,
**Tailwind CSS 4**, **Framer Motion**, **Lucide icons**, and the
**[@marmoui/ui](https://www.npmjs.com/package/@marmoui/ui)** component
library. The design language is intentionally editorial and dark-first —
inspired by Linear, Raycast, Stripe, and Cloudflare.

---

## ✨ Highlights

- **Five routes** — Home, Projects (filterable grid), About (story + skills),
  Blog (post list with categories), Contact (validated form posting to an
  API route).
- **Premium motion** — page transitions, scroll-reveal, parallax hero,
  magnetic buttons, cursor glow, animated counters, scroll-driven timeline,
  marquee.
- **Hand-crafted design system** — custom OKLCH palette (electric lime +
  neon violet), Geist font via `next/font`, custom scrollbar, noise + grid
  backgrounds, hairline dividers, mono labels.
- **Marmo UI components** — `Button`, `Badge`, `Card`, `Input`, `Textarea`,
  `Avatar`, `Tabs`, etc. Custom components only where Marmo UI doesn't ship
  one (e.g. `AuroraBackground`, `MagneticButton`, `ScrollReveal`).
- **SEO-ready** — full metadata, `app/sitemap.ts`, `app/robots.ts`,
  `app/manifest.ts`, dynamic `app/opengraph-image.tsx` (1200×630 PNG),
  `app/icon.tsx`, `app/apple-icon.tsx`, Twitter Card, Open Graph.
- **Edge-rendered OG image** — branded 1200×630 PNG generated on the fly via
  `next/og`.
- **Production headers** — `X-Content-Type-Options`, `X-Frame-Options`,
  `Referrer-Policy`, `Permissions-Policy`.
- **Zero TypeScript errors, zero ESLint errors, zero ESLint warnings.**

---

## 🧱 Tech Stack

| Concern         | Choice                                        |
| --------------- | --------------------------------------------- |
| Framework       | Next.js 16 (App Router, Turbopack)            |
| Language        | TypeScript 5                                  |
| Styling         | Tailwind CSS 4 + `@marmoui/ui` 2.0.1          |
| Fonts           | Geist Sans / Geist Mono via `next/font`       |
| Animation       | Framer Motion 12                              |
| Icons           | `lucide-react`                                |
| Theming         | `next-themes` (dark-first, `.class` strategy) |
| Linting         | ESLint 9 (flat config) + `eslint-config-next` |
| Package manager | npm                                           |

---

## 🚀 Getting Started

```bash
# 1. Install dependencies
npm install

# 2. Copy the env example (optional — the site runs without it)
cp .env.example .env.local

# 3. Start the dev server
npm run dev
# → http://localhost:3000

# 4. Production build
npm run build
npm run start
```

### Requirements

- Node.js ≥ 20 (tested on Node 24)
- npm ≥ 10

---

## 📁 Project Structure

```
nhutcoder-team/
├─ app/                          # App Router routes
│  ├─ layout.tsx                 # Root layout, fonts, providers, metadata
│  ├─ page.tsx                   # Home
│  ├─ globals.css                # Tailwind + Marmo UI + custom theme
│  ├─ not-found.tsx              # Custom 404
│  ├─ opengraph-image.tsx        # Edge-rendered OG image (1200×630)
│  ├─ icon.tsx                   # Dynamic favicon
│  ├─ apple-icon.tsx             # Apple touch icon
│  ├─ manifest.ts                # Web manifest
│  ├─ robots.ts                  # robots.txt (route)
│  ├─ sitemap.ts                 # sitemap.xml (route)
│  ├─ projects/page.tsx
│  ├─ about/page.tsx
│  ├─ blog/page.tsx
│  ├─ contact/page.tsx
│  └─ api/contact/route.ts       # Contact form endpoint
├─ components/                   # Shared building blocks
│  ├─ aurora-background.tsx
│  ├─ cursor-glow.tsx
│  ├─ footer.tsx
│  ├─ logo.tsx
│  ├─ magnetic-button.tsx
│  ├─ navbar.tsx
│  ├─ page-transition.tsx
│  ├─ scroll-progress.tsx
│  ├─ scroll-reveal.tsx
│  ├─ section-heading.tsx
│  ├─ theme-provider.tsx
│  └─ theme-toggle.tsx
├─ features/                     # Page-scoped feature modules
│  ├─ home/                      # hero, featured-projects, technology, …
│  ├─ projects/                  # project-card, project-explorer
│  ├─ about/                     # skill-grid
│  ├─ blog/                      # blog-card, blog-list
│  └─ contact/                   # contact-form
├─ hooks/                        # use-mouse-position, use-magnetic, …
├─ lib/                          # data.ts (content), utils.ts (helpers)
├─ types/                        # shared TypeScript types
├─ public/                       # static assets (icon.svg)
├─ next.config.ts
├─ tsconfig.json
├─ eslint.config.mjs             # flat config
├─ postcss.config.mjs
├─ wrangler.toml             # Cloudflare Pages config
└─ .env.example
```

---

## 🎨 Design System

### Color Tokens

The palette is defined in OKLCH inside `app/globals.css` under `@theme`:

- **Brand (lime)** — `--color-brand-50` → `--color-brand-950`
- **Accent (violet)** — `--color-accent-300` → `--color-accent-600`
- **Surfaces** — `--color-surface-0` (deepest) → `--color-surface-3`
- **Ink** — `--color-ink-strong` / `--color-ink-soft` / `--color-ink-faint`
- **Edges** — `--color-edge` / `--color-edge-strong`

These override Marmo UI's `--color-bg`, `--color-panel`, `--color-ink`,
`--color-border`, and primary tokens so every Marmo component picks up the
brand palette automatically.

### Typography

- **Display + Sans** — Geist Sans (variable, via `next/font`)
- **Mono** — Geist Mono (variable, via `next/font`)

All headings use `var(--font-display)` with `-0.025em` tracking.

### Motion

- Easing tokens: `--ease-premium` (`cubic-bezier(0.22, 1, 0.36, 1)`) and
  `--ease-emphasized` (`cubic-bezier(0.32, 0.72, 0, 1)`)
- `prefers-reduced-motion` is honoured globally — animations collapse to
  near-instant transitions.

---

## 📨 Contact API

`POST /api/contact` accepts JSON:

```ts
{
  name: string;            // required, ≥ 2 chars
  email: string;           // required, valid email
  company?: string;
  projectType?: string;    // "Web app" | "AI product" | "Game" | …
  budget?: string;         // "< $5k" | "$5k – $15k" | …
  message: string;         // required, ≥ 10 chars
}
```

Returns `{ ok: true, message: string }` on success or
`{ ok: false, error: string }` with the appropriate HTTP status on failure.

By default, submissions are logged server-side. Set `CONTACT_WEBHOOK_URL` in
`.env.local` to also forward each submission to Slack / Discord / Zapier /
Resend / your own backend.

---

## 🔌 Environment Variables

See [`.env.example`](./.env.example) for the full list. Summary:

| Variable                      | Required | Description                                 |
| ----------------------------- | -------- | ------------------------------------------- |
| `NEXT_PUBLIC_SITE_URL`        | no       | Canonical URL used for SEO / OG / sitemap.  |
| `NEXT_PUBLIC_GITHUB_USERNAME` | no       | GitHub handle surfaced in the UI.           |
| `CONTACT_WEBHOOK_URL`         | no       | Optional webhook to forward submissions to. |
| `CONTACT_EMAIL_TO`            | no       | Address you want enquiries routed to.       |
| `CONTACT_EMAIL_FROM`          | no       | `From:` address for outbound emails.        |

---

## ♿ Accessibility

- Semantic landmarks (`header`, `main`, `footer`, `nav`).
- "Skip to content" link visible on focus.
- All interactive elements are keyboard accessible with visible focus rings.
- `aria-label`s on icon-only buttons.
- `prefers-reduced-motion` respected.
- Color contrast meets WCAG AA on the dark surface.

---

## ⚡ Performance

- Tailwind 4 + Turbopack for fast builds.
- `next/font` self-hosts Geist — no Google Fonts request.
- `optimizePackageImports` enabled for `lucide-react` and `framer-motion`.
- Static generation for all top-level routes; only the OG image, icon, and
  contact API run on demand.
- Headers set `X-Content-Type-Options`, `X-Frame-Options`, etc.

---

## 🧪 Scripts

| Script              | Description                            |
| ------------------- | -------------------------------------- |
| `npm run dev`       | Start Next.js dev server on port 3000. |
| `npm run build`     | Production build.                      |
| `npm run start`     | Run the production build.              |
| `npm run lint`      | ESLint (flat config).                  |
| `npm run typecheck` | `tsc --noEmit` type check.             |

---

## ☁️ Deploying to Cloudflare Pages

This repository is Cloudflare-ready:

### Option A: Cloudflare Dashboard
1. Push to GitHub.
2. Go to [Cloudflare Dashboard](https://dash.cloudflare.com) → Pages → Create a project.
3. Connect your GitHub repo.
4. Framework preset: **Next.js**.
5. Build command: `npm run build`
6. Output directory: `.next/static`
7. Add env vars from `.env.example`.
8. Deploy.

### Option B: Wrangler CLI
```bash
npm install -g wrangler
wrangler login
wrangler pages deploy .next/static --project-name=nhutcoder-team
```

### Cloudflare D1 Database
```bash
# Create D1 database
wrangler d1 create nhutcoder-team-db

# Apply schema
wrangler d1 execute nhutcoder-team-db --file=db/schema.sql

# Run locally
wrangler pages dev .next/static --d1=DB
```

`wrangler.toml` pins the D1 database binding, KV cache, and build config.

---

## 📝 License

Source code: **MIT** — see [LICENSE](./LICENSE).

Brand assets (logo, wordmark) are © NhutCoder Team and not covered by the MIT
license.

---

## 🔗 Links

- **GitHub** — <https://github.com/nhut0902>
- **Facebook** — Nhutcoder Team
- **TikTok** — @nhutcoderlamcontent

---

Built with care in Ho Chi Minh City, Vietnam.
