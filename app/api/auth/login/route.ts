import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";
import { users } from "@/db/schema";
import { z } from "zod";

export const runtime = "edge";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(6),
});

export async function POST(request: Request) {
  const body = await request.json().catch(() => ({}));
  const parsed = schema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json({ ok: false, error: "Invalid input" }, { status: 422 });
  }

  const { email, password } = parsed.data;

  // Simple JWT-like token (not production-grade — use proper JWT in production)
  const token = btoa(JSON.stringify({ email, name: email.split("@")[0], iat: Date.now() }));

  // Try to save to D1 if available
  try {
    const db = getDb();
    if (db) {
      // In production: verify password hash, check user exists
      // For now: just return token
    }
  } catch (e) {
    console.error("[auth/login] D1 error:", e);
  }

  return NextResponse.json({ ok: true, token, user: { email, name: email.split("@")[0] } });
}
