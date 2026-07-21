"use client";

import { useTheme } from "next-themes";
import { Moon, Sun } from "lucide-react";
import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";

/**
 * Minimal, premium theme toggle. Defaults to dark mode.
 * Avoids hydration mismatch by rendering a placeholder until mounted.
 */
export function ThemeToggle({ className }: { className?: string }) {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);

  const isDark = theme === "dark";

  return (
    <button
      type="button"
      aria-label={isDark ? "Switch to light theme" : "Switch to dark theme"}
      onClick={() => setTheme(isDark ? "light" : "dark")}
      className={cn(
        "group relative inline-flex h-9 w-9 items-center justify-center rounded-full",
        "border border-[var(--color-border)] bg-[var(--color-panel)]",
        "text-[var(--color-ink-soft)] hover:text-[var(--color-ink-strong)]",
        "transition-colors duration-300 hover:border-[var(--color-border-hover)]",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-brand-500)] focus-visible:ring-offset-2 focus-visible:ring-offset-[var(--color-bg)]",
        className
      )}
    >
      {!mounted ? (
        <span className="block h-4 w-4" />
      ) : isDark ? (
        <Sun className="h-4 w-4 transition-transform duration-500 group-hover:rotate-45" />
      ) : (
        <Moon className="h-4 w-4 transition-transform duration-500 group-hover:-rotate-12" />
      )}
    </button>
  );
}
