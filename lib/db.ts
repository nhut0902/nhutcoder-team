// Simple D1 database access — no Drizzle runtime needed
// Uses raw SQL via the D1 binding

interface D1Result {
  results?: Record<string, unknown>[];
  success: boolean;
  meta?: Record<string, unknown>;
}

function getD1(): D1Database | null {
  // On Cloudflare Workers, D1 is available via globalThis.env or process.env
  // OpenNext passes env bindings to process.env
  const env = (process.env as Record<string, unknown>).DB as D1Database | undefined;
  if (env) return env;

  // Try globalThis (some OpenNext versions)
  const globalEnv = (globalThis as Record<string, unknown>).env as { DB?: D1Database } | undefined;
  if (globalEnv?.DB) return globalEnv.DB;

  return null;
}

export async function dbQuery(sql: string, params: unknown[] = []): Promise<Record<string, unknown>[]> {
  const db = getD1();
  if (!db) {
    console.warn("[db] No D1 binding — returning empty results");
    return [];
  }
  try {
    const stmt = db.prepare(sql);
    const bound = params.length > 0 ? stmt.bind(...params) : stmt;
    const result = await bound.all() as D1Result;
    return result.results || [];
  } catch (e) {
    console.error("[db] Query error:", e, "SQL:", sql);
    return [];
  }
}

export async function dbRun(sql: string, params: unknown[] = []): Promise<boolean> {
  const db = getD1();
  if (!db) {
    console.warn("[db] No D1 binding — skipping write");
    return false;
  }
  try {
    const stmt = db.prepare(sql);
    const bound = params.length > 0 ? stmt.bind(...params) : stmt;
    await bound.run();
    return true;
  } catch (e) {
    console.error("[db] Run error:", e, "SQL:", sql);
    return false;
  }
}

export function hasDb(): boolean {
  return getD1() !== null;
}
