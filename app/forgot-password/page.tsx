"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { Mail, ArrowRight, KeyRound } from "lucide-react";
import Link from "next/link";
import { PageTransition } from "@/components/page-transition";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const [resetMode, setResetMode] = useState(false);
  const [error, setError] = useState("");

  const handleSendReset = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/auth/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      const data: { ok: boolean; error?: string } = await res.json();
      if (!res.ok) throw new Error(data.error || "Gửi email thất bại");
      setSent(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Gửi email thất bại");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/auth/reset-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, newPassword }),
      });
      const data: { ok: boolean; error?: string } = await res.json();
      if (!res.ok) throw new Error(data.error || "Đặt lại thất bại");
      window.location.href = "/login";
    } catch (err) {
      setError(err instanceof Error ? err.message : "Đặt lại thất bại");
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageTransition>
      <div className="min-h-screen flex items-center justify-center px-4 pt-24 pb-12">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-md bg-[var(--surface)] border border-[var(--border)] rounded-2xl p-8">
          <h1 className="text-2xl font-bold mb-6 text-center">Quên mật khẩu</h1>
          {error && <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-sm text-red-400">{error}</div>}
          {sent && !resetMode ? (
            <div className="text-center">
              <p className="text-[var(--text-muted)] mb-4">Link đặt lại mật khẩu đã được gửi đến <strong>{email}</strong>. Kiểm tra hộp thư (và thư rác).</p>
              <button onClick={() => setResetMode(true)} className="text-[var(--accent)] hover:underline text-sm">Tôi đã nhận link — đặt mật khẩu mới</button>
            </div>
          ) : resetMode ? (
            <>
              <p className="text-sm text-[var(--text-muted)] mb-6">Nhập mật khẩu mới cho <strong>{email}</strong></p>
              <form onSubmit={handleReset} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1.5">Mật khẩu mới</label>
                  <div className="relative">
                    <KeyRound className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--text-muted)]" />
                    <input type="password" required minLength={6} value={newPassword} onChange={e => setNewPassword(e.target.value)}
                      className="w-full pl-10 pr-4 py-2.5 bg-[var(--bg)] border border-[var(--border)] rounded-lg text-sm focus:outline-none focus:border-[var(--accent)]" />
                  </div>
                </div>
                <button type="submit" disabled={loading}
                  className="w-full py-2.5 bg-[var(--accent)] text-[var(--bg)] rounded-lg font-medium text-sm flex items-center justify-center gap-2 hover:opacity-90 transition-opacity disabled:opacity-50">
                  {loading ? "Đang đặt lại..." : <>Đặt mật khẩu mới <ArrowRight className="w-4 h-4" /></>}
                </button>
              </form>
            </>
          ) : (
            <>
              <p className="text-sm text-[var(--text-muted)] mb-6">Nhập email, chúng tôi sẽ gửi link đặt lại mật khẩu.</p>
              <form onSubmit={handleSendReset} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1.5">Email</label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--text-muted)]" />
                    <input type="email" required value={email} onChange={e => setEmail(e.target.value)}
                      className="w-full pl-10 pr-4 py-2.5 bg-[var(--bg)] border border-[var(--border)] rounded-lg text-sm focus:outline-none focus:border-[var(--accent)]" />
                  </div>
                </div>
                <button type="submit" disabled={loading}
                  className="w-full py-2.5 bg-[var(--accent)] text-[var(--bg)] rounded-lg font-medium text-sm flex items-center justify-center gap-2 hover:opacity-90 transition-opacity disabled:opacity-50">
                  {loading ? "Đang gửi..." : <>Gửi link đặt lại <ArrowRight className="w-4 h-4" /></>}
                </button>
              </form>
            </>
          )}
          <div className="mt-6 text-center text-sm">
            <Link href="/login" className="text-[var(--text-muted)] hover:text-[var(--accent)]">← Quay lại đăng nhập</Link>
          </div>
        </motion.div>
      </div>
    </PageTransition>
  );
}
