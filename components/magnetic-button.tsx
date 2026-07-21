"use client";

import { forwardRef, type ReactNode } from "react";
import Link from "next/link";
import { cn } from "@/lib/utils";
import { useMagnetic } from "@/hooks/use-magnetic";

interface MagneticButtonProps {
  children: ReactNode;
  href?: string;
  onClick?: () => void;
  className?: string;
  strength?: number;
  radius?: number;
  type?: "button" | "submit";
  ariaLabel?: string;
}

/**
 * MagneticButton — wraps any content in a magnetic-hover shell.
 * Use for primary CTAs where the premium "the cursor pulls the button" feel matters.
 */
export const MagneticButton = forwardRef<HTMLElement, MagneticButtonProps>(
  function MagneticButton(
    {
      children,
      href,
      onClick,
      className,
      strength = 0.4,
      radius = 10,
      type = "button",
      ariaLabel,
    },
    _ref
  ) {
    const innerRef = useMagnetic<HTMLElement>({ strength, radius });

    const cls = cn(
      "relative inline-flex items-center justify-center will-change-transform",
      "transition-[transform] duration-500 [transition-timing-function:cubic-bezier(0.22,1,0.36,1)]",
      className
    );

    if (href) {
      return (
        <Link
          href={href}
          ref={innerRef as React.RefObject<HTMLAnchorElement | null> as never}
          className={cls}
          aria-label={ariaLabel}
        >
          {children}
        </Link>
      );
    }

    return (
      <button
        ref={innerRef as React.RefObject<HTMLButtonElement | null> as never}
        type={type}
        onClick={onClick}
        className={cls}
        aria-label={ariaLabel}
      >
        {children}
      </button>
    );
  }
);
