import { NextResponse } from "next/server";
import { contactSchema } from "@/lib/validation";
import { getDb } from "@/lib/db";
import { contacts } from "@/db/schema";

export const runtime = "edge";

export async function POST(request: Request) {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ ok: false, error: "Invalid JSON" }, { status: 400 });
  }

  const parsed = contactSchema.safeParse(body);
  if (!parsed.success) {
    const firstError = parsed.error.issues[0];
    return NextResponse.json(
      { ok: false, error: firstError?.message || "Validation failed" },
      { status: 422 }
    );
  }

  const { name, email, company, projectType, budget, message } = parsed.data;

  // Save to D1 via Drizzle
  try {
    const db = getDb();
    if (db) {
      await db.insert(contacts).values({
        name,
        email,
        company: company || null,
        projectType: projectType || null,
        budget: budget || null,
        message,
      });
    }
  } catch (e) {
    console.error("[contact] D1 insert failed:", e);
  }

  console.log(`[contact] submission from ${name} <${email}>`);

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
