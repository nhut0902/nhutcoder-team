import { cn } from "@/lib/utils";

interface SectionHeadingProps {
  eyebrow?: string;
  title: React.ReactNode;
  description?: React.ReactNode;
  align?: "left" | "center";
  className?: string;
  id?: string;
}

/**
 * SectionHeading — consistent editorial section opener.
 * Uses mono eyebrow + display heading + soft description.
 */
export function SectionHeading({
  eyebrow,
  title,
  description,
  align = "left",
  className,
  id,
}: SectionHeadingProps) {
  return (
    <div
      id={id}
      className={cn(
        "flex flex-col gap-3",
        align === "center" && "items-center text-center",
        className
      )}
    >
      {eyebrow && (
        <div
          className={cn(
            "flex items-center gap-2.5",
            align === "center" && "justify-center"
          )}
        >
          <span className="h-1.5 w-1.5 rounded-full bg-[var(--color-brand-500)]" />
          <span className="label-mono text-[var(--color-brand-400)]">
            {eyebrow}
          </span>
        </div>
      )}
      <h2 className="max-w-3xl text-balance text-3xl font-semibold leading-[1.1] tracking-tight md:text-4xl lg:text-[2.75rem]">
        {title}
      </h2>
      {description && (
        <p
          className={cn(
            "max-w-2xl text-pretty text-base leading-relaxed text-[var(--color-ink-soft)] md:text-[17px]",
            align === "center" && "mx-auto"
          )}
        >
          {description}
        </p>
      )}
    </div>
  );
}
