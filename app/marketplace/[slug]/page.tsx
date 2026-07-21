import { notFound } from "next/navigation";
import { PRODUCTS, getProductBySlug } from "@/lib/marketplace-data";
import { ProductDetailClient } from "./product-detail-client";

export function generateStaticParams() {
  return PRODUCTS.map(p => ({ slug: p.slug }));
}

export default function ProductDetailPage({ params }: { params: { slug: string } }) {
  const product = getProductBySlug(params.slug);
  if (!product) notFound();
  return <ProductDetailClient product={product} />;
}
