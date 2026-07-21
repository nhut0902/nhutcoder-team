import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Tailwind-aware className combiner.
 * Falls back to marmoui/ui's `cn` if you'd prefer — both behave identically.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Format a date as e.g. "Mar 12, 2025" — locale-aware.
 */
export function formatDate(date: Date | string, locale = "en-US") {
  const d = typeof date === "string" ? new Date(date) : date;
  return new Intl.DateTimeFormat(locale, {
    year: "numeric",
    month: "short",
    day: "numeric",
  }).format(d);
}

/**
 * Rough reading-time estimate from a markdown/plain string.
 */
export function readingTime(text: string, wpm = 220) {
  const words = text.trim().split(/\s+/).length;
  return Math.max(1, Math.round(words / wpm));
}

/**
 * Clamp helper used by parallax / magnetic hooks.
 */
export function clamp(value: number, min: number, max: number) {
  return Math.min(Math.max(value, min), max);
}

/**
 * Build an absolute URL for SEO when a path is relative.
 */
export function absoluteUrl(
  path = "",
  base = process.env.NEXT_PUBLIC_SITE_URL
) {
  if (!base) return path;
  const root = base.replace(/\/$/, "");
  const tail = path.startsWith("/") ? path : `/${path}`;
  return `${root}${tail}`;
}
