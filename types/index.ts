export type AccentColor = "lime" | "violet" | "cyan" | "amber" | "rose";

export interface ProjectMetric {
  label: string;
  value: string;
}

export interface Project {
  slug: string;
  name: string;
  tagline: string;
  description: string;
  tags: string[];
  category: "ai" | "tools" | "libraries" | "games" | "web";
  featured: boolean;
  year: number;
  stack: string[];
  metrics: ProjectMetric[];
  repo?: string;
  demo?: string;
  accent: AccentColor;
}

export interface Skill {
  name: string;
  level: number; // 0-100
  group: string;
  years: number;
}

export interface TimelineEntry {
  year: string;
  title: string;
  description: string;
  tag: string;
}

export interface ExperienceEntry {
  role: string;
  company: string;
  period: string;
  location: string;
  summary: string;
  highlights: string[];
  stack: string[];
}

export interface BlogPost {
  slug: string;
  title: string;
  excerpt: string;
  date: string; // ISO date
  readingMinutes: number;
  category: string;
  tags: string[];
  author: string;
  featured: boolean;
}

export interface NavItem {
  label: string;
  href: string;
}

export type SocialIcon = "github" | "facebook" | "tiktok";

export interface SocialLink {
  label: string;
  href: string;
  handle: string;
  icon: SocialIcon;
  category: "code" | "social";
}

export interface ContactPayload {
  name: string;
  email: string;
  company?: string;
  budget?: string;
  message: string;
  projectType?: string;
}
