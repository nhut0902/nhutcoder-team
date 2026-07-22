import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";
import { users } from "@/db/schema";
import { eq } from "drizzle-orm";
import { z } from "zod";
import { generateOTP, sendOTPEmail } from "@/lib/email";

export const runtime = "edge";

const schema = z.object({
  name: z.string().min(2, "Tên phải có ít nhất 2 ký tự"),
  email: z.string().email("Email không hợp lệ"),
  password: z.string().min(6, "Mật khẩu phải có ít nhất 6 ký tự"),
});

export async function POST(request: Request) {
  const body = await request.json().catch(() => ({}));
  const parsed = schema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json(
      { ok: false, error: parsed.error.issues[0]?.message || "Dữ liệu không hợp lệ" },
      { status: 422 }
    );
  }

  const { name, email, password } = parsed.data;

  // Check if user already exists in D1
  try {
    const db = getDb();
    if (db) {
      const existing = await db.select().from(users).where(eq(users.email, email)).limit(1);
      if (existing.length > 0) {
        return NextResponse.json(
          { ok: false, error: "Email đã được đăng ký. Vui lòng đăng nhập." },
          { status: 409 }
        );
      }
    }
  } catch (e) {
    console.error("[auth/register] D1 check error:", e);
  }

  // Generate + store OTP
  const otp = generateOTP();
  await sendOTPEmail(email, otp);

  // Save user to D1 (pending verification)
  try {
    const db = getDb();
    if (db) {
      await db.insert(users).values({
        name,
        email,
        passwordHash: btoa(password),
        verified: false,
      }).onConflictDoNothing();
    }
  } catch (e) {
    console.error("[auth/register] D1 insert error:", e);
  }

  return NextResponse.json({
    ok: true,
    message: "OTP đã được gửi đến email của bạn. Kiểm tra hộp thư (và thư rác).",
    // For testing: return OTP in dev mode (remove in production)
    dev_otp: process.env.NODE_ENV === "development" ? otp : undefined,
  });
}
