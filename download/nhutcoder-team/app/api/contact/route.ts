import { NextResponse } from "next/server";
import type { ContactPayload } from "@/types";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Cloudflare D1 binding (injected at runtime on Cloudflare Pages)
interface Env {
  DB: { prepare: (sql: string) => { bind: (...args: any[]) => { run: () => Promise<any> } } };
}

export async function POST(request: Request) {
  let body: ContactPayload;

  try {
    body = (await request.json()) as ContactPayload;
  } catch {
    return NextResponse.json(
      { ok: false, error: "Invalid JSON body" },
      { status: 400 }
    );
  }

  const name = (body.name ?? "").trim();
  const email = (body.email ?? "").trim();
  const message = (body.message ?? "").trim();

  if (!name || name.length < 2) {
    return NextResponse.json(
      { ok: false, error: "Please provide your name." },
      { status: 422 }
    );
  }
  if (!EMAIL_RE.test(email)) {
    return NextResponse.json(
      { ok: false, error: "Please provide a valid email address." },
      { status: 422 }
    );
  }
  if (!message || message.length < 10) {
    return NextResponse.json(
      { ok: false, error: "Please include a message of at least 10 characters." },
      { status: 422 }
    );
  }

  const record = {
    name,
    email,
    company: (body.company ?? "").trim() || "",
    projectType: body.projectType || "",
    budget: body.budget || "",
    message,
    receivedAt: new Date().toISOString(),
  };

  // Try to save to Cloudflare D1
  try {
    const env = (process.env as unknown) as Env;
    if (env.DB) {
      await env.DB.prepare(
        "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)"
      )
        .bind(name, email, message)
        .run();
    }
  } catch {
    console.error("contact: D1 insert failed, continuing without DB");
  }

  // Optional webhook
  const webhook = process.env.CONTACT_WEBHOOK_URL;
  if (webhook) {
    try {
      await fetch(webhook, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(record),
      });
    } catch {
      console.error("contact: webhook delivery failed");
    }
  }

  console.log(`[contact] received submission from ${name} <${email}>`);

  return NextResponse.json({
    ok: true,
    message: "Message received — we'll reply within one business day.",
  });
}

export async function GET() {
  return NextResponse.json({
    ok: true,
    endpoint: "POST /api/contact",
    fields: ["name", "email", "company?", "projectType?", "budget?", "message"],
  });
}
