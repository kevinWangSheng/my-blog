import { getCollection, type CollectionEntry } from 'astro:content';
import { sitePath } from './urls';

export type PublicCollection = 'projects' | 'notes' | 'logs' | 'essays' | 'links';
export type AnyEntry = CollectionEntry<PublicCollection>;

export function entrySlug(entry: { id: string }) {
  return entry.id.replace(/\.(md|mdx)$/i, '');
}

export function collectionPath(collection: PublicCollection) {
  return collection === 'links' ? sitePath('/links') : sitePath(`/${collection}`);
}

export function entryPath(collection: PublicCollection, entry: { id: string }) {
  if (collection === 'links') return sitePath('/links');
  return `${collectionPath(collection)}/${entrySlug(entry)}`;
}

export function formatDate(date: Date | string) {
  return new Intl.DateTimeFormat('en', { year: 'numeric', month: 'short', day: '2-digit' }).format(new Date(date));
}

export function byDateDesc<T extends { data: { date: Date } }>(items: T[]) {
  return [...items].sort((a, b) => +new Date(b.data.date) - +new Date(a.data.date));
}

export async function getPublicCollection<T extends PublicCollection>(collection: T) {
  const entries = await getCollection(collection, ({ data }) => data.visibility === 'public');
  return byDateDesc(entries);
}

export const collectionLabels: Record<PublicCollection, { title: string; eyebrow: string; description: string }> = {
  projects: {
    title: 'Projects',
    eyebrow: 'Capability evidence',
    description: '能看出系统设计、产品判断和实际构建能力的作品入口。'
  },
  notes: {
    title: 'Notes',
    eyebrow: 'Working memory',
    description: '短而密的阶段性判断,保留正在形成的想法和可复用的概念。'
  },
  logs: {
    title: 'Logs',
    eyebrow: 'Lab telemetry',
    description: '按周或阶段记录系统正在怎样变化,避免学习和项目只剩结果。'
  },
  essays: {
    title: 'Essays',
    eyebrow: 'Long-form synthesis',
    description: '更完整的文章,把学习、实验和判断收束成可以被别人阅读的表达。'
  },
  links: {
    title: 'Links',
    eyebrow: 'Source shelf',
    description: '值得反复返回的资料、工具和参考源,附带为什么收藏它。'
  }
};
