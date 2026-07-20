import { NextResponse } from "next/server";
import type { ContactPayload } from "@/types";

// In-memory store for demo purposes — survives across hot reloads
// within a single Node process. Swap for a real DB / queue in production.
const submissionLog: Array<ContactPayload & { receivedAt: string }> = [];

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

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
      {
        ok: false,
        error: "Please include a message of at least 10 characters.",
      },
      { status: 422 }
    );
  }

  const record = {
    name,
    email,
    company: (body.company ?? "").trim() || undefined,
    projectType: body.projectType || undefined,
    budget: body.budget || undefined,
    message,
    receivedAt: new Date().toISOString(),
  };

  submissionLog.push(record);

  // Optional: forward to an external webhook (Slack, Discord, Zapier, Resend…)
  const webhook = process.env.CONTACT_WEBHOOK_URL;
  if (webhook) {
    try {
      await fetch(webhook, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(record),
      });
    } catch {
      // Don't fail the user-facing response if the webhook hiccups
      console.error("contact: webhook delivery failed");
    }
  }

  // Light log for server-side debugging
  console.log(`[contact] received submission from ${name} <${email}>`);

  return NextResponse.json({
    ok: true,
    message: "Message received — we'll reply within one business day.",
  });
}

export async function GET() {
  // Friendly hint for anyone sniffing the endpoint
  return NextResponse.json({
    ok: true,
    endpoint: "POST /api/contact",
    fields: ["name", "email", "company?", "projectType?", "budget?", "message"],
  });
}
