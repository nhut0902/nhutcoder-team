import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";
import { users } from "@/db/schema";
import { z } from "zod";
import { generateOTP, sendOTPEmail } from "@/lib/email";

export const runtime = "nodejs"; // nodemailer needs Node.js runtime

const schema = z.object({
  name: z.string().min(2, "Tên phải có ít nhất 2 ký tự"),
  email: z.string().email("Email không hợp lệ"),
  password: z.string().min(6, "Mật khẩu phải có ít nhất 6 ký tự"),
});

// Store OTPs temporarily (in production: use KV or D1)
const otpStore = new Map<string, { otp: string; expires: number }>();

export async function POST(request: Request) {
  const body = await request.json().catch(() => ({}));
  const parsed = schema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json({ ok: false, error: parsed.error.issues[0]?.message || "Dữ liệu không hợp lệ" }, { status: 422 });
  }

  const { name, email, password } = parsed.data;

  // Generate OTP
  const otp = generateOTP();
  otpStore.set(email, { otp, expires: Date.now() + 5 * 60 * 1000 });

  // Send OTP email
  const sent = await sendOTPEmail(email, otp);
  if (!sent) {
    return NextResponse.json({ ok: false, error: "Không thể gửi email. Vui lòng thử lại." }, { status: 500 });
  }

  // Save user to D1 (pending verification)
  try {
    const db = getDb();
    if (db) {
      await db.insert(users).values({
        name,
        email,
        passwordHash: btoa(password),
      }).onConflictDoNothing();
    }
  } catch (e) {
    console.error("[auth/register] D1 error:", e);
  }

  // Store OTP in global for verify-otp route
  (globalThis as any).__otpStore = otpStore;

  return NextResponse.json({ ok: true, message: "OTP đã được gửi đến email của bạn" });
}

export { otpStore };
