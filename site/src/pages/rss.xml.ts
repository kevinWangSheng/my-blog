import rss from '@astrojs/rss';
import { getPublicCollection, entryPath } from '../lib/content';

export async function GET(context: any) {
  const [essays, logs, notes] = await Promise.all([
    getPublicCollection('essays'), getPublicCollection('logs'), getPublicCollection('notes')
  ]);
  const items = [
    ...essays.map((entry) => ({ entry, collection: 'essays' as const })),
    ...logs.map((entry) => ({ entry, collection: 'logs' as const })),
    ...notes.map((entry) => ({ entry, collection: 'notes' as const }))
  ].sort((a, b) => +b.entry.data.date - +a.entry.data.date);

  return rss({
    title: 'Shawn AI Lab Manual',
    description: 'Learning systems, agent notes, projects, and essays from Shawn.',
    site: context.site,
    items: items.map(({ entry, collection }) => ({
      title: entry.data.title,
      description: entry.data.description,
      pubDate: entry.data.date,
      link: entryPath(collection, entry)
    }))
  });
}
