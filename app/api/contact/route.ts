import { NextResponse } from "next/server";
import { dbRun, hasDb } from "@/lib/db";

export const runtime = "edge";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export async function POST(request: Request) {
  try {
    const body = (await request.json().catch(() => ({}))) as Record<string, unknown>;
    const name = typeof body.name === "string" ? body.name.trim() : "";
    const email = typeof body.email === "string" ? body.email.trim() : "";
    const message = typeof body.message === "string" ? body.message.trim() : "";

    if (!name || name.length < 2) {
      return NextResponse.json({ ok: false, error: "Tên quá ngắn" }, { status: 422 });
    }
    if (!EMAIL_RE.test(email)) {
      return NextResponse.json({ ok: false, error: "Email không hợp lệ" }, { status: 422 });
    }
    if (!message || message.length < 10) {
      return NextResponse.json({ ok: false, error: "Tin nhắn quá ngắn" }, { status: 422 });
    }

    if (hasDb()) {
      await dbRun(
        "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
        [name, email, message]
      );
    }

    return NextResponse.json({ ok: true, message: "Tin nhắn đã được gửi!" });
  } catch (error) {
    console.error("[contact] Error:", error);
    return NextResponse.json({ ok: false, error: "Lỗi server" }, { status: 500 });
  }
}

export async function GET() {
  return NextResponse.json({ ok: true, endpoint: "POST /api/contact" });
}
