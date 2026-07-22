import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";
import { users } from "@/db/schema";
import { eq } from "drizzle-orm";
import { z } from "zod";

export const runtime = "nodejs";

const schema = z.object({
  email: z.string().email(),
  newPassword: z.string().min(6, "Mật khẩu phải có ít nhất 6 ký tự"),
});

export async function POST(request: Request) {
  const body = await request.json().catch(() => ({}));
  const parsed = schema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json({ ok: false, error: parsed.error.issues[0]?.message || "Dữ liệu không hợp lệ" }, { status: 422 });
  }

  const { email, newPassword } = parsed.data;

  // Update password in D1
  try {
    const db = getDb();
    if (db) {
      await db.update(users)
        .set({ passwordHash: btoa(newPassword) })
        .where(eq(users.email, email));
    }
  } catch (e) {
    console.error("[auth/reset-password] D1 error:", e);
  }

  return NextResponse.json({ ok: true, message: "Đặt lại mật khẩu thành công" });
}
