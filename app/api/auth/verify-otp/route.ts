import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";
import { users } from "@/db/schema";
import { eq } from "drizzle-orm";
import { verifyOTP } from "@/lib/email";
import { z } from "zod";

export const runtime = "edge";

const schema = z.object({
  email: z.string().email(),
  otp: z.string().length(6),
});

export async function POST(request: Request) {
  const body = await request.json().catch(() => ({}));
  const parsed = schema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json({ ok: false, error: "Email và mã OTP 6 số là bắt buộc" }, { status: 422 });
  }

  const { email, otp } = parsed.data;

  // Verify OTP from D1
  const valid = await verifyOTP(email, otp);
  if (!valid) {
    return NextResponse.json(
      { ok: false, error: "Mã OTP không đúng hoặc đã hết hạn" },
      { status: 400 }
    );
  }

  // Mark user as verified in D1
  try {
    const db = getDb();
    if (db) {
      await db.update(users)
        .set({ verified: true })
        .where(eq(users.email, email));

      // Get user data
      const userRecords = await db.select().from(users).where(eq(users.email, email)).limit(1);
      if (userRecords.length > 0) {
        const user = userRecords[0];
        const token = btoa(JSON.stringify({
          id: user.id,
          name: user.name,
          email: user.email,
          verified: true,
          iat: Date.now(),
        }));
        return NextResponse.json({ ok: true, token, user: { name: user.name, email: user.email } });
      }
    }
  } catch (e) {
    console.error("[auth/verify-otp] D1 error:", e);
  }

  // Fallback: return token even if D1 update failed
  const token = btoa(JSON.stringify({ email, name: email.split("@")[0], verified: true, iat: Date.now() }));
  return NextResponse.json({ ok: true, token, user: { email, name: email.split("@")[0] } });
}
