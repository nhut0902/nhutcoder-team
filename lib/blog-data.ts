// Blog post data — stored locally

export interface BlogPost {
  slug: string;
  title: string;
  excerpt: string;
  content: string;
  category: string;
  tags: string[];
  date: string;
  readingTime: number;
  featured: boolean;
}

export const BLOG_POSTS: BlogPost[] = [];

export const BLOG_CATEGORIES = ["Tất cả", "Thiết kế", "Hướng dẫn", "Phát triển", "Game"];

export function getFeaturedPosts(): BlogPost[] {
  return BLOG_POSTS.filter(p => p.featured);
}

export function getPostBySlug(slug: string): BlogPost | undefined {
  return BLOG_POSTS.find(p => p.slug === slug);
}

export function getPostsByCategory(category: string): BlogPost[] {
  if (category === "Tất cả") return BLOG_POSTS;
  return BLOG_POSTS.filter(p => p.category === category);
}

export function searchPosts(query: string): BlogPost[] {
  const q = query.toLowerCase();
  return BLOG_POSTS.filter(p =>
    p.title.toLowerCase().includes(q) ||
    p.excerpt.toLowerCase().includes(q) ||
    p.tags.some(t => t.toLowerCase().includes(q))
  );
}

export function getRelatedPosts(slug: string, limit = 3): BlogPost[] {
  const post = getPostBySlug(slug);
  if (!post) return [];
  return BLOG_POSTS
    .filter(p => p.slug !== slug && p.category === post.category)
    .slice(0, limit);
}
