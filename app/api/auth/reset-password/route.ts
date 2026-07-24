import { NextResponse } from "next/server";
import { dbRun, hasDb } from "@/lib/db";

export const runtime = "edge";

export async function POST(request: Request) {
  try {
    const body = (await request.json().catch(() => ({}))) as { email?: string; newPassword?: string };
    const email = typeof body.email === "string" ? body.email.trim() : "";
    const newPassword = typeof body.newPassword === "string" ? body.newPassword : "";

    if (!email || !newPassword || newPassword.length < 6) {
      return NextResponse.json({ ok: false, error: "Email và mật khẩu mới (6+ ký tự) là bắt buộc" }, { status: 422 });
    }

    const passwordHash = btoa(newPassword);

    if (hasDb()) {
      await dbRun("UPDATE users SET password_hash = ? WHERE email = ?", [passwordHash, email]);
    }

    return NextResponse.json({ ok: true, message: "Đặt lại mật khẩu thành công" });
  } catch (error) {
    console.error("[auth/reset-password] Error:", error);
    return NextResponse.json({ ok: false, error: "Lỗi server: " + String(error) }, { status: 500 });
  }
}
