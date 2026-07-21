import { NextResponse } from "next/server";
import { uploadImage } from "@/lib/r2";
import { getDb } from "@/lib/db";
import { images } from "@/db/schema";

export const runtime = "edge";

export async function POST(request: Request) {
  const formData = await request.formData();
  const file = formData.get("file") as File | null;

  if (!file) {
    return NextResponse.json({ ok: false, error: "No file provided" }, { status: 400 });
  }

  if (file.size > 10 * 1024 * 1024) {
    return NextResponse.json({ ok: false, error: "File too large (max 10MB)" }, { status: 413 });
  }

  const result = await uploadImage(file, process.env as any);
  if (!result) {
    return NextResponse.json({ ok: false, error: "R2 not configured" }, { status: 500 });
  }

  // Store metadata in D1
  try {
    const db = getDb();
    if (db) {
      await db.insert(images).values({
        filename: result.filename,
        r2Key: result.key,
        url: result.url,
        mimeType: result.mimeType,
        size: result.size,
      });
    }
  } catch (e) {
    console.error("[upload] D1 metadata insert failed:", e);
  }

  return NextResponse.json({ ok: true, ...result });
}
