"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { Mail, ArrowRight } from "lucide-react";
import Link from "next/link";
import { PageTransition } from "@/components/page-transition";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    await new Promise(r => setTimeout(r, 1000));
    setSent(true);
    setLoading(false);
  };

  return (
    <PageTransition>
      <div className="min-h-screen flex items-center justify-center px-4 pt-24 pb-12">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-md bg-[var(--surface)] border border-[var(--border)] rounded-2xl p-8">
          <h1 className="text-2xl font-bold mb-6 text-center">Reset Password</h1>
          {sent ? (
            <div className="text-center">
              <p className="text-[var(--text-muted)] mb-4">If an account exists for {email}, you&apos;ll receive a reset link shortly.</p>
              <Link href="/login" className="text-[var(--accent)] hover:underline text-sm">Back to login</Link>
            </div>
          ) : (
            <>
              <p className="text-sm text-[var(--text-muted)] mb-6">Enter your email and we&apos;ll send you a reset link.</p>
              <form onSubmit={handleSubmit} className="space-y-4">
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
                  {loading ? "Sending..." : <>Send Reset Link <ArrowRight className="w-4 h-4" /></>}
                </button>
              </form>
              <div className="mt-6 text-center text-sm">
                <Link href="/login" className="text-[var(--text-muted)] hover:text-[var(--accent)]">Back to login</Link>
              </div>
            </>
          )}
        </motion.div>
      </div>
    </PageTransition>
  );
}
