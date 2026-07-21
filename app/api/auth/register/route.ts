import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";
import { users } from "@/db/schema";
import { z } from "zod";

export const runtime = "edge";

const schema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  password: z.string().min(6),
});

export async function POST(request: Request) {
  const body = await request.json().catch(() => ({}));
  const parsed = schema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json({ ok: false, error: parsed.error.issues[0]?.message || "Invalid input" }, { status: 422 });
  }

  const { name, email, password } = parsed.data;

  // Simple token (NOT production-grade — use proper JWT + bcrypt in production)
  const token = btoa(JSON.stringify({ name, email, iat: Date.now() }));

  // Try to save user to D1
  try {
    const db = getDb();
    if (db) {
      await db.insert(users).values({
        name,
        email,
        passwordHash: btoa(password), // NOT secure — use bcrypt in production
      }).onConflictDoNothing();
    }
  } catch (e) {
    console.error("[auth/register] D1 error:", e);
  }

  return NextResponse.json({ ok: true, token, user: { name, email } });
}
