import { NextResponse } from "next/server";
import { dbRun, hasDb } from "@/lib/db";
import { generateOTP } from "@/lib/email";

export const runtime = "edge";

export async function POST(request: Request) {
  try {
    const body = (await request.json().catch(() => ({}))) as { email?: string };
    const email = typeof body.email === "string" ? body.email.trim() : "";

    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return NextResponse.json({ ok: false, error: "Email không hợp lệ" }, { status: 422 });
    }

    const code = generateOTP();
    if (hasDb()) {
      const expiresAt = new Date(Date.now() + 30 * 60 * 1000).toISOString();
      await dbRun(
        "INSERT INTO otp_codes (email, code, type, expires_at, used) VALUES (?, ?, 'reset', ?, 0)",
        [email, code, expiresAt]
      );
    }

    return NextResponse.json({
      ok: true,
      message: "Mã đặt lại mật khẩu đã được tạo.",
      code: code,
    });
  } catch (error) {
    console.error("[auth/forgot-password] Error:", error);
    return NextResponse.json({ ok: false, error: "Lỗi server: " + String(error) }, { status: 500 });
  }
}
