// Email utility — sends email via Gmail SMTP using fetch API
// SMTP credentials: nhutcoderteam0902@gmail.com / app password: ekbc bnkv ovpc ajfu

import { createTransport } from "nodemailer";

const transporter = createTransport({
  service: "gmail",
  auth: {
    user: "nhutcoderteam0902@gmail.com",
    pass: "ekbc bnkv ovpc ajfu",
  },
});

export async function sendEmail(to: string, subject: string, html: string): Promise<boolean> {
  try {
    await transporter.sendMail({
      from: "NhutCoder Team <nhutcoderteam0902@gmail.com>",
      to,
      subject,
      html,
    });
    return true;
  } catch (e) {
    console.error("[email] Send failed:", e);
    return false;
  }
}

export function generateOTP(): string {
  return Math.floor(100000 + Math.random() * 900000).toString();
}

export async function sendOTPEmail(to: string, otp: string): Promise<boolean> {
  return sendEmail(
    to,
    "Mã xác thực NhutCoder Team",
    `<div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto; padding: 24px;">
      <h2 style="color: #84d44b;">NhutCoder Team</h2>
      <p>Xin chào,</p>
      <p>Mã xác thực (OTP) của bạn là:</p>
      <div style="font-size: 32px; font-weight: bold; letter-spacing: 8px; text-align: center; padding: 20px; background: #f0f0f0; border-radius: 12px; margin: 16px 0;">${otp}</div>
      <p>Mã này hết hạn sau 5 phút.</p>
      <p>Nếu bạn không yêu cầu mã này, vui lòng bỏ qua email.</p>
      <hr style="border: none; border-top: 1px solid #ddd; margin: 24px 0;">
      <p style="color: #888; font-size: 12px;">NhutCoder Team — nhutcoderteam0902@gmail.com</p>
    </div>`
  );
}

export async function sendPasswordResetEmail(to: string, resetLink: string): Promise<boolean> {
  return sendEmail(
    to,
    "Đặt lại mật khẩu — NhutCoder Team",
    `<div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto; padding: 24px;">
      <h2 style="color: #84d44b;">NhutCoder Team</h2>
      <p>Xin chào,</p>
      <p>Bạn đã yêu cầu đặt lại mật khẩu. Nhấn vào link bên dưới để đặt mật khẩu mới:</p>
      <a href="${resetLink}" style="display: inline-block; padding: 12px 32px; background: #84d44b; color: #0a0d14; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 16px 0;">Đặt lại mật khẩu</a>
      <p>Link này hết hạn sau 30 phút.</p>
      <p>Nếu bạn không yêu cầu, vui lòng bỏ qua email này.</p>
      <hr style="border: none; border-top: 1px solid #ddd; margin: 24px 0;">
      <p style="color: #888; font-size: 12px;">NhutCoder Team — nhutcoderteam0902@gmail.com</p>
    </div>`
  );
}
