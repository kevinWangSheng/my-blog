import { getPublicCollection, entryPath } from '../lib/content';

const staticRoutes = ['/', '/about', '/projects', '/notes', '/logs', '/essays', '/links', '/rss.xml'];

export async function GET({ site }: { site: URL }) {
  const collections = ['projects', 'notes', 'logs', 'essays'] as const;
  const dynamicRoutes = (await Promise.all(collections.map(async (collection) => {
    const entries = await getPublicCollection(collection);
    return entries.map((entry) => entryPath(collection, entry));
  }))).flat();
  const urls = [...staticRoutes, ...dynamicRoutes].map((path) => `<url><loc>${new URL(path, site).toString()}</loc></url>`).join('');
  return new Response(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${urls}</urlset>`, {
    headers: { 'Content-Type': 'application/xml' }
  });
}
