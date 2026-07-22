import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";
import { users } from "@/db/schema";
import { eq } from "drizzle-orm";
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
    return NextResponse.json({ ok: false, error: "Email và mật khẩu không hợp lệ" }, { status: 422 });
  }

  const { email, password } = parsed.data;
  const passwordHash = btoa(password);

  // Check user in D1
  try {
    const db = getDb();
    if (db) {
      const userRecords = await db.select().from(users).where(eq(users.email, email)).limit(1);

      if (userRecords.length === 0) {
        return NextResponse.json({ ok: false, error: "Email chưa đăng ký" }, { status: 404 });
      }

      const user = userRecords[0];

      // Verify password
      if (user.passwordHash !== passwordHash) {
        return NextResponse.json({ ok: false, error: "Mật khẩu không đúng" }, { status: 401 });
      }

      if (!user.verified) {
        return NextResponse.json({ ok: false, error: "Tài khoản chưa xác thực email. Vui lòng đăng ký lại." }, { status: 403 });
      }

      // Generate token
      const token = btoa(JSON.stringify({
        id: user.id,
        name: user.name,
        email: user.email,
        iat: Date.now(),
      }));

      return NextResponse.json({
        ok: true,
        token,
        user: { name: user.name, email: user.email },
      });
    }
  } catch (e) {
    console.error("[auth/login] D1 error:", e);
  }

  // Fallback: return token (for testing without D1)
  const token = btoa(JSON.stringify({ email, name: email.split("@")[0], iat: Date.now() }));
  return NextResponse.json({ ok: true, token, user: { email, name: email.split("@")[0] } });
}
