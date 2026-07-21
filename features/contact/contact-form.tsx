"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { ArrowUpRight, CheckCircle2, Loader2, Send } from "lucide-react";
import { Button, Input, Textarea } from "@marmoui/ui";
import { cn } from "@/lib/utils";

type Status = "idle" | "loading" | "success" | "error";

const PROJECT_TYPES = [
  "Web app",
  "AI product",
  "Open-source tool",
  "Game",
  "Design system",
  "Something else",
];

const BUDGETS = ["< $5k", "$5k – $15k", "$15k – $50k", "$50k+", "Not sure yet"];

export function ContactForm() {
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState<string | null>(null);
  const [projectType, setProjectType] = useState<string>("");
  const [budget, setBudget] = useState<string>("");

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus("loading");
    setError(null);

    const form = e.currentTarget;
    const data = new FormData(form);
    const payload = {
      name: String(data.get("name") ?? "").trim(),
      email: String(data.get("email") ?? "").trim(),
      company: String(data.get("company") ?? "").trim(),
      projectType,
      budget,
      message: String(data.get("message") ?? "").trim(),
    };

    if (!payload.name || !payload.email || !payload.message) {
      setStatus("error");
      setError("Please fill in your name, email, and message.");
      return;
    }

    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        let errorMsg = "Something went wrong. Please try again.";
        try {
          const body = await res.json() as { error?: string };
          if (body?.error) errorMsg = body.error;
        } catch {}
        throw new Error(errorMsg);
      }

      setStatus("success");
      form.reset();
      setProjectType("");
      setBudget("");
    } catch (err) {
      setStatus("error");
      setError(err instanceof Error ? err.message : "Unknown error");
    }
  }

  if (status === "success") {
    return (
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col items-center justify-center rounded-2xl border border-[var(--color-edge)] bg-[var(--color-panel)] p-10 text-center md:p-16"
      >
        <span className="grid h-12 w-12 place-items-center rounded-full border border-[var(--color-brand-500)]/40 bg-[var(--color-brand-500)]/10 text-[var(--color-brand-400)]">
          <CheckCircle2 className="h-6 w-6" />
        </span>
        <h3 className="mt-5 text-2xl font-semibold text-[var(--color-ink-strong)]">
          Message received.
        </h3>
        <p className="mt-2 max-w-md text-sm text-[var(--color-ink-soft)]">
          Thanks for reaching out — we read every message and reply within one
          business day. In the meantime, feel free to poke around our GitHub.
        </p>
        <button
          type="button"
          onClick={() => setStatus("idle")}
          className="mt-6 text-sm font-medium text-[var(--color-brand-400)] hover:text-[var(--color-brand-300)]"
        >
          Send another message
        </button>
      </motion.div>
    );
  }

  return (
    <form
      onSubmit={onSubmit}
      className="rounded-2xl border border-[var(--color-edge)] bg-[var(--color-panel)] p-6 md:p-8"
      noValidate
    >
      <div className="grid gap-5 sm:grid-cols-2">
        <Field label="Your name" htmlFor="name" required>
          <Input
            id="name"
            name="name"
            required
            autoComplete="name"
            placeholder="Jane Doe"
            className="h-11"
          />
        </Field>
        <Field label="Email" htmlFor="email" required>
          <Input
            id="email"
            name="email"
            type="email"
            required
            autoComplete="email"
            placeholder="jane@company.com"
            className="h-11"
          />
        </Field>
        <Field label="Company / team (optional)" htmlFor="company">
          <Input
            id="company"
            name="company"
            autoComplete="organization"
            placeholder="Acme Inc."
            className="h-11"
          />
        </Field>
        <Field label="Project type">
          <div className="flex flex-wrap gap-1.5">
            {PROJECT_TYPES.map((t) => (
              <Chip
                key={t}
                active={projectType === t}
                onClick={() => setProjectType((prev) => (prev === t ? "" : t))}
              >
                {t}
              </Chip>
            ))}
          </div>
        </Field>
      </div>

      <div className="mt-5">
        <Field label="Budget range (optional)">
          <div className="flex flex-wrap gap-1.5">
            {BUDGETS.map((b) => (
              <Chip
                key={b}
                active={budget === b}
                onClick={() => setBudget((prev) => (prev === b ? "" : b))}
              >
                {b}
              </Chip>
            ))}
          </div>
        </Field>
      </div>

      <div className="mt-5">
        <Field label="Tell us about the project" htmlFor="message" required>
          <Textarea
            id="message"
            name="message"
            required
            rows={6}
            placeholder="What are you building, what's the timeline, and what does success look like?"
            className="resize-none"
          />
        </Field>
      </div>

      {error && (
        <p className="mt-4 rounded-lg border border-[oklch(0.6_0.2_25_/_0.4)] bg-[oklch(0.6_0.2_25_/_0.1)] px-3 py-2 text-sm text-[oklch(0.82_0.16_25)]">
          {error}
        </p>
      )}

      <div className="mt-6 flex flex-col items-start gap-3 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-xs text-[var(--color-ink-faint)]">
          By submitting, you agree to be contacted about your enquiry. We never
          share your details.
        </p>
        <Button
          type="submit"
          variant="primary"
          size="md"
          disabled={status === "loading"}
          loading={status === "loading"}
          loadingText="Sending…"
          rightIcon={
            status !== "loading" ? <Send className="h-4 w-4" /> : undefined
          }
        >
          Send message
        </Button>
      </div>
    </form>
  );
}

function Field({
  label,
  htmlFor,
  required,
  children,
}: {
  label: string;
  htmlFor?: string;
  required?: boolean;
  children: React.ReactNode;
}) {
  return (
    <div>
      <label
        htmlFor={htmlFor}
        className="mb-2 block text-sm font-medium text-[var(--color-ink-strong)]"
      >
        {label}
        {required && (
          <span className="ml-1 text-[var(--color-brand-400)]">*</span>
        )}
      </label>
      {children}
    </div>
  );
}

function Chip({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        "rounded-full border px-3 py-1.5 text-xs font-medium transition-colors",
        active
          ? "border-[var(--color-brand-500)] bg-[var(--color-brand-500)]/10 text-[var(--color-brand-300)]"
          : "border-[var(--color-edge)] bg-[var(--color-surface-2)] text-[var(--color-ink-soft)] hover:border-[var(--color-border-hover)] hover:text-[var(--color-ink-strong)]"
      )}
    >
      {children}
    </button>
  );
}

// Tiny utility for the icon usage elsewhere — keeps imports clean.
export function ContactArrowUpRight() {
  return <ArrowUpRight className="h-4 w-4" />;
}

export function ContactLoader() {
  return <Loader2 className="h-4 w-4 animate-spin" />;
}
