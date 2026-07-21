/**
 * Cloudflare R2 image upload utility.
 * Usage in API routes:
 *   const { url, key } = await uploadImage(file, env);
 */

export interface R2Env {
  R2: R2Bucket;
}

export interface UploadResult {
  url: string;
  key: string;
  filename: string;
  mimeType: string;
  size: number;
}

export async function uploadImage(
  file: File,
  env: R2Env,
  prefix = "uploads"
): Promise<UploadResult | null> {
  const bucket = (env.R2 ?? (process.env as any).R2) as R2Bucket | undefined;
  if (!bucket) {
    console.warn("[r2] No R2 binding found");
    return null;
  }

  const ext = file.name.split(".").pop() || "bin";
  const key = `${prefix}/${Date.now()}-${Math.random().toString(36).slice(2, 8)}.${ext}`;
  const arrayBuffer = await file.arrayBuffer();

  await bucket.put(key, arrayBuffer, {
    httpMetadata: { contentType: file.type },
  });

  // Public URL via R2 custom domain or Cloudflare Pages
  const publicUrl = process.env.NEXT_PUBLIC_R2_PUBLIC_URL || "";
  const url = publicUrl ? `${publicUrl}/${key}` : `/api/images/${key}`;

  return {
    url,
    key,
    filename: file.name,
    mimeType: file.type,
    size: file.size,
  };
}

export async function getImage(key: string, env: R2Env): Promise<{ body: ReadableStream; contentType: string } | null> {
  const bucket = (env.R2 ?? (process.env as any).R2) as R2Bucket | undefined;
  if (!bucket) return null;

  const object = await bucket.get(key);
  if (!object) return null;

  return {
    body: object.body,
    contentType: object.httpMetadata?.contentType || "application/octet-stream",
  };
}

export async function deleteImage(key: string, env: R2Env): Promise<boolean> {
  const bucket = (env.R2 ?? (process.env as any).R2) as R2Bucket | undefined;
  if (!bucket) return false;
  await bucket.delete(key);
  return true;
}
