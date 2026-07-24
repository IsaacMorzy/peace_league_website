import type { APIRoute } from 'astro';
import events from '../lib/events-data.json';
import causes from '../lib/causes-data.json';
import blogs from '../lib/blog-data.json';
// Award categories live in the backend fixtures; the frontend build imports them
// at build-time so the index is fully static (no runtime API cost).
import awardCategories from '../../../peace_league_website/fixtures/award_categories.json';

type SearchType = 'event' | 'cause' | 'blog' | 'category';

const URL_BY_TYPE: Record<SearchType, (slug: string) => string> = {
  event: (slug) => `/events/${slug}/`,
  cause: (slug) => `/causes/${slug}/`,
  blog: (slug) => `/blog/${slug}/`,
  category: (slug) => `/awards/category/${slug}/`,
};

function stripHtml(s: string): string {
  return s.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
}

function clampDescription(s: string): string {
  if (s.length <= 280) return s;
  const cut = s.slice(0, 280);
  const lastSpace = cut.lastIndexOf(' ');
  return lastSpace > 200 ? cut.slice(0, lastSpace) : cut;
}

function normalize(item: any, type: SearchType) {
  const slug = String(item.slug ?? '').trim();
  if (!slug) return null;
  const title = String(
    item.title ?? item.name ?? item.category_name ?? ''
  ).trim();
  if (!title) return null;
  const description = clampDescription(stripHtml(item.description ?? ''));
  return {
    id: `${type}-${slug}`,
    type,
    title,
    description,
    url: URL_BY_TYPE[type](slug),
  };
}

export const GET: APIRoute = async () => {
  const documents = [
    ...((events as any[]).map((e) => normalize(e, 'event'))),
    ...((causes as any[]).map((c) => normalize(c, 'cause'))),
    ...((blogs as any[]).map((b) => normalize(b, 'blog'))),
    ...((awardCategories as any[]).map((cat) => normalize(cat, 'category'))),
  ].filter((d): d is NonNullable<typeof d> => d !== null);

  return new Response(JSON.stringify({ documents }), {
    headers: { 'Content-Type': 'application/json' },
  });
};
