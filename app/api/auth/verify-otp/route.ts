import { NextResponse } from "next/server";
import { dbQuery, dbRun, hasDb } from "@/lib/db";
import { verifyOTPCode } from "@/lib/email";

export const runtime = "edge";

export async function POST(request: Request) {
  try {
    const body = (await request.json().catch(() => ({}))) as Record<string, unknown>;
    const email = typeof body.email === "string" ? body.email.trim() : "";
    const otp = typeof body.otp === "string" ? body.otp.trim() : "";

    if (!email || !otp) {
      return NextResponse.json({ ok: false, error: "Thiếu email hoặc mã OTP" }, { status: 422 });
    }

    // Verify OTP
    if (hasDb()) {
      const valid = await verifyOTPCode(email, otp);
      if (!valid) {
        return NextResponse.json({ ok: false, error: "Mã OTP không đúng hoặc đã hết hạn" }, { status: 400 });
      }

      // Mark user as verified
      await dbRun("UPDATE users SET verified = 1 WHERE email = ?", [email]);

      // Get user
      const users = await dbQuery("SELECT id, name, email FROM users WHERE email = ? LIMIT 1", [email]);
      if (users.length > 0) {
        const user = users[0];
        const token = btoa(JSON.stringify({
          id: user.id, name: user.name, email: user.email, iat: Date.now()
        }));
        return NextResponse.json({ ok: true, token, user: { name: user.name, email: user.email } });
      }
    }

    // Fallback
    const token = btoa(JSON.stringify({ email, name: email.split("@")[0], iat: Date.now() }));
    return NextResponse.json({ ok: true, token, user: { email, name: email.split("@")[0] } });
  } catch (error) {
    console.error("[auth/verify-otp] Error:", error);
    return NextResponse.json({ ok: false, error: "Lỗi server: " + String(error) }, { status: 500 });
  }
}
