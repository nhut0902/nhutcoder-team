import { drizzle } from "drizzle-orm/d1";
import * as schema from "@/db/schema";

type DB = ReturnType<typeof drizzle<typeof schema>>;

let _db: DB | null = null;

export function getDb(env?: { DB: D1Database }): DB | null {
  if (_db) return _db;
  const binding = (env?.DB ?? (process.env as Record<string, unknown>).DB) as D1Database | undefined;
  if (!binding) {
    console.warn("[db] No D1 binding found — running without database");
    return null;
  }
  _db = drizzle(binding, { schema });
  return _db;
}
