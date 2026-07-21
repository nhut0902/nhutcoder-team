import { notFound } from "next/navigation";
import { BLOG_POSTS, getPostBySlug, getRelatedPosts } from "@/lib/blog-data";
import { BlogPostClient } from "./blog-post-client";

export function generateStaticParams() {
  return BLOG_POSTS.map(p => ({ slug: p.slug }));
}

export default function BlogPostPage({ params }: { params: { slug: string } }) {
  const post = getPostBySlug(params.slug);
  if (!post) notFound();
  const related = getRelatedPosts(params.slug);
  return <BlogPostClient post={post} related={related} />;
}
