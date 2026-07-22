"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { Mail, Lock, User, ArrowRight, KeyRound } from "lucide-react";
import Link from "next/link";
import { PageTransition } from "@/components/page-transition";

export default function RegisterPage() {
  const [step, setStep] = useState<"register" | "otp">("register");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });
      const data: { ok: boolean; error?: string; message?: string } = await res.json();
      if (!res.ok) throw new Error(data.error || "Đăng ký thất bại");
      setStep("otp");
      setSuccess("Mã OTP đã được gửi đến email của bạn!");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Đăng ký thất bại");
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOTP = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/auth/verify-otp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, otp }),
      });
      const data: { ok: boolean; error?: string; token?: string } = await res.json();
      if (!res.ok) throw new Error(data.error || "Xác thực thất bại");
      if (data.token) localStorage.setItem("token", data.token);
      window.location.href = "/dashboard";
    } catch (err) {
      setError(err instanceof Error ? err.message : "Xác thực thất bại");
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageTransition>
      <div className="min-h-screen flex items-center justify-center px-4 pt-24 pb-12">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-md bg-[var(--surface)] border border-[var(--border)] rounded-2xl p-8">
          {step === "register" ? (
            <>
              <h1 className="text-2xl font-bold mb-2 text-center">Tạo tài khoản</h1>
              <p className="text-sm text-[var(--text-muted)] mb-6 text-center">Đăng ký để mua code và lưu bài viết yêu thích</p>
              {error && <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-sm text-red-400">{error}</div>}
              <form onSubmit={handleRegister} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1.5">Họ tên</label>
                  <div className="relative">
                    <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--text-muted)]" />
                    <input type="text" required value={name} onChange={e => setName(e.target.value)}
                      className="w-full pl-10 pr-4 py-2.5 bg-[var(--bg)] border border-[var(--border)] rounded-lg text-sm focus:outline-none focus:border-[var(--accent)]" />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1.5">Email</label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--text-muted)]" />
                    <input type="email" required value={email} onChange={e => setEmail(e.target.value)}
                      className="w-full pl-10 pr-4 py-2.5 bg-[var(--bg)] border border-[var(--border)] rounded-lg text-sm focus:outline-none focus:border-[var(--accent)]" />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1.5">Mật khẩu</label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--text-muted)]" />
                    <input type="password" required minLength={6} value={password} onChange={e => setPassword(e.target.value)}
                      className="w-full pl-10 pr-4 py-2.5 bg-[var(--bg)] border border-[var(--border)] rounded-lg text-sm focus:outline-none focus:border-[var(--accent)]" />
                  </div>
                </div>
                <button type="submit" disabled={loading}
                  className="w-full py-2.5 bg-[var(--accent)] text-[var(--bg)] rounded-lg font-medium text-sm flex items-center justify-center gap-2 hover:opacity-90 transition-opacity disabled:opacity-50">
                  {loading ? "Đang gửi OTP..." : <>Đăng ký <ArrowRight className="w-4 h-4" /></>}
                </button>
              </form>
              <div className="mt-6 text-center text-sm text-[var(--text-muted)]">
                Đã có tài khoản? <Link href="/login" className="text-[var(--accent)] hover:underline">Đăng nhập</Link>
              </div>
            </>
          ) : (
            <>
              <h1 className="text-2xl font-bold mb-2 text-center">Xác thực OTP</h1>
              {success && <div className="mb-4 p-3 bg-green-500/10 border border-green-500/30 rounded-lg text-sm text-green-400">{success}</div>}
              {error && <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-sm text-red-400">{error}</div>}
              <form onSubmit={handleVerifyOTP} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1.5">Mã OTP (6 số)</label>
                  <div className="relative">
                    <KeyRound className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--text-muted)]" />
                    <input type="text" required maxLength={6} value={otp} onChange={e => setOtp(e.target.value.replace(/\D/g, ""))}
                      className="w-full pl-10 pr-4 py-2.5 bg-[var(--bg)] border border-[var(--border)] rounded-lg text-sm focus:outline-none focus:border-[var(--accent)] tracking-widest text-center text-lg"
                      placeholder="000000" />
                  </div>
                </div>
                <button type="submit" disabled={loading}
                  className="w-full py-2.5 bg-[var(--accent)] text-[var(--bg)] rounded-lg font-medium text-sm flex items-center justify-center gap-2 hover:opacity-90 transition-opacity disabled:opacity-50">
                  {loading ? "Đang xác thực..." : <>Xác thực</>}
                </button>
              </form>
              <button onClick={() => setStep("register")} className="mt-4 w-full text-center text-sm text-[var(--text-muted)] hover:text-[var(--accent)]">
                ← Quay lại
              </button>
            </>
          )}
        </motion.div>
      </div>
    </PageTransition>
  );
}
