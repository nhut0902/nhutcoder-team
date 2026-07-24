import { NextResponse } from "next/server";
import { dbQuery, hasDb } from "@/lib/db";

export const runtime = "edge";

export async function POST(request: Request) {
  try {
    const body = (await request.json().catch(() => ({}))) as Record<string, unknown>;
    const email = typeof body.email === "string" ? body.email.trim() : "";
    const password = typeof body.password === "string" ? body.password : "";

    if (!email || !password) {
      return NextResponse.json({ ok: false, error: "Thiếu email hoặc mật khẩu" }, { status: 422 });
    }

    const passwordHash = btoa(password);

    if (!hasDb()) {
      // No DB — return token anyway for testing
      const token = btoa(JSON.stringify({ email, name: email.split("@")[0], iat: Date.now() }));
      return NextResponse.json({ ok: true, token, user: { name: email.split("@")[0], email } });
    }

    // Find user
    const users = await dbQuery(
      "SELECT id, name, email, password_hash, verified FROM users WHERE email = ? LIMIT 1",
      [email]
    );

    if (users.length === 0) {
      return NextResponse.json({ ok: false, error: "Email chưa đăng ký" }, { status: 404 });
    }

    const user = users[0];
    if (user.password_hash !== passwordHash) {
      return NextResponse.json({ ok: false, error: "Mật khẩu không đúng" }, { status: 401 });
    }

    if (!user.verified) {
      return NextResponse.json({ ok: false, error: "Tài khoản chưa xác thực" }, { status: 403 });
    }

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
  } catch (error) {
    console.error("[auth/login] Error:", error);
    return NextResponse.json(
      { ok: false, error: "Lỗi server: " + String(error) },
      { status: 500 }
    );
  }
}
