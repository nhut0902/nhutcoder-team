import { NextResponse } from "next/server";

export const runtime = "nodejs";

export async function POST(request: Request) {
  const body = await request.json().catch(() => ({}));
  const { email, otp } = body as { email?: string; otp?: string };

  if (!email || !otp) {
    return NextResponse.json({ ok: false, error: "Thiếu email hoặc OTP" }, { status: 422 });
  }

  // Get OTP from store
  const otpStore = (globalThis as any).__otpStore as Map<string, { otp: string; expires: number }> | undefined;
  if (!otpStore) {
    return NextResponse.json({ ok: false, error: "Phiên đã hết hạn. Vui lòng đăng ký lại." }, { status: 400 });
  }

  const stored = otpStore.get(email);
  if (!stored) {
    return NextResponse.json({ ok: false, error: "Không tìm thấy OTP. Vui lòng đăng ký lại." }, { status: 400 });
  }

  if (Date.now() > stored.expires) {
    otpStore.delete(email);
    return NextResponse.json({ ok: false, error: "OTP đã hết hạn. Vui lòng đăng ký lại." }, { status: 400 });
  }

  if (stored.otp !== otp) {
    return NextResponse.json({ ok: false, error: "OTP không đúng" }, { status: 400 });
  }

  // OTP verified — clean up
  otpStore.delete(email);

  // Generate token
  const token = btoa(JSON.stringify({ email, name: email.split("@")[0], verified: true, iat: Date.now() }));

  return NextResponse.json({ ok: true, token, user: { email, name: email.split("@")[0] } });
}
