import { NextResponse } from "next/server";
import { dbQuery, dbRun, hasDb } from "@/lib/db";
import { generateOTP, storeOTP } from "@/lib/email";

export const runtime = "edge";

export async function POST(request: Request) {
  try {
    const body = (await request.json().catch(() => ({}))) as Record<string, unknown>;
    const name = typeof body.name === "string" ? body.name.trim() : "";
    const email = typeof body.email === "string" ? body.email.trim() : "";
    const password = typeof body.password === "string" ? body.password : "";

    // Validate
    if (!name || name.length < 2) {
      return NextResponse.json({ ok: false, error: "Tên phải có ít nhất 2 ký tự" }, { status: 422 });
    }
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return NextResponse.json({ ok: false, error: "Email không hợp lệ" }, { status: 422 });
    }
    if (!password || password.length < 6) {
      return NextResponse.json({ ok: false, error: "Mật khẩu phải có ít nhất 6 ký tự" }, { status: 422 });
    }

    const passwordHash = btoa(password);

    // Check existing user
    if (hasDb()) {
      const existing = await dbQuery("SELECT id FROM users WHERE email = ? LIMIT 1", [email]);
      if (existing.length > 0) {
        return NextResponse.json({ ok: false, error: "Email đã được đăng ký" }, { status: 409 });
      }
    }

    // Insert user
    if (hasDb()) {
      await dbRun(
        "INSERT INTO users (name, email, password_hash, verified) VALUES (?, ?, ?, 0)",
        [name, email, passwordHash]
      );
    }

    // Generate + store OTP
    const otp = generateOTP();
    if (hasDb()) {
      await storeOTP(email, otp, "register");
    }

    return NextResponse.json({
      ok: true,
      message: "Đăng ký thành công! Mã OTP đã được tạo.",
      otp: otp, // Return OTP directly (no email sending on Workers)
    });
  } catch (error) {
    console.error("[auth/register] Error:", error);
    return NextResponse.json(
      { ok: false, error: "Lỗi server: " + String(error) },
      { status: 500 }
    );
  }
}
