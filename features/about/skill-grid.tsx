"use client";

import { motion } from "framer-motion";
import { SKILLS, SKILL_GROUPS } from "@/lib/data";
import { cn } from "@/lib/utils";

/**
 * SkillGrid — visualises skill levels with an animated bar chart.
 */
export function SkillGrid() {
  return (
    <div className="space-y-10">
      {SKILL_GROUPS.map((group, gi) => {
        const items = SKILLS.filter((s) => s.group === group);
        return (
          <div key={group}>
            <div className="mb-4 flex items-baseline justify-between border-b border-[var(--color-edge)] pb-2">
              <h3 className="font-display text-lg font-semibold text-[var(--color-ink-strong)]">
                {group}
              </h3>
              <span className="font-mono text-xs text-[var(--color-ink-faint)]">
                {items.length} skills
              </span>
            </div>
            <div className="grid gap-x-8 gap-y-5 sm:grid-cols-2">
              {items.map((skill, i) => (
                <SkillBar
                  key={skill.name}
                  skill={skill}
                  delay={gi * 0.05 + i * 0.04}
                />
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function SkillBar({
  skill,
  delay = 0,
}: {
  skill: { name: string; level: number; years: number };
  delay?: number;
}) {
  return (
    <div className="group">
      <div className="flex items-baseline justify-between">
        <span className="text-sm font-medium text-[var(--color-ink-strong)]">
          {skill.name}
        </span>
        <span className="font-mono text-xs text-[var(--color-ink-faint)]">
          {skill.years}y · {skill.level}%
        </span>
      </div>
      <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-[var(--color-surface-3)]">
        <motion.div
          className={cn(
            "h-full rounded-full bg-gradient-to-r from-[var(--color-brand-500)] to-[var(--color-brand-300)]"
          )}
          initial={{ width: 0 }}
          whileInView={{ width: `${skill.level}%` }}
          viewport={{ once: true, margin: "-10% 0px" }}
          transition={{ duration: 0.9, delay, ease: [0.22, 1, 0.36, 1] }}
        />
      </div>
    </div>
  );
}
