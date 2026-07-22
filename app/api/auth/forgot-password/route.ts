import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";
import { otpCodes } from "@/db/schema";
import { z } from "zod";
import { generateOTP } from "@/lib/email";

export const runtime = "edge";

const schema = z.object({ email: z.string().email() });

export async function POST(request: Request) {
  const body = await request.json().catch(() => ({}));
  const parsed = schema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json({ ok: false, error: "Email không hợp lệ" }, { status: 422 });
  }

  const { email } = parsed.data;

  // Generate reset code and store in D1
  const resetCode = generateOTP();
  try {
    const db = getDb();
    if (db) {
      const expiresAt = new Date(Date.now() + 30 * 60 * 1000).toISOString();
      await db.insert(otpCodes).values({
        email,
        code: resetCode,
        type: "reset",
        expiresAt,
      });
    }
  } catch (e) {
    console.error("[auth/forgot-password] D1 error:", e);
  }

  // TODO: Send email with reset link containing the code
  // For now: log it (in production use Resend/SendGrid)
  console.log(`[RESET] Email: ${email} | Code: ${resetCode}`);

  return NextResponse.json({
    ok: true,
    message: "Link đặt lại mật khẩu đã được gửi đến email của bạn",
    // For testing: return code in dev mode
    dev_code: process.env.NODE_ENV === "development" ? resetCode : undefined,
  });
}
