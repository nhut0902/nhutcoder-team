import { NextResponse } from "next/server";
import { z } from "zod";
import { sendPasswordResetEmail } from "@/lib/email";

export const runtime = "nodejs";

const schema = z.object({ email: z.string().email() });

// Store reset tokens temporarily
const resetStore = new Map<string, { expires: number }>();
(globalThis as any).__resetStore = resetStore;

export async function POST(request: Request) {
  const body = await request.json().catch(() => ({}));
  const parsed = schema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json({ ok: false, error: "Email không hợp lệ" }, { status: 422 });
  }

  const { email } = parsed.data;

  // Generate reset link
  const resetToken = btoa(email + ":" + Date.now());
  const resetLink = `${process.env.NEXT_PUBLIC_SITE_URL || "https://nhutcoder-team.workers.dev"}/forgot-password?token=${resetToken}`;
  
  resetStore.set(resetToken, { expires: Date.now() + 30 * 60 * 1000 });

  // Send email
  const sent = await sendPasswordResetEmail(email, resetLink);
  if (!sent) {
    return NextResponse.json({ ok: false, error: "Không thể gửi email" }, { status: 500 });
  }

  return NextResponse.json({ ok: true, message: "Link đặt lại mật khẩu đã được gửi" });
}
