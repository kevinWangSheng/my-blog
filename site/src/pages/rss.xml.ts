import rss from '@astrojs/rss';
import { getPublicCollection, entryPath } from '../lib/content';
import { sitePath } from '../lib/urls';

export async function GET(context: any) {
  const [essays, notes] = await Promise.all([
    getPublicCollection('essays'), getPublicCollection('notes')
  ]);
  const items = [
    ...essays.map((entry) => ({ entry, collection: 'essays' as const })),
    ...notes.map((entry) => ({ entry, collection: 'notes' as const }))
  ].sort((a, b) => +b.entry.data.date - +a.entry.data.date);

  return rss({
    title: 'Shawn Field Notes',
    description: 'Learning systems, agent notes, projects, and essays from Shawn.',
    site: new URL(sitePath('/'), context.site).toString(),
    items: items.map(({ entry, collection }) => ({
      title: entry.data.title,
      description: entry.data.description,
      pubDate: entry.data.date,
      link: entryPath(collection, entry)
    }))
  });
}
