// Email + OTP utility — D1-based, no external dependencies
import { dbRun, dbQuery } from "@/lib/db";

export function generateOTP(): string {
  return Math.floor(100000 + Math.random() * 900000).toString();
}

export async function storeOTP(email: string, otp: string, type: string = "register"): Promise<void> {
  const expiresAt = new Date(Date.now() + 5 * 60 * 1000).toISOString();
  await dbRun(
    "INSERT INTO otp_codes (email, code, type, expires_at, used) VALUES (?, ?, ?, ?, 0)",
    [email, otp, type, expiresAt]
  );
}

export async function verifyOTPCode(email: string, code: string): Promise<boolean> {
  const now = new Date().toISOString();
  const rows = await dbQuery(
    "SELECT id FROM otp_codes WHERE email = ? AND code = ? AND used = 0 AND expires_at > ? ORDER BY id DESC LIMIT 1",
    [email, code, now]
  );
  if (rows.length === 0) return false;

  await dbRun("UPDATE otp_codes SET used = 1 WHERE id = ?", [rows[0].id]);
  return true;
}
